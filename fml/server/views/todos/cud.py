import copy
import datetime
import typing as t
from abc import abstractmethod

from sqlalchemy import exists
from sqlalchemy.orm import joinedload, Query

from flask import request, Blueprint
from flask.views import View
from flask_api import status
from flask_api.request import APIRequest

from hardcandy import fields
from hardcandy.schema import DeserializationError, Field

from fml.server import models
from fml.server import schemas
from fml.server.retrieve import (
    get_todo_for_project_and_identifier,
    get_project_and_minimum_priority,
)
from fml.server.schemas import ToDoSchema
from fml.server.session import SessionContainer as SC
from fml.server.views.utils import inject_schema, with_errors


todo_cud_views = Blueprint("todo_crud_views", __name__)
request: APIRequest


@todo_cud_views.route("/todo/", methods=["POST"])
@with_errors
def create_todo():
    schema = ToDoSchema()

    try:
        todo_data = schema.deserialize_raw(request.data)
        create_data = schemas.CreateTodoSchema().deserialize_raw(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    project = models.Project.get_for_identifier_or_raise(
        SC.session,
        create_data.get("project"),
        schemas.ProjectSchema(),
    )
    todo_data["project_id"] = project.id

    priority = models.Priority.get_for_identifier_or_raise(
        session=SC.session,
        identifier=create_data.get("priority"),
        schema=schemas.PrioritySchema(),
        base_query=SC.session.query(models.Priority).filter(
            models.Priority.project_id == project.id
        ),
    )

    todo_data["priority_id"] = priority.id

    todo = models.ToDo(**todo_data)

    for tag in create_data["tags"]:
        todo.tags.append(
            models.Tag.get_for_identifier_or_raise(
                SC.session,
                tag,
                schemas.TagSchema(),
            )
        )

    for parent in create_data["parents"]:
        parent = get_todo_for_project_and_identifier(SC.session, parent, project)
        todo.parents.append(parent)

    SC.session.add(todo)

    SC.session.commit()

    return schema.serialize(todo)


@todo_cud_views.route("/todo/description/", methods=["PATCH"])
@with_errors
@inject_schema(schemas.ModifyToDoSchema(), use_args=False)
def modify_todo_description(
    target: t.Union[int, str], project: models.Project, description: str
):
    todo = get_todo_for_project_and_identifier(SC.session, target, project)
    todo.text = description
    SC.session.commit()
    return schemas.ToDoSchema().serialize(todo)


class ModifyTodo(View):
    _RECURSIVE: bool = True

    def _modify_todo(self, todo: models.ToDo) -> None:
        pass

    @with_errors
    @inject_schema(schemas.UpdateTodoSchema(), use_args=False)
    def dispatch_request(self, target: t.Union[int, str], project: models.Project):
        todo = get_todo_for_project_and_identifier(SC.session, target, project)

        self._modify_todo(todo)

        if self._RECURSIVE:
            for child in todo.traverse_children(active_only=False):
                self._modify_todo(child)

        SC.session.commit()

        return ToDoSchema().serialize(todo)


class CancelTodo(ModifyTodo):
    def _modify_todo(self, todo: models.ToDo) -> None:
        todo.state = models.State.CANCELED
        todo.finished_at = datetime.datetime.now()


todo_cud_views.add_url_rule(
    "/todo/cancel/", methods=["PATCH"], view_func=CancelTodo.as_view("cancel_todo")
)


class ToggleWaitingTodo(ModifyTodo):
    _RECURSIVE: bool = False

    def _modify_todo(self, todo: models.ToDo) -> None:
        todo.state = (
            models.State.WAITING
            if todo.state == models.State.PENDING
            else models.State.PENDING
        )


todo_cud_views.add_url_rule(
    "/todo/toggle-wait/",
    methods=["PATCH"],
    view_func=ToggleWaitingTodo.as_view("toggle_wait_todo"),
)


class FinishTodo(ModifyTodo):
    def _modify_todo(self, todo: models.ToDo) -> None:
        todo.state = models.State.COMPLETED
        todo.finished_at = datetime.datetime.now()


todo_cud_views.add_url_rule(
    "/todo/finish/", methods=["PATCH"], view_func=FinishTodo.as_view("finish_todo")
)


@todo_cud_views.route("/todo/single/", methods=["GET"])
@with_errors
@inject_schema(schemas.UpdateTodoSchema())
def get_todo(target: t.Union[int, str], project: models.Project):
    return ToDoSchema().serialize(
        get_todo_for_project_and_identifier(SC.session, target, project)
    )


class BaseToDoList(View):
    _order_by_map = {
        "created_at": models.ToDo.created_at.desc(),
        "finished_at": models.ToDo.finished_at.desc(),
        "state": models.ToDo.state,
        "priority": models.Priority.level,
        "project": models.Project.created_at,
    }

    @abstractmethod
    def get_base_query(self) -> Query:
        pass

    @abstractmethod
    def get_schema_fields(self) -> t.Mapping[str, Field]:
        pass

    def limit(self, query: Query, limit: int) -> Query:
        return query

    def order_todos(self, query: Query) -> Query:
        return query.order_by(models.ToDo.created_at.desc())

    @with_errors
    @inject_schema(schemas.ToDoListOptions(), use_args=False)
    def dispatch_request(
        self,
        project: t.Union[str, int, None],
        tag: t.Optional[models.Tag],
        query: t.Optional[str],
        all_tasks: bool,
        flat: bool,
        limit: int,
        minimum_priority: t.Union[int, str, None],
        ignore_priority: bool,
        state: t.Optional[models.State],
        order_by: t.Optional[t.List[str]],
    ):
        project, level = get_project_and_minimum_priority(
            SC.session, project, minimum_priority, ignore_priority
        )

        todos = (
            self.get_base_query()
            .options(
                joinedload(models.ToDo.tags),
                joinedload(models.ToDo.children),
                joinedload(models.ToDo.comments),
            )
            .join(models.Priority)
        )

        if order_by:
            todos = todos.order_by(*(self._order_by_map[s] for s in order_by))
        else:
            todos = self.order_todos(todos)

        if project is not None:
            todos = todos.filter(models.ToDo.project_id == project.id)

        if level is not None:
            todos = todos.filter(models.Priority.level <= level)

        if state is not None:
            todos = todos.filter(models.ToDo.state == state)

        if not all_tasks:
            todos = todos.filter(
                ~exists().where(models.Dependency.child_id == models.ToDo.id),
            )

        if query:
            todos = todos.filter(models.ToDo.text.contains(query))

        if tag is not None:
            todos = todos.join(models.Tagged).filter(models.Tagged.tag_id == tag.id)

        todos = self.limit(todos, limit)

        schema = schemas.ToDoSchema(fields=self.get_schema_fields())

        if flat:
            schema.fields = copy.copy(schema.fields)
            del schema.fields["children"]

        return {"todos": [schema.serialize(todo) for todo in todos]}


class ToDoHistory(BaseToDoList):
    def get_schema_fields(self) -> t.Mapping[str, Field]:
        return {"children": fields.List(fields.SelfRelated(), read_only=True)}

    def get_base_query(self) -> Query:
        return SC.session.query(models.ToDo)

    def limit(self, query: Query, limit: int) -> Query:
        return query.limit(limit)


todo_cud_views.add_url_rule(
    "/todo/history/", methods=["GET"], view_func=ToDoHistory.as_view("todo_history")
)


class ToDoList(BaseToDoList):
    def get_schema_fields(self) -> t.Mapping[str, Field]:
        return {}

    def get_base_query(self) -> Query:
        return models.ToDo.active_todos(SC.session)

    def order_todos(self, query: Query) -> Query:
        return query.order_by(
            models.ToDo.state,
            models.Priority.level,
            models.ToDo.created_at.desc(),
        )


todo_cud_views.add_url_rule(
    "/todo/", methods=["GET"], view_func=ToDoList.as_view("todo_list")
)

import copy
import datetime
import typing as t
from abc import abstractmethod

from sqlalchemy import exists
from sqlalchemy.orm import joinedload, Query
from sqlalchemy.orm.exc import MultipleResultsFound

from flask import request, Blueprint
from flask.views import View
from flask_api import status
from flask_api.request import APIRequest

from hardcandy import fields
from hardcandy.schema import DeserializationError, Field

from fml.server import models
from fml.server import schemas
from fml.server.schemas import ToDoSchema
from fml.server.session import SessionContainer as SC
from fml.server.views.utils import inject_schema


todo_cud_views = Blueprint('todo_crud_views', __name__)
request: APIRequest


@todo_cud_views.route('/todo/', methods = ['POST'])
def create_todo():
    schema = ToDoSchema()

    try:
        todo_data = schema.deserialize_raw(request.data)
        create_data = schemas.CreateTodoSchema().deserialize_raw(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    project = create_data.get('project')

    if not project:
        todo_data['project_id'] = SC.session.query(models.Project.id).filter(models.Project.is_default == True).scalar()
    else:
        if isinstance(project, int):
            _project = SC.session.query(models.Project.id).get(project)
        else:
            try:
                _project = SC.session.query(models.Project.id).filter(
                    models.Project.name.contains(project)
                ).scalar()
            except MultipleResultsFound:
                return 'ambiguous project "{}"'.format(project), status.HTTP_400_BAD_REQUEST

            if _project is None:
                return 'unknown project "{}"'.format(project), status.HTTP_400_BAD_REQUEST

            todo_data['project_id'] = _project

    priority_id = models.Priority.get_for_identifier(
        session = SC.session,
        identifier = create_data.get('priority'),
        base_query = SC.session.query(models.Priority.id).filter(models.Priority.project_id == todo_data['project_id'])
    )

    if priority_id is None:
        return 'invalid priority', status.HTTP_400_BAD_REQUEST

    todo_data['priority_id'] = priority_id

    todo = models.ToDo(**todo_data)

    for tag in create_data['tags']:
        if isinstance(tag, int):
            _tag = SC.session.query(models.Tag).get(tag)
        else:
            try:
                _tag = SC.session.query(models.Tag).filter(
                    models.Tag.name.contains(tag)
                ).scalar()
            except MultipleResultsFound:
                return 'ambiguous tag "{}"'.format(tag), status.HTTP_400_BAD_REQUEST

        if _tag is None:
            return 'unknown tag "{}"'.format(tag), status.HTTP_400_BAD_REQUEST

        todo.tags.append(_tag)

    for parent in create_data['parents']:
        parent = models.ToDo.get_for_identifier(SC.session, parent, base_query = models.ToDo.active_todos(SC.session))
        if parent is None:
            return 'Invalid parent', status.HTTP_400_BAD_REQUEST

        todo.parents.append(parent)

    SC.session.add(todo)

    SC.session.commit()

    return schema.serialize(todo)


class ModifyTodo(View):

    def _modify_todo(self, todo: models.ToDo) -> None:
        pass

    def dispatch_request(self):
        target = request.data.get('target')

        if target is None:
            return 'no target', status.HTTP_400_BAD_REQUEST

        try:
            target = int(target)
        except ValueError:
            try:
                todo: t.Optional[models.ToDo] = models.ToDo.active_todos(SC.session).filter(
                    models.ToDo.text.contains(target)
                ).scalar()
            except MultipleResultsFound:
                return 'ambiguous target', status.HTTP_400_BAD_REQUEST

        else:
            todo: t.Optional[models.ToDo] = models.ToDo.active_todos(SC.session).filter(
                models.ToDo.id == target).scalar()

        if todo is None:
            return 'no such todo', status.HTTP_404_NOT_FOUND

        self._modify_todo(todo)

        for child in todo.traverse_children(active_only = False):
            self._modify_todo(child)

        SC.session.commit()

        return ToDoSchema().serialize(todo)


class CancelTodo(ModifyTodo):

    def _modify_todo(self, todo: models.ToDo) -> None:
        todo.canceled = True
        todo.finished_at = datetime.datetime.now()


todo_cud_views.add_url_rule('/todo/cancel/', methods = ['PATCH'], view_func = CancelTodo.as_view('cancel_todo'))


class FinishTodo(ModifyTodo):

    def _modify_todo(self, todo: models.ToDo) -> None:
        todo.finished_at = datetime.datetime.now()


todo_cud_views.add_url_rule('/todo/finish/', methods = ['PATCH'], view_func = FinishTodo.as_view('finish_todo'))


@todo_cud_views.route('/todo/<int:pk>/', methods = ['GET'])
def get_todo(pk: int):
    todo: t.Optional[models.ToDo] = SC.session.query(models.ToDo).get(pk)

    if todo is None:
        return 'no such todo', status.HTTP_404_NOT_FOUND

    return ToDoSchema().serialize(todo)


class BaseToDoList(View):

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

    @inject_schema(schemas.ToDoListOptions())
    def dispatch_request(
        self,
        project: models.Project,
        tag: t.Optional[models.Tag],
        query: t.Optional[str],
        all_tasks: bool,
        flat: bool,
        limit: int,
        priority: t.Union[str, int, None],
    ):
        todos = self.order_todos(
            self.get_base_query().filter(
                models.ToDo.project_id == project.id,
            ).options(joinedload('tags'), joinedload('children'), joinedload('priority'))
        )

        if priority is not None:
            priority_id = models.Priority.get_for_identifier_and_project(
                session = SC.session,
                project_id = project.id,
                identifier = priority,
                target = models.Priority.id,
            )
            if priority_id is None:
                return 'invalid priority', status.HTTP_400_BAD_REQUEST
            todos = todos.filter(models.ToDo.priority_id == priority_id)

        if not all_tasks:
            todos = todos.filter(
                ~exists().where(models.Dependency.child_id == models.ToDo.id),
            )

        if query:
            todos = todos.filter(models.ToDo.text.contains(query))

        if tag is not None:
            todos = todos.join(models.Tagged).filter(models.Tagged.tag_id == tag.id)

        todos = self.limit(todos, limit)

        schema = schemas.ToDoSchema(
            fields = self.get_schema_fields()
        )

        if flat:
            schema.fields = copy.copy(schema.fields)
            del schema.fields['children']

        return {
            'todos': [
                schema.serialize(todo)
                for todo in
                todos
            ]
        }


class ToDoHistory(BaseToDoList):

    def get_schema_fields(self) -> t.Mapping[str, Field]:
        return {
            'children': fields.List(fields.SelfRelated(), read_only = True)
        }

    def get_base_query(self) -> Query:
        return SC.session.query(models.ToDo)

    def limit(self, query: Query, limit: int) -> Query:
        return query.limit(limit)


todo_cud_views.add_url_rule('/todo/history/', methods = ['GET'], view_func = ToDoHistory.as_view('todo_history'))


class ToDoList(BaseToDoList):

    def get_schema_fields(self) -> t.Mapping[str, Field]:
        return {}

    def get_base_query(self) -> Query:
        return models.ToDo.active_todos(SC.session)

    def order_todos(self, query: Query) -> Query:
        return query.join(models.ToDo.priority).order_by(
            models.Priority.level,
            models.ToDo.created_at.desc(),
        )


todo_cud_views.add_url_rule('/todo/', methods = ['GET'], view_func = ToDoList.as_view('todo_list'))
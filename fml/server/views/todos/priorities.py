import typing as t

from sqlalchemy.exc import IntegrityError

from flask import request, Blueprint
from flask_api import status
from flask_api.request import APIRequest

from hardcandy.schema import DeserializationError

from fml.server import schemas, models
from fml.server.retrieve import get_todo_for_project_and_identifier
from fml.server.session import SessionContainer as SC
from fml.server.views.utils import inject_project, inject_schema, with_errors


todo_priority_views = Blueprint(
    "todo_priority_views", __name__, url_prefix="/priorities"
)
request: APIRequest


@todo_priority_views.route("/", methods=["POST"])
def create_priority():
    try:
        priority = schemas.PriorityCreateSchema().deserialize(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    if priority.is_default:
        SC.session.query(models.Priority).filter(
            project_id=priority.project_id,
        ).update({models.Priority.is_default: False}, synchronize_session=False)

    SC.session.add(priority)

    try:
        SC.session.commit()
    except IntegrityError:
        return "Invalid priority", status.HTTP_400_BAD_REQUEST

    return schemas.PrioritySchema().serialize(priority)


@todo_priority_views.route("/", methods=["GET"])
@inject_project()
def priorities_list(project_id: int):
    priorities = (
        SC.session.query(models.Priority)
        .filter(
            models.Priority.project_id == project_id,
        )
        .order_by(models.Priority.level.asc())
    )

    schema = schemas.PrioritySchema()

    return {"priorities": [schema.serialize(tag) for tag in priorities]}


@todo_priority_views.route("/swap-levels", methods=["PATCH"])
@inject_project(use_args=False)
def swap_levels(project_id: int):
    first = models.Priority.get_for_identifier_and_project(
        session=SC.session,
        project_id=project_id,
        identifier=request.data.get("first"),
    )

    second = models.Priority.get_for_identifier_and_project(
        session=SC.session,
        project_id=project_id,
        identifier=request.data.get("second"),
    )

    if first is None or second is None:
        return "invalid priority", status.HTTP_400_BAD_REQUEST

    SC.session.execute("SET CONSTRAINTS ALL DEFERRED")

    first.level, second.level = second.level, first.level

    SC.session.commit()

    schema = schemas.PrioritySchema()

    return {"priorities": [schema.serialize(tag) for tag in (first, second)]}


@todo_priority_views.route("/modify", methods=["PATCH"])
@with_errors
@inject_schema(schemas.ModifyPrioritySchema(), use_args=False)
def modify_priority_level(
    todo: t.Union[str, int],
    priority: t.Union[str, int],
    project: models.Project,
    recursive: bool,
):
    todo = get_todo_for_project_and_identifier(SC.session, todo, project)

    priority_id = models.Priority.get_for_identifier_and_project(
        session=SC.session,
        project_id=todo.project_id,
        identifier=priority,
        target=models.Priority.id,
    )
    if priority_id is None:
        return "invalid priority", status.HTTP_400_BAD_REQUEST

    todo.priority_id = priority_id

    if recursive:
        for child in todo.traverse_children():
            child.priority_id = priority_id

    SC.session.commit()

    return schemas.ToDoSchema().serialize(todo)

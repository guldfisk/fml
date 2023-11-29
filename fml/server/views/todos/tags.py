import typing as t

from sqlalchemy.exc import IntegrityError, OperationalError

from flask import request, Blueprint
from flask_api import status
from flask_api.request import APIRequest

from hardcandy.schema import DeserializationError

from fml.server import models
from fml.server import schemas
from fml.server.retrieve import get_todo_for_project_and_identifier
from fml.server.session import SessionContainer as SC
from fml.server.views.utils import with_errors, inject_schema


todo_tag_views = Blueprint("todo_tag_views", __name__)
request: APIRequest


@todo_tag_views.route("/tag/", methods=["POST"])
def create_tag():
    schema = schemas.TagSchema()

    try:
        tag = schema.deserialize(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    SC.session.add(tag)

    try:
        SC.session.commit()
    except IntegrityError:
        SC.session.rollback()
        return "Tag already exists", status.HTTP_400_BAD_REQUEST

    return schema.serialize(tag)


@todo_tag_views.route("/todo/tag/", methods=["POST"])
@with_errors
@inject_schema(schemas.TaggedSchema(), use_args=False)
def tag_todo(
    todo_target: t.Union[str, int],
    tag_target: models.Tag,
    project: models.Project,
    recursive: bool,
):
    todo = get_todo_for_project_and_identifier(
        SC.session,
        todo_target,
        project,
    )

    todo.tags.append(tag_target)

    if recursive:
        for child in todo.traverse_children():
            child.tags.append(tag_target)

    try:
        SC.session.commit()
    except (IntegrityError, OperationalError):
        SC.session.rollback()
        return "Invalid args", status.HTTP_400_BAD_REQUEST

    return schemas.ToDoSchema().serialize(todo), status.HTTP_201_CREATED


@todo_tag_views.route("/tag/", methods=["GET"])
def tag_list():
    tags: t.List[models.Tag] = SC.session.query(models.Tag).order_by(
        models.Tag.created_at.desc()
    )

    schema = schemas.TagSchema()

    return {"tags": [schema.serialize(tag) for tag in tags]}

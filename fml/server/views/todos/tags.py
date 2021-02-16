import typing as t

from sqlalchemy.exc import IntegrityError, OperationalError

from flask import request, Blueprint
from flask_api import status
from flask_api.request import APIRequest

from hardcandy.schema import DeserializationError

from fml.server import models
from fml.server.schemas import TagSchema, TaggedSchema
from fml.server.session import SessionContainer as SC


todo_tag_views = Blueprint('todo_tag_views', __name__)
request: APIRequest


@todo_tag_views.route('/tag/', methods = ['POST'])
def create_tag():
    schema = TagSchema()

    try:
        tag = schema.deserialize(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    SC.session.add(tag)

    try:
        SC.session.commit()
    except IntegrityError:
        SC.session.rollback()
        return 'Tag already exists', status.HTTP_400_BAD_REQUEST

    return schema.serialize(tag)


@todo_tag_views.route('/todo/tag/', methods = ['POST'])
def tag_todo():
    schema = TaggedSchema()

    try:
        tagged = schema.deserialize_raw(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    todo: t.Optional[models.ToDo] = models.ToDo.get_for_identifier(
        SC.session,
        tagged['todo_id'],
        base_query = models.ToDo.active_todos(SC.session),
    )

    if todo is None:
        return 'Invalid todo', status.HTTP_400_BAD_REQUEST

    tag: t.Optional[models.Tag] = models.Tag.get_for_identifier(
        SC.session,
        tagged['tag_id'],
        target = models.Tag,
    )

    if tag is None:
        return 'Invalid tag', status.HTTP_400_BAD_REQUEST

    todo.tags.append(tag)

    if tagged['recursive']:
        for child in todo.traverse_children():
            child.tags.append(tag)

    try:
        SC.session.commit()
    except (IntegrityError, OperationalError):
        SC.session.rollback()
        return 'Invalid args', status.HTTP_400_BAD_REQUEST

    return {'status': 'ok'}, status.HTTP_201_CREATED


@todo_tag_views.route('/tag/', methods = ['GET'])
def tag_list():
    tags: t.List[models.Tag] = SC.session.query(models.Tag).order_by(models.Tag.created_at.desc())

    schema = TagSchema()

    return {
        'tags': [
            schema.serialize(tag)
            for tag in
            tags
        ]
    }

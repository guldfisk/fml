import typing as t

from sqlalchemy.exc import IntegrityError, OperationalError

from flask import request, Blueprint
from flask_api import status
from flask_api.request import APIRequest

from fml.server import models
from fml.server import schemas
from fml.server.session import SessionContainer as SC


todo_dependency_views = Blueprint('todo_dependency_views', __name__)
request: APIRequest


@todo_dependency_views.route('/todo/add-dependency/', methods = ['POST'])
def add_dependency():
    parent: t.Optional[models.ToDo] = models.ToDo.get_for_identifier(
        SC.session,
        request.data.get('parent'),
        base_query = models.ToDo.active_todos(SC.session),
    )

    if parent is None:
        return 'Invalid parent', status.HTTP_400_BAD_REQUEST

    child: t.Optional[models.ToDo] = models.ToDo.get_for_identifier(
        SC.session,
        request.data.get('child'),
        base_query = models.ToDo.active_todos(SC.session),
    )

    if child is None:
        return 'Invalid child', status.HTTP_400_BAD_REQUEST

    if parent in child.traverse_children(active_only = False):
        return 'Dependencies can not be circular', status.HTTP_400_BAD_REQUEST

    dependency = models.Dependency(parent_id = parent.id, child_id = child.id)

    SC.session.add(dependency)

    try:
        SC.session.commit()
    except (IntegrityError, OperationalError):
        SC.session.rollback()
        return 'Invalid args', status.HTTP_400_BAD_REQUEST

    return schemas.ToDoSchema().serialize(parent), status.HTTP_201_CREATED

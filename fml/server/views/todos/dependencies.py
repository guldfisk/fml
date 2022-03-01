from sqlalchemy.exc import IntegrityError, OperationalError

from flask import Blueprint
from flask_api import status
from flask_api.request import APIRequest

from fml.server import models
from fml.server import schemas
from fml.server.session import SessionContainer as SC
from fml.server.views.utils import inject_schema


todo_dependency_views = Blueprint('todo_dependency_views', __name__)
request: APIRequest


@todo_dependency_views.route('/todo/add-dependency/', methods = ['POST'])
@inject_schema(schemas.UpdateDependencySchema(), use_args = False)
def add_dependency(parent: models.ToDo, child: models.ToDo):
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


# @todo_dependency_views.route('/todo/remove-dependency/', methods = ['DELETE'])
# @inject_schema(schemas.UpdateDependencySchema(), use_args = False)
# def add_dependency(parent: models.ToDo, child: models.ToDo):
#     SC.session.query(models.Dependency).filter(
#
#     )
#
#     SC.session.add(dependency)
#
#     try:
#         SC.session.commit()
#     except (IntegrityError, OperationalError):
#         SC.session.rollback()
#         return 'Invalid args', status.HTTP_400_BAD_REQUEST
#
#     return schemas.ToDoSchema().serialize(parent), status.HTTP_201_CREATED

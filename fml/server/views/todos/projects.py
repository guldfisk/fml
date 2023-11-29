import typing as t

from sqlalchemy.exc import IntegrityError

from flask import request, Blueprint
from flask_api import status
from flask_api.request import APIRequest

from hardcandy import fields
from hardcandy.schema import DeserializationError, Schema

from fml.server import models
from fml.server import schemas
from fml.server.fields import StringIdentifiedField
from fml.server.retrieve import get_priority_level
from fml.server.session import SessionContainer as SC
from fml.server.views.utils import inject_schema


todo_project_views = Blueprint("todo_project_views", __name__)
request: APIRequest


@todo_project_views.route("/project/", methods=["POST"])
def create_project():
    schema = schemas.ProjectSchema()

    try:
        project = schema.deserialize(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    if project.is_default:
        SC.session.query(models.Project).update(
            {models.Project.is_default: False}, synchronize_session=False
        )

    SC.session.add(project)

    try:
        SC.session.commit()
    except IntegrityError:
        SC.session.rollback()
        return "Project already exists", status.HTTP_400_BAD_REQUEST

    return schema.serialize(project)


@todo_project_views.route("/project/", methods=["PATCH"])
@inject_schema(
    Schema(
        {
            "project": StringIdentifiedField(models.Project),
            "default_priority_filter": fields.CoalesceField(
                [fields.Integer(), fields.Text()],
                default=None,
                required=False,
            ),
        }
    ),
    use_args=False,
)
def modify_project(
    project: models.Project, default_priority_filter: t.Union[int, str, None]
):
    if default_priority_filter is not None:
        default_priority_filter = get_priority_level(
            SC.session, default_priority_filter, project
        )
    project.default_priority_filter = default_priority_filter
    SC.session.commit()
    return schemas.ProjectSchema().serialize(project)


@todo_project_views.route("/project/", methods=["GET"])
def project_list():
    projects: t.List[models.ToDo] = SC.session.query(models.Project).order_by(
        models.Project.created_at.desc()
    )

    schema = schemas.ProjectSchema()

    return {"projects": [schema.serialize(project) for project in projects]}

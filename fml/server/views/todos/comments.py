import typing as t

from flask import Blueprint
from flask_api.request import APIRequest

from fml.server import models, schemas
from fml.server.retrieve import get_todo_for_project_and_identifier
from fml.server.schemas import CommentSchema
from fml.server.session import SessionContainer as SC
from fml.server.views.utils import inject_schema, with_errors


todo_comments_view = Blueprint('todo_comment_views', __name__)
request: APIRequest


@todo_comments_view.route('/todo/comment/', methods = ['POST'])
@with_errors
@inject_schema(schema = CommentSchema(), use_args = False)
def comment_todo(target: t.Union[str, int], project: models.Project, comment: str):
    todo = get_todo_for_project_and_identifier(SC.session, target, project)
    comment = models.Comment(todo = todo, text = comment)
    SC.session.add(comment)
    SC.session.commit()

    return schemas.ToDoSchema().serialize(todo)

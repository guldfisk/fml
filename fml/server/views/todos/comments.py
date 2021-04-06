from flask import Blueprint
from flask_api.request import APIRequest

from fml.server import models, schemas
from fml.server.schemas import CommentSchema
from fml.server.session import SessionContainer as SC
from fml.server.views.utils import inject_schema


todo_comments_view = Blueprint('todo_comment_views', __name__)
request: APIRequest


@todo_comments_view.route('/todo/comment/', methods = ['POST'])
@inject_schema(schema = CommentSchema(), use_args = False)
def comment_todo(todo: models.ToDo, comment: str):
    comment = models.Comment(todo = todo, text = comment)
    SC.session.add(comment)
    SC.session.commit()

    return schemas.ToDoSchema().serialize(todo)

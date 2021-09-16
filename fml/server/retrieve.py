import datetime
import typing as t

from sqlalchemy.orm import Session

from fml.server import models, schemas
from fml.server.exceptions import SimpleError, MultipleCandidateError


def get_todo_for_project_and_identifier(
    session: Session,
    identifier: t.Union[str, int],
    project: models.Project,
) -> models.ToDo:
    if identifier == 'l':
        todo = session.query(models.ToDo).filter(
            models.ToDo.project == project,
        ).order_by(models.ToDo.created_at.desc()).first()
        if todo is None:
            raise SimpleError('invalid todo')
        if todo.created_at < datetime.datetime.now() - datetime.timedelta(hours = 1):
            raise SimpleError('todo too old for selecting as last')
        return todo

    todos = models.ToDo.get_list_for_identifier(
        session = session,
        identifier = identifier,
        base_query = models.ToDo.active_todos(session).filter(models.ToDo.project_id == project.id),
    )
    if not todos:
        raise SimpleError('invalid todo')
    if len(todos) > 1:
        raise MultipleCandidateError(
            models.ToDo,
            sorted(todos, key = lambda _todo: (-_todo.priority.level, _todo.created_at), reverse = True),
            schemas.ToDoSchema(),
        )

    return todos[0]

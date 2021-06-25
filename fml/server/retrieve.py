import typing as t

from sqlalchemy.orm import Session

from fml.server import models, schemas
from fml.server.exceptions import SimpleError, MultipleCandidateError


def get_todo_for_project_and_identifier(
    session: Session,
    identifier: t.Union[str, int],
    project: models.Project,
) -> models.ToDo:
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

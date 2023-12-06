import datetime
import typing as t

from sqlalchemy.orm import Session

from fml.server import models, schemas
from fml.server.exceptions import SimpleError, MultipleCandidateError


def get_todo_for_project_and_identifier(
    session: Session,
    identifier: t.Union[str, int],
    project: models.Project,
    active_only: bool = True,
) -> models.ToDo:
    if identifier == "l":
        todo = (
            session.query(models.ToDo)
            .filter(
                models.ToDo.project == project,
            )
            .order_by(models.ToDo.created_at.desc())
            .first()
        )
        if todo is None:
            raise SimpleError("invalid todo")
        if todo.created_at < datetime.datetime.now() - datetime.timedelta(hours=1):
            raise SimpleError("todo too old for selecting as last")
        return todo

    todos = models.ToDo.get_list_for_identifier(
        session=session,
        identifier=identifier,
        base_query=(
            models.ToDo.active_todos(session)
            if active_only
            else session.query(models.ToDo)
        ).filter(models.ToDo.project_id == project.id),
    )
    if not todos:
        raise SimpleError("invalid todo")
    if len(todos) > 1:
        raise MultipleCandidateError(
            models.ToDo,
            sorted(
                todos,
                key=lambda _todo: (-_todo.priority.level, _todo.created_at),
                reverse=True,
            ),
            schemas.ToDoSchema(),
        )

    return todos[0]


def get_priority_level(
    session: Session,
    level: t.Union[str, int, None],
    project: models.Project,
) -> int:
    if isinstance(level, int):
        return level
    return models.Priority.get_for_identifier_or_raise(
        session,
        level,
        schemas.PrioritySchema(),
        base_query=session.query(models.Priority).filter(
            models.Priority.project_id == project.id,
        ),
    ).level


def get_project_and_minimum_priority(
    session: Session,
    project: t.Union[str, int, None],
    minimum_priority: t.Union[str, int, None],
    ignore_priority: bool = False,
) -> t.Tuple[t.Optional[models.Project], t.Optional[int]]:
    project = (
        None
        if project == "all"
        else models.Project.get_for_identifier_or_raise(
            session,
            project,
            schemas.ProjectSchema(),
        )
    )
    level = None

    if not ignore_priority:
        if project is None:
            if minimum_priority is not None:
                if not isinstance(minimum_priority, int):
                    raise SimpleError(
                        "When filtering on priority levels for multiple projects, level just be specified as an int"
                    )
                level = minimum_priority

        else:
            if minimum_priority is not None:
                level = get_priority_level(session, minimum_priority, project)
            elif project.default_priority_filter is not None:
                level = project.default_priority_filter

    return project, level

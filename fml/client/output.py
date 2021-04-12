import typing as t

from rich.console import Console, RenderableType
from rich.table import Table
from rich.style import Style
from rich.text import Text

from fml.client import models
from fml.client.utils import format_timedelta
from fml.client import values as v


def _print_striped_table(headers: t.Sequence[str], rows: t.Iterable[t.Sequence[RenderableType]]):
    table = Table()

    for column_name in headers:
        table.add_column(column_name)

    for idx, row in enumerate(rows):
        table.add_row(
            *row,
            style = Style(bgcolor = v.LINE_BG_COLOR_ALTERNATE if idx & 1 else v.LINE_BG_COLOR),
        )

    console = Console()
    console.print(table)


def print_projects(project: t.Sequence[models.Project]) -> None:
    _print_striped_table(
        ['ID', 'Name', 'Created At', 'Is Default', 'Default Priority Filter'],
        (
            [
                str(project.pk),
                project.name,
                project.created_at.strftime(models.DATETIME_FORMAT),
                str(project.is_default),
                str(project.default_priority_filter),
            ]
            for project in
            project
        ),
    )


def print_project(project: models.Project) -> None:
    print_projects((project,))


def print_priorities(priorities: t.Sequence[models.Priority]) -> None:
    _print_striped_table(
        ['ID', 'Name', 'Project', 'Level', 'Is Default', 'Created At'],
        [
            [
                str(priority.pk),
                priority.name,
                priority.project,
                str(priority.level),
                str(priority.is_default),
                priority.created_at.strftime(models.DATETIME_FORMAT),
            ]
            for priority in
            priorities
        ],
    )


def print_priority(priority: models.Priority) -> None:
    print_priorities((priority,))


def print_alarm(alarm: models.Alarm) -> None:
    print_alarms((alarm,))


def print_alarms(alarms: t.Sequence[models.Alarm]) -> None:
    _print_striped_table(
        ['ID', 'Text', 'Start', 'End', 'ETA', 'Elapsed', 'flags', 'status'],
        (
            [
                str(alarm.pk),
                alarm.text,
                alarm.started_at.strftime(models.DATETIME_FORMAT),
                alarm.end_at.strftime(models.DATETIME_FORMAT),
                alarm.eta,
                format_timedelta(alarm.elapsed),
                ' '.join(alarm.flags),
                Text(alarm.status, style = Style(color = v.ALARM_STATUS_COLOR_MAP[alarm.status])),
            ]
            for alarm in
            alarms
        ),
    )


def print_todo(todo: models.ToDo, *, show_comments: bool = True) -> None:
    print_todos((todo,), show_comments = show_comments)


def _iterate_todos(todos: t.Sequence[models.ToDo], indent: int = 0) -> t.Iterator[t.Tuple[models.ToDo, int]]:
    for todo in todos:
        yield todo, indent
        yield from _iterate_todos(todo.children, indent + 1)


def print_todos(todos: t.Sequence[models.ToDo], *, show_comments: bool = True) -> None:
    _print_striped_table(
        ['ID', 'Text', 'Created At', 'Finished At', 'Elapsed', 'Duration', 'State', 'Priority', 'Tags', 'Project'],
        (
            [
                str(todo.pk),
                '-|' * indent + todo.text + (
                    ''.join(
                        '\n' + '-|' * indent + ' - ' + comment
                        for comment in
                        todo.comments
                    ) if show_comments else
                    ''
                ),
                todo.created_at.strftime(models.DATETIME_FORMAT),
                todo.finished_at.strftime(models.DATETIME_FORMAT) if todo.finished_at else '-',
                format_timedelta(todo.elapsed),
                format_timedelta(todo.duration) if todo.finished_at else '-',
                Text(todo.status, style = Style(color = v.STATUS_COLOR_MAP[todo.status])),
                Text(todo.priority, style = Style(color = v.PRIORITY_COLOR_MAP.get(todo.priority, v.C_NEUTRAL))),
                ', '.join(todo.tags),
                todo.project,
            ]
            for (todo, indent) in
            _iterate_todos(todos)
        ),
    )

import datetime
import typing as t

from rich.console import Console, RenderableType
from rich.table import Table
from rich.style import Style
from rich.text import Text

from fml.client import models
from fml.client import values as v
from fml.client.utils import format_timedelta
from fml.client.values import ALARM_DATETIME_FORMAT, DATETIME_FORMAT


def _print_striped_table(
    headers: t.Sequence[str],
    rows: t.Iterable[t.Sequence[RenderableType]],
    title: t.Optional[str] = None,
):
    table = Table(title = title)

    for column_name in headers:
        table.add_column(column_name)

    for idx, row in enumerate(rows):
        table.add_row(
            *row,
            style = Style(bgcolor = v.LINE_BG_COLOR_ALTERNATE if idx & 1 else v.LINE_BG_COLOR),
        )

    console = Console()
    console.print(table)


def print_projects(project: t.Sequence[models.Project], title: t.Optional[str] = None) -> None:
    _print_striped_table(
        ['ID', 'Name', 'Created At', 'Is Default', 'Default Priority Filter'],
        (
            [
                str(project.pk),
                project.name,
                project.created_at.strftime(DATETIME_FORMAT),
                str(project.is_default),
                str(project.default_priority_filter),
            ]
            for project in
            project
        ),
        title = title,
    )


def print_project(project: models.Project) -> None:
    print_projects((project,))


def print_priorities(priorities: t.Sequence[models.Priority], title: t.Optional[str] = None) -> None:
    _print_striped_table(
        ['ID', 'Name', 'Project', 'Level', 'Is Default', 'Created At'],
        [
            [
                str(priority.pk),
                Text(
                    priority.name,
                    style = Style(color = v.PRIORITY_COLOR_MAP.get(priority.level, v.C_NEUTRAL)),
                ),
                priority.project,
                str(priority.level),
                str(priority.is_default),
                priority.created_at.strftime(DATETIME_FORMAT),
            ]
            for priority in
            priorities
        ],
        title = title,
    )


def print_tags(tags: t.Sequence[models.Tag], title: t.Optional[str] = None) -> None:
    _print_striped_table(
        ['ID', 'Name', 'Created At'],
        [
            [
                str(tag.pk),
                tag.name,
                tag.created_at.strftime(DATETIME_FORMAT),
            ]
            for tag in
            tags
        ],
        title = title,
    )


def print_priority(priority: models.Priority) -> None:
    print_priorities((priority,))


def print_alarm(alarm: models.Alarm) -> None:
    print_alarms((alarm,))


def print_alarms(alarms: t.Sequence[models.Alarm], title: t.Optional[str] = None) -> None:
    _print_striped_table(
        ['ID', 'Text', 'Start', 'End', 'ETA', 'Elapsed', 'Duration', 'flags', 'status'],
        (
            [
                str(alarm.pk),
                alarm.text,
                alarm.started_at.strftime(ALARM_DATETIME_FORMAT),
                alarm.end_at.strftime(ALARM_DATETIME_FORMAT),
                alarm.eta,
                format_timedelta(alarm.elapsed),
                format_timedelta(alarm.duration),
                ' '.join(alarm.flags),
                Text(alarm.status, style = Style(color = v.ALARM_STATUS_COLOR_MAP[alarm.status])),
            ]
            for alarm in
            alarms
        ),
        title = title,
    )


def print_todo(todo: models.ToDo, *, show_comments: bool = True) -> None:
    print_todos((todo,), show_comments = show_comments)


def _iterate_todos(todos: t.Sequence[models.ToDo], indent: int = 0) -> t.Iterator[t.Tuple[models.ToDo, int]]:
    for todo in todos:
        yield todo, indent
        yield from _iterate_todos(todo.children, indent + 1)


def print_todos(
    todos: t.Sequence[models.ToDo],
    *,
    show_comments: bool = True,
    title: t.Optional[str] = None,
) -> None:
    _print_striped_table(
        [
            'ID', 'Text', 'Created At', 'Finished At', 'Elapsed', 'Duration', 'Since', 'State', 'Priority', 'Tags',
            'Project',
        ],
        (
            [
                str(todo.pk),
                Text('-|' * indent) + Text(
                    todo.text,
                    style = Style(color = v.C_NEUTRAL if todo.status == v.State.WAITING else v.C_WHITE),
                ) + Text(
                    ''.join(
                        '\n' + '-|' * indent + ' - ' + comment
                        for comment in
                        todo.comments
                    ) if show_comments else
                    ''
                ),
                todo.created_at.strftime(DATETIME_FORMAT),
                todo.finished_at.strftime(DATETIME_FORMAT) if todo.finished_at else '-',
                format_timedelta(todo.elapsed),
                format_timedelta(todo.duration) if todo.finished_at else '-',
                format_timedelta(todo.time_since) if todo.finished_at else '-',
                Text(todo.status.name, style = Style(color = v.STATUS_COLOR_MAP[todo.status])),
                Text(
                    todo.priority.name,
                    style = Style(color = v.PRIORITY_COLOR_MAP.get(todo.priority.level, v.C_NEUTRAL)),
                ),
                ', '.join(todo.tags),
                todo.project,
            ]
            for (todo, indent) in
            _iterate_todos(todos)
        ),
        title = title,
    )


def show_points(points: t.Sequence[t.Tuple[datetime.datetime, t.Union[int, float]]], chart: bool = False) -> None:
    import numpy as np
    import gnuplotlib as gp

    if not points:
        print('No data')
        return

    args = {
        'unset': 'grid',
        'set': ('xdata time', 'format x "%d/%m/%y"'),
    }

    if not chart:
        args['terminal'] = 'dumb 160 40'

    gp.plot(
        np.asarray([date.timestamp() for date, _ in points]),
        np.asarray([active for _, active in points]),
        **args,
    )

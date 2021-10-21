import dataclasses
import datetime
import json
import re
import typing as t
from abc import abstractmethod

from rich import print
from rich.console import Console, RenderableType
from rich.style import Style
from rich.table import Table
from rich.text import Text

from fml.client import models
from fml.client import values as v
from fml.client.cli.context import Context, OutputMode
from fml.client.utils import format_timedelta
from fml.client.values import ALARM_DATETIME_FORMAT, DATETIME_FORMAT
from fml.common.ci.models import CIRun


def _get_striped_table(
    headers: t.Sequence[str],
    rows: t.Iterable[t.Sequence[RenderableType]],
    title: t.Optional[str] = None,
) -> Table:
    table = Table(title = title)

    for column_name in headers:
        table.add_column(column_name)

    for idx, row in enumerate(rows):
        table.add_row(
            *row,
            style = Style(bgcolor = v.LINE_BG_COLOR_ALTERNATE if idx & 1 else v.LINE_BG_COLOR),
        )

    return table


def _print_striped_table(
    headers: t.Sequence[str],
    rows: t.Iterable[t.Sequence[RenderableType]],
    title: t.Optional[str] = None,
):
    table = _get_striped_table(headers, rows, title)
    console = Console()
    console.print(table)


T = t.TypeVar('T')


def json_serialize(obj: t.Any) -> str:
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError(f'Type {type(obj)} not serializable')


class _MultiItemPrinter(t.Generic[T]):
    title: str
    headers: t.Sequence[str]

    @classmethod
    @abstractmethod
    def format_item(cls, item: T, **kwargs) -> t.Sequence[t.Any]:
        pass

    @classmethod
    @abstractmethod
    def get_item_header(cls, item: T, **kwargs) -> str:
        pass

    def get_table(self, items: t.Sequence[T], **kwargs) -> Table:
        return _get_striped_table(
            self.headers,
            [self.format_item(item, idx = idx, **kwargs) for idx, item in enumerate(items)],
            title = kwargs.get('title', self.title),
        )

    def __call__(self, items: t.Union[T, t.Sequence[T]], **kwargs) -> None:
        if not isinstance(items, t.Sequence) and Context.output_mode in (OutputMode.TABLE, OutputMode.LIST):
            items = [items]
        if Context.output_mode == OutputMode.TABLE:
            _print_striped_table(
                self.headers,
                [self.format_item(item, idx = idx, **kwargs) for idx, item in enumerate(items)],
                title = kwargs.get('title', self.title),
            )
        elif Context.output_mode == OutputMode.LIST:
            title = kwargs.get('title', self.title)
            if title:
                print(title)
            for idx, item in enumerate(items):
                print(self.get_item_header(item, **kwargs))
                for key, value in zip(self.headers, self.format_item(item, idx = idx, **kwargs)):
                    print(
                        Text('\t')
                        + Text(key, style = Style(color = v.C_LIGHT_GREY))
                        + Text(': ')
                        + value
                    )
        elif Context.output_mode == OutputMode.JSON:
            print(
                json.dumps(
                    [dataclasses.asdict(item) for item in items]
                    if isinstance(items, t.Sequence) else
                    dataclasses.asdict(items),
                    default = json_serialize,
                )
            )


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


class AlarmPrinter(_MultiItemPrinter[models.Alarm]):
    title = None
    headers = ['ID', 'Text', 'Start', 'End', 'ETA', 'Elapsed', 'Duration', 'flags', 'status']

    @classmethod
    def format_item(cls, item: models.Alarm, **kwargs) -> t.Sequence[t.Any]:
        return [
            str(item.pk),
            item.text,
            item.started_at.strftime(ALARM_DATETIME_FORMAT),
            item.end_at.strftime(ALARM_DATETIME_FORMAT),
            item.eta,
            format_timedelta(item.elapsed),
            format_timedelta(item.duration),
            ' '.join(item.flags),
            Text(item.status, style = Style(color = v.ALARM_STATUS_COLOR_MAP[item.status])),
        ]

    @classmethod
    def get_item_header(cls, item: models.Alarm, **kwargs) -> str:
        return str(item.pk)


print_alarms = print_alarm = AlarmPrinter()


class TodoPrinter(_MultiItemPrinter[models.ToDo]):
    title = None
    headers = [
        'ID', 'Text', 'Created At', 'Finished At', 'Elapsed', 'Duration', 'Since', 'State', 'Priority', 'Tags',
        'Project',
    ]

    @classmethod
    def _iterate_todos(cls, todos: t.Sequence[models.ToDo], indent: int = 0) -> t.Iterator[t.Tuple[models.ToDo, int]]:
        for todo in todos:
            yield todo, indent
            yield from cls._iterate_todos(todo.children, indent + 1)

    @classmethod
    def format_item(cls, item: models.ToDo, **kwargs) -> t.Sequence[t.Any]:
        return [
            str(item.pk),
            Text('-|' * kwargs['indent']) + Text(
                item.text,
                style = Style(color = v.C_NEUTRAL if item.status == v.State.WAITING else v.C_WHITE),
            ) + Text(
                ''.join(
                    '\n' + kwargs.get('ident_string', '-|') * (
                        kwargs['indent'] + kwargs.get('comment_indent', 0)) + ' - ' + comment
                    for comment in
                    item.comments
                ) if kwargs.get('show_comments', True) else
                ''
            ),
            item.created_at.strftime(DATETIME_FORMAT),
            item.finished_at.strftime(DATETIME_FORMAT) if item.finished_at else '-',
            format_timedelta(item.elapsed),
            format_timedelta(item.duration) if item.finished_at else '-',
            format_timedelta(item.time_since) if item.finished_at else '-',
            Text(item.status.name, style = Style(color = v.STATUS_COLOR_MAP[item.status])),
            Text(
                item.priority.name,
                style = Style(color = v.PRIORITY_COLOR_MAP.get(item.priority.level, v.C_NEUTRAL)),
            ),
            ', '.join(item.tags),
            item.project,
        ]

    @classmethod
    def get_item_header(cls, item: models.ToDo, **kwargs) -> str:
        return str(item.pk)

    def __call__(self, items: t.Union[models.ToDo, t.Sequence[models.ToDo]], **kwargs) -> None:
        if not isinstance(items, t.Sequence):
            items = [items]
        if Context.output_mode == OutputMode.TABLE:
            _print_striped_table(
                self.headers,
                [self.format_item(item, indent = indent, **kwargs) for item, indent in self._iterate_todos(items)],
                title = kwargs.get('title', self.title),
            )
        elif Context.output_mode == OutputMode.LIST:
            title = kwargs.get('title', self.title)
            if title:
                print(title)
            for item, indent in self._iterate_todos(items):
                print((indent * '----') + '> ' + self.get_item_header(item, **kwargs))
                for key, value in zip(
                    self.headers,
                    self.format_item(
                        item,
                        indent = 0,
                        comment_indent = indent + 1,
                        ident_string = '\t', **kwargs,
                    )
                ):
                    print(
                        Text((indent + 1) * '\t')
                        + Text(key, style = Style(color = v.C_LIGHT_GREY))
                        + Text(': ')
                        + value
                    )


print_todos = print_todo = TodoPrinter()


def show_points(
    points: t.Sequence[t.Tuple[datetime.datetime, t.Union[int, float]]],
    title: str,
    y_label: str,
) -> None:
    if not points:
        print('No data')
        return

    import plotext as plt

    dates, values = zip(*points)
    date_time_stamps = [d.timestamp() for d in dates]

    plt.plot(date_time_stamps, values)
    plt.xticks(date_time_stamps, (d.strftime('%Y/%m/%d') for d in dates))
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(y_label)
    plt.canvas_color('iron')
    plt.axes_color('cloud')
    plt.grid(False, True)

    plt.show()


class CICheckerPrinter(_MultiItemPrinter[models.CIChecker]):
    title = None
    headers = ['Run ID', 'Started', 'Timeout', 'Status']

    @classmethod
    def format_item(cls, item: models.CIChecker, **kwargs) -> t.Sequence[t.Any]:
        return [
            '[link={}]{}[/link]'.format(item.link, item.pk),
            item.started.strftime(ALARM_DATETIME_FORMAT),
            item.timeout.strftime(ALARM_DATETIME_FORMAT),
            Text(item.status, style = Style(color = v.ALARM_STATUS_COLOR_MAP[item.status])),
        ]

    @classmethod
    def get_item_header(cls, item: models.Alarm, **kwargs) -> str:
        return str(item.pk)


print_ci_checkers = CICheckerPrinter()


class CIRunPrinter(_MultiItemPrinter[CIRun]):
    title = None
    headers = ['IDX', 'ID', 'Name', 'Start', 'Elapsed', 'State', 'Result']

    @classmethod
    def format_item(cls, item: CIRun, **kwargs) -> t.Sequence[t.Any]:
        _diff_regex = re.compile('D\d+$')

        #TODO remove
        try:
            _diff_regex.match(item.name)
        except TypeError:
            print(item.name)

        return [
            str(kwargs['idx']),
            '[link={}]{}[/link]'.format(item.link, item['id']),
            (
                '[link=https://phabricator.uniid.it/{diff}]{diff}[/link]'.format(diff = item.name)
                if _diff_regex.match(item.name) else
                item.name
            ),
            item.started_at.strftime(ALARM_DATETIME_FORMAT),
            format_timedelta(item.elapsed),
            Text(item['state'], style = Style(color = v.CI_STATUS_COLOR_MAP.get(item['state'], v.C_NEUTRAL))),
            Text(item['result'], style = Style(color = v.CI_STATUS_COLOR_MAP.get(item['result'], v.C_NEUTRAL))),
        ]

    @classmethod
    def get_item_header(cls, item: models.Alarm, **kwargs) -> str:
        return str(item.pk)


print_ci_runs = CIRunPrinter()

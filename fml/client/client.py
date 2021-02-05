import logging
import typing as t
import datetime

import requests
import click
import gnuplotlib as gp
import numpy as np
from texttable import Texttable

from pkg_resources import iter_entry_points
from click_plugins import with_plugins

from fml.client import models
from fml.client.dateparse import parse_datetime, DateParseException
from fml.client.utils import format_timedelta


class ClientError(Exception):

    def __init__(self, message: str) -> None:
        super().__init__()
        self._message = message

    @property
    def message(self) -> str:
        return self._message


class Client(object):

    def __init__(self, host: str = 'localhost:8888'):
        self._host = host

    def _make_request(
        self,
        endpoint: str,
        method: str = 'GET',
        data: t.Optional[t.Mapping[str, t.Any]] = None,
        **kwargs,
    ) -> t.Any:
        if data is None:
            data = {}

        url = f'http://{self._host}/{endpoint}'

        logging.info('{} {} {}'.format(method, url, kwargs))

        response = requests.request(
            method,
            url,
            json = data,
            params = kwargs,
        )
        try:
            response.raise_for_status()
        except Exception:
            raise ClientError(
                response.content.decode('utf-8')
                if isinstance(response.content, bytes) else
                str(response.content)
            )
        return response.json()

    def new_alarm(
        self,
        text: str,
        end_at: datetime.datetime,
        mail: bool = False,
        silent: bool = False,
        requires_acknowledgment: bool = False,
        retry_delay: int = 60,
    ) -> models.Alarm:
        return models.Alarm.from_remote(
            self._make_request(
                'alarm/',
                'POST',
                {
                    'text': text,
                    'end_at': end_at.strftime('%d/%m/%Y %H:%M:%S'),
                    'send_email': mail,
                    'silent': silent,
                    'requires_acknowledgment': requires_acknowledgment,
                    'retry_delay': retry_delay,
                }
            )
        )

    def cancel_alarm(self, alarm_id: int) -> models.Alarm:
        return models.Alarm.from_remote(
            self._make_request(
                'alarms/cancel/{}/'.format(alarm_id),
                'PATCH',
            )
        )

    def acknowledge_alarm(self, alarm_id: int) -> models.Alarm:
        return models.Alarm.from_remote(
            self._make_request(
                'alarms/acknowledge/{}/'.format(alarm_id),
                'PATCH',
            )
        )

    def active_alarms(self, limit: t.Optional[int] = None) -> t.Sequence[models.Alarm]:
        return [
            models.Alarm.from_remote(alarm)
            for alarm in
            self._make_request('alarms/', limit = limit)['alarms']
        ]

    def alarm_history(self, limit: t.Optional[int] = 10) -> t.Sequence[models.Alarm]:
        return [
            models.Alarm.from_remote(alarm)
            for alarm in
            self._make_request('alarms/history/', limit = limit)['alarms']
        ]

    def cancel_all_alarms(self) -> t.Sequence[models.Alarm]:
        return [
            models.Alarm.from_remote(alarm)
            for alarm in
            self._make_request('alarms/cancel/', 'PATCH')['alarms']
        ]

    def acknowledge_all_alarms(self) -> t.Sequence[models.Alarm]:
        return [
            models.Alarm.from_remote(alarm)
            for alarm in
            self._make_request('alarms/acknowledge/', 'PATCH')['alarms']
        ]

    def create_project(
        self,
        name: str,
    ) -> models.Project:
        return models.Project.from_remote(
            self._make_request(
                'project/',
                'POST',
                {
                    'name': name,
                    'is_default': False,
                }
            )
        )

    def list_projects(self, limit: t.Optional[int] = 25) -> t.Sequence[models.Project]:
        return [
            models.Project.from_remote(project)
            for project in
            self._make_request('project/', limit = limit)['projects']
        ]

    def new_todo(
        self,
        text: str,
        project: t.Optional[str] = None,
        tags: t.Collection[str] = (),
        parents: t.Collection[str] = (),
    ) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'todo/',
                'POST',
                {
                    'text': text,
                    'project': project,
                    'tags': tags,
                    'parents': parents,
                }
            )
        )

    def cancel_todo(self, target: str) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'todo/cancel/',
                'PATCH',
                {'target': target},
            )
        )

    def finish_todo(self, target: str) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'todo/finish/',
                'PATCH',
                {'target': target},
            )
        )

    def active_todos(
        self,
        project: t.Optional[str] = None,
        tag: t.Optional[str] = None,
    ) -> t.Sequence[models.ToDo]:
        return [
            models.ToDo.from_remote(todo)
            for todo in
            self._make_request('todo/', project = project, tag = tag)['todos']
        ]

    def todo_history(
        self,
        limit: t.Optional[int] = 25,
        project: t.Optional[str] = None,
        tag: t.Optional[str] = None,
    ) -> t.Sequence[models.ToDo]:
        return [
            models.ToDo.from_remote(todo)
            for todo in
            self._make_request(
                'todo/history/',
                limit = limit,
                project = project,
                tag = tag,
            )['todos']
        ]

    def todo_burn_down(
        self,
        project: t.Optional[str] = None,
        tag: t.Optional[str] = None,
    ) -> t.Sequence[t.Tuple[datetime.datetime, int]]:
        return [
            (
                datetime.datetime.strptime(date, models.DATETIME_FORMAT),
                active_todos,
            )
            for date, active_todos in
            self._make_request(
                'todo/burn-down/',
                project = project,
                tag = tag,
            )['points']
        ]

    def todo_throughput(
        self,
        project: t.Optional[str] = None,
        tag: t.Optional[str] = None,
    ) -> t.Sequence[t.Tuple[datetime.datetime, int]]:
        return [
            (
                datetime.datetime.strptime(date, models.DATETIME_FORMAT),
                throughput,
            )
            for date, throughput in
            self._make_request(
                'todo/throughput/',
                project = project,
                tag = tag,
            )['points']
        ]

    def list_tags(self) -> t.Sequence[str]:
        return [
            tag['name']
            for tag in
            self._make_request('tag/')['tags']
        ]

    def create_tag(self, tag: str) -> None:
        self._make_request(
            'tag/',
            method = 'POST',
            data = {
                'name': tag,
            }
        )

    def tag_todo(
        self,
        todo: t.Union[int, str],
        tag: t.Union[int, str],
        recursive: bool = False,
    ) -> None:
        self._make_request(
            'todo/tag/',
            method = 'POST',
            data = {
                'todo_id': todo,
                'tag_id': tag,
                'recursive': recursive,
            }
        )

    def register_dependency(self, parent: t.Union[int, str], child: t.Union[int, str]) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'todo/add-dependency/',
                method = 'POST',
                data = {
                    'parent': parent,
                    'child': child,
                }
            )
        )


def print_projects(project: t.Sequence[models.Project]) -> None:
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_max_width(180)
    table.header(
        ['ID', 'Name', 'Created At', 'Is Default']
    )
    table.add_rows(
        [
            [
                project.pk,
                project.name,
                project.created_at.strftime(models.DATETIME_FORMAT),
                str(project.is_default),
            ]
            for project in
            project
        ],
        header = False,
    )
    print(table.draw())


def print_project(project: models.Project) -> None:
    print_projects((project,))


def print_alarm(alarm: models.Alarm) -> None:
    print_alarms((alarm,))


def print_alarms(alarms: t.Sequence[models.Alarm]) -> None:
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_max_width(180)
    table.header(
        ['ID', 'Text', 'Start', 'End', 'ETA', 'Elapsed', 'flags', 'status']
    )
    table.add_rows(
        [
            [
                alarm.pk,
                alarm.text,
                alarm.started_at.strftime(models.DATETIME_FORMAT),
                alarm.end_at.strftime(models.DATETIME_FORMAT),
                alarm.eta,
                format_timedelta(alarm.elapsed),
                ' '.join(alarm.flags),
                alarm.status,
            ]
            for alarm in
            alarms
        ],
        header = False,
    )
    print(table.draw())


def print_todo(todo: models.ToDo) -> None:
    print_todos((todo,))


def iterate_todos(todos: t.Sequence[models.ToDo], indent: int = 0) -> t.Iterator[t.Tuple[models.ToDo, int]]:
    for todo in todos:
        yield todo, indent
        yield from iterate_todos(todo.children, indent + 1)


def print_todos(todos: t.Sequence[models.ToDo]) -> None:
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_max_width(180)
    table.header(
        ['ID', 'Text', 'Created At', 'Finished At', 'Elapsed', 'Duration', 'State', 'Tags', 'Project']
    )
    table.add_rows(
        [
            [
                todo.pk,
                '-|' * indent + todo.text,
                todo.created_at.strftime(models.DATETIME_FORMAT),
                todo.finished_at.strftime(models.DATETIME_FORMAT) if todo.finished_at else '-',
                format_timedelta(todo.elapsed),
                format_timedelta(todo.duration) if todo.finished_at else '-',
                todo.status,
                ', '.join(todo.tags),
                todo.project,
            ]
            for todo, indent in
            iterate_todos(todos)
        ],
        header = False,
    )
    print(table.draw())


@with_plugins(iter_entry_points('click_command_tree'))
@click.group()
def main() -> None:
    """
    Keep track of stuff and such.
    """
    pass


@main.group('alarm')
def alarm_service() -> None:
    """
    Timed alarms.
    """
    pass


@alarm_service.command(name = 'new')
@click.argument('text', type = str)
@click.argument('absolute', default = None, type = str, required = False)
@click.option('--seconds', '-s', default = 0, type = int, help = 'Relative offset seconds.')
@click.option('--minutes', '-m', default = 0, type = int, help = 'Relative offset minutes.')
@click.option('--hours', '-h', default = 0, type = int, help = 'Relative offset hours.')
@click.option(
    '--retry-delay',
    default = 60,
    type = int,
    help = 'Delay in seconds for re-notification delay. Only relevant when acknowledgment is required.',
)
@click.option('--mail', default = False, type = bool, is_flag = True, show_default = True, help = 'Also send email.')
@click.option('--silent', default = False, type = bool, is_flag = True, show_default = True,
              help = 'Don\'t play sound.')
@click.option(
    '--requires-acknowledgement',
    '--ack',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Re notify until acknowledged.',
)
def new_alarm(
    text: str,
    absolute: t.Optional[str] = None,
    seconds: int = 0,
    minutes: int = 0,
    hours: int = 0,
    retry_delay: int = 60,
    mail: bool = False,
    silent: bool = False,
    requires_acknowledgement: bool = False,
) -> None:
    """
    Create new alarm.
    """
    if absolute is None:
        target = datetime.datetime.now(
        ) + datetime.timedelta(
            seconds = seconds,
            minutes = minutes,
            hours = hours,
        )
    else:
        try:
            target = parse_datetime(absolute)
        except DateParseException:
            print('invalid datetime format "{}"'.format(absolute))
            return

    print_alarm(
        Client().new_alarm(
            text,
            end_at = target,
            mail = mail,
            silent = silent,
            requires_acknowledgment = requires_acknowledgement,
            retry_delay = retry_delay,
        )
    )


@alarm_service.command(name = 'list')
@click.option(
    '--history',
    '-h',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Include all alarms, not just active ones.',
)
@click.option('--limit', '-l', default = 10, type = int, help = 'Limit.')
def list_alarms(history: bool = False, limit: int = 10) -> None:
    """
    List active alarms.
    """
    print_alarms(
        Client().alarm_history(limit = limit) if history else Client().active_alarms(limit = limit)
    )


@alarm_service.command(name = 'cancel')
@click.argument('target', type = str)
def cancel_alarms(target: str) -> None:
    """
    Cancel alarms with id. "all" for cancelling all active alarms.
    """
    if target == 'all':
        print_alarms(
            Client().cancel_all_alarms()
        )
    else:
        try:
            alarm_id = int(target)
        except ValueError:
            print('invalid target')
            return
        print_alarm(Client().cancel_alarm(alarm_id))


@alarm_service.command(name = 'ack')
@click.argument('target', type = str)
def acknowledge_alarms(target: str) -> None:
    """
    Acknowledge alarm requiring acknowledgement. You can only acknowledge commands after their target time.
    Target is either id of alarm or "all" for all acknowledgeable alarms.
    """
    if target == 'all':
        print_alarms(
            Client().acknowledge_all_alarms()
        )
    else:
        try:
            alarm_id = int(target)
        except ValueError:
            print('invalid target')
            return
        print_alarm(Client().acknowledge_alarm(alarm_id))


@main.group('todo')
def todo_service() -> None:
    """
    Keep track of stuff to do.
    """
    pass


@todo_service.command(name = 'new')
@click.argument('text', type = str, required = True, nargs = -1)
@click.option('--project', '-p', type = str, help = 'Project.')
@click.option('--tag', '-t', default = (), type = str, help = 'Tags.', multiple = True)
@click.option('--parent', '-a', default = (), type = str, help = 'parent.', multiple = True)
def new_todo(
    text: t.Sequence[str],
    project: str,
    tag: t.Sequence[str],
    parent: t.Sequence[str],
) -> None:
    """
    Create new todo.
    """
    print_todo(
        Client().new_todo(
            ' '.join(text),
            project = project,
            tags = tag,
            parents = parent,
        )
    )


@todo_service.command(name = 'cancel')
@click.argument('target', type = str)
def cancel_todo(target: str) -> None:
    """
    Cancel todo. Target is either id or partial text of todo.
    """
    print_todo(Client().cancel_todo(target))


@todo_service.command(name = 'finish')
@click.argument('target', type = str)
def finish_todo(target: str) -> None:
    """
    Finish todo. Target is either id or partial text of todo.
    """
    print_todo(Client().finish_todo(target))


@todo_service.command(name = 'list')
@click.option(
    '--history',
    '-h',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Include non-pending todos.'
)
@click.option('--limit', '-l', default = 25, type = int, help = 'Limit.')
@click.option('--project', '-p', type = str, help = 'Project.')
@click.option('--tag', '-t', type = str, help = 'Filter on tag.')
def list_todos(
    history: bool = False,
    limit: int = 25,
    project: t.Optional[str] = None,
    tag: t.Optional[str] = None,
) -> None:
    """
    List pending todos.
    """
    print_todos(
        Client().todo_history(project = project, limit = limit, tag = tag)
        if history else
        Client().active_todos(project = project, tag = tag)
    )


def _show_points(points: t.Sequence[t.Tuple[datetime.datetime, t.Union[int, float]]], chart: bool = False) -> None:
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


@todo_service.command(name = 'burndown')
@click.option(
    '--chart',
    '-c',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Output to window instead of terminal',
)
@click.option('--project', '-p', type = str, help = 'Project.')
@click.option('--tag', '-t', type = str, help = 'Filter on tag.')
def todos_burn_down(
    chart: bool = False,
    project: t.Optional[str] = None,
    tag: t.Optional[str] = None,
) -> None:
    """
    Show todo burndown chart.
    """
    _show_points(
        Client().todo_burn_down(project = project, tag = tag),
        chart,
    )


@todo_service.command(name = 'throughput')
@click.option(
    '--chart',
    '-c',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Output to window instead of terminal',
)
@click.option('--project', '-p', type = str, help = 'Project.')
@click.option('--tag', '-t', type = str, help = 'Filter on Tag.')
def todos_throughput(
    chart: bool = False,
    project: t.Optional[str] = None,
    tag: t.Optional[str] = None,
) -> None:
    """
    Show todo throughput chart.
    """
    _show_points(
        Client().todo_throughput(project = project, tag = tag),
        chart,
    )


@todo_service.group('tag')
def tag_service() -> None:
    """
    Todo tags.
    """
    pass


@tag_service.command(name = 'list')
def list_tags() -> None:
    """
    List tags.
    """
    for tag in Client().list_tags():
        print(tag)


@tag_service.command(name = 'new')
@click.argument('tag', type = str, required = True)
def create_tag(
    tag: str,
) -> None:
    """
    Create a new tag
    """
    Client().create_tag(tag)
    print('ok')


@tag_service.command(name = 'add')
@click.argument('todo', type = str, required = True)
@click.argument('tag', type = str, required = True)
@click.option(
    '--recursive',
    '-r',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Add tag to all children recursivly.',
)
def tag_todo(
    todo: str,
    tag: str,
    recursive: bool = False,
) -> None:
    """
    Tag todo.
    """
    Client().tag_todo(todo, tag, recursive)
    print('ok')


@todo_service.command(name = 'dep')
@click.argument('parent', type = str, required = True)
@click.argument('task', type = str, required = True)
def tag_todo(
    parent: str,
    task: str,
) -> None:
    """
    Register task as subtask of other task
    """
    print_todo(
        Client().register_dependency(parent, task)
    )


@todo_service.group('project')
def project_service() -> None:
    """
    Todo projects.
    """
    pass


@project_service.command(name = 'list')
def list_tags() -> None:
    """
    List projects.
    """
    print_projects(
        Client().list_projects()
    )


@project_service.command(name = 'new')
@click.argument('name', type = str, required = True)
def create_tag(
    name: str,
) -> None:
    """
    Create a new tag
    """
    print_project(
        Client().create_project(name)
    )


if __name__ == '__main__':
    try:
        main()
    except ClientError as e:
        print(e.message)

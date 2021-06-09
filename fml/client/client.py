import json
import logging
import os
import typing as t
import datetime

import requests
import click

from fml import sound
from fml.client import models
from fml.client import output
from fml.client.dateparse import parse_datetime, DateParseException


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
            try:
                message = json.dumps(response.json(), indent = 4)
            except ValueError:
                message = (
                    response.content.decode('utf-8')
                    if isinstance(response.content, bytes) else
                    str(response.content)
                )
            raise ClientError(message)
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
                'alarms/',
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

    def active_alarms(self, limit: t.Optional[int] = None, query: t.Optional[str] = None) -> t.Sequence[models.Alarm]:
        return [
            models.Alarm.from_remote(alarm)
            for alarm in
            self._make_request('alarms/', limit = limit, query = query)['alarms']
        ]

    def alarm_history(self, limit: t.Optional[int] = 10, query: t.Optional[str] = None) -> t.Sequence[models.Alarm]:
        return [
            models.Alarm.from_remote(alarm)
            for alarm in
            self._make_request('alarms/history/', limit = limit, query = query)['alarms']
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

    def modify_project_default_priority_filter(
        self,
        project: t.Union[int, str],
        default_priority_filter: t.Union[int, str, None],
    ) -> models.Project:
        return models.Project.from_remote(
            self._make_request(
                'project/',
                method = 'PATCH',
                data = {
                    'project': project,
                    'default_priority_filter': default_priority_filter,
                }
            )
        )

    def list_projects(self, limit: t.Optional[int] = 25) -> t.Sequence[models.Project]:
        return [
            models.Project.from_remote(project)
            for project in
            self._make_request('project/', limit = limit)['projects']
        ]

    def list_priorities(
        self,
        project: t.Union[str, int, None],
        limit: t.Optional[int] = 25,
    ) -> t.Sequence[models.Priority]:
        return [
            models.Priority.from_remote(project)
            for project in
            self._make_request('priorities/', limit = limit, project = project)['priorities']
        ]

    def new_todo(
        self,
        text: str,
        project: t.Optional[str] = None,
        priority: t.Optional[str] = None,
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
                    'priority': priority,
                    'tags': tags,
                    'parents': parents,
                }
            )
        )

    def get_todo(self, todo: t.Union[str, int]) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'todo/single/',
                todo = todo,
            )
        )

    def new_priority(
        self,
        name: str,
        level: int,
        project: t.Union[str, int, None],
        is_default: bool = False,
    ) -> models.Priority:
        return models.Priority.from_remote(
            self._make_request(
                'priorities/',
                'POST',
                {
                    'name': name,
                    'project': project,
                    'level': level,
                    'is_default': is_default,
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
        query: t.Optional[str] = None,
        all_tasks: bool = False,
        flat: bool = False,
        minimum_priority: t.Union[str, int, None] = None,
        ignore_priority: bool = False,
    ) -> t.Sequence[models.ToDo]:
        return [
            models.ToDo.from_remote(todo)
            for todo in
            self._make_request(
                'todo/',
                project = project,
                tag = tag,
                query = query,
                all_tasks = all_tasks,
                flat = flat,
                minimum_priority = minimum_priority,
                ignore_priority = ignore_priority,
            )['todos']
        ]

    def todo_history(
        self,
        limit: t.Optional[int] = 25,
        project: t.Optional[str] = None,
        tag: t.Optional[str] = None,
        query: t.Optional[str] = None,
        all_tasks: bool = False,
        flat: bool = False,
        minimum_priority: t.Union[str, int, None] = None,
        ignore_priority: bool = False,
    ) -> t.Sequence[models.ToDo]:
        return [
            models.ToDo.from_remote(todo)
            for todo in
            self._make_request(
                'todo/history/',
                limit = limit,
                project = project,
                tag = tag,
                query = query,
                all_tasks = all_tasks,
                flat = flat,
                minimum_priority = minimum_priority,
                ignore_priority = ignore_priority,
            )['todos']
        ]

    def todo_burn_down(
        self,
        project: t.Optional[str] = None,
        tag: t.Optional[str] = None,
        all_tasks: bool = False,
        ignore_priority: bool = False,
        minimum_priority: t.Optional[str] = None,
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
                top_level_only = not all_tasks,
                ignore_priority = ignore_priority,
                minimum_priority = minimum_priority,
            )['points']
        ]

    def todo_throughput(
        self,
        project: t.Optional[str] = None,
        tag: t.Optional[str] = None,
        all_tasks: bool = False,
        ignore_priority: bool = False,
        minimum_priority: t.Optional[str] = None,
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
                top_level_only = not all_tasks,
                ignore_priority = ignore_priority,
                minimum_priority = minimum_priority,
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

    def comment_todo(
        self,
        todo: t.Union[int, str],
        comment: str,
    ) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'todo/comment/',
                method = 'POST',
                data = {
                    'todo': todo,
                    'comment': comment,
                }
            )
        )

    def modify_todo_priority(
        self,
        todo: t.Union[int, str],
        priority: t.Union[int, str],
        recursive: bool = False,
    ) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'priorities/modify',
                method = 'PATCH',
                data = {
                    'todo': todo,
                    'priority': priority,
                    'recursive': recursive,
                }
            )
        )

    def modify_todo_description(
        self,
        todo: t.Union[int, str],
        description: str,
    ) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'todo/description/',
                method = 'PATCH',
                data = {
                    'todo': todo,
                    'description': description,
                }
            )
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

    def swap_priority_levels(
        self,
        first: t.Union[int, str],
        second: t.Union[int, str],
        project: t.Union[int, str, None] = None,
    ) -> t.Sequence[models.Priority]:
        return [
            models.Priority.from_remote(project)
            for project in
            self._make_request(
                'priorities/swap-levels',
                method = 'PATCH',
                data = {
                    'first': first,
                    'second': second,
                    'project': project,
                }
            )['priorities']
        ]


class AliasedGroup(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [
            x
            for x in
            self.list_commands(ctx)
            if x.startswith(cmd_name)
        ]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: {}'.format(', '.join(sorted(matches))))


@click.group(cls = AliasedGroup)
def main() -> None:
    """
    Keep track of stuff and such.
    """
    pass


@main.command(name = 'ding')
def ding() -> None:
    """
    Play alarm sound.
    """
    sound.play_sound()


@main.group('alarm', cls = AliasedGroup)
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
@click.option('--days', '-d', default = 0, type = int, help = 'Relative offset days.')
@click.option('--weeks', '-w', default = 0, type = int, help = 'Relative offset weeks.')
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
    days: int = 0,
    weeks: int = 0,
    retry_delay: int = 60,
    mail: bool = False,
    silent: bool = False,
    requires_acknowledgement: bool = False,
) -> None:
    """
    Create new alarm.
    """
    if absolute is None:
        base_datetime = datetime.datetime.now()
    else:
        try:
            base_datetime = parse_datetime(absolute)
        except DateParseException as e:
            print('invalid datetime format "{}" ({})'.format(absolute, e))
            return
    target = base_datetime + datetime.timedelta(
        seconds = seconds,
        minutes = minutes,
        hours = hours,
        days = days + weeks * 7,
    )
    if target < datetime.datetime.now():
        print('alarm must be scheduled for future')
        return

    output.print_alarm(
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
@click.option('--query', '-q', type = str, help = 'Filter on text or id.')
@click.option('--limit', '-l', default = 10, type = int, help = 'Limit.')
def list_alarms(history: bool = False, query: t.Optional[str] = None, limit: int = 10) -> None:
    """
    List active alarms.
    """
    output.print_alarms(
        Client().alarm_history(limit = limit, query = query)
        if history else
        Client().active_alarms(limit = limit, query = query)
    )


@alarm_service.command(name = 'cancel')
@click.argument('target', type = str)
def cancel_alarms(target: str) -> None:
    """
    Cancel alarms with id. "all" for cancelling all active alarms.
    """
    if target == 'all':
        output.print_alarms(
            Client().cancel_all_alarms()
        )
    else:
        try:
            alarm_id = int(target)
        except ValueError:
            print('invalid target')
            return
        output.print_alarm(Client().cancel_alarm(alarm_id))


@alarm_service.command(name = 'ack')
@click.argument('target', type = str)
def acknowledge_alarms(target: str) -> None:
    """
    Acknowledge alarm requiring acknowledgement. You can only acknowledge commands after their target time.
    Target is either id of alarm or "all" for all acknowledgeable alarms.
    """
    if target == 'all':
        output.print_alarms(
            Client().acknowledge_all_alarms()
        )
    else:
        try:
            alarm_id = int(target)
        except ValueError:
            print('invalid target')
            return
        output.print_alarm(Client().acknowledge_alarm(alarm_id))


@main.group('todo', cls = AliasedGroup)
def todo_service() -> None:
    """
    Keep track of stuff to do.
    """
    pass


def get_default_project(project: t.Optional[str] = None) -> t.Optional[str]:
    p = project or os.environ.get('DEFP')
    return p if p else None


@todo_service.command(name = 'new')
@click.argument('text', type = str, required = True, nargs = -1)
@click.option('--project', '-p', type = str, help = 'Project.')
@click.option('--priority', '-i', default = None, type = str, help = 'Priority.')
@click.option('--tag', '-t', default = (), type = str, help = 'Tags.', multiple = True)
@click.option('--parent', '-a', default = (), type = str, help = 'Parent.', multiple = True)
def new_todo(
    text: t.Sequence[str],
    project: t.Optional[str],
    priority: t.Optional[str],
    tag: t.Sequence[str],
    parent: t.Sequence[str],
) -> None:
    """
    Create new todo.
    """
    output.print_todo(
        Client().new_todo(
            ' '.join(text),
            project = get_default_project(project),
            priority = priority,
            tags = tag,
            parents = parent,
        )
    )


@todo_service.command(name = 'mod')
@click.argument('todo', type = str, required = True)
@click.argument('description', type = str, required = False)
def change_priority(
    todo: str,
    description: t.Optional[str],
) -> None:
    """
    Modify todo description.
    """
    client = Client()
    if description is None:
        existing_todo = client.get_todo(todo)
        description = click.edit(existing_todo.text)
        if description is None:
            print('aborted')
            return
        description = description.rstrip('\n')
    output.print_todo(
        Client().modify_todo_description(todo, description)
    )


@todo_service.command(name = 'com')
@click.argument('todo', type = str, required = True)
@click.argument('comment', type = str, required = True)
def comment_todo(
    todo: str,
    comment: str,
) -> None:
    """
    Add comment to todo.
    """
    output.print_todo(
        Client().comment_todo(todo, comment)
    )


@todo_service.command(name = 'cancel')
@click.argument('target', type = str)
def cancel_todo(target: str) -> None:
    """
    Cancel todo. Target is either id or partial text of todo.
    """
    output.print_todo(Client().cancel_todo(target))


@todo_service.command(name = 'finish')
@click.argument('target', type = str)
def finish_todo(target: str) -> None:
    """
    Finish todo. Target is either id or partial text of todo.
    """
    output.print_todo(Client().finish_todo(target))


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
@click.option(
    '--limit',
    '-l',
    default = 25,
    type = int,
    help = 'Maximum number of top level todos to fetch.',
    show_default = True,
)
@click.option('--project', '-p', type = str, help = 'Specify project. If not specified, use default project.')
@click.option('--tag', '-t', type = str, help = 'Filter on tag.')
@click.option('--query', '-q', type = str, help = 'Filter on text.')
@click.option(
    '--all-tasks',
    '-a',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Include all tasks, not just top level ones.',
)
@click.option(
    '--ignore-priority',
    '-i',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Don\'t filter on priority',
)
@click.option(
    '--flat',
    '-f',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Dont show task children',
)
@click.option('--minimum-priority', '-m', default = None, type = str, help = 'Minimum priority.')
@click.option(
    '--no-comments',
    '-c',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Dont show comments',
)
def list_todos(
    history: bool = False,
    limit: int = 25,
    **kwargs,
) -> None:
    """
    List pending todos.
    """
    kwargs['project'] = get_default_project(kwargs['project'])
    no_comments = kwargs.pop('no_comments')
    output.print_todos(
        Client().todo_history(limit = limit, **kwargs)
        if history else
        Client().active_todos(**kwargs),
        show_comments = not no_comments,
    )


def _show_points(points: t.Sequence[t.Tuple[datetime.datetime, t.Union[int, float]]], chart: bool = False) -> None:
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
@click.option(
    '--all-tasks',
    '-a',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Include all tasks, not just top level ones.',
)
@click.option(
    '--ignore-priority',
    '-i',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Don\'t filter on priority',
)
@click.option('--minimum-priority', '-m', default = None, type = str, help = 'Minimum priority.')
def todos_burn_down(
    chart: bool = False,
    project: t.Optional[str] = None,
    tag: t.Optional[str] = None,
    all_tasks: bool = False,
    ignore_priority: bool = False,
    minimum_priority: t.Optional[str] = None,
) -> None:
    """
    Show todo burndown chart.
    """
    _show_points(
        Client().todo_burn_down(
            project = get_default_project(project),
            tag = tag,
            all_tasks = all_tasks,
            ignore_priority = ignore_priority,
            minimum_priority = minimum_priority,
        ),
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
@click.option(
    '--all-tasks',
    '-a',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Include all tasks, not just top level ones.',
)
@click.option(
    '--ignore-priority',
    '-i',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Don\'t filter on priority',
)
@click.option('--minimum-priority', '-m', default = None, type = str, help = 'Minimum priority.')
def todos_throughput(
    chart: bool = False,
    project: t.Optional[str] = None,
    tag: t.Optional[str] = None,
    all_tasks: bool = False,
    ignore_priority: bool = False,
    minimum_priority: t.Optional[str] = None,
) -> None:
    """
    Show todo throughput chart.
    """
    _show_points(
        Client().todo_throughput(
            project = get_default_project(project),
            tag = tag,
            all_tasks = all_tasks,
            ignore_priority = ignore_priority,
            minimum_priority = minimum_priority,
        ),
        chart,
    )


@todo_service.group('tag', cls = AliasedGroup)
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
    help = 'Add tag to all children recursively.',
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
    output.print_todo(
        Client().register_dependency(parent, task)
    )


@todo_service.group('project', cls = AliasedGroup)
def project_service() -> None:
    """
    Todo projects.
    """
    pass


@project_service.command(name = 'list')
def list_projects() -> None:
    """
    List projects.
    """
    output.print_projects(
        Client().list_projects()
    )


@project_service.command(name = 'new')
@click.argument('name', type = str, required = True)
def create_project(
    name: str,
) -> None:
    """
    Create a new project
    """
    output.print_project(
        Client().create_project(name)
    )


@project_service.command(name = 'mod')
@click.argument('name', type = str, required = True)
@click.argument('level', type = str, required = True)
def modify_project_default_priority_filter(
    name: str,
    level: str,
) -> None:
    """
    Modify default priority level for new todos
    """
    output.print_project(
        Client().modify_project_default_priority_filter(name, None if level.lower() == 'none' else level),
    )


@todo_service.group('p', cls = AliasedGroup)
def priority_service() -> None:
    """
    Todo priorities.
    """
    pass


@priority_service.command(name = 'new')
@click.argument('name', type = str, required = True)
@click.option('--project', '-p', type = str, help = 'Project.')
@click.option('--level', '-l', default = 0, type = int, help = 'Level.')
def new_priority(
    name: str,
    project: str,
    level: int,
) -> None:
    """
    Create a new priority.
    """
    output.print_priority(
        Client().new_priority(
            name = name,
            level = level,
            project = get_default_project(project),
        )
    )


@priority_service.command(name = 'swap')
@click.argument('first', type = str, required = True)
@click.argument('second', type = str, required = True)
@click.option('--project', '-p', type = str, help = 'Project.')
def swap_priority_levels(
    first: str,
    second: str,
    project: t.Optional[str],
) -> None:
    """
    Create priority levels of priorities.
    """
    output.print_priorities(
        Client().swap_priority_levels(
            first = first,
            second = second,
            project = get_default_project(project),
        )
    )


@priority_service.command(name = 'list')
@click.option('--project', '-p', type = str, help = 'Project.')
def list_priorities(project: str) -> None:
    """
    List priorities.
    """
    output.print_priorities(
        Client().list_priorities(project = get_default_project(project))
    )


@priority_service.command(name = 'mod')
@click.argument('todo', type = str, required = True)
@click.argument('priority', type = str, required = True)
@click.option(
    '--recursive',
    '-r',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Change priority of all children recursively.',
)
def change_priority(
    todo: str,
    priority: str,
    recursive: bool = False,
) -> None:
    """
    Modify todo priority.
    """
    output.print_todo(
        Client().modify_todo_priority(todo, priority, recursive = recursive)
    )


if __name__ == '__main__':
    try:
        main()
    except ClientError as e:
        print(e.message)

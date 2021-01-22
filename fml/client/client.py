import logging
import typing as t
import datetime

import requests
import click
import gnuplotlib as gp
import numpy as np
from texttable import Texttable

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
            data = data,
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

    def new_todo(
        self,
        text: str,
    ) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'todo/',
                'POST',
                {
                    'text': text,
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

    def active_todos(self) -> t.Sequence[models.ToDo]:
        return [
            models.ToDo.from_remote(todo)
            for todo in
            self._make_request('todo/')['todos']
        ]

    def todo_history(self, limit: t.Optional[int] = 25) -> t.Sequence[models.ToDo]:
        return [
            models.ToDo.from_remote(todo)
            for todo in
            self._make_request('todo/history/', limit = limit)['todos']
        ]

    def todo_burn_down(self) -> t.Sequence[t.Tuple[datetime.datetime, int]]:
        return [
            (
                datetime.datetime.strptime(date, "%d-%m-%Y"),
                active_todos,
            )
            for date, active_todos in
            self._make_request('todo/burn-down/')['points']
        ]


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


def print_todos(todos: t.Sequence[models.ToDo]) -> None:
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_max_width(180)
    table.header(
        ['ID', 'Text', 'Created At', 'Finished At', 'Elapsed', 'Duration', 'State']
    )
    table.add_rows(
        [
            [
                todo.pk,
                todo.text,
                todo.created_at.strftime(models.DATETIME_FORMAT),
                todo.finished_at.strftime(models.DATETIME_FORMAT) if todo.finished_at else '-',
                format_timedelta(todo.elapsed),
                format_timedelta(todo.duration) if todo.finished_at else '-',
                todo.status,
            ]
            for todo in
            todos
        ],
        header = False,
    )
    print(table.draw())


@click.group()
def main():
    """
    Keep track of stuff and such.
    """
    pass


@main.group('alarm')
def alarm_service():
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
    help = 'Delay in seconds for re-notification delay. Only relevant when ackowledgement is required.',
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
    retry_delay: int = 0,
    mail: bool = False,
    silent: bool = False,
    requires_acknowledgement: bool = False,
):
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
def list_alarms(history: bool = False, limit: int = 10):
    """
    List active alarms.
    """
    print_alarms(
        Client().alarm_history(limit = limit) if history else Client().active_alarms(limit = limit)
    )


@alarm_service.command(name = 'cancel')
@click.argument('target', type = str)
def cancel_alarms(target: str):
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
def acknowledge_alarms(target: str):
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
def todo_service():
    """
    Keep track of stuff to do.
    """
    pass


@todo_service.command(name = 'new')
@click.argument('text', type = str, required = True, nargs = -1)
def new_todo(
    text: t.Sequence[str],
):
    """
    Create new todo.
    """
    print_todo(
        Client().new_todo(
            ' '.join(text),
        )
    )


@todo_service.command(name = 'cancel')
@click.argument('target', type = str)
def cancel_todo(target: str):
    """
    Cancel todo. Target is either id or partial text of todo.
    """
    print_todo(Client().cancel_todo(target))


@todo_service.command(name = 'finish')
@click.argument('target', type = str)
def finish_todo(target: str):
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
def list_todos(history: bool = False, limit: int = 25):
    """
    List pending todos.
    """
    print_todos(
        Client().todo_history(limit = limit) if history else Client().active_todos()
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
def todos_burn_down(chart: bool = False):
    points = Client().todo_burn_down()

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


if __name__ == '__main__':
    try:
        main()
    except ClientError as e:
        print(e.message)

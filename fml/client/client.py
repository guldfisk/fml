import logging
import typing as t
import datetime

import requests
import click
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

    def active_alarms(self) -> t.Sequence[models.Alarm]:
        return [
            models.Alarm.from_remote(alarm)
            for alarm in
            self._make_request('alarms/')['alarms']
        ]

    def alarm_history(self) -> t.Sequence[models.Alarm]:
        return [
            models.Alarm.from_remote(alarm)
            for alarm in
            self._make_request('alarms/history/')['alarms']
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

    def todo_history(self) -> t.Sequence[models.ToDo]:
        return [
            models.ToDo.from_remote(todo)
            for todo in
            self._make_request('todo/history/')['todos']
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
        ['ID', 'Text', 'Created At', 'Finished At', 'State']
    )
    table.add_rows(
        [
            [
                todo.pk,
                todo.text,
                todo.created_at.strftime(models.DATETIME_FORMAT),
                todo.finished_at.strftime(models.DATETIME_FORMAT) if todo.finished_at else '-',
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
    pass


@main.group('alarm')
def alarm_service():
    pass


@alarm_service.command(name = 'new')
@click.argument('text', type = str)
@click.argument('absolute', default = None, type = str, required = False)
@click.option('--seconds', '-s', default = 0, type = int)
@click.option('--minutes', '-m', default = 0, type = int)
@click.option('--hours', '-h', default = 0, type = int)
@click.option('--retry-delay', default = 60, type = int)
@click.option('--mail', default = False, type = bool, is_flag = True, show_default = True)
@click.option('--silent', default = False, type = bool, is_flag = True, show_default = True)
@click.option('--requires-acknowledgement', '--ack', default = False, type = bool, is_flag = True, show_default = True)
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
@click.option('--history', '-h', default = False, type = bool, is_flag = True, show_default = True)
def list_alarms(history: bool = False):
    print_alarms(
        Client().alarm_history() if history else Client().active_alarms()
    )


@alarm_service.command(name = 'cancel')
@click.argument('target', type = str)
def cancel_alarms(target: str):
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
    pass


@todo_service.command(name = 'new')
@click.argument('text', type = str, required = True, nargs = -1)
def new_todo(
    text: t.Sequence[str],
):
    print_todo(
        Client().new_todo(
            ' '.join(text),
        )
    )


@todo_service.command(name = 'cancel')
@click.argument('target', type = str)
def cancel_todo(target: str):
    print_todo(Client().cancel_todo(target))


@todo_service.command(name = 'finish')
@click.argument('target', type = str)
def finish_todo(target: str):
    print_todo(Client().finish_todo(target))


@todo_service.command(name = 'list')
@click.option('--history', '-h', default = False, type = bool, is_flag = True, show_default = True)
def list_todos(history: bool = False):
    print_todos(
        Client().todo_history() if history else Client().active_todos()
    )


if __name__ == '__main__':
    try:
        main()
    except ClientError as e:
        print(e.message)

import logging
import typing as t
import argparse
import datetime
import requests

from texttable import Texttable

from fml.client import models
from fml.client.models import DATETIME_FORMAT


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
        response.raise_for_status()
        return response.json()

    def new_alarm(self, text: str, end_at: datetime.datetime, mail: bool = False, silent: bool = False) -> models.Alarm:
        return models.Alarm.from_remote(
            self._make_request(
                'alarm/',
                'POST',
                {
                    'text': text,
                    'end_at': end_at.strftime('%d/%m/%Y %H:%M:%S'),
                    'send_email': mail,
                    'silent': silent,

                }
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
            self._make_request('alarms/cancel/', 'POST')['alarms']
        ]


def print_alarm(alarm: models.Alarm) -> None:
    print_alarms((alarm,))


def print_alarms(alarms: t.Sequence[models.Alarm]) -> None:
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_max_width(180)
    table.header(
        ['ID', 'Text', 'Start', 'End', 'ETA', 'flags', 'status']
    )
    table.add_rows(
        [
            [
                alarm.pk,
                alarm.text,
                alarm.started_at.strftime(models.DATETIME_FORMAT),
                alarm.end_at.strftime(models.DATETIME_FORMAT),
                alarm.eta,
                ' '.join(alarm.flags),
                alarm.status,
            ]
            for alarm in
            alarms
        ],
        header = False,
    )
    print(table.draw())


def new(args: argparse.Namespace):
    print_alarm(
        Client().new_alarm(
            args.text,
            (
                datetime.datetime.now() +
                datetime.timedelta(
                    seconds = args.seconds,
                    minutes = args.minutes,
                    hours = args.hours,
                )
            ) if args.absolute is None else
            datetime.datetime.strptime(
                args.absolute,
                DATETIME_FORMAT,
            ),
            mail = args.mail,
            silent = args.silent,
        )
    )


def list_alarms(args: argparse.Namespace):
    print_alarms(
        Client().alarm_history() if args.history else Client().active_alarms()
    )


def cancel_all(args: argparse.Namespace):
    for alarm in Client().cancel_all_alarms():
        print_alarm(alarm)


def invoke():
    parser = argparse.ArgumentParser(description = 'Alarms', add_help = False)

    subparsers = parser.add_subparsers()

    parser_new = subparsers.add_parser('new', add_help = False)
    parser_new.add_argument('text', type = str)
    parser_new.add_argument(
        '-s', '--seconds',
        type = int,
        default = 0,
    )
    parser_new.add_argument(
        '-m', '--minutes',
        type = int,
        default = 0,
    )
    parser_new.add_argument(
        '-h', '--hours',
        type = int,
        default = 0,
    )
    parser_new.add_argument(
        '-a', '--absolute',
        type = str,
        default = None,
    )
    parser_new.add_argument(
        '--mail',
        action = 'store_true',
        default = False,
    )
    parser_new.add_argument(
        '--silent',
        action = 'store_true',
        default = False,
    )

    parser_new.set_defaults(command = new)

    parser_list = subparsers.add_parser('list')
    parser_list.add_argument(
        '--history',
        action = 'store_true',
        default = False,
    )
    parser_list.set_defaults(command = list_alarms)

    parser_list = subparsers.add_parser('cancel_all')
    parser_list.set_defaults(command = cancel_all)

    args = parser.parse_args()

    try:
        command = args.command
    except AttributeError:
        print('no command selected')
        return

    command(args)


if __name__ == '__main__':
    invoke()

import datetime
import typing as t

import click

from fml.client import output
from fml.client.cli.common import AliasedGroup, main, split_text_option, force_option
from fml.client.client import Client
from fml.client.dtmath.parse import DTMParseException


@main.group('alarm', cls = AliasedGroup)
def alarm_service() -> None:
    """
    Timed alarms.
    """
    pass


@alarm_service.command(name = 'new')
@split_text_option('text')
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
@click.option(
    '--silent',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Don\'t play sound.',
)
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
    text: t.Sequence[str],
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
        from fml.client.dtmath.parse import DTMParser
        try:
            base_datetime = DTMParser().parse(absolute)
        except (DTMParseException, ValueError) as e:
            print(e)
            return
        except TypeError:
            print('can\'t add dates')
            return
        if isinstance(base_datetime, datetime.timedelta):
            base_datetime += datetime.datetime.now()
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
            ' '.join(text),
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
@split_text_option()
@force_option
def cancel_alarms(target: t.Sequence[str], force: bool) -> None:
    """
    Cancel alarms by id or a unique identifying string. "all" for cancelling all active alarms.
    """
    target = ' '.join(target)
    if target == 'all':
        if not force:
            active_alarms = Client().active_alarms()
            if len(active_alarms) > 1:
                output.print_alarms(active_alarms)
                if not click.confirm('Cancel these alarms?', default = False):
                    return
        output.print_alarms(
            Client().cancel_all_alarms()
        )
    else:
        output.print_alarm(Client().cancel_alarm(target))


@alarm_service.command(name = 'ack')
@split_text_option()
def acknowledge_alarms(target: str) -> None:
    """
    Acknowledge alarm requiring acknowledgement. You can only acknowledge alarms after their target time.
    Target is either id of alarm, a unique identifying string or "all" for all acknowledgeable alarms.
    """
    target = ' '.join(target)
    if target == 'all':
        output.print_alarms(
            Client().acknowledge_all_alarms()
        )
    else:
        output.print_alarm(Client().acknowledge_alarm(target))


@alarm_service.command(name = 'snooze')
@split_text_option()
@click.argument('new_target_time', default = None, type = str)
def snooze_alarm(target: str, new_target_time: str) -> None:
    """
    Snooze alarm requiring acknowledgement. You can only snooze alarms after their target time.
    Target is either id of alarm or a uniquely identifying string.
    """
    from fml.client.dtmath.parse import DTMParser

    try:
        new_target_time = DTMParser().parse(new_target_time)
    except (DTMParseException, ValueError) as e:
        print(e)
        return
    except TypeError:
        print('can\'t add dates')
        return

    if isinstance(new_target_time, datetime.timedelta):
        new_target_time += datetime.datetime.now()

    if new_target_time < datetime.datetime.now():
        print('alarm must be scheduled for future')
        return

    output.print_alarm(Client().snooze_alarm(' '.join(target), new_target_time))

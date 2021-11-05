import datetime
import typing as t

import click

from fml.client.cli.common import main, split_text_option
from fml.client.utils import format_timedelta, format_timedelta_years
from fml.client.values import FULL_DATETIME_FORMAT


@main.command(name = 'dt')
@split_text_option('args')
@click.option(
    '--format-years',
    '-y',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Approximate years as 365 days when formatting time delta.',
)
def dt_math(args: t.Sequence[str], format_years: bool):
    """
    Datetime calculator.
    Time to next year: ".1/jan - n".
    """
    from fml.client.dtmath.parse import DTMParser, DTMParseException
    import re

    s = re.sub('{(.*?)}', lambda m: str(eval(m.group(1))), ' '.join(args))
    try:
        result = DTMParser().parse(s)
    except (DTMParseException, ValueError) as e:
        print(e)
    except TypeError:
        print('can\'t add dates')
    else:
        if isinstance(result, datetime.timedelta):
            print(
                'delta: ' + (
                    format_timedelta_years
                    if format_years else
                    format_timedelta
                )(result)
            )
        else:
            print('time: ' + result.strftime(FULL_DATETIME_FORMAT))

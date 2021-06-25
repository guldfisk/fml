# encoding: utf-8

import datetime
import re


PATTERN = re.compile(
    r'((((\d{1,2})/((\d{1,2})|([a-zøæå]+))?(/(\d{4}))?)|(\+(\d+)))|([a-zøæå]+))?'
    r'[\s-]*(((\d{2})(\d{2}))|((\d{1,2})(:(\d{1,2}))?(:(\d{1,2}))?))?$',
    re.IGNORECASE,
)

WEEKDAY_NAMES = (
    ('mon', 'man', 'monday', 'mandag'),
    ('tue', 'tir', 'tuesday', 'tirsdag'),
    ('wed', 'ons', 'wednesday', 'onsdag'),
    ('thu', 'tor', 'thursday', 'torsdag'),
    ('fri', 'fre', 'friday', 'fredag'),
    ('sat', 'lør', 'saturday', 'lørdag'),
    ('sun', 'søn', 'sunday', 'søndag'),
)

MONTH_NAMES = (
    ('jan', 'january', 'januar'),
    ('feb', 'february', 'februar'),
    ('mar', 'march', 'marts'),
    ('apr', 'april'),
    ('may', 'maj'),
    ('jun', 'june', 'juni'),
    ('jul', 'july', 'juli'),
    ('aug', 'august'),
    ('sep', 'september'),
    ('oct', 'okt', 'october', 'oktober'),
    ('nov', 'november'),
    ('dec', 'december'),
)

WEEKDAY_MAP = {}

for idx, names in enumerate(WEEKDAY_NAMES):
    for name in names:
        WEEKDAY_MAP[name] = idx

MONTH_MAP = {}

for idx, names in enumerate(MONTH_NAMES):
    for name in names:
        MONTH_MAP[name] = idx


class DateParseException(Exception):
    pass


def get_next_weekday(weekday: str) -> datetime.datetime:
    try:
        target_weekday = WEEKDAY_MAP[weekday.lower()]
    except KeyError:
        raise DateParseException('Invalid weekday')
    now = datetime.datetime.now()
    current_weekday = now.weekday()
    return now + datetime.timedelta(
        days = (
            target_weekday - current_weekday
            if target_weekday > current_weekday else
            7 - current_weekday + target_weekday
        )
    )


def get_next_month(month: str, target_time: datetime.datetime) -> datetime.datetime:
    try:
        target_month = MONTH_MAP[month.lower()]
    except KeyError:
        raise DateParseException('Invalid month')

    now = datetime.datetime.now()
    target_time = target_time.replace(month = target_month + 1)
    if target_time < now:
        return target_time.replace(year = now.year + 1)
    return target_time


def parse_datetime(s: str) -> datetime.datetime:
    m = PATTERN.match(s)

    if m is None:
        raise DateParseException('invalid date')

    (
        _, _, _, day, month, month_number, month_name, _, year, _, day_delta, weekday,
        _, _, _hour, _minute, _, hour, _, minute, _, second
    ) = m.groups()

    try:
        current_date = (
            get_next_weekday(weekday) if weekday is not None else datetime.datetime.now()
        ).replace(
            **{
                k: v
                for k, v in
                {
                    'year': None if year is None else int(year),
                    'month': None if month is None or month_name is not None else int(month),
                    'day': None if day is None else int(day),
                    'hour': int(_hour or hour or 0),
                    'minute': int(_minute or minute or 0),
                    'second': 0 if second is None else int(second),
                }.items()
                if v is not None
            }
        )
    except ValueError as e:
        raise DateParseException(e)

    if month_name:
        current_date = get_next_month(month_name, current_date)

    return current_date + datetime.timedelta(days = 0 if day_delta is None else int(day_delta))

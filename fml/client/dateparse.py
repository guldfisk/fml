# encoding: utf-8

import datetime
import re


PATTERN = re.compile(
    r'((((\d{1,2})/(\d{1,2})?(/(\d{4}))?)|(\+(\d+)))|(\w+))?'
    r'[\s-]*(((\d{2})(\d{2}))|((\d{1,2})(:(\d{1,2}))?(:(\d{1,2}))?))$',
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

WEEKDAY_MAP = {}

for idx, names in enumerate(WEEKDAY_NAMES):
    for name in names:
        WEEKDAY_MAP[name] = idx


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
            if target_weekday >= current_weekday else
            6 - current_weekday + target_weekday
        )
    )


def parse_datetime(s: str) -> datetime.datetime:
    m = PATTERN.match(s)

    if m is None:
        raise DateParseException('invalid date')

    _, _, _, day, month, _, year, _, day_delta, weekday, _, _, _hour, _minute, _, hour, _, minute, _, second = m.groups()
    current_date = get_next_weekday(weekday) if weekday is not None else datetime.datetime.now()

    return datetime.datetime(
        year = current_date.year if year is None else int(year),
        month = current_date.month if month is None else int(month),
        day = current_date.day if day is None else int(day),
        hour = int(_hour or hour or 0),
        minute = int(_minute or minute or 0),
        second = 0 if second is None else int(second),
    ) + datetime.timedelta(days = 0 if day_delta is None else int(day_delta))

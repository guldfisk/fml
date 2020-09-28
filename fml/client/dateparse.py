import datetime
import re


PATTERN = re.compile(r'((\d{1,2})/(\d{1,2})?(/(\d{4}))?)?[\s-]*(\d{1,2})(:(\d{1,2}))?(:(\d{1,2}))?$')


class DateParseException(Exception):
    pass


def parse_datetime(s: str) -> datetime.datetime:
    m = PATTERN.match(s)

    if m is None:
        raise DateParseException('invalid date')

    _, day, month, _, year, hour, _, minute, _, second = m.groups()
    current_date = datetime.datetime.now()

    return datetime.datetime(
        year = current_date.year if year is None else int(year),
        month = current_date.month if month is None else int(month),
        day = current_date.day if day is None else int(day),
        hour = 0 if hour is None else int(hour),
        minute = 0 if minute is None else int(minute),
        second = 0 if second is None else int(second),
    )

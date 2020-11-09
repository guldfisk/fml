import datetime
import re


PATTERN = re.compile(
    r'(((\d{1,2})/(\d{1,2})?(/(\d{4}))?)|(\+(\d+)))?[\s-]*(((\d{2})(\d{2}))|((\d{1,2})(:(\d{1,2}))?(:(\d{1,2}))?))$'
)


class DateParseException(Exception):
    pass


def parse_datetime(s: str) -> datetime.datetime:
    m = PATTERN.match(s)

    if m is None:
        raise DateParseException('invalid date')

    _, _, day, month, _, year, _, day_delta, _, _, _hour, _minute, _, hour, _, minute, _, second = m.groups()
    current_date = datetime.datetime.now()

    return datetime.datetime(
        year = current_date.year if year is None else int(year),
        month = current_date.month if month is None else int(month),
        day = current_date.day if day is None else int(day),
        hour = int(_hour or hour or 0),
        minute = int(_minute or minute or 0),
        second = 0 if second is None else int(second),
    ) + datetime.timedelta(days=0 if day_delta is None else int(day_delta))

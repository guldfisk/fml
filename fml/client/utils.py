import datetime


def format_timedelta(delta: datetime.timedelta) -> str:
    return str(delta).split('.')[0]

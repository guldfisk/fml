import datetime


def get_weekday(weekday: int, now: datetime.datetime) -> datetime.datetime:
    return now + datetime.timedelta(
        days = weekday - now.weekday()
    )


def get_next_weekday(weekday: int, now: datetime.datetime) -> datetime.datetime:
    current_weekday = now.weekday()
    return now + datetime.timedelta(
        days = (
            weekday - current_weekday
            if weekday > current_weekday else
            7 - current_weekday + weekday
        )
    )

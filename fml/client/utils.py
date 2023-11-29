import datetime


def plural(n):
    return abs(n) != 1 and "s" or ""


def format_timedelta(delta: datetime.timedelta) -> str:
    mm, ss = divmod(delta.seconds, 60)
    hh, mm = divmod(mm, 60)
    s = f"{hh:d}:{mm:02d}:{ss:02d}"

    if delta.days:
        s = f"{delta.days:d} day{plural(delta.days)}, " + s

    return s


def format_timedelta_years(delta: datetime.timedelta) -> str:
    mm, ss = divmod(delta.seconds, 60)
    hh, mm = divmod(mm, 60)
    s = f"{hh:d}:{mm:02d}:{ss:02d}"

    if delta.days:
        y, d = divmod(delta.days, 365)

        s = f"{d:d} day{plural(d)}, " + s

        if y:
            s = f"{y:d} year{plural(y)}, " + s

    return s

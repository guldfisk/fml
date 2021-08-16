from enum import Enum


DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'
ALARM_DATETIME_FORMAT = '%d/%m/%Y %a %H:%M:%S'

LINE_BG_COLOR = '#101010'
LINE_BG_COLOR_ALTERNATE = '#303030'

C_PENDING = '#aa9bf3'
C_ERROR = '#fb3957'
C_ALERT = '#f59947'
C_IMPORTANT = '#f9f57a'
C_SUCCESS = '#5fef66'
C_NEUTRAL = '#bfdcf5'
C_WHITE = '#ffffff'


class State(Enum):
    PENDING = 'pending'
    WAITING = 'waiting'
    COMPLETED = 'completed'
    CANCELED = 'canceled'


STATUS_COLOR_MAP = {
    State.PENDING: C_PENDING,
    State.WAITING: C_NEUTRAL,
    State.COMPLETED: C_SUCCESS,
    State.CANCELED: C_ERROR,
}

PRIORITY_COLOR_MAP = {
    0: C_ERROR,
    1: C_ALERT,
    2: C_IMPORTANT,
    3: C_SUCCESS,
    4: C_PENDING,
}

ALARM_STATUS_COLOR_MAP = {
    'PENDING': C_PENDING,
    'COMPLETED': C_SUCCESS,
    'CANCELED': C_ERROR,
    'AWAITING_ACKNOWLEDGEMENT': C_ALERT,
    'COMPLETED_LATE': C_IMPORTANT,
}

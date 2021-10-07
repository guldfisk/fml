from enum import Enum


class OutputMode(Enum):
    TABLE = 'table'
    LIST = 'list'


class Context(object):
    output_mode = OutputMode.TABLE

from enum import Enum


class OutputMode(Enum):
    TABLE = "table"
    LIST = "list"
    JSON = "json"


class Context(object):
    output_mode = OutputMode.TABLE

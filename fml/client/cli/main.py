from fml.client.cli.common import main
from fml.client.client import ClientError

from alarms import alarm_service  # noqa F401
from dtmath import dt_math  # noqa F401
from todos import todo_service  # noqa F401
from ci import ci_service  # noqa F401


if __name__ == "__main__":
    try:
        main()
    except ClientError as e:
        e.show()

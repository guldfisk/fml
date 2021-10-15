from fml.client.cli.common import main
from fml.client.client import ClientError

from alarms import alarm_service
from dtmath import dt_math
from todos import todo_service
from ci import ci_service


if __name__ == '__main__':
    try:
        main()
    except ClientError as e:
        e.show()

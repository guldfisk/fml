import datetime
import json
import logging
import typing as t
from abc import abstractmethod

import requests
from rich import print as rich_print
from rich.style import Style
from rich.text import Text

from fml.client import models, values
from fml.client import output


class ClientError(Exception):

    @property
    @abstractmethod
    def message(self) -> str:
        pass

    def show(self):
        rich_print(
            Text(
                self.message,
                style = Style(color = values.C_ERROR),
            )
        )


class SimpleClientError(ClientError):

    def __init__(self, message: str) -> None:
        super().__init__()
        self._message = message

    @property
    def message(self) -> str:
        return self._message


class ErrorMessage(ClientError):

    def __init__(self, message: t.Any) -> None:
        super().__init__()
        self._message = message

    @property
    def message(self) -> str:
        return self._message['message']


class ClientJsonError(ClientError):

    def __init__(self, message: t.Any) -> None:
        super().__init__()
        self._message = message

    @property
    def message(self) -> str:
        return json.dumps(self._message, indent = 4)


class ClientMultiObjectContext(ClientError):
    type_view_map = {
        'todo': (models.ToDo, output.print_todos),
        'alarm': (models.Alarm, output.print_alarms),
        'priority': (models.Priority, output.print_priorities),
        'tag': (models.Tag, output.print_tags),
        'project': (models.Project, output.print_projects),
    }

    def __init__(self, message: t.Any) -> None:
        super().__init__()
        self._message = message

    @property
    def message(self) -> str:
        return self._message['message']

    def show(self):
        candidate_class, candidate_printer = self.type_view_map.get(self._message['candidate_type'], (None, None))
        if not candidate_class:
            print('unknown candidate type "{}"'.format(self._message['candidate_type']))
        else:
            candidate_printer(
                [candidate_class.from_remote(c) for c in self._message['candidates']],
                title = Text(
                    self.message,
                    style = Style(color = values.C_ERROR),
                ),
            )


EXCEPTION_TYPE_MAP = {
    'multiple_candidate_error': ClientMultiObjectContext,
    'error_message': ErrorMessage,
}


class Client(object):

    def __init__(self, host: str = 'localhost:8888'):
        self._host = host

    def _make_request(
        self,
        endpoint: str,
        method: str = 'GET',
        data: t.Optional[t.Mapping[str, t.Any]] = None,
        **kwargs,
    ) -> t.Any:
        if data is None:
            data = {}

        url = f'http://{self._host}/{endpoint}'

        logging.info('{} {} {}'.format(method, url, kwargs))

        response = requests.request(
            method,
            url,
            json = data,
            params = kwargs,
        )
        try:
            response.raise_for_status()
        except Exception:
            try:
                message = response.json()
                if message.get('error_type') in EXCEPTION_TYPE_MAP:
                    raise EXCEPTION_TYPE_MAP[message['error_type']](message)
                raise ClientJsonError(message)
            except ValueError:
                raise SimpleClientError(
                    response.content.decode('utf-8')
                    if isinstance(response.content, bytes) else
                    str(response.content)
                )
        return response.json()

    def ding(self) -> t.Any:
        return self._make_request(
            'alarms/ding/',
            'POST',
        )

    def new_alarm(
        self,
        text: str,
        end_at: datetime.datetime,
        mail: bool = False,
        silent: bool = False,
        requires_acknowledgment: bool = False,
        retry_delay: int = 60,
    ) -> models.Alarm:
        return models.Alarm.from_remote(
            self._make_request(
                'alarms/',
                'POST',
                {
                    'text': text,
                    'end_at': end_at.strftime('%d/%m/%Y %H:%M:%S'),
                    'send_email': mail,
                    'silent': silent,
                    'requires_acknowledgment': requires_acknowledgment,
                    'retry_delay': retry_delay,
                }
            )
        )

    def cancel_alarm(self, target: t.Union[str, int]) -> models.Alarm:
        return models.Alarm.from_remote(
            self._make_request(
                'alarms/cancel/',
                'PATCH',
                {'target': target},
            )
        )

    def acknowledge_alarm(self, target: t.Union[str, int]) -> models.Alarm:
        return models.Alarm.from_remote(
            self._make_request(
                'alarms/acknowledge/',
                'PATCH',
                {'target': target},
            )
        )

    def snooze_alarm(self, target: t.Union[str, int], new_target_time: datetime.datetime) -> models.Alarm:
        return models.Alarm.from_remote(
            self._make_request(
                'alarms/snooze/',
                'PATCH',
                {
                    'target': target,
                    'new_target_time': new_target_time.strftime('%d/%m/%Y %H:%M:%S'),
                },
            )
        )

    def active_alarms(self, limit: t.Optional[int] = None, query: t.Optional[str] = None) -> t.Sequence[models.Alarm]:
        return [
            models.Alarm.from_remote(alarm)
            for alarm in
            self._make_request('alarms/', limit = limit, query = query)['alarms']
        ]

    def alarm_history(self, limit: t.Optional[int] = 10, query: t.Optional[str] = None) -> t.Sequence[models.Alarm]:
        return [
            models.Alarm.from_remote(alarm)
            for alarm in
            self._make_request('alarms/history/', limit = limit, query = query)['alarms']
        ]

    def cancel_all_alarms(self) -> t.Sequence[models.Alarm]:
        return [
            models.Alarm.from_remote(alarm)
            for alarm in
            self._make_request('alarms/cancel/', 'PATCH')['alarms']
        ]

    def acknowledge_all_alarms(self) -> t.Sequence[models.Alarm]:
        return [
            models.Alarm.from_remote(alarm)
            for alarm in
            self._make_request('alarms/acknowledge/all/', 'PATCH')['alarms']
        ]

    def create_project(
        self,
        name: str,
    ) -> models.Project:
        return models.Project.from_remote(
            self._make_request(
                'project/',
                'POST',
                {
                    'name': name,
                    'is_default': False,
                }
            )
        )

    def modify_project_default_priority_filter(
        self,
        project: t.Union[int, str],
        default_priority_filter: t.Union[int, str, None],
    ) -> models.Project:
        return models.Project.from_remote(
            self._make_request(
                'project/',
                method = 'PATCH',
                data = {
                    'project': project,
                    'default_priority_filter': default_priority_filter,
                }
            )
        )

    def list_projects(self, limit: t.Optional[int] = 25) -> t.Sequence[models.Project]:
        return [
            models.Project.from_remote(project)
            for project in
            self._make_request('project/', limit = limit)['projects']
        ]

    def list_priorities(
        self,
        project: t.Union[str, int, None],
        limit: t.Optional[int] = 25,
    ) -> t.Sequence[models.Priority]:
        return [
            models.Priority.from_remote(project)
            for project in
            self._make_request('priorities/', limit = limit, project = project)['priorities']
        ]

    def new_todo(
        self,
        text: str,
        project: t.Optional[str] = None,
        priority: t.Optional[str] = None,
        tags: t.Collection[str] = (),
        parents: t.Collection[str] = (),
    ) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'todo/',
                'POST',
                {
                    'text': text,
                    'project': project,
                    'priority': priority,
                    'tags': tags,
                    'parents': parents,
                }
            )
        )

    def get_todo(self, todo: t.Union[str, int], project: t.Union[str, int, None] = None) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'todo/single/',
                target = todo,
                project = project,
            )
        )

    def new_priority(
        self,
        name: str,
        level: int,
        project: t.Union[str, int, None],
        is_default: bool = False,
    ) -> models.Priority:
        return models.Priority.from_remote(
            self._make_request(
                'priorities/',
                'POST',
                {
                    'name': name,
                    'project': project,
                    'level': level,
                    'is_default': is_default,
                }
            )
        )

    def cancel_todo(self, target: str, project: t.Optional[str] = None) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'todo/cancel/',
                'PATCH',
                {'target': target, 'project': project},
            )
        )

    def toggle_todo_waiting(self, target: str, project: t.Optional[str] = None) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'todo/toggle-wait/',
                'PATCH',
                {'target': target, 'project': project},
            )
        )

    def finish_todo(self, target: str, project: t.Optional[str] = None) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'todo/finish/',
                'PATCH',
                {'target': target, 'project': project},
            )
        )

    def active_todos(
        self,
        project: t.Optional[str] = None,
        tag: t.Optional[str] = None,
        query: t.Optional[str] = None,
        all_tasks: bool = False,
        flat: bool = False,
        minimum_priority: t.Union[str, int, None] = None,
        ignore_priority: bool = False,
        state: t.Optional[str] = None,
        order_by: t.Optional[t.Sequence[str]] = None,
    ) -> t.Sequence[models.ToDo]:
        return [
            models.ToDo.from_remote(todo)
            for todo in
            self._make_request(
                'todo/',
                data = {
                    'project': project,
                    'tag': tag,
                    'query': query,
                    'all_tasks': all_tasks,
                    'flat': flat,
                    'minimum_priority': minimum_priority,
                    'ignore_priority': ignore_priority,
                    'state': state,
                    'order_by': order_by,
                },
            )['todos']
        ]

    def todo_history(
        self,
        limit: t.Optional[int] = 25,
        project: t.Optional[str] = None,
        tag: t.Optional[str] = None,
        query: t.Optional[str] = None,
        all_tasks: bool = False,
        flat: bool = False,
        minimum_priority: t.Union[str, int, None] = None,
        ignore_priority: bool = False,
        state: t.Optional[str] = None,
        order_by: t.Optional[t.Sequence[str]] = None,
    ) -> t.Sequence[models.ToDo]:
        return [
            models.ToDo.from_remote(todo)
            for todo in
            self._make_request(
                'todo/history/',
                data = {
                    'limit': limit,
                    'project': project,
                    'tag': tag,
                    'query': query,
                    'all_tasks': all_tasks,
                    'flat': flat,
                    'minimum_priority': minimum_priority,
                    'ignore_priority': ignore_priority,
                    'state': state,
                    'order_by': order_by,
                }
            )['todos']
        ]

    def todo_burn_down(
        self,
        project: t.Optional[str] = None,
        tag: t.Optional[str] = None,
        all_tasks: bool = False,
        ignore_priority: bool = False,
        minimum_priority: t.Optional[str] = None,
        last_n_days: int = 128,
    ) -> t.Sequence[t.Tuple[datetime.datetime, int]]:
        return [
            (
                datetime.datetime.strptime(date, models.DATETIME_FORMAT),
                active_todos,
            )
            for date, active_todos in
            self._make_request(
                'todo/burn-down/',
                project = project,
                tag = tag,
                top_level_only = not all_tasks,
                ignore_priority = ignore_priority,
                minimum_priority = minimum_priority,
                last_n_days = last_n_days,
            )['points']
        ]

    def todo_throughput(
        self,
        project: t.Optional[str] = None,
        tag: t.Optional[str] = None,
        all_tasks: bool = False,
        ignore_priority: bool = False,
        minimum_priority: t.Optional[str] = None,
        last_n_days: int = 128,
    ) -> t.Sequence[t.Tuple[datetime.datetime, int]]:
        return [
            (
                datetime.datetime.strptime(date, models.DATETIME_FORMAT),
                throughput,
            )
            for date, throughput in
            self._make_request(
                'todo/throughput/',
                project = project,
                tag = tag,
                top_level_only = not all_tasks,
                ignore_priority = ignore_priority,
                minimum_priority = minimum_priority,
                last_n_days = last_n_days,
            )['points']
        ]

    def list_tags(self) -> t.Sequence[models.Tag]:
        return [
            models.Tag.from_remote(tag)
            for tag in
            self._make_request('tag/')['tags']
        ]

    def create_tag(self, tag: str) -> None:
        self._make_request(
            'tag/',
            method = 'POST',
            data = {
                'name': tag,
            }
        )

    def tag_todo(
        self,
        todo: t.Union[int, str],
        tag: t.Union[int, str],
        project: t.Union[int, str, None],
        recursive: bool = False,
    ) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'todo/tag/',
                method = 'POST',
                data = {
                    'todo_target': todo,
                    'tag_target': tag,
                    'project': project,
                    'recursive': recursive,
                }
            )
        )

    def comment_todo(
        self,
        todo: t.Union[int, str],
        comment: str,
        project: t.Union[int, str, None] = None,
    ) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'todo/comment/',
                method = 'POST',
                data = {
                    'target': todo,
                    'project': project,
                    'comment': comment,
                }
            )
        )

    def modify_todo_priority(
        self,
        todo: t.Union[int, str],
        priority: t.Union[int, str],
        project: t.Optional[str] = None,
        recursive: bool = False,
    ) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'priorities/modify',
                method = 'PATCH',
                data = {
                    'todo': todo,
                    'priority': priority,
                    'project': project,
                    'recursive': recursive,
                }
            )
        )

    def modify_todo_description(
        self,
        todo: t.Union[int, str],
        description: str,
        project: t.Union[int, str, None] = None,
    ) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'todo/description/',
                method = 'PATCH',
                data = {
                    'target': todo,
                    'project': project,
                    'description': description,
                }
            )
        )

    def register_dependency(self, parent: t.Union[int, str], child: t.Union[int, str]) -> models.ToDo:
        return models.ToDo.from_remote(
            self._make_request(
                'todo/add-dependency/',
                method = 'POST',
                data = {
                    'parent': parent,
                    'child': child,
                }
            )
        )

    def swap_priority_levels(
        self,
        first: t.Union[int, str],
        second: t.Union[int, str],
        project: t.Union[int, str, None] = None,
    ) -> t.Sequence[models.Priority]:
        return [
            models.Priority.from_remote(project)
            for project in
            self._make_request(
                'priorities/swap-levels',
                method = 'PATCH',
                data = {
                    'first': first,
                    'second': second,
                    'project': project,
                }
            )['priorities']
        ]

    def ci_watch(self, run_id: t.Union[str, int], superseed: bool = False) -> models.CIChecker:
        return models.CIChecker.from_remote(
            self._make_request(
                'ci/watch/',
                'POST',
                {
                    'run_id': run_id,
                    'superseed': superseed,
                }
            )
        )

    def ci_watching(self) -> t.Sequence[models.CIChecker]:
        return [
            models.CIChecker.from_remote(checker)
            for checker in
            self._make_request(
                'ci/watching/',
            )['ci_checkers']
        ]

    def latest_ci_token(self) -> t.Mapping[str, str]:
        return self._make_request(
            'ci/latest-token/',
        )

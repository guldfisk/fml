from __future__ import annotations

import dataclasses
import datetime
import typing as t

from abc import ABC, abstractmethod

from fml.client.utils import format_timedelta
from fml.client.values import DATETIME_FORMAT, State


Serialized = t.Mapping[str, t.Any]


class RemoteModel(ABC):
    pk: t.Union[str, int]

    @classmethod
    @abstractmethod
    def from_remote(cls, remote: Serialized) -> RemoteModel:
        pass

    def __hash__(self) -> int:
        return hash((self.__class__, self.pk))

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.pk == other.pk
        )


@dataclasses.dataclass
class Alarm(RemoteModel):
    pk: int
    text: str
    started_at: datetime.datetime
    end_at: datetime.datetime
    next_reminder_time_target: t.Optional[datetime.datetime]
    requires_acknowledgment: bool
    send_email: bool
    silent: bool
    level: str
    times_notified: int
    acknowledged: bool
    canceled: bool
    success: bool

    @classmethod
    def from_remote(cls, remote: Serialized) -> Alarm:
        return cls(
            pk = remote['id'],
            text = remote['text'],
            started_at = datetime.datetime.strptime(remote['started_at'], DATETIME_FORMAT),
            end_at = datetime.datetime.strptime(remote['end_at'], DATETIME_FORMAT),
            next_reminder_time_target = (
                datetime.datetime.strptime(remote['next_reminder_time_target'], DATETIME_FORMAT)
                if remote['next_reminder_time_target'] else
                None
            ),
            requires_acknowledgment = remote['requires_acknowledgment'],
            send_email = remote['send_email'],
            silent = remote['silent'],
            level = remote['level'],
            times_notified = remote['times_notified'],
            acknowledged = remote['acknowledged'],
            canceled = remote['canceled'],
            success = remote['success'],
        )

    @property
    def flags(self) -> t.Iterator[str]:
        if self.silent:
            yield 'silent'
        if self.send_email:
            yield 'mail'
        if self.requires_acknowledgment:
            yield 'ack'

    @property
    def status(self) -> str:
        if self.canceled:
            return 'CANCELED'
        if self.requires_acknowledgment and not self.acknowledged and self.times_notified:
            return 'AWAITING_ACKNOWLEDGEMENT'
        if (
            self.requires_acknowledgment and self.acknowledged
            or not self.requires_acknowledgment and self.times_notified
        ):
            if self.success:
                return 'COMPLETED'
            return 'COMPLETED_LATE'
        return 'PENDING'

    @property
    def next_target_time(self) -> datetime.datetime:
        return self.next_reminder_time_target or self.end_at

    @property
    def eta(self) -> str:
        eta = self.next_target_time - datetime.datetime.now()
        if eta.total_seconds() > 0:
            return format_timedelta(eta) + (' (reminder)' if self.next_reminder_time_target else '')
        return '-'

    @property
    def elapsed(self) -> datetime.timedelta:
        return max(datetime.datetime.now() - self.started_at, datetime.timedelta(seconds = 0))

    @property
    def duration(self) -> datetime.timedelta:
        return self.end_at - self.started_at


class Project(RemoteModel):

    def __init__(
        self,
        pk: int,
        name: str,
        created_at: datetime.datetime,
        is_default: bool = True,
        default_priority_filter: t.Optional[int] = None,
    ):
        self._pk = pk
        self._name = name
        self._created_at = created_at
        self._is_default = is_default
        self._default_priority_filter = default_priority_filter

    @property
    def pk(self) -> int:
        return self._pk

    @property
    def name(self) -> str:
        return self._name

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

    @property
    def is_default(self) -> bool:
        return self._is_default

    @property
    def default_priority_filter(self) -> t.Optional[int]:
        return self._default_priority_filter

    @classmethod
    def from_remote(cls, remote: Serialized) -> Project:
        return cls(
            pk = remote['id'],
            name = remote['name'],
            created_at = datetime.datetime.strptime(remote['created_at'], DATETIME_FORMAT),
            is_default = remote['is_default'],
            default_priority_filter = remote['default_priority_filter'],
        )


class Priority(RemoteModel):

    def __init__(
        self,
        pk: int,
        name: str,
        project: str,
        level: int,
        is_default: bool,
        created_at: datetime.datetime,
    ):
        self._pk = pk
        self._name = name
        self._project = project
        self._level = level
        self._is_default = is_default
        self._created_at = created_at

    @property
    def pk(self) -> int:
        return self._pk

    @property
    def name(self) -> str:
        return self._name

    @property
    def project(self) -> str:
        return self._project

    @property
    def level(self) -> int:
        return self._level

    @property
    def is_default(self) -> bool:
        return self._is_default

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

    @classmethod
    def from_remote(cls, remote: Serialized) -> Priority:
        return cls(
            pk = remote['id'],
            name = remote['name'],
            project = remote['project'],
            level = remote['level'],
            is_default = remote['is_default'],
            created_at = datetime.datetime.strptime(remote['created_at'], DATETIME_FORMAT),
        )


class Tag(RemoteModel):

    def __init__(
        self,
        pk: int,
        name: str,
        created_at: datetime.datetime,
    ):
        self._pk = pk
        self._name = name
        self._created_at = created_at

    @property
    def pk(self) -> int:
        return self._pk

    @property
    def name(self) -> str:
        return self._name

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

    @classmethod
    def from_remote(cls, remote: Serialized) -> Tag:
        return cls(
            pk = remote['id'],
            name = remote['name'],
            created_at = datetime.datetime.strptime(remote['created_at'], DATETIME_FORMAT),
        )


class ToDo(RemoteModel):

    def __init__(
        self,
        pk: int,
        text: str,
        created_at: datetime.datetime,
        finished_at: t.Optional[datetime.datetime],
        state: State,
        tags: t.Sequence[str],
        comments: t.Sequence[str],
        project: str,
        priority: Priority,
        children: t.Optional[t.Sequence[ToDo]] = None,
        parents: t.Optional[t.Sequence[ToDo]] = None,
    ):
        self._pk = pk
        self._text = text
        self._created_at = created_at
        self._finished_at = finished_at
        self._state = state
        self._tags = tags
        self._comments = comments
        self._project = project
        self._children = children
        self._parents = parents
        self._priority = priority

    @property
    def pk(self) -> int:
        return self._pk

    @classmethod
    def from_remote(cls, remote: Serialized) -> ToDo:
        return cls(
            pk = remote['id'],
            text = remote['text'],
            created_at = datetime.datetime.strptime(remote['created_at'], DATETIME_FORMAT),
            finished_at = (
                datetime.datetime.strptime(remote['finished_at'], DATETIME_FORMAT)
                if remote['finished_at'] else
                None
            ),
            state = State[remote['state']],
            tags = remote['tags'],
            comments = remote['comments'],
            project = remote['project'],
            priority = Priority.from_remote(remote['priority']),
            children = [cls.from_remote(child) for child in remote['children']] if 'children' in remote else None,
            parents = [cls.from_remote(parent) for parent in remote['parents']] if 'parents' in remote else None,
        )

    @property
    def text(self) -> str:
        return self._text

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

    @property
    def finished_at(self) -> t.Optional[datetime.datetime]:
        return self._finished_at

    @property
    def canceled(self) -> bool:
        return self._state == State.CANCELED

    @property
    def tags(self) -> t.Sequence[str]:
        return self._tags

    @property
    def comments(self) -> t.Sequence[str]:
        return self._comments

    @property
    def project(self) -> str:
        return self._project

    @property
    def priority(self) -> Priority:
        return self._priority

    @property
    def children(self) -> t.Sequence[ToDo]:
        if self._children is None:
            return []
        return self._children

    @property
    def parents(self) -> t.Sequence[ToDo]:
        return self._parents

    @property
    def status(self) -> State:
        return self._state

    @property
    def elapsed(self) -> datetime.timedelta:
        return max(datetime.datetime.now() - self._created_at, datetime.timedelta(seconds = 0))

    @property
    def duration(self) -> datetime.timedelta:
        return (self._finished_at or datetime.datetime.now()) - self._created_at

    @property
    def time_since(self) -> t.Optional[datetime.timedelta]:
        return (datetime.datetime.now() - self._finished_at) if self._finished_at else None


@dataclasses.dataclass
class CIChecker(RemoteModel):
    run_id: t.Union[str, int]
    started: datetime.datetime
    timeout: datetime.datetime
    link: str
    canceled: bool

    @property
    def pk(self) -> t.Union[str, int]:
        return self.run_id

    @property
    def status(self) -> str:
        if self.canceled:
            return 'CANCELED'
        return 'PENDING'

    @property
    def elapsed(self) -> datetime.timedelta:
        return max(datetime.datetime.now() - self.started, datetime.timedelta(seconds = 0))

    @classmethod
    def from_remote(cls, remote: Serialized) -> CIChecker:
        return cls(
            run_id = remote['run_id'],
            started = datetime.datetime.strptime(remote['started'], DATETIME_FORMAT),
            timeout = datetime.datetime.strptime(remote['timeout'], DATETIME_FORMAT),
            link = remote['link'],
            canceled = remote['canceled'],
        )

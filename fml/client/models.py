from __future__ import annotations

import datetime
import typing as t

from abc import ABC, abstractmethod

from fml.client.utils import format_timedelta


Serialized = t.Mapping[str, t.Any]

DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'


class RemoteModel(ABC):

    def __init__(self, pk: t.Union[str, int]):
        self._pk = pk

    @property
    def pk(self) -> t.Union[str, int]:
        return self._pk

    @classmethod
    @abstractmethod
    def from_remote(cls, remote: Serialized) -> RemoteModel:
        pass

    def __hash__(self) -> int:
        return hash((self.__class__, self._pk))

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__)
            and self._pk == other._pk
        )


class Alarm(RemoteModel):

    def __init__(
        self,
        pk: int,
        text: str,
        started_at: datetime.datetime,
        end_at: datetime.datetime,
        requires_acknowledgment: bool,
        send_email: bool,
        silent: bool,
        level: str,
        times_notified: int,
        acknowledged: bool,
        canceled: bool,
        success: bool,
    ):
        super().__init__(pk)
        self._text = text
        self._started_at = started_at
        self._end_at = end_at
        self._requires_acknowledgment = requires_acknowledgment
        self._send_email = send_email
        self._silent = silent
        self._level = level
        self._times_notified = times_notified
        self._acknowledged = acknowledged
        self._canceled = canceled
        self._success = success

    @classmethod
    def from_remote(cls, remote: Serialized) -> Alarm:
        return cls(
            pk = remote['id'],
            text = remote['text'],
            started_at = datetime.datetime.strptime(remote['started_at'], DATETIME_FORMAT),
            end_at = datetime.datetime.strptime(remote['end_at'], DATETIME_FORMAT),
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
    def text(self) -> str:
        return self._text

    @property
    def started_at(self) -> datetime.datetime:
        return self._started_at

    @property
    def end_at(self) -> datetime.datetime:
        return self._end_at

    @property
    def requires_acknowledgment(self) -> bool:
        return self._requires_acknowledgment

    @property
    def send_email(self) -> bool:
        return self._send_email

    @property
    def silent(self) -> bool:
        return self._silent

    @property
    def level(self) -> str:
        return self._level

    @property
    def times_notified(self) -> int:
        return self._times_notified

    @property
    def acknowledged(self) -> bool:
        return self._acknowledged

    @property
    def canceled(self) -> bool:
        return self._canceled

    @property
    def success(self) -> bool:
        return self._success

    @property
    def flags(self) -> t.Iterator[str]:
        if self._silent:
            yield 'silent'
        if self._send_email:
            yield 'mail'
        if self._requires_acknowledgment:
            yield 'ack'

    @property
    def status(self) -> str:
        if self._canceled:
            return 'CANCELED'
        if self._requires_acknowledgment and not self._acknowledged and self._times_notified:
            return 'AWAITING_ACKNOWLEDGEMENT'
        if (
            self._requires_acknowledgment and self._acknowledged
            or not self._requires_acknowledgment and self._times_notified
        ):
            if self._success:
                return 'COMPLETED'
            return 'COMPLETED_LATE'
        return 'PENDING'

    @property
    def eta(self) -> str:
        eta = self._end_at - datetime.datetime.now()
        if eta.total_seconds() > 0:
            return format_timedelta(eta)
        return '-'

    @property
    def elapsed(self) -> datetime.timedelta:
        return max(datetime.datetime.now() - self._started_at, datetime.timedelta(seconds = 0))


class ToDo(RemoteModel):

    def __init__(
        self,
        pk: int,
        text: str,
        created_at: datetime.datetime,
        finished_at: t.Optional[datetime.datetime],
        canceled: bool,
    ):
        super().__init__(pk)
        self._text = text
        self._created_at = created_at
        self._finished_at = finished_at
        self._canceled = canceled

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
            canceled = remote['canceled'],
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
        return self._canceled

    @property
    def status(self) -> str:
        if self._canceled:
            return 'CANCELED'
        if self._finished_at:
            return 'SUCCESS'
        return 'PENDING'

    @property
    def elapsed(self) -> datetime.timedelta:
        return max(datetime.datetime.now() - self._created_at, datetime.timedelta(seconds = 0))

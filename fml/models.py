from __future__ import annotations

import typing as t
import datetime
from enum import Enum as _Enum

from sqlalchemy import Integer, String, Boolean, Enum, DateTime, Column, or_, and_, not_, ForeignKey, UniqueConstraint
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, Query, relationship
from sqlalchemy.orm.exc import MultipleResultsFound


Base = declarative_base()


class ImportanceLevel(_Enum):
    NORMAL = 'normal'
    IMPORTANT = 'important'


class Alarm(Base):
    __tablename__ = 'alarm'

    id = Column(Integer, primary_key = True)

    text = Column(String(127))

    started_at = Column(DateTime, default = datetime.datetime.now)
    end_at = Column(DateTime)

    requires_acknowledgment = Column(Boolean, default = False)
    retry_delay = Column(Integer, default = 60)
    send_email = Column(Boolean, default = False)
    silent = Column(Boolean, default = False)
    level = Column(Enum(ImportanceLevel), default = ImportanceLevel.NORMAL)

    times_notified = Column(Integer, default = 0)
    next_reminder_time_target = Column(DateTime, nullable = True)
    acknowledged = Column(Boolean, default = False)

    canceled = Column(Boolean, default = False)
    success = Column(Boolean, default = False)

    @property
    def cancelable(self) -> bool:
        return not self.canceled and (
            (
                self.requires_acknowledgment and not self.acknowledged
            ) or
            (
                not self.requires_acknowledgment and self.times_notified <= 0
            )
        )

    @property
    def next_target_time(self) -> datetime.datetime:
        return self.next_reminder_time_target or self.end_at

    @classmethod
    def active_alarms(cls, session: Session, target = None) -> Query:
        return session.query(Alarm if target is None else target).filter(
            and_(
                not_(Alarm.canceled),
                or_(
                    and_(
                        Alarm.requires_acknowledgment,
                        not_(Alarm.acknowledged),
                    ),
                    and_(
                        not_(Alarm.requires_acknowledgment),
                        Alarm.times_notified < 1,
                    ),
                )
            )
        )


class Tagged(Base):
    __tablename__ = 'tagged'

    id = Column(Integer, primary_key = True)
    tag_id = Column(
        Integer,
        ForeignKey('tag.id', ondelete = 'CASCADE'),
        nullable = False,
    )
    todo_id = Column(
        Integer,
        ForeignKey('todo.id', ondelete = 'CASCADE'),
        nullable = False,
    )

    __table_args__ = (UniqueConstraint('tag_id', 'todo_id'),)


class StringIdentified(Base):
    __abstract__ = True
    id: Column[Integer]
    name: Column[String]

    @classmethod
    def get_for_no_identifier(cls, session: Session) -> t.Optional[int]:
        return None

    @classmethod
    def get_for_identifier(cls, session: Session, identifier: t.Union[str, int, None]) -> t.Optional[int]:
        if not identifier:
            return cls.get_for_no_identifier(session)
        if isinstance(identifier, int):
            return session.query(cls.id).get(cls.id)
        try:
            return session.query(cls.id).filter(
                cls.name.contains(identifier)
            ).scalar()
        except MultipleResultsFound:
            return None


class Tag(StringIdentified):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key = True)
    name = Column(String(127), unique = True)
    todos: t.Sequence[ToDo] = relationship('ToDo', back_populates = 'tags', secondary = Tagged.__table__)
    created_at = Column(DateTime, default = datetime.datetime.now)


class Project(StringIdentified):
    __tablename__ = 'project'

    id = Column(Integer, primary_key = True)
    name = Column(String(127), unique = True)
    created_at = Column(DateTime, default = datetime.datetime.now)
    is_default = Column(Boolean, default = False)

    todos = relationship(
        'ToDo',
        back_populates = 'project',
        cascade = 'all, delete-orphan',
    )

    @classmethod
    def get_for_no_identifier(cls, session: Session) -> t.Optional[int]:
        return session.query(cls.id).filter(cls.is_default == True).scalar()


class ToDo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key = True)

    text = Column(String(127))

    created_at = Column(DateTime, default = datetime.datetime.now)
    finished_at = Column(DateTime, nullable = True)
    canceled = Column(Boolean, default = False)

    project_id = Column(
        Integer,
        ForeignKey('project.id', ondelete = 'CASCADE'),
        nullable = False,
    )
    project = relationship('Project', back_populates = 'todos')

    tags: t.Sequence[Tag] = relationship(
        'Tag',
        back_populates = 'todos',
        secondary = Tagged.__table__,
    )

    @property
    def cancelable(self) -> bool:
        return not self.canceled and not self.finished_at

    @classmethod
    def active_todos(cls, session: Session, target = None) -> Query:
        return session.query(cls if target is None else target).filter(
            not_(cls.canceled),
            cls.finished_at == None,
        )


def create(engine: Engine):
    Base.metadata.create_all(engine)

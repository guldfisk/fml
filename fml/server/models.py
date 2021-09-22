from __future__ import annotations

import typing as t
import datetime
from enum import Enum as _Enum

from sqlalchemy import (
    Integer, String, Boolean, Enum, DateTime, Column, or_, and_, not_, ForeignKey, UniqueConstraint, asc, Text
)
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, Query, relationship, backref, synonym
from sqlalchemy.orm.exc import MultipleResultsFound

from hardcandy.schema import Schema

from fml.server.exceptions import SimpleError, MultipleCandidateError


Base = declarative_base()


class ImportanceLevel(_Enum):
    NORMAL = 'normal'
    IMPORTANT = 'important'


class StringIdentified(Base):
    __abstract__ = True
    id: Column[Integer]
    text_identifier: Column[String]
    sort_keys: t.Optional[t.Tuple[str]] = None

    @classmethod
    def get_for_no_identifier(
        cls,
        session: Session,
        target = None,
        base_query: t.Optional[Query] = None,
    ) -> t.Optional[StringIdentified]:
        return None

    @classmethod
    def get_for_identifier(
        cls,
        session: Session,
        identifier: t.Union[str, int, None],
        target = None,
        base_query: t.Optional[Query] = None,
    ) -> t.Optional[StringIdentified]:
        target = target or cls
        base_query = session.query(target) if base_query is None else base_query

        if not identifier:
            return cls.get_for_no_identifier(session, target = target, base_query = base_query)
        if isinstance(identifier, int):
            return base_query.filter(cls.id == identifier).scalar()
        try:
            return base_query.filter(
                cls.text_identifier.contains(identifier)
            ).scalar()
        except MultipleResultsFound:
            return None

    @classmethod
    def get_for_identifier_or_raise(
        cls,
        session: Session,
        identifier: t.Union[str, int, None],
        schema: Schema,
        target = None,
        base_query: t.Optional[Query] = None,
    ) -> StringIdentified:
        target = target or cls
        base_query = session.query(target) if base_query is None else base_query

        if not identifier:
            v = cls.get_for_no_identifier(session, target = target, base_query = base_query)
            if v is None:
                raise SimpleError('invalid target')
            return v
        candidates = cls.get_list_for_identifier(
            session = session,
            identifier = identifier,
            base_query = base_query,
        )
        if not candidates:
            raise SimpleError('invalid target')
        if len(candidates) > 1:
            raise MultipleCandidateError(
                cls,
                candidates if cls.sort_keys is None else sorted(
                    candidates,
                    key = lambda _c: tuple(getattr(_c, sv) for sv in cls.sort_keys),
                ),
                schema,
            )
        return candidates[0]

    @classmethod
    def get_list_for_identifier(
        cls,
        session: Session,
        identifier: t.Union[str, int, None],
        target = None,
        base_query: t.Optional[Query] = None,
    ) -> t.List[StringIdentified]:
        target = target or cls
        base_query = session.query(target) if base_query is None else base_query

        if not identifier:
            return [cls.get_for_no_identifier(session, target = target, base_query = base_query)]
        if isinstance(identifier, int):
            return list(base_query.filter(cls.id == identifier))

        return list(
            base_query.filter(
                cls.text_identifier.contains(identifier)
            )
        )


class Alarm(StringIdentified):
    __tablename__ = 'alarm'

    sort_keys = ('end_at',)

    id = Column(Integer, primary_key = True)

    text = Column(String(127))
    text_identifier = synonym('text')

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


class Tag(StringIdentified):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key = True)
    name = Column(String(127), unique = True)
    todos: t.Sequence[ToDo] = relationship('ToDo', back_populates = 'tags', secondary = Tagged.__table__)
    created_at = Column(DateTime, default = datetime.datetime.now)

    text_identifier = synonym('name')


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key = True)
    text = Column(Text, nullable = False)
    created_at = Column(DateTime, default = datetime.datetime.now)
    todo_id = Column(
        Integer,
        ForeignKey('todo.id', ondelete = 'CASCADE'),
        nullable = False,
    )
    todo = relationship('ToDo', back_populates = 'comments')


class Priority(StringIdentified):
    __tablename__ = 'priority'

    id = Column(Integer, primary_key = True)
    name = Column(String(127))
    todos: t.Sequence[ToDo] = relationship('ToDo', back_populates = 'priority')
    created_at = Column(DateTime, default = datetime.datetime.now)
    project_id = Column(
        Integer,
        ForeignKey('project.id', ondelete = 'CASCADE'),
        nullable = False,
    )
    project = relationship('Project', back_populates = 'priorities')
    level = Column(Integer)
    is_default = Column(Boolean, default = False)

    text_identifier = synonym('name')

    __table_args__ = (UniqueConstraint('project_id', 'level'), UniqueConstraint('project_id', 'name'),)

    @classmethod
    def get_for_no_identifier(
        cls,
        session: Session,
        target = None,
        base_query: t.Optional[Query] = None,
    ) -> t.Optional[StringIdentified]:
        return base_query.filter(cls.is_default == True).scalar()

    @classmethod
    def get_for_identifier_and_project(
        cls,
        session: Session,
        project_id: int,
        identifier: t.Union[str, int, None],
        target = None,
    ):
        target = target or cls
        return cls.get_for_identifier(
            session = session,
            identifier = identifier,
            base_query = session.query(target or cls).filter(
                cls.project_id == project_id
            )
        )


class Project(StringIdentified):
    __tablename__ = 'project'

    id = Column(Integer, primary_key = True)
    name = Column(String(127), unique = True)
    created_at = Column(DateTime, default = datetime.datetime.now)
    is_default = Column(Boolean, default = False)
    default_priority_filter = Column(Integer, nullable = True, default = None)

    todos = relationship(
        'ToDo',
        back_populates = 'project',
        cascade = 'all, delete-orphan',
    )

    priorities = relationship(
        'Priority',
        back_populates = 'project',
        cascade = 'all, delete-orphan',
    )

    text_identifier = synonym('name')

    @classmethod
    def get_for_no_identifier(
        cls,
        session: Session,
        target = None,
        base_query: t.Optional[Query] = None,
    ) -> t.Optional[StringIdentified]:
        return session.query(target or cls).filter(cls.is_default).scalar()


class Dependency(Base):
    __tablename__ = 'dependency'

    id = Column(Integer, primary_key = True)
    parent_id = Column(
        Integer,
        ForeignKey('todo.id', ondelete = 'CASCADE'),
        nullable = False,
    )
    child_id = Column(
        Integer,
        ForeignKey('todo.id', ondelete = 'CASCADE'),
        nullable = False,
    )

    __table_args__ = (UniqueConstraint('parent_id', 'child_id'),)


class State(_Enum):
    PENDING = 'pending'
    WAITING = 'waiting'
    COMPLETED = 'completed'
    CANCELED = 'canceled'


class ToDo(StringIdentified):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key = True)

    text = Column(String(127))

    created_at = Column(DateTime, default = datetime.datetime.now)
    finished_at = Column(DateTime, nullable = True)
    state = Column(Enum(State), default = State.PENDING)

    project_id = Column(
        Integer,
        ForeignKey('project.id', ondelete = 'CASCADE'),
        nullable = False,
    )
    project = relationship('Project', back_populates = 'todos')

    priority_id = Column(
        Integer,
        ForeignKey('priority.id', ondelete = 'CASCADE'),
        nullable = True,
    )
    priority = relationship('Priority', back_populates = 'todos')

    tags: t.Sequence[Tag] = relationship(
        'Tag',
        back_populates = 'todos',
        secondary = Tagged.__table__,
    )

    comments = relationship(
        'Comment',
        back_populates = 'todo',
        cascade = 'all, delete-orphan',
        order_by = asc(Comment.created_at),
    )

    parents = relationship(
        'ToDo',
        secondary = Dependency.__table__,
        primaryjoin = id == Dependency.child_id,
        secondaryjoin = id == Dependency.parent_id,
        backref = backref('children'),
    )

    text_identifier = synonym('text')

    @property
    def active_children(self) -> t.Iterator[ToDo]:
        for child in self.children:
            if child.active:
                yield child

    def traverse_children(self, active_only: bool = True) -> t.Iterator[ToDo]:
        for child in self.children:
            if active_only and not child.active:
                continue
            yield child
            yield from child.traverse_children()

    @property
    def cancelable(self) -> bool:
        return self.state in (State.PENDING, State.WAITING)

    @property
    def active(self) -> bool:
        return self.cancelable

    @classmethod
    def active_todos(cls, session: Session, target = None) -> Query:
        return session.query(cls if target is None else target).filter(
            cls.state.in_((State.PENDING, State.WAITING)),
        )


def create(engine: Engine):
    Base.metadata.create_all(engine)

from __future__ import annotations

import datetime
from enum import Enum as _Enum

from sqlalchemy import Integer, String, Boolean, Enum, DateTime, Column, or_, and_, not_
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, Query


Base = declarative_base()


class ImportanceLevel(_Enum):
    NORMAL = 'normal'
    IMPORTANT = 'important'


class Alarm(Base):
    __tablename__ = 'alarm'

    id = Column(Integer, primary_key = True)

    text = Column(String(127))

    started_at = Column(DateTime, default = datetime.datetime.now)
    end_at = Column(DateTime, )

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
    def next_target_time(self):
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


class ToDo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key = True)

    text = Column(String(127))

    created_at = Column(DateTime, default = datetime.datetime.now)
    finished_at = Column(DateTime, nullable = True)
    canceled = Column(Boolean, default = False)

    @classmethod
    def active_todos(cls, session: Session, target = None) -> Query:
        return session.query(cls if target is None else target).filter(
            not_(cls.canceled),
            cls.finished_at == None,
        )


def create(engine: Engine):
    Base.metadata.create_all(engine)

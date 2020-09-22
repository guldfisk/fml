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
    send_email = Column(Boolean, default = False)
    silent = Column(Boolean, default = False)
    level = Column(Enum(ImportanceLevel), default = ImportanceLevel.NORMAL)

    times_notified = Column(Integer, default = 0)
    acknowledged = Column(Boolean, default = False)

    canceled = Column(Boolean, default = False)
    success = Column(Boolean, default = False)

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


def create(engine: Engine):
    Base.metadata.create_all(engine)

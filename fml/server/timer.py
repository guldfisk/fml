from __future__ import annotations

import typing as t
import threading
import datetime

from sqlalchemy import not_, and_
from sqlalchemy.orm import Session

from fml.server import ScopedSession
from fml.server.models import Alarm
from fml import sound, notify


class AlarmWorker(threading.Thread):

    def __init__(
        self,
        alarm_id: int,
        callback: t.Optional[t.Callable[[AlarmWorker, bool], None]] = None,
    ):
        super().__init__()
        self._alarm_id = alarm_id
        self._callback = callback
        self._stopped = threading.Event()

    @property
    def alarm_id(self) -> int:
        return self._alarm_id

    def run(self) -> None:
        session: Session = ScopedSession()
        alarm: Alarm = session.query(Alarm).get(self._alarm_id)

        target_time = alarm.next_target_time

        session.commit()

        canceled = self._stopped.wait((target_time - datetime.datetime.now()).total_seconds())

        if not canceled:
            session: Session = ScopedSession()
            alarm: Alarm = session.query(Alarm).get(self._alarm_id)

            if not alarm.canceled and not alarm.acknowledged:
                missed_by = (datetime.datetime.now() - alarm.end_at).total_seconds()

                success = missed_by < .5

                body = '{notification_text} {time_text}'.format(
                    notification_text = (
                        'Re-notified (number {})'.format(alarm.times_notified)
                        if alarm.times_notified else
                        'Notified'
                    ),
                    time_text = (
                        'on time'
                        if success else
                        'late by {} seconds'.format(round(missed_by, 1))
                    )
                )

                notify.notify(alarm.text, description = body)
                if not alarm.silent:
                    sound.ding_sync()
                if alarm.send_email:
                    notify.send_mail(alarm.text, body)

                session.query(Alarm).filter(Alarm.id == alarm.id).update(
                    {
                        'times_notified': (Alarm.times_notified + 1),
                        'next_reminder_time_target': datetime.datetime.now() + datetime.timedelta(
                            seconds = alarm.retry_delay
                        ),
                        **(
                            {'success': success}
                            if alarm.times_notified <= 0 else
                            {}
                        )
                    }
                )

                session.commit()

        if self._callback is not None:
            self._callback(self, canceled)

    def cancel(self):
        self._stopped.set()


class Checker(threading.Thread):

    def __init__(self, manager: AlarmManager):
        super().__init__()
        self._manager = manager
        self._canceled = threading.Event()

    def run(self) -> None:
        while not self._canceled.wait(4*60):
            self._manager.check()


class AlarmManager(object):

    def __init__(self):
        self._lock = threading.Lock()
        self._alarm_map: t.MutableMapping[int, AlarmWorker] = {}

    def handle_alarm(self, alarm_id: int) -> None:
        with self._lock:
            if alarm_id in self._alarm_map:
                return
            worker = AlarmWorker(alarm_id, self._alarm_completed)
            self._alarm_map[alarm_id] = worker
        worker.start()

    def _alarm_completed(self, worker: AlarmWorker, canceled: bool) -> None:
        session: Session = ScopedSession()
        alarm: Alarm = session.query(Alarm).get(worker.alarm_id)
        with self._lock:
            try:
                del self._alarm_map[worker.alarm_id]
            except KeyError:
                pass
        if not canceled and not alarm.canceled and alarm.requires_acknowledgment and not alarm.acknowledged:
            self.handle_alarm(alarm_id = worker.alarm_id)

    def check(self) -> None:
        session: Session = ScopedSession()
        now = datetime.datetime.now()
        for alarm in Alarm.active_alarms(session).all():
            if alarm.next_target_time - now < datetime.timedelta(minutes=5):
                self.handle_alarm(alarm.id)

    def cancel(self, alarm_id: int, session: Session) -> t.Optional[Alarm]:
        alarm = Alarm.active_alarms(session).filter(Alarm.id == alarm_id).scalar()

        if alarm is not None:
            alarm.canceled = True
            alarm.success = False
            session.commit()

        with self._lock:
            alarm_worker = self._alarm_map.get(alarm_id)
        if alarm_worker:
            alarm_worker.cancel()

        return alarm

    def acknowledge(self, alarm_id, session: Session) -> t.Optional[Alarm]:
        alarm: Alarm = session.query(Alarm).get(alarm_id)

        if alarm is None or not (
            alarm.requires_acknowledgment
            and alarm.times_notified
            and alarm.end_at <= datetime.datetime.now()
        ):
            return

        alarm.acknowledged = True
        session.commit()

        with self._lock:
            alarm_worker = self._alarm_map.get(alarm_id)
        if alarm_worker:
            alarm_worker.cancel()

        return alarm

    def snooze(self, alarm_id, session: Session, new_target_time: datetime.datetime) -> t.Optional[Alarm]:
        alarm: Alarm = session.query(Alarm).get(alarm_id)

        if alarm is None or not (
            alarm.requires_acknowledgment
            and alarm.times_notified
            and alarm.end_at <= datetime.datetime.now()
        ):
            return

        with self._lock:
            alarm_worker = self._alarm_map.get(alarm.id)
        if alarm_worker:
            self._alarm_map[alarm.id].cancel()
            alarm_worker.join(3)

        alarm.next_reminder_time_target = new_target_time
        session.commit()
        self.handle_alarm(alarm_id)

        return alarm

    def cancel_all(self, session: Session) -> t.Sequence[Alarm]:
        alarms = Alarm.active_alarms(session).all()
        for alarm in alarms:
            with self._lock:
                alarm_worker = self._alarm_map.get(alarm.id)
            if alarm_worker:
                alarm_worker.cancel()
            alarm.canceled = True
            alarm.success = False

        session.add_all(alarms)
        session.commit()

        return alarms

    def acknowledge_all(self, session: Session) -> t.Sequence[Alarm]:
        alarms = session.query(Alarm).filter(
            and_(
                not_(Alarm.canceled),
                Alarm.requires_acknowledgment,
                not_(Alarm.acknowledged),
                Alarm.end_at <= datetime.datetime.now()
            )
        ).all()
        for alarm in alarms:
            alarm.acknowledged = True
            session.add(alarm)
            session.commit()

            with self._lock:
                alarm_worker = self._alarm_map.get(alarm.id)
            if alarm_worker:
                alarm_worker.cancel()

        return alarms


MANAGER = AlarmManager()

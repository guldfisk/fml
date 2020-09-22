from __future__ import annotations

import typing as t
import threading
import datetime

from sqlalchemy.orm import Session

from fml import ScopedSession
from fml.models import Alarm
from fml import notify


class AlarmWorker(threading.Thread):

    def __init__(
        self,
        alarm_id: int,
        callback: t.Optional[t.Callable[[AlarmWorker], None]] = None,
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

        if not self._stopped.wait((alarm.end_at - datetime.datetime.now()).total_seconds()):
            missed_by = (datetime.datetime.now() - alarm.end_at).total_seconds()

            success = missed_by < .5

            body = 'Notified on time' if success else 'Notified late by {} seconds'.format(round(missed_by, 1))

            notify.notify(alarm.text, description = body)
            if not alarm.silent:
                notify.play_sound()
            if alarm.send_email:
                notify.send_mail(alarm.text, body)

            session.query(Alarm).filter(Alarm.id == alarm.id).update(
                {
                    'times_notified': (Alarm.times_notified + 1),
                    'canceled': False,
                    'success': success,
                }
            )

        session.commit()

        if self._callback is not None:
            self._callback(self)

    def cancel(self):
        self._stopped.set()


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

    def _alarm_completed(self, worker: AlarmWorker) -> None:
        with self._lock:
            try:
                del self._alarm_map[worker.alarm_id]
            except KeyError:
                pass

    def check(self) -> None:
        session: Session = ScopedSession()
        for alarm_id in Alarm.active_alarms(session, target = Alarm.id).all():
            self.handle_alarm(alarm_id)

    def cancel(self, alarm_id: int, session: Session) -> t.Optional[Alarm]:
        alarm = session.query(Alarm).get(alarm_id)

        if alarm is None:
            return

        with self._lock:
            alarm_worker = self._alarm_map.get(alarm_id)
        if alarm_worker:
            self._alarm_map[alarm_id].cancel()
            del self._alarm_map[alarm_id]
        alarm.canceled = True
        alarm.success = False

        session.commit()

        return alarm

    def cancel_all(self, session: Session) -> t.Sequence[Alarm]:
        alarms = Alarm.active_alarms(session).all()
        for alarm in alarms:
            with self._lock:
                alarm_worker = self._alarm_map.get(alarm.id)
            if alarm_worker:
                self._alarm_map[alarm.id].cancel()
                del self._alarm_map[alarm.id]
            alarm.canceled = True
            alarm.success = False

        session.add_all(alarms)

        session.commit()

        return alarms


MANAGER = AlarmManager()

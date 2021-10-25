import datetime
import typing as t
import threading

from fml import notify
from fml.common.ci.client import CIClient
from fml.server.views.utils import DATETIME_FORMAT


class CIChecker(threading.Thread):
    _st: datetime.datetime

    def __init__(
        self,
        cookie_name: str,
        cookie_value: str,
        run_id: t.Union[int, str],
        timeout: t.Optional[datetime.datetime] = None,
        callback: t.Optional[t.Callable[[t.Union[str, int], bool], None]] = None,
    ):
        super().__init__()
        self._client = CIClient(cookie_name, cookie_value)
        self._run_id = run_id
        self._timeout = timeout
        self._callback = callback or (lambda _, __: None)
        self._canceled = threading.Event()

    def cancel(self) -> None:
        self._canceled.set()

    @property
    def started_at(self) -> datetime.datetime:
        return self._st

    @property
    def link(self) -> str:
        return 'https://ci.uniid.it/blue/organizations/jenkins/unisport/detail/unisport/{}/pipeline'.format(
            self._run_id,
        )

    def run(self) -> None:
        self._st = datetime.datetime.now()
        if self._timeout is None:
            self._timeout = self._st + datetime.timedelta(hours = 1)
        while True:
            if self._canceled.is_set():
                self._callback(self._run_id, False)
                return
            if datetime.datetime.now() > self._timeout:
                notify.notify('Timed out checking CI run', str(self._run_id))
                self._callback(self._run_id, False)
                return
            try:
                status = self._client.get_run_status(self._run_id)
            except Exception as e:
                notify.notify('Failed getting status for CI run {}'.format(self._run_id), str(e))
                self._callback(self._run_id, False)
                return
            if status.finished:
                notify.notify(
                    'CI run finished: {}'.format('SUCCEEDED' if status.succeeded else 'FAILED'),
                    self.link,
                )
                self._callback(self._run_id, True)
                return
            self._canceled.wait(5)

    def serialize(self) -> t.Mapping[str, t.Any]:
        return {
            'run_id': self._run_id,
            'started': self._st.strftime(DATETIME_FORMAT),
            'timeout': self._timeout.strftime(DATETIME_FORMAT),
            'link': self.link,
            'canceled': self._canceled.is_set(),
        }

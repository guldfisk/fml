import datetime
import time
import typing as t
import threading

from fml import notify
from fml.server.ciwatch.client import CIClient


class CIChecker(threading.Thread):
    _st: datetime.datetime

    def __init__(
        self,
        cookie_name: str,
        cookie_value: str,
        run_id: t.Union[int, str],
        timeout: int = 60 * 30,
        callback: t.Optional[t.Callable[[t.Union[str, int], bool], None]] = None,
    ):
        super().__init__()
        self._client = CIClient(cookie_name, cookie_value)
        self._run_id = run_id
        self._timeout = timeout
        self._callback = callback or (lambda _, __: None)

    def run(self) -> None:
        self._st = datetime.datetime.now()
        while True:
            if datetime.datetime.now() > self._st + datetime.timedelta(seconds = self._timeout):
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
                    'http://ci.uniid.it/blue/organizations/jenkins/unisport/detail/unisport/{}/pipeline'.format(
                        self._run_id,
                    ),
                )
                self._callback(self._run_id, True)
                return
            time.sleep(5)

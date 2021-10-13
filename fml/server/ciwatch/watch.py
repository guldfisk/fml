import typing as t
import threading

from fml.server.ciwatch.checker import CIChecker


class CIWatchManager(object):

    def __init__(self):
        self._watching: t.MutableMapping[str, CIChecker] = {}
        self._lock = threading.Lock()

    def _on_completed(self, run_id: t.Union[str, int], success: bool) -> None:
        with self._lock:
            try:
                del self._watching[str(run_id)]
            except KeyError:
                pass

    def watch(
        self,
        cookie_name: str,
        cookie_value: str,
        run_id: t.Union[int, str],
        timeout: int = 60 * 30,
    ) -> None:
        run_id = str(run_id)
        with self._lock:
            if run_id not in self._watching:
                checker = CIChecker(
                    cookie_name,
                    cookie_value,
                    run_id,
                    timeout = timeout,
                    callback = self._on_completed,
                )
                self._watching[run_id] = checker
                checker.start()

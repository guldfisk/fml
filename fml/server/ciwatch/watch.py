import datetime
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

    def watching(self) -> t.Sequence[CIChecker]:
        with self._lock:
            return sorted(
                self._watching.values(), key=lambda v: v.started_at, reverse=True
            )

    def watch(
        self,
        cookie_name: str,
        cookie_value: str,
        run_id: t.Union[int, str],
        timeout: t.Optional[datetime.datetime] = None,
        superseed: bool = False,
    ) -> CIChecker:
        run_id = str(run_id)
        with self._lock:
            if superseed:
                for k, v in self._watching.items():
                    if k != run_id:
                        v.cancel()
            if run_id not in self._watching:
                checker = CIChecker(
                    cookie_name,
                    cookie_value,
                    run_id,
                    timeout=timeout,
                    callback=self._on_completed,
                )
                self._watching[run_id] = checker
                checker.start()
                return checker
            return self._watching[run_id]


CI_WATCHER = CIWatchManager()

import typing as t

import requests


class RunStatus(list):

    @property
    def finished(self) -> bool:
        return all(n.get('state') in ('FINISHED', 'NOT_BUILT') for n in self)

    @property
    def succeeded(self):
        return all(n.get('result') in ('SUCCESS', 'NOT_BUILT') for n in self)


class CIClient(object):
    host = 'ci.uniid.it'

    def __init__(self, cookie_name: str, cookie_value: str):
        self._cookie_name = cookie_name
        self._cookie_value = cookie_value

        self._session = requests.session()
        self._session.cookies.set(self._cookie_name, self._cookie_value, domain = self.host)

    def get_run_status(self, run_id: t.Union[str, int]) -> RunStatus:
        return RunStatus(
            self._session.get(
                'http://{}/blue/rest/organizations/jenkins/pipelines/unisport/runs/{}/nodes/'.format(
                    self.host,
                    run_id,
                )
            ).json()
        )

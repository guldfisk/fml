import typing as t

import requests

from fml.common.ci import models


class CIClient(object):
    host = 'ci.uniid.it'

    def __init__(self, cookie_name: str, cookie_value: str):
        self._cookie_name = cookie_name
        self._cookie_value = cookie_value

        self._session = requests.session()
        self._session.cookies.set(self._cookie_name, self._cookie_value, domain = self.host)

    def get_run_status(self, run_id: t.Union[str, int]) -> models.RunStatus:
        return models.RunStatus(
            self._session.get(
                'http://{}/blue/rest/organizations/jenkins/pipelines/unisport/runs/{}/nodes/'.format(
                    self.host,
                    run_id,
                )
            ).json()
        )

    def get_runs(self, start: int = 0, limit: int = 10) -> t.Sequence[models.CIRun]:
        return [
            models.CIRun(run)
            for run in
            self._session.get(
                'http://{}/blue/rest/organizations/jenkins/pipelines/unisport/runs/'.format(
                    self.host,
                ),
                params = {'start': start, 'limit': limit}
            ).json()
        ]

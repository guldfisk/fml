import typing as t

import datetime


LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo


class RunStatus(dict):

    @property
    def finished(self) -> bool:
        return self.get('result') not in ('UNKNOWN', 'RUNNING')

    @property
    def succeeded(self) -> bool:
        return self.get('result') == 'SUCCESS'


class CIRun(dict):
    DT_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'

    @property
    def started_at(self) -> datetime.datetime:
        return datetime.datetime.strptime(
            self['startTime'],
            self.DT_FORMAT,
        ).astimezone(LOCAL_TIMEZONE).replace(tzinfo = None) if 'startTime' in self else datetime.datetime.now()

    @property
    def ended_at(self) -> t.Optional[datetime.datetime]:
        return (
            datetime.datetime.strptime(
                self['endTime'],
                self.DT_FORMAT,
            ).astimezone(LOCAL_TIMEZONE).replace(tzinfo = None)
            if self.get('endTime') else
            None
        )

    @property
    def elapsed(self) -> datetime.timedelta:
        return datetime.datetime.now() - self.started_at

    @property
    def link(self) -> str:
        return 'https://ci.uniid.it/blue/organizations/jenkins/unisport/detail/unisport/{}/pipeline'.format(
            self['id'],
        )

    @property
    def name(self) -> str:
        return self.get('name') or 'unknown'

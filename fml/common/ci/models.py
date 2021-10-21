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

    @property
    def started_at(self):
        return datetime.datetime.strptime(
            self['startTime'],
            '%Y-%m-%dT%H:%M:%S.%f%z',
        ).astimezone(LOCAL_TIMEZONE).replace(tzinfo = None)

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

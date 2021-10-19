import datetime


LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo


class RunStatus(list):

    @property
    def finished(self) -> bool:
        return all(n.get('state') in ('FINISHED', 'NOT_BUILT') for n in self)

    @property
    def succeeded(self):
        return all(n.get('result') in ('SUCCESS', 'NOT_BUILT') for n in self)


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
        return 'http://ci.uniid.it/blue/organizations/jenkins/unisport/detail/unisport/{}/pipeline'.format(
            self['id'],
        )

    @property
    def name(self) -> str:
        return self.get('name', 'unknown')

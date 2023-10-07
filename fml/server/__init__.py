from configparser import ConfigParser

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import scoped_session

from fml import paths


_parser = ConfigParser()
_parser.read(paths.CONFIG_PATH)
_keys = _parser['DB']

MAILGUN_KEY = _parser['MAIL']['mailgun_key']
MAILGUN_DOMAIN = _parser['MAIL']['mailgun_domain']
EMAIL = _parser['MAIL']['owner_email']

uri = '{dialect}+{driver}://{username}:{password}@{host}/{database}'.format(**_keys)
print(uri)

engine = create_engine(
    uri,
    pool_size = 32,
    echo = False,
    pool_pre_ping = True,
)

session_factory = sessionmaker(bind = engine)
ScopedSession = scoped_session(session_factory)

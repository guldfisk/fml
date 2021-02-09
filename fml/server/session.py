from flask import Flask
from flask_sqlalchemy_session import flask_scoped_session

from sqlalchemy.orm import Session

from fml.server import session_factory


class SessionContainer(object):
    session: Session

    @classmethod
    def init(cls, app: Flask) -> None:
        cls.session = flask_scoped_session(session_factory, app)

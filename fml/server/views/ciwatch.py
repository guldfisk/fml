import datetime
import typing as t

from flask import Blueprint
from flask_api.request import APIRequest

from hardcandy import fields
from hardcandy.schema import Schema

from fml.server import models
from fml.server.ciwatch.watch import CI_WATCHER
from fml.server.session import SessionContainer as SC
from fml.server.views.utils import inject_schema, with_errors


ci_watch_views = Blueprint("ci_watch_views", __name__, url_prefix="/ci")
request: APIRequest


@ci_watch_views.route("/watch/", methods=["POST"])
@with_errors
@inject_schema(
    Schema(
        {
            "cookie_name": fields.Text(required=False, default=None),
            "cookie_value": fields.Text(required=False, default=None),
            "run_id": fields.Text(),
            "timeout": fields.Datetime(required=False, default=None),
            "superseed": fields.Bool(default=False),
        }
    ),
    use_args=False,
)
def watch_ci(
    cookie_name: t.Optional[str],
    cookie_value: t.Optional[str],
    run_id: str,
    timeout: t.Optional[datetime.datetime],
    superseed: bool,
):
    if cookie_name and cookie_value:
        token = models.CIToken(name=cookie_name, value=cookie_value)
        SC.session.add(token)
        SC.session.commit()
    else:
        token = (
            SC.session.query(models.CIToken)
            .order_by(models.CIToken.created_at.desc())
            .first()
        )
        cookie_name, cookie_value = token.name, token.value
    return CI_WATCHER.watch(
        cookie_name, cookie_value, run_id, timeout=timeout, superseed=superseed
    ).serialize()


@ci_watch_views.route("/watching/", methods=["GET"])
@with_errors
def watching():
    return {"ci_checkers": [checker.serialize() for checker in CI_WATCHER.watching()]}


@ci_watch_views.route("/update-token/", methods=["POST"])
@with_errors
@inject_schema(
    Schema(
        {
            "cookie_name": fields.Text(),
            "cookie_value": fields.Text(),
        }
    ),
    use_args=False,
)
def update_token(cookie_name: str, cookie_value: str):
    token = models.CIToken(name=cookie_name, value=cookie_value)
    SC.session.add(token)
    SC.session.commit()
    return {"status": "ok"}


@ci_watch_views.route("/latest-token/", methods=["GET"])
@with_errors
def latest_token():
    token = (
        SC.session.query(models.CIToken)
        .order_by(models.CIToken.created_at.desc())
        .first()
    )
    return {
        "name": token.name,
        "value": token.value,
    }

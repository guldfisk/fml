from flask import Blueprint
from flask_api.request import APIRequest

from hardcandy import fields
from hardcandy.schema import Schema

from fml.server.ciwatch.checker import CIChecker
from fml.server.views.utils import inject_schema, with_errors


ci_watch_views = Blueprint('ci_watch_views', __name__, url_prefix = '/ci')
request: APIRequest


@ci_watch_views.route('/watch/', methods = ['POST'])
@with_errors
@inject_schema(
    Schema(
        {
            'cookie_name': fields.Text(),
            'cookie_value': fields.Text(),
            'run_id': fields.Text(),
        }
    ),
    use_args = False,
)
def watch_ci(cookie_name: str, cookie_value: str, run_id: str):
    CIChecker(cookie_name, cookie_value, run_id).start()
    return {
        'status': 'ok'
    }

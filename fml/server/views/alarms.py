import typing as t
import datetime
from abc import abstractmethod

from flask import request, Blueprint
from flask.views import View
from flask_api import status
from flask_api.request import APIRequest

from sqlalchemy.orm import Query

from hardcandy.schema import DeserializationError, Schema
from hardcandy import fields

from fml.notify import notify as _notify
from fml.server import models, schemas
from fml.server.schemas import AlarmSchema
from fml.server.session import SessionContainer as SC
from fml.server.timer import MANAGER
from fml.server.views.utils import inject_schema, with_errors
from fml.sound import ding_sync


alarm_views = Blueprint("alarm_views", __name__, url_prefix="/alarms")
request: APIRequest


@alarm_views.route("/", methods=["POST"])
def create_alarm():
    schema = AlarmSchema()

    try:
        alarm: models.Alarm = schema.deserialize(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    if alarm.end_at < datetime.datetime.now() - datetime.timedelta(seconds=1):
        return "Alarm must finish in the future", status.HTTP_400_BAD_REQUEST

    SC.session.add(alarm)

    SC.session.commit()

    MANAGER.handle_alarm(alarm.id)

    return schema.serialize(alarm)


@alarm_views.route("/ding/", methods=["POST"])
def ding():
    ding_sync()
    return {"status": "ok"}


@alarm_views.route("/notify/", methods=["POST"])
@with_errors
@inject_schema(
    Schema(
        fields={
            "title": fields.Text(max=61),
            "description": fields.Text(
                max=127,
                required=False,
                default="",
            ),
        }
    ),
    use_args=False,
)
def notify(title: str, description: str):
    _notify(title, description)
    return {"status": "ok"}


class BaseAlarmList(View):
    @abstractmethod
    def get_base_query(self) -> Query:
        pass

    @abstractmethod
    def order_alarms(self, query: Query) -> Query:
        pass

    @inject_schema(schemas.AlarmListOptions())
    def dispatch_request(
        self,
        limit: int,
        query: t.Union[int, str, None],
    ):
        alarms = self.get_base_query()

        if isinstance(query, int):
            alarms = alarms.filter(models.Alarm.id == query)
        elif isinstance(query, str):
            alarms = alarms.filter(models.Alarm.text.contains(query))

        schema = AlarmSchema()

        return {
            "alarms": [
                schema.serialize(alarm)
                for alarm in self.order_alarms(alarms).limit(limit)
            ]
        }


class ViewAlarms(BaseAlarmList):
    def get_base_query(self) -> Query:
        return models.Alarm.active_alarms(SC.session)

    def order_alarms(self, query: Query) -> Query:
        return query.order_by(models.Alarm.end_at)


alarm_views.add_url_rule(
    "/", methods=["GET"], view_func=ViewAlarms.as_view("view_alarms")
)


class AlarmHistory(BaseAlarmList):
    def get_base_query(self) -> Query:
        return SC.session.query(models.Alarm)

    def order_alarms(self, query: Query) -> Query:
        return query.order_by(models.Alarm.started_at.desc())


alarm_views.add_url_rule(
    "/history/", methods=["GET"], view_func=AlarmHistory.as_view("alarm_history")
)


@alarm_views.route("/cancel/", methods=["PATCH"])
@with_errors
@inject_schema(schemas.UpdateAlarm(), use_args=False)
def cancel_alarm(target: models.Alarm):
    return AlarmSchema().serialize(MANAGER.cancel(target.id, SC.session))


@alarm_views.route("/acknowledge/", methods=["PATCH"])
@with_errors
@inject_schema(schemas.UpdateAlarm(), use_args=False)
def acknowledge_alarm(target: models.Alarm):
    return AlarmSchema().serialize(MANAGER.acknowledge(target.id, SC.session))


@alarm_views.route("/snooze/", methods=["PATCH"])
@with_errors
@inject_schema(schemas.SnoozeAlarm(), use_args=False)
def snooze_alarm(target: models.Alarm, new_target_time: datetime.datetime):
    return AlarmSchema().serialize(
        MANAGER.snooze(target.id, SC.session, new_target_time)
    )


@alarm_views.route("/cancel/", methods=["PATCH"])
def cancel_alarms():
    schema = AlarmSchema()

    return {
        "alarms": [schema.serialize(alarm) for alarm in MANAGER.cancel_all(SC.session)]
    }


@alarm_views.route("/acknowledge/all/", methods=["PATCH"])
def acknowledge_alarms():
    schema = AlarmSchema()

    return {
        "alarms": [
            schema.serialize(alarm) for alarm in MANAGER.acknowledge_all(SC.session)
        ]
    }

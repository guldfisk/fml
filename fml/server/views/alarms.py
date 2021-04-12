import datetime

from flask import request, Blueprint
from flask_api import status
from flask_api.request import APIRequest

from hardcandy.schema import DeserializationError

from fml.server import models
from fml.server.schemas import AlarmSchema
from fml.server.session import SessionContainer as SC
from fml.server.timer import MANAGER


alarm_views = Blueprint('alarm_views', __name__, url_prefix = '/alarms')
request: APIRequest


@alarm_views.route('/', methods = ['POST'])
def create_alarm():
    schema = AlarmSchema()

    try:
        alarm: models.Alarm = schema.deserialize(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    if alarm.end_at < datetime.datetime.now() - datetime.timedelta(seconds = 1):
        return 'Alarm must finish in the future', status.HTTP_400_BAD_REQUEST

    SC.session.add(alarm)

    SC.session.commit()

    MANAGER.handle_alarm(alarm.id)

    return schema.serialize(alarm)


@alarm_views.route('/', methods = ['GET'])
def view_alarms():
    limit = request.args.get('limit')

    alarms = models.Alarm.active_alarms(SC.session).order_by(models.Alarm.end_at).limit(limit)

    schema = AlarmSchema()

    return {
        'alarms': [
            schema.serialize(alarm)
            for alarm in
            alarms
        ]
    }


@alarm_views.route('/history/', methods = ['GET'])
def alarms_history():
    limit = request.args.get('limit')

    alarms = SC.session.query(models.Alarm).order_by(models.Alarm.started_at.desc()).limit(limit)

    schema = AlarmSchema()

    return {
        'alarms': [
            schema.serialize(alarm)
            for alarm in
            alarms
        ]
    }


@alarm_views.route('/cancel/<int:pk>/', methods = ['PATCH'])
def cancel_alarm(pk: int):
    alarm = MANAGER.cancel(pk, SC.session)

    if alarm is None:
        return 'no such alarm', status.HTTP_404_NOT_FOUND

    return AlarmSchema().serialize(alarm)


@alarm_views.route('/acknowledge/<int:pk>/', methods = ['PATCH'])
def acknowledge_alarm(pk: int):
    alarm = MANAGER.acknowledge(pk, SC.session)

    if alarm is None:
        return 'no such alarm', status.HTTP_404_NOT_FOUND

    return AlarmSchema().serialize(alarm)


@alarm_views.route('/cancel/', methods = ['PATCH'])
def cancel_alarms():
    schema = AlarmSchema()

    return {
        'alarms': [
            schema.serialize(alarm)
            for alarm in
            MANAGER.cancel_all(SC.session)
        ]
    }


@alarm_views.route('/acknowledge/', methods = ['PATCH'])
def acknowledge_alarms():
    schema = AlarmSchema()

    return {
        'alarms': [
            schema.serialize(alarm)
            for alarm in
            MANAGER.acknowledge_all(SC.session)
        ]
    }

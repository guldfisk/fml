from flask_api import FlaskAPI, status
from flask import request, Flask

from flask_api.request import APIRequest

from flask_sqlalchemy_session import flask_scoped_session

from sqlalchemy.orm import Session

from hardcandy.schema import DeserializationError

from fml import session_factory, models
from fml.schemas import AlarmSchema
from fml.timer import MANAGER


server_app: Flask = FlaskAPI(__name__)
session: Session = flask_scoped_session(session_factory, server_app)
request: APIRequest


@server_app.route('/', methods = ['GET'])
def ping():
    return 'ok'


@server_app.route('/alarm/', methods = ['POST'])
def create_alarm():
    schema = AlarmSchema()

    try:
        alarm = schema.deserialize(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    session.add(alarm)

    session.commit()

    MANAGER.handle_alarm(alarm.id)

    return schema.serialize(alarm)


@server_app.route('/alarms/', methods = ['GET'])
def view_alarms():
    alarms = models.Alarm.active_alarms(session).order_by(models.Alarm.end_at).all()

    schema = AlarmSchema()

    return {
        'alarms': [
            schema.serialize(alarm)
            for alarm in
            alarms
        ]
    }


@server_app.route('/alarms/history/', methods = ['GET'])
def alarms_history():
    alarms = session.query(models.Alarm).order_by(models.Alarm.started_at.desc()).limit(10)

    schema = AlarmSchema()

    return {
        'alarms': [
            schema.serialize(alarm)
            for alarm in
            alarms
        ]
    }


@server_app.route('/alarms/cancel/<int:pk>/', methods = ['POST'])
def cancel_alarm(pk: int):
    alarm = MANAGER.cancel(pk, session)

    if alarm is None:
        return 'no such alarm', status.HTTP_404_NOT_FOUND

    return AlarmSchema().serialize(alarm)


@server_app.route('/alarms/acknowledge/<int:pk>/', methods = ['POST'])
def acknowledge_alarm(pk: int):
    alarm = MANAGER.acknowledge(pk, session)

    if alarm is None:
        return 'no such alarm', status.HTTP_404_NOT_FOUND

    return AlarmSchema().serialize(alarm)


@server_app.route('/alarms/cancel/', methods = ['POST'])
def cancel_alarms():
    schema = AlarmSchema()

    return {
        'alarms': [
            schema.serialize(alarm)
            for alarm in
            MANAGER.cancel_all(session)
        ]
    }


@server_app.route('/alarms/acknowledge/', methods = ['POST'])
def acknowledge_alarms():
    schema = AlarmSchema()

    return {
        'alarms': [
            schema.serialize(alarm)
            for alarm in
            MANAGER.acknowledge_all(session)
        ]
    }

import datetime
import typing as t

from flask import request, Flask
from flask.views import View

from flask_api import FlaskAPI, status
from flask_api.request import APIRequest

from flask_sqlalchemy_session import flask_scoped_session

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import MultipleResultsFound

from hardcandy.schema import DeserializationError

from fml import session_factory, models
from fml.schemas import AlarmSchema, ToDoSchema
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


@server_app.route('/alarms/cancel/<int:pk>/', methods = ['PATCH'])
def cancel_alarm(pk: int):
    alarm = MANAGER.cancel(pk, session)

    if alarm is None:
        return 'no such alarm', status.HTTP_404_NOT_FOUND

    return AlarmSchema().serialize(alarm)


@server_app.route('/alarms/acknowledge/<int:pk>/', methods = ['PATCH'])
def acknowledge_alarm(pk: int):
    alarm = MANAGER.acknowledge(pk, session)

    if alarm is None:
        return 'no such alarm', status.HTTP_404_NOT_FOUND

    return AlarmSchema().serialize(alarm)


@server_app.route('/alarms/cancel/', methods = ['PATCH'])
def cancel_alarms():
    schema = AlarmSchema()

    return {
        'alarms': [
            schema.serialize(alarm)
            for alarm in
            MANAGER.cancel_all(session)
        ]
    }


@server_app.route('/alarms/acknowledge/', methods = ['PATCH'])
def acknowledge_alarms():
    schema = AlarmSchema()

    return {
        'alarms': [
            schema.serialize(alarm)
            for alarm in
            MANAGER.acknowledge_all(session)
        ]
    }


@server_app.route('/todo/', methods = ['POST'])
def create_todo():
    schema = ToDoSchema()

    try:
        todo = schema.deserialize(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    session.add(todo)

    session.commit()

    return schema.serialize(todo)


class ModifyTodo(View):

    def _modify_todo(self, todo: models.ToDo) -> None:
        pass

    def dispatch_request(self):
        target = request.data.get('target')

        if target is None:
            return 'no target', status.HTTP_400_BAD_REQUEST

        try:
            target = int(target)
        except ValueError:
            try:
                todo: t.Optional[models.ToDo] = models.ToDo.active_todos(session).filter(
                    models.ToDo.text.contains(target)
                ).scalar()
            except MultipleResultsFound:
                return 'ambiguous target', status.HTTP_400_BAD_REQUEST

        else:
            todo: t.Optional[models.ToDo] = models.ToDo.active_todos(session).filter(models.ToDo.id == target).scalar()

        if todo is None:
            return 'no such todo', status.HTTP_404_NOT_FOUND

        self._modify_todo(todo)

        session.commit()

        return ToDoSchema().serialize(todo)


class CancelTodo(ModifyTodo):

    def _modify_todo(self, todo: models.ToDo) -> None:
        todo.canceled = True


server_app.add_url_rule('/todo/cancel/', methods = ['PATCH'], view_func = CancelTodo.as_view('cancel_todo'))


class FinishTodo(ModifyTodo):

    def _modify_todo(self, todo: models.ToDo) -> None:
        todo.finished_at = datetime.datetime.now()


server_app.add_url_rule('/todo/finish/', methods = ['PATCH'], view_func = FinishTodo.as_view('finish_todo'))


@server_app.route('/todo/<int:pk>/', methods = ['GET'])
def get_todo(pk: int):
    todo: t.Optional[models.ToDo] = session.query(models.ToDo).get(pk)

    if todo is None:
        return 'no such todo', status.HTTP_404_NOT_FOUND

    return ToDoSchema().serialize(todo)


@server_app.route('/todo/history/', methods = ['GET'])
def todo_history():
    todos: t.List[models.ToDo] = session.query(models.ToDo).order_by(models.ToDo.created_at.desc())

    schema = ToDoSchema()

    return {
        'todos': [
            schema.serialize(todo)
            for todo in
            todos
        ]
    }


@server_app.route('/todo/', methods = ['GET'])
def todo_list():
    todos: t.List[models.ToDo] = models.ToDo.active_todos(session).order_by(models.ToDo.created_at.desc())

    schema = ToDoSchema()

    return {
        'todos': [
            schema.serialize(todo)
            for todo in
            todos
        ]
    }

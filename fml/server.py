import datetime
import functools
import typing as t

from flask import request, Flask
from flask.views import View

from flask_api import FlaskAPI, status
from flask_api.request import APIRequest

from flask_sqlalchemy_session import flask_scoped_session

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import MultipleResultsFound

from hardcandy.schema import DeserializationError

from fml import schemas
from fml import session_factory, models
from fml.schemas import AlarmSchema, ToDoSchema, TagSchema, TaggedSchema
from fml.timer import MANAGER


DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'

server_app: Flask = FlaskAPI(__name__)
session: Session = flask_scoped_session(session_factory, server_app)
request: APIRequest


def inject_project(f: t.Callable):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        project_id = models.Project.get_for_identifier(
            session,
            request.args.get('project'),
        )

        if project_id is None:
            return 'Invalid project', status.HTTP_400_BAD_REQUEST

        return f(*args, project_id = project_id, **kwargs)

    return wrapper


def inject_tag(f: t.Callable):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        tag_id = models.Tag.get_for_identifier(
            session,
            request.args.get('tag'),
        )

        return f(*args, tag_id = tag_id, **kwargs)

    return wrapper


@server_app.route('/', methods = ['GET'])
def ping():
    return 'ok'


@server_app.route('/alarm/', methods = ['POST'])
def create_alarm():
    schema = AlarmSchema()

    try:
        alarm: models.Alarm = schema.deserialize(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    if alarm.end_at < datetime.datetime.now() - datetime.timedelta(seconds = 1):
        return 'Alarm must finish in the future', status.HTTP_400_BAD_REQUEST

    session.add(alarm)

    session.commit()

    MANAGER.handle_alarm(alarm.id)

    return schema.serialize(alarm)


@server_app.route('/alarms/', methods = ['GET'])
def view_alarms():
    limit = request.args.get('limit')

    alarms = models.Alarm.active_alarms(session).order_by(models.Alarm.end_at).limit(limit)

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
    limit = request.args.get('limit')

    alarms = session.query(models.Alarm).order_by(models.Alarm.started_at.desc()).limit(limit)

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


@server_app.route('/project/', methods = ['POST'])
def create_project():
    schema = schemas.ProjectSchema()

    try:
        project = schema.deserialize(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    if project.is_default:
        session.query(models.Project).update({models.Project.is_default: False}, synchronize_session = False)

    session.add(project)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return 'Project already exists', status.HTTP_400_BAD_REQUEST

    return schema.serialize(project)


@server_app.route('/project/', methods = ['GET'])
def project_list():
    projects: t.List[models.ToDo] = session.query(models.Project).order_by(models.Project.created_at.desc())

    schema = schemas.ProjectSchema()

    return {
        'projects': [
            schema.serialize(project)
            for project in
            projects
        ]
    }


@server_app.route('/todo/', methods = ['POST'])
def create_todo():
    schema = ToDoSchema()

    try:
        todo_data = schema.deserialize_raw(request.data)
        create_data = schemas.CreateTodoSchema().deserialize_raw(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    project = create_data.get('project')

    if not project:
        todo_data['project_id'] = session.query(models.Project.id).filter(models.Project.is_default == True).scalar()
    else:
        if isinstance(project, int):
            _project = session.query(models.Project.id).get(project)
        else:
            try:
                _project = session.query(models.Project.id).filter(
                    models.Project.name.contains(project)
                ).scalar()
            except MultipleResultsFound:
                return 'ambiguous project "{}"'.format(project), status.HTTP_400_BAD_REQUEST

            if _project is None:
                return 'unknown project "{}"'.format(project), status.HTTP_400_BAD_REQUEST

            todo_data['project_id'] = _project

    todo = models.ToDo(**todo_data)

    for tag in create_data['tags']:
        if isinstance(tag, int):
            _tag = session.query(models.Tag).get(tag)
        else:
            try:
                _tag = session.query(models.Tag).filter(
                    models.Tag.name.contains(tag)
                ).scalar()
            except MultipleResultsFound:
                return 'ambiguous tag "{}"'.format(tag), status.HTTP_400_BAD_REQUEST

        if _tag is None:
            return 'unknown tag "{}"'.format(tag), status.HTTP_400_BAD_REQUEST

        todo.tags.append(_tag)

    session.add(todo)

    session.commit()

    return schema.serialize(todo)


@server_app.route('/tag/', methods = ['POST'])
def create_tag():
    schema = TagSchema()

    try:
        tag = schema.deserialize(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    session.add(tag)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return 'Tag already exists', status.HTTP_400_BAD_REQUEST

    return schema.serialize(tag)


@server_app.route('/todo/tag/', methods = ['POST'])
def tag_todo():
    schema = TaggedSchema()

    try:
        tagged = schema.deserialize_raw(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    if isinstance(tagged['todo_id'], int):
        todo_id = tagged['todo_id']
    else:
        try:
            todo_id = models.ToDo.active_todos(session, target = models.ToDo.id).filter(
                models.ToDo.text.contains(tagged['todo_id'])
            ).scalar()
        except MultipleResultsFound:
            return 'ambiguous todo', status.HTTP_400_BAD_REQUEST

    if isinstance(tagged['tag_id'], int):
        tag_id = tagged['tag_id']
    else:
        try:
            tag_id = session.query(models.Tag.id).filter(
                models.Tag.name.contains(tagged['tag_id'])
            ).scalar()
        except MultipleResultsFound:
            return 'ambiguous tag', status.HTTP_400_BAD_REQUEST

    tag = models.Tagged(todo_id = todo_id, tag_id = tag_id)

    session.add(tag)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return 'Invalid args', status.HTTP_400_BAD_REQUEST

    return {'status': 'ok'}, status.HTTP_201_CREATED


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

        v = self._modify_todo(todo)

        if isinstance(v, t.Tuple):
            return v

        session.commit()

        return ToDoSchema().serialize(todo)


class CancelTodo(ModifyTodo):

    def _modify_todo(self, todo: models.ToDo) -> None:
        todo.canceled = True
        todo.finished_at = datetime.datetime.now()


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
@inject_project
@inject_tag
def todo_history(project_id: int, tag_id: t.Optional[int]):
    limit = request.args.get('limit')

    todos = session.query(models.ToDo).filter(
        models.ToDo.project_id == project_id
    ).order_by(models.ToDo.created_at.desc())

    if tag_id is not None:
        todos = todos.join(models.Tagged).filter(models.Tagged.tag_id == tag_id)

    todos = todos.limit(limit)

    schema = ToDoSchema()

    return {
        'todos': [
            schema.serialize(todo)
            for todo in
            todos
        ]
    }


@server_app.route('/todo/', methods = ['GET'])
@inject_project
@inject_tag
def todo_list(project_id: int, tag_id: t.Optional[int]):
    todos = models.ToDo.active_todos(session).filter(
        models.ToDo.project_id == project_id
    ).order_by(models.ToDo.created_at.desc())

    if tag_id is not None:
        todos = todos.join(models.Tagged).filter(models.Tagged.tag_id == tag_id)

    schema = ToDoSchema()

    return {
        'todos': [
            schema.serialize(todo)
            for todo in
            todos
        ]
    }


@server_app.route('/tag/', methods = ['GET'])
def tag_list():
    tags: t.List[models.Tag] = session.query(models.Tag).order_by(models.Tag.created_at.desc())

    schema = TagSchema()

    return {
        'tags': [
            schema.serialize(tag)
            for tag in
            tags
        ]
    }


@server_app.route('/todo/burn-down/', methods = ['GET'])
@inject_project
@inject_tag
def todo_burn_down(project_id: int, tag_id = t.Optional[int]):
    todos = session.query(models.ToDo).filter(models.ToDo.project_id == project_id)

    if tag_id is not None:
        todos = todos.join(models.Tagged).filter(models.Tagged.tag_id == tag_id)

    todos = list(todos)

    if not todos:
        return {
            'points': [],
        }

    changes: t.List[t.Tuple[datetime.datetime, int]] = []

    for todo in todos:
        changes.append((todo.created_at, 1))
        if todo.finished_at is not None:
            changes.append((todo.finished_at, -1))

    changes.append((datetime.datetime.now(), 0))

    changes = sorted(changes, key = lambda p: p[0])

    active = 0
    points = []

    for time, delta in changes:
        active += delta
        points.append(
            (
                time.strftime(DATETIME_FORMAT),
                active,
            )
        )

    return {
        'points': points,
    }


@server_app.route('/todo/throughput/', methods = ['GET'])
@inject_project
@inject_tag
def todo_throughput(project_id: int, tag_id: t.Optional[int]):
    todos = session.query(models.ToDo.finished_at).filter(
        models.ToDo.canceled == False,
        models.ToDo.finished_at != None,
        models.ToDo.project_id == project_id,
    ).order_by(models.ToDo.finished_at)

    if tag_id is not None:
        todos = todos.join(models.Tagged).filter(models.Tagged.tag_id == tag_id)

    finished_dates = [
        v[0].date()
        for v in
        todos
    ]

    if not finished_dates:
        return {
            'points': [],
        }

    finished_dates_map = [
        0
        for _ in range(
            (datetime.datetime.now().date() - finished_dates[0]).days + 1
        )
    ]

    for finished_date in finished_dates:
        finished_dates_map[(finished_date - finished_dates[0]).days] += 1

    points = []

    for idx in range(len(finished_dates_map)):
        _slice = finished_dates_map[max(0, idx - 5):idx + 1]
        points.append(
            (
                (finished_dates[0] + datetime.timedelta(days = idx)).strftime(DATETIME_FORMAT),
                sum(_slice) / len(_slice),
            )
        )

    return {
        'points': points,
    }

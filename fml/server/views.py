import copy
import datetime
import functools
import typing as t
from abc import abstractmethod

from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import joinedload, Query
from sqlalchemy.orm.exc import MultipleResultsFound

from flask import request, Blueprint
from flask.views import View
from flask_api import status
from flask_api.request import APIRequest

from hardcandy import fields
from hardcandy.schema import DeserializationError, Schema, Field

from fml.server import models
from fml.server import schemas
from fml.server.schemas import AlarmSchema, ToDoSchema, TagSchema, TaggedSchema
from fml.server.session import SessionContainer as SC
from fml.server.timer import MANAGER


DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'

views = Blueprint('views', __name__)
request: APIRequest


def inject_project(f: t.Callable):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        project_id = models.Project.get_for_identifier(
            SC.session,
            request.args.get('project'),
            target = models.Project.id,
        )

        if project_id is None:
            return 'Invalid project', status.HTTP_400_BAD_REQUEST

        return f(*args, project_id = project_id, **kwargs)

    return wrapper


def inject_tag(f: t.Callable):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        tag_id = models.Tag.get_for_identifier(
            SC.session,
            request.args.get('tag'),
            target = models.Tag.id,
        )

        return f(*args, tag_id = tag_id, **kwargs)

    return wrapper


def inject_schema(schema: Schema):
    def wrapper(f: t.Callable):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            try:
                values = schema.deserialize_raw(request.args)
            except DeserializationError as e:
                return e.serialized, status.HTTP_400_BAD_REQUEST

            return f(*args, **values, **kwargs)

        return wrapped

    return wrapper


@views.route('/', methods = ['GET'])
def ping():
    return 'ok'


@views.route('/alarm/', methods = ['POST'])
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


@views.route('/alarms/', methods = ['GET'])
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


@views.route('/alarms/history/', methods = ['GET'])
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


@views.route('/alarms/cancel/<int:pk>/', methods = ['PATCH'])
def cancel_alarm(pk: int):
    alarm = MANAGER.cancel(pk, SC.session)

    if alarm is None:
        return 'no such alarm', status.HTTP_404_NOT_FOUND

    return AlarmSchema().serialize(alarm)


@views.route('/alarms/acknowledge/<int:pk>/', methods = ['PATCH'])
def acknowledge_alarm(pk: int):
    alarm = MANAGER.acknowledge(pk, SC.session)

    if alarm is None:
        return 'no such alarm', status.HTTP_404_NOT_FOUND

    return AlarmSchema().serialize(alarm)


@views.route('/alarms/cancel/', methods = ['PATCH'])
def cancel_alarms():
    schema = AlarmSchema()

    return {
        'alarms': [
            schema.serialize(alarm)
            for alarm in
            MANAGER.cancel_all(SC.session)
        ]
    }


@views.route('/alarms/acknowledge/', methods = ['PATCH'])
def acknowledge_alarms():
    schema = AlarmSchema()

    return {
        'alarms': [
            schema.serialize(alarm)
            for alarm in
            MANAGER.acknowledge_all(SC.session)
        ]
    }


@views.route('/project/', methods = ['POST'])
def create_project():
    schema = schemas.ProjectSchema()

    try:
        project = schema.deserialize(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    if project.is_default:
        SC.session.query(models.Project).update({models.Project.is_default: False}, synchronize_session = False)

    SC.session.add(project)

    try:
        SC.session.commit()
    except IntegrityError:
        SC.session.rollback()
        return 'Project already exists', status.HTTP_400_BAD_REQUEST

    return schema.serialize(project)


@views.route('/project/', methods = ['GET'])
def project_list():
    projects: t.List[models.ToDo] = SC.session.query(models.Project).order_by(models.Project.created_at.desc())

    schema = schemas.ProjectSchema()

    return {
        'projects': [
            schema.serialize(project)
            for project in
            projects
        ]
    }


@views.route('/todo/', methods = ['POST'])
def create_todo():
    schema = ToDoSchema()

    try:
        todo_data = schema.deserialize_raw(request.data)
        create_data = schemas.CreateTodoSchema().deserialize_raw(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    project = create_data.get('project')

    if not project:
        todo_data['project_id'] = SC.session.query(models.Project.id).filter(models.Project.is_default == True).scalar()
    else:
        if isinstance(project, int):
            _project = SC.session.query(models.Project.id).get(project)
        else:
            try:
                _project = SC.session.query(models.Project.id).filter(
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
            _tag = SC.session.query(models.Tag).get(tag)
        else:
            try:
                _tag = SC.session.query(models.Tag).filter(
                    models.Tag.name.contains(tag)
                ).scalar()
            except MultipleResultsFound:
                return 'ambiguous tag "{}"'.format(tag), status.HTTP_400_BAD_REQUEST

        if _tag is None:
            return 'unknown tag "{}"'.format(tag), status.HTTP_400_BAD_REQUEST

        todo.tags.append(_tag)

    for parent in create_data['parents']:
        parent = models.ToDo.get_for_identifier(SC.session, parent, base_query = models.ToDo.active_todos(SC.session))
        if parent is None:
            return 'Invalid parent', status.HTTP_400_BAD_REQUEST

        todo.parents.append(parent)

    SC.session.add(todo)

    SC.session.commit()

    return schema.serialize(todo)


@views.route('/tag/', methods = ['POST'])
def create_tag():
    schema = TagSchema()

    try:
        tag = schema.deserialize(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    SC.session.add(tag)

    try:
        SC.session.commit()
    except IntegrityError:
        SC.session.rollback()
        return 'Tag already exists', status.HTTP_400_BAD_REQUEST

    return schema.serialize(tag)


@views.route('/todo/tag/', methods = ['POST'])
def tag_todo():
    schema = TaggedSchema()

    try:
        tagged = schema.deserialize_raw(request.data)
    except DeserializationError as e:
        return e.serialized, status.HTTP_400_BAD_REQUEST

    todo: t.Optional[models.ToDo] = models.ToDo.get_for_identifier(
        SC.session,
        tagged['todo_id'],
        base_query = models.ToDo.active_todos(SC.session),
    )

    if todo is None:
        return 'Invalid todo', status.HTTP_400_BAD_REQUEST

    tag: t.Optional[models.Tag] = models.Tag.get_for_identifier(
        SC.session,
        tagged['tag_id'],
        target = models.Tag,
    )

    if tag is None:
        return 'Invalid tag', status.HTTP_400_BAD_REQUEST

    todo.tags.append(tag)

    if tagged['recursive']:
        for child in todo.traverse_children():
            child.tags.append(tag)

    try:
        SC.session.commit()
    except (IntegrityError, OperationalError):
        SC.session.rollback()
        return 'Invalid args', status.HTTP_400_BAD_REQUEST

    return {'status': 'ok'}, status.HTTP_201_CREATED


@views.route('/todo/add-dependency/', methods = ['POST'])
def add_dependency():
    parent: t.Optional[models.ToDo] = models.ToDo.get_for_identifier(
        SC.session,
        request.data.get('parent'),
        base_query = models.ToDo.active_todos(SC.session),
    )

    if parent is None:
        return 'Invalid parent', status.HTTP_400_BAD_REQUEST

    child: t.Optional[models.ToDo] = models.ToDo.get_for_identifier(
        SC.session,
        request.data.get('child'),
        base_query = models.ToDo.active_todos(SC.session),
    )

    if child is None:
        return 'Invalid child', status.HTTP_400_BAD_REQUEST

    if parent in child.traverse_children(active_only = False):
        return 'Dependencies can not be circular', status.HTTP_400_BAD_REQUEST

    dependency = models.Dependency(parent_id = parent.id, child_id = child.id)

    SC.session.add(dependency)

    try:
        SC.session.commit()
    except (IntegrityError, OperationalError):
        SC.session.rollback()
        return 'Invalid args', status.HTTP_400_BAD_REQUEST

    return schemas.ToDoSchema().serialize(parent), status.HTTP_201_CREATED


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
                todo: t.Optional[models.ToDo] = models.ToDo.active_todos(SC.session).filter(
                    models.ToDo.text.contains(target)
                ).scalar()
            except MultipleResultsFound:
                return 'ambiguous target', status.HTTP_400_BAD_REQUEST

        else:
            todo: t.Optional[models.ToDo] = models.ToDo.active_todos(SC.session).filter(
                models.ToDo.id == target).scalar()

        if todo is None:
            return 'no such todo', status.HTTP_404_NOT_FOUND

        self._modify_todo(todo)

        for child in todo.traverse_children(active_only = False):
            self._modify_todo(child)

        SC.session.commit()

        return ToDoSchema().serialize(todo)


class CancelTodo(ModifyTodo):

    def _modify_todo(self, todo: models.ToDo) -> None:
        todo.canceled = True
        todo.finished_at = datetime.datetime.now()


views.add_url_rule('/todo/cancel/', methods = ['PATCH'], view_func = CancelTodo.as_view('cancel_todo'))


class FinishTodo(ModifyTodo):

    def _modify_todo(self, todo: models.ToDo) -> None:
        todo.finished_at = datetime.datetime.now()


views.add_url_rule('/todo/finish/', methods = ['PATCH'], view_func = FinishTodo.as_view('finish_todo'))


@views.route('/todo/<int:pk>/', methods = ['GET'])
def get_todo(pk: int):
    todo: t.Optional[models.ToDo] = SC.session.query(models.ToDo).get(pk)

    if todo is None:
        return 'no such todo', status.HTTP_404_NOT_FOUND

    return ToDoSchema().serialize(todo)


class BaseToDoList(View):

    @abstractmethod
    def get_base_query(self) -> Query:
        pass

    @abstractmethod
    def get_schema_fields(self) -> t.Mapping[str, Field]:
        pass

    def limit(self, query: Query, limit: int) -> Query:
        return query

    @inject_schema(schemas.ToDoListOptions())
    def dispatch_request(
        self,
        project: models.Project,
        tag: t.Optional[models.Tag],
        query: t.Optional[str],
        all_tasks: bool,
        flat: bool,
        limit: int,
    ):
        todos = self.get_base_query().filter(
            models.ToDo.project_id == project.id,
        ).order_by(models.ToDo.created_at.desc()).options(joinedload('tags'), joinedload('children'))

        if not all_tasks:
            todos = todos.filter(
                ~exists().where(models.Dependency.child_id == models.ToDo.id),
            )

        if query:
            todos = todos.filter(models.ToDo.text.contains(query))

        if tag is not None:
            todos = todos.join(models.Tagged).filter(models.Tagged.tag_id == tag.id)

        todos = self.limit(todos, limit)

        schema = schemas.ToDoSchema(
            fields = self.get_schema_fields()
        )

        if flat:
            schema.fields = copy.copy(schema.fields)
            del schema.fields['children']

        return {
            'todos': [
                schema.serialize(todo)
                for todo in
                todos
            ]
        }


class ToDoHistory(BaseToDoList):

    def get_schema_fields(self) -> t.Mapping[str, Field]:
        return {
            'children': fields.List(fields.SelfRelated(), read_only = True)
        }

    def get_base_query(self) -> Query:
        return SC.session.query(models.ToDo)

    def limit(self, query: Query, limit: int) -> Query:
        return query.limit(limit)


views.add_url_rule('/todo/history/', methods = ['GET'], view_func = ToDoHistory.as_view('todo_history'))


class ToDoList(BaseToDoList):

    def get_schema_fields(self) -> t.Mapping[str, Field]:
        return {}

    def get_base_query(self) -> Query:
        return models.ToDo.active_todos(SC.session)


views.add_url_rule('/todo/', methods = ['GET'], view_func = ToDoList.as_view('todo_list'))


@views.route('/tag/', methods = ['GET'])
def tag_list():
    tags: t.List[models.Tag] = SC.session.query(models.Tag).order_by(models.Tag.created_at.desc())

    schema = TagSchema()

    return {
        'tags': [
            schema.serialize(tag)
            for tag in
            tags
        ]
    }


@views.route('/todo/burn-down/', methods = ['GET'])
@inject_project
@inject_tag
def todo_burn_down(project_id: int, tag_id = t.Optional[int]):
    todos = SC.session.query(models.ToDo).filter(models.ToDo.project_id == project_id)

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


@views.route('/todo/throughput/', methods = ['GET'])
@inject_project
@inject_tag
def todo_throughput(project_id: int, tag_id: t.Optional[int]):
    todos = SC.session.query(models.ToDo.finished_at).filter(
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

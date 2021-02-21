import datetime
import typing as t

from flask import Blueprint
from flask_api.request import APIRequest

from fml.server import models
from fml.server.session import SessionContainer as SC
from fml.server.views.utils import inject_project, inject_tag, DATETIME_FORMAT


todo_stat_views = Blueprint('todo_stat_views', __name__)
request: APIRequest


@todo_stat_views.route('/todo/burn-down/', methods = ['GET'])
@inject_project()
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


@todo_stat_views.route('/todo/throughput/', methods = ['GET'])
@inject_project()
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
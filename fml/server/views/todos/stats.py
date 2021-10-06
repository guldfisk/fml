import datetime
import typing as t

from flask import Blueprint
from flask_api.request import APIRequest

from sqlalchemy import exists

import pandas as pd

from fml.server import models, schemas
from fml.server.retrieve import get_project_and_minimum_priority
from fml.server.session import SessionContainer as SC
from fml.server.views.utils import DATETIME_FORMAT, inject_schema, with_errors


todo_stat_views = Blueprint('todo_stat_views', __name__)
request: APIRequest


@todo_stat_views.route('/todo/burn-down/', methods = ['GET'])
@with_errors
@inject_schema(schemas.StatsOptionsSchema())
def todo_burn_down(
    project: t.Union[int, str, None],
    tag: t.Optional[models.Tag],
    top_level_only: bool,
    minimum_priority: t.Union[int, str, None],
    ignore_priority: bool,
    last_n_days: int,
):
    project, level = get_project_and_minimum_priority(SC.session, project, minimum_priority, ignore_priority)

    todos = SC.session.query(models.ToDo)

    if project is not None:
        todos = todos.filter(models.ToDo.project_id == project.id)

    if level is not None:
        todos = todos.join(models.Priority).filter(models.Priority.level <= level)

    if tag is not None:
        todos = todos.join(models.Tagged).filter(models.Tagged.tag_id == tag.id)

    if top_level_only:
        todos = todos.filter(
            ~exists().where(models.Dependency.child_id == models.ToDo.id),
        )

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
        'points': points[-last_n_days:],
    }


@todo_stat_views.route('/todo/throughput/', methods = ['GET'])
@with_errors
@inject_schema(schemas.StatsOptionsSchema())
def todo_throughput(
    project: t.Union[int, str, None],
    tag: t.Optional[models.Tag],
    top_level_only: bool,
    minimum_priority: t.Union[int, str, None],
    ignore_priority: bool,
    last_n_days: int,
):
    project, level = get_project_and_minimum_priority(SC.session, project, minimum_priority, ignore_priority)

    todos = SC.session.query(models.ToDo.finished_at).filter(
        models.ToDo.state == models.State.COMPLETED,
    ).order_by(models.ToDo.finished_at)

    if project is not None:
        todos = todos.filter(models.ToDo.project_id == project.id, )

    if level is not None:
        todos = todos.join(models.Priority).filter(models.Priority.level <= level)

    if tag is not None:
        todos = todos.join(models.Tagged).filter(models.Tagged.tag_id == tag.id)

    if top_level_only:
        todos = todos.filter(
            ~exists().where(models.Dependency.child_id == models.ToDo.id),
        )

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

    series = pd.Series([0] + finished_dates_map)

    smooth_points = list(series.ewm(halflife = 16).mean())[1:]

    points = [
        (
            (finished_dates[0] + datetime.timedelta(days = idx)).strftime(DATETIME_FORMAT),
            smooth_points[idx],
        )
        for idx in
        range(max(0, len(finished_dates_map) - last_n_days), len(finished_dates_map))
    ]

    return {
        'points': points,
    }

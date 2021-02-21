import functools
import typing as t

from flask import request
from flask_api import status

from fml.server import models
from fml.server.session import SessionContainer as SC
from hardcandy.schema import DeserializationError, Schema


DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'


def inject_project(use_args: bool = True):
    def wrapper(f: t.Callable):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            project_id = models.Project.get_for_identifier(
                SC.session,
                request.args.get('project') if use_args else request.data.get('project'),
                target = models.Project.id,
            )

            if project_id is None:
                return 'Invalid project', status.HTTP_400_BAD_REQUEST

            return f(*args, project_id = project_id, **kwargs)

        return wrapped

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


def inject_schema(schema: Schema, use_args: bool = True):
    def wrapper(f: t.Callable):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            try:
                values = schema.deserialize_raw(request.args if use_args else request.data)
            except DeserializationError as e:
                return e.serialized, status.HTTP_400_BAD_REQUEST

            return f(*args, **values, **kwargs)

        return wrapped

    return wrapper

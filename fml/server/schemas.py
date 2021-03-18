import re

from hardcandy import fields
from hardcandy.schema import Schema

from fml.server import models
from fml.server import fields as custom_fields


class AlarmSchema(Schema[models.Alarm]):
    id = fields.Integer(read_only = True)

    text = fields.Text()

    started_at = fields.Datetime(read_only = True)
    end_at = fields.Datetime()

    requires_acknowledgment = fields.Bool(required = False)
    retry_delay = fields.Integer(required = False, min = 5)
    send_email = fields.Bool(required = False)
    silent = fields.Bool(required = False)
    level = fields.Enum(models.ImportanceLevel, required = False)

    times_notified = fields.Integer(read_only = True)
    acknowledged = fields.Bool(read_only = True)

    canceled = fields.Bool(read_only = True)
    success = fields.Bool(read_only = True)


class ProjectSchema(Schema[models.Project]):
    id = fields.Integer(read_only = True)
    name = fields.Text(min = 1, max = 127, pattern = re.compile(r'\w+'))
    created_at = fields.Datetime(read_only = True)
    is_default = fields.Bool(default = False)


class TaggedSchema(Schema[models.Tagged]):
    todo_id = fields.CoalesceField([fields.Integer(), fields.Text()])
    tag_id = fields.CoalesceField([fields.Integer(), fields.Text()])
    recursive = fields.Bool(default = False, write_only = True)


class TagSchema(Schema[models.Tag]):
    id = fields.Integer(read_only = True)
    name = fields.Text(min = 1, max = 127, pattern = re.compile(r'\w+'))
    created_at = fields.Datetime(read_only = True)


class PrioritySchema(Schema[models.Priority]):
    id = fields.Integer(read_only = True)
    name = fields.Text(min = 1, max = 127, pattern = re.compile(r'\w+'))
    created_at = fields.Datetime(read_only = True)
    level = fields.Integer()
    project = fields.Lambda(lambda p: p.project.name)
    is_default = fields.Bool(default = False)


class PriorityCreateSchema(PrioritySchema):
    project = custom_fields.StringIdentifiedField(models.Project, default = None)


class CreateTodoSchema(Schema):
    tags = fields.List(
        fields.CoalesceField(
            [
                fields.Integer(),
                fields.Text(min = 1, max = 127, pattern = re.compile(r'\w+')),
            ]
        ),
        default = (),
    )
    project = fields.CoalesceField(
        [
            fields.Integer(),
            fields.Text(min = 1, max = 127, pattern = re.compile(r'\w+')),
        ],
        required = False,
    )
    parents = fields.List(
        fields.CoalesceField(
            [
                fields.Integer(),
                fields.Text(),
            ]
        ),
        default = (),
    )
    priority = fields.CoalesceField(
        [
            fields.Integer(),
            fields.Text(min = 1, max = 127, pattern = re.compile(r'\w+')),
        ],
        required = False,
    )


class UpdateDependencySchema(Schema):
    parent = custom_fields.StringIdentifiedField(models.ToDo, base_query_getter = lambda s: models.ToDo.active_todos(s))
    child = custom_fields.StringIdentifiedField(models.ToDo, base_query_getter = lambda s: models.ToDo.active_todos(s))


class ToDoListOptions(Schema):
    project = custom_fields.StringIdentifiedField(models.Project, default = None)
    tag = custom_fields.StringIdentifiedField(models.Tag, default = None, required = False)
    query = fields.Text(default = '')
    all_tasks = fields.Bool(default = False)
    flat = fields.Bool(default = False)
    limit = fields.Integer(default = 25)
    priority = fields.CoalesceField([fields.Integer(), fields.Text()], default = None, required = False)


class ToDoSchema(Schema[models.ToDo]):
    id = fields.Integer(read_only = True)

    text = fields.Text()

    tags = fields.Lambda(lambda todo: [tag.name for tag in todo.tags])
    project = fields.Lambda(lambda todo: todo.project.name)

    priority = fields.Lambda(lambda todo: todo.priority.name)

    created_at = fields.Datetime(read_only = True)
    finished_at = fields.Datetime(read_only = True)

    canceled = fields.Bool(read_only = True)

    children = fields.List(fields.SelfRelated(), read_only = True, source = 'active_children')


class ModifyPrioritySchema(Schema[models.Tagged]):
    todo = custom_fields.StringIdentifiedField(
        models.ToDo,
        base_query_getter = lambda s: models.ToDo.active_todos(s),
    )
    priority = fields.CoalesceField([fields.Integer(), fields.Text()])
    recursive = fields.Bool(default = False, write_only = True)


class ModifyToDoSchema(Schema):
    todo = custom_fields.StringIdentifiedField(
        models.ToDo,
        base_query_getter = lambda s: models.ToDo.active_todos(s),
    )
    description = fields.Text()

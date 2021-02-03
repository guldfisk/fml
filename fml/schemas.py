import re

from hardcandy import fields
from hardcandy.schema import Schema

from fml import models


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


class TaggedSchema(Schema[models.Tagged]):
    todo_id = fields.CoalesceField([fields.Integer(), fields.Text()])
    tag_id = fields.CoalesceField([fields.Integer(), fields.Text()])


class TagSchema(Schema[models.Tag]):
    id = fields.Integer(read_only = True)
    name = fields.Text(min = 1, max = 127, pattern = re.compile(r'\w+'))
    created_at = fields.Datetime(read_only = True)


class TagsSchema(Schema):
    tags = fields.List(
        fields.CoalesceField(
            [
                fields.Integer(),
                fields.Text(min = 1, max = 127, pattern = re.compile(r'\w+')),
            ]
        ),
        default = (),
    )


class ToDoSchema(Schema[models.ToDo]):
    id = fields.Integer(read_only = True)

    text = fields.Text()

    tags = fields.Lambda(lambda todo: [tag.name for tag in todo.tags])

    created_at = fields.Datetime(read_only = True)
    finished_at = fields.Datetime(read_only = True)

    canceled = fields.Bool(read_only = True)

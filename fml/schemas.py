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

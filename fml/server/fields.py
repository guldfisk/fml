import typing as t

from hardcandy.schema import Field, Schema, Primitive, T, FieldValidationError

from fml.server.models import StringIdentified
from fml.server.session import SessionContainer as SC


S = t.TypeVar('S', bound = StringIdentified)


class StringIdentifiedField(Field[S]):

    def __init__(self, model: t.Type[S], **kwargs):
        super().__init__(**kwargs)
        self._model = model

    def serialize(self, value: T, instance: object, schema: Schema) -> Primitive:
        raise NotImplemented()

    def deserialize(self, value: Primitive, schema: Schema) -> S:
        if not (value is None or isinstance(value, int) or isinstance(value, str)):
            raise FieldValidationError(self, 'invalid value type')

        model = self._model.get_for_identifier(
            SC.session,
            value,
        )

        if self.required and model is None:
            raise FieldValidationError(self, 'No match')

        return model

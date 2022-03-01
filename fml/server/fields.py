import typing as t

from sqlalchemy.orm import Query, Session

from hardcandy.schema import Field, Schema, Primitive, T, FieldValidationError

from fml.server.models import StringIdentified
from fml.server.session import SessionContainer as SC


S = t.TypeVar('S', bound = StringIdentified)


class StringIdentifiedField(Field[S]):

    def __init__(self, model: t.Type[S], base_query_getter: t.Optional[t.Callable[[Session], Query]] = None, **kwargs):
        kwargs['deserialize_none'] = True
        super().__init__(**kwargs)
        self._model = model
        self._base_query_getter = base_query_getter

    def serialize(self, value: T, instance: object, schema: Schema) -> Primitive:
        raise NotImplemented()

    def deserialize(self, value: Primitive, schema: Schema) -> S:
        if value is None or isinstance(value, int):
            pass
        elif isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        else:
            raise FieldValidationError(self, 'invalid value type')

        model = self._model.get_for_identifier(
            SC.session,
            value,
            base_query = None if self._base_query_getter is None else self._base_query_getter(SC.session),
        )

        if self.required and model is None:
            raise FieldValidationError(self, 'No match')

        return model


class StringIdentifiedOrRaiseField(Field[S]):

    def __init__(
        self,
        model: t.Type[S],
        error_schema: Schema,
        base_query_getter: t.Optional[t.Callable[[Session], Query]] = None,
        **kwargs,
    ):
        kwargs['deserialize_none'] = True
        super().__init__(**kwargs)
        self._model = model
        self._error_schema = error_schema
        self._base_query_getter = base_query_getter

    def serialize(self, value: T, instance: object, schema: Schema) -> Primitive:
        raise NotImplemented()

    def deserialize(self, value: Primitive, schema: Schema) -> S:
        if value is None or isinstance(value, int):
            pass
        elif isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        else:
            raise FieldValidationError(self, 'invalid value type')

        model = self._model.get_for_identifier_or_raise(
            SC.session,
            value,
            self._error_schema,
            base_query = None if self._base_query_getter is None else self._base_query_getter(SC.session)
        )

        if self.required and model is None:
            raise FieldValidationError(self, 'No match')

        return model

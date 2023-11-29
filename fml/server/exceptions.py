import typing as t
from abc import abstractmethod

from hardcandy.schema import Schema


class RequestError(Exception):
    error_name: str

    @abstractmethod
    def error_body(self) -> t.Mapping[str, t.Any]:
        pass

    def serialize(self) -> t.Mapping[str, t.Any]:
        return {
            "error_type": self.error_name,
            **self.error_body(),
        }


class SimpleError(RequestError):
    error_name = "error_message"

    def __init__(self, message: str):
        self._message = message

    def error_body(self) -> t.Mapping[str, t.Any]:
        return {
            "message": self._message,
        }


class MultipleCandidateError(RequestError):
    error_name = "multiple_candidate_error"

    def __init__(
        self,
        candidate_type: t.Type,
        candidates: t.List[object],
        schema: Schema,
        message: str = "ambiguous target",
    ):
        self._candidate_type = candidate_type
        self._candidates = candidates
        self._schema = schema
        self._message = message

    def error_body(self) -> t.Mapping[str, t.Any]:
        return {
            "message": self._message,
            "candidate_type": self._candidate_type.__name__.lower(),
            "candidates": [
                self._schema.serialize(candidate) for candidate in self._candidates
            ],
        }

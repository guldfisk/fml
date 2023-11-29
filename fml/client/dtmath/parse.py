import datetime
import typing as t

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from fml.client.dtmath.gen.dtmath_grammarLexer import dtmath_grammarLexer
from fml.client.dtmath.gen.dtmath_grammarParser import dtmath_grammarParser
from fml.client.dtmath.visitor import DTMVisitor


class DTMParseException(Exception):
    pass


class SearchPatternParseListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise DTMParseException("Syntax error")

    def reportContextSensitivity(
        self, recognizer, dfa, startIndex, stopIndex, prediction, configs
    ):
        raise DTMParseException("Conetext sensitivity")


class DTMParser(object):
    def __init__(self):
        self._visitor = DTMVisitor()

    def parse(self, s: str) -> t.Union[datetime.datetime, datetime.timedelta]:
        parser = dtmath_grammarParser(
            CommonTokenStream(dtmath_grammarLexer(InputStream(s)))
        )

        parser._listeners = [SearchPatternParseListener()]

        return self._visitor.visit(parser.start())

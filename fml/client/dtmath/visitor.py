import datetime

from fml.client.dtmath.gen.dtmath_grammarParser import dtmath_grammarParser
from fml.client.dtmath.gen.dtmath_grammarVisitor import dtmath_grammarVisitor
from fml.client.dtmath.utils import get_next_weekday, get_weekday


class DTMVisitor(dtmath_grammarVisitor):

    def __init__(self):
        self._now = datetime.datetime.now()

    def _current_date(self) -> datetime.datetime:
        return datetime.datetime(year = self._now.year, month = self._now.month, day = self._now.day)

    def visitStart(self, ctx: dtmath_grammarParser.StartContext):
        return self.visit(ctx.operation())

    def visitAdditionOperation(self, ctx: dtmath_grammarParser.AdditionOperationContext):
        return self.visit(ctx.operation(0)) + self.visit(ctx.operation(1))

    def visitSubtractionOperation(self, ctx: dtmath_grammarParser.SubtractionOperationContext):
        return self.visit(ctx.operation(0)) - self.visit(ctx.operation(1))

    def visitTimeOperation(self, ctx: dtmath_grammarParser.TimeOperationContext):
        return self.visit(ctx.time())

    def visitTimeAbs(self, ctx: dtmath_grammarParser.TimeAbsContext):
        return self.visit(ctx.abs_time())

    def visitTimeDelta(self, ctx: dtmath_grammarParser.TimeDeltaContext):
        return self.visit(ctx.delta_time())

    def visitDeltaTimeSingle(self, ctx: dtmath_grammarParser.DeltaTimeSingleContext):
        return self.visit(ctx.delta_time_unit())

    def visitDeltaTimeChain(self, ctx: dtmath_grammarParser.DeltaTimeChainContext):
        return self.visit(ctx.delta_time_unit()) + self.visit(ctx.delta_time())

    def visitDeltaUnitFirst(self, ctx: dtmath_grammarParser.DeltaUnitFirstContext):
        return datetime.timedelta(**{self.visit(ctx.delta_unit()): self.visit(ctx.any_number())})

    def visitDeltaValueFirst(self, ctx: dtmath_grammarParser.DeltaValueFirstContext):
        return datetime.timedelta(**{self.visit(ctx.delta_unit()): self.visit(ctx.any_number())})

    def visitDeltaSecond(self, ctx: dtmath_grammarParser.DeltaSecondContext):
        return 'seconds'

    def visitDeltaMinute(self, ctx: dtmath_grammarParser.DeltaMinuteContext):
        return 'minutes'

    def visitDeltaHour(self, ctx: dtmath_grammarParser.DeltaHourContext):
        return 'hours'

    def visitDeltaDay(self, ctx: dtmath_grammarParser.DeltaDayContext):
        return 'days'

    def visitAbsTimeDay(self, ctx: dtmath_grammarParser.AbsTimeDayContext):
        return self.visit(ctx.day())

    def visitTodayAbsTime(self, ctx: dtmath_grammarParser.TodayAbsTimeContext):
        return self._current_date() + self.visit(ctx.timeofday())

    def visitFullAbsTime(self, ctx: dtmath_grammarParser.FullAbsTimeContext):
        return self.visit(ctx.day()) + self.visit(ctx.timeofday())

    def visitDayOffset(self, ctx: dtmath_grammarParser.DayOffsetContext):
        return self._current_date() + datetime.timedelta(days = int(ctx.getText()[1:]))

    def visitNextWeekday(self, ctx: dtmath_grammarParser.NextWeekdayContext):
        return get_next_weekday(self.visit(ctx.weekday()), self._current_date())

    def visitMonthDay(self, ctx: dtmath_grammarParser.MonthDayContext):
        return self._current_date().replace(day = self.visit(ctx.duo()))

    def visitRecurringDate(self, ctx: dtmath_grammarParser.RecurringDateContext):
        return self._current_date().replace(day = self.visit(ctx.duo()), month = self.visit(ctx.month()))

    def visitDate(self, ctx: dtmath_grammarParser.DateContext):
        return datetime.datetime(
            day = self.visit(ctx.duo()),
            month = self.visit(ctx.month()),
            year = self.visit(ctx.year()),
        )

    def visitNumericalMonth(self, ctx: dtmath_grammarParser.NumericalMonthContext):
        return self.visit(ctx.duo())

    def visitStringMonth(self, ctx: dtmath_grammarParser.StringMonthContext):
        return self.visit(ctx.month_name())

    def visitCentury(self, ctx: dtmath_grammarParser.CenturyContext):
        return 2000 + int(ctx.getText())

    def visitQuadTime(self, ctx: dtmath_grammarParser.QuadTimeContext):
        text = ctx.getText()
        return datetime.timedelta(
            hours = int(text[:2]),
            minutes = int(text[2:]),
        )

    def visitHour(self, ctx: dtmath_grammarParser.HourContext):
        return datetime.timedelta(hours = self.visit(ctx.duo()))

    def visitHourMinute(self, ctx: dtmath_grammarParser.HourMinuteContext):
        return datetime.timedelta(
            hours = self.visit(ctx.duo(0)),
            minutes = self.visit(ctx.duo(1)),
        )

    def visitHourMinuteSecond(self, ctx: dtmath_grammarParser.HourMinuteSecondContext):
        return datetime.timedelta(
            hours = self.visit(ctx.duo(0)),
            minutes = self.visit(ctx.duo(1)),
            seconds = self.visit(ctx.duo(2)),
        )

    def visitDuo(self, ctx: dtmath_grammarParser.DuoContext):
        return int(ctx.getText())

    def visitMonday(self, ctx: dtmath_grammarParser.MondayContext):
        return 0

    def visitTuesday(self, ctx: dtmath_grammarParser.TuesdayContext):
        return 1

    def visitWednesday(self, ctx: dtmath_grammarParser.WednesdayContext):
        return 2

    def visitThursday(self, ctx: dtmath_grammarParser.ThursdayContext):
        return 3

    def visitFriday(self, ctx: dtmath_grammarParser.FridayContext):
        return 4

    def visitSaturday(self, ctx: dtmath_grammarParser.SaturdayContext):
        return 5

    def visitSunday(self, ctx: dtmath_grammarParser.SundayContext):
        return 6

    def visitJanuary(self, ctx: dtmath_grammarParser.JanuaryContext):
        return 1

    def visitMarch(self, ctx: dtmath_grammarParser.MarchContext):
        return 3

    def visitApril(self, ctx: dtmath_grammarParser.AprilContext):
        return 4

    def visitMay(self, ctx: dtmath_grammarParser.MayContext):
        return 5

    def visitJune(self, ctx: dtmath_grammarParser.JuneContext):
        return 6

    def visitJuly(self, ctx: dtmath_grammarParser.JulyContext):
        return 7

    def visitAugust(self, ctx: dtmath_grammarParser.AugustContext):
        return 8

    def visitSeptember(self, ctx: dtmath_grammarParser.SeptemberContext):
        return 9

    def visitOctober(self, ctx: dtmath_grammarParser.OctoberContext):
        return 10

    def visitNovember(self, ctx: dtmath_grammarParser.NovemberContext):
        return 11

    def visitDecember(self, ctx: dtmath_grammarParser.DecemberContext):
        return 12

    def visitAny_number(self, ctx: dtmath_grammarParser.Any_numberContext):
        return int(ctx.getText())

    def visitNowAbsTime(self, ctx: dtmath_grammarParser.NowAbsTimeContext):
        return self._now

    def visitFebruary(self, ctx: dtmath_grammarParser.FebruaryContext):
        return 2

    def visitMillennium(self, ctx: dtmath_grammarParser.MillenniumContext):
        return int(ctx.getText())

    def visitDeltaTimeNow(self, ctx: dtmath_grammarParser.DeltaTimeNowContext):
        return datetime.timedelta(
            hours = self._now.hour,
            minutes = self._now.minute,
            seconds = self._now.second,
        )

    def visitParenthesisOperation(self, ctx: dtmath_grammarParser.ParenthesisOperationContext):
        return self.visit(ctx.operation())

    def visitThisWeekday(self, ctx: dtmath_grammarParser.ThisWeekdayContext):
        return get_weekday(self.visit(ctx.weekday()), self._current_date())

    def visitNextRecurringDate(self, ctx: dtmath_grammarParser.NextRecurringDateContext):
        date = self._current_date().replace(day = self.visit(ctx.duo()), month = self.visit(ctx.month()))
        return date if date > self._now else date.replace(year = date.year + 1)

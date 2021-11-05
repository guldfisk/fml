# Generated from /home/phdk/PycharmProjects/fml/fml/client/dtmath/dtmath_grammar.g4 by ANTLR 4.9.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .dtmath_grammarParser import dtmath_grammarParser
else:
    from dtmath_grammarParser import dtmath_grammarParser

# This class defines a complete generic visitor for a parse tree produced by dtmath_grammarParser.

class dtmath_grammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by dtmath_grammarParser#start.
    def visitStart(self, ctx:dtmath_grammarParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#AdditionOperation.
    def visitAdditionOperation(self, ctx:dtmath_grammarParser.AdditionOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#SubtractionOperation.
    def visitSubtractionOperation(self, ctx:dtmath_grammarParser.SubtractionOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#ParenthesisOperation.
    def visitParenthesisOperation(self, ctx:dtmath_grammarParser.ParenthesisOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#TimeOperation.
    def visitTimeOperation(self, ctx:dtmath_grammarParser.TimeOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#TimeAbs.
    def visitTimeAbs(self, ctx:dtmath_grammarParser.TimeAbsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#TimeDelta.
    def visitTimeDelta(self, ctx:dtmath_grammarParser.TimeDeltaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#DeltaTimeNow.
    def visitDeltaTimeNow(self, ctx:dtmath_grammarParser.DeltaTimeNowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#DeltaTimeSingle.
    def visitDeltaTimeSingle(self, ctx:dtmath_grammarParser.DeltaTimeSingleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#DeltaTimeChain.
    def visitDeltaTimeChain(self, ctx:dtmath_grammarParser.DeltaTimeChainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#DeltaUnitFirst.
    def visitDeltaUnitFirst(self, ctx:dtmath_grammarParser.DeltaUnitFirstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#DeltaValueFirst.
    def visitDeltaValueFirst(self, ctx:dtmath_grammarParser.DeltaValueFirstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#DeltaSecond.
    def visitDeltaSecond(self, ctx:dtmath_grammarParser.DeltaSecondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#DeltaMinute.
    def visitDeltaMinute(self, ctx:dtmath_grammarParser.DeltaMinuteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#DeltaHour.
    def visitDeltaHour(self, ctx:dtmath_grammarParser.DeltaHourContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#DeltaDay.
    def visitDeltaDay(self, ctx:dtmath_grammarParser.DeltaDayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#AbsTimeDay.
    def visitAbsTimeDay(self, ctx:dtmath_grammarParser.AbsTimeDayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#TodayAbsTime.
    def visitTodayAbsTime(self, ctx:dtmath_grammarParser.TodayAbsTimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#FullAbsTime.
    def visitFullAbsTime(self, ctx:dtmath_grammarParser.FullAbsTimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#NowAbsTime.
    def visitNowAbsTime(self, ctx:dtmath_grammarParser.NowAbsTimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#DayOffset.
    def visitDayOffset(self, ctx:dtmath_grammarParser.DayOffsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#ThisWeekday.
    def visitThisWeekday(self, ctx:dtmath_grammarParser.ThisWeekdayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#NextWeekday.
    def visitNextWeekday(self, ctx:dtmath_grammarParser.NextWeekdayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#MonthDay.
    def visitMonthDay(self, ctx:dtmath_grammarParser.MonthDayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#RecurringDate.
    def visitRecurringDate(self, ctx:dtmath_grammarParser.RecurringDateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#NextRecurringDate.
    def visitNextRecurringDate(self, ctx:dtmath_grammarParser.NextRecurringDateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#Date.
    def visitDate(self, ctx:dtmath_grammarParser.DateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#WeekNumberDay.
    def visitWeekNumberDay(self, ctx:dtmath_grammarParser.WeekNumberDayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#NextWeekNumberDay.
    def visitNextWeekNumberDay(self, ctx:dtmath_grammarParser.NextWeekNumberDayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#NumericalMonth.
    def visitNumericalMonth(self, ctx:dtmath_grammarParser.NumericalMonthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#StringMonth.
    def visitStringMonth(self, ctx:dtmath_grammarParser.StringMonthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#Century.
    def visitCentury(self, ctx:dtmath_grammarParser.CenturyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#Millennium.
    def visitMillennium(self, ctx:dtmath_grammarParser.MillenniumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#QuadTime.
    def visitQuadTime(self, ctx:dtmath_grammarParser.QuadTimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#Hour.
    def visitHour(self, ctx:dtmath_grammarParser.HourContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#AmpmHour.
    def visitAmpmHour(self, ctx:dtmath_grammarParser.AmpmHourContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#AmpmHourMinute.
    def visitAmpmHourMinute(self, ctx:dtmath_grammarParser.AmpmHourMinuteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#AmpmHourSecond.
    def visitAmpmHourSecond(self, ctx:dtmath_grammarParser.AmpmHourSecondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#HourMinute.
    def visitHourMinute(self, ctx:dtmath_grammarParser.HourMinuteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#HourMinuteSecond.
    def visitHourMinuteSecond(self, ctx:dtmath_grammarParser.HourMinuteSecondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#ampm.
    def visitAmpm(self, ctx:dtmath_grammarParser.AmpmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#duo.
    def visitDuo(self, ctx:dtmath_grammarParser.DuoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#Monday.
    def visitMonday(self, ctx:dtmath_grammarParser.MondayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#Tuesday.
    def visitTuesday(self, ctx:dtmath_grammarParser.TuesdayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#Wednesday.
    def visitWednesday(self, ctx:dtmath_grammarParser.WednesdayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#Thursday.
    def visitThursday(self, ctx:dtmath_grammarParser.ThursdayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#Friday.
    def visitFriday(self, ctx:dtmath_grammarParser.FridayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#Saturday.
    def visitSaturday(self, ctx:dtmath_grammarParser.SaturdayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#Sunday.
    def visitSunday(self, ctx:dtmath_grammarParser.SundayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#January.
    def visitJanuary(self, ctx:dtmath_grammarParser.JanuaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#February.
    def visitFebruary(self, ctx:dtmath_grammarParser.FebruaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#March.
    def visitMarch(self, ctx:dtmath_grammarParser.MarchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#April.
    def visitApril(self, ctx:dtmath_grammarParser.AprilContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#May.
    def visitMay(self, ctx:dtmath_grammarParser.MayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#June.
    def visitJune(self, ctx:dtmath_grammarParser.JuneContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#July.
    def visitJuly(self, ctx:dtmath_grammarParser.JulyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#August.
    def visitAugust(self, ctx:dtmath_grammarParser.AugustContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#September.
    def visitSeptember(self, ctx:dtmath_grammarParser.SeptemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#October.
    def visitOctober(self, ctx:dtmath_grammarParser.OctoberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#November.
    def visitNovember(self, ctx:dtmath_grammarParser.NovemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#December.
    def visitDecember(self, ctx:dtmath_grammarParser.DecemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dtmath_grammarParser#any_number.
    def visitAny_number(self, ctx:dtmath_grammarParser.Any_numberContext):
        return self.visitChildren(ctx)



del dtmath_grammarParser
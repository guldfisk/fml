# Generated from /home/phdk/PycharmProjects/fml/fml/client/dtmath/dtmath_grammar.g4 by ANTLR 4.9.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .dtmath_grammarParser import dtmath_grammarParser
else:
    from dtmath_grammarParser import dtmath_grammarParser

# This class defines a complete listener for a parse tree produced by dtmath_grammarParser.
class dtmath_grammarListener(ParseTreeListener):

    # Enter a parse tree produced by dtmath_grammarParser#start.
    def enterStart(self, ctx:dtmath_grammarParser.StartContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#start.
    def exitStart(self, ctx:dtmath_grammarParser.StartContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#AdditionOperation.
    def enterAdditionOperation(self, ctx:dtmath_grammarParser.AdditionOperationContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#AdditionOperation.
    def exitAdditionOperation(self, ctx:dtmath_grammarParser.AdditionOperationContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#SubtractionOperation.
    def enterSubtractionOperation(self, ctx:dtmath_grammarParser.SubtractionOperationContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#SubtractionOperation.
    def exitSubtractionOperation(self, ctx:dtmath_grammarParser.SubtractionOperationContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#ParenthesisOperation.
    def enterParenthesisOperation(self, ctx:dtmath_grammarParser.ParenthesisOperationContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#ParenthesisOperation.
    def exitParenthesisOperation(self, ctx:dtmath_grammarParser.ParenthesisOperationContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#TimeOperation.
    def enterTimeOperation(self, ctx:dtmath_grammarParser.TimeOperationContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#TimeOperation.
    def exitTimeOperation(self, ctx:dtmath_grammarParser.TimeOperationContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#TimeAbs.
    def enterTimeAbs(self, ctx:dtmath_grammarParser.TimeAbsContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#TimeAbs.
    def exitTimeAbs(self, ctx:dtmath_grammarParser.TimeAbsContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#TimeDelta.
    def enterTimeDelta(self, ctx:dtmath_grammarParser.TimeDeltaContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#TimeDelta.
    def exitTimeDelta(self, ctx:dtmath_grammarParser.TimeDeltaContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#DeltaTimeNow.
    def enterDeltaTimeNow(self, ctx:dtmath_grammarParser.DeltaTimeNowContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#DeltaTimeNow.
    def exitDeltaTimeNow(self, ctx:dtmath_grammarParser.DeltaTimeNowContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#DeltaTimeSingle.
    def enterDeltaTimeSingle(self, ctx:dtmath_grammarParser.DeltaTimeSingleContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#DeltaTimeSingle.
    def exitDeltaTimeSingle(self, ctx:dtmath_grammarParser.DeltaTimeSingleContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#DeltaTimeChain.
    def enterDeltaTimeChain(self, ctx:dtmath_grammarParser.DeltaTimeChainContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#DeltaTimeChain.
    def exitDeltaTimeChain(self, ctx:dtmath_grammarParser.DeltaTimeChainContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#DeltaUnitFirst.
    def enterDeltaUnitFirst(self, ctx:dtmath_grammarParser.DeltaUnitFirstContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#DeltaUnitFirst.
    def exitDeltaUnitFirst(self, ctx:dtmath_grammarParser.DeltaUnitFirstContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#DeltaValueFirst.
    def enterDeltaValueFirst(self, ctx:dtmath_grammarParser.DeltaValueFirstContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#DeltaValueFirst.
    def exitDeltaValueFirst(self, ctx:dtmath_grammarParser.DeltaValueFirstContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#DeltaSecond.
    def enterDeltaSecond(self, ctx:dtmath_grammarParser.DeltaSecondContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#DeltaSecond.
    def exitDeltaSecond(self, ctx:dtmath_grammarParser.DeltaSecondContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#DeltaMinute.
    def enterDeltaMinute(self, ctx:dtmath_grammarParser.DeltaMinuteContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#DeltaMinute.
    def exitDeltaMinute(self, ctx:dtmath_grammarParser.DeltaMinuteContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#DeltaHour.
    def enterDeltaHour(self, ctx:dtmath_grammarParser.DeltaHourContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#DeltaHour.
    def exitDeltaHour(self, ctx:dtmath_grammarParser.DeltaHourContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#DeltaDay.
    def enterDeltaDay(self, ctx:dtmath_grammarParser.DeltaDayContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#DeltaDay.
    def exitDeltaDay(self, ctx:dtmath_grammarParser.DeltaDayContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#AbsTimeDay.
    def enterAbsTimeDay(self, ctx:dtmath_grammarParser.AbsTimeDayContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#AbsTimeDay.
    def exitAbsTimeDay(self, ctx:dtmath_grammarParser.AbsTimeDayContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#TodayAbsTime.
    def enterTodayAbsTime(self, ctx:dtmath_grammarParser.TodayAbsTimeContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#TodayAbsTime.
    def exitTodayAbsTime(self, ctx:dtmath_grammarParser.TodayAbsTimeContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#FullAbsTime.
    def enterFullAbsTime(self, ctx:dtmath_grammarParser.FullAbsTimeContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#FullAbsTime.
    def exitFullAbsTime(self, ctx:dtmath_grammarParser.FullAbsTimeContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#NowAbsTime.
    def enterNowAbsTime(self, ctx:dtmath_grammarParser.NowAbsTimeContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#NowAbsTime.
    def exitNowAbsTime(self, ctx:dtmath_grammarParser.NowAbsTimeContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#DayOffset.
    def enterDayOffset(self, ctx:dtmath_grammarParser.DayOffsetContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#DayOffset.
    def exitDayOffset(self, ctx:dtmath_grammarParser.DayOffsetContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#ThisWeekday.
    def enterThisWeekday(self, ctx:dtmath_grammarParser.ThisWeekdayContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#ThisWeekday.
    def exitThisWeekday(self, ctx:dtmath_grammarParser.ThisWeekdayContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#NextWeekday.
    def enterNextWeekday(self, ctx:dtmath_grammarParser.NextWeekdayContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#NextWeekday.
    def exitNextWeekday(self, ctx:dtmath_grammarParser.NextWeekdayContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#MonthDay.
    def enterMonthDay(self, ctx:dtmath_grammarParser.MonthDayContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#MonthDay.
    def exitMonthDay(self, ctx:dtmath_grammarParser.MonthDayContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#RecurringDate.
    def enterRecurringDate(self, ctx:dtmath_grammarParser.RecurringDateContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#RecurringDate.
    def exitRecurringDate(self, ctx:dtmath_grammarParser.RecurringDateContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#NextRecurringDate.
    def enterNextRecurringDate(self, ctx:dtmath_grammarParser.NextRecurringDateContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#NextRecurringDate.
    def exitNextRecurringDate(self, ctx:dtmath_grammarParser.NextRecurringDateContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#Date.
    def enterDate(self, ctx:dtmath_grammarParser.DateContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#Date.
    def exitDate(self, ctx:dtmath_grammarParser.DateContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#WeekNumberDay.
    def enterWeekNumberDay(self, ctx:dtmath_grammarParser.WeekNumberDayContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#WeekNumberDay.
    def exitWeekNumberDay(self, ctx:dtmath_grammarParser.WeekNumberDayContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#NextWeekNumberDay.
    def enterNextWeekNumberDay(self, ctx:dtmath_grammarParser.NextWeekNumberDayContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#NextWeekNumberDay.
    def exitNextWeekNumberDay(self, ctx:dtmath_grammarParser.NextWeekNumberDayContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#NumericalMonth.
    def enterNumericalMonth(self, ctx:dtmath_grammarParser.NumericalMonthContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#NumericalMonth.
    def exitNumericalMonth(self, ctx:dtmath_grammarParser.NumericalMonthContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#StringMonth.
    def enterStringMonth(self, ctx:dtmath_grammarParser.StringMonthContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#StringMonth.
    def exitStringMonth(self, ctx:dtmath_grammarParser.StringMonthContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#Century.
    def enterCentury(self, ctx:dtmath_grammarParser.CenturyContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#Century.
    def exitCentury(self, ctx:dtmath_grammarParser.CenturyContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#Millennium.
    def enterMillennium(self, ctx:dtmath_grammarParser.MillenniumContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#Millennium.
    def exitMillennium(self, ctx:dtmath_grammarParser.MillenniumContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#QuadTime.
    def enterQuadTime(self, ctx:dtmath_grammarParser.QuadTimeContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#QuadTime.
    def exitQuadTime(self, ctx:dtmath_grammarParser.QuadTimeContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#Hour.
    def enterHour(self, ctx:dtmath_grammarParser.HourContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#Hour.
    def exitHour(self, ctx:dtmath_grammarParser.HourContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#AmpmHour.
    def enterAmpmHour(self, ctx:dtmath_grammarParser.AmpmHourContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#AmpmHour.
    def exitAmpmHour(self, ctx:dtmath_grammarParser.AmpmHourContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#AmpmHourMinute.
    def enterAmpmHourMinute(self, ctx:dtmath_grammarParser.AmpmHourMinuteContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#AmpmHourMinute.
    def exitAmpmHourMinute(self, ctx:dtmath_grammarParser.AmpmHourMinuteContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#AmpmHourSecond.
    def enterAmpmHourSecond(self, ctx:dtmath_grammarParser.AmpmHourSecondContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#AmpmHourSecond.
    def exitAmpmHourSecond(self, ctx:dtmath_grammarParser.AmpmHourSecondContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#HourMinute.
    def enterHourMinute(self, ctx:dtmath_grammarParser.HourMinuteContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#HourMinute.
    def exitHourMinute(self, ctx:dtmath_grammarParser.HourMinuteContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#HourMinuteSecond.
    def enterHourMinuteSecond(self, ctx:dtmath_grammarParser.HourMinuteSecondContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#HourMinuteSecond.
    def exitHourMinuteSecond(self, ctx:dtmath_grammarParser.HourMinuteSecondContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#ampm.
    def enterAmpm(self, ctx:dtmath_grammarParser.AmpmContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#ampm.
    def exitAmpm(self, ctx:dtmath_grammarParser.AmpmContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#duo.
    def enterDuo(self, ctx:dtmath_grammarParser.DuoContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#duo.
    def exitDuo(self, ctx:dtmath_grammarParser.DuoContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#Monday.
    def enterMonday(self, ctx:dtmath_grammarParser.MondayContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#Monday.
    def exitMonday(self, ctx:dtmath_grammarParser.MondayContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#Tuesday.
    def enterTuesday(self, ctx:dtmath_grammarParser.TuesdayContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#Tuesday.
    def exitTuesday(self, ctx:dtmath_grammarParser.TuesdayContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#Wednesday.
    def enterWednesday(self, ctx:dtmath_grammarParser.WednesdayContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#Wednesday.
    def exitWednesday(self, ctx:dtmath_grammarParser.WednesdayContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#Thursday.
    def enterThursday(self, ctx:dtmath_grammarParser.ThursdayContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#Thursday.
    def exitThursday(self, ctx:dtmath_grammarParser.ThursdayContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#Friday.
    def enterFriday(self, ctx:dtmath_grammarParser.FridayContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#Friday.
    def exitFriday(self, ctx:dtmath_grammarParser.FridayContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#Saturday.
    def enterSaturday(self, ctx:dtmath_grammarParser.SaturdayContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#Saturday.
    def exitSaturday(self, ctx:dtmath_grammarParser.SaturdayContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#Sunday.
    def enterSunday(self, ctx:dtmath_grammarParser.SundayContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#Sunday.
    def exitSunday(self, ctx:dtmath_grammarParser.SundayContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#January.
    def enterJanuary(self, ctx:dtmath_grammarParser.JanuaryContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#January.
    def exitJanuary(self, ctx:dtmath_grammarParser.JanuaryContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#February.
    def enterFebruary(self, ctx:dtmath_grammarParser.FebruaryContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#February.
    def exitFebruary(self, ctx:dtmath_grammarParser.FebruaryContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#March.
    def enterMarch(self, ctx:dtmath_grammarParser.MarchContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#March.
    def exitMarch(self, ctx:dtmath_grammarParser.MarchContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#April.
    def enterApril(self, ctx:dtmath_grammarParser.AprilContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#April.
    def exitApril(self, ctx:dtmath_grammarParser.AprilContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#May.
    def enterMay(self, ctx:dtmath_grammarParser.MayContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#May.
    def exitMay(self, ctx:dtmath_grammarParser.MayContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#June.
    def enterJune(self, ctx:dtmath_grammarParser.JuneContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#June.
    def exitJune(self, ctx:dtmath_grammarParser.JuneContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#July.
    def enterJuly(self, ctx:dtmath_grammarParser.JulyContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#July.
    def exitJuly(self, ctx:dtmath_grammarParser.JulyContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#August.
    def enterAugust(self, ctx:dtmath_grammarParser.AugustContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#August.
    def exitAugust(self, ctx:dtmath_grammarParser.AugustContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#September.
    def enterSeptember(self, ctx:dtmath_grammarParser.SeptemberContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#September.
    def exitSeptember(self, ctx:dtmath_grammarParser.SeptemberContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#October.
    def enterOctober(self, ctx:dtmath_grammarParser.OctoberContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#October.
    def exitOctober(self, ctx:dtmath_grammarParser.OctoberContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#November.
    def enterNovember(self, ctx:dtmath_grammarParser.NovemberContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#November.
    def exitNovember(self, ctx:dtmath_grammarParser.NovemberContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#December.
    def enterDecember(self, ctx:dtmath_grammarParser.DecemberContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#December.
    def exitDecember(self, ctx:dtmath_grammarParser.DecemberContext):
        pass


    # Enter a parse tree produced by dtmath_grammarParser#any_number.
    def enterAny_number(self, ctx:dtmath_grammarParser.Any_numberContext):
        pass

    # Exit a parse tree produced by dtmath_grammarParser#any_number.
    def exitAny_number(self, ctx:dtmath_grammarParser.Any_numberContext):
        pass



del dtmath_grammarParser
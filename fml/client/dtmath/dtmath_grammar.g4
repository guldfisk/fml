grammar dtmath_grammar;


start :
    operation EOF
;

operation :
    time #TimeOperation
    | '(' operation ')' #ParenthesisOperation
    | operation '-' operation #SubtractionOperation
    | operation '+' operation #AdditionOperation
;

time :
    abs_time #TimeAbs
    | delta_time #TimeDelta
;

delta_time :
    delta_time_unit #DeltaTimeSingle
    | NOW_TIME #DeltaTimeNow
    | delta_time delta_time_unit #DeltaTimeChain
;

delta_time_unit :
    delta_unit any_number #DeltaUnitFirst
    | any_number delta_unit #DeltaValueFirst
;

delta_unit :
    SECOND #DeltaSecond
    | MINUTE #DeltaMinute
    | HOUR #DeltaHour
    | DAY #DeltaDay
;

abs_time :
    day #AbsTimeDay
    | timeofday #TodayAbsTime
    | day DIVIDER timeofday #FullAbsTime
    | NOW #NowAbsTime
;

day :
    '.' any_number #DayOffset
    | weekday #ThisWeekday
    | '.' weekday #NextWeekday
    | duo '/' #MonthDay
    | duo '/' month #RecurringDate
    | '.' duo '/' month #NextRecurringDate
    | duo '/' month '/' year #Date
;

month :
    duo #NumericalMonth
    | month_name #StringMonth
;

year :
    duo #Century
    | QUAD #Millennium
;

timeofday :
    QUAD #QuadTime
    | duo #Hour
    | duo ':' duo #HourMinute
    | duo ':' duo ':' duo #HourMinuteSecond
;

duo : PAIR | SINGLE;

weekday :
    'mon' #Monday
    | 'man' #Monday
    | 'monday' #Monday
    | 'mandag' #Monday
    | 'tue' #Tuesday
    | 'tir' #Tuesday
    | 'tuesday' #Tuesday
    | 'tirsdag' #Tuesday
    | 'wed' #Wednesday
    | 'ons' #Wednesday
    | 'wednesday' #Wednesday
    | 'onsdag' #Wednesday
    | 'thu' #Thursday
    | 'tor' #Thursday
    | 'thursday' #Thursday
    | 'torsdag' #Thursday
    | 'fri' #Friday
    | 'fre' #Friday
    | 'friday' #Friday
    | 'fredag' #Friday
    | 'sat' #Saturday
    | 'lør' #Saturday
    | 'saturday' #Saturday
    | 'lørdag' #Saturday
    | 'sun' #Sunday
    | 'søn' #Sunday
    | 'sunday' #Sunday
    | 'søndag' #Sunday
;

month_name :
    'jan' #January
    | 'january' #January
    | 'januar' #January
    | 'feb' #February
    | 'february' #February
    | 'februar' #February
    | 'mar' #March
    | 'march' #March
    | 'marts' #March
    | 'apr' #April
    | 'april' #April
    | 'may' #May
    | 'maj' #May
    | 'jun' #June
    | 'june' #June
    | 'juni' #June
    | 'jul' #July
    | 'july' #July
    | 'juli' #July
    | 'aug' #August
    | 'august' #August
    | 'sep' #September
    | 'september' #September
    | 'oct' #October
    | 'okt' #October
    | 'october' #October
    | 'oktober' #October
    | 'nov' #November
    | 'november' #November
    | 'dec' #December
    | 'december' #December
;

any_number : SINGLE | PAIR | QUAD | BIGNUMBER;


QUAD: [0-9][0-9][0-9][0-9];
PAIR: [0-9][0-9];
SINGLE: [0-9];
BIGNUMBER: [0-9]+;

NOW: [nN];

NOW_TIME: 'nt';
DIVIDER: [_|];
SECOND: [sS];
MINUTE: [mM];
HOUR: [hH];
DAY: [dD];

WHITESPACE : [ \n\t\r] -> skip;
ERRORCHARACTER : . ;

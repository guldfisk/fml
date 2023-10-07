# Generated from /home/phdk/PycharmProjects/fml/fml/client/dtmath/dtmath_grammar.g4 by ANTLR 4.12.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,82,236,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,3,1,42,8,
        1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,50,8,1,10,1,12,1,53,9,1,1,2,1,2,3,
        2,57,8,2,1,3,1,3,1,3,3,3,62,8,3,1,3,1,3,5,3,66,8,3,10,3,12,3,69,
        9,3,1,4,1,4,1,4,1,4,1,4,1,4,3,4,77,8,4,1,5,1,5,1,5,1,5,3,5,83,8,
        5,1,6,1,6,1,6,1,6,1,6,1,6,1,6,3,6,92,8,6,1,7,1,7,1,7,1,7,1,7,1,7,
        1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,
        1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,3,7,128,8,7,1,8,
        1,8,3,8,132,8,8,1,9,1,9,3,9,136,8,9,1,10,1,10,1,10,1,10,1,10,1,10,
        1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,
        1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,3,10,165,8,10,1,11,1,11,
        1,12,1,12,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,
        1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,
        1,13,1,13,1,13,1,13,3,13,199,8,13,1,14,1,14,1,14,1,14,1,14,1,14,
        1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,
        1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,3,14,
        232,8,14,1,15,1,15,1,15,0,2,2,6,16,0,2,4,6,8,10,12,14,16,18,20,22,
        24,26,28,30,0,3,1,0,9,10,1,0,71,72,1,0,70,73,305,0,32,1,0,0,0,2,
        41,1,0,0,0,4,56,1,0,0,0,6,61,1,0,0,0,8,76,1,0,0,0,10,82,1,0,0,0,
        12,91,1,0,0,0,14,127,1,0,0,0,16,131,1,0,0,0,18,135,1,0,0,0,20,164,
        1,0,0,0,22,166,1,0,0,0,24,168,1,0,0,0,26,198,1,0,0,0,28,231,1,0,
        0,0,30,233,1,0,0,0,32,33,3,2,1,0,33,34,5,0,0,1,34,1,1,0,0,0,35,36,
        6,1,-1,0,36,42,3,4,2,0,37,38,5,1,0,0,38,39,3,2,1,0,39,40,5,2,0,0,
        40,42,1,0,0,0,41,35,1,0,0,0,41,37,1,0,0,0,42,51,1,0,0,0,43,44,10,
        2,0,0,44,45,5,3,0,0,45,50,3,2,1,3,46,47,10,1,0,0,47,48,5,4,0,0,48,
        50,3,2,1,2,49,43,1,0,0,0,49,46,1,0,0,0,50,53,1,0,0,0,51,49,1,0,0,
        0,51,52,1,0,0,0,52,3,1,0,0,0,53,51,1,0,0,0,54,57,3,12,6,0,55,57,
        3,6,3,0,56,54,1,0,0,0,56,55,1,0,0,0,57,5,1,0,0,0,58,59,6,3,-1,0,
        59,62,3,8,4,0,60,62,5,75,0,0,61,58,1,0,0,0,61,60,1,0,0,0,62,67,1,
        0,0,0,63,64,10,1,0,0,64,66,3,8,4,0,65,63,1,0,0,0,66,69,1,0,0,0,67,
        65,1,0,0,0,67,68,1,0,0,0,68,7,1,0,0,0,69,67,1,0,0,0,70,71,3,10,5,
        0,71,72,3,30,15,0,72,77,1,0,0,0,73,74,3,30,15,0,74,75,3,10,5,0,75,
        77,1,0,0,0,76,70,1,0,0,0,76,73,1,0,0,0,77,9,1,0,0,0,78,83,5,77,0,
        0,79,83,5,78,0,0,80,83,5,79,0,0,81,83,5,80,0,0,82,78,1,0,0,0,82,
        79,1,0,0,0,82,80,1,0,0,0,82,81,1,0,0,0,83,11,1,0,0,0,84,92,3,14,
        7,0,85,92,3,20,10,0,86,87,3,14,7,0,87,88,5,76,0,0,88,89,3,20,10,
        0,89,92,1,0,0,0,90,92,5,74,0,0,91,84,1,0,0,0,91,85,1,0,0,0,91,86,
        1,0,0,0,91,90,1,0,0,0,92,13,1,0,0,0,93,94,5,5,0,0,94,128,3,30,15,
        0,95,128,3,26,13,0,96,97,5,5,0,0,97,128,3,26,13,0,98,99,3,24,12,
        0,99,100,5,6,0,0,100,128,1,0,0,0,101,102,3,24,12,0,102,103,5,6,0,
        0,103,104,3,16,8,0,104,128,1,0,0,0,105,106,5,5,0,0,106,107,3,24,
        12,0,107,108,5,6,0,0,108,109,3,16,8,0,109,128,1,0,0,0,110,111,3,
        24,12,0,111,112,5,6,0,0,112,113,3,16,8,0,113,114,5,6,0,0,114,115,
        3,18,9,0,115,128,1,0,0,0,116,117,5,7,0,0,117,118,3,30,15,0,118,119,
        5,6,0,0,119,120,3,26,13,0,120,128,1,0,0,0,121,122,5,5,0,0,122,123,
        5,7,0,0,123,124,3,30,15,0,124,125,5,6,0,0,125,126,3,26,13,0,126,
        128,1,0,0,0,127,93,1,0,0,0,127,95,1,0,0,0,127,96,1,0,0,0,127,98,
        1,0,0,0,127,101,1,0,0,0,127,105,1,0,0,0,127,110,1,0,0,0,127,116,
        1,0,0,0,127,121,1,0,0,0,128,15,1,0,0,0,129,132,3,24,12,0,130,132,
        3,28,14,0,131,129,1,0,0,0,131,130,1,0,0,0,132,17,1,0,0,0,133,136,
        3,24,12,0,134,136,5,70,0,0,135,133,1,0,0,0,135,134,1,0,0,0,136,19,
        1,0,0,0,137,165,5,70,0,0,138,165,3,24,12,0,139,140,3,24,12,0,140,
        141,3,22,11,0,141,165,1,0,0,0,142,143,3,24,12,0,143,144,5,8,0,0,
        144,145,3,24,12,0,145,146,3,22,11,0,146,165,1,0,0,0,147,148,3,24,
        12,0,148,149,5,8,0,0,149,150,3,24,12,0,150,151,5,8,0,0,151,152,3,
        24,12,0,152,153,3,22,11,0,153,165,1,0,0,0,154,155,3,24,12,0,155,
        156,5,8,0,0,156,157,3,24,12,0,157,165,1,0,0,0,158,159,3,24,12,0,
        159,160,5,8,0,0,160,161,3,24,12,0,161,162,5,8,0,0,162,163,3,24,12,
        0,163,165,1,0,0,0,164,137,1,0,0,0,164,138,1,0,0,0,164,139,1,0,0,
        0,164,142,1,0,0,0,164,147,1,0,0,0,164,154,1,0,0,0,164,158,1,0,0,
        0,165,21,1,0,0,0,166,167,7,0,0,0,167,23,1,0,0,0,168,169,7,1,0,0,
        169,25,1,0,0,0,170,199,5,11,0,0,171,199,5,12,0,0,172,199,5,13,0,
        0,173,199,5,14,0,0,174,199,5,15,0,0,175,199,5,16,0,0,176,199,5,17,
        0,0,177,199,5,18,0,0,178,199,5,19,0,0,179,199,5,20,0,0,180,199,5,
        21,0,0,181,199,5,22,0,0,182,199,5,23,0,0,183,199,5,24,0,0,184,199,
        5,25,0,0,185,199,5,26,0,0,186,199,5,27,0,0,187,199,5,28,0,0,188,
        199,5,29,0,0,189,199,5,30,0,0,190,199,5,31,0,0,191,199,5,32,0,0,
        192,199,5,33,0,0,193,199,5,34,0,0,194,199,5,35,0,0,195,199,5,36,
        0,0,196,199,5,37,0,0,197,199,5,38,0,0,198,170,1,0,0,0,198,171,1,
        0,0,0,198,172,1,0,0,0,198,173,1,0,0,0,198,174,1,0,0,0,198,175,1,
        0,0,0,198,176,1,0,0,0,198,177,1,0,0,0,198,178,1,0,0,0,198,179,1,
        0,0,0,198,180,1,0,0,0,198,181,1,0,0,0,198,182,1,0,0,0,198,183,1,
        0,0,0,198,184,1,0,0,0,198,185,1,0,0,0,198,186,1,0,0,0,198,187,1,
        0,0,0,198,188,1,0,0,0,198,189,1,0,0,0,198,190,1,0,0,0,198,191,1,
        0,0,0,198,192,1,0,0,0,198,193,1,0,0,0,198,194,1,0,0,0,198,195,1,
        0,0,0,198,196,1,0,0,0,198,197,1,0,0,0,199,27,1,0,0,0,200,232,5,39,
        0,0,201,232,5,40,0,0,202,232,5,41,0,0,203,232,5,42,0,0,204,232,5,
        43,0,0,205,232,5,44,0,0,206,232,5,45,0,0,207,232,5,46,0,0,208,232,
        5,47,0,0,209,232,5,48,0,0,210,232,5,49,0,0,211,232,5,50,0,0,212,
        232,5,51,0,0,213,232,5,52,0,0,214,232,5,53,0,0,215,232,5,54,0,0,
        216,232,5,55,0,0,217,232,5,56,0,0,218,232,5,57,0,0,219,232,5,58,
        0,0,220,232,5,59,0,0,221,232,5,60,0,0,222,232,5,61,0,0,223,232,5,
        62,0,0,224,232,5,63,0,0,225,232,5,64,0,0,226,232,5,65,0,0,227,232,
        5,66,0,0,228,232,5,67,0,0,229,232,5,68,0,0,230,232,5,69,0,0,231,
        200,1,0,0,0,231,201,1,0,0,0,231,202,1,0,0,0,231,203,1,0,0,0,231,
        204,1,0,0,0,231,205,1,0,0,0,231,206,1,0,0,0,231,207,1,0,0,0,231,
        208,1,0,0,0,231,209,1,0,0,0,231,210,1,0,0,0,231,211,1,0,0,0,231,
        212,1,0,0,0,231,213,1,0,0,0,231,214,1,0,0,0,231,215,1,0,0,0,231,
        216,1,0,0,0,231,217,1,0,0,0,231,218,1,0,0,0,231,219,1,0,0,0,231,
        220,1,0,0,0,231,221,1,0,0,0,231,222,1,0,0,0,231,223,1,0,0,0,231,
        224,1,0,0,0,231,225,1,0,0,0,231,226,1,0,0,0,231,227,1,0,0,0,231,
        228,1,0,0,0,231,229,1,0,0,0,231,230,1,0,0,0,232,29,1,0,0,0,233,234,
        7,2,0,0,234,31,1,0,0,0,15,41,49,51,56,61,67,76,82,91,127,131,135,
        164,198,231
    ]

class dtmath_grammarParser ( Parser ):

    grammarFileName = "dtmath_grammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'-'", "'+'", "'.'", "'/'", 
                     "'w'", "':'", "'am'", "'pm'", "'mon'", "'man'", "'monday'", 
                     "'mandag'", "'tue'", "'tir'", "'tuesday'", "'tirsdag'", 
                     "'wed'", "'ons'", "'wednesday'", "'onsdag'", "'thu'", 
                     "'tor'", "'thursday'", "'torsdag'", "'fri'", "'fre'", 
                     "'friday'", "'fredag'", "'sat'", "'l\\u00F8r'", "'saturday'", 
                     "'l\\u00F8rdag'", "'sun'", "'s\\u00F8n'", "'sunday'", 
                     "'s\\u00F8ndag'", "'jan'", "'january'", "'januar'", 
                     "'feb'", "'february'", "'februar'", "'mar'", "'march'", 
                     "'marts'", "'apr'", "'april'", "'may'", "'maj'", "'jun'", 
                     "'june'", "'juni'", "'jul'", "'july'", "'juli'", "'aug'", 
                     "'august'", "'sep'", "'september'", "'oct'", "'okt'", 
                     "'october'", "'oktober'", "'nov'", "'november'", "'dec'", 
                     "'december'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'nt'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "QUAD", "PAIR", "SINGLE", 
                      "BIGNUMBER", "NOW", "NOW_TIME", "DIVIDER", "SECOND", 
                      "MINUTE", "HOUR", "DAY", "WHITESPACE", "ERRORCHARACTER" ]

    RULE_start = 0
    RULE_operation = 1
    RULE_time = 2
    RULE_delta_time = 3
    RULE_delta_time_unit = 4
    RULE_delta_unit = 5
    RULE_abs_time = 6
    RULE_day = 7
    RULE_month = 8
    RULE_year = 9
    RULE_timeofday = 10
    RULE_ampm = 11
    RULE_duo = 12
    RULE_weekday = 13
    RULE_month_name = 14
    RULE_any_number = 15

    ruleNames =  [ "start", "operation", "time", "delta_time", "delta_time_unit", 
                   "delta_unit", "abs_time", "day", "month", "year", "timeofday", 
                   "ampm", "duo", "weekday", "month_name", "any_number" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    T__24=25
    T__25=26
    T__26=27
    T__27=28
    T__28=29
    T__29=30
    T__30=31
    T__31=32
    T__32=33
    T__33=34
    T__34=35
    T__35=36
    T__36=37
    T__37=38
    T__38=39
    T__39=40
    T__40=41
    T__41=42
    T__42=43
    T__43=44
    T__44=45
    T__45=46
    T__46=47
    T__47=48
    T__48=49
    T__49=50
    T__50=51
    T__51=52
    T__52=53
    T__53=54
    T__54=55
    T__55=56
    T__56=57
    T__57=58
    T__58=59
    T__59=60
    T__60=61
    T__61=62
    T__62=63
    T__63=64
    T__64=65
    T__65=66
    T__66=67
    T__67=68
    T__68=69
    QUAD=70
    PAIR=71
    SINGLE=72
    BIGNUMBER=73
    NOW=74
    NOW_TIME=75
    DIVIDER=76
    SECOND=77
    MINUTE=78
    HOUR=79
    DAY=80
    WHITESPACE=81
    ERRORCHARACTER=82

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.12.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def operation(self):
            return self.getTypedRuleContext(dtmath_grammarParser.OperationContext,0)


        def EOF(self):
            return self.getToken(dtmath_grammarParser.EOF, 0)

        def getRuleIndex(self):
            return dtmath_grammarParser.RULE_start

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart" ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart" ):
                listener.exitStart(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStart" ):
                return visitor.visitStart(self)
            else:
                return visitor.visitChildren(self)




    def start(self):

        localctx = dtmath_grammarParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 32
            self.operation(0)
            self.state = 33
            self.match(dtmath_grammarParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OperationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return dtmath_grammarParser.RULE_operation

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class AdditionOperationContext(OperationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.OperationContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def operation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dtmath_grammarParser.OperationContext)
            else:
                return self.getTypedRuleContext(dtmath_grammarParser.OperationContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdditionOperation" ):
                listener.enterAdditionOperation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdditionOperation" ):
                listener.exitAdditionOperation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdditionOperation" ):
                return visitor.visitAdditionOperation(self)
            else:
                return visitor.visitChildren(self)


    class SubtractionOperationContext(OperationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.OperationContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def operation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dtmath_grammarParser.OperationContext)
            else:
                return self.getTypedRuleContext(dtmath_grammarParser.OperationContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSubtractionOperation" ):
                listener.enterSubtractionOperation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSubtractionOperation" ):
                listener.exitSubtractionOperation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSubtractionOperation" ):
                return visitor.visitSubtractionOperation(self)
            else:
                return visitor.visitChildren(self)


    class ParenthesisOperationContext(OperationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.OperationContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def operation(self):
            return self.getTypedRuleContext(dtmath_grammarParser.OperationContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenthesisOperation" ):
                listener.enterParenthesisOperation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenthesisOperation" ):
                listener.exitParenthesisOperation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenthesisOperation" ):
                return visitor.visitParenthesisOperation(self)
            else:
                return visitor.visitChildren(self)


    class TimeOperationContext(OperationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.OperationContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def time(self):
            return self.getTypedRuleContext(dtmath_grammarParser.TimeContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTimeOperation" ):
                listener.enterTimeOperation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTimeOperation" ):
                listener.exitTimeOperation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTimeOperation" ):
                return visitor.visitTimeOperation(self)
            else:
                return visitor.visitChildren(self)



    def operation(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = dtmath_grammarParser.OperationContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_operation, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 70, 71, 72, 73, 74, 75, 77, 78, 79, 80]:
                localctx = dtmath_grammarParser.TimeOperationContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 36
                self.time()
                pass
            elif token in [1]:
                localctx = dtmath_grammarParser.ParenthesisOperationContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 37
                self.match(dtmath_grammarParser.T__0)
                self.state = 38
                self.operation(0)
                self.state = 39
                self.match(dtmath_grammarParser.T__1)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 51
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 49
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = dtmath_grammarParser.SubtractionOperationContext(self, dtmath_grammarParser.OperationContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_operation)
                        self.state = 43
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 44
                        self.match(dtmath_grammarParser.T__2)
                        self.state = 45
                        self.operation(3)
                        pass

                    elif la_ == 2:
                        localctx = dtmath_grammarParser.AdditionOperationContext(self, dtmath_grammarParser.OperationContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_operation)
                        self.state = 46
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 47
                        self.match(dtmath_grammarParser.T__3)
                        self.state = 48
                        self.operation(2)
                        pass

             
                self.state = 53
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class TimeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return dtmath_grammarParser.RULE_time

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class TimeAbsContext(TimeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.TimeContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def abs_time(self):
            return self.getTypedRuleContext(dtmath_grammarParser.Abs_timeContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTimeAbs" ):
                listener.enterTimeAbs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTimeAbs" ):
                listener.exitTimeAbs(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTimeAbs" ):
                return visitor.visitTimeAbs(self)
            else:
                return visitor.visitChildren(self)


    class TimeDeltaContext(TimeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.TimeContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def delta_time(self):
            return self.getTypedRuleContext(dtmath_grammarParser.Delta_timeContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTimeDelta" ):
                listener.enterTimeDelta(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTimeDelta" ):
                listener.exitTimeDelta(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTimeDelta" ):
                return visitor.visitTimeDelta(self)
            else:
                return visitor.visitChildren(self)



    def time(self):

        localctx = dtmath_grammarParser.TimeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_time)
        try:
            self.state = 56
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                localctx = dtmath_grammarParser.TimeAbsContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 54
                self.abs_time()
                pass

            elif la_ == 2:
                localctx = dtmath_grammarParser.TimeDeltaContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 55
                self.delta_time(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Delta_timeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return dtmath_grammarParser.RULE_delta_time

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class DeltaTimeNowContext(Delta_timeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Delta_timeContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NOW_TIME(self):
            return self.getToken(dtmath_grammarParser.NOW_TIME, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeltaTimeNow" ):
                listener.enterDeltaTimeNow(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeltaTimeNow" ):
                listener.exitDeltaTimeNow(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeltaTimeNow" ):
                return visitor.visitDeltaTimeNow(self)
            else:
                return visitor.visitChildren(self)


    class DeltaTimeSingleContext(Delta_timeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Delta_timeContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def delta_time_unit(self):
            return self.getTypedRuleContext(dtmath_grammarParser.Delta_time_unitContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeltaTimeSingle" ):
                listener.enterDeltaTimeSingle(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeltaTimeSingle" ):
                listener.exitDeltaTimeSingle(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeltaTimeSingle" ):
                return visitor.visitDeltaTimeSingle(self)
            else:
                return visitor.visitChildren(self)


    class DeltaTimeChainContext(Delta_timeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Delta_timeContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def delta_time(self):
            return self.getTypedRuleContext(dtmath_grammarParser.Delta_timeContext,0)

        def delta_time_unit(self):
            return self.getTypedRuleContext(dtmath_grammarParser.Delta_time_unitContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeltaTimeChain" ):
                listener.enterDeltaTimeChain(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeltaTimeChain" ):
                listener.exitDeltaTimeChain(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeltaTimeChain" ):
                return visitor.visitDeltaTimeChain(self)
            else:
                return visitor.visitChildren(self)



    def delta_time(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = dtmath_grammarParser.Delta_timeContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 6
        self.enterRecursionRule(localctx, 6, self.RULE_delta_time, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [70, 71, 72, 73, 77, 78, 79, 80]:
                localctx = dtmath_grammarParser.DeltaTimeSingleContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 59
                self.delta_time_unit()
                pass
            elif token in [75]:
                localctx = dtmath_grammarParser.DeltaTimeNowContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 60
                self.match(dtmath_grammarParser.NOW_TIME)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 67
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = dtmath_grammarParser.DeltaTimeChainContext(self, dtmath_grammarParser.Delta_timeContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_delta_time)
                    self.state = 63
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 64
                    self.delta_time_unit() 
                self.state = 69
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class Delta_time_unitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return dtmath_grammarParser.RULE_delta_time_unit

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class DeltaValueFirstContext(Delta_time_unitContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Delta_time_unitContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def any_number(self):
            return self.getTypedRuleContext(dtmath_grammarParser.Any_numberContext,0)

        def delta_unit(self):
            return self.getTypedRuleContext(dtmath_grammarParser.Delta_unitContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeltaValueFirst" ):
                listener.enterDeltaValueFirst(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeltaValueFirst" ):
                listener.exitDeltaValueFirst(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeltaValueFirst" ):
                return visitor.visitDeltaValueFirst(self)
            else:
                return visitor.visitChildren(self)


    class DeltaUnitFirstContext(Delta_time_unitContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Delta_time_unitContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def delta_unit(self):
            return self.getTypedRuleContext(dtmath_grammarParser.Delta_unitContext,0)

        def any_number(self):
            return self.getTypedRuleContext(dtmath_grammarParser.Any_numberContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeltaUnitFirst" ):
                listener.enterDeltaUnitFirst(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeltaUnitFirst" ):
                listener.exitDeltaUnitFirst(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeltaUnitFirst" ):
                return visitor.visitDeltaUnitFirst(self)
            else:
                return visitor.visitChildren(self)



    def delta_time_unit(self):

        localctx = dtmath_grammarParser.Delta_time_unitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_delta_time_unit)
        try:
            self.state = 76
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [77, 78, 79, 80]:
                localctx = dtmath_grammarParser.DeltaUnitFirstContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 70
                self.delta_unit()
                self.state = 71
                self.any_number()
                pass
            elif token in [70, 71, 72, 73]:
                localctx = dtmath_grammarParser.DeltaValueFirstContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 73
                self.any_number()
                self.state = 74
                self.delta_unit()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Delta_unitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return dtmath_grammarParser.RULE_delta_unit

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class DeltaSecondContext(Delta_unitContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Delta_unitContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def SECOND(self):
            return self.getToken(dtmath_grammarParser.SECOND, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeltaSecond" ):
                listener.enterDeltaSecond(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeltaSecond" ):
                listener.exitDeltaSecond(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeltaSecond" ):
                return visitor.visitDeltaSecond(self)
            else:
                return visitor.visitChildren(self)


    class DeltaMinuteContext(Delta_unitContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Delta_unitContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def MINUTE(self):
            return self.getToken(dtmath_grammarParser.MINUTE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeltaMinute" ):
                listener.enterDeltaMinute(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeltaMinute" ):
                listener.exitDeltaMinute(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeltaMinute" ):
                return visitor.visitDeltaMinute(self)
            else:
                return visitor.visitChildren(self)


    class DeltaDayContext(Delta_unitContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Delta_unitContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DAY(self):
            return self.getToken(dtmath_grammarParser.DAY, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeltaDay" ):
                listener.enterDeltaDay(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeltaDay" ):
                listener.exitDeltaDay(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeltaDay" ):
                return visitor.visitDeltaDay(self)
            else:
                return visitor.visitChildren(self)


    class DeltaHourContext(Delta_unitContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Delta_unitContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def HOUR(self):
            return self.getToken(dtmath_grammarParser.HOUR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeltaHour" ):
                listener.enterDeltaHour(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeltaHour" ):
                listener.exitDeltaHour(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeltaHour" ):
                return visitor.visitDeltaHour(self)
            else:
                return visitor.visitChildren(self)



    def delta_unit(self):

        localctx = dtmath_grammarParser.Delta_unitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_delta_unit)
        try:
            self.state = 82
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [77]:
                localctx = dtmath_grammarParser.DeltaSecondContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 78
                self.match(dtmath_grammarParser.SECOND)
                pass
            elif token in [78]:
                localctx = dtmath_grammarParser.DeltaMinuteContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 79
                self.match(dtmath_grammarParser.MINUTE)
                pass
            elif token in [79]:
                localctx = dtmath_grammarParser.DeltaHourContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 80
                self.match(dtmath_grammarParser.HOUR)
                pass
            elif token in [80]:
                localctx = dtmath_grammarParser.DeltaDayContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 81
                self.match(dtmath_grammarParser.DAY)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Abs_timeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return dtmath_grammarParser.RULE_abs_time

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class TodayAbsTimeContext(Abs_timeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Abs_timeContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def timeofday(self):
            return self.getTypedRuleContext(dtmath_grammarParser.TimeofdayContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTodayAbsTime" ):
                listener.enterTodayAbsTime(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTodayAbsTime" ):
                listener.exitTodayAbsTime(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTodayAbsTime" ):
                return visitor.visitTodayAbsTime(self)
            else:
                return visitor.visitChildren(self)


    class FullAbsTimeContext(Abs_timeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Abs_timeContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def day(self):
            return self.getTypedRuleContext(dtmath_grammarParser.DayContext,0)

        def DIVIDER(self):
            return self.getToken(dtmath_grammarParser.DIVIDER, 0)
        def timeofday(self):
            return self.getTypedRuleContext(dtmath_grammarParser.TimeofdayContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFullAbsTime" ):
                listener.enterFullAbsTime(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFullAbsTime" ):
                listener.exitFullAbsTime(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFullAbsTime" ):
                return visitor.visitFullAbsTime(self)
            else:
                return visitor.visitChildren(self)


    class AbsTimeDayContext(Abs_timeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Abs_timeContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def day(self):
            return self.getTypedRuleContext(dtmath_grammarParser.DayContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAbsTimeDay" ):
                listener.enterAbsTimeDay(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAbsTimeDay" ):
                listener.exitAbsTimeDay(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAbsTimeDay" ):
                return visitor.visitAbsTimeDay(self)
            else:
                return visitor.visitChildren(self)


    class NowAbsTimeContext(Abs_timeContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Abs_timeContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NOW(self):
            return self.getToken(dtmath_grammarParser.NOW, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNowAbsTime" ):
                listener.enterNowAbsTime(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNowAbsTime" ):
                listener.exitNowAbsTime(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNowAbsTime" ):
                return visitor.visitNowAbsTime(self)
            else:
                return visitor.visitChildren(self)



    def abs_time(self):

        localctx = dtmath_grammarParser.Abs_timeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_abs_time)
        try:
            self.state = 91
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                localctx = dtmath_grammarParser.AbsTimeDayContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 84
                self.day()
                pass

            elif la_ == 2:
                localctx = dtmath_grammarParser.TodayAbsTimeContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 85
                self.timeofday()
                pass

            elif la_ == 3:
                localctx = dtmath_grammarParser.FullAbsTimeContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 86
                self.day()
                self.state = 87
                self.match(dtmath_grammarParser.DIVIDER)
                self.state = 88
                self.timeofday()
                pass

            elif la_ == 4:
                localctx = dtmath_grammarParser.NowAbsTimeContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 90
                self.match(dtmath_grammarParser.NOW)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DayContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return dtmath_grammarParser.RULE_day

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class DayOffsetContext(DayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.DayContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def any_number(self):
            return self.getTypedRuleContext(dtmath_grammarParser.Any_numberContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDayOffset" ):
                listener.enterDayOffset(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDayOffset" ):
                listener.exitDayOffset(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDayOffset" ):
                return visitor.visitDayOffset(self)
            else:
                return visitor.visitChildren(self)


    class RecurringDateContext(DayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.DayContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def duo(self):
            return self.getTypedRuleContext(dtmath_grammarParser.DuoContext,0)

        def month(self):
            return self.getTypedRuleContext(dtmath_grammarParser.MonthContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRecurringDate" ):
                listener.enterRecurringDate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRecurringDate" ):
                listener.exitRecurringDate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRecurringDate" ):
                return visitor.visitRecurringDate(self)
            else:
                return visitor.visitChildren(self)


    class NextWeekNumberDayContext(DayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.DayContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def any_number(self):
            return self.getTypedRuleContext(dtmath_grammarParser.Any_numberContext,0)

        def weekday(self):
            return self.getTypedRuleContext(dtmath_grammarParser.WeekdayContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNextWeekNumberDay" ):
                listener.enterNextWeekNumberDay(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNextWeekNumberDay" ):
                listener.exitNextWeekNumberDay(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNextWeekNumberDay" ):
                return visitor.visitNextWeekNumberDay(self)
            else:
                return visitor.visitChildren(self)


    class ThisWeekdayContext(DayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.DayContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def weekday(self):
            return self.getTypedRuleContext(dtmath_grammarParser.WeekdayContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterThisWeekday" ):
                listener.enterThisWeekday(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitThisWeekday" ):
                listener.exitThisWeekday(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitThisWeekday" ):
                return visitor.visitThisWeekday(self)
            else:
                return visitor.visitChildren(self)


    class NextWeekdayContext(DayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.DayContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def weekday(self):
            return self.getTypedRuleContext(dtmath_grammarParser.WeekdayContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNextWeekday" ):
                listener.enterNextWeekday(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNextWeekday" ):
                listener.exitNextWeekday(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNextWeekday" ):
                return visitor.visitNextWeekday(self)
            else:
                return visitor.visitChildren(self)


    class MonthDayContext(DayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.DayContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def duo(self):
            return self.getTypedRuleContext(dtmath_grammarParser.DuoContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMonthDay" ):
                listener.enterMonthDay(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMonthDay" ):
                listener.exitMonthDay(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMonthDay" ):
                return visitor.visitMonthDay(self)
            else:
                return visitor.visitChildren(self)


    class WeekNumberDayContext(DayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.DayContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def any_number(self):
            return self.getTypedRuleContext(dtmath_grammarParser.Any_numberContext,0)

        def weekday(self):
            return self.getTypedRuleContext(dtmath_grammarParser.WeekdayContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWeekNumberDay" ):
                listener.enterWeekNumberDay(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWeekNumberDay" ):
                listener.exitWeekNumberDay(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWeekNumberDay" ):
                return visitor.visitWeekNumberDay(self)
            else:
                return visitor.visitChildren(self)


    class NextRecurringDateContext(DayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.DayContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def duo(self):
            return self.getTypedRuleContext(dtmath_grammarParser.DuoContext,0)

        def month(self):
            return self.getTypedRuleContext(dtmath_grammarParser.MonthContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNextRecurringDate" ):
                listener.enterNextRecurringDate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNextRecurringDate" ):
                listener.exitNextRecurringDate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNextRecurringDate" ):
                return visitor.visitNextRecurringDate(self)
            else:
                return visitor.visitChildren(self)


    class DateContext(DayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.DayContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def duo(self):
            return self.getTypedRuleContext(dtmath_grammarParser.DuoContext,0)

        def month(self):
            return self.getTypedRuleContext(dtmath_grammarParser.MonthContext,0)

        def year(self):
            return self.getTypedRuleContext(dtmath_grammarParser.YearContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDate" ):
                listener.enterDate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDate" ):
                listener.exitDate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDate" ):
                return visitor.visitDate(self)
            else:
                return visitor.visitChildren(self)



    def day(self):

        localctx = dtmath_grammarParser.DayContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_day)
        try:
            self.state = 127
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                localctx = dtmath_grammarParser.DayOffsetContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 93
                self.match(dtmath_grammarParser.T__4)
                self.state = 94
                self.any_number()
                pass

            elif la_ == 2:
                localctx = dtmath_grammarParser.ThisWeekdayContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 95
                self.weekday()
                pass

            elif la_ == 3:
                localctx = dtmath_grammarParser.NextWeekdayContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 96
                self.match(dtmath_grammarParser.T__4)
                self.state = 97
                self.weekday()
                pass

            elif la_ == 4:
                localctx = dtmath_grammarParser.MonthDayContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 98
                self.duo()
                self.state = 99
                self.match(dtmath_grammarParser.T__5)
                pass

            elif la_ == 5:
                localctx = dtmath_grammarParser.RecurringDateContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 101
                self.duo()
                self.state = 102
                self.match(dtmath_grammarParser.T__5)
                self.state = 103
                self.month()
                pass

            elif la_ == 6:
                localctx = dtmath_grammarParser.NextRecurringDateContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 105
                self.match(dtmath_grammarParser.T__4)
                self.state = 106
                self.duo()
                self.state = 107
                self.match(dtmath_grammarParser.T__5)
                self.state = 108
                self.month()
                pass

            elif la_ == 7:
                localctx = dtmath_grammarParser.DateContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 110
                self.duo()
                self.state = 111
                self.match(dtmath_grammarParser.T__5)
                self.state = 112
                self.month()
                self.state = 113
                self.match(dtmath_grammarParser.T__5)
                self.state = 114
                self.year()
                pass

            elif la_ == 8:
                localctx = dtmath_grammarParser.WeekNumberDayContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 116
                self.match(dtmath_grammarParser.T__6)
                self.state = 117
                self.any_number()
                self.state = 118
                self.match(dtmath_grammarParser.T__5)
                self.state = 119
                self.weekday()
                pass

            elif la_ == 9:
                localctx = dtmath_grammarParser.NextWeekNumberDayContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 121
                self.match(dtmath_grammarParser.T__4)
                self.state = 122
                self.match(dtmath_grammarParser.T__6)
                self.state = 123
                self.any_number()
                self.state = 124
                self.match(dtmath_grammarParser.T__5)
                self.state = 125
                self.weekday()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MonthContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return dtmath_grammarParser.RULE_month

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class StringMonthContext(MonthContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.MonthContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def month_name(self):
            return self.getTypedRuleContext(dtmath_grammarParser.Month_nameContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringMonth" ):
                listener.enterStringMonth(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringMonth" ):
                listener.exitStringMonth(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringMonth" ):
                return visitor.visitStringMonth(self)
            else:
                return visitor.visitChildren(self)


    class NumericalMonthContext(MonthContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.MonthContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def duo(self):
            return self.getTypedRuleContext(dtmath_grammarParser.DuoContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumericalMonth" ):
                listener.enterNumericalMonth(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumericalMonth" ):
                listener.exitNumericalMonth(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumericalMonth" ):
                return visitor.visitNumericalMonth(self)
            else:
                return visitor.visitChildren(self)



    def month(self):

        localctx = dtmath_grammarParser.MonthContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_month)
        try:
            self.state = 131
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [71, 72]:
                localctx = dtmath_grammarParser.NumericalMonthContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 129
                self.duo()
                pass
            elif token in [39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]:
                localctx = dtmath_grammarParser.StringMonthContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 130
                self.month_name()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class YearContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return dtmath_grammarParser.RULE_year

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class CenturyContext(YearContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.YearContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def duo(self):
            return self.getTypedRuleContext(dtmath_grammarParser.DuoContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCentury" ):
                listener.enterCentury(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCentury" ):
                listener.exitCentury(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCentury" ):
                return visitor.visitCentury(self)
            else:
                return visitor.visitChildren(self)


    class MillenniumContext(YearContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.YearContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def QUAD(self):
            return self.getToken(dtmath_grammarParser.QUAD, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMillennium" ):
                listener.enterMillennium(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMillennium" ):
                listener.exitMillennium(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMillennium" ):
                return visitor.visitMillennium(self)
            else:
                return visitor.visitChildren(self)



    def year(self):

        localctx = dtmath_grammarParser.YearContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_year)
        try:
            self.state = 135
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [71, 72]:
                localctx = dtmath_grammarParser.CenturyContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 133
                self.duo()
                pass
            elif token in [70]:
                localctx = dtmath_grammarParser.MillenniumContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 134
                self.match(dtmath_grammarParser.QUAD)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TimeofdayContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return dtmath_grammarParser.RULE_timeofday

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class HourMinuteSecondContext(TimeofdayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.TimeofdayContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def duo(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dtmath_grammarParser.DuoContext)
            else:
                return self.getTypedRuleContext(dtmath_grammarParser.DuoContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHourMinuteSecond" ):
                listener.enterHourMinuteSecond(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHourMinuteSecond" ):
                listener.exitHourMinuteSecond(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHourMinuteSecond" ):
                return visitor.visitHourMinuteSecond(self)
            else:
                return visitor.visitChildren(self)


    class QuadTimeContext(TimeofdayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.TimeofdayContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def QUAD(self):
            return self.getToken(dtmath_grammarParser.QUAD, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuadTime" ):
                listener.enterQuadTime(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuadTime" ):
                listener.exitQuadTime(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuadTime" ):
                return visitor.visitQuadTime(self)
            else:
                return visitor.visitChildren(self)


    class HourContext(TimeofdayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.TimeofdayContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def duo(self):
            return self.getTypedRuleContext(dtmath_grammarParser.DuoContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHour" ):
                listener.enterHour(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHour" ):
                listener.exitHour(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHour" ):
                return visitor.visitHour(self)
            else:
                return visitor.visitChildren(self)


    class AmpmHourMinuteContext(TimeofdayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.TimeofdayContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def duo(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dtmath_grammarParser.DuoContext)
            else:
                return self.getTypedRuleContext(dtmath_grammarParser.DuoContext,i)

        def ampm(self):
            return self.getTypedRuleContext(dtmath_grammarParser.AmpmContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAmpmHourMinute" ):
                listener.enterAmpmHourMinute(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAmpmHourMinute" ):
                listener.exitAmpmHourMinute(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAmpmHourMinute" ):
                return visitor.visitAmpmHourMinute(self)
            else:
                return visitor.visitChildren(self)


    class AmpmHourSecondContext(TimeofdayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.TimeofdayContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def duo(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dtmath_grammarParser.DuoContext)
            else:
                return self.getTypedRuleContext(dtmath_grammarParser.DuoContext,i)

        def ampm(self):
            return self.getTypedRuleContext(dtmath_grammarParser.AmpmContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAmpmHourSecond" ):
                listener.enterAmpmHourSecond(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAmpmHourSecond" ):
                listener.exitAmpmHourSecond(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAmpmHourSecond" ):
                return visitor.visitAmpmHourSecond(self)
            else:
                return visitor.visitChildren(self)


    class AmpmHourContext(TimeofdayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.TimeofdayContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def duo(self):
            return self.getTypedRuleContext(dtmath_grammarParser.DuoContext,0)

        def ampm(self):
            return self.getTypedRuleContext(dtmath_grammarParser.AmpmContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAmpmHour" ):
                listener.enterAmpmHour(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAmpmHour" ):
                listener.exitAmpmHour(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAmpmHour" ):
                return visitor.visitAmpmHour(self)
            else:
                return visitor.visitChildren(self)


    class HourMinuteContext(TimeofdayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.TimeofdayContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def duo(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dtmath_grammarParser.DuoContext)
            else:
                return self.getTypedRuleContext(dtmath_grammarParser.DuoContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHourMinute" ):
                listener.enterHourMinute(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHourMinute" ):
                listener.exitHourMinute(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHourMinute" ):
                return visitor.visitHourMinute(self)
            else:
                return visitor.visitChildren(self)



    def timeofday(self):

        localctx = dtmath_grammarParser.TimeofdayContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_timeofday)
        try:
            self.state = 164
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
            if la_ == 1:
                localctx = dtmath_grammarParser.QuadTimeContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 137
                self.match(dtmath_grammarParser.QUAD)
                pass

            elif la_ == 2:
                localctx = dtmath_grammarParser.HourContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 138
                self.duo()
                pass

            elif la_ == 3:
                localctx = dtmath_grammarParser.AmpmHourContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 139
                self.duo()
                self.state = 140
                self.ampm()
                pass

            elif la_ == 4:
                localctx = dtmath_grammarParser.AmpmHourMinuteContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 142
                self.duo()
                self.state = 143
                self.match(dtmath_grammarParser.T__7)
                self.state = 144
                self.duo()
                self.state = 145
                self.ampm()
                pass

            elif la_ == 5:
                localctx = dtmath_grammarParser.AmpmHourSecondContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 147
                self.duo()
                self.state = 148
                self.match(dtmath_grammarParser.T__7)
                self.state = 149
                self.duo()
                self.state = 150
                self.match(dtmath_grammarParser.T__7)
                self.state = 151
                self.duo()
                self.state = 152
                self.ampm()
                pass

            elif la_ == 6:
                localctx = dtmath_grammarParser.HourMinuteContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 154
                self.duo()
                self.state = 155
                self.match(dtmath_grammarParser.T__7)
                self.state = 156
                self.duo()
                pass

            elif la_ == 7:
                localctx = dtmath_grammarParser.HourMinuteSecondContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 158
                self.duo()
                self.state = 159
                self.match(dtmath_grammarParser.T__7)
                self.state = 160
                self.duo()
                self.state = 161
                self.match(dtmath_grammarParser.T__7)
                self.state = 162
                self.duo()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AmpmContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return dtmath_grammarParser.RULE_ampm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAmpm" ):
                listener.enterAmpm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAmpm" ):
                listener.exitAmpm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAmpm" ):
                return visitor.visitAmpm(self)
            else:
                return visitor.visitChildren(self)




    def ampm(self):

        localctx = dtmath_grammarParser.AmpmContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_ampm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 166
            _la = self._input.LA(1)
            if not(_la==9 or _la==10):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DuoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PAIR(self):
            return self.getToken(dtmath_grammarParser.PAIR, 0)

        def SINGLE(self):
            return self.getToken(dtmath_grammarParser.SINGLE, 0)

        def getRuleIndex(self):
            return dtmath_grammarParser.RULE_duo

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDuo" ):
                listener.enterDuo(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDuo" ):
                listener.exitDuo(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDuo" ):
                return visitor.visitDuo(self)
            else:
                return visitor.visitChildren(self)




    def duo(self):

        localctx = dtmath_grammarParser.DuoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_duo)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 168
            _la = self._input.LA(1)
            if not(_la==71 or _la==72):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WeekdayContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return dtmath_grammarParser.RULE_weekday

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class MondayContext(WeekdayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.WeekdayContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMonday" ):
                listener.enterMonday(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMonday" ):
                listener.exitMonday(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMonday" ):
                return visitor.visitMonday(self)
            else:
                return visitor.visitChildren(self)


    class ThursdayContext(WeekdayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.WeekdayContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterThursday" ):
                listener.enterThursday(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitThursday" ):
                listener.exitThursday(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitThursday" ):
                return visitor.visitThursday(self)
            else:
                return visitor.visitChildren(self)


    class FridayContext(WeekdayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.WeekdayContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFriday" ):
                listener.enterFriday(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFriday" ):
                listener.exitFriday(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFriday" ):
                return visitor.visitFriday(self)
            else:
                return visitor.visitChildren(self)


    class SundayContext(WeekdayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.WeekdayContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSunday" ):
                listener.enterSunday(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSunday" ):
                listener.exitSunday(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSunday" ):
                return visitor.visitSunday(self)
            else:
                return visitor.visitChildren(self)


    class WednesdayContext(WeekdayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.WeekdayContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWednesday" ):
                listener.enterWednesday(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWednesday" ):
                listener.exitWednesday(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWednesday" ):
                return visitor.visitWednesday(self)
            else:
                return visitor.visitChildren(self)


    class TuesdayContext(WeekdayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.WeekdayContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTuesday" ):
                listener.enterTuesday(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTuesday" ):
                listener.exitTuesday(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTuesday" ):
                return visitor.visitTuesday(self)
            else:
                return visitor.visitChildren(self)


    class SaturdayContext(WeekdayContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.WeekdayContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSaturday" ):
                listener.enterSaturday(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSaturday" ):
                listener.exitSaturday(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSaturday" ):
                return visitor.visitSaturday(self)
            else:
                return visitor.visitChildren(self)



    def weekday(self):

        localctx = dtmath_grammarParser.WeekdayContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_weekday)
        try:
            self.state = 198
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11]:
                localctx = dtmath_grammarParser.MondayContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 170
                self.match(dtmath_grammarParser.T__10)
                pass
            elif token in [12]:
                localctx = dtmath_grammarParser.MondayContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 171
                self.match(dtmath_grammarParser.T__11)
                pass
            elif token in [13]:
                localctx = dtmath_grammarParser.MondayContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 172
                self.match(dtmath_grammarParser.T__12)
                pass
            elif token in [14]:
                localctx = dtmath_grammarParser.MondayContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 173
                self.match(dtmath_grammarParser.T__13)
                pass
            elif token in [15]:
                localctx = dtmath_grammarParser.TuesdayContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 174
                self.match(dtmath_grammarParser.T__14)
                pass
            elif token in [16]:
                localctx = dtmath_grammarParser.TuesdayContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 175
                self.match(dtmath_grammarParser.T__15)
                pass
            elif token in [17]:
                localctx = dtmath_grammarParser.TuesdayContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 176
                self.match(dtmath_grammarParser.T__16)
                pass
            elif token in [18]:
                localctx = dtmath_grammarParser.TuesdayContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 177
                self.match(dtmath_grammarParser.T__17)
                pass
            elif token in [19]:
                localctx = dtmath_grammarParser.WednesdayContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 178
                self.match(dtmath_grammarParser.T__18)
                pass
            elif token in [20]:
                localctx = dtmath_grammarParser.WednesdayContext(self, localctx)
                self.enterOuterAlt(localctx, 10)
                self.state = 179
                self.match(dtmath_grammarParser.T__19)
                pass
            elif token in [21]:
                localctx = dtmath_grammarParser.WednesdayContext(self, localctx)
                self.enterOuterAlt(localctx, 11)
                self.state = 180
                self.match(dtmath_grammarParser.T__20)
                pass
            elif token in [22]:
                localctx = dtmath_grammarParser.WednesdayContext(self, localctx)
                self.enterOuterAlt(localctx, 12)
                self.state = 181
                self.match(dtmath_grammarParser.T__21)
                pass
            elif token in [23]:
                localctx = dtmath_grammarParser.ThursdayContext(self, localctx)
                self.enterOuterAlt(localctx, 13)
                self.state = 182
                self.match(dtmath_grammarParser.T__22)
                pass
            elif token in [24]:
                localctx = dtmath_grammarParser.ThursdayContext(self, localctx)
                self.enterOuterAlt(localctx, 14)
                self.state = 183
                self.match(dtmath_grammarParser.T__23)
                pass
            elif token in [25]:
                localctx = dtmath_grammarParser.ThursdayContext(self, localctx)
                self.enterOuterAlt(localctx, 15)
                self.state = 184
                self.match(dtmath_grammarParser.T__24)
                pass
            elif token in [26]:
                localctx = dtmath_grammarParser.ThursdayContext(self, localctx)
                self.enterOuterAlt(localctx, 16)
                self.state = 185
                self.match(dtmath_grammarParser.T__25)
                pass
            elif token in [27]:
                localctx = dtmath_grammarParser.FridayContext(self, localctx)
                self.enterOuterAlt(localctx, 17)
                self.state = 186
                self.match(dtmath_grammarParser.T__26)
                pass
            elif token in [28]:
                localctx = dtmath_grammarParser.FridayContext(self, localctx)
                self.enterOuterAlt(localctx, 18)
                self.state = 187
                self.match(dtmath_grammarParser.T__27)
                pass
            elif token in [29]:
                localctx = dtmath_grammarParser.FridayContext(self, localctx)
                self.enterOuterAlt(localctx, 19)
                self.state = 188
                self.match(dtmath_grammarParser.T__28)
                pass
            elif token in [30]:
                localctx = dtmath_grammarParser.FridayContext(self, localctx)
                self.enterOuterAlt(localctx, 20)
                self.state = 189
                self.match(dtmath_grammarParser.T__29)
                pass
            elif token in [31]:
                localctx = dtmath_grammarParser.SaturdayContext(self, localctx)
                self.enterOuterAlt(localctx, 21)
                self.state = 190
                self.match(dtmath_grammarParser.T__30)
                pass
            elif token in [32]:
                localctx = dtmath_grammarParser.SaturdayContext(self, localctx)
                self.enterOuterAlt(localctx, 22)
                self.state = 191
                self.match(dtmath_grammarParser.T__31)
                pass
            elif token in [33]:
                localctx = dtmath_grammarParser.SaturdayContext(self, localctx)
                self.enterOuterAlt(localctx, 23)
                self.state = 192
                self.match(dtmath_grammarParser.T__32)
                pass
            elif token in [34]:
                localctx = dtmath_grammarParser.SaturdayContext(self, localctx)
                self.enterOuterAlt(localctx, 24)
                self.state = 193
                self.match(dtmath_grammarParser.T__33)
                pass
            elif token in [35]:
                localctx = dtmath_grammarParser.SundayContext(self, localctx)
                self.enterOuterAlt(localctx, 25)
                self.state = 194
                self.match(dtmath_grammarParser.T__34)
                pass
            elif token in [36]:
                localctx = dtmath_grammarParser.SundayContext(self, localctx)
                self.enterOuterAlt(localctx, 26)
                self.state = 195
                self.match(dtmath_grammarParser.T__35)
                pass
            elif token in [37]:
                localctx = dtmath_grammarParser.SundayContext(self, localctx)
                self.enterOuterAlt(localctx, 27)
                self.state = 196
                self.match(dtmath_grammarParser.T__36)
                pass
            elif token in [38]:
                localctx = dtmath_grammarParser.SundayContext(self, localctx)
                self.enterOuterAlt(localctx, 28)
                self.state = 197
                self.match(dtmath_grammarParser.T__37)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Month_nameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return dtmath_grammarParser.RULE_month_name

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class JuneContext(Month_nameContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Month_nameContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJune" ):
                listener.enterJune(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJune" ):
                listener.exitJune(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJune" ):
                return visitor.visitJune(self)
            else:
                return visitor.visitChildren(self)


    class OctoberContext(Month_nameContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Month_nameContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOctober" ):
                listener.enterOctober(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOctober" ):
                listener.exitOctober(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOctober" ):
                return visitor.visitOctober(self)
            else:
                return visitor.visitChildren(self)


    class DecemberContext(Month_nameContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Month_nameContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDecember" ):
                listener.enterDecember(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDecember" ):
                listener.exitDecember(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDecember" ):
                return visitor.visitDecember(self)
            else:
                return visitor.visitChildren(self)


    class MayContext(Month_nameContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Month_nameContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMay" ):
                listener.enterMay(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMay" ):
                listener.exitMay(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMay" ):
                return visitor.visitMay(self)
            else:
                return visitor.visitChildren(self)


    class SeptemberContext(Month_nameContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Month_nameContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSeptember" ):
                listener.enterSeptember(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSeptember" ):
                listener.exitSeptember(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSeptember" ):
                return visitor.visitSeptember(self)
            else:
                return visitor.visitChildren(self)


    class MarchContext(Month_nameContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Month_nameContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMarch" ):
                listener.enterMarch(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMarch" ):
                listener.exitMarch(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMarch" ):
                return visitor.visitMarch(self)
            else:
                return visitor.visitChildren(self)


    class JulyContext(Month_nameContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Month_nameContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJuly" ):
                listener.enterJuly(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJuly" ):
                listener.exitJuly(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJuly" ):
                return visitor.visitJuly(self)
            else:
                return visitor.visitChildren(self)


    class JanuaryContext(Month_nameContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Month_nameContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJanuary" ):
                listener.enterJanuary(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJanuary" ):
                listener.exitJanuary(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJanuary" ):
                return visitor.visitJanuary(self)
            else:
                return visitor.visitChildren(self)


    class FebruaryContext(Month_nameContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Month_nameContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFebruary" ):
                listener.enterFebruary(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFebruary" ):
                listener.exitFebruary(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFebruary" ):
                return visitor.visitFebruary(self)
            else:
                return visitor.visitChildren(self)


    class AprilContext(Month_nameContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Month_nameContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterApril" ):
                listener.enterApril(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitApril" ):
                listener.exitApril(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitApril" ):
                return visitor.visitApril(self)
            else:
                return visitor.visitChildren(self)


    class AugustContext(Month_nameContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Month_nameContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAugust" ):
                listener.enterAugust(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAugust" ):
                listener.exitAugust(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAugust" ):
                return visitor.visitAugust(self)
            else:
                return visitor.visitChildren(self)


    class NovemberContext(Month_nameContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a dtmath_grammarParser.Month_nameContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNovember" ):
                listener.enterNovember(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNovember" ):
                listener.exitNovember(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNovember" ):
                return visitor.visitNovember(self)
            else:
                return visitor.visitChildren(self)



    def month_name(self):

        localctx = dtmath_grammarParser.Month_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_month_name)
        try:
            self.state = 231
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [39]:
                localctx = dtmath_grammarParser.JanuaryContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 200
                self.match(dtmath_grammarParser.T__38)
                pass
            elif token in [40]:
                localctx = dtmath_grammarParser.JanuaryContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 201
                self.match(dtmath_grammarParser.T__39)
                pass
            elif token in [41]:
                localctx = dtmath_grammarParser.JanuaryContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 202
                self.match(dtmath_grammarParser.T__40)
                pass
            elif token in [42]:
                localctx = dtmath_grammarParser.FebruaryContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 203
                self.match(dtmath_grammarParser.T__41)
                pass
            elif token in [43]:
                localctx = dtmath_grammarParser.FebruaryContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 204
                self.match(dtmath_grammarParser.T__42)
                pass
            elif token in [44]:
                localctx = dtmath_grammarParser.FebruaryContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 205
                self.match(dtmath_grammarParser.T__43)
                pass
            elif token in [45]:
                localctx = dtmath_grammarParser.MarchContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 206
                self.match(dtmath_grammarParser.T__44)
                pass
            elif token in [46]:
                localctx = dtmath_grammarParser.MarchContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 207
                self.match(dtmath_grammarParser.T__45)
                pass
            elif token in [47]:
                localctx = dtmath_grammarParser.MarchContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 208
                self.match(dtmath_grammarParser.T__46)
                pass
            elif token in [48]:
                localctx = dtmath_grammarParser.AprilContext(self, localctx)
                self.enterOuterAlt(localctx, 10)
                self.state = 209
                self.match(dtmath_grammarParser.T__47)
                pass
            elif token in [49]:
                localctx = dtmath_grammarParser.AprilContext(self, localctx)
                self.enterOuterAlt(localctx, 11)
                self.state = 210
                self.match(dtmath_grammarParser.T__48)
                pass
            elif token in [50]:
                localctx = dtmath_grammarParser.MayContext(self, localctx)
                self.enterOuterAlt(localctx, 12)
                self.state = 211
                self.match(dtmath_grammarParser.T__49)
                pass
            elif token in [51]:
                localctx = dtmath_grammarParser.MayContext(self, localctx)
                self.enterOuterAlt(localctx, 13)
                self.state = 212
                self.match(dtmath_grammarParser.T__50)
                pass
            elif token in [52]:
                localctx = dtmath_grammarParser.JuneContext(self, localctx)
                self.enterOuterAlt(localctx, 14)
                self.state = 213
                self.match(dtmath_grammarParser.T__51)
                pass
            elif token in [53]:
                localctx = dtmath_grammarParser.JuneContext(self, localctx)
                self.enterOuterAlt(localctx, 15)
                self.state = 214
                self.match(dtmath_grammarParser.T__52)
                pass
            elif token in [54]:
                localctx = dtmath_grammarParser.JuneContext(self, localctx)
                self.enterOuterAlt(localctx, 16)
                self.state = 215
                self.match(dtmath_grammarParser.T__53)
                pass
            elif token in [55]:
                localctx = dtmath_grammarParser.JulyContext(self, localctx)
                self.enterOuterAlt(localctx, 17)
                self.state = 216
                self.match(dtmath_grammarParser.T__54)
                pass
            elif token in [56]:
                localctx = dtmath_grammarParser.JulyContext(self, localctx)
                self.enterOuterAlt(localctx, 18)
                self.state = 217
                self.match(dtmath_grammarParser.T__55)
                pass
            elif token in [57]:
                localctx = dtmath_grammarParser.JulyContext(self, localctx)
                self.enterOuterAlt(localctx, 19)
                self.state = 218
                self.match(dtmath_grammarParser.T__56)
                pass
            elif token in [58]:
                localctx = dtmath_grammarParser.AugustContext(self, localctx)
                self.enterOuterAlt(localctx, 20)
                self.state = 219
                self.match(dtmath_grammarParser.T__57)
                pass
            elif token in [59]:
                localctx = dtmath_grammarParser.AugustContext(self, localctx)
                self.enterOuterAlt(localctx, 21)
                self.state = 220
                self.match(dtmath_grammarParser.T__58)
                pass
            elif token in [60]:
                localctx = dtmath_grammarParser.SeptemberContext(self, localctx)
                self.enterOuterAlt(localctx, 22)
                self.state = 221
                self.match(dtmath_grammarParser.T__59)
                pass
            elif token in [61]:
                localctx = dtmath_grammarParser.SeptemberContext(self, localctx)
                self.enterOuterAlt(localctx, 23)
                self.state = 222
                self.match(dtmath_grammarParser.T__60)
                pass
            elif token in [62]:
                localctx = dtmath_grammarParser.OctoberContext(self, localctx)
                self.enterOuterAlt(localctx, 24)
                self.state = 223
                self.match(dtmath_grammarParser.T__61)
                pass
            elif token in [63]:
                localctx = dtmath_grammarParser.OctoberContext(self, localctx)
                self.enterOuterAlt(localctx, 25)
                self.state = 224
                self.match(dtmath_grammarParser.T__62)
                pass
            elif token in [64]:
                localctx = dtmath_grammarParser.OctoberContext(self, localctx)
                self.enterOuterAlt(localctx, 26)
                self.state = 225
                self.match(dtmath_grammarParser.T__63)
                pass
            elif token in [65]:
                localctx = dtmath_grammarParser.OctoberContext(self, localctx)
                self.enterOuterAlt(localctx, 27)
                self.state = 226
                self.match(dtmath_grammarParser.T__64)
                pass
            elif token in [66]:
                localctx = dtmath_grammarParser.NovemberContext(self, localctx)
                self.enterOuterAlt(localctx, 28)
                self.state = 227
                self.match(dtmath_grammarParser.T__65)
                pass
            elif token in [67]:
                localctx = dtmath_grammarParser.NovemberContext(self, localctx)
                self.enterOuterAlt(localctx, 29)
                self.state = 228
                self.match(dtmath_grammarParser.T__66)
                pass
            elif token in [68]:
                localctx = dtmath_grammarParser.DecemberContext(self, localctx)
                self.enterOuterAlt(localctx, 30)
                self.state = 229
                self.match(dtmath_grammarParser.T__67)
                pass
            elif token in [69]:
                localctx = dtmath_grammarParser.DecemberContext(self, localctx)
                self.enterOuterAlt(localctx, 31)
                self.state = 230
                self.match(dtmath_grammarParser.T__68)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Any_numberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SINGLE(self):
            return self.getToken(dtmath_grammarParser.SINGLE, 0)

        def PAIR(self):
            return self.getToken(dtmath_grammarParser.PAIR, 0)

        def QUAD(self):
            return self.getToken(dtmath_grammarParser.QUAD, 0)

        def BIGNUMBER(self):
            return self.getToken(dtmath_grammarParser.BIGNUMBER, 0)

        def getRuleIndex(self):
            return dtmath_grammarParser.RULE_any_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAny_number" ):
                listener.enterAny_number(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAny_number" ):
                listener.exitAny_number(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAny_number" ):
                return visitor.visitAny_number(self)
            else:
                return visitor.visitChildren(self)




    def any_number(self):

        localctx = dtmath_grammarParser.Any_numberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_any_number)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 233
            _la = self._input.LA(1)
            if not(((((_la - 70)) & ~0x3f) == 0 and ((1 << (_la - 70)) & 15) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.operation_sempred
        self._predicates[3] = self.delta_time_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def operation_sempred(self, localctx:OperationContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 1)
         

    def delta_time_sempred(self, localctx:Delta_timeContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 1)
         





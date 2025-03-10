# testing parser for core of milestone 3

import unittest
from interp import Expr, Lit, Add, Sub, Mul, Div, Neg, And, Or, Not, \
                  Let, Name, Eq, Lt, If, Letfun, App, \
                  Read, Show, Assign, Seq

from contextlib import redirect_stdout, redirect_stderr
with redirect_stdout(None), redirect_stderr(None):
    from parse_run import just_parse

class TestParsing(unittest.TestCase):
    def parse(self, concrete:str, expected:Expr|None):
        got = just_parse(concrete)
        self.assertEqual(
            got,
            expected,
            f'parser error: "{concrete}" got: {got} expected: {expected}')            

    def test_0(self):
        self.parse("false", Lit(False))

    def test_1(self):
        self.parse("true", Lit(True))

    def test_2(self):
        self.parse("xyz", Name("xyz"))

    def test_3(self):
        self.parse("123", Lit(123))

    def test_4(self):           
        self.parse("123 + 456", Add(Lit(123), Lit(456)))

    def test_5(self):
        self.parse("123 - 456", Sub(Lit(123), Lit(456)))

    def test_6(self):         
        self.parse("123 * 456", Mul(Lit(123), Lit(456)))

    def test_7(self):
        self.parse("123 / 456", Div(Lit(123), Lit(456)))

    def test_8(self):
        self.parse("-123", Neg(Lit(123)))   

    def test_9(self):   
        self.parse("x && y", And(Name("x"), Name("y")))

    def test_10(self):  
        self.parse("x || y", Or(Name("x"),Name("y")))

    def test_11(self):
        self.parse("! x", Not(Name("x")) )   

    def test_12(self):
        self.parse("x == y", Eq(Name("x"), Name("y")))            

    def test_13(self):
        self.parse("x < y", Lt(Name("x"), Name("y")))

    def test_14(self):
        self.parse("let x = 123 in x end", Let("x", Lit(123), Name("x")))  

    def test_15(self):          
        self.parse("if x then y else z", If(Name("x"), Name("y"), Name("z")))

    def test_16(self):
          self.parse("letfun f(x) = y in z end", Letfun("f", "x", Name("y"), Name("z")))
          
    def test_17(self):
        self.parse("read", Read())

    def test_18(self):  
        self.parse("show x", Show(Name("x")))   

    def test_19(self):
        self.parse("x := y", Assign("x", Name("y")))

    def test_20(self):  
        self.parse("x; y", Seq(Name("x"), Name("y")))

    def test_21(self):
        self.parse("f(x)", App(Name("f"), Name("x")))   
        
    def test_22(self):
        self.parse("(x)", Name("x"))

    def test_23(self):
        self.parse("x;y;z", Seq(Name("x"), Seq(Name("y"), Name("z"))))

    def test_24(self):
        self.parse("x := y; z", Seq(Assign("x", Name("y")), Name("z")))
                   
    def test_25(self):
        self.parse("x; y:= z", Seq(Name("x"), Assign("y", Name("z"))) )

    def test_26(self):
        self.parse("show x; y", Seq(Show(Name("x")), Name("y")))

    def test_27(self):
        self.parse("x; show y", Seq(Name("x"), Show(Name("y"))))
                   
    def test_28(self):
        self.parse("x := y; if x then y else z", 
                   Seq(Assign("x", Name("y")), If(Name("x"), Name("y"), Name("z"))))

    def test_29(self):
        self.parse("if x then y else z; x := y", 
                   Seq(If(Name("x"), Name("y"), Name("z")), Assign("x", Name("y"))))

    def test_30(self):
        self.parse("x := show y", Assign("x", Show(Name("y"))))

    def test_31(self):
        self.parse("show x := y", Show(Assign("x",Name("y"))))

    def test_32(self):
        self.parse("if x then y else show x", 
                     If(Name("x"), Name("y"), Show(Name("x"))))

    def test_33(self):
        self.parse("show if x then y else z", 
                     Show(If(Name("x"), Name("y"), Name("z"))))

    def test_34(self):
        self.parse("if x then y else z := 3", 
                    If(Name("x"), Name("y"), Assign("z", Lit(3))))

    def test_35(self):
        self.parse("x := y || z", 
                    Assign("x", Or(Name("y"), Name("z"))))

    def test_36(self):
        self.parse("show x || y",
                    Show(Or(Name("x"), Name("y"))))

    def test_37(self):
        self.parse("if x then y else z || w",
                    If(Name("x"), Name("y"), Or(Name("z"), Name("w"))))

    def test_38(self):
        self.parse("x || y || z",
                    Or(Or(Name("x"), Name("y")), Name("z"))) 

    def test_39(self):
        self.parse("x || y && z",
                    Or(Name("x"), And(Name("y"), Name("z"))))

    def test_40(self):
        self.parse("x && y || z",
                    Or(And(Name("x"), Name("y")), Name("z")))

    def test_41(self):
        self.parse("x && y && z",
                    And(And(Name("x"), Name("y")), Name("z")))

    def test_42(self):
        self.parse("! x && y",
                    And(Not(Name("x")), Name("y")))

    def test_43(self):
        self.parse("x && ! y",
                    And(Name("x"), Not(Name("y")))) 

    def test_44(self):
        self.parse("x == y == z", None)

    def test_45(self):
        self.parse("x == y < z", None)                         

    def test_46(self):
        self.parse("x < y == z", None)

    def test_47(self):        
        self.parse("x < y < z", None)   

    def test_48(self):
        self.parse("!x == y",
                    Not(Eq(Name("x"), Name("y"))))

    def test_49(self):
        self.parse("x == !y", None)

    def test_50(self):
        self.parse("!x < y",
                    Not(Lt(Name("x"),Name("y"))))

    def test_51(self):
        self.parse("x < !y", None)

    def test_52(self):
        self.parse("x + y + z",
                    Add(Add(Name("x"), Name("y")), Name("z")))

    def test_53(self):
        self.parse("x + y - z",
                    Sub(Add(Name("x"), Name("y")), Name("z")))

    def test_54(self):
        self.parse("x - y + z",
                    Add(Sub(Name("x"), Name("y")), Name("z")))

    def test_55(self): 
        self.parse("x - y - z",
                    Sub(Sub(Name("x"), Name("y")), Name("z")))

    def test_56(self): 
        self.parse("x + y < z",
                    Lt(Add(Name("x"), Name("y")), Name("z")))

    def test_57(self):
        self.parse("x < y + z",
                    Lt(Name("x"), Add(Name("y"), Name("z"))))

    def test_58(self):
        self.parse("x - y < z",
                    Lt(Sub(Name("x"), Name("y")), Name("z")))

    def test_59(self):
        self.parse("x < y - z",
                    Lt(Name("x"), Sub(Name("y"), Name("z"))))

    def test_60(self):
        self.parse("x + y == z",
                    Eq(Add(Name("x"), Name("y")), Name("z")))

    def test_61(self):   
        self.parse("x == y + z",
                    Eq(Name("x"), Add(Name("y"), Name("z"))))

    def test_62(self):   
        self.parse("x - y == z",
                    Eq(Sub(Name("x"), Name("y")), Name("z")))

    def test_63(self):
        self.parse("x == y - z",
                    Eq(Name("x"), Sub(Name("y"), Name("z"))))

    def test_64(self):
        self.parse("x * y * z",
                    Mul(Mul(Name("x"), Name("y")), Name("z")))

    def test_65(self):
        self.parse("x * y / z",
                    Div(Mul(Name("x"), Name("y")), Name("z")))

    def test_66(self):
        self.parse("x / y * z",
                    Mul(Div(Name("x"), Name("y")), Name("z")))  

    def test_67(self):
        self.parse("x / y / z",
                    Div(Div(Name("x"), Name("y")), Name("z")))  

    def test_68(self):
        self.parse("x * y + z",
                    Add(Mul(Name("x"), Name("y")), Name("z")))

    def test_69(self):
        self.parse("x + y * z",
                    Add(Name("x"), Mul(Name("y"), Name("z"))))

    def test_70(self):
        self.parse("x - y * z",
                    Sub(Name("x"), Mul(Name("y"), Name("z"))))

    def test_71(self):   
        self.parse("x * y - z",
                    Sub(Mul(Name("x"), Name("y")), Name("z")))

    def test_72(self): 
        self.parse("x + y / z",
                    Add(Name("x"), Div(Name("y"), Name("z"))))

    def test_73(self):
        self.parse("x / y + z",
                    Add(Div(Name("x"), Name("y")), Name("z")))

    def test_74(self):
        self.parse("x - y / z",
                    Sub(Name("x"), Div(Name("y"), Name("z"))))

    def test_75(self):
        self.parse("x / y - z",
                    Sub(Div(Name("x"), Name("y")), Name("z")))

    def test_76(self):
        self.parse("!!x", Not(Not(Name("x"))))

    def test_77(self):
        self.parse("--x", Neg(Neg(Name("x"))))

    def test_78(self):
        self.parse("x * -y",
                    Mul(Name("x"), Neg(Name("y"))))

    def test_79(self):
        self.parse("-x * y",
                    Mul(Neg(Name("x")), Name("y")))

    def test_80(self):
        self.parse("x / -y",
                    Div(Name("x"), Neg(Name("y"))))  

    def test_81(self):
        self.parse("-x / y",
                    Div(Neg(Name("x")), Name("y")))

    def test_82(self):
        self.parse("f(a;b)", App(Name("f"), Seq(Name("a"), Name("b"))))

    def test_83(self):
        self.parse("let x = a;b in c;d end",
                    Let("x", Seq(Name("a"), Name("b")), Seq(Name("c"), Name("d"))))

    def test_84(self):  
        self.parse("letfun f(x) = a;b in c;d end",
                    Letfun("f", "x", Seq(Name("a"), Name("b")), Seq(Name("c"), Name("d"))))

    def test_85(self):
        self.parse("(a;b);c", Seq(Seq(Name("a"), Name("b")), Name("c")))

    def test_86(self):
        self.parse("- f(x)", Neg(App(Name("f"), Name("x"))))

    def test_87(self):
        self.parse("-23", Neg(Lit(23)))

    def test_88(self):
        self.parse("f(g)(x)", App(App(Name("f"), Name("g")), Name("x")))


if __name__ == "__main__":
    unittest.main()

from interp import (Add, Sub, Mul, Div, Neg, Let, Name, Lit, If, 
                     LetFun, App, Expr, ImgPath, StitchHorizontal, 
                     Rotate90, And, Or, Not, Eq, Lt, run)

from lark import Lark, Token, ParseTree, Transformer
from lark.exceptions import VisitError
from pathlib import Path

parser = Lark(Path('expr.lark').read_text(),
              start='expr',
              parser='lalr',
              strict=True)

class ParseError(Exception): 
    pass

def parse(s: str) -> ParseTree:
    try:
        return parser.parse(s)
    except Exception as e:
        raise ParseError(e)

class AmbiguousParse(Exception):
    pass

class ToExpr(Transformer[Token, Expr]):
    def add(self, args: tuple[Expr, Expr]) -> Expr:
        return Add(args[0], args[1])
    
    def sub(self, args: tuple[Expr, Expr]) -> Expr:
        return Sub(args[0], args[1])
    
    def mul(self, args: tuple[Expr, Expr]) -> Expr:
        return Mul(args[0], args[1])
    
    def div(self, args: tuple[Expr, Expr]) -> Expr:
        return Div(args[0], args[1])
    
    def neg(self, args: tuple[Expr]) -> Expr:
        return Neg(args[0])
    
    def and_(self, args: tuple[Expr, Expr]) -> Expr:
        return And(args[0], args[1])
    
    def or_(self, args: tuple[Expr, Expr]) -> Expr:
        return Or(args[0], args[1])
    
    def not_(self, args: tuple[Expr]) -> Expr:
        return Not(args[0])
    
    def eq(self, args: tuple[Expr, Expr]) -> Expr:
        return Eq(args[0], args[1])
    
    def lt(self, args: tuple[Expr, Expr]) -> Expr:
        return Lt(args[0], args[1])
    
    def let(self, args: tuple[Token, Expr, Expr]) -> Expr:
        return Let(args[0].value, args[1], args[2])
    
    def letfun(self, args: tuple[Token, Token, Expr, Expr]) -> Expr:
        return LetFun(args[0].value, args[1].value, args[2], args[3])
    
    def app(self, args: tuple[Expr, Expr]) -> Expr:
        return App(args[0], args[1])
    
    def if_then_else(self, args: tuple[Expr, Expr, Expr]) -> Expr:
        return If(args[0], args[1], args[2])
    
    def int_lit(self, args: tuple[Token]) -> Expr:
        return Lit(int(args[0].value))
    
    def true_lit(self, _) -> Expr:
        return Lit(True)
    
    def false_lit(self, _) -> Expr:
        return Lit(False)
    
    def var(self, args: tuple[Token]) -> Expr:
        return Name(args[0].value)
    
    def image_lit(self, args: tuple[Token]) -> Expr:
        path = args[0].value[1:-1]
        return Lit(ImgPath(path))
    
    def stitch_horizontal(self, args: tuple[Expr, Expr]) -> Expr:
        return StitchHorizontal(args[0], args[1])
    
    def rotate90(self, args: tuple[Expr]) -> Expr:
        return Rotate90(args[0])
    
    def _ambig(self, _) -> Expr:
        raise AmbiguousParse()

def genAST(t: ParseTree) -> Expr:
    try:
        return ToExpr().transform(t)
    except VisitError as e:
        if isinstance(e.orig_exc, AmbiguousParse):
            raise AmbiguousParse()
        else:
            raise e

def parse_and_run(s: str) -> None:
    try:
        tree = parse(s)
        ast = genAST(tree)
        run(ast)
    except AmbiguousParse:
        print("Error: Ambiguous parse")
    except ParseError as e:
        print("Error parsing expression:")
        print(e)

tests = [
    "let x = 1 + 2 in x - 3 end",
    "let x = 1 in let x = 2 in x * 3 end end",
    "let x = 2 in if x == 5 then x + 5 else 8 - x end",
    '"hopper.jpg" ++ "hopper.jpg"',
    '@"hopper.jpg"'
]

if __name__ == "__main__":
    print("Running test expressions...")
    for test in tests:
        print(f"\nTesting: {test}")
        parse_and_run(test)
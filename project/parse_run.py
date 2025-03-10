# FIXES FROM MILESTONE 2:
# RENAMED FILE FROM parse-run.py to parse_run.py
# NO MORE CODE AT THE TOP LEVEL
# INCLUDING IMAGE FILES IN SUBMISSION


from interp import (Add, Sub, Mul, Div, Neg, Let, Name, Lit, If, 
                     Letfun, App, Expr, Assign, Seq, Show, Read, ImgPath, StitchHorizontal, 
                     Rotate90, And, Or, Not, Eq, Lt, Filter, Collage, run)

from lark import Lark, Token, ParseTree, Transformer, Tree
from lark.exceptions import VisitError
from pathlib import Path


#parser = Lark(Path('expr.lark').read_text(), start='expr', parser='earley', ambiguity='explicit')
parser = Lark(Path('expr.lark').read_text(), start='expr', parser='lalr', strict=False)

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
        return Letfun(args[0].value, args[1].value, args[2], args[3])
    
    def app(self, args: tuple[Expr, Expr]) -> Expr:
        return App(args[0], args[1])

    def assign(self, args: tuple[Token, Expr]) -> Expr:
        return Assign(args[0].value, args[1])

    def seq(self, args: tuple[Expr, Expr]) -> Expr:
        return Seq(args[0], args[1])

    def show(self, args: tuple[Expr]) -> Expr:
        return Show(args[0])

    def read(self, args) -> Expr:
        return Read()

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
    
    def filter(self, args: tuple[Token, Expr]) -> Expr:
        filter_type = args[0].value
        image = args[1]
        return Filter(filter_type, image)
    
    def collage(self, args: tuple[list[Expr], Expr, Expr]) -> Expr:
        images = args[0]
        rows = args[1]
        cols = args[2]
        return Collage(images, rows, cols)
    
    def expr_list(self, args: list[Expr]) -> list[Expr]:
        return args
    
    def empty_list(self, _) -> list[Expr]:
        return []
    
    def seq_expr(self, args):
        if len(args) == 1:
            return args[0]
        return args[0]
    
    def __default__(self, data, children, meta):
        if isinstance(data, Token):
            return data
        if len(children) == 1:
            return children[0]
        return Tree(data, children)
    
   # def _ambig(self, _) -> Expr:
       # raise AmbiguousParse()

def genAST(t: ParseTree) -> Expr:
    try:
        result = ToExpr().transform(t)
        if isinstance(result, Tree):
            if len(result.children) == 1:
                return result.children[0]
        return result
    except VisitError as e:
        if isinstance(e.orig_exc, AmbiguousParse):
            raise AmbiguousParse()
        else:
            raise e

def just_parse(s: str):
    try:
        tree = parse(s)
        ast = genAST(tree)
        return ast
    except AmbiguousParse:
        print("Error: Ambiguous parse")
        return None
    except ParseError as e:
        print("Error parsing expression:")
        print(e)
        return None

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

def driver():
    """Interactive driver for the interpreter"""
    print("Enter expressions to evaluate, or 'quit' to exit.")
    history = []
    
    while True:
        try:
            lines = []
            line = input("> ")
            if line.lower() == 'quit':
                break
                
            lines.append(line)
            
            while True:
                continuation = input("... ")
                if not continuation.strip():
                    break
                lines.append(continuation)
                
            expr_text = '\n'.join(lines)
            
            history.append(expr_text)
            
            parse_and_run(expr_text)
            
        except KeyboardInterrupt:
            print("\nInterrupted")
        except EOFError:
            print("\nExiting")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Run the sample programs that demonstrate the language features"""
    print("\n=== Testing basic image operations ===")
    test1 = 'let x = "hopper.jpg" in show x ++ "hopper.jpg" end'
    print(f"Running: {test1}")
    parse_and_run(test1)
    
    print("\n=== Testing advanced image operations with filters ===")
    test2 = 'let img = "hopper.jpg" in show filter red img; show filter green img; show filter blue img end'
    print(f"Running: {test2}")
    parse_and_run(test2)
    
    print("\n=== Testing image collage with user input ===")
    test3 = '''
    let rows = read in
    let cols = read in
    show collage ["hopper.jpg", "hopper.jpg", "hopper.jpg", "hopper.jpg"] rows , cols
    end end
    '''
    print(f"Running: {test3}")
    print("(This program will prompt for rows and columns for the collage)")
    parse_and_run(test3)
    
    print("\n=== Testing sequence and assignment ===")
    test4 = '''
    let x = 5 in
    show x;
    x := x * 2;
    show x;
    show x + 10
    end
    '''
    print(f"Running: {test4}")
    parse_and_run(test4)

    print("\n=== Testing read ===")
    test5 = '''
    let x = read in
    show x
    end
    '''
    print(f"Running: {test5}")
    parse_and_run(test5)

if __name__ == "__main__":
    # You can uncomment one of these to run when executing this file directly
    # driver()
    # main()
    pass
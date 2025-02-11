from lark import Lark, ParseTree

grammar = '''
ID.1: /[A-Za-z]+/
_TRUE.2: "true"
_FALSE.2: "false"

%import common.WS
%ignore WS

?expr: or_expr
     | "let" ID "=" expr "in" expr -> let

?or_expr: or_expr "||" and_expr -> or_
        | and_expr

?and_expr: and_expr "&&" not_expr -> and_
         | not_expr

?not_expr: "!" not_expr -> not_
         | atom

?atom: "true"  -> true
     | "false" -> false
     | ID      -> id
     | "(" expr ")"
'''

parser = Lark(grammar, start='expr', ambiguity="explicit", lexer="basic")

class ParseError(Exception):
    pass

def parse(s: str) -> ParseTree:
    try:
        return parser.parse(s)
    except Exception as e:
        raise ParseError(e)

def driver():
    while True:
        try:
            s = input('expr: ')
            t = parse(s)
            print("raw:", t)
            print("pretty:")
            print(t.pretty())
        except ParseError as e:
            print("parse error:")
            print(e)
        except EOFError:
            break

driver()

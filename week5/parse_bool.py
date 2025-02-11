# Problem 1: Boolean Expression Parsing

# This is an almost unchanged copy of the parse_arith.py program
# described in lecture. Your task is to replace the arithmetic
# expression grammar read into Lark with a boolean expression grammar.
# (You should just define your new grammar as a string in this file,
# rather than bothering with a separate .lark file.)
#
# Start by creating a copy of this file called parse_bool1.py.
# Do your work there and submit that file.
#
# Your boolean expression language should support 
# boolean literals `true` and `false`, the operators
# `||` (or), `&&` (and), and `!` (not), `let` bindings,
# and names.
#
# Precedence of operators: `!` should have the highest
# precedence, followed by `&&`, followed by `||`.
# The two binary operators should be left-associative.
#
# Hint: the necessary grammar structure is very similar
# to the one for arithmetic expressions!
#
# One wrinkle: `true` and `false` look just like ordinary
# identifier names, so some lexer-level magic (described below)
# is needed to make sure that we treat them as special tokens. 
#

from lark import Lark, ParseTree

grammar ='''
# put your .lark grammar here, rather than in a separate file.

# Some magic follows...
# To avoid confusion between the literals `true` and `false`
# and identifiers, use these definitions which carry priority suffixes.
# The lexer will match the tokens with .2 in preference to the one with .1 
# We must also specify lexer='basic' when processing the grammar.
# The leading underscores prevent building an extra level of
# tree for the literal cases.
ID.1: /[A-Za-z]+/ 
_TRUE.2: "true" 
_FALSE.2: "false"

# remainder of your grammar goes here...

'''

parser = Lark(grammar,start='expr',ambiguity="explicit",
              lexer="basic")  # this is important to make lexer token priorities work

class ParseError(Exception):
    pass

def parse(s:str) -> ParseTree:
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




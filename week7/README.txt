Week 7 Practice Exercises

The practice exercises for this week consists of 4 problems,
with a total of 6 files to submit:

parse_run_imp1.py
imp1.lark
interp_imp1.py
fib.toy
fpure.py
selection.txt

To submit, place these files in a single directory called week7,
zip them together to produce a single file week7.zip, and upload
this file to Canvas.

As usual, please make sure that you zip the files
in context of the directory, not just the individual files,
so that when unzipped a new directory is created. 

PROBLEM 1: Extension to the imperative language implementation.

This problems deals with the imperative language parser and
interpreter dicussed in class on Feb. 17.  The relevant files are
imp.lark, interp_imp.py, and parse_run_imp.py .

Begin by making copies of these files, called imp1.lark,
interp_imp1.py and parse_run_imp1.py.  Your task with these files is
to extend the language handled by this interpreter, by adding a new
`for` statement, with the syntax:

for x in e1 to e2 do s

where `x` is a variable name, `e1` and `e2` are expressions, and `s`
is a statement.  To execute this statement, the interpreter should:

(1) Evaluate `e1` and `e2` in the current environment to values --
    let's call them `v1` and `v2`

(2) Define a new variable with name `x` whose scope is just `s`, and
    initialize it to `v1`.

(3) As long as the value of `x` is no greater than `v2`, execute the
    statement `s`.

(4) Add 1 to the value of `x` and repeat from step (iii).

Here are a few example programs, with their intended output:

{ for x in 1 to 5 do print x }
-> prints 1 2 3 4 5
{ var x := 5; for x in x to 2*x do print x; print x}
-> prints 5 6 7 8 9 10 5
{ for x in 1 to 10 do {print x; x:= x + 1}}
-> prints 1 3 5 7 9
{ for x in 1 to 5 do {var x := 0; print x}}
-> prints 0 0 0 0 0

PROBLEM 2: Recursion into iteration

The value of the n'th Fibonacci number can be computed recursively in
Python as follows:

def fib(n:int) -> int: 
  if 2 > n:
    return n  
  else: 
    return fib(n-1) + fib(n-2)

print(fib(10))   # prints 55

Your task is to write an *iterative* implementation of the Fibonacci
function using our toy imperative language (NOT Python!).  In other
words, you should write a program which you can feed to our
interpreter that computes the n'th Fibonacci number for an arbitrary
choice of n (e.g. n = 10). You can use either the original interpreter
(parse_run_imp.py) or your modified version that supports `for` loops
(parse_run_imp1.py), since it is easy to solve this problem with
either `for` or `whilenz`.

If you're not sure how to compute Fibonacci iteratively, feel free to 
do a little research on the Web. 

Put your solution in a file `fib.toy`. 

PROBLEM 3: Iteration into recursion

Consider this Python function:

def f(n:int) -> int:
  a = 0
  c = -1
  while n > a:
    a = a * 2 + 1
    c = c + 1
  return c

Write a *pure, recursive* Python function that has the same behavior
as `f` on all inputs `n`.  You may not use assignment or any other
effects! Hint: A nested function may be useful.

Put your solution in a file `fpure.py`.

By the way, what does this function compute?

PROBLEM 4: Analysis 

Compare and contrast the C++ `switch` statement and the Python `match`
statement. What are their similarities and differences, both
syntactically and semantically? Is one strictly more powerful than the
other?  Aim for about 250 words.

Put your answer in a plain-text file `selection.txt`.

Note: Yes, I know you can get an LLM to answer this question for you.
If you do that, try to absorb what it tells you. Does it address all
the issues you think are important? And, as always, be on the lookout
for nonsense!

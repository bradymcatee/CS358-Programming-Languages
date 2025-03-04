Week 8 Practice Exercises

The practice exercises for this week consists of 5 problems.
The first problem, based on the interpreter, is described below,
and should produce two submission files: interp_arr1.py and parse_run_arr1.py. 
The remaining problems are in data_exercises.pdf, and the
corresponding solutions should be placed in data_solutions.txt.

In summary, there are a total of 3 files to submit:

interp_arr1.py
parse_run_arr1.py
data_solutions.txt

To submit, place these files in a single directory called week8,
zip them together to produce a single file week8.zip, and upload
this file to Canvas.

As usual, please make sure that you zip the files
in context of the directory, not just the individual files,
so that when unzipped a new directory is created. 

PROBLEM 1: Implementing array operations.

This problem deals extending our expression language to support
(mutable) arrays and sequence expressions. For this problem,
the necessary AST and parsing support for the new expressions is
already provided; your task is just to add support for evaluating them.
The relevant files are expr_arr.lark, interp_arr.py, and parse_run_arr.py .

Begin by making a copies of interp_arr.py and parse_run_arr.py,
called interp_arr1.py and parse_run_arr1.py respectively. 
Modify parse_run_arr1.py to import from interp_arr1 instead of interp_arr;
otherwise this file needs no changes.

Note that parse_run_arr1.py has been slightly modified to improve support for
entry of text expressions from the keyboard. Multi-line expressions are now supported
using `\` as a continuation character (just like in Python itself), and line
editing (back-space, history, etc.) is now available because module `readline` 
is imported. (This feature may not work properly on smart phones.)

Now modify interp_arr1.py file to add additional cases to the `evalInEnv` 
function to handle the four new expression forms Arr, Get, Set, and Seq. 
The concrete syntax for these forms is already defined in expr_arr.lark,
as follows:

Arr
Syntax: [ e1, e2, ..., en ]
Semantics: evaluate the expressions e1,...,en, create a new array a containing
the resulting values, and return a. 

Get
Syntax: e1 [ e2 ]
Semantics: evaluate e1 to an array value a and e2 to an integer i,
and return the i'th element of a (counting from 0).
Raise an exception if a is not an array, i is not an integer, or i is
outside the bounds of a. 

Set
Syntax: e1 [e2] := e3
Semantics: evaluate e1 to an array value a, e2 to an integer i, and e3 to a
value v, set the i'th element of a (counting from 0) to v, and return a.
Raise an exception if a is not an array, i is not an integer, or i is
outside the bounds of a. 

Seq
Syntax e1 ; e2
Semantics: evaluate e1, throw away the result, then evaluate e2 and return its value.

To implement these, you will first need to expand the `Value` type to support
array values.  It is up to you to figure out what needs to be added.

As a test example, the following expression should evaluate to [2,1]:

letfun swap(p) = let t = p[0] in p[0] := p[1]; p[1] := t end in swap([1,2]) end

Note that arrays can contain other arrays. For example, the following expression
essentially builds a linked list of two-element arrays, terminated by a 0, and then
sums up its elements, so it should evaluate to 60:

letfun sum(l) = ifnz l then l[0] + sum(l[1]) else 0 in \
  let mylist = [10,[20,[30,0]]] in \
     sum(mylist) \
  end \
end

Submit your interp_arr1.py and parse_run_arr1.py files. 

REMAINING PROBLEMS ARE IN data_exercises.pdf





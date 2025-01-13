# Week 1 Practice Exercises  (due at noon, 1/13/25)
#
# Your task is to complete the missing parts of this file.
# For the text answer for Problem 6, place it in
# a comment block, so the program code can run.
#
# The file test1.py contains a test driver for all the python
# problems in this assignment.  You can run it just using
# python3 test1.py
# Of course, you may wish to do additional testing as well.
#
# You will receive credit for each problem you ATTEMPT, even
# if your code does not work perfectly. Make sure that
# your submitted file can be executed by Python, i.e.
# don't let errors in incomplete solutions prevent your
# completed code from running!
#
# SUBMISSION: When you're done modifying this file, submit it
# to the Canvas dropbox, without zipping or renaming the file.
# Do not submit any other files.  There's no need to put your
# name in the source code; Canvas will tell us which submission is yours.
# MAKE SURE TO CLICK THE SUBMIT BUTTON; the submission isn't registered
# until then.  You can resubmit as many times as you like up
# until the deadline; we'll only look at the last submission.

# For these exercises, you'll need to have access to a working version of
# the python3.12 or later interpreter.  This is available at the
# command line on the linuxlab systems (the default version there is 3.12.3),
# and is also easy to install on your own system (see https://www.python.org/downloads).
# Make sure not to try earlier versions. 

# Unless you are strongly committed to another editor, we recommend that you
# use JS Code for your Python work.  It has the important advantage of supporting
# type checking using the pylance plug-in.  It also supports powerful AI support
# using the CoPilot plug-in; this is a mixed blessing, but it can save a lot of time. 

# If you are new to Python, you might want to start with the
# comprehensive tutorial at https://docs.python.org/3/tutorial/.
# The most relevant sections are:
#   Tutorial 3.1.2 Text
#   Tutorial 3.1.3 Lists
#   Tutorial 4.1 If
#   Tutorial 4.7 Match Statements
#   Tutorial 4.8 Functions
#   Tutorial 5.3 Tuples and Sequences
#   Tutorial 9.3 Classes
# Of course, google is always your friend.

# Note: Our code templates use type annotations as documentation, and to
# allow you to run your code through a typechecking tool (we recommend
# using pylance/pyright under VS Code for this, as described above).
# However, your solutions are NOT REQUIRED to pass such a type checker.
# Remember that Python ignores these type annotations at runtime, so if
# the code can still run correctly even if it doesn't obey them.
# But Python does still require that any annotations present be syntactically
# correct and that any type names used in them be properly in scope.

# Problem 1
#
# A palindrome is a string that reads the same backwards as forwards, e.g.
#   aba
#   ++ ** ++
#   12/22/21
#
# Complete the definitions of the following two versions of a
# palindrome testing function

def ispal1(s:str) -> bool :
    """Return True iff s is a palindrome"""
    for i in range (len(s) // 2):
        if s[i] != s[len(s)-i-1]:
            return False
    return True

def ispal2(s:str) -> bool :
    """Return True iff s is a palindrome"""
    if s == s[::-1]:
        return True
    return False

# Problem 2
#
# The factorial of a non-negative integer n is the product
# 1 * 2 * 3 * ... * n
# By convention, the factorial of 0 is 1. 
#
# Complete the definitions of the following two versions of
# a function to compute factorials

def fac1(n:int) -> int | None:
    for i in range(n-1):
        i = i * i+1

def fac2(n:int) -> int | None:
    if n <= 0:
        return None
    else:
        return n * fac2(n-1)

# Problem 3
#
# A Python sequence is an object that supports iteration, element
# access using [] notation and the len() function. Examples
# include lists, tuples, and ranges.
#
# Complete the definitions of the following two versions of
# a function that takes an integer sequence and returns a
# list containing a copy of the input in which every instance of
# 0 is duplicated.
#
# Examples
# input:               output:
#  [0]                  [0,0]
#  (1)                  [1]
#  (0,1,0)              [0,0,1,0,0]
#  range(3)             [0,0,1,2]
#
#

from typing import Sequence

def dupz1(nums:Sequence[int]) -> list[int]:
    """Return copy of nums in which every instance of 0 is duplicated."""
    # implement using a loop over nums
    ...


def dupz2(nums:Sequence[int]) -> list[int]:  # type: ignore (see below)
    """Return copy of nums in which every instance of 0 is duplicated."""
    # implement using a match case statement over nums.
    # You might get type errors here; ignore them.
    ...
    
# Problem 4
#
# Consider binary trees that have integer values at the leaves
# (and no values at interior nodes).  Such a tree is either:
# - a Leaf node carrying an int, or
# - a Branch node carrying two subtrees (each of which is either a Leaf or another Branch)
#
# There are several different ways to encode such trees in Python.
# For this problem we will use a (fairly) conventional object-oriented programming
# (OOP) approach, with two classes, Branch and Leaf.  We use dataclasses
# because they conveniently define the constructors for us (and these support
# positional matching in match case statements).  Normal OOP practice would be
# to make these sub-classes of a common abstract super-class Tree;
# this would be "abstract" because we never instantiate Tree directly,
# only its subclasses Branch and Leaf.  But instead of defining Tree as a class,
# we'll define it as a Python union type, stating directly that a Tree is the union of
# Branch and Leaf, because this gets us better type-checking support. 
# We override the default implementation of the __str__() method in both
# classes to give a more compact # representation of trees on output.
#  
# To calculate over trees, the conventional OOP approach is to
# define methods for the base  Tree and override them appropriately
# in each sub-class. This is how __str__ and size() are defined below.
# Notice how this approach groups together all the code for each sub-class.
#
# An alternative approach is to think of the tree objects as "just data"
# and traverse them using pattern matching. This is how sum() is defined below.
# Notice how this approach groups together the code for the different cases,
# which the OOP approach scatters across the different sub-class definitions.

from dataclasses import dataclass

type Tree = Branch | Leaf

@dataclass
class Branch():
    left: Tree
    right: Tree
    def __str__(self) -> str:
        return f"({self.left},{self.right})"
    def size(self) -> int:
        """Return number of nodes in this tree"""
        return self.left.size() + self.right.size() + 1

 
@dataclass
class Leaf():
    value: int
    def __str__(self) -> str:
        return f"{self.value}"
    def size(self) -> int:
        """Return number of nodes in this tree"""
        return 1


def sum(t:Tree) -> int:
    """Return sum of leaf values in this tree"""
    match t:
        case Branch(l,r): return sum(l) + sum(r)
        case Leaf(v): return v

a : Tree = Branch(Branch(Leaf(1),Leaf(2)),Branch(Branch(Leaf(3),Leaf(4)),Leaf(5)))

print(a)
print(a.size())
print(sum(a))

# Your tasks for this problem are to implement two additional functions on trees:

# t.depth() should return the depth of the tree, i.e. the number of
# edges in the longest path from the root of the tree to any leaf.
# For example: a.depth() = 3 and Leaf(42).depth() = 0.
# This should be implemented as a method by adding appropriate definitions
# to the Leaf and Node classes, using size() as a model.

# swap(t) should return a copy of tree t with the left and right
# branched swapped at every level.
# For example: swap(a) = Branch(Branch(Leaf(5),Branch(Leaf(4),Leaf(3))),Branch(Leaf(2),Leaf(1)))
# This should be implemented as a function using match case, taking size1()
# as a model. 

# Hint: neither of these functions requires much code at all; it's just a
# matter of putting it in the right place!


# Problem 5
#
# Another way to encode the binary trees from Problem 4 is to use labeled lists.
# This is arguably the more "Pythonic" way to do things.
# This has the advantage of not requiring any new class or type definitions.
# It has the corresponding disadvantage of giving less useful feedback
# about static typing errors.
# 
# We represent Leaf(n) by the list ['L', n] and Branch(l,r) by the list ['B',l,r]
# We operate on these using match cases (there is no "OOP" alternative).
# Note the need for a "default" case at the end to handle the possibility
# that our trees are ill-formed. A type-checker probably complains if we don't
# provide this -- as well it should!
#

from typing import Any

type LTree = list[Any]  # lists with arbitrary contents: a very loose type! 

def showlt(t:LTree) -> str:
    """Return string representation of tree t"""
    match t:
       case ['B', l, r]: return f"({showlt(l)},{showlt(r)})"
       case ['L', v]: return str(v)
       case _: raise Exception("Invalid tree")

def sizelt(t: LTree) -> int:
    """Return number of nodes in this tree"""
    match t:
       case ['B', l, r]: return sizelt(l) + sizelt(r) + 1
       case ['L', _]: return 1
       case _: raise Exception("Invalid tree")
        
def sumlt(t: LTree) -> int :
    """Return sum of leaf values in this tree"""
    match t:
       case ['B', l, r]: return sumlt(l) + sumlt(r)
       case ['L', v]:  return v
       case _: raise Exception("Invalid tree")
       
alt : LTree = ['B', ['B', ['L', 1], ['L', 2]], \
                    ['B', ['B', ['L', 3], \
                                ['L', 4]], \
                          ['L', 5]]]
print(showlt(alt))
print(sizelt(alt))
print(sumlt(alt))

# Your task is to reimplement the swap and depth from Problem 4 
# to operate on this tree representation.

def swaplt(t: LTree) -> LTree:
    """Return copy of tree t with left and right
       branches swapped at every level"""
    ...
        

def depthlt(t:LTree) -> int:
    """Return depth of tree t"""
    ...
        
#print(showlt(swaplt(alt)))
#print(depthlt(alt))     


# Problem 6
#
# Describe some key differences between Python strings and C++ strings
# (as provided by std::string class).
#
# In particular, address these questions with respect to both languages:
#
#  1. Are strings mutable or immutable?
#  2. What is the syntax for string literals and how are new strings created from literals?
#  3. How can we append strings together?
#  4. How can we extract substrings?
#  5. How can we search for a substring?
#
# Provide code examples to illustrate your answers as appropriate.
#
# You may find it handy to use a web-based C++ engine such as https://cpp.sh/
# to test out C++ code.  The python3 top-level-loop probably suffices for
# Python experiments.
#
# This is a large subject; don't feel the need to go into elaborate detail.
# Aim for an answer of under 250 words (including code examples).
#
# Note: you can certainly get AI tools to answer this question for you, but please
# don't rely SOLELY on them. Remember that they can get things wrong!
# You should be able to explain your answers if you are asked. 
#
# Just put your answer in this large text comment block:
'''
1. Python strings are immutable, whereas instances of C++ std::string are mutable.

2. In Python, string literals are usually surrounded by single quotes ('abc') or
double quotes ("abc"). (There are several more variants for creating raw strings, formatted
strings. etc., and triple-quote format for multi-line strings.)
Each string literal mentioned in the source directly allocates a string object. 

In C++, string literals are actually arrays of the basic C/C++ char type, written
between double quotes ("abc"). To produce an instance of std::string, we must either
use a constructor, e.g. 

std::string s("abc");

or an assignment, e.g.

std::string s = "abc";

3. In Python, we use the + operator to produce a new string, e.g.

s1 = "abc"
s2 = "def"
s3 = s1 + s2  # "abcdef"

In C++, we can use the + operator in the same way, e.g.

std::string s1 = "abc";
std::string s2 = "def";
std::string s3 = s1 + s2; // "abcdef"

or we can modify an existing string:

s1.append("def")  // s1 = "abcdef"

4. In Python, we can use the slice operator to extract a substring. In simplest
form, it takes a starting index (inclusive) and ending index (exclusive), e.g.

s = 'abcdef'
s[2::4]  # 'cd'

In C++, we use a method call like substring(), which takes a starting position
and number of characters, e.g.

std::string s = "abcdef";
s.substring(2,2)  # "cd" 

5. In Python, we use the method s.find(t),  which returns the index of the
first appearance of t in s, or -1 if not found.

In C++ we use a similar find method, s.find(t), which return string::npos
(the maximum possible size of a string) if not found.  (Actually, npos = -1 !)
'''




# Week 3 Practice Exercises  (due at noon, 1/27/25)
#
# Your task is to complete the missing parts of this file.
# There are four problems.
#
# The file test3.py contains a test driver for all the python
# problems in this assignment.  You can run it just using
# python3 test3.py
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
# Do not submit any other files.  There's no need to pu your
# name in the source code; Canvas will tell us which submission is yours.
# MAKE SURE TO CLICK THE SUBMIT BUTTON; the submission isn't registered
# until then.  You can resubmit as many times as you like up
# until the deadline; we'll only look at the last submission.

# COMPILATION
#
# This week's problems have to do with compilation, i.e. the translation
# of source expressions into another language for which we already
# have an execution engine.   While we won't study compilation in
# detail in this course, these exercises should help you get a basic
# feel for the difference between interpretation and compilation,
# and some of the intermediate possiblities that combine both.
#
# Our target language will be a simple stack-machine with a byte
# code instruction set. We can think of this as either a simple
# example of a _machine_, similar to a real processor, but
# stripped down to avoid the complexities of things like
# memory and registers.

# Alternatively, we can think of this as an _intermediate language_
# in an interpreter pipeline: rather than
# interpreting the source AST directly, we first translate it
# to byte code and then interpret that.  Many real-world "interpreters"
# actually do this, because byte code is often simpler and faster
# to interpret than the AST.  Hence they are really combining
# a mini-compiler and an interpreter into one engine.
#
#
# We will study a very simpler translator to stack machine byte code
# from arithmetic expressions with let bindings and variables, and
# also conditionals.

# SOURCE: EXPRESSIONS

from dataclasses import dataclass

type Expr = Add | Sub | Mul | Lit | Let | Name | Ifnz

# Most of these classes are the same as in interp_arith.py

@dataclass
class Add():
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} + {self.right})"
    
@dataclass
class Sub():
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} - {self.right})"

@dataclass
class Mul():
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} * {self.right})"


@dataclass
class Lit():
    value: int
    def __str__(self) -> str:
        return f"{self.value}"

@dataclass
class Let():
    name: str
    defexpr: Expr
    bodyexpr: Expr
    def __str__(self) -> str:
        return f"(let {self.name} = {self.defexpr} in {self.bodyexpr})"

@dataclass
class Name():
    name:str
    def __str__(self) -> str:
        return self.name

# New class for conditional expressions.
# Since we have no Booleans, we test an integer value directly; Ifnz stands for "if not zero"
@dataclass
class Ifnz():
    cond: Expr
    thenexpr: Expr
    elseexpr: Expr
    def __str__(self) -> str:
        return f"(if {self.cond} != 0 then {self.thenexpr} else {self.elseexpr})"
   


# Here are some example expressions to test the compiler
a : Expr = Mul(Add(Lit(1), Lit(2)), 
               Add(Lit(3), Lit(4)))

b : Expr = Ifnz(Add(Lit(1), Lit(1)), 
                Lit(2), 
                Lit(3))

c : Expr = Sub(Lit(1), Lit(2))

d : Expr = Ifnz(Sub(Lit(1), Lit(1)), 
                Lit(2), 
                Lit(3))

e : Expr = Let('x', Add(Lit(1), Lit(2)), 
                    Mul(Name('x'), Lit(3)))

f : Expr = Let('x', Lit(1), 
                    Add(Let('x', Lit(2), 
                             Mul(Name('x'), Lit(3))),
                        Name('x')))

g : Expr = Let('x', Lit(1), 
                    Add(Let('x', Lit(2), 
                             Mul(Lit(3),Name('x'))),
                        Name('x')))

# TARGET: STACK MACHINE BYTE CODE
#
# Our goal in this exercise is to compile expressions to stack machine byte code.
# A stack machine is a simple form of computer that uses a stack to hold intermediate
# results of computations.  Real hardware seldom directly implements a stack machine, 
# but it is commonly used as a virtual machine (i.e. a software abstraction that can
# be interpreted by a real computer) or as an intermediate form in a compiler.
# The main characteristic of a stack machine is that all operations are performed
# on values at the top of the stack, rather than using registers or memory addresses.
# Stack machine programs for arithmetic expressions look like RPN (Reverse Polish Notation)
# which may be familiar to you from some old-fashioned calculators.
# Here is the definition of the stack machine instruction set

type Instr = Push | Plus | Times | Dup | Swap | Pop | Brnz | Label

@dataclass
class Push():
    '''Push the specified value onto the stack'''
    value: int
    def __str__(self) -> str:
        return f"push {self.value}"
    
@dataclass
class Plus():
    '''Pop two values from the stack, add them, and push the result'''
    def __str__(self) -> str:
        return "plus"
    
@dataclass
class Times():
    '''Pop two values from the stack, multiply them, and push the result'''
    def __str__(self) -> str:
        return "times"
    
@dataclass
class Dup():
    '''Push a duplicate of the value at the specified index on the stack, counting the top of stack as 0'''
    index: int
    def __str__(self) -> str:
        return f"dup {self.index}"
    
@dataclass  
class Swap():
    '''Swap the top two values on the stack'''
    def __str__(self) -> str:
        return "swap"
    
@dataclass
class Pop():
    '''Pop the top value from the stack'''
    def __str__(self) -> str:
        return "pop"

@dataclass
class Brnz():
    '''Pop the top value from the stack and branch to the specified label if it is not zero'''
    label: str
    def __str__(self) -> str:
        return f"brnz {self.label}"
    
@dataclass
class Label():
    '''Define a label as a target for a branching instruction'''
    label: str
    def __str__(self) -> str:
        return f"{self.label}:"
    
from typing import Sequence

def strSequence[T](xs: Sequence[T]) -> str:
    '''Convert stack machine program to printable string'''
    # only needed because Python str() invokes repr() (not str()) on sequence elements
    return "[" + ", ".join(str(x) for x in xs) + "]"


# EXECUTING STACK MACHINE CODE
#
# We will use a simple stack machine interpreter to execute the compiled code
# This interpreter is similar to our expression interpreters, but it does not
# need to be recursive (since stack machine code is a linear sequence).

def exec(instrs: Sequence[Instr]) -> int:
    '''Execute a stack machine program and return the result'''
    stack : list[int] = []  # top of stack is at the right
    pc = 0                  # program counter: index into list of instructions
    while pc < len(instrs): # repeat until pc reaches end of instruction list
        instr = instrs[pc]  # fetch the current instruction
        match instr:
            case Push(value):
                stack.append(value)
            case Plus():
                stack.append(stack.pop() + stack.pop())
            case Times():
                stack.append(stack.pop() * stack.pop())
            case Dup(index): # index is distance from top of stack
                stack.append(stack[-(index+1)])
            case Swap():    # swap top two elements of stack
                stack[-1], stack[-2] = stack[-2], stack[-1]                                
            case Pop():
                stack.pop()
            case Brnz(label):
                if stack.pop() != 0:                # jump if top of stack is not zero
                    pc = instrs.index(Label(label)) # find the label in the instruction list
                # otherwise fall through to next instruction
            case Label(label):
                pass        # executing a label doesn't do anything                
        pc += 1             # move to next instruction  
    return stack[0]         # return the top of stack as the result  


# COMPILATION FROM EXPRESSIONS TO STACK MACHINE CODE

# First we consider a simplified version of the compiler that does not support
# let bindings or variables (or, temporarily, Subtraction).

class CompilerError(Exception):
    pass

def scompile(e: Expr) -> list[Instr]:
    instrs : list[Instr] = []
    labelCounter: int = 0
    def newLabel() -> str:
        nonlocal labelCounter
        label = f"L{labelCounter}"
        labelCounter += 1
        return label

    def gen(e: Expr) -> None:
        match e:
            case Add(left, right):
                gen(left)
                gen(right)
                instrs.append(Plus())
            case Mul(left, right):
                gen(left)
                gen(right)
                instrs.append(Times())
            case Sub(left, right):
                gen(left)
                gen(Mul(Lit(-1), right))
                instrs.append(Plus())
            case Lit(value):
                instrs.append(Push(value))
            case Let(_,_,_):
                raise CompilerError("let expressions not supported")
            case Name(_):
                raise CompilerError("variable references not supported")
            case Ifnz(cond, thenexpr, elseexpr):
                thenLabel = newLabel()
                joinLabel = newLabel()
                gen(cond)
                instrs.append(Brnz(thenLabel))
                gen(elseexpr)
                instrs.append(Push(1))  # synthesize an unconditional branch to joinLabel
                instrs.append(Brnz(joinLabel))
                instrs.append(Label(thenLabel))
                gen(thenexpr)
                instrs.append(Label(joinLabel))        
    gen(e)
    return instrs

# EXECUTION PIPELINE: COMPILE AND THEN INTERPRET THE RESULTING CODE

def srun(e: Expr) -> None:
    '''Compile an expression to bytecode and then execute that code to obtain a value'''
    print(f"compiling: {e}")
    try:
        p = scompile(e)
        print(f"executing: {strSequence(p)}")        
        i = exec(p)
        print(f"result: {i}")
    except CompilerError as err:
        print("Compiler error:", err)

srun(a)
srun(b)
srun(c)
srun(d)

# PROBLEM 1
# 
# Consider the expression concretely written as 
#
# (2 * (if (0 + 0) != 0 then 2 else 3))
# 
# Write the constructor expression (of type Expr) 
# that pretty-prints to that concrete expression.
# (i.e. the expression s such that print(s) gives
# the concrete expression above). 

p1 = Mul(Lit(2), Ifnz(Add(Lit(0), Lit(0)), Lit(2), Lit(3)))
print("----------------------------")
print(p1)
print(scompile(p1))
print("----------------------------")

# 
# Then show the bytecode generated by scompile on that Expr.
# Demonstrate that you understand how this code works by
# annotating each instruction with its purpose, and
# showing the stack contents at each step.
# Write your solution in the following block comment. 
#
'''
[Push(value=2), #Push literal value 2 onto the stack, stack: 2
 Push(value=0), #Push literal value 0 onto the stack, stack: 0,2
 Push(value=0), #Push literal value 0 onto the stack, stack: 0,0,2
 Plus(), #Add the last two items from the stack, popping them and pushing the result, stack: 0,2
 Brnz(label='L0'), #Pop the top value of the stack and label next item L0, stack: 2
 Push(value=3), #Push literal value 3 onto the stack, stack: 3,2
 Push(value=1), #Push literal value 1 onto the stack, stack: 1,3,2
 Brnz(label='L1'), #Pop top value of the stack and branch to L0, stack: 2
 Label(label='L0'), #Do nothing, move to next instruction, stack: 2
 Push(value=2), #Push literal value 2 onto the stack, stack: 2,2
 Label(label='L1'), #Do nothing, move to next instruction. stack: 2,2
 Times() #Multiply top two items on the stack, popping them and pushing the result, stack:4
'''

# PROBLEM 2
#
# Fill in the missing case for Subtraction in the code of scompile, above.
# Note: you must NOT add any new instructions to the stack machine,
# but instead figure out how to use the existing instructions
# to implement subtraction. (Hint: Literals can be negative.)
# Test your implementation.

# COMPILATION AGAIN WITH LETS AND NAMES
#
# For the remainder of this file, we will consider a more complete version of the compiler
# that also handles Lets and Names. The idea is that variables can live on the stack, since
# they are only in scope while evaluating a subexpression.  As we compile, we use an
# environment to keep track of the stack depth of each variable.  When we compile a Let
# expression, we remember the stack depth of the value of the definition.
# When we compile a Name expression, we look up its variable's depth and calculate
# the corresponding index into the current stack. As usual, we need to make sure we
# do the right thing when the same variable is bound multiple times in a nested scope.

# Environment support is just as in previous files 
type Binding[V] = tuple[str,V]  # this tuple type is always a pair
type Env[V] = tuple[Binding[V], ...] # this tuple type has arbitrary length 
from typing import Any
emptyEnv : Env[Any] = ()  # the empty environment has no bindings
def extendEnv[V](name: str, value: V, env:Env[V]) -> Env[V]:
    '''Return a new environment that extends the input environment env with a new binding from name to value'''
    return ((name,value),) + env
def lookupEnv[V](name: str, env: Env[V]) -> (V | None) :
    '''Return the first value bound to name in the input environment env
       (or raise an exception if there is no such binding)'''
    try:
        return next(v for (n,v) in env if n == name)   # use handy generator expression to search for name
    except StopIteration:
        return None

# Here is the full compiler
def compile(e: Expr) -> list[Instr]:
    instrs : list[Instr] = []
    labelCounter: int = 0
    def newLabel() -> str:
        nonlocal labelCounter
        label = f"L{labelCounter}"
        labelCounter += 1
        return label
    def gen(e: Expr, depth:int, vars: Env[int]) -> None:
        match e:
            case Add(left, right):
                gen(left, depth, vars)
                gen(right, depth+1, vars)
                instrs.append(Plus())
            case Mul(left, right):
                gen(left, depth, vars)
                gen(right, depth+1, vars)
                instrs.append(Times())
            case Sub(left, right):
                raise CompilerError("subtraction not supported")
            case Lit(value):
                instrs.append(Push(value))
            case Let(name, defexpr, bodyexpr):
                gen(defexpr, depth, vars)
                newEnv = extendEnv(name, depth+1, vars) # remember stack depth of value of defexpr for variable
                gen(bodyexpr, depth+1, newEnv)
                instrs.append(Swap()) # move value of defexpr to top of stack
                instrs.append(Pop())  # and get rid of it, leaving value of bodyexpr on top
            case Name(name):
                varDepth = lookupEnv(name, vars)  # get stack depth of variable
                if varDepth is None:
                    raise CompilerError(f"undefined variable: {name}")
                instrs.append(Dup(depth-varDepth)) # calculate offset to variable on stack and fetch its value
            case Ifnz(cond, thenexpr, elseexpr):
                thenLabel = newLabel()
                joinLabel = newLabel()
                gen(cond, depth, vars)
                instrs.append(Brnz(thenLabel))
                gen(elseexpr, depth, vars)
                instrs.append(Push(1))  # synthesize an unconditional branch
                instrs.append(Brnz(joinLabel))
                instrs.append(Label(thenLabel))
                gen(thenexpr, depth, vars)
                instrs.append(Label(joinLabel))        
    gen(e, 0, emptyEnv)
    return instrs


def run(e: Expr) -> None:
    '''Compile an expression to bytecode and then execute that code to obtain a value'''
    print(f"compiling: {e}")
    try:
        p = compile(e)
        print(f"executing: {strSequence(p)}")        
        i = exec(p)
        print(f"result: {i}")
    except CompilerError as err:
        print("Compiler error:", err)

run(a)
run(b)
run(c)
run(d)
run(e)
run(f)
run(g)

# PROBLEM 3
#
# This problem is to test your understanding of how the extended compiler works.
# Each use of a variable induces a DUP(n) instruction in the compiled code, where
# n is the difference in stack depth between the variable and the current top of stack.
# Write down a source expression tree which generates code that contains a DUP(4)
# instruction. For added insight, see if you can find such an expression that
# contains only one LET binding. In general, what can make n get large?

p3 = Let('x', Lit(5), Add(Lit(2), Add(Lit(2), Add(Lit(2), Add(Lit(2), Name('x'))))))

# (Add any observations about how to make n large here.)
# N gets large by nesting expressions more and more within a body expression

# PROBLEM 4  (Analysis)
#
# C++ and Python typically use different implementation strategies.

# (a) Give one or more reasons why C++ is typically compiled whereas
# Python is typically interpreted. 

# (b) Clang is one typical C++ compiler, which is used on unix-based systems.
# CPython is the original and de facto standard Python interpreter.
# Briefly contrast the internal structure of these two systems, 
# identifying any important intermediate languages or processing stages. 

# You'll need to do some research to answer this question.
# Write your solution in the following block comment. Aim for about 250 words.
'''
(a) I think that C++ is typically compiled because it's easier to optimize for better performance. People tend to use C++ because 
    it is extremely fast compared to other languages. It would be much harder to optimize if there were no compiler to optimize the
    user-written code. Python on the other hand is often interpreted because people tend to use it as a scripting language. People
    want to be able to open an editor and start running python code as easily as possible, and an interpreter makes it so that you 
    don't have to recompile everytime you want to execute your code

(b) Like most compilers, Clang is split up into three phases: The frontend that parses the source code and builds language-specific 
    ASTS, the optimizer, where the AST generated by the frontend is optimized for better performance, and the backend, where the 
    final bytecode is generated to be executed by the machine. Clang uses LLVM intermediate representation, which is a powerful l
    anguage-agnostic code representation that is optimized and transformed before being translated into machine code by the backend. 
    The output is a binary executable that can run on a target machine

    Cpython works by compiling the source code into bytcode, then interpreting that bytecode at runtime. 
    
    The compilation stage is split up into 5 stepes:

    1. Tokenize the source code
    2. Parse the stream of tokens into an AST
    3. Transform the AST into an instruction sequence
    4. Contruct a Control Flow Graph and apply optimizations to it
    5. Emit bytecode based on the Control Flow Graph

    Once the bytecode has been generated, the bytecode intepreter decodes and evaluates the instructions.
    The decoding is done by looping over the instructions, decoding each into it's opcode and oparg, and
    then executing the switch case that implements the opcode

    The evaluation is implemented via a stack machine. Instructions operate by pushing data onto and popping
    if off the stack. At any point during execution, the stack level is knowable based on the instruction pointer alone
'''

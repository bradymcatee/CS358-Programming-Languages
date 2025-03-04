# A simple interpreter for arithmetic expressions with let bindings
# now including integer division.

from dataclasses import dataclass

type Program = Block
type Decl = VarDecl
type Stmt = Block | Assign | Ifnz | Whilenz| Print 
type Expr = Add | Sub | Mul | Div | Neg | Lit | Name

@dataclass
class Block():
    decls: list[Decl]
    stmts: list[Stmt]
    def __str__(self) -> str:
        return "{" + "; ".join([str(s) for s in self.decls + self.stmts]) + "}"
    
@dataclass
class VarDecl():
    name: str
    expr: Expr
    def __str__(self) -> str:
        return f"var {self.name} := {self.expr}"
    
@dataclass
class Assign():
    name: str
    expr: Expr
    def __str__(self) -> str:
        return f"{self.name} := {self.expr}"

@dataclass
class Ifnz():
    cond: Expr
    then: Stmt
    else_: Stmt
    def __str__(self) -> str:
        return f"ifnz {self.cond} then {self.then} else {self.else_}"        
    
@dataclass
class Whilenz():
    cond: Expr
    body: Stmt
    def __str__(self) -> str:
        return f"whilenz {self.cond} do {self.body}"
    
@dataclass
class Print():
    expr: Expr
    def __str__(self) -> str:
        return f"print {self.expr}"
    

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
class Div():
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} / {self.right})"

@dataclass
class Neg():
    subexpr: Expr
    def __str__(self) -> str:
        return f"(- {self.subexpr})"

@dataclass
class Lit():
    value: int
    def __str__(self) -> str:
        return f"{self.value}"

@dataclass
class Name():
    name:str
    def __str__(self) -> str:
        return self.name



type Binding[V] = tuple[str,V]  # this tuple type is always a pair
type Env[V] = tuple[Binding[V], ...] # this tuple type has arbitrary length 

from typing import Any
emptyEnv : Env[Any] = ()  # the empty environment has no bindings

def extendEnv[V](name: str, value: V, env:Env[V]) -> Env[V]:
    '''Return a new environment that extends the input environment 
       env with a new binding from name to value'''
    return ((name,value),) + env

def lookupEnv[V](name: str, env: Env[V]) -> (V | None) :
    '''Return the first value bound to name in the input environment env
       (or raise an exception if there is no such binding)'''
    # exercises2b.py shows a different implementation alternative
    match env:
        case ((n,v), *rest) :
            if n == name:
                return v
            else:
                return lookupEnv(name, rest) # type:ignore
        case _ :
            return None        

# model memory locations as (mutable) singleton lists
type Loc[V] = list[V] # always a singleton list
def newLoc[V](value: V) -> Loc[V]:
    return [value]
def getLoc[V](loc: Loc[V]) -> V:
    return loc[0]
def setLoc[V](loc: Loc[V], value: V) -> None:
    loc[0] = value
        
class EvalError(Exception):
    pass

def eval(e: Expr) -> int :
    return evalInEnv(emptyEnv, e)

def evalInEnv(env: Env[Loc[int]], e:Expr) -> int:
    match e:
        case Add(l,r):
            return evalInEnv(env,l) + evalInEnv(env,r)
        case Sub(l,r):
            return evalInEnv(env,l) - evalInEnv(env,r)
        case Mul(l,r):
            lv = evalInEnv(env,l)
            rv = evalInEnv(env,r)
            return lv * rv
        case Div(l,r):
            lv = evalInEnv(env,l)
            rv = evalInEnv(env,r)
            if rv == 0:
                raise EvalError("division by zero")
            return lv // rv
        case Neg(s):
            return - (evalInEnv(env,s))
        case Lit(i):
            return i
        case Name(n):
            l = lookupEnv(n, env)
            if l is None:
                raise EvalError(f"unbound name {n}")
            return getLoc(l)

def execute(s: Stmt) -> None:
    executeInEnv(emptyEnv, s)   

def executeInEnv(env: Env[Loc[int]], s: Stmt) -> None:
    match s:
        case Block(ds,ss):
            for d in ds:
                match d:
                    case VarDecl(n, e):
                        v = evalInEnv(env, e)
                        l = newLoc(v)
                        env = extendEnv(n, l, env)
            for s in ss:
                executeInEnv(env, s)
        case Assign(n, e):
            l = lookupEnv(n, env)
            if l is None:
                raise EvalError(f"unbound name {n}")
            v = evalInEnv(env, e)
            setLoc(l,v)
        case Ifnz(c, t, e):
            if evalInEnv(env, c) != 0:
                executeInEnv(env, t)
            else:
                executeInEnv(env, e)
        case Whilenz(c, b):
            while evalInEnv(env, c) != 0:
                executeInEnv(env, b)
        case Print(e):
            print(evalInEnv(env, e))

def run(p: Program) -> None:
    print(f"running: {p}")
    try:
        execute(p)
    except EvalError as err:
        print(err)


# Extra Packages:
# Name: pillow
# Version: 11.1.0

from dataclasses import dataclass
from PIL import Image
from typing import Callable

@dataclass
class ImgPath():
    path: str
    def __str__(self) -> str:
        return self.path

type Literal = int | bool | ImgPath

type Expr = Add | Sub | Mul | Div | Neg | And | Or | Not | Let | Name | Eq | Lt | If | StitchHorizontal | Rotate90

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
    value: Literal
    def __str__(self) -> str:
        return f"{self.value}"
@dataclass
class Or():
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} or {self.right})"

@dataclass
class And():
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} and {self.right})"

@dataclass
class Not():
    subexpr: Expr
    def __str__(self) -> str:
        return f"(not {self.subexpr})"

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

@dataclass
class Eq():
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"{self.left} == {self.right}"
@dataclass
class Lt():
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"{self.left} < {self.right}"

@dataclass
class If():
    cond: Expr
    thenexpr: Expr
    elseexpr: Expr
    def __str__(self) -> str:
        return f"if {self.cond} then {self.thenexpr} else {self.elseexpr}"

@dataclass
class StitchHorizontal():
    first: ImgPath
    second: ImgPath
    def __str__(self) -> str:
        return f"{self.first} stitched horizontal with {self.second}"

@dataclass
class Rotate90():
    image: ImgPath
    def __str__(self) -> str:
        return f"{self.image} rotated 90 clockwise"

@dataclass
class LetFun():
    fname: str         
    param: str         
    body: Expr        
    inexp: Expr      
    def __str__(self) -> str:
        return f"(letfun {self.fname}({self.param}) = {self.body} in {self.inexp})"

@dataclass
class App():
    funexpr: Expr   
    arg: Expr      
    def __str__(self) -> str:
        return f"{self.funexpr}({self.arg})"


type Binding[V] = tuple[str,V]  # this tuple type is always a pair
type Env[V] = tuple[Binding[V], ...] # this tuple type has arbitrary length 

type Value = int | ImgPath | bool

@dataclass
class Closure():
    param: str    
    body: Expr   
    env: Env[Value] 
    def __str__(self) -> str:
        return "<function>"

from typing import Any
emptyEnv : Env[Any] = ()  # the empty environment has no bindings

def extendEnv[V](name: str, value: V, env:Env[V]) -> Env[V]:
    '''Return a new environment that extends the input environment env with a new binding from name to value'''
    return ((name,value),) + env

def lookupEnv[V](name: str, env: Env[V]) -> (V | None) :
    '''Return the first value bound to name in the input environment env
       (or raise an exception if there is no such binding)'''
    match env:
        case ((n,v), *rest) :
            if n == name:
                return v
            else:
                return lookupEnv(name, rest) # type:ignore
        case _ :
            return None        
        
class EvalError(Exception):
    pass

def merge(im1: Image.Image, im2: Image.Image) -> Image.Image:
    '''merge function for Pillow images'''
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGB", (w, h))

    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))

    return im

def eval(e: Expr) -> Value :
    return evalInEnv(emptyEnv, e)

def evalInEnv(env: Env[Value], e:Expr) -> Value:
    match e:
        case Add(l,r):
            match (evalInEnv(env,l), evalInEnv(env,r)):
                case (int(lv), int(rv)):
                    if isinstance(lv, bool) | isinstance(rv, bool):
                        raise EvalError("addition of booleans")
                    return lv + rv
                case _:
                    raise EvalError("addition of non-integers")
        case Sub(l,r):
            match (evalInEnv(env,l), evalInEnv(env,r)):
                case (int(lv), int(rv)):
                    if isinstance(lv, bool) | isinstance(rv, bool):
                        raise EvalError("subtraction of booleans")
                    return lv - rv
                case _:
                    raise EvalError("subtraction of non-integers")
        case Mul(l,r):
            match (evalInEnv(env,l), evalInEnv(env,r)):
                case (int(lv), int(rv)):
                    if isinstance(lv, bool) | isinstance(rv, bool):
                        raise EvalError("multiplication of booleans")
                    return lv * rv
                case _:
                    raise EvalError("multiplication of non-integers")
        case Div(l,r):
            match (evalInEnv(env,l), evalInEnv(env,r)):
                case (int(lv), int(rv)):
                    if isinstance(lv, bool) | isinstance(rv, bool):
                        raise EvalError("division of booleans")
                    if rv == 0:
                        raise EvalError("division by zero")
                    return lv // rv
                case _:
                    raise EvalError("division of non-integers")                
        case Neg(s):
            match evalInEnv(env,s):
                case int(i):
                    if isinstance(i, bool):
                        raise EvalError("negation of boolean")
                    return -i
                case _:
                    raise EvalError("negation of non-integer")
        case(Lit(lit)):
            match lit:  # two-level matching keeps type-checker happy
                case int(i):
                    return i
                case ImgPath(_) as a:
                    return ImgPath(a)
                case _:
                    raise EvalError("non-supported literal")
        case Name(n):
            v = lookupEnv(n, env)
            if v is None:
                raise EvalError(f"unbound name {n}")
            return v
        case Let(n,d,b):
            v = evalInEnv(env, d)
            newEnv = extendEnv(n, v, env)
            return evalInEnv(newEnv, b)
        case Or(l,r):
            match (evalInEnv(env, l), r):
                case(bool(lv), r):
                    if lv == True:
                        return lv
                    else:
                        match (evalInEnv(env, r)):
                            case bool(rv):
                                return rv
                            case _:
                                raise EvalError("or of non-boolean")
                case (l, bool(rv)):
                    if rv == True:
                        return rv
                    else:
                        match(evalInEnv(env, l)):
                            case bool(lv):
                                return lv
                            case _:
                                raise EvalError("or of non-boolean")
                case _:
                    raise EvalError("or of non-boolean") 
        case And(l,r):
            match (evalInEnv(env, l), r):
                case (bool(lv), r):
                    if lv == False:
                        return lv
                    else:
                        match(evalInEnv(env, r)):
                            case bool(rv):
                                return rv
                            case _:
                                raise EvalError("and of non-boolean")
                case (l, bool(rv)):
                    if rv == False:
                        return rv
                    else:
                        match(evalInEnv(env ,l)):
                            case bool(lv):
                                return lv
                            case _:
                                raise EvalError("and of non-boolean") 
                case _:
                    raise EvalError("and of non-boolean") 
        case Not(b):
            match evalInEnv(env,b):
                case bool(v):
                    return not v
                case _:
                    raise EvalError("not of non-boolean")
        case Eq(l,r):
            match(evalInEnv(env, l), evalInEnv(env,r)):
                case ImgPath(lv), ImgPath(rv):
                    return lv.path == rv.path
                case bool(lv), bool(rv):
                    return lv == rv
                case int(lv), int(rv):
                    if isinstance(lv, bool) | isinstance(rv, bool):
                        raise EvalError("equality of mismatched types")
                    return lv == rv
                case _:
                    raise EvalError("Equality of non-supported type")
        case Lt(l,r):
            match(evalInEnv(env, l), evalInEnv(env,r)):
                case int(lv), int(rv):
                    if isinstance(lv, bool) | isinstance(rv, bool):
                        raise EvalError("less than of booleans")
                    return lv < rv
                case _:
                    raise EvalError("less than of non-integer")
        case If(b,t,e):
            match(evalInEnv(env, b)):
                case bool(b):
                    if b:
                        return evalInEnv(env, t)
                    else:
                        return evalInEnv(env, e)
                case _:
                    raise EvalError("Condition not a boolean value")

        case StitchHorizontal(l,r):
            match (evalInEnv(env, l), evalInEnv(env, r)):
                case ImgPath(lp), ImgPath(rp):
                    try:
                        im_l = Image.open(lp.path)
                        im_r = Image.open(rp.path)
                    except:
                        raise ValueError("Image path not found, couldn't open")
                    merged_img = merge(im_l, im_r)
                    outfile = "result_stitch.jpg"
                    merged_img.save(outfile)
                    return ImgPath(outfile)
                case _:
                    raise EvalError("Cannot stitch non-images")
        case Rotate90(i):
            match (evalInEnv(env, i)):
                case ImgPath(i):
                    try:
                        img = Image.open(i.path)
                    except:
                        raise ValueError("Image path not found")
                    out = img.rotate(270)
                    outfile = "result_rotate.jpg"
                    out.save(outfile)
                    return ImgPath(outfile)
        case LetFun(fname, param, body, inexp):
            # Create closure capturing current environment
            closure = Closure(param, body, env)
            # Extend environment with function binding
            newEnv = extendEnv(fname, closure, env)
            # Evaluate the body expression in new environment
            return evalInEnv(newEnv, inexp)
            
        case App(funexpr, arg):
            # Evaluate function expression to get closure
            match evalInEnv(env, funexpr):
                case Closure(param, body, closure_env):
                    # Evaluate argument
                    arg_val = evalInEnv(env, arg)
                    # Create new environment extending closure's env
                    call_env = extendEnv(param, arg_val, closure_env)
                    # Evaluate function body in new environment
                    return evalInEnv(call_env, body)
                case _:
                    raise EvalError("Trying to apply a non-function")

# Add to your run function's match:
        case Closure(_):
            print("result <function>")

def run(e: Expr) -> None:
    print(f"running {e}")
    try:
        match eval(e):
            case int(i):
                print(f"result {i}")
            case bool(b):
                print(f"result {b}")
            case ImgPath(a):
                img = Image.open(a)
                img.show()
    except EvalError as err:
        print(err)

a : Expr = Let('x', Add(Lit(1), Lit(2)), 
                    Sub(Name('x'), Lit(3)))

b : Expr = Let('x', Lit(1),
                    Let('x', Lit(2), 
                             Mul(Name('x'), Lit(3))))

c : Expr = Add(Let('x', Lit(1), 
                        Sub(Name('x'), Lit(2))),
               Mul(Name('x'), Lit(3)))

d : Expr = Add(Lit(1), Div(Lit(2), Lit(0)))

f : Expr =  Let('x', Lit(2), 
                  If(Eq(Name('x'), Lit(5)), Add(Name('x'), Lit(5)), Sub(Lit(8), Name('x'))))

g : Expr = StitchHorizontal(Lit(ImgPath("hopper.jpg")), Lit(ImgPath("hopper.jpg")))

h : Expr = Rotate90(Lit(ImgPath("hopper.jpg")))

run(a)
run(b)
run(c)

run(d)
run(f)
run(g)
run(h)

'''
I decided to implement the "Images" DSL for this project 

The domain-specific features that I've implemented so far are the StitchHorizontal and Rotate90 functions

These allow a user to provide a ImgPath literal that contains the path to the image they want to manipulate

The result of the image manipulation is stored as a jpg in the users current working directory and is automatically opened after evaluation
'''
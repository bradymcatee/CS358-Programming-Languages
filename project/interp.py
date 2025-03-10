# Extra Packages:
# Name: pillow
# Version: 11.1.0

from dataclasses import dataclass
from PIL import Image
from typing import Callable
import sys

@dataclass
class ImgPath():
    path: str
    def __str__(self) -> str:
        return self.path

type Literal = int | bool | ImgPath

type Expr = Add | Sub | Mul | Div | Neg | And | Or | Not | Let | Name | Eq | Lt | If | Assign | Seq | Show | Read | Letfun | StitchHorizontal | Rotate90 | Filter | Collage

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
class Letfun():
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

@dataclass
class Assign():
    name: str
    expr: Expr
    def __str__(self) -> str:
        return f"{self.name} := {self.expr}"

@dataclass
class Seq():
    expr1: Expr
    expr2: Expr
    def __str__(self) -> str:
        return f"({self.expr1}; {self.expr2})"
@dataclass
class Show():
    expr: Expr
    def __str__(self) -> str:
        return f"Showing {self.expr}"

@dataclass
class Read():
    def __str__(self) -> str:
        return "read"
@dataclass
class Filter():
    color: str
    img: ImgPath
    def __str__(self) -> str:
        return f"Apply {self.color} filter to {self.img}"
@dataclass
class Collage():
    images: list[Expr]
    rows: Expr
    cols: Expr
    def __str__(self) -> str:
        return f"Collage of {len(self.images)} images in {self.rows}x{self.cols} grid"

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
            return getLoc(v)
        case Let(n,d,b):
            v = evalInEnv(env, d)
            l = newLoc(v)
            newEnv = extendEnv(n, l, env)
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

        case Filter(color, img_expr):
            match evalInEnv(env, img_expr):
                case ImgPath(path):
                    try:
                        img = Image.open(path.path)
                    except:
                        raise ValueError(f"Image path not found {path.path}")
                    if color == "red":
                        r, g, b = img.split()
                        img = Image.merge("RGB", (r, Image.new('L', img.size, 0), Image.new('L', img.size, 0)))
                    elif color == "green":
                        r, g, b = img.split()
                        img = Image.merge("RGB", (Image.new('L', img.size, 0), g, Image.new('L', img.size, 0)))
                    elif color == "blue":
                        # Keep only blue channel
                        r, g, b = img.split()
                        img = Image.merge("RGB", (Image.new('L', img.size, 0), Image.new('L', img.size, 0), b))
                    elif color == "grayscale":
                        # Convert to grayscale
                        img = img.convert("L").convert("RGB")
                    elif color == "sepia":
                        # Apply sepia filter
                        img = img.convert("L")
                        img = Image.merge("RGB", 
                            (
                                img.point(lambda p: p * 1.08),
                                img.point(lambda p: p * 0.82), 
                                img.point(lambda p: p * 0.6)
                            )
                        )
                    else:
                        raise EvalError(f"Unknown filter type: {color}")
                    
                    # Save the filtered image
                    outfile = f"result_filter_{color}.jpg"
                    img.save(outfile)
                    return ImgPath(outfile)
                case _:
                    raise EvalError("Cannot apply filter to non-image")

        case Collage(image_exprs, rows_expr, cols_expr):
            # Evaluate all image expressions
            rows_val = evalInEnv(env, rows_expr)
            cols_val = evalInEnv(env, cols_expr)
            if not isinstance(rows_val, int) or not isinstance(cols_val, int):
                raise EvalError("Rows and columns for collage must be integers")
            images = []
            for img_expr in image_exprs:
                match evalInEnv(env, img_expr):
                    case ImgPath(path):
                        try:
                            img = Image.open(path.path)
                            images.append(img)
                        except:
                            raise ValueError(f"Image path not found: {path.path}")
                    case _:
                        raise EvalError("Collage can only contain images")
            
            # Calculate the size of the collage
            if len(images) == 0:
                raise EvalError("Cannot create an empty collage")
            
            # Determine the size of each cell based on the largest image
            max_width = max(img.width for img in images)
            max_height = max(img.height for img in images)
            
            # Create a new blank image for the collage
            collage_width = max_width * cols_val
            collage_height = max_height * rows_val
            collage = Image.new("RGB", (collage_width, collage_height), (255, 255, 255))
            
            # Place each image in the grid
            for i, img in enumerate(images):
                if i >= rows_val * cols_val:
                    break  # Don't exceed the grid size
                
                # Calculate position in the grid
                row = i // cols_val
                col = i % cols_val
                
                # Calculate position in pixels
                x = col * max_width
                y = row * max_height
                
                # Resize image to fit cell if needed
                if img.width != max_width or img.height != max_height:
                    # Resize proportionally to fit within the cell
                    img.thumbnail((max_width, max_height), Image.LANCZOS)
                
                # Calculate centering offsets
                x_offset = (max_width - img.width) // 2
                y_offset = (max_height - img.height) // 2
                
                # Paste the image
                collage.paste(img, (x + x_offset, y + y_offset))
            
            # Save the collage
            outfile = "result_collage.jpg"
            collage.save(outfile)
            return ImgPath(outfile)

        case Letfun(fname, param, body, inexp):
            closure = Closure(param, body, env)
            l = newLoc(closure)
            newEnv = extendEnv(fname, l, env)
            return evalInEnv(newEnv, inexp)
            
        case App(funexpr, arg):
            match evalInEnv(env, funexpr):
                case Closure(param, body, closure_env):
                    arg_val = evalInEnv(env, arg)
                    l = newLoc(arg_val)
                    call_env = extendEnv(param, l, closure_env)
                    return evalInEnv(call_env, body)
                case _:
                    raise EvalError("Trying to apply a non-function")
        case Assign(n, e):
            l = lookupEnv(n, env)
            if l is None:
                raise EvalError(f"unbound name {n}")
            if isinstance(getLoc(l), Closure):
                raise EvalError(f"cannot assign to function {n}")
            v = evalInEnv(env, e)
            setLoc(l,v)
            return v

        case Seq(f, s):
            evalInEnv(env, f)
            return evalInEnv(env ,s)

        case Show(e):
            v = evalInEnv(env, e)
            try:
                match v:
                    case int(i):
                        print(f"result {i}")
                    case bool(b):
                        print(f"result {b}")
                    case ImgPath(a):
                        img = Image.open(a)
                        img.show()
            except EvalError as err:
                print(err)
            return v

        case Read():
            try:
                user_input = input("Enter an integer: ")
                val = int(user_input)
                return val
            except ValueError:
                raise EvalError("Input is not a valid integer")

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

'''
I decided to implement the "Images" DSL for this project 

The domain-specific features that I've implemented so far are the StitchHorizontal and Rotate90 functions

These allow a user to provide a ImgPath literal that contains the path to the image they want to manipulate

The result of the image manipulation is stored as a jpg in the users current working directory and is automatically opened after evaluation
'''
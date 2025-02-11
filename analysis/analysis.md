## CS358 Principles of Programming Languages -- Winter 2025

## Language Analysis Report

#### Basic information

- What is your chosen language?

  Java

- What range of applications/programming tasks is this language intended for?

  Java is designed for general-purpose programming with particular strengths in:

  - Enterprise software and large-scale applications
  - Web applications and servers (using frameworks like Spring)
  - Android mobile development
  - Cross-platform desktop applications
  - Distributed systems and cloud services
  - Financial services applications

- What (if any) distinctive features does the language have that
  differentiate it from other languages? (What does the language documentation
  brag about?)

  Java's key distinctive features that are often highlighted:

  - Platform independence ("Write Once, Run Anywhere") through the Java Virtual Machine

  - Strong static typing with extensive compile-time checks
  - Automatic memory management through garbage collection
  - Rich standard library (Java Class Library) with built-in security features
  - Object-oriented design with single inheritance but multiple interface implementation
  - Built-in support for multithreading and concurrent programming
  - Backward compatibility - older code typically runs on newer versions
  - Extensive tooling ecosystem and mature development environment support

    The language documentation particularly emphasizes security, portability, and reliability as core design principles

- Who originally invented the language, and when?

  Java was created by James Gosling and his team at Sun Microsystems in 1991-1995

- What are the main implementations of the language available today,
  and who maintains them?

  The main Java implementations today are:

  1. Oracle JDK
     - Maintained by Oracle
     - The primary commercial implementation
     - Most widely used
  2. OpenJDK
     - The open-source reference implementation
     - Largley maintained by Oracle, but with community contributions

- Which exact implementation/version of the language are you reporting
  on here?

  OpenJDK 23

- What authoritative documentation (reference manuals, etc.) is available
  for the language/implementation?

  The main authoritative docs include JLS (Java Language Specification), JVMS (Java Virtual Machine Specification), and JavaDoc API documentation

- Is the language officially standardized by some industry group or
  government organization? If so, include a pointer to the relevant standards
  document.

  Java is standardized through the Java Community Process (JCP) under JSR (Java Specification Requests)

  https://www.jcp.org/en/home/index

- Is the language typically compiled or interpreted? What about the
  implementation you are reporting on here? If the implementation includes
  multiple stages (e.g. compilation to an intermediate code that is interpreted),
  describe this.

  Java uses a two-stage model:

  1. Source code is compiled into bytecode
  2. Bytecode is interpreted/executed by the Java Virtual Machine

- Is there an official formal grammar (e.g. in BNF) for the language?
  If so, include a pointer to this if possible.

  Yes, the official grammar can be found here: https://docs.oracle.com/javase/specs/jls/se7/html/jls-18.html

#### Primitive types and expressions

- Does the language use static or dynamic typing?

  Java uses static typing

- What kinds of primitive numeric types are supported (integers, floats, etc.)?

- What are their ranges and precisions?

  ```java
  byte // 8-bit signed, -128 to 127
  short // 16-bit signed, -32,768 to 32,767
  int // 32-bit signed, -2^31 to 2^31-1
  long // 64-bit signed, -2^63 to 2^63-1
  float // 32-bit IEEE 754
  double // 64-bit IEEE 754
  char // 16-bit Unicode, 0 to 65,535
  boolean // true/false only
  ```

- What happens if integer operations overflow? What happens on division
  by zero?

  If integers operations overflow, it wraps around silently. On division by zero, an ArithmeticException is raised for integer division, and infinty or NaN is returned for floating-point division

- How are booleans represented? Are booleans distinct from integers?
  What values are considered "truthy" and "falsy" in conditional tests?

  Booleans in Java are represented as logical values of either 'true' or 'false'. The excact memory representation is not specified.
  They are distinct from integers.

  Only true/false values are valid in conditional tests, there are no truthy/falsy values

- How are strings represented? How are basic string operations (substring,
  concatenation, etc.) performed?

  Strings are represented as objects of the String class. Each character within the string is stored using 16 bits, adhering to UTF-16 encoding. They are immutable

  Concatentation is done with the + operator, and substring is done with the class method substring()

- What operators are allowed in expressions? What are any interesting
  features of the precedence and associativity rules for operators (e.g.,
  differences from other languages like C++ or Python)?

  Arithmetic: +, -, \_, /, %, ++, --

  Relational: <, >, <=, >=, ==, !=

  Logical: &&, ||, !, ^

  Bitwise: &, |, ^, ~, <<, >>, >>>

  Assignment: =, +=, -=, \_=, /=, %=, &=, |=, ^=, <<=, >>=, >>>=

  Other: ?:, instanceof, ->

  There is no comma operator like in C/C++, there is no direct pointer arithmetic, no operator overloading, && and || are short circuiting

- Is there an equivalent to `let` bindings in expressions?

  There is no equivalent to 'let' bindings in expressions in Java

#### Functions, binding, scoping

- What is the syntax for function definitions? What about for mutually
  recursive function definitions?

  1. Function Definition Syntax:

  ```java
  [access_modifier] [static] return_type methodName(parameter_list) {
    // method body
  }
  ```

  2. Mutually Recursive Methods: Just define them in the same class

  ```java
  class Example {
    boolean isEven(int n) {
        if (n == 0) return true;
        if (n == 1) return false;
        return isOdd(n - 1);
    }

    boolean isOdd(int n) {
        if (n == 0) return false;
        if (n == 1) return true;
        return isEven(n - 1);
    }
  }
  ```

- Can function definitions be nested (i.e. can we define a local function
  within the body of another function)? If so, what is the syntax for this?

  Java does not support nested method definitions, you would need to use inner classes or lambda expressions as an alternative

- Are there any unusual features to the binding and scoping rules (e.g.
  like Python's `global` and `nonlocal` declarations)?

  Java uses only lexical scoping, there are no global/nonlocal declarations like python

- Can functions be passed as arguments to other functions (e.g. passing
  a comparison operator to a general-purpose `sort` function)?

  Yes, through functional interfaces, method references, and lambda expressions

  ```java
  list.sort((a, b) -> a.compareTo(b));
  list.sort(String::compareToIgnoreCase);
  ```

- Can functions be stored in data structures (e.g. when serving as a
  call-back)?

  Yes, using functional interfaces:

  ```java
  Map<String, Consumer<String>> callbacks = new HashMap<>();
  callbacks.put("print", s -> System.out.println(s));
  ```

- Is there support for anonymous functions (lambda expressions)? If so,
  what is the syntax for them? Are there restrictions on the form of
  anonymous function bodies?

  Lambda expression syntax:

  ```java
  (parameters) -> expression
  (parameters) -> { statements; }
  ```

  The restrictions are:

  - Must conform to functional interface
  - Can only access effectively final local variables
  - cannoy modify local variables from enclosing scope

- Does the language use static or dynamic binding (in the sense discussed
  in class)?

  Java uses static binding for class methods, and dynamic dispatch for virtual methods based on runtime type

- How are arguments passed to functions (e.g., by value, by name,
  something else)?

  Primitive types are passed by value

  Object references are passed by value (not the objects themselves)

  There is no pass by reference

  ```java
  void example(int x, String s) {  // x is copied, s is a copied reference
    x = 42;        // doesn't affect caller
    s = "new";     // doesn't affect caller's reference
    s.toLowerCase(); // affects shared object if mutable
  }
  ```

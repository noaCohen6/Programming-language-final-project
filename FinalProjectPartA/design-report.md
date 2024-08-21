# Design and Implementation Report: Custom Programming Language

## 1. Introduction

This report discusses the design and implementation of a custom programming language interpreter. The project involved creating a lexer, parser, and interpreter for a new programming language, implementing various features such as arithmetic operations, control structures, and function definitions.

## 2. Design Decisions

### 2.1 Language Syntax

The language syntax was designed to be intuitive yet powerful, incorporating elements from both functional and imperative programming paradigms. Key syntax decisions include:

- Using `DEFUN` for function definitions.
- Implementing a Python-like syntax for control structures (e.g., `IF ... THEN ... ELSE`).
- Supporting lambda functions for anonymous function creation.

### 2.2 Lexer Design

The lexer (`my_Lexer` class) was implemented to tokenize the input string. Design decisions include:

- Using a position tracking system (`Position` class) for error reporting.
- Implementing a method to peek at the next character, allowing for multi-character tokens.
- Creating specific token types for each language feature (e.g., `T_INT`, `T_PLUS`, `T_IF`).

### 2.3 Parser Design

The parser (`Parser` class) uses a recursive descent approach. Key design choices include:

- Implementing a `ParseResult` class to handle both successful parsing and error cases.
- Using separate methods for different language constructs (e.g., `expr()`, `term()`, `factor()`).
- Creating specific node types for each language construct (e.g., `NumberNode`, `BinOpNode`, `IfNode`).

### 2.4 Interpreter Design

The interpreter (`Interpreter` class) uses the visitor pattern to traverse and execute the abstract syntax tree (AST). Design decisions include:

- Implementing a global symbol table for variable and function storage.
- Using a `Context` class to manage scopes and aid in error reporting.
- Creating an `RTResult` class to handle both successful execution and runtime errors.

## 3. Challenges Faced and Solutions Implemented

### 3.1 Challenge: Operator Precedence

**Challenge**: Implementing correct operator precedence in arithmetic expressions.

**Solution**: The parser uses separate methods for different precedence levels (`expr()`, `term()`, `factor()`, `primary()`). This ensures that operations are parsed and executed in the correct order.

### 3.2 Challenge: Error Handling and Reporting

**Challenge**: Providing meaningful error messages with accurate position information.

**Solution**: 
- Implemented a `Position` class to track the current position in the source code.
- Created specific error classes (e.g., `IllegalCharError`, `ExpectedCharError`) for different error types.
- Used the `Error` base class to generate formatted error messages with file and line information.

### 3.3 Challenge: Function Implementation

**Challenge**: Implementing function definitions and calls, including recursion.

**Solution**: 
- Created `FunctionDefNode` and `FunctionCallNode` to represent function definitions and calls in the AST.
- Implemented a `Function` class to store function information and handle execution.
- Used the global symbol table to store defined functions, allowing for recursive calls.

### 3.4 Challenge: Lambda Functions

**Challenge**: Implementing anonymous lambda functions.

**Solution**: 
- Added a `LambdaNode` to represent lambda expressions in the AST.
- Extended the parser to recognize and parse lambda syntax.
- Implemented lambda execution in the interpreter, creating anonymous functions on the fly.

### 3.5 Challenge: Control Structures

**Challenge**: Implementing control structures like if-statements and for-loops.

**Solution**: 
- Created specific node types (`IfNode`, `ForNode`) to represent these structures in the AST.
- Implemented corresponding visit methods in the interpreter to execute these structures.
- Used the `RTResult` class to handle the flow control and return values from these structures.

## 4. Conclusion

The development of this custom programming language interpreter presented various challenges in language design, parsing, and runtime implementation. By carefully considering design decisions and implementing robust solutions, we've created a functional interpreter capable of executing a wide range of programming constructs.

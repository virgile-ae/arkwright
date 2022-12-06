# Goals

- To write an compiler for a usable LISP-derived language into Javascript.
- To write tests to ensure that the compiler works correctly and produces a correct and executable output.
- Report helpful errors the user.

# Non-goals

- To write a type-checker to ensure that the user's code is type-safe.
- T

# Plan

- Write a lexer for the language to tokenize the inputted string.
- Parse the tokens into an AST (abstract syntax tree) using a recursive descent parser.
- Transform the AST 
- Report errors encountered along the way to the user.

# Features of the language

- Mutable and (almost) immutable assignement with `let` and `const` (and reassignment through `set`).
- Input and output through `input` and `print` (access the DOM in the browser should also work but hasn't been tested).
- Functions can be created through `func`.
- Boolean expressions are available through `and`, `or`, and `not`.
- Comparison and arithmetic operators (`=`, `!=`, `>=`, `>`, `<=`, `<`, `+`, `-`, `*`, `/`)
- 

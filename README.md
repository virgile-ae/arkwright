# Aims

- To write an interpreter/compiler for a LISP-derived language
- The language should have:
  - Data literals (numbers, strings, booleans, lists)
  - Variables
  - Input and output
  - Functions and builtin functions (e.g. arithmetic and boolean operators)
- To write tests to ensure that the interpreter/compilewrite tests to ensure that the interpreter/compiler works correctly.

# Plan

- Write a lexer for the language to tokenize the inputted string.
- Parse the tokens into an AST.
- Transform the AST.
- Execute the transformed AST using Python's builtin AST module.
- Report errors encountered along the way to the user.

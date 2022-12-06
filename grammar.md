
# Grammar

## What is a grammar?

- A grammar is a formal specification for a programming language.
- It describes how all functioning programs in a programming language can be constructed (in essence the programming language's syntax).
- It is used to help build the lexer and parser as terminal symbols can be mapped to lexemes and non-terminal symbols can be mapped to functions in a recursive descent parser.

## How to read the grammar?

- The grammar is a cross between EBNF and PCRE (although the latter is commonly used for regular expressions, I found it quite suitable for writing a grammar)
- `#` for comments.
- `;` to end each parsing expression.
- `+` indicates one or more.
- `*` indicates zero or more.
- `?` indicates optionally.
- `.` indicates any character.
- `..` indicates any of a range (e.g. a, b, c, or d would be 'a'..'d').
- `|` indicates a choice between two parsing expressions.
- `(` and `)` are used for grouping.
- `^` negates a parsing expression (i.e. anything other than the listed patterns).
- `'` indicates the start and end of a string of text which is to be parsed (terminal symbols).
- `<` and `>` indicate the start and end of the variable of a parsing expression (nonterminal symbols).

## Other info

- The builtin functions will be treated as keywords by the interpreter.
- Whitespace only delimits arguments in s-expressions (it isn't otherwise significant)
- The grammar is referentially transparent (it would be the same if all uses of non-terminals were replaced with their value, although this would be impractical as it would be very difficult to read.)

## The grammar

```python
expression = <s_expr> | <list> | <value> ;

s_expr = '(' <identifier> <expression>* ')'

identifier = <keyword> | <variable> ;

value = <literal> | <variable> ;

literal =
    <number> |
    <string> |
    <boolean> |
    "nil"
    ;

list = '[' expression* ']' ;

# all of the below are handled by the lexer

# value which can hold a function or data
variable = ( 'a'..'z' | 'A'..'Z' | '_' )+ ;

# these are all the keywords specified in the lexer (see _keywords)
# they have been emitted for brevity
keyword = ... ;

number = ('0'..'9')+ ("." ('0'..'9')+)? ;

string = '"' (^ '"')* '"' ;

boolean = 'true' | 'false' ;
```

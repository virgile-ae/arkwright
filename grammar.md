
# Grammar

## How to read the grammar

- The grammar is similar to PCRE's grammar.
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
- Whitespace only delimits arguments in s-expressions (isn't otherwise significant)

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

keyword =
    'var' |
    'input' | 'print' |
    'if' |
    'func' |
    '+' | '-' | '*' | '/' |
    'and' | 'or' | 'not' | '=' | '!=' | '>=' | '<=' | '>' | '<'
    ;

number = ('0'..'9')+ ("." ('0'..'9')+)? ;

string = '"' (^ '"')* '"' ;

boolean = 'true' | 'false' ;
```

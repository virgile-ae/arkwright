from dataclasses import dataclass
from lex import Lexeme

@dataclass
class SExpr:
    identifier: object
    arguments: list

    def __repr__(self) -> str:
        args = ' '.join(map(str, self.arguments))
        return f'({self.identifier} {args})'

@dataclass
class Value:
    """Values can be variabls or literals."""
    type: str
    value: object

    def __repr__(self) -> str:
        return str(self.value)

# An expression is something which evaluates to something,
# so everything is an expression.
Expression = SExpr | Value

# object can be a sexpr, literal, keyword, variable
ParseResult = tuple[object, list[Lexeme]] | None

def parse_expression(lexemes: list[Lexeme]) -> ParseResult:
    if not lexemes:
        return

    match lexemes[0].type:
        case 'left paren':
            return parse_sexpr(lexemes)
        case 'number' | 'string' | 'boolean':
            return parse_value(lexemes)
        case _ if lexemes[0].value == None:
            return parse_value(lexemes)
        case 'right paren':
            return
        case _:
            raise RuntimeError(f'unexpected lexeme: {lexemes[0].value}')

def parse_sexpr(lexemes: list[Lexeme]) -> ParseResult:
    if not lexemes or lexemes[0].type != 'left paren':
        return # signals failure (thing which is to be parsed isn't an s expression)

    if lexemes[1].type not in ['variable', 'keyword']: # if it isn't an identifier
        raise RuntimeError(f"unexpected lexeme: '{lexemes[1].value}', expected identifier")

    identifier = lexemes[1]

    arguments = []
    lexemes = lexemes[2:]
    while result := parse_expression(lexemes):
        lexemes = result[1]
        arguments.append(result[0])

    if lexemes[0].type != 'right paren':
        raise RuntimeError(f'unexpected EOF: expected right paren')
    
    return SExpr(identifier.value, arguments), lexemes[1:]


def parse_value(lexemes: list[Lexeme]) -> ParseResult:
    if not lexemes or                                                         \
        lexemes[0].type not in ['number', 'string', 'boolean', 'variable'] or \
        lexemes[0].value == None:
        return
    return Value(lexemes[0].type, lexemes[0].value,), lexemes[1:]


# PARSER
def parse(lexemes: list[Lexeme]) -> list[SExpr | Value]:
    expressions = []
    while result := parse_expression(lexemes):
        lexemes = result[1]
        expressions.append(result[0])
    return expressions

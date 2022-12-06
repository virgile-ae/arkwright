# Transforms the lexemes into an AST
from dataclasses import dataclass
from errors import ErrorHandler
from lex import Lexeme

error_handler = ErrorHandler()


@dataclass
class Value:
    """Values represent variables or literals."""
    type: str  # used for checking that the suitable inputs are passed to certain functions
    value: object
    line: int  # line number of the value in text (for errors)

    def __repr__(self) -> str:
        return str(self.value)

    def __eq__(self, other) -> bool:
        if isinstance(other, Value):
            return self.value == other.value and self.type == other.type
        raise TypeError


@dataclass
class SExpr:
    """
    S-Expressions make up most of a program. They are used to call functions and to take advantage of keywords.
    """
    identifier: str  # the first part of the s-expression. it indicates 
    arguments: list
    line: int

    def __repr__(self) -> str:
        args = ' '.join(map(str, self.arguments))
        return f'({self.identifier} {args})'

    def __eq__(self, other) -> bool:
        return isinstance(other, SExpr) and        \
            self.identifier == other.identifier and\
            self.arguments == other.arguments


# ParseResult represents the fallible result from a parsing function
# None represents the failure of a parse function
# the tuple is the result from the parsing and the remaining lexemes
ParseResult = tuple[SExpr | Value, list[Lexeme]] | None


def parse_expression(lexemes: list[Lexeme]) -> ParseResult:
    if not lexemes:  # if list is empty
        return

    first = lexemes[0].type

    if first == 'left paren':
        return parse_sexpr(lexemes)

    if first in ['number', 'string', 'boolean', 'nil', 'left bracket', 'variable']:
        return parse_value(lexemes)

    if first in ['right paren', 'right bracket']:
        return

    error_handler.new_error(
        f'unexpected lexeme: {lexemes[0].value}', lexemes[0].line)


def parse_sexpr(lexemes: list[Lexeme]) -> ParseResult:
    if not lexemes or lexemes[0].type != 'left paren':
        # signals failure (thing which is to be parsed isn't an s expression)
        return
    line = lexemes[0].line

    if lexemes[1].type not in ['variable', 'keyword', 'symbol']:
        # if it isn't an identifier
        error_handler.new_error(
            f": unexpected lexeme: '{lexemes[1].value}', expected identifier", lexemes[1].line)

    identifier = lexemes[1]
    arguments = []
    lexemes = lexemes[2:]

    while result := parse_expression(lexemes):
        lexemes = result[1]
        arguments.append(result[0])

    if not lexemes:
        error_handler.new_error('unexpected EOF: expected right paren', line)

    if lexemes[0].type != 'right paren':
        error_handler.new_error(
            f"unexpected lexeme: '{lexemes[0]}', expected right paren", lexemes[0].line)

    return SExpr(identifier.value, arguments, line), lexemes[1:]


def parse_value(lexemes: list[Lexeme]) -> ParseResult:
    if not lexemes or lexemes[0].type not in ['number', 'string', 'boolean', 'variable', 'nil', 'left bracket']:
        return
    line = lexemes[0].line
    if lexemes[0].type == 'left bracket':
        return parse_list(lexemes)
    return Value(lexemes[0].type, lexemes[0].value, line), lexemes[1:]


def parse_list(lexemes: list[Lexeme]) -> ParseResult:
    """Parses lexemes which make up a list into a Value with the """
    if not lexemes or lexemes[0].type != 'left bracket':
        return

    line = lexemes[0].line

    elements = []
    lexemes = lexemes[1:]

    # while there are still elements in the array
    while result := parse_expression(lexemes):
        lexemes = result[1]
        elements.append(result[0])

    if not lexemes:
        error_handler.new_error(
            f'unexpected EOF: expected right bracket', lexemes[0].line)

    if lexemes[0].type != 'right bracket':
        error_handler.new_error(
            f"unexpected lexeme: '{lexemes[0]}', expected right bracket", lexemes[0].line)

    return Value('list', elements, line), lexemes[1:]


# PARSER
def parse(lexemes: list[Lexeme], local_handler: ErrorHandler) -> list[SExpr | Value]:
    """Parses the lexemes into an abstract syntax tree."""
    global error_handler
    error_handler = local_handler
    expressions = []
    while result := parse_expression(lexemes):
        lexemes = result[1]
        expressions.append(result[0])

    if lexemes:  # no lexemes should be left
        error_handler.new_error(
            f"unexpected lexemes at EOF: '{lexemes}'", lexemes[0].line, can_continue=True)

    return expressions

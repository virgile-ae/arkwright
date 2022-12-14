import re

from errors import ErrorHandler

# Token name, regex
KEYWORDS = ['let', 'const', 'input', 'print', 'if',
            'func', 'and', 'or', 'not', 'nth', 'do', 'set']
keywords = [('keyword', f'\b{x}\b') for x in KEYWORDS]

_symbols = [
    '=', r'!=', '>=', '>', '<=', '<',
    r'\+', '-', r'\*', '/']
symbols = [('symbol', x) for x in _symbols]

patterns = [
    ['left paren', r'\('],
    ['right paren', r'\)'],
    ['left bracket', r'\['],
    ['right bracket', r'\]'],
    ['number', r'(-)?\d+(\.\d+)?'],
    ['boolean', r'true|false'],
    ['nil', r'nil'],
    ['string', r'"(.*)"'],
    ['variable', r'[a-zA-Z_\.]+'],
    # Includes '.' to allow indexing so that object properties and methods can be accessed
    ['newline', r'\r(\n)?|\n'],
    ['whitespace', r'(\t| )+'],
    ['comment', r'//.*'],  # . matches everything except a newline
]

# compiling all of the regex patterns
LEXEMES = [(name, re.compile(f'({pattern})'))
           for [name, pattern] in [*keywords, *patterns, *symbols]]


class Lexeme:
    def __init__(self, type: str, value, line: int = 0, offset: int = 0) -> None:
        self.type = type
        self.value = value
        self.line = line
        self.offset = offset

    def __repr__(self) -> str:
        return f'{self.type}: "{self.value}"'

    def __eq__(self, other) -> bool:
        return isinstance(other, Lexeme) and \
            self.type == other.type and self.value == other.value


# LEXER
def lex(input_string: str, error_handler: ErrorHandler) -> list[Lexeme]:
    """Groups characters into lexemes so they are easier to parse."""
    line = 1
    offset = 0
    lexemes = []
    while len(input_string):
        for [name, pattern] in LEXEMES:
            # if the regex pattern matches
            if matches := pattern.match(input_string):
                m = str(matches.groups(1)[0])
                if name == 'number':
                    lexemes.append(Lexeme(name, float(m), line, offset))
                elif name == 'string':
                    lexemes.append(Lexeme(name, m[1:-1], line, offset))
                elif name == 'boolean':
                    lexemes.append(
                        Lexeme(name, eval(m.capitalize()), line, offset))
                elif name == 'nil':
                    lexemes.append(Lexeme(name, None, line, offset))
                elif name == 'newline':
                    line += 1
                    offset = 0
                elif name in ['whitespace', 'comment']:
                    pass  # so it doesn't get added
                else:
                    lexemes.append(Lexeme(name, m, line, offset))
                input_string = input_string[len(m):]
                offset += len(m)
                break
        else:  # if all the patterns have been tried and have failed
            error_handler.new_error(
                f"unrecognized lexeme: {input_string.splitlines()[0]}", line)
    return lexemes

import re

# Token name, regex
_keywords = ['var', 'input', 'print', 'if', 'func', 'and', 'or', 'not']
keywords = [('keyword', x) for x in _keywords]

_symbols = [
    '=',
    '>',
    '>=',
    '<',
    '<=',
    r'\+',
    '-',
    r'\*',
    '/',
]
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
    ['variable', r'[a-zA-Z_]+'],
    ['newline', r'\r(\n)?|\n'],
    ['whitespace', r'(\t| )+'],
]

# compiling all of the regex patterns for the
LEXEMES = [(name, re.compile(f'({pattern})'))
           for [name, pattern] in [*keywords, *patterns, *symbols]]


class Lexeme:

    def __init__(self, type: str, value, line=0, offset=0) -> None:
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
def lex(input_string: str) -> list[Lexeme]:
    """Groups characters into lexemes so they are easier to parse."""
    input_string = input_string
    line = 1
    offset = 0
    tokens = []
    while len(input_string):
        for [name, pattern] in LEXEMES:
            if matches := pattern.match(input_string):
                m = str(matches.groups(1)[0])
                if name == 'number':
                    tokens.append(Lexeme(name, float(m), line, offset))
                elif name == 'string':
                    tokens.append(Lexeme(name, m[1:-1], line, offset))
                elif name == 'boolean':
                    tokens.append(Lexeme(name, eval(m.capitalize()), line, offset))
                elif name == 'nil':
                    tokens.append(Lexeme(name, None, line, offset))
                elif name == 'newline':
                    line += 1
                    offset = 0
                elif name == 'whitespace':
                    pass # so it doesnt get added
                else:
                    tokens.append(Lexeme(name, m, line, offset))
                input_string = input_string[len(m):]
                offset += len(m)
                break
        else:
            raise RuntimeError(
                f"unrecognized lexeme on line {line}: {input_string.splitlines()[0]}"
            )
    return tokens

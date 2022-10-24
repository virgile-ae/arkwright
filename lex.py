import re

# Token name, regex
keywords = ['var', 'input', 'print', 'if', 'func', 'and', 'or', 'not'] 
keywords = [ ('keyword', x) for x in keywords ]

symbols = ['=', r'\+', '-', r'\*', '/']
symbols = [ ('keyword', x) for x in symbols ]

patterns = [
    ['left paren',    r'\('],
    ['right paren',   r'\)'],
    ['left bracket',  r'\]'],
    ['right bracket', r'\['],
    ['number',        r'(-)?\d+(\.\d+)?'],
    ['boolean',       r'true|false'],
    ['nil',           r'nil'],
    ['string',        r'"(.*)"'],
    ['variable',      r'[a-zA-Z_]+'],
    ['newline',       '\n'],
]

# compiling all of the regex patterns for the 
TOKENS = [ (name, re.compile(f'({pattern})')) for [name, pattern] in [*keywords, *patterns, *symbols] ]

class Lexeme:
    def __init__(self, type: str, value, line: int = 0) -> None:
        self.type = type
        # value can be a string, number, boolean, function, identifier, function call...
        # so no type annotation
        self.value = value
        self.line = line

    def __repr__(self) -> str:
        return f'{self.type}: "{self.value}"'

    def __eq__(self, other) -> bool:
        return isinstance(other, Lexeme) and self.type == other.type and self.value == other.value


# LEXER
def lex(input_string: str) -> list[Lexeme]:
    """Groups characters into lexemes so they are easier to parse."""
    input_string = input_string.strip()
    line = 1
    tokens = []
    while len(input_string):
        for [name, pattern] in TOKENS:
            if matches := pattern.match(input_string):
                m = str(matches.groups(1)[0])
                if name == 'number':
                    tokens.append(Lexeme(name, float(m), line))
                elif name == 'string':
                    tokens.append(Lexeme(name, m[1:-1], line))
                elif name == 'boolean':
                    tokens.append(Lexeme(name, bool(m.capitalize()), line))
                elif name == 'nil':
                    tokens.append(Lexeme(name, None, line))
                elif name == 'newline':
                    line += 1
                else:
                    tokens.append(Lexeme(name, m, line))
                input_string = input_string[len(m):].strip()
                break
        else:
            raise RuntimeError(f"unrecognized lexeme on line {line}: {input_string.splitlines()[0]}")
    return tokens
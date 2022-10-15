# C
from typing import Any
import re

DO_TESTS = True
# LISP compiler to js

def main():
    print("hello world")

# Token name, regex
TOKENS = [
    ['left paren',    r'\('], # for function calls
    ['right paren',   r'\)'],
    ['left bracket',  r'\['], # for arrays
    ['right bracket', r'\]'],
    ['left brace',    r'{'], # for objects
    ['right brace',   r'}'],
    ['number',        r'\d+(\.\d+)?'],
    ['boolean',       r'(true|false)'],
    ['string',        r'\".*\"'],
    ['symbol',        r':.+'],
    ['identifier',    r'([+\-*/_]|[a-zA-Z][\w_\-]+)'],
]

# compiling all of the regex patterns for the 
TOKENS = map(lambda x: (x[0], re.compile(x[1])), TOKENS)

class Token:
    """Represents a token in the """
    def __init__(self, type: str, value) -> None:
        self.type = type
        # value can be a string, number or boolean depending on the type
        self.value = value


# TOKENIZER
def tokenize(input: str) -> list[Token]:
    tokens = []
    while len(input):
        for [name, pattern] in TOKENS:
            pass
    return tokens

# PARSER
def parse(tokens):
    pass

def traverse_tree():
    pass

# CODEGEN
def generate_code(parse_tree):
    pass

if DO_TESTS:
    from doctest import testmod
    testmod()
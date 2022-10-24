from lex import lex
from parse import parse


def interpreter(code: str):
    lexemes = lex(code)
    parse_tree = parse(lexemes)
    return
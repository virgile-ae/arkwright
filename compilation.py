"""Defines 'compile_to_js' which transforms the code into JS."""
from lex import lex
from parse import parse
from transform import transform


def compile_to_js(code: str) -> str:
    """
    Pipes the result of each step in the compilation to the next,
    to go from the LISP-like language to JS.
    """
    lexemes = lex(code)
    parse_tree = parse(lexemes)
    transformed = transform(parse_tree)
    return transformed

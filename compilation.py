from lex import lex
from parse import parse
from transform import transform
from errors import ErrorHandler


def compile_to_js(code: str) -> str | None:
    """
    Pipes the result of each step in the compilation to the next,
    to go from the LISP-like language to JS.
    """
    errors = ErrorHandler()
    lexemes = lex(code, errors)
    if errors.errors:
        errors.output_errors()
        return
    parse_tree = parse(lexemes, errors)
    if errors.errors:
        errors.output_errors()
        return
    transformed = transform(parse_tree, errors)
    if errors.errors:
        errors.output_errors()
        return
    return transformed

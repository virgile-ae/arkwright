from lex import lex
import parse
from transform import transform
from parseparint import parseprint
import ast

def interpreter(code: str):
    lexemes = lex(code)
    print(lexemes)
    parse_tree = parse.parse(lexemes)
    print(parse_tree)
    
    transformed = transform(parse_tree)
    parseprint(transformed)
    code_object = compile(transformed, filename='<ast>', mode='exec')
    exec(code_object)

def run(tree):
    exec(compile(tree, filename='<ast>', mode='exec'))

if __name__ == '__main__':
    # from test_all import *
    # import unittest
    # unittest.main()
    py=ast.parse('print("hello")')
    parseprint(py)
    result = transform(parse.parse(lex('(print "hello")')))
    print(vars(result.body[0]))
    run(result)
from lex import lex
from parse import parse_sexpr


print(parse_sexpr(lex('(hello "there" -123.2)')))
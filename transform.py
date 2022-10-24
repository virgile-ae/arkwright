import ast
from parse import SExpr, Value
from lex import keywords, symbols
# BinOp, Add, Sub, Mult, Div,
# BoolOp, And, Or, Eq, NotEq, UnaryOp, Not, USub,
# Call, IfExpr, Assign, Name, Expr,
# FunctionDef, arguments, arg, Return
# Module

# print , input

Tree = SExpr | Value

KEYWORDS = [ y for (x, y) in [*keywords, *symbols]]

# KEYWORDS[-2] = '*'
# KEYWORDS[-4] = '+'


def transform_tree(tree: Tree):
    if type(tree) == SExpr:
        if tree.identifier in KEYWORDS:
            return transform_keyword(tree)
        else:
            return transform_function_call(tree)
    else: # type(tree) == Value
        return transform_value(tree)


def transform_var():
    pass


def transform_unary_op(tree: Tree):
    pass


def transform_bin_op(tree: Tree):
    pass 
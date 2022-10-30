from parse import SExpr, Value
from lex import keywords, symbols

Tree = SExpr | Value

KEYWORDS = [y for (x, y) in [*keywords, *symbols]]


def transform(trees: list[Tree]):
    return


def transform_tree(tree: Tree):
    if type(tree) == SExpr:
        return transform_keyword_expr(tree)    \
            if tree.identifier in KEYWORDS     \
            else transform_function_call(tree)
    return transform_value(tree)  # type(tree) == Value


def transform_keyword_expr(tree):
    keyword = tree.identifier

    if keyword == 'var':
        return transform_var(tree)
    if keyword == 'func':
        return transform_function_definition(tree)
    if keyword == 'if':
        return transform_if_expr(tree)
    if keyword in ['print', 'input']:
        return transform_io(tree)
    if keyword == 'not':
        return transform_unary_op(tree)
    if keyword in ['and', 'or', '=', '!=', '>', '>=', '<', '<=']:
        return transform_bool_op(tree)
    if keyword in ['+', '-', '*', '/']:
        return transform_bin_op(tree)


def transform_value(tree: Value):
    if tree.type == 'identifier':
        return transform_identifier(tree)
    return transform_constant(tree)


def transform_constant(tree: Value):
    if tree.type not in ['number', 'string', 'boolean', 'nil', 'list']:
        return
    if tree.type == 'list':
        return str(list(map(transform_tree, tree)))
    if tree.type == 'nil':
        return 'null'
    if tree.type == 'string':
        return f'"{tree.value}"'
    
    return str(tree.value).lower()

def transform_identifier(tree: Value):
    if tree.type != 'identifier':
        return
    return tree.value


def transform_function_definition(tree: SExpr):
    if len(tree.arguments) != 3:
        return
    if tree.arguemnts[0].type != 'identifier':
        raise RuntimeError() # TODO
    if tree.arguments[1].type != 'list':
        raise RuntimeError() # TODO
    
    return


def transform_function_call(tree: SExpr):
    args = map(transform_tree, tree.arguments)
    args = ', '.join(args)
    return f'{tree.identifier}({args})'


def transform_var(tree: SExpr):
    if tree.identifier != 'var':
        return

    if len(tree.arguments) != 2 or tree.arguments[0].type != 'variable':
        raise RuntimeError(
            f"'var' keyword only takes 2 arguments, an identifier and value, but {len(tree.arguments)} were provided"
        )

    iden = tree.arguments[0].value
    value = transform_tree(tree.arguments[1])

    return f'\nvar {iden} = {value};'


def transform_if_expr(tree: SExpr):
    if tree.identifier != 'if':
        return

    if len(tree.arguments) != 3:
        raise RuntimeError(
            f"'if' keyword takes 3 arguments, a condition, and 2 expressions, but {len(tree.arguments)} were provided"
        )

    return f'({transform_tree(tree.arguments[0])} ? {transform_tree(tree.arguments[1])} : {transform_tree(tree.arguments[2])})'

def transform_unary_op(tree: SExpr):
    if tree.identifier != 'not':
        return

    if len(tree.arguments) != 1:
        raise RuntimeError(
            f"'not' takes 1 argument but, {len(tree.arguments)} were provided")

    return f'!({transform_tree(tree.arguments[0])})'


def transform_bin_op(tree: SExpr):
    if tree.identifier not in [r'\*', r'\+', '/', '-']:
        return

    if len(tree.arguments) != 1:
        raise RuntimeError(
            f"'{tree.identifier}' takes 2 arguments, but '{len(tree.arguments)}' were provided"
        )
    op = {
        r'\*': '*',
        '/': '/',
        r'\+': '+',
        '-': '-',
    }[tree.identifier]

    left = transform_tree(tree.arguments[0])
    right = transform_tree(tree.arguments[1])
    
    return f'({left} {op} {right})'


def transform_bool_op(tree: SExpr):
    if len(tree.arguments) < 2:
        raise RuntimeError(f"'{tree.identifier}' expects 2 arguments but {len(tree.arguments)} were provided")
    
    if tree.identifier in ['and', 'or', '=']:
        args = map(transform_tree, )
        
        return
    return


def transform_io(tree: SExpr):
    if tree.identifier == 'print':
        arguments = ', '.join(map(tree_transform, tree.arguments))
        return f'console.log({arguments})'
    elif len(tree.arguments) != 1:
        raise RuntimeError(f"'input' function takes 1 argument but {len(tree.arguments)} were provided")
    else:
        return f'prompt({transform_tree(tree.arguments[0])})'
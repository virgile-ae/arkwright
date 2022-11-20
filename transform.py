from parse import SExpr, Value
from lex import keywords

# A tree can be an S-Expression or a Value
Tree = SExpr | Value


# All the keywords which are handled here
unescaped_symbols = [
    '=', '>', '>=', '<', '<=', '!=',
    '+', '-', '*', '/'
]
KEYWORDS = [y for _, y in keywords] + unescaped_symbols


# a consists of a list of trees which evaluate to expressions.
def transform(trees: list[Tree]) -> str:
    """Transforms the entire AST into JS code."""
    return '\n'.join(map(transform_tree, trees))


def transform_tree(tree: Tree) -> str:
    """Transforms one expression from the AST into JS code."""
    if isinstance(tree, SExpr):
        if tree.identifier in KEYWORDS:
            return transform_keyword_expr(tree)
        return transform_function_call(tree)
    return transform_value(tree)  # type(tree) == Value


def transform_keyword_expr(tree: SExpr) -> str:
    """
    Transforms a keyword expression into JS code by distributing
    various keyword expressions to specific functions.
    """
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
    if keyword == 'nth':
        return transform_index(tree)

    raise RuntimeError(f"expected keyword, got '{keyword}'")


def transform_value(tree: Value) -> str:
    if tree.type == 'variable':
        return transform_identifier(tree)
    return transform_constant(tree)


def transform_constant(tree: Value) -> str:
    """Transforms literal values."""
    if tree.type not in ['number', 'string', 'boolean', 'nil', 'list']:
        raise RuntimeError(f"expected constant, got '{tree.type}'")
    if tree.type == 'list':
        return '[ ' + ', '.join(
            [transform_tree(x) for x in tree.value]  # type: ignore
        ) + ' ]'
    if tree.type == 'nil':
        return 'null'
    if tree.type == 'string':
        return f'"{tree.value}"'

    return str(tree.value).lower()


def transform_identifier(tree: Value) -> str:
    if tree.type != 'variable':
        raise RuntimeError(f"expected identifier, got '{tree.type}'")
    return str(tree.value)


def transform_index(tree: SExpr) -> str:
    if len(tree.arguments) != 2:
        raise RuntimeError(
            f"'nth' function takes 2 arguments: a list and an index")

    if tree.arguments[0].type not in ['variable', 'list', 'string']:
        raise RuntimeError(
            "'nth' function takes a list or variable as its first argument")

    if tree.arguments[1].type not in ['variable', 'number']:
        raise RuntimeError(
            "'nth' function takes a number or variable as its second argument")

    return f' {transform_tree(tree.arguments[0])}[{transform_tree(tree.arguments[1])}]'


def transform_function_definition(tree: SExpr) -> str:
    if tree.identifier != 'func':
        raise RuntimeError(f"expected func, got '{tree.identifier}'")
    if (num := len(tree.arguments)) != 3:
        raise RuntimeError(
            'func expression takes 3 arguments: an identifier, a list of arguments,'
            f' and the function body, but {num} were provided')
    if tree.arguments[0].type != 'variable' or tree.arguments[1].type != 'list':
        raise RuntimeError(
            'func expression takes 3 arguments: an identifier, a list of arguments, and the function body')

# TODO
    arguments = ', '.join([transform_identifier(i)
                          for i in tree.arguments[1].value])
    return_expr = transform_tree(tree.arguments[2])

    return f'function {tree.arguments[0].value}({arguments})' + ' { return ' + return_expr + ' };\n'


def transform_function_call(tree: SExpr) -> str:
    args = map(transform_tree, tree.arguments)
    args = ', '.join(args)
    return f' {tree.identifier}({args})'


def transform_var(tree: SExpr) -> str:
    if tree.identifier != 'var':
        raise RuntimeError(f"expected var expression, got '{tree.identifier}'")

    if len(tree.arguments) != 2 or tree.arguments[0].type != 'variable':
        raise RuntimeError(
            f"'var' keyword only takes 2 arguments, an identifier and value, but {len(tree.arguments)} were provided"
        )

    iden = tree.arguments[0].value
    value = transform_tree(tree.arguments[1])

    return f'\nvar {iden} = {value};'


def transform_if_expr(tree: SExpr) -> str:
    if tree.identifier != 'if':
        raise RuntimeError(f"expected if expression, got '{tree.identifier}'")

    if len(tree.arguments) != 3:
        raise RuntimeError(
            "'if' keyword takes 3 arguments: a condition, and 2 expressions,"
            f" but {len(tree.arguments)} were provided"
        )

    return f'({transform_tree(tree.arguments[0])} ? ' \
        f'{transform_tree(tree.arguments[1])} : {transform_tree(tree.arguments[2])})'


def transform_unary_op(tree: SExpr) -> str:
    if tree.identifier != 'not':
        raise RuntimeError(f"expected unary operator, got '{tree.identifier}'")

    if len(tree.arguments) != 1:
        raise RuntimeError(
            f"'not' takes 1 argument but, {len(tree.arguments)} were provided")

    return f'!({transform_tree(tree.arguments[0])})'


def transform_bin_op(tree: SExpr) -> str:
    if tree.identifier not in ['*', '+', '/', '-']:
        raise RuntimeError(
            f"expected binary operator, got '{tree.identifier}'")

    if len(tree.arguments) != 2:
        raise RuntimeError(
            f"'{tree.identifier}' takes 2 arguments, but '{len(tree.arguments)}' were provided"
        )

    left = transform_tree(tree.arguments[0])
    right = transform_tree(tree.arguments[1])

    return f'({left} {tree.identifier} {right})'


def transform_bool_op(tree: SExpr) -> str:
    if len(tree.arguments) < 2:
        raise RuntimeError(
            f"'{tree.identifier}' expects 2 arguments but {len(tree.arguments)} were provided")

    if tree.identifier in ['and', 'or']:
        args = [transform_tree(i) for i in tree.arguments]
        op = {
            'and': ' && ',
            'or': ' || '
        }
        return '(' + op[tree.identifier].join(args) + ')'

    op = {
        '=': '===', # strict equality operator
        '!=': '!==', # strict inequality operator
    }
    op = tree.identifier if tree.identifier not in op.keys() else op[tree.identifier]
    return f'({transform_tree(tree.arguments[0])}' \
        f' {op} {transform_tree(tree.arguments[1])})'


def transform_io(tree: SExpr) -> str:
    if tree.identifier == 'print':
        arguments = ', '.join(map(transform_tree, tree.arguments))
        return f'console.log({arguments})'

    if len(tree.arguments) != 1:
        raise RuntimeError(
            f"'input' function takes 1 argument but {len(tree.arguments)} were provided")
    return f' prompt({transform_tree(tree.arguments[0])})'

from errors import ErrorHandler
from lex import keywords
from parse import SExpr, Value


error_handler = ErrorHandler()

# A tree can be an S-Expression or a Value
Tree = SExpr | Value

# All the keywords which are handled here
unescaped_symbols = ['=', '>', '>=', '<', '<=', '!=', '+', '-', '*', '/']
KEYWORDS = [y for _, y in keywords] + unescaped_symbols


# a consists of a list of trees which evaluate to expressions.
def transform(trees: list[Tree], local_handler: ErrorHandler) -> str:
    """Transforms the entire AST into JS code."""
    global error_handler
    error_handler = local_handler
    return '\n'.join(map(transform_tree, trees))


def transform_tree(tree: Tree) -> str:
    """Transforms one expression from the AST into JS code."""
    if isinstance(tree, SExpr):
        if tree.identifier in KEYWORDS:
            return transform_keyword_expr(tree)
        return transform_function_call(tree)
    return transform_value(tree)


def transform_keyword_expr(tree: SExpr) -> str:
    """
    Transforms a keyword expression into JS code by distributing
    various keyword expressions to specific functions.
    """
    keyword = tree.identifier

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
    if keyword == 'do':
        return transform_do_statement(tree)
    if keyword in ['let', 'const']:
        return transform_assignment(tree)
    if keyword == 'set':
        return transform_set(tree)

    error_handler.new_error(
        f"unexpected keyword: '{keyword}'", tree.arguments[0].line, True)
    return ''


def transform_value(tree: Value) -> str:
    if tree.type == 'variable':
        return transform_identifier(tree)
    return transform_constant(tree)


def transform_constant(tree: Value) -> str:
    """Transforms literal values."""
    if tree.type not in ['number', 'string', 'boolean', 'nil', 'list']:
        error_handler.new_error(
            f"expected constant, got '{tree.type}'", tree.line, True)
    if tree.type == 'list':
        return '[' + ', '.join(
            [transform_tree(x) for x in tree.value]  # type: ignore
        ) + ']'
    if tree.type == 'nil':
        return 'null'
    if tree.type == 'string':
        return f'"{tree.value}"'

    return str(tree.value).lower()


def transform_identifier(tree: Value) -> str:
    if tree.type != 'variable':
        error_handler.new_error(
            f"expected identifier, got '{tree.type}'", tree.line, True)
    return str(tree.value)


def transform_index(tree: SExpr) -> str:
    if len(tree.arguments) != 2:
        error_handler.new_error(
            "'nth' function takes 2 arguments: a list and an index", tree.line, True)
        return ''

    if tree.arguments[0].type not in ['variable', 'list', 'string']:
        error_handler.new_error(
            "'nth' function takes a list or variable as its first argument", tree.line, True)
        return ''

    if tree.arguments[1].type not in ['variable', 'number']:
        error_handler.new_error(
            "'nth' function takes a number or variable as its second argument", tree.line, True)
        return ''

    return f'{transform_tree(tree.arguments[0])}.at({transform_tree(tree.arguments[1])})'


def transform_function_definition(tree: SExpr) -> str:
    if tree.identifier != 'func':
        error_handler.new_error(
            f"expected func, got '{tree.identifier}'", tree.line, True)
        return ''
    if (num := len(tree.arguments)) != 3:
        error_handler.new_error('func expression takes 3 arguments: an identifier, a list of arguments,'
                                f' and the function body, but {num} were provided', tree.line, True)
        return ''
    if tree.arguments[0].type != 'variable' or tree.arguments[1].type != 'list':
        error_handler.new_error(
            'func expression takes 3 arguments: an identifier, a list of arguments, and the function body', tree.line, True)
        return ''

    arguments = ', '.join([transform_identifier(i)
                          for i in tree.arguments[1].value])
    return_expr = transform_tree(tree.arguments[2])

    return f'function {tree.arguments[0].value}({arguments})' + ' {\n  return ' + return_expr + '\n}'


def transform_function_call(tree: SExpr) -> str:
    args = map(transform_tree, tree.arguments)
    args = ', '.join(args)
    return f'{tree.identifier}({args})'


def transform_if_expr(tree: SExpr) -> str:
    if tree.identifier != 'if':
        error_handler.new_error(
            f"expected if expression, got '{tree.identifier}'", tree.line, True)
        return ''

    if len(tree.arguments) != 3:
        error_handler.new_error("'if' keyword takes 3 arguments: a condition, and 2 expressions,"
                                f" but {len(tree.arguments)} were provided", tree.line, True)
        return ''

    # use ternary expression so that it evaluates to something
    return f'({transform_tree(tree.arguments[0])} ? ' \
        f'{transform_tree(tree.arguments[1])} : {transform_tree(tree.arguments[2])})'


def transform_unary_op(tree: SExpr) -> str:
    if tree.identifier != 'not':
        error_handler.new_error(
            f"expected unary operator, got '{tree.identifier}'", tree.line, True)

    if len(tree.arguments) != 1:
        error_handler.new_error(
            f"'not' takes 1 argument but, {len(tree.arguments)} were provided", tree.line, True)

    return f' !({transform_tree(tree.arguments[0])})'


def transform_bin_op(tree: SExpr) -> str:
    if tree.identifier not in ['*', '+', '/', '-']:
        error_handler.new_error(
            f"expected binary operator, got '{tree.identifier}'", tree.line, True)

    if tree.identifier in '*+':
        args = map(transform_tree, tree.arguments)
        return '(' + f' {tree.identifier} '.join(args) + ')'
    elif len(tree.arguments) != 2:
        error_handler.new_error(
            f"'{tree.identifier}' takes 2 arguments, but '{len(tree.arguments)}' were provided", tree.line, True)
        return ''
    else:
        left = transform_tree(tree.arguments[0])
        right = transform_tree(tree.arguments[1])
        return f'({left} {tree.identifier} {right})'


def transform_bool_op(tree: SExpr) -> str:
    if len(tree.arguments) < 2:
        error_handler.new_error(
            f"'{tree.identifier}' expects 2 arguments but {len(tree.arguments)} were provided", tree.line, True)
        return ''

    # cases where the identifier isn't the same in JS
    args = [transform_tree(i) for i in tree.arguments]

    op = {
        '=': '===',  # strict equality operator
        '!=': '!==',  # strict inequality operator
        'and': ' && ',
        'or': ' || ',
    }
    op = tree.identifier if tree.identifier not in op.keys(
    ) else op[tree.identifier]
    return f'({transform_tree(tree.arguments[0])}' \
        f' {tree.identifier} {transform_tree(tree.arguments[1])})'


def transform_io(tree: SExpr) -> str:
    if tree.identifier == 'print':
        arguments = ', '.join(map(transform_tree, tree.arguments))
        return f'console.log({arguments})'

    if len(tree.arguments) != 1:
        error_handler.new_error(
            f"'input' function takes 1 argument but {len(tree.arguments)} were provided", tree.line, True)
        return ''
    return f'prompt({transform_tree(tree.arguments[0])})'


def transform_do_statement(tree: SExpr) -> str:
    statements = '\n  '.join(map(transform_tree, tree.arguments[:-1]))
    return '(() => { ' + statements + '\n  return ' + transform_tree(tree.arguments[-1]) + '\n})()'


def transform_assignment(tree: SExpr) -> str:
    if tree.identifier not in ['let', 'const']:
        error_handler.new_error(
            f"expected assignment expression, got '{tree.identifier}'", tree.line, True)
        return ''

    if len(tree.arguments) != 2 or tree.arguments[0].type != 'variable':
        error_handler.new_error(
            f"assignment expression takes 2 arguments, an identifier and value, but {len(tree.arguments)} were provided", tree.line, True)
        return ''

    iden = tree.arguments[0].value
    value = transform_tree(tree.arguments[1])

    return f'{tree.identifier} {iden} = {value};'


def transform_set(tree: SExpr) -> str:
    if len(tree.arguments) != 2:
        error_handler.new_error(
            f"'set' function takes 2 arguments but {len(tree.arguments)} were provided",
            tree.line)
        return ''
    return f'{transform_tree(tree.arguments[0])} = {transform_tree(tree.arguments[1])}'

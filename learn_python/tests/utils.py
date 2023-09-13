import importlib
import inspect
import ast
from math import isclose
from functools import wraps


def import_string(str_to_import):
    module_name, attr_name = str_to_import.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, attr_name, None)



def is_function_called(calling_func, called_func):
    """
    Check if the calling_func calls the called_func.
    """
    called_name = called_func if isinstance(called_func, str) else called_func.__name__
    for node in ast.walk(parse_ast(calling_func)):
        if isinstance(node, ast.Call):
            func_name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr
            if func_name == called_name:
                return True
    return False


def count_calls(calling_func, called_func = None):
    """
    Count the number of function calls made from the function.

    :param calling_func: function - the function to check
    :param called_func: str or function - the function to count calls to,
        if None count all calls
    """
    calls = 0
    for node in ast.walk(parse_ast(calling_func)):
        if isinstance(node, ast.Call):
            if (
                called_func is None or 
                (isinstance(called_func, str) and called_func == node.func.id) or
                called_func.__name__ == node.func.id
            ):
                calls += 1
    return calls


def parse_ast(func):
    if not isinstance(func, ast.AST):
        return ast.parse(inspect.getsource(func))
    return func


def has_docstring(func):
    parsed_ast = parse_ast(func)
    if is_function(parsed_ast) or is_class(parsed_ast):
        node = parsed_ast.body[0]
    elif parsed_ast.body:
        node = parsed_ast.body[0]
    else:
        return False
    return (
        isinstance(node.body[0], ast.Expr) and 
        isinstance(node.body[0].value, ast.Str)
    )


def is_class(func):
    tree = parse_ast(func)
    return tree.body and isinstance(parse_ast(func).body[0], ast.ClassDef)


def is_function(func):
    tree = parse_ast(func)
    return tree.body and isinstance(parse_ast(func).body[0], ast.FunctionDef)


def num_statements(func):
    tree = parse_ast(func)
    return sum(
        1 for child in ast.walk(tree) if isinstance(child, ast.stmt)
    ) - 1 if is_function(tree) or is_class(tree) else 0


def count_statements(func, statement):
    statements = 0
    for node in ast.walk(parse_ast(func)):
        if isinstance(node, statement):
            statements += 1
    return statements


def has_statement(func, statement):
    for node in ast.walk(parse_ast(func)):
        if isinstance(node, statement):
            return True
    return False


def has_ternary(func):
    return has_statement(func, ast.IfExp)


def has_list_comprehension(func):
    return has_statement(func, ast.ListComp)


def has_set_comprehension(func):
    return has_statement(func, ast.SetComp)


def has_dict_comprehension(func):
    return has_statement(func, ast.DictComp)


def has_pass(func):
    return has_statement(func, ast.Pass)


def has_and(func):
    for node in ast.walk(parse_ast(func)):
        if isinstance(node, ast.BoolOp):
            if isinstance(node.op, ast.And):
                return True
    return False


def has_or(func):
    for node in ast.walk(parse_ast(func)):
        if isinstance(node, ast.BoolOp):
            if isinstance(node.op, ast.Or):
                return True
    return False


def has_not(func):
    for node in ast.walk(parse_ast(func)):
        if isinstance(node, ast.BoolOp):
            if isinstance(node.op, ast.Not):
                return True
    return False


def has_logical_operator(func):
    tree = parse_ast(func)
    return has_and(tree) or has_or(tree) or has_not(tree)


def has_format_specifier(func):
    for node in ast.walk(parse_ast(func)):
        if isinstance(node, ast.FormattedValue) and node.format_spec is not None:
            return node.format_spec.values[0].value
    return False


def has_while_loop(func):
    return has_statement(func, ast.While)


def has_for_loop(func):
    return has_statement(func, ast.For)


def has_break(func):
    return has_statement(func, ast.Break)


def has_continue(func):
    return has_statement(func, ast.Continue)


def has_func_definition(func):
    return has_statement(func, ast.FunctionDef)


def has_slice(func):
    return has_statement(func, ast.Slice)


def is_unimplemented(func):
    """
    A function is considered unimplemented if it has only a doctstring, only a pass
    or only a docstring and a pass statement.
    """
    tree = parse_ast(func)
    return (
        (num_statements(tree) == 1 and (has_pass(tree) or has_docstring(tree))) or
        (num_statements(tree) == 2 and has_docstring(tree) and has_pass(tree))
    )

def compare_floats(list1, list2, tolerance=1e-9):
    if len(list1) == len(list2):
        for a, b in zip(list1, list2):
            if not isclose(a, b, abs_tol=tolerance):
                return False
        return True
    return False


def float_range(start, stop, step):
    """
    Like range(), but with floats and stop is inclusive.
    """
    step = abs(step) * (-1 if start > stop else 1)
    # we use step/2 to account for floating point precision error, using any value less than
    # the step size will always work
    stop = stop + step/2
    while (step > 0 and start < stop) or (step < 0 and start > stop):
        yield start
        start += step


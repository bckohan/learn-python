import io
from contextlib import redirect_stdout, redirect_stderr
import subprocess
from pathlib import Path
import sys
import pytest
from pprint import pformat
import ast
import inspect
from learn_python.utils import import_string


modules = Path(__file__).parent.parent 
gateway2 = modules / 'module2_data_types' / 'gateway2.py'

def unimplemented(function_name) -> bool:
    source_code = inspect.getsource(
        import_string(f'learn_python.module2_data_types.gateway2.{function_name}')
    )

    # Get the AST of the function
    parsed_ast = ast.parse(source_code)
    if not parsed_ast.body:
        return True
    
    if not parsed_ast.body[0].body:
        return True
    
    if len(parsed_ast.body[0].body) == 2:
        if isinstance(parsed_ast.body[0].body[-1], ast.Pass):
            if isinstance(parsed_ast.body[0].body[0], ast.Expr):
                if isinstance(parsed_ast.body[0].body[0].value, ast.Str):
                    return True
    elif len(parsed_ast.body[0].body) == 1:
        if isinstance(parsed_ast.body[0].body[0], ast.Pass) or (
             isinstance(parsed_ast.body[0].body[0], ast.Expr) and
             isinstance(parsed_ast.body[0].body[0].value, ast.Str)
        ):
            return True
        
    # an attempt has likely been made at an implementation
    return False

@pytest.mark.skipif(
    not gateway2.exists() or unimplemented('are_same_object'),
    reason="are_same_object not implemented yet."
)
def test_gateway2_are_same_object():
    from learn_python.module2_data_types.gateway2 import are_same_object

    assert are_same_object(None, None) is True, f'are_same_object(None, None) should return True, but returns {are_same_object(None, None)}'

    five = 5
    six = 6
    assert are_same_object(five, six) is False, f'are_same_object(five, five2) should return False, but returns {are_same_object(five, six)}'
    assert are_same_object(five, five) is True, f'are_same_object(five, five) should return False, but returns {are_same_object(five, five)}'

    list1 = list2 = []
    assert are_same_object(list1, list2) is True, f'are_same_object(list1, list2) should return True, but returns {are_same_object(list1, list2)}'

    list3 = []
    assert are_same_object(list1, list3) is False, f'are_same_object(list1, list3) should return False, but returns {are_same_object(list1, list3)}'

    five += six
    assert are_same_object(five, six) is False, f'are_same_object(five, six) after five += six, should return False, but returns {are_same_object(five, six)}'

    five = six
    assert are_same_object(five, six) is True, f'are_same_object(five, six) after five = six, should return True, but returns {are_same_object(five, six)}'


@pytest.mark.skipif(
    not gateway2.exists() or unimplemented('normal_distribution'),
    reason="normal_distribution not implemented yet."
)
def test_gateway2_normal_distribution():

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.stats import norm

    from learn_python.module2_data_types.gateway2 import normal_distribution

    # Values for mu and sigma
    params = [
        (0, 1),   # mu=0, sigma=1
        (2, 1),   # mu=2, sigma=1
        (0, 0.5), # mu=0, sigma=0.5
        (2, 2)    # mu=2, sigma=2
    ]

    tolerance = 10e-12

    x_values = np.linspace(-5, 5, 1000)

    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    
    for mu, sigma in params:
        y = norm.pdf(x_values, mu, sigma)
        axs[0].plot(x_values, y, label=f"µ={mu}, σ={sigma}")
    
    axs[0].set_title("Correct Normal Distributions")
    axs[0].legend()
    
    passing = True
    plots = 0
    for mu, sigma in params:
        y_values = []
        for index, x in enumerate(np.linspace(-5, 5, 1000)):
            y = normal_distribution(x, sigma, mu)

            # make sure we don't try to plot garbage!
            if not isinstance(y, (int, float)):
                continue

            y_values.append(y)
            passing &= abs(y - norm.pdf(x, mu, sigma)) < tolerance
        
        # make sure we don't try to plot garbage!
        if len(x_values) == len(y_values):
            axs[1].plot(x_values, y_values, label=f"µ={mu}, σ={sigma}")
            plots += 1
        else:
            passing = False
    
    axs[1].set_title("Your Normal Distributions")
    if plots:
        axs[1].legend()

    axs[0].set_xlabel("x")
    axs[0].set_ylabel("Probability Density")
    axs[1].set_xlabel("x")
    axs[1].set_ylabel("Probability Density")
    plt.tight_layout()

    # on osx matplot lib is printing a stack trace to stderr when you close
    # the plot - hide this! best not to scare the students
    plt.subplots_adjust(top=0.88)
    if passing:
        fig.suptitle('normal_distribution(): PASSING', fontsize=16, color='green')
        plt.show(block=False)
        plt.pause(5)
        plt.close("all")
    else:
        fig.suptitle('normal_distribution(): FAILING (close to continue)', fontsize=16, color='red')
        plt.show()

    if not passing:
        pytest.fail("normal_distribution does not match scipy.stats.norm.pdf")


def is_identity(matrix, size=None):
    size = size or len(matrix)
    if len(matrix) != size:
        return False
    for row_idx, row in enumerate(matrix):
        if not isinstance(row, (tuple, list)):
            return False
        if len(row) != size:
            return False
        for col_idx, value in enumerate(row):
            if row_idx == col_idx:
                if value != 1:
                    return False
            elif value != 0:
                return False
    return True

@pytest.mark.skipif(
    not gateway2.exists() or unimplemented('identity_matrix'),
    reason="identity_matrix not implemented yet."
)
def test_gateway2_identity_matrix():
    from learn_python.module2_data_types.gateway2 import identity_matrix

    assert identity_matrix(-1) is None
    assert identity_matrix(0) == []
    assert is_identity(identity_matrix(1), 1), f'identity_matrix(1) is not correct: {pformat(identity_matrix(1))}'
    assert is_identity(identity_matrix(2), 2), f'identity_matrix(2) is not correct: {pformat(identity_matrix(2))}'
    assert is_identity(identity_matrix(3), 3), f'identity_matrix(3) is not correct: {pformat(identity_matrix(3))}'
    assert is_identity(identity_matrix(4), 4), f'identity_matrix(4) is not correct: {pformat(identity_matrix(4))}'
    assert is_identity(identity_matrix(26), 26), f'identity_matrix(26) is not correct: {pformat(identity_matrix(26))}'


@pytest.mark.skipif(
    not gateway2.exists() or unimplemented('identity_matrix_comprehension'),
    reason="identity_matrix_comprehension not implemented yet."
)
def test_gateway2_identity_matrix_comprehension():
    from learn_python.module2_data_types.gateway2 import identity_matrix_comprehension

    assert identity_matrix_comprehension(-1) is None
    assert identity_matrix_comprehension(0) == []
    assert is_identity(identity_matrix_comprehension(1), 1), f'identity_matrix_comprehension(1) is not correct: {pformat(identity_matrix_comprehension(1))}'
    assert is_identity(identity_matrix_comprehension(2), 2), f'identity_matrix_comprehension(2) is not correct: {pformat(identity_matrix_comprehension(2))}'
    assert is_identity(identity_matrix_comprehension(3), 3), f'identity_matrix_comprehension(3) is not correct: {pformat(identity_matrix_comprehension(3))}'
    assert is_identity(identity_matrix_comprehension(4), 4), f'identity_matrix_comprehension(4) is not correct: {pformat(identity_matrix_comprehension(4))}'
    assert is_identity(identity_matrix_comprehension(26), 26), f'identity_matrix_comprehension(26) is not correct: {pformat(identity_matrix_comprehension(26))}'

    source_code = inspect.getsource(identity_matrix_comprehension)
    parsed_ast = ast.parse(source_code)
    assert len(parsed_ast.body[0].body) in {1, 2}, f'identity_matrix_comprehension should be a single statement, but it is {len(parsed_ast.body[0].body)}'
    return_expression = parsed_ast.body[0].body[-1]
    assert isinstance(return_expression, ast.Return), f'identity_matrix_comprehension last statement should be a return statement'
    ternary = return_expression.value
    assert isinstance(ternary, ast.IfExp), f'identity_matrix_comprehension does not use a list comprehension with a ternary if condition'
    list_comprehension = ternary.body
    assert isinstance(list_comprehension, ast.ListComp), f'identity_matrix_comprehension does not use a list comprehension with a ternary if condition'

@pytest.mark.skipif(
    not gateway2.exists() or unimplemented('is_identity'),
    reason="is_identity not implemented yet."
)
def test_gateway2_is_identity():
    from learn_python.module2_data_types.gateway2 import is_identity

    assert is_identity(None) is False, f'is_identity(None) should return False, but returns {is_identity(None)}'
    assert is_identity([]) is False, f'is_identity([]) should return False, but returns {is_identity([])}'
    
    assert is_identity([1]) is False, f'is_identity([1]) should return False, but returns {is_identity([1])}'
    assert is_identity([0]) is False, f'is_identity([0]) should return False, but returns {is_identity([0])}'

    assert is_identity([[1]]) is True, f'is_identity([[1]]) should return True, but returns {is_identity([[1]])}'
    assert is_identity([[0]]) is False, f'is_identity([[0]]) should return False, but returns {is_identity([[0]])}'

    assert is_identity([[1, 0], [0, 1]]) is True, f'is_identity([[1, 0], [0, 1]]) should return True, but returns {is_identity([[1, 0], [0, 1]])}'
    assert is_identity([[2, 0], [0, 1]]) is False, f'is_identity([[1, 0], [0, 1]]) should return True, but returns {is_identity([[2, 0], [0, 1]])}'
    assert is_identity([[1, 0], [0, 0]]) is False, f'is_identity([[1, 0], [0, 0]]) should return False, but returns {is_identity([[1, 0], [0, 0]])}'
    assert is_identity([[1, 0], [0, 1, 0]]) is False, f'is_identity([[1, 0], [0, 1, 0]]) should return False, but returns {is_identity([[1, 0], [0, 1, 0]])}'
    assert is_identity([[1, 0, 0], [0, 1, 0]]) is False, f'is_identity([[1, 0, 0], [0, 1, 0]]) should return False, but returns {is_identity([[1, 0, 0], [0, 1, 0]])}'
    assert is_identity([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) is True, f'is_identity([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) should return True, but returns {is_identity([[1, 0, 0], [0, 1, 0], [0, 0, 1]])}'
    assert is_identity([[1, 0, 0], [0, 0, 1], [0, 1, 0]]) is False, f'is_identity([[1, 0, 0], [0, 0, 1], [0, 1, 0]]) should return True, but returns {is_identity([[1, 0, 0], [0, 0, 1], [0, 1, 0]])}'

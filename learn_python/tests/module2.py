import io
from contextlib import redirect_stdout, redirect_stderr
import subprocess
from pathlib import Path
import sys
import pytest
from pprint import pformat
import ast
import inspect
from learn_python.tests.utils import (
    import_string,
    is_function_called,
    has_pass,
    has_docstring,
    num_statements,
    is_unimplemented,
    has_ternary,
    has_list_comprehension,
    has_set_comprehension,
    has_dict_comprehension,
    has_and,
    has_or,
    has_not,
    has_logical_operator,
    count_calls
)
import platform


modules = Path(__file__).parent.parent 
gateway2 = modules / 'module2_basics' / 'gateway2.py'


def unimplemented(function_name) -> bool:
    try:
        return is_unimplemented(
            import_string(
                f'learn_python.module2_basics.gateway2.{function_name}'
            )
        )
    except:
        return True


@pytest.mark.skipif(
    not gateway2.exists() or unimplemented('is_even'),
    reason='is_even not implemented yet.'
)
def test_gateway2_is_even():
    from learn_python.module2_basics.gateway2 import is_even as gateway_is_even

    def is_even(x):
        return x % 2 == 0

    for val in range(1000):
        assert gateway_is_even(val) == is_even(val), f'is_even({val}) should return {is_even(val)}, but returns {gateway_is_even(val)}'
    
    for val in range(-1000, 0):
        assert gateway_is_even(val) == is_even(val), f'is_even({val}) should return {is_even(val)}, but returns {gateway_is_even(val)}'


@pytest.mark.skipif(
    not gateway2.exists() or unimplemented('is_odd'),
    reason='is_odd not implemented yet.'
)
def test_gateway2_is_odd():
    try:
        from learn_python.module2_basics.gateway2 import is_even
    except ImportError:
        pytest.fail('is_even not implemented yet so you cannot have used it in your is_odd() implementation!')

    from learn_python.module2_basics.gateway2 import is_odd as gateway_is_odd

    def is_odd(x):
        return x % 2 == 1

    for val in range(1000):
        assert gateway_is_odd(val) == is_odd(val), f'is_odd({val}) should return {is_odd(val)}, but returns {gateway_is_odd(val)}'
    
    for val in range(-1000, 0):
        assert gateway_is_odd(val) == is_odd(val), f'is_odd({val}) should return {is_odd(val)}, but returns {gateway_is_odd(val)}'

    assert is_function_called(gateway_is_odd, is_even), f'is_odd() does not call is_even() - you must use is_even() to impelment is_odd()'


@pytest.mark.skipif(
    not gateway2.exists() or unimplemented('is_even_safe'),
    reason='is_even_safe not implemented yet.'
)
def test_gateway2_is_even_safe():
    from learn_python.module2_basics.gateway2 import is_even_safe

    def is_even(x):
        return x % 2 == 0

    for val in range(1000):
        assert is_even_safe(val) == is_even(val), f'is_even_safe({val}) should return {is_even(val)}, but returns {is_even_safe(val)}'
    
    for val in range(-1000, 0):
        assert is_even_safe(val) == is_even(val), f'is_even_safe({val}) should return {is_even(val)}, but returns {is_even_safe(val)}'

    assert is_even_safe(None) is None, f'is_even_safe(None) should return None, but returns {is_even_safe(None)}'


@pytest.mark.skipif(
    not gateway2.exists() or unimplemented('is_even_safe_ternary'),
    reason='is_even_safe_ternary not implemented yet.'
)
def test_gateway2_is_even_safe_ternary():
    from learn_python.module2_basics.gateway2 import is_even_safe_ternary

    def is_even(x):
        return x % 2 == 0

    for val in range(1000):
        assert is_even_safe_ternary(val) == is_even(val), f'is_even_safe_ternary({val}) should return {is_even(val)}, but returns {is_even_safe_ternary(val)}'
    
    for val in range(-1000, 0):
        assert is_even_safe_ternary(val) == is_even(val), f'is_even_safe_ternary({val}) should return {is_even(val)}, but returns {is_even_safe_ternary(val)}'

    assert is_even_safe_ternary(None) is None, f'is_even_safe_ternary(None) should return None, but returns {is_even_safe_ternary(None)}'

    assert has_ternary(is_even_safe_ternary), f'is_even_safe_ternary() does not use a ternary expression'
    assert num_statements(is_even_safe_ternary) == 2 and has_docstring(is_even_safe_ternary) or num_statements(is_even_safe_ternary) == 1, 'is_even_safe_ternary() should only require one statement, or one statement plus a docstring'


def check_logic_play(logic_play):
    pos_evens = list(range(100))[::2]
    pos_odds = list(range(100))[1::2]    
    
    neg_evens = list(range(-100))[::2]
    neg_odds = list(range(-100))[1::2]
    
    for lst1, lst2 in [
        (pos_evens, pos_evens),
        (pos_evens, neg_evens),
        (neg_evens, neg_evens),
        (neg_evens, pos_evens)
    ]:
        for x, y in zip(lst1, lst2):
            assert logic_play(x, y) == x * y, f'{logic_play.__name__}({x}, {y}) should return {x * y}, but returns {logic_play(x, y)}'

    for lst1, lst2 in [
        (pos_odds, pos_odds),
        (pos_odds, neg_odds),
        (neg_odds, neg_odds),
        (neg_odds, pos_odds)
    ]:
        for x, y in zip(lst1, lst2):
            assert logic_play(x, y) == x / y, f'{logic_play.__name__}({x}, {y}) should return {x / y}, but returns {logic_play(x, y)}'

    for lst1, lst2 in [
        (pos_evens, pos_odds),
        (pos_odds, pos_evens),
        (neg_odds, neg_evens),
        (neg_evens, neg_odds),
        (neg_evens, pos_odds),
        (pos_odds, neg_evens)
    ]:
        for x, y in zip(lst1, lst2):
            assert logic_play(x, y) is None, f'{logic_play.__name__}({x}, {y}) should return None, but returns {logic_play(x, y)}'


@pytest.mark.skipif(
    not gateway2.exists() or unimplemented('logic_play'),
    reason='logic_play not implemented yet.'
)
def test_gateway2_logic_play():
    from learn_python.module2_basics.gateway2 import logic_play
    check_logic_play(logic_play)
    assert has_and(logic_play), 'logic_play() does not use the logical operator "and"'


@pytest.mark.skipif(
    not gateway2.exists() or unimplemented('logic_play2'),
    reason='logic_play2 not implemented yet.'
)
def test_gateway2_logic_play2():
    from learn_python.module2_basics.gateway2 import logic_play2
    check_logic_play(logic_play2)
    assert not has_logical_operator(logic_play2), 'logic_play2() is not allowed to use any logical operators!'
    assert num_statements(logic_play2) <= 5 or has_docstring(logic_play2) and num_statements(logic_play2) <= 6, 'logic_play2() should only require 5 statements, or 5 statements plus a docstring'
    assert count_calls(logic_play2) <= 3, 'logic_play2() may only call another function a maximum of 3 times'
    

@pytest.mark.skipif(
    not gateway2.exists() or unimplemented('default_args'),
    reason='default_args not implemented yet.'
)
def test_gateway2_default_args():
    from learn_python.module2_basics.gateway2 import default_args

    signature = inspect.signature(default_args)
    assert len(signature.parameters) == 4, f'default_args() should have 4 parameters, but has {len(signature.parameters)}'
    for param in signature.parameters.values():
        assert param.default is not inspect.Parameter.empty, f'default_args() should have default values for all parameters, but {param.name} does not'
    
    default_params = {
        param: value.default
        for param, value in signature.parameters.items()
    }

    differing_params = {}
    for param, default in default_params.items():
        val = 0
        while val == default:
            val += 1
        differing_params[param] = val

    def call_str(params):
        return ', '.join([
            f'{param}={value}' for param, value in params.items()
        ])

    assert default_args() == (True, True, True, True), f'default_args() should return [True, True, True, True], but returns {default_args()}'
    assert default_args(**default_params) == (True, True, True, True), f'default_args({call_str(default_params)}) should return [True, True, True, True], but returns {default_args(**default_params)}'
    assert default_args(**differing_params) == (False, False, False, False), f'default_args({call_str(differing_params)}) should return [False, False, False, False], but returns {default_args(**differing_params)}'

    args = list(default_params.keys())

    test1 = {**default_params, args[0]: differing_params[args[0]]}
    assert default_args(**test1) == (False, True, True, True), f'default_args({call_str(test1)}) should return [False, True, True, True], but returns {default_args(**test1)}'

    test2 = {**default_params, args[1]: differing_params[args[1]]}
    assert default_args(**test2) == (True, False, True, True), f'default_args({call_str(test2)}) should return [True, False, True, True], but returns {default_args(**test2)}'

    test3 = {**default_params, args[2]: differing_params[args[2]]}
    assert default_args(**test3) == (True, True, False, True), f'default_args({call_str(test3)}) should return [True, True, False, True], but returns {default_args(**test3)}'

    test4 = {**default_params, args[3]: differing_params[args[3]]}
    assert default_args(**test4) == (True, True, True, False), f'default_args({call_str(test4)}) should return [True, True, True, False], but returns {default_args(**test4)}'

@pytest.mark.skipif(
    not gateway2.exists() or unimplemented('is_close'),
    reason='is_close not implemented yet.'
)
def test_gateway2_is_close():
    from learn_python.module2_basics.gateway2 import is_close

    assert is_close(0, 0) is True, f'is_close(0, 0) should return True, but returns {is_close(0, 0)}'
    assert is_close(0, 1) is False, f'is_close(0, 1) should return False, but returns {is_close(0, 1)}'
    assert is_close(1, 0) is False, f'is_close(1, 0) should return False, but returns {is_close(1, 0)}'
    assert is_close(1, 1) is True, f'is_close(1, 1) should return True, but returns {is_close(1, 1)}'

    assert is_close(0, 1e-10) is True, f'is_close(0, 1e-10) should return True, but returns {is_close(0, 1e-10)}'
    assert is_close(0, 1e-8) is False, f'is_close(0, 1e-8) should return True, but returns {is_close(0, 1e-8)}'

    assert is_close(0.0, 1e-10, 1e-11) is False, f'is_close(0.0, 1e-10, 1e-11) should return False, but returns {is_close(0, 1e-11, 1e-11)}'
    assert is_close(0.0, 1e-12, 1e-11) is True, f'is_close(0.0, 1e-12, 1e-11) should return True, but returns {is_close(0, 1e-12, 1e-11)}'

    assert not is_function_called(is_close, 'isclose'), f'isclose() should not call math.isclose()'


@pytest.mark.skipif(
    not gateway2.exists() or unimplemented('normal_distribution'),
    reason="normal_distribution not implemented yet."
)
def test_gateway2_normal_distribution():

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.stats import norm

    from learn_python.module2_basics.gateway2 import normal_distribution

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
    #fig.canvas.manager.window.attributes('-topmost', 1)  # Set the figure to be on top
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


@pytest.mark.skipif(
    not gateway2.exists() or unimplemented('are_same_object'),
    reason="are_same_object not implemented yet."
)
def test_gateway2_are_same_object():
    from learn_python.module2_basics.gateway2 import are_same_object

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
    from learn_python.module2_basics.gateway2 import identity_matrix

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
    from learn_python.module2_basics.gateway2 import identity_matrix_comprehension

    assert identity_matrix_comprehension(-1) is None
    assert identity_matrix_comprehension(0) == []
    assert is_identity(identity_matrix_comprehension(1), 1), f'identity_matrix_comprehension(1) is not correct: {pformat(identity_matrix_comprehension(1))}'
    assert is_identity(identity_matrix_comprehension(2), 2), f'identity_matrix_comprehension(2) is not correct: {pformat(identity_matrix_comprehension(2))}'
    assert is_identity(identity_matrix_comprehension(3), 3), f'identity_matrix_comprehension(3) is not correct: {pformat(identity_matrix_comprehension(3))}'
    assert is_identity(identity_matrix_comprehension(4), 4), f'identity_matrix_comprehension(4) is not correct: {pformat(identity_matrix_comprehension(4))}'
    assert is_identity(identity_matrix_comprehension(26), 26), f'identity_matrix_comprehension(26) is not correct: {pformat(identity_matrix_comprehension(26))}'

    assert num_statements(identity_matrix_comprehension) == 2 and has_docstring(identity_matrix_comprehension) or num_statements(identity_matrix_comprehension) == 1, 'identity_matrix_comprehension() should only require one statement, or one statement plus a docstring'
    assert has_list_comprehension(identity_matrix_comprehension), 'identity_matrix_comprehension() does not use a list comprehension'
    assert has_ternary(identity_matrix_comprehension), 'identity_matrix_comprehension() does not use a ternary if condition'
    try:
        from learn_python.module2_basics.gateway2 import identity_matrix
        assert not is_function_called(identity_matrix_comprehension, identity_matrix), 'identity_matrix_comprehension() should not call identity_matrix()'
    except ImportError:
        pass
    

@pytest.mark.skipif(
    not gateway2.exists() or unimplemented('is_identity'),
    reason="is_identity not implemented yet."
)
def test_gateway2_is_identity():
    from learn_python.module2_basics.gateway2 import is_identity

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

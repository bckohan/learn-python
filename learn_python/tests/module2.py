import io
from contextlib import redirect_stdout
from pathlib import Path
import pytest
from pprint import pformat
import ast
import inspect
from learn_python.tests.utils import *
from learn_python.tests.tasks import *
from functools import partial
import glob
import re


modules = Path(__file__).parent.parent 
gateway2_dir = modules / 'module2_basics' / 'gateway2'

task_re = re.compile(r'task(?P<number>\d+)_(?P<name>\w+).py')

module2_tasks = []
task_map = {}


def lists_compare(list1, list2):
    from learn_python.tests.utils import compare_floats
    return compare_floats(sorted(list1), sorted(list2))


def get_task_module(task_name, number=None):
    module_import = f'learn_python.module2_basics.gateway2.task{number}_{task_name}'
    try:
        return module_import, importlib.import_module(module_import)
    except (ImportError, ModuleNotFoundError):
        pass
    return module_import, None


def import_task(task_name, number=None):
    if number is None:
        task = task_map.get(task_name, None)
        if not task:
            return None
        number = task.number
    return import_string(f'{get_task_module(task_name, number)[0]}.{task_name}')


for task in glob.glob(str(gateway2_dir / 'task*.py')):
    task_path = Path(task)
    mtch = task_re.match(task_path.name)
    if mtch:
        task_name = mtch.groupdict()['name']
        number = int(mtch.groupdict()['number'])
        mod_str, task_mod = get_task_module(task_name, number)
        task = Task(
            number=number,
            name=task_name,
            path=task_path,
            test=f'learn_python.tests.module2.test_gateway2_{task_name}',
            function=import_task(task_name, number) or task_name,
            module='module2',
            modules=[task_mod or mod_str]
        )
        while len(module2_tasks) <= task.number:
            module2_tasks.append(None)
        module2_tasks[task.number] = task
        task_map[task.name] = task


def unimplemented(task_name) -> bool:
    task = task_map.get(task_name, None)
    if task:
        imported_task = import_task(task.name)
        if imported_task:
            return is_unimplemented(imported_task)
    return True


@pytest.mark.skipif(unimplemented('is_even'), reason='is_even not implemented yet.')
def test_gateway2_is_even():
    gateway_is_even = import_task('is_even')

    def is_even(x):
        return x % 2 == 0

    for val in range(1000):
        assert gateway_is_even(val) == is_even(val), f'is_even({val}) should return {is_even(val)}, but returns {gateway_is_even(val)}'
    
    for val in range(-1000, 0):
        assert gateway_is_even(val) == is_even(val), f'is_even({val}) should return {is_even(val)}, but returns {gateway_is_even(val)}'


@pytest.mark.skipif(unimplemented('is_odd'), reason='is_odd not implemented yet.')
def test_gateway2_is_odd():
    try:
        is_even = import_task('is_even')
    except ImportError:
        pytest.fail('is_even not implemented yet so you cannot have used it in your is_odd() implementation!')

    gateway_is_odd = import_task('is_odd')

    def is_odd(x):
        return x % 2 == 1

    for val in range(1000):
        assert gateway_is_odd(val) == is_odd(val), f'is_odd({val}) should return {is_odd(val)}, but returns {gateway_is_odd(val)}'
    
    for val in range(-1000, 0):
        assert gateway_is_odd(val) == is_odd(val), f'is_odd({val}) should return {is_odd(val)}, but returns {gateway_is_odd(val)}'

    assert is_function_called(gateway_is_odd, is_even), f'is_odd() does not call is_even() - you must use is_even() to implement is_odd()'


@pytest.mark.skipif(unimplemented('is_even_safe'), reason='is_even_safe not implemented yet.')
def test_gateway2_is_even_safe():
    is_even_safe = import_task('is_even_safe')

    def is_even(x):
        return x % 2 == 0

    for val in range(1000):
        assert is_even_safe(val) == is_even(val), f'is_even_safe({val}) should return {is_even(val)}, but returns {is_even_safe(val)}'
    
    for val in range(-1000, 0):
        assert is_even_safe(val) == is_even(val), f'is_even_safe({val}) should return {is_even(val)}, but returns {is_even_safe(val)}'

    assert is_even_safe(None) is None, f'is_even_safe(None) should return None, but returns {is_even_safe(None)}'


@pytest.mark.skipif(unimplemented('is_even_safe_ternary'), reason='is_even_safe_ternary not implemented yet.')
def test_gateway2_is_even_safe_ternary():
    is_even_safe_ternary = import_task('is_even_safe_ternary')

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


@pytest.mark.skipif(unimplemented('logic_play'), reason='logic_play not implemented yet.')
def test_gateway2_logic_play():
    logic_play = import_task('logic_play')
    check_logic_play(logic_play)
    assert has_and(logic_play), 'logic_play() does not use the logical operator "and"'


@pytest.mark.skipif(unimplemented('logic_play2'), reason='logic_play2 not implemented yet.')
def test_gateway2_logic_play2():
    logic_play2 = import_task('logic_play2')
    check_logic_play(logic_play2)
    assert not has_logical_operator(logic_play2), 'logic_play2() is not allowed to use any logical operators!'
    assert num_statements(logic_play2) <= 5 or has_docstring(logic_play2) and num_statements(logic_play2) <= 6, 'logic_play2() should only require 5 statements, or 5 statements plus a docstring'
    assert count_calls(logic_play2) <= 3, 'logic_play2() may only call another function a maximum of 3 times'
    

@pytest.mark.skipif(unimplemented('default_args'), reason='default_args not implemented yet.')
def test_gateway2_default_args():
    default_args = import_task('default_args')

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


@pytest.mark.skipif(unimplemented('get_delegate'), reason='get_delegate not implemented yet.')
def test_gateway2_get_delegate():
    get_delegate = import_task('get_delegate')
    delegate = get_delegate(None)
    assert delegate() == 0, f'get_delegate(None)() should return 0, but returns {delegate()}'
    def six():
        return 6
    assert get_delegate(six)() == 6, f'get_delegate(function)() should return function(), but returns {get_delegate(six)()}'
    assert has_func_definition(get_delegate), f'You must define the default delegate function inside get_delegate()'


@pytest.mark.skipif( unimplemented('is_close'), reason='is_close not implemented yet.')
def test_gateway2_is_close():
    is_close = import_task('is_close')

    assert is_close(0, 0) is True, f'is_close(0, 0) should return True, but returns {is_close(0, 0)}'
    assert is_close(0, 1) is False, f'is_close(0, 1) should return False, but returns {is_close(0, 1)}'
    assert is_close(1, 0) is False, f'is_close(1, 0) should return False, but returns {is_close(1, 0)}'
    assert is_close(1, 1) is True, f'is_close(1, 1) should return True, but returns {is_close(1, 1)}'

    assert is_close(0, 1e-10) is True, f'is_close(0, 1e-10) should return True, but returns {is_close(0, 1e-10)}'
    assert is_close(0, 1e-8) is False, f'is_close(0, 1e-8) should return True, but returns {is_close(0, 1e-8)}'

    assert is_close(0.0, 1e-10, 1e-11) is False, f'is_close(0.0, 1e-10, 1e-11) should return False, but returns {is_close(0, 1e-11, 1e-11)}'
    assert is_close(0.0, 1e-12, 1e-11) is True, f'is_close(0.0, 1e-12, 1e-11) should return True, but returns {is_close(0, 1e-12, 1e-11)}'

    assert not is_function_called(is_close, 'isclose'), f'isclose() should not call math.isclose()'


@pytest.mark.skipif(unimplemented('normal_distribution'), reason="normal_distribution not implemented yet.")
def test_gateway2_normal_distribution():

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.stats import norm

    normal_distribution = import_task('normal_distribution')

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
    if not passing:
        fig.suptitle('normal_distribution(): FAILING (close to continue)', fontsize=16, color='red')
        plt.show()
        pytest.fail("normal_distribution plots are not correct.")


@pytest.mark.skipif(unimplemented('type_divide'), reason='divide not implemented yet.')
def test_gateway2_type_divide():
    type_divide = import_task('type_divide')
    import math

    assert type_divide(1, 1) == 1, f'type_divide(1, 1) should return 1, but returns {type_divide(1, 1)}'
    assert type(type_divide(1, 1)) is int, f'type_divide(1, 1) should return an integer, but returns {type(type_divide(1, 1))}'
    assert type_divide(1, 2) == 0, f'type_divide(1, 2) should return 0, but returns {type_divide(1, 2)}'
    assert type(type_divide(1, 2)) is int, f'type_divide(1, 2) should return an integer, but returns {type(type_divide(1, 2))}'

    assert type_divide(1, 2.0) == 0.5, f'type_divide(1, 2.0) should return 0.5, but returns {type_divide(1, 2.0)}'
    assert type_divide(1.0, 2) == 0.5, f'type_divide(1.0, 2) should return 0.5, but returns {type_divide(1.0, 2)}'

    assert type_divide(3, 0) is None, f'type_divide(3, 0) should return None, but returns {type_divide(3, 0)}'
    assert type_divide(5.0, 0) is None, f'type_divide(5.0, 0) should return None, but returns {type_divide(5.0, 0)}'
    assert type_divide(5.5, 0.0) is None, f'type_divide(5.5, 0.0) should return None, but returns {type_divide(5.5, 0.0)}'

    assert math.isclose(type_divide(2.5, 1e-300), 2.5e300), f'type_divide(2.5, 1e-300) should return 2.5e300, but returns {type_divide(2.5, 1e-300)}'

@pytest.mark.skipif(unimplemented('get_decimal'), reason='get_decimal not implemented yet.')
def test_gateway2_get_decimal():
    get_decimal = import_task('get_decimal')
    from math import isclose

    assert get_decimal(0.0) == 0, f'get_decimal(0.0) should return 0.0, but returns {get_decimal(0.0)}'
    assert get_decimal(1.0) == 0, f'get_decimal(1.0) should return 0.0, but returns {get_decimal(1.0)}'
    assert isclose(get_decimal(1.1), 0.1), f'get_decimal(1.1) should return 0.1, but returns {get_decimal(1.1)}'
    assert isclose(get_decimal(1.9), 0.9), f'get_decimal(1.9) should return 0.9, but returns {get_decimal(1.9)}'
    assert isclose(get_decimal(3.14159), 0.14159), f'get_decimal(3.14159) should return 0.14159, but returns {get_decimal(3.14159)}'
    assert isclose(get_decimal(2.71828), 0.71828), f'get_decimal(2.71828) should return 0.71828, but returns {get_decimal(2.71828)}'
    assert isclose(get_decimal(-123.126662), -0.126662), f'get_decimal(-123.126662) should return -0.126662, but returns {get_decimal(-123.126662)}'
    assert isclose(get_decimal(8), 0.0), f'get_decimal(8) should return 0.0, but returns {get_decimal(8)}'
    assert type(get_decimal(8)) is float, f'get_decimal(8) should return a float, but returns {type(get_decimal(8))}'
    assert num_statements(get_decimal) == 1 or (num_statements(get_decimal) == 2 and has_docstring(get_decimal)), 'get_decimal() should only require one statement'


@pytest.mark.skipif(unimplemented('get_element'), reason='get_element not implemented yet.')
def test_gateway2_get_element():
    get_element = import_task('get_element')

    test_list = [0, 1, 2, 3, 4]

    assert get_element(test_list, 0) == 0, f'get_element({test_list}, 0) should return 0 but returned {get_element(test_list, 0)}'
    assert get_element(test_list, -5) == 0, f'get_element({test_list}, -5) should return 0 but returned {get_element(test_list, -5)}'

    assert get_element(test_list, 1) == 1, f'get_element({test_list}, 1) should return 1 but returned {get_element(test_list, 1)}'
    assert get_element(test_list, -4) == 1, f'get_element({test_list}, -4) should return 1 but returned {get_element(test_list, -4)}'

    assert get_element(test_list, 2) == 2, f'get_element({test_list}, 2) should return 2 but returned {get_element(test_list, 2)}'
    assert get_element(test_list, -3) == 2, f'get_element({test_list}, -3) should return 2 but returned {get_element(test_list, -3)}'

    assert get_element(test_list, 3) == 3, f'get_element({test_list}, 3) should return 3 but returned {get_element(test_list, 3)}'
    assert get_element(test_list, -2) == 3, f'get_element({test_list}, -2) should return 3 but returned {get_element(test_list, -2)}'

    assert get_element(test_list, 4) == 4, f'get_element({test_list}, 4) should return 4 but returned {get_element(test_list, 4)}'
    assert get_element(test_list, -1) == 4, f'get_element({test_list}, -1) should return 4 but returned {get_element(test_list, -1)}'

    assert get_element(test_list, 5) is None, f'get_element({test_list}, 5) should return None but returned {get_element(test_list, 5)}'
    assert get_element(test_list, -6) is None, f'get_element({test_list}, -6) should return None but returned {get_element(test_list, -6)}'
    
    assert get_element(test_list, 25) is None, f'get_element({test_list}, 25) should return None but returned {get_element(test_list, 25)}'
    assert get_element(test_list, -26) is None, f'get_element({test_list}, -26) should return None but returned {get_element(test_list, -26)}'


@pytest.mark.skipif(unimplemented('split'), reason='split not implemented yet.')
def test_gateway2_split():
    split = import_task('split')

    test_list = [0, 1, 2, 3, 4]

    assert split(test_list, 0) == ([], [0, 1, 2, 3, 4]), f'split({test_list}, 0) should return ([], [0, 1, 2, 3, 4]) but returned {split(test_list, 0)}'
    assert split(test_list, 1) == ([0], [1, 2, 3, 4]), f'split({test_list}, 1) should return ([0], [1, 2, 3, 4]) but returned {split(test_list, 1)}'
    assert split(test_list, 2) == ([0, 1], [2, 3, 4]), f'split({test_list}, 2) should return ([0, 1], [2, 3, 4]) but returned {split(test_list, 2)}'
    assert split(test_list, 3) == ([0, 1, 2], [3, 4]), f'split({test_list}, 3) should return ([0, 1, 2], [3, 4]) but returned {split(test_list, 3)}'
    assert split(test_list, 4) == ([0, 1, 2, 3], [4]), f'split({test_list}, 4) should return ([0, 1, 2, 3], [4]) but returned {split(test_list, 4)}'
    assert split(test_list, 5) == ([0, 1, 2, 3, 4], []), f'split({test_list}, 5) should return ([0, 1, 2, 3, 4], []) but returned {split(test_list, 5)}'
    assert split(test_list) == ([0, 1], [2, 3, 4]), f'split({test_list}) should return (([0, 1], [2, 3, 4])) but returned {split(test_list)}'
    assert split(test_list, None) == ([0, 1], [2, 3, 4]), f'split({test_list}, None) should return (([0, 1], [2, 3, 4])) but returned {split(test_list, None)}'
    assert split(test_list, -1) == ([1, 2, 3, 4], [0]), f'split({test_list}, -1) should return ([1, 2, 3, 4], [0]) but returned {split(test_list, -1)}'
    assert split(test_list, -2) == ([2, 3, 4], [0, 1]), f'split({test_list}, -2) should return ([2, 3, 4], [0, 1]) but returned {split(test_list, -2)}'
    assert split(test_list, -3) == ([3, 4], [0, 1, 2]), f'split({test_list}, -3) should return ([3, 4], [0, 1, 2]) but returned {split(test_list, -3)}'
    assert split(test_list, -4) == ([4], [0, 1, 2, 3]), f'split({test_list}, -4) should return ([4], [0, 1, 2, 3]) but returned {split(test_list, -4)}'
    assert split(test_list, -5) == ([], [0, 1, 2, 3, 4]), f'split({test_list}, -5) should return ([], [0, 1, 2, 3, 4]) but returned {split(test_list, -5)}'
    

@pytest.mark.skipif(unimplemented('decimate'), reason='decimate not implemented yet.')
def test_gateway2_decimate():
    from learn_python.tests.utils import float_range
    decimate = import_task('decimate')

    list1 = [1, 2, 3, 4, 5, 6]
    list2 = list(float_range(12, -3, 0.1))

    assert decimate(list1, 1) == [1, 2, 3, 4, 5, 6], f'decimate({list1}, 1) should return {list1}, but returns {decimate(list1, 1)}'
    assert decimate(list1, 2) == [1, 3, 5], f'decimate({list1}, 2) should return [1, 3, 5], but returns {decimate(list1, 2)}'
    assert decimate(list1, 3) == [1, 4], f'decimate({list1}, 3) should return [1, 4], but returns {decimate(list1, 3)}'
    assert decimate(list1, 4) == [1, 5], f'decimate({list1}, 4) should return [1, 5], but returns {decimate(list1, 4)}'
    assert decimate(list1) == [1] == decimate(list1, factor=10), f'decimate({list1}) should return [1], but returns {decimate(list1)}'

    assert decimate(list2, 1) == list2, f'decimate({list2}, 1) should return {list2}, but returns {decimate(list2, 1)}'
    assert decimate(list2) == list2[::10], f'decimate({list2}) should return {list2[::10]}, but returns {decimate(list2)}'
    assert decimate(list2, 25) == list2[::25], f'decimate({list2}) should return {list2[::25]}, but returns {decimate(list2, 25)}'



@pytest.mark.skipif(unimplemented('combine'), reason='combine not implemented yet.')
def test_gateway2_combine():
    combine = import_task('combine')
    from learn_python.tests.utils import float_range

    for expected, (list1, list2) in [
        ([(x, x+0.01) for x in range(0, 5)], ([x for x in range(0, 5)], [x+0.01 for x in range(0, 5)])),
        ([(x, x-1.56) for x in float_range(0, -1, 0.1)], ([x for x in float_range(0, -1, 0.1)], [x-1.56 for x in float_range(0, -1, 0.1)]))
    ]:
        assert combine(list1, list2) == expected, f'combine({list1}, {list2}) should return {expected}, but returns {combine(list1, list2)}'


@pytest.mark.skipif(unimplemented('split_name'), reason='split_name not implemented yet.')
def test_gateway2_split_name():
    split_name = import_task('split_name')
    
    assert split_name('brian christopher john kohan') == ('Brian', 'Christopher John', 'Kohan'), f'split_name("brian christopher john kohan") should return ("Brian", "Christopher John", "Kohan"), but returns {split_name("brian christopher john kohan")}'
    assert split_name('brian kohan') == ('Brian', None, 'Kohan'), f'split_name("brian kohan") should return ("Brian", None, "Kohan"), but returns {split_name("brian kohan")}'
    assert split_name('brian') == ('Brian', None, None), f'split_name("brian") should return ("Brian", None, None), but returns {split_name("brian")}'
    assert split_name('') == (None, None, None), f'split_name("") should return (None, None, None), but returns {split_name("")}'

    assert is_function_called(split_name, 'split'), 'split_name() must call str.split()'
    assert is_function_called(split_name, 'title'), 'split_name() must call str.title()'
    assert is_function_called(split_name, 'join'), 'split_name() must call str.join()'


@pytest.mark.skipif(unimplemented('label_names'), reason='label_names not implemented yet.')
def test_gateway2_label_names():
    label_names = import_task('label_names')
    
    assert label_names('Brian', 'Christopher John', 'Kohan') == 'first=Brian, middle=Christopher John, last=Kohan', f'label_names("Brian", "Christopher John", "Kohan") should return "first=Brian, middle=Christopher John, last=Kohan", but returns {label_names("Brian", "Christopher John", "Kohan")}'
    assert label_names('Brian', '', 'Kohan') == 'first=Brian, last=Kohan', f'label_names("Brian", "", "Kohan") should return "first=Brian, last=Kohan", but returns {label_names("Brian", "", "Kohan")}'
    assert label_names('Brian', None, None) == 'first=Brian', f'label_names("Brian", None, None) should return "first=Brian", but returns {label_names("Brian", None, None)}'
    assert label_names(None, None, None) == '', f'label_names(None, None, None) should return "", but returns {label_names(None, None, None)}'
    assert label_names('', '', '') == '', f'label_names("", "", "") should return "", but returns {label_names("", "", "")}'
    assert label_names(last='Kohan') == 'last=Kohan', f'label_names(last="Kohan") should return "last=Kohan", but returns {label_names(last="Kohan")}'

    assert is_function_called(label_names, 'append'), 'label_names() must call list.append()'
    assert has_statement(label_names, ast.JoinedStr), 'label_names() must use f-strings'
    assert is_function_called(label_names, 'join'), 'label_names() must call str.join()'


@pytest.mark.skipif(unimplemented('format_constant'), reason='format_constant not implemented yet.')
def test_gateway2_format_constant():
    format_constant = import_task('format_constant')
    get_decimal = import_task('get_decimal')
    assert get_decimal, 'format_constant() must call get_decimal() but get_decimal() has not been implemented.'

    assert format_constant('π', 3.141592653589793) == 'π        3.1416', f'format_constant("π", 3.141592653589793) should return "π        3.1416", but returns {format_constant("π", 3.141592653589793)}'
    assert format_constant('e', 2.718281828459045) == 'e        2.7183', f'format_constant("e", 2.718281828459045) should return "e        2.7183", but returns {format_constant("e", 2.718281828459045)}'
    assert format_constant('e', 2.718281828459045, decimals=6) == 'e      2.718282', f'format_constant("e", 2.718281828459045, decimals=6) should return "e      2.718282", but returns {format_constant("e", 2.718281828459045, decimals=6)}'
    assert format_constant('Golden Ratio', (1 + 5 ** 0.5) / 2, line_length=30) == 'Golden Ratio            1.6180', f'format_constant("Golden Ratio", (1 + 5 ** 0.5) / 2, line_length=30) should return "Golden Ratio            2.7183", but returns {format_constant("Golden Ratio", (1 + 5 ** 0.5) / 2, line_length=30)}'
    result_str = format_constant("Kaprekar's Constant", 6174, line_length=30, decimals=0)
    assert result_str == "Kaprekar's Constant       6174", f'format_constant("Kaprekar\'s Constant", 6174, line_length=30, decimals=0) should return "Kaprekar\'s Constant       6174", but returns {result_str}'
    result_str = format_constant("Kaprekar's Constant", 6174, line_length=30)
    assert result_str == "Kaprekar's Constant  6174.0000", f'format_constant("Kaprekar\'s Constant", 6174, line_length=30) should return "Kaprekar\'s Constant       6174.0000", but returns {result_str}'
    assert is_function_called(format_constant, get_decimal), 'format_constant() must call get_decimal()'
    assert is_function_called(format_constant, round), 'format_constant() must call round()'
    assert not has_format_specifier(format_constant), f'format_constant() cannot use an f-string format specifier: {has_format_specifier(format_constant)}' 
    assert num_statements(format_constant) == 3 or (num_statements(format_constant) == 4 and has_docstring(format_constant)), 'format_constant() should only require 3 statements'


@pytest.mark.skipif(unimplemented('format_constant2'), reason='format_constant2 not implemented yet.')
def test_gateway2_format_constant2():
    format_constant2 = import_task('format_constant2')

    assert format_constant2('π', 3.141592653589793) == 'π        3.1416', f'format_constant2("π", 3.141592653589793) should return "π        3.1416", but returns {format_constant2("π", 3.141592653589793)}'
    assert format_constant2('e', 2.718281828459045) == 'e        2.7183', f'format_constant2("e", 2.718281828459045) should return "e        2.7183", but returns {format_constant2("e", 2.718281828459045)}'
    assert format_constant2('e', 2.718281828459045, decimals=6) == 'e      2.718282', f'format_constant2("e", 2.718281828459045, decimals=6) should return "e      2.718282", but returns {format_constant2("e", 2.718281828459045, decimals=6)}'
    assert format_constant2('Golden Ratio', (1 + 5 ** 0.5) / 2, line_length=30) == 'Golden Ratio            1.6180', f'format_constant2("Golden Ratio", (1 + 5 ** 0.5) / 2, line_length=30) should return "Golden Ratio            2.7183", but returns {format_constant2("Golden Ratio", (1 + 5 ** 0.5) / 2, line_length=30)}'
    result_str = format_constant2("Kaprekar's Constant", 6174, line_length=30, decimals=0)
    assert result_str == "Kaprekar's Constant       6174", f'format_constant2("Kaprekar\'s Constant", 6174, line_length=30, decimals=0) should return "Kaprekar\'s Constant       6174", but returns {result_str}'
    result_str = format_constant2("Kaprekar's Constant", 6174, line_length=30)
    assert result_str == "Kaprekar's Constant  6174.0000", f'format_constant2("Kaprekar\'s Constant", 6174, line_length=30) should return "Kaprekar\'s Constant       6174.0000", but returns {result_str}'
    
    assert not is_function_called(format_constant2, 'get_decimal'), 'format_constant2() must not call get_decimal()'
    assert has_format_specifier(format_constant2), f'format_constant2() must use f-string format specifiers.' 
    assert not has_statement(format_constant2, ast.Mult), 'format_constant2() must not use *'
    assert not is_function_called(format_constant2, 'format_constant'), 'format_constant2() must not call format_constant()'
    assert num_statements(format_constant2) == 1 or (num_statements(format_constant2) == 2 and has_docstring(format_constant2)), 'format_constant2() should only require 1 statement'


@pytest.mark.skipif(unimplemented('ends_with'), reason='ends_with not implemented yet.')
def test_gateway2_ends_with():
    ends_with = import_task('ends_with')
    
    assert ends_with('anna maria  ', 'ria')
    assert ends_with('anna maria', 'anna mAria')
    assert not ends_with('anna maria', ' aria')
    assert ends_with('anna maria', ' maria')
    assert ends_with('Anna Maria', ' maria  ')
    assert not ends_with('anna maria', '  MARIA')
    
    assert ends_with('anna maria  ', 'ria'), f'ends_with("anna maria  ", "ria") should return True, but returns: {ends_with("anna maria  ", "ria")}'
    assert ends_with('anna maria', 'anna mAria'), f'ends_with("anna maria  ", "anna mAria") should return True, but returns: {ends_with("anna maria  ", "anna mAria")}'
    assert not ends_with('anna maria', ' aria'), f'ends_with("anna maria  ", " aria") should return False, but returns: {ends_with("anna maria  ", " aria")}'
    assert ends_with('anna maria', ' maria'), f'ends_with("anna maria  ", " maria") should return True, but returns: {ends_with("anna maria  ", " maria")}'
    assert ends_with('Anna Maria', ' maria  '), f'ends_with("Anna Maria  ", " maria  ") should return True, but returns: {ends_with("Anna Maria  ", " maria  ")}'
    assert not ends_with('anna maria', '  MARIA'), f'ends_with("anna maria  ", "  MARIA") should return False, but returns: {ends_with("anna maria  ", "  MARIA")}'


@pytest.mark.skipif(
    unimplemented('are_same_object'), reason="are_same_object not implemented yet."
)
def test_gateway2_are_same_object():
    are_same_object = import_task('are_same_object')

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


@pytest.mark.skipif(unimplemented('list_difference'), reason='list_difference not implemented yet.')
def test_gateway2_list_difference():
    list_difference = import_task('list_difference')
    from learn_python.tests.utils import float_range, compare_floats

    list1 = list(range(-5, 5))
    list2 = list(range(0, 10))

    list3 = list(float_range(2, -2, 0.1))
    list4 = [*list3[:len(list3)//2],  *float_range(2.1, 4, 0.1)]

    assert lists_compare(list_difference(list1, list2), list1[:list1.index(0)]), f'list_difference({list1}, {list2}) should return {list1[:list1.index(0)]}, but returns {list_difference(list1, list2)}'
    assert lists_compare(list_difference(list3, list4), list3[len(list3)//2:]), f'list_difference({list3}, {list4}) should return {list3[len(list3)//2:]}, but returns {list_difference(list3, list4)}'
    assert num_statements(list_difference) == 1 or (num_statements(list_difference) == 2 and has_docstring(list_difference)), 'list_difference() should only require 1 statement'
    assert is_function_called(list_difference, set), f'list_difference() must call set()'


@pytest.mark.skipif(unimplemented('deduplicate'), reason='deduplicate not implemented yet.')
def test_gateway2_deduplicate():
    deduplicate = import_task('deduplicate')
    from learn_python.tests.utils import float_range

    list1 = [-4, 4, 1, 2, 3, 1, 2, 3, 4]
    de_duplicated = deduplicate(list1)
    assert type(de_duplicated) is list, f'deduplicate({list1}) should return a list, but returns {type(de_duplicated)}'
    assert de_duplicated != [-4, 1, 2, 3, 4] and sorted(de_duplicated) == [-4, 1, 2, 3, 4], f'deduplicate({list1}) should return [-4, 1, 2, 3, 4], but returns {de_duplicated}'
    de_duplicated = deduplicate(list1, preserve_order=True)
    assert type(de_duplicated) is list, f'deduplicate({list1}, preserve_order=True) should return a list, but returns {type(de_duplicated)}'
    assert de_duplicated == [-4, 4, 1, 2, 3], f'deduplicate({list1}) should return [-4, 4, 1, 2, 3], but returns {de_duplicated}'
    assert num_statements(deduplicate) == 1 or (num_statements(deduplicate) == 2 and has_docstring(deduplicate)), 'deduplicate() should only require 1 statement'



@pytest.mark.skipif(unimplemented('separate'), reason='separate not implemented yet.')
def test_gateway2_separate():
    separate = import_task('separate')
    from learn_python.tests.utils import float_range

    for inpt, expected in [
        ([(x, x+0.01) for x in range(0, 5)], ([x for x in range(0, 5)], [x+0.01 for x in range(0, 5)])),
        ([(x, x-1.56) for x in float_range(0, -1, 0.1)], ([x for x in float_range(0, -1, 0.1)], [x-1.56 for x in float_range(0, -1, 0.1)]))
    ]:
        assert separate(inpt) == expected, f'separate({inpt}) should return {expected}, but returns {separate(inpt)}'


@pytest.mark.skipif(unimplemented('get_slices'), reason='get_slices not implemented yet.')
def test_gateway2_get_slices():
    get_slices = import_task('get_slices')

    test_list = [0, 1, 2, 3, 4]
    slices = [(0, 2), (3, None)]
    result = [0, 1, 3, 4]
    assert get_slices(test_list, [(0,2), (3,None)]) == result, f'get_slices({test_list}, {slices}) should return {result} but returns {get_slices(test_list, slices)}'

    slices = [(0, None), (2, -1)]
    result = [0, 1, 2, 3, 4, 2, 3]
    assert get_slices(test_list, slices) == result, f'get_slices({test_list}, {slices}) should return {result} but returns {get_slices(test_list, slices)}'

    slices = [(3, -1), (1, 4), (None, 100)]
    result = [3, 1, 2, 3, 0, 1, 2, 3, 4]
    assert get_slices(test_list, slices) == result, f'get_slices({test_list}, {slices}) should return {result} but returns {get_slices(test_list, slices)}'

    assert has_slice(get_slices), 'get_slices() must use a slice expression'
    
    assert has_for_loop(get_slices), 'get_slices() must use a for loop'
    assert has_statement(get_slices, ast.AugAssign), 'get_slices() must use the += operator'


@pytest.mark.skipif(unimplemented('list_intersection'), reason='list_intersection not implemented yet.')
def test_gateway2_list_intersection():
    list_intersection = import_task('list_intersection')
    from learn_python.tests.utils import float_range, compare_floats

    list1 = [1, 2, 4, 3]
    list2 = [6, 3, 4]
    assert list_intersection(list1, list2) == [4, 3, 3, 4]

    list3 = [None, 0, '3', '', None, 4.5, 5]
    list4 = [None, 0, 3, 4.5, '']
    expected = [None, 0, '', None, 4.5, None, 0, 4.5, '']
    assert list_intersection(list3, list4) == expected, f'list_intersection({list3}, {list4}) should return {expected} but returned {list_intersection(list3, list4)}'

    assert not is_function_called(list_intersection, set), f'list_intersection() must not call set()'
    assert has_for_loop(list_intersection), f'list_intersection() must use a for loop'


def check_is_fibonacci(numbers):
    if len(numbers) == 1:
        return numbers == [0]
    elif len(numbers) == 2:
        return numbers == [0, 1]
    for index, value in enumerate(numbers):
        if index > 2:
            if value != numbers[index-1] + numbers[index-2]:
                return False
    return True
    

@pytest.mark.skipif(unimplemented('fibonacci'), reason='fibonacci not implemented yet.')
def test_gateway2_fibonacci():
    from learn_python.tests.utils import float_range, compare_floats

    fibonacci = import_task('fibonacci')
    
    assert fibonacci(0) == [], f'fibonacci(0) should return [], but returns {fibonacci(0)}'
    assert fibonacci(1) == [0], f'fibonacci(1) should return [0], but returns {fibonacci(1)}'
    assert fibonacci(2) == [0, 1], f'fibonacci(2) should return [0, 1], but returns {fibonacci(2)}'
    assert fibonacci(3) == [0, 1, 1], f'fibonacci(3) should return [0, 1, 1], but returns {fibonacci(3)}'
    assert fibonacci(4) == [0, 1, 1, 2], f'fibonacci(4) should return [0, 1, 1, 2], but returns {fibonacci(4)}'
    assert fibonacci(5) == [0, 1, 1, 2, 3], f'fibonacci(5) should return [0, 1, 1, 2, 3], but returns {fibonacci(5)}'

    for length in [6, 12, 24, 37]:
        numbers = fibonacci(length)
        assert len(numbers) == length, f'fibonacci({length}) should return a list of length {length}, but returns {len(numbers)}'
        assert check_is_fibonacci(numbers), f'fibonacci({length}) == {numbers} is not a fibonacci sequence'

    assert has_while_loop(fibonacci), 'fibonacci() does not use a while loop!'


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


@pytest.mark.skipif(unimplemented('identity_matrix'), reason="identity_matrix not implemented yet.")
def test_gateway2_identity_matrix():
    identity_matrix = import_task('identity_matrix')

    assert identity_matrix(-1) is None
    assert identity_matrix(0) == []
    assert is_identity(identity_matrix(1), 1), f'identity_matrix(1) is not correct: {pformat(identity_matrix(1))}'
    assert is_identity(identity_matrix(2), 2), f'identity_matrix(2) is not correct: {pformat(identity_matrix(2))}'
    assert is_identity(identity_matrix(3), 3), f'identity_matrix(3) is not correct: {pformat(identity_matrix(3))}'
    assert is_identity(identity_matrix(4), 4), f'identity_matrix(4) is not correct: {pformat(identity_matrix(4))}'
    assert is_identity(identity_matrix(26), 26), f'identity_matrix(26) is not correct: {pformat(identity_matrix(26))}'
    assert has_for_loop(identity_matrix), 'identity_matrix() does not use any for loops'


@pytest.mark.skipif(unimplemented('is_identity'), reason="is_identity not implemented yet.")
def test_gateway2_is_identity():
    is_identity = import_task('is_identity')

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


@pytest.mark.skipif(unimplemented('identity_matrix2'),  reason="identity_matrix2 not implemented yet.")
def test_gateway2_identity_matrix2():
    identity_matrix2 = import_task('identity_matrix2')

    assert identity_matrix2(-1) is None
    assert identity_matrix2(0) == []
    assert is_identity(identity_matrix2(1), 1), f'identity_matrix2(1) is not correct: {pformat(identity_matrix2(1))}'
    assert is_identity(identity_matrix2(2), 2), f'identity_matrix2(2) is not correct: {pformat(identity_matrix2(2))}'
    assert is_identity(identity_matrix2(3), 3), f'identity_matrix2(3) is not correct: {pformat(identity_matrix2(3))}'
    assert is_identity(identity_matrix2(4), 4), f'identity_matrix2(4) is not correct: {pformat(identity_matrix2(4))}'
    assert is_identity(identity_matrix2(26), 26), f'identity_matrix2(26) is not correct: {pformat(identity_matrix2(26))}'

    assert num_statements(identity_matrix2) == 2 and has_docstring(identity_matrix2) or num_statements(identity_matrix2) == 1, 'identity_matrix2() should only require one statement, or one statement plus a docstring'
    assert has_list_comprehension(identity_matrix2), 'identity_matrix2() does not use a list comprehension'
    assert has_ternary(identity_matrix2), 'identity_matrix2() does not use a ternary if condition'
    try:
        from learn_python.module2_basics.gateway2.task0_is_even import identity_matrix
        assert not is_function_called(identity_matrix2, identity_matrix), 'identity_matrix2() should not call identity_matrix()'
    except ImportError:
        pass


@pytest.mark.skipif(unimplemented('fibonacci_gr'), reason='fibonacci_gr not implemented yet.')
def test_gateway2_fibonacci_gr():
    fibonacci_gr = import_task('fibonacci_gr')
    from learn_python.tests.utils import float_range, compare_floats
    
    for tol in [1e-2, 1e-3, 1e-6, 1e-8, 1e-12, 1e-100]:
        numbers = fibonacci_gr(tol)
        assert check_is_fibonacci(numbers), f'fibonacci({tol}) == {numbers} is not a fibonacci sequence'
        assert abs(numbers[-1] / numbers[-2] - ((1 + 5 ** 0.5) / 2)) < tol, f'fibonacci({tol:.2E}) produced {len(numbers)} numbers and did not reach the tolerance {tol:.2E}. Last ratio: {numbers[-1] / numbers[-2]:.12f}'
        assert abs(numbers[-2] / numbers[-3] - ((1 + 5 ** 0.5) / 2)) > tol,  f'fibonacci({tol:.2E}) produced {len(numbers)} numbers and went past the tolerance {tol:.2E}. Ratio before last: {numbers[-2] / numbers[-3]:.12f}'

    assert has_break(fibonacci_gr), 'fibonacci() does not use a break statement!'


@pytest.mark.skipif(unimplemented('float_range'), reason='float_range not implemented yet.')
def test_gateway2_float_range():
    float_range = import_task('float_range')

    assert compare_floats(float_range(0, 1, 0.1), [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]), f'float_range(0, 1, 0.1) should return [0, 0.1, 0.2, 0.3, 0.4, 0.5, ..., 1], but returns {float_range(0, 1, 0.1)}'
    assert compare_floats(float_range(0, -1, -0.1), [0, -0.1, -0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9, -1]), f'float_range(0, -1, -0.1) should return [0, -0.1, -0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9, -1], but returns {float_range(0, -1, -0.1)}'
    assert compare_floats(float_range(0, -1, -0.1), float_range(0, -1, 0.1)), f'float_range(0, -1, -0.1) should return the same as float_range(0, -1, 0.1), but returns {float_range(0, -1, -0.1)}'
    assert compare_floats(float_range(0, -1.01, -0.1), float_range(0, -1, -0.1)), f'float_range(0, -1.01, -0.1) should return the same as float_range(0, -1, -0.1), but returns {float_range(0, -1.01, -0.1)}'
    assert compare_floats(float_range(3, 2, -0.5), [3, 2.5, 2]), f'float_range(3, 2, -0.5) should return [3, 2.5, 2], but returns {float_range(3, 2, -0.5)}'
    assert compare_floats(float_range(1e-12, 2e-12, 2e-13), [1e-12, 1.2e-12, 1.4e-12, 1.6e-12, 1.8e-12, 2e-12]), f'float_range(1e-12, 2e-12, 2e-13) should return [1e-12, 1.2e-12, 1.4e-12, 1.6e-12, 1.8e-12, 2e-12], but returns {float_range(1e-12, 2e-12, 1e-13)}'
    assert compare_floats(float_range(0.099, 0.297, 0.099), [0.099, 0.198, 0.297]), f'float_range(0.099, 0.297, 0.099) should return [0.099, 0.198, 0.297], but returns {float_range(0.099, 0.297, 0.099)}'

@pytest.mark.skipif(unimplemented('xy_values'), reason='xy_values not implemented yet.')
def test_gateway2_xy_values():
    xy_values = import_task('xy_values')
    from learn_python.tests.utils import float_range
    from math import isclose

    def normal(x, σ=1, μ=0):
        from math import pi, sqrt, exp
        return 1 / (σ * sqrt(2 * pi)) * exp(-0.5 * ((x - μ) / σ) ** 2)
    
    def poisson(x, λ=1):
        from math import exp
        from math import factorial as fact
        return exp(-λ) * λ ** int(x) / fact(int(x))

    params = [
        (normal, ({'σ': 1, 'μ': 0}, (-3, 3, 0.01))),     # normal(σ=1, μ=0)
        (normal, ({'σ': 1, 'μ': 2}, (-2, 6, 0.05))),     # normal(σ=1, μ=2)
        (normal, ({'σ': 0.5, 'μ': 0}, (-2, 2, 0.005))),  # normal(σ=0.5, μ=0)
        (normal, ({'σ': 2, 'μ': 2}, (-4, 8, 0.1))),      # normal(σ=2, μ=2)
        (poisson, ({'λ': 0.5}, (0, 4, 1))),              # poisson(λ=0.5)
        (poisson, ({'λ': 1}, (0, 6, 1))),                # poisson(λ=1)
        (poisson, ({'λ': 2}, (0, 8, 1))),                # poisson(λ=2)
        (poisson, ({'λ': 3}, (0, 10, 1))),               # poisson(λ=3)
        (poisson, ({'λ': 6}, (0, 12, 1))),               # poisson(λ=6)
    ]

    for pdf, (kwargs, (x_min, x_max, step)) in params:
        x_range = list(float_range(x_min, x_max, step))
        returned = xy_values(partial(pdf, **kwargs), start=x_min, stop=x_max, step=step)
        assert len(returned) == len(x_range), f'xy_values({str(pdf)}, start={x_min}, stop={x_max}, step={step}) should return {len(x_range)} values, but returns {len(returned)}'
        expected = [(x, pdf(x, **kwargs)) for x in x_range]
        for index, (exp, ret) in enumerate(zip(expected, returned)):
            assert isclose(exp[0], ret[0]), f'xy_values(partial({pdf.__name__}, {kwargs}), start={x_min}, stop={x_max}, step={step})[{index}] x value == {ret[0]} when {exp[0]} was expected.'
            assert isclose(exp[1], ret[1]), f'xy_values(partial({pdf.__name__}, {kwargs}), start={x_min}, stop={x_max}, step={step})[{index}] y value == {ret[1]} when {exp[1]} was expected'


@pytest.mark.skipif(unimplemented('approximate_integral'), reason='approximate_integral not implemented yet.')
def test_gateway2_approximate_integral():
    approximate_integral = import_task('approximate_integral')
    from learn_python.tests.utils import float_range
    from math import isclose

    def normal(x, σ=1, μ=0):
        from math import pi, sqrt, exp
        return 1 / (σ * sqrt(2 * pi)) * exp(-0.5 * ((x - μ) / σ) ** 2)
    
    def xy_values(pdf, start, stop, step):
        return [(x, pdf(x)) for x in float_range(start, stop, step)]

    try:
        approximate_integral([])
        assert False, 'approximate_integral() should raise an AssertionError if the list of xy values is empty'
    except AssertionError:
        pass
    for pdf, (kwargs, (x_min, x_max, step)) in [
        (normal, ({'σ': 1, 'μ': 0}, (-6, 6, 0.04))),      # normal(σ=1, μ=0)
        (normal, ({'σ': 1, 'μ': 2}, (-4, 8, 0.04))),      # normal(σ=1, μ=2)
        (normal, ({'σ': 0.5, 'μ': 0}, (-4, 4, 0.005))),   # normal(σ=0.5, μ=0)
        (normal, ({'σ': 2, 'μ': 2}, (-8, 12, 0.1))),      # normal(σ=2, μ=2)
    ]:
        xy = xy_values(partial(pdf, **kwargs), start=x_min, stop=x_max, step=step)
        area = approximate_integral(xy)
        assert isclose(area, 1.0, abs_tol=.01), f'approximate_integral() should return ~1.0 for any normal distribution, but returns {area}'
        assert num_statements(approximate_integral) == 2 or (num_statements(approximate_integral) == 3 and has_docstring(approximate_integral)), 'approximate_integral() should only require 2 statements'
        assert count_statements(approximate_integral, ast.ListComp) == 2, 'approximate_integral() implementation should use 2 list comprehensions'
        assert count_statements(approximate_integral, ast.Slice) == 2, 'approximate_integral() implementation should use 2 slices'
        assert count_calls(approximate_integral, sum) == 2, 'approximate_integral() implementation should use 2 calls to sum()'


@pytest.mark.skipif(unimplemented('add_to_list'), reason="add_to_list not implemented yet.")
def test_gateway2_add_to_list():
    add_to_list = import_task('add_to_list')
    my_list = [1, 2, 3]
    appended = add_to_list(my_list, 4, 5)
    assert appended == [1, 2, 3, 4, 5], f'add_to_list(my_list, 4, 5) should return the list [[1, 2, 3, 4, 5]] but returns {add_to_list(my_list, 4, 5)}'
    assert appended is not my_list, f'mutate=False should not modify the list that was passed in'
    mutated = add_to_list(my_list, 6, 7, 8, mutate=True)
    assert mutated == [1, 2, 3, 6, 7, 8], f'add_to_list(my_list, 6, 7, 8, mutate=True) should return the list [[1, 2, 3, 6, 7, 8]] but returns {add_to_list(my_list, 6, 7, 8, mutate=True)}'
    assert mutated is my_list, f'mutate=True should modify the list that was passed in'


@pytest.mark.skipif(unimplemented('time_function'), reason="time_function not implemented yet.")
def test_gateway2_time_function():
    time_function = import_task('time_function')
    from time import perf_counter

    def func_to_time(*args, **kwargs):
        return args, kwargs
    
    start = perf_counter()
    seconds, result = time_function(func_to_time, 1, 2, 3, a=4, b=5, c=6)
    test_time = perf_counter() - start
    
    assert seconds > 0, f'time_function(func_to_time, 1, 2, 3, a=4, b=5, c=6) should return a positive number of seconds, but returns {seconds}'
    assert test_time > seconds, f'time_function(func_to_time, 1, 2, 3, a=4, b=5, c=6) should return a number of seconds less than the time it took to run the test {test_time}, but returns {seconds}'
    assert result == ((1, 2, 3), {'a': 4, 'b': 5, 'c': 6}), f'time_function(func_to_time, 1, 2, 3, a=4, b=5, c=6) should return ((1, 2, 3), {{\'a\': 4, \'b\': 5, \'c\': 6}}), but returns {result}'


@pytest.mark.skipif(unimplemented('list_intersection2'), reason='list_intersection2 not implemented yet.')
def test_gateway2_list_intersection2():
    list_intersection2 = import_task('list_intersection2')
    from learn_python.tests.utils import float_range, compare_floats

    list1 = [1, 2, 4, 3]
    list2 = [6, 3, 4]
    assert list_intersection2(list1, list2) == [4, 3, 3, 4]

    list3 = [None, 0, '3', '', None, 4.5, 5]
    list4 = [None, 0, 3, 4.5, '']
    expected = [None, 0, '', None, 4.5, None, 0, 4.5, '']
    assert list_intersection2(list3, list4) == expected, f'list_intersection2({list3}, {list4}) should return {expected} but returned {list_intersection2(list3, list4)}'

    assert not is_function_called(list_intersection2, set), f'list_intersection2() must not call set()'
    assert not has_for_loop(list_intersection2), f'list_intersection2() must not use a for loop'
    assert num_statements(list_intersection2) == 2 and has_docstring(list_intersection2) or num_statements(list_intersection2) == 1, 'list_intersection2() should only require one statement, or one statement plus a docstring'
    assert has_list_comprehension(list_intersection2), f'list_intersection2() does not use a list comprehension'


# test scenario
candidates = {
    0: 'Ada Lovelace',
    1: 'Grace Hopper',
    2: 'Annie Easley',
    3: 'Katherine Johnson'
}
ballots = [
    *[[0, 2, 3]] * 6,  # 6 ballots look like [Ada, Annie, Katherine]
    *[[1, 3, 2]] * 4,  # 4 ballots look like [Grace, Katherine, Annie]
    *[[2, 0, 1, 3]] * 2,
    *[[2, 3]] * 2,
    *[[2, 1]] * 1,
    *[[3, 1, 0, 2]] * 2,
    [3]
]

@pytest.mark.skipif(unimplemented('ranked_choice'), reason="ranked_choice not implemented yet.")
def test_gateway2_ranked_choice():
    ranked_choice = import_task('ranked_choice')

    scenario1 = ranked_choice(candidates, ballots)
    assert scenario1['winner'] == 'Ada Lovelace', "Ada Lovelace should have won! Not: {scenario1['winner']}"
    assert len(scenario1['rounds']) == 3, f"The test election scenario should have had 3 rounds! Not: {len(scenario1['rounds'])}"
    assert len(scenario1['rounds']) == 3, f"The test election scenario should have had 3 rounds! Not: {len(scenario1['rounds'])}"

    round1 = scenario1['rounds'][0]
    round2 = scenario1['rounds'][1]
    round3 = scenario1['rounds'][2]

    assert round1['votes'] == 18, f"Round 1 should have had 18 votes! Not: {round1['votes']}"
    assert round2['votes'] == 17, f"Round 2 should have had 17 votes! Not: {round2['votes']}"
    assert round3['votes'] == 15, f"Round 2 should have had 15 votes! Not: {round3['votes']}"

    round1_result = [('Ada Lovelace', 6), ('Annie Easley', 5), ('Grace Hopper', 4), ('Katherine Johnson', 3)]
    round2_result = [('Ada Lovelace', 6), ('Grace Hopper', 6), ('Annie Easley', 5)]
    round3_result = [('Ada Lovelace', 8), ('Grace Hopper', 7)]
    assert round1['ranking'] == round1_result, f"Round 1 ranking is not correct: {round1['ranking']} - expected: {round1_result}" 
    assert round2['ranking'] == round2_result, f"Round 2 ranking is not correct: {round2['ranking']} - expected: {round2_result}" 
    assert round3['ranking'] == round3_result, f"Round 3 ranking is not correct: {round3['ranking']} - expected: {round3_result}" 



@pytest.mark.skipif(unimplemented('ranked_choice') or unimplemented('print_report'), reason="ranked_choice and/or print_report not implemented yet.")
def test_gateway2_print_report():
    ranked_choice, print_report = import_task('ranked_choice'), import_task('print_report')

    f = io.StringIO()
    with redirect_stdout(f):
        print_report(ranked_choice(candidates, ballots))
    output = f.getvalue().split('\n')

    assert output[0] == '-' * 32, "line 0 should be 32 dashes."
    assert output[1] == 'Round 0', "line 1 should be 'Round 0'"
    assert output[2] == '       Ada Lovelace:  6 (33.33%)', "Line 2 should be '       Ada Lovelace:  6 (33.33%)'"
    assert output[3] == '       Annie Easley:  5 (27.78%)', "Line 3 should be '       Annie Easley:  5 (27.78%)'"
    assert output[4] == '       Grace Hopper:  4 (22.22%)', "Line 3 should be '       Grace Hopper:  4 (22.22%)'"
    assert output[5] == '  Katherine Johnson:  3 (16.67%)', "Line 3 should be '  Katherine Johnson:  3 (16.67%)'"
    assert output[6] == '-' * 32, "line 6 should be 32 dashes."
    assert output[7] == 'Round 1', "line 7 should be 'Round 1'"
    assert output[8] == '       Ada Lovelace:  6 (35.29%)', "Line 2 should be '       Ada Lovelace:  6 (35.29%)'"
    assert output[9] == '       Grace Hopper:  6 (35.29%)', "Line 2 should be '       Grace Hopper:  6 (35.29%)'"
    assert output[10] == '       Annie Easley:  5 (29.41%)', "Line 2 should be '       Annie Easley:  5 (29.41%)'"
    assert output[11] == '-' * 32, "line 11 should be 32 dashes."
    assert output[12] == 'Round 2 (Winner: Ada Lovelace)', "line 12 should be 'Round 2 (Winner: Ada Lovelace)'"
    assert output[13] == '       Ada Lovelace:  8 (53.33%)', "Line 13 should be '       Ada Lovelace:  8 (53.33%)'"
    assert output[14] == '       Grace Hopper:  7 (46.67%)', "Line 14 should be '       Grace Hopper:  7 (46.67%)'"

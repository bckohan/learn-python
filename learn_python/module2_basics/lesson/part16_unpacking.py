"""
The * and ** operators can be used as unary operators to unpack sequences.

This is shorthand that can be used to avoid writing additional loops.
It can be hard to parse until you know to look for it so lets go through
some examples!
"""
from learn_python.module2_basics.lesson.part15_dictionaries import *

# when you see a * followed by a sequence, read it as "unpack the
# inner sequence into the outer sequence". The below line unpacks the 
# inner list into the outer list.
assert [*[1, 2, 3]] == [1, 2, 3]

# this line unpacks multiple lists into one list
assert [*[1, 2, 3], *[4, 5]] == [1, 2, 3, 4, 5]

# the * operator works on any sequence, not just lists
assert [*{1, 2, 3, 1, 2}] == [1, 2, 3]
# the above line creates a set literal (which eliminates duplicates) then
# the * operator unpacks that set into the containing list.

# the * operator can also be used to unpack a string into a list of characters
# because strings are sequences of characters!
assert [*'hello'] == ['h', 'e', 'l', 'l', 'o']

# recall that when you iterate a dictionary without .items() you just get the keys
# so the below line unpacks the keys of the dictionary into a set
assert {*{'a': 1, 'b': 2}} == {'a', 'b'}

# if you want to unpack both the keys and values of a dictionary you can use
# the ** operator - but the containing sequence must also be a dictionary!
assert {**{'a': 1, 'b': 2}} == {'a': 1, 'b': 2}

# why is this helpful? you can combine different dictionaries easily:
assert {
    **{'a': 1, 'b': 2},
    **{'b': 5}
} == {'a': 1, 'b': 5}
# notice that the second dictionary overwrote the value of 'b' in the first

# we've been using literals - but you can also use variables:
assert (*my_list,) == (1, 2, 3, 4)
# ^ recall, a single value tuple needs a trailing comma

# Unpacking into function call arguments.
# You can unpack lists into the arguments of functions in order and dictionaries
# into any arguments, so long as the keys match the name:

def do_something(arg1, arg2, arg3=5):
    return arg1, arg2, arg3

assert do_something(*[1, 2, 3]) == (1, 2, 3)
assert do_something(*[1, 2]) == (1, 2, 5)
assert do_something(*[1, 2], -3) == (1, 2, -3)
assert do_something(-1, *[2, 3]) == (-1, 2, 3)

assert do_something(**{'arg2': 2, 'arg3': 3, 'arg1': 1}) == (1, 2, 3)
assert do_something(arg3=-3, **{'arg2': 2, 'arg1': 1}) == (1, 2, -3)

assert do_something(*[1], **{'arg2': 2, 'arg3': 3}) == (1, 2, 3)

# This allows us to pass around and manipulate the arguments to functions
# before the call is made. In some situations this can help keep our code
# DRY - we will see examples of how it is useful in later modules.

options = {
    'color': 'red',
    'line_style': '--'
}

def plot(line_style='-', color='black', line_width=1):
    return line_style, color, line_width

assert plot(**options) == ('--', 'red', 1)


# Variadic Functions
# the other place you will see * and ** as unary operators is in the 
# definition of variadic functions. That is, functions that accept
# a variable number of positional or named arguments:

def variadic_function(*args, **kwargs):
    # args is a tuple of positional argument values
    assert type(args) == tuple
    # kwargs is a dictionary where the keys are the argument names and the 
    # values are the values
    assert type(kwargs) == dict
    return args, kwargs

assert variadic_function(1, 2, 3, a=1, b=2) == ((1, 2, 3), {'a': 1, 'b': 2})

# the names "args" and "kwargs" (which stands for key-word arguments) are often 
# used by convention - you could use whatever names you want followed by the
# * and ** operators.

def only_kwargs(**kwargs):
    return kwargs

# you cant do this: only_kwargs(1, 2)

# but you can do this!
assert only_kwargs(a=1, b=2) == {'a': 1, 'b': 2}

def only_args(*args):
    return args

assert only_args('a', 'b', 'c') == ('a', 'b', 'c')


# why is this useful? It can make your code more readable by removing
# the need to use a list literal:
def add(*args):
    return sum(args)

assert add(1, 2, 3) == 6
assert add(3, 3) == 6

# Often the choice to use a variadic function is a stylistic one because
# they are functionally equivalent to passing a list and/or a dictionary as
# arguments. Using them can make the function calls a bit more clear in certain
# situations. A good rule of thumb is that anywhere you might want to call a 
# function with a dictionary literal as its main argument, you should consider using
# a variadic function that takes key word arguments.

# Another very good reason to use variadic arguments is when one function calls another
# and you do not know if the second function will be changed to accept additional 
# arguments in the future. In this situation you can use variadic arguments to pass
# arguments through:

def wrapped(**kwargs):
    return kwargs

def wrapper(my_arg=False, **kwargs):
    if my_arg:
        return wrapped(**kwargs)
    return {}

# notice below how kwargs only captures the arguments that are not named in the
# in the other part of the function signature
assert wrapper(my_arg=True, a=1, b=2) == {'a': 1, 'b': 2}
assert wrapper(d=4, e=5) == {}

# this particular pattern enables some pretty fancy stuff in python - for example
# decorators which we will cover in a later module


# ****************************************************************************
# Do Gateway 2 tasks 22-40 before proceeding to the next module!             *
# ****************************************************************************


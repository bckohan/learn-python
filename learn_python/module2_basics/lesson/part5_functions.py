"""
We talked about basic function definitions last time - but here's a few more
things to know about python functions.
"""
from learn_python.module2_basics.lesson.part4_ternary_if_else import *


# 1) They can have default arguments! For example, when called if the y
#    argument is not supplied it will default to 2
def add(x, y=2):
    return x + y

assert add(1) == 3
assert add(1, 5) == 6

# 2) If functions do not return anything, their return value is None
def returns_nothing():
    pass

assert returns_nothing() is None

# the above is equivalent to:
def also_returns_nothing():
    return None

assert also_returns_nothing() is returns_nothing() is None

# 3) Functions can return multiple values! This is a very common pattern in
#    python:
def returns_multiple_values():
    return 1, 2, 3

a, b, c = returns_multiple_values()

assert a == 1 and b == 2 and c == 3

# 4) Function arguments can be passed by name, this is useful when you have 
#    many default arguments:
def lots_of_args(w=0, x=1, y=2, z=3):
    return w, x, y, z

# if you wanted to invoke lots_of_args and only use a non-default value for z
# you could call it like this:
assert lots_of_args(0, 1, 2, 4) == (0, 1, 2, 4)

# or you could call it like this:
assert lots_of_args(z=4) == (0, 1, 2, 4)  # much simpler huh?

# not only is the second version simpler, it is more robust! If the maintainer
# of lots_of_args decided to change the values of the defaults in a future
# version, your invocation of the function in the first example would be
# "hard coded" to the original default values!

# When should you provide default arguments for your function? Usually anytime
# you can think of a "reasonable default". Many functions do a lot of work
# for you to execute some complex task that can be "configured" via various
# parameters, so think of defaults as providing a sensible basic configuration
# For example, you might have a function that plots a graph and one of the inputs
# might be the color of the line to use. Maybe a reasonable default for that color
# is black: plot(data, color='black')

# 5) Functions can have multiple return statements, that are hit by different
#    logic conditions - but only one will execute per invocation because once
#    you return - you are out of the function!
def multiple_returns(x):
    """
    6) Functions can have docstrings too! Try:
        from learn_python.module2_basics import lesson
        help(lesson.multiple_returns)
    
    This function returns either -1, 0, or 1 depending on if
    the value of x is negative (-1), zero (0), or positive (1).

    :param x: int - the value to return the sign of
    :return: int - -1 if x is negative, 0 if x is zero, 1 if x is positive
    """
    if x < 0:
        return -1
    elif x > 0:
        return 1
    return x  # we could have put this in an else statement, but this is 
              # functionally equivalent and less code!

assert multiple_returns(-1123) == -1
assert multiple_returns(0) == 0
assert multiple_returns(1123) == 1

# 7) In python you can store practically anything in a variable - including
# functions!

my_function = add
assert my_function(1, 2) == 3

# this means you can pass functions as arguments to other functions!
def apply_function(func):
    return func(1, 2)

assert apply_function(add) == 3

# this is a technique or pattern called "inversion of control" or delegation
# it can be very powerful in situations where you want to plug-in different
# specific behavior to the overall business logic of your program.

# when we store a function in a variable, we can "bind" some or all of its
# arguments, using the partial function from the functools package in the
# standard library
from functools import partial

add_one = partial(add, y=1)
assert add_one(2) == 3 == add(2, 1)
assert add_one(5) == 6 == add(5, 1)

add_one_to_five = partial(add, x=1, y=5)
assert add_one_to_five() == 6

# 8) naming arguments in a function call
def function_args(arg1, arg2, arg3=None, arg4=None):
    return arg1, arg2, arg3, arg4

# you do not have to not have to pass arguments into python functions in the
# order they appear in the function definition - IF you name them in your
# function call - it is often good practice to name arguments in function
# calls - this can make your code more robust to future changes to the function
# definition
assert function_args(1, 2, 3, 4) == (1, 2, 3, 4)
assert function_args(arg4=4, arg3=3, arg2=2, arg1=1) == (1, 2, 3, 4)

# 9) Nested function definitions
# you can define functions INSIDE other functions! And even RETURN them!
def get_delegate(var):
    
    def handle_none():
        return 0
    
    def handle_other():
        return var
    
    if var is None:
        return handle_none
    return handle_other

# get a delegate function and then call it!
assert get_delegate(None)() == 0
assert get_delegate(1)() == 1

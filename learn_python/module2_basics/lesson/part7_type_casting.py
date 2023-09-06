"""
Python has dynamic typing - meaning a variable might hold anything!
When you are not sure what a variable is you can use built-in function
`type() <https://docs.python.org/3/library/functions.html#type>`_ to 
find out!
"""
from learn_python.module2_basics.lesson.part6_floating_point import *


assert type(my_int) is int
assert type(my_float) is float
assert type(my_boolean) is bool
assert type(6.1) is float
assert type(6) is int
assert type(True) is bool
assert type('hello world') is str

# everything has a type!
def even_functions():
    pass

from types import FunctionType
assert type(even_functions) is FunctionType

# None is a special type called NoneType, there is no way to import it 
# directly, but you can get it by calling type() on None:
NoneType = type(None)
assert type(empty) is NoneType

# we use "is" to compare types - more on this when we talk about immutability 
# and memory but == also works!
assert type(my_int) == int


# ********* Casting (aka Coercion) *******************************************
# variables can be coerced to other types! this is also called "type casting"
# to attempt a coercion use the type name as a function!
assert int(6.1) == 6  # for example float -> int loses the decimal
assert float(6) == 6.0  # and int -> float adds a decimal

# but be careful! if you try to cast a string to an int, it will fail!
# int('hello') -> this will error out because it's meaningless!
# but you can cast a string to a float or integer if it is a number!
assert float('6.1') == 6.1
assert int('6') == 6
# or back to a string!
assert str(6.1) == '6.1'
assert str(6) == '6'

# everything in python can be cast to a string!
assert str(True) == 'True'
assert str(None) == 'None'

# but the string value is not always what you might expect!
assert str(type(None)) ==  "<class 'NoneType'>"
assert str(int) == "<class 'int'>"

# what happens when you coerce an imported module to a string?
from learn_python.module2_basics import lesson
demo_str = str(lesson)

# when you divide two integers you get a float!
assert 4/3 == (1 + 1/3)
assert type(int(4) / int(3)) == float

# unless you do integer (aka floor) division
assert 4 // 3 == 1
assert type(4 // 2) == int

# when you multiply two ints you get an int
assert type(4 * 3) == int
# but when you multiply an int and a float, you get a float
assert type(4 * 3.0) == float

# whenever an expression is used as a condition of an if/else statement or used with
# a logical operator, the expression is implicitly cast to a bool. For example:

if not my_int:
    assert False  # shouldn't happen b/c my_int == 3 and bool(my_int) == True

# the above is equivalent to:
if not bool(my_int):
    assert False
    
# this will be important when we talk about empty lists next!

# ****************************************************************************
# Do Gateway 2 tasks 10-11 before proceeding!                                *
# ****************************************************************************

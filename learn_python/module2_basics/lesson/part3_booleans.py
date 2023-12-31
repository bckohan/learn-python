"""
..  youtube:: xmfm4Gy8m8g
   :width: 70%
   :align: center
   :url_parameters: ?vq=hd1080

|

`Booleans <https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not>`_
are either True or False.

.. note::

    When used as literals True and False must be capitalized!

+---------+---------------------------------------------------------------------------------------+
| Operator| Description                                                                           |
+---------+---------------------------------------------------------------------------------------+
| ``and`` | Logical AND: Returns True if both the operands are true.                              |
+---------+---------------------------------------------------------------------------------------+
| ``or``  | Logical OR: Returns True if either of the operands is true.                           |
+---------+---------------------------------------------------------------------------------------+
| ``not`` | Logical NOT: Returns True if the operand is false, and False if it's true.            |
+---------+---------------------------------------------------------------------------------------+
| ``==``  | Equality: Checks if two booleans are equal.                                           |
+---------+---------------------------------------------------------------------------------------+
| ``!=``  | Inequality: Checks if two booleans are not equal.                                     |
+---------+---------------------------------------------------------------------------------------+
| ``&``   | Bitwise AND: Equivalent to logical AND for booleans.                                  |
+---------+---------------------------------------------------------------------------------------+
| ``|``   | Bitwise OR: Equivalent to logical OR for booleans.                                    |
+---------+---------------------------------------------------------------------------------------+
| ``^``   | Bitwise XOR: Returns True if exactly one of the operands is true.                     |
+---------+---------------------------------------------------------------------------------------+
"""
from learn_python.module2_basics.lesson.part2_integers import *


my_boolean = True
assert my_boolean

#  logical operators are "and", "or" and "not"

#       and
assert (True and True) is True
assert (False and True) is False
assert (False and False) is False

#       or
assert (True or True) is True
assert (False or True) is True
assert (False or False) is False

#       not
assert not True is False
assert not False is True

assert not not my_boolean

# parentheses can be used to control order of operations just like in math!
assert not (my_boolean and False)
assert my_boolean or False

# if you are ever confused about why your logic statement is not working
# correctly - try explicitly adding parenthesis just to make sure its not
# an order of operations problem!

# booleans behave like integers when you do math on them!
#  where True == 1 and False == 0
assert True == 1
assert False == 0
assert my_boolean + 1 == 2
assert not my_boolean - 1
assert my_boolean + my_int == 4

# The logical operators will do as little work as possible. If you have False 
# and True, python will not look at the "True" because nothing and-ed with 
# False can be True, so it will evaluate to False immediately. This is useful
# for logic expressions where it is dangerous to perform the second expression
# if the first is not True.
# For Example, None does not support the < or > operators, so if we tried None > 0
# the program would crash. We could write:
variable = None
var_is_greater_than_zero = False
if variable is not None:
    if variable > 0:
        var_is_greater_than_zero = True

# or we could take advantage of the laziness optimization and simply write:
if variable is not None and variable > 0:
    var_is_greater_than_zero = True

# this is safe to do because if variable is None, variable > 0 will not
# execute
    
# we could also shorten the above to:
if variable and variable > 0:
    var_is_greater_than_zero = True

# remember that when used in an if statement expressions are implicitly treated
# as booleans. "variable" by itself is an expression. None always evaluates
# to False and integers evaluate to False only if they are 0. So in the first
# if condition, variable > 0 is checked only when variable is not None and in
# the second if condition variable > 0 is checked only when variable is an
# integer less than or greater than 0. You'll note that the second if condition
# is both more efficient, concise and logically equivalent to the first if
# condition.
    
# But notice that logical equivalence is dependent on our second expression,
# For example, this is incorrect:

var_is_greater_than_or_eq_to_zero = False
if variable and variable >= 0:
    var_is_greater_than_or_eq_to_zero = True

# why is this if condition incorrect?
# be careful when short handing if statements when Nones are involved!

# The or operator can be used with the assignment operator as shorthand 
# (or idiom) for assignment to a variable to whichever of a group of 
# variables does not evaluate to False
# for example:
zero = 0
two = 2
if zero:
    x = zero
else:
    x = two

# could also be written as:
y = zero or two

assert x == y == two

# when you assign using "or" like this, the first variable that evaluates to 
# True is used
if zero:
    x = zero
elif False:
    x = False
else:
    x = two

# the above is equivalent to:
x = zero or False or two

assert x == two

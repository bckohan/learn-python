"""
Tuples are like lists, but they are immutable (unchanging). Tuples are specified with parenthesis 
instead of square brackets.

+------------+----------------------------------------------------------------------------------------+
| Operator   | Description                                                                            |
+------------+----------------------------------------------------------------------------------------+
| ``+``      | Concatenation: Combines two tuples.                                                    |
+------------+----------------------------------------------------------------------------------------+
| ``*``      | Repetition: Replicates the tuple a given number of times.                              |
+------------+----------------------------------------------------------------------------------------+
| ``==``     | Equality: Checks if two tuples have the same elements in the same order.               |
+------------+----------------------------------------------------------------------------------------+
| ``!=``     | Inequality: Checks if two tuples are different.                                        |
+------------+----------------------------------------------------------------------------------------+
| ``<``      | Less than: Compares tuples lexicographically.                                          |
+------------+----------------------------------------------------------------------------------------+
| ``>``      | Greater than: Compares tuples lexicographically.                                       |
+------------+----------------------------------------------------------------------------------------+
| ``<=``     | Less than or equal to: Compares tuples lexicographically.                              |
+------------+----------------------------------------------------------------------------------------+
| ``>=``     | Greater than or equal to: Compares tuples lexicographically.                           |
+------------+----------------------------------------------------------------------------------------+
| ``in``     | Membership: Checks if an item is present in the tuple.                                 |
+------------+----------------------------------------------------------------------------------------+
| ``not in`` | Non-membership: Checks if an item is not present in the tuple.                         |
+------------+----------------------------------------------------------------------------------------+

"""
from learn_python.module2_basics.lesson.part8_lists import *
 
my_tuple = (1, 2, 3)
assert type(my_tuple) == tuple
assert my_tuple[0] == 1
assert my_tuple[-1] == 3

# When python sees a , without any enclosing [], {} or () characters it will
# assume a default of (). This means it will interpret comma separate lists
# as tuples by default.
# This means you can also specify a tuple without parenthesis:
my_tuple = 1, 2, 3
assert type(my_tuple) == tuple
assert my_tuple[0] == 1
assert my_tuple[-1] == 3

# tuples are sliceable like lists
assert my_tuple[1:3] == (2, 3)

# but you cannot change their elements!
# my_tuple[0] = 0 -> this will error out!

# tuples are preferred to lists in situations where the number of elements are 
# small, fixed and unchanging

# they are also preferable because "unpacking" a tuple is safer than unpacking 
# a list, because the length of a list might change on you!
a, b, c = my_tuple
assert a == 1
assert b == 2
assert c == 3

# this is especially useful when returning multiple values from a function
def my_function():
    return 1, 2, 3

a, b, c = my_function()
assert a == 1 and b == 2 and c == 3

# our functions that return multiple values are actually returning a tuple!
returned_value = my_function()
assert type(returned_value) == tuple
assert returned_value == (1, 2, 3)

# Sometimes you may need a single value tuple, but you can't specify it like
# this:
assert (1) == 1  
# this is just the number 1 because the parenthesis are interpreted as order
# of operation grouping

# single value tuples need a trailing comma to signal to the interpreter that you
# mean this to be a 1-tuple:
assert (1,) == tuple([1])

# ****************************************************************************
# Do Gateway 2 tasks 12-15 before proceeding!                                *
# ****************************************************************************

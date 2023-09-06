"""
Variables are references to objects in memory - think of them as addresses
or pointers to specific chunks of memory. Python hides this complexity from us 
because usually when we use a variable we want to use its value and not know anything
about its address. However, knowing variable addresses can help us understand
how and when operators change existing objects in memory (mutability) or create new 
objects in memory (immutability). 

We mostly do not have to think about this in Python, because the decisions the 
language makes for us tend to be intuitive - but we should build a basic intuition 
using the `built-in id() function <https://docs.python.org/3/library/functions.html#id>`_.
This will help us write better code and understand certain classes of bugs that may
arise.
"""
from learn_python.module2_basics.lesson.part11_methods import *

# the id() built-in function returns the virtual memory address of the variable!
my_int_address = id(my_int)
assert my_int_address == id(my_int)

# integers are immutable, so when we do math on them Python creates new integers
# we can see this because the memory address will change:
my_int += 1
assert my_int_address != id(my_int)

# this is handy in function calls because we can rest assured that our original
# integer will be unchanged!
assert my_int == 4

def add_one(x):
    x += 1
    return x

incremented = add_one(my_int)
assert incremented == 5
assert my_int == 4

# but lists are mutable!
my_list = [1, 2, 3]

def append_item(lst, item):
    lst.append(item)
    return lst

appended = append_item(my_list, 4)
assert appended == [1, 2, 3, 4]
assert my_list == [1, 2, 3, 4]
assert id(appended) == id(my_list)

# the is operator checks if two variables are the same object in memory, it is
# the same as comparing their memory addresses with id()
assert appended is my_list
# my_list and appended point to the same memory!

# this is why we use "is" to check if a variable is None - because None is a
# special object in memory that is immutable and there is only one of them!
assert id(None) == id(None)
assert None is None

my_none = None
other_none = None
assert id(my_none) == id(other_none)
assert my_none is other_none

# functions are pass-by-reference as opposed to pass-by-value, meaning that
#  when you pass a variable to a function, the function gets a reference to
#  the variable in memory, not a copy of the variable!

def pass_by_ref_example(my_argument):
    # my_argument is the same piece of memory as my_int
    assert my_argument is my_int

pass_by_ref_example(my_int)

# this might seem confusing, but you mostly do not have to worry about it
# because the choices the language has made are intuitive! Just
# be aware that when dealing with mutable types like lists, sets or dictionaries
# functions can modify the original object!

# Python offers two ways to copy memory, a shallow copy and a deep copy
from copy import copy, deepcopy

# a shallow copy creates a new object in memory, but the contents of the object
# are references to the original object's contents:

nested_list = [
    [0, 1, 2, 3],
    [4, 5, 6, 7]
]

nested_list_copy = copy(nested_list)

# the outer list is a new object in memory
# but the inner lists are references to the original inner lists!
assert id(nested_list) != id(nested_list_copy)
assert id(nested_list[0]) == id(nested_list_copy[0])
assert id(nested_list[1]) == id(nested_list_copy[1])

assert nested_list[0] == [0, 1, 2, 3]
nested_list_copy[0][0] = -1
assert nested_list[0] == [-1, 1, 2, 3]

# a deep copy creates a new object in memory and copies all nested 
# contents of the original object into the new object recursively:
nested_list_deepcopy = deepcopy(nested_list)
assert id(nested_list) != id(nested_list_deepcopy)
assert id(nested_list[0]) != id(nested_list_deepcopy[0])
assert id(nested_list[1]) != id(nested_list_deepcopy[1])

assert nested_list[0] == [-1, 1, 2, 3]
nested_list_deepcopy[0][0] = -2
assert nested_list[0] == [-1, 1, 2, 3]
assert nested_list_deepcopy[0] == [-2, 1, 2, 3]

# A common type of bug may occur when you pass a mutable object around to other
# parts of your code base and that code modifies the object without you realizing
# it. This is why it is important to understand mutability and immutability.

# ****************************************************************************
# Do Gateway 2 tasks 16-21 before proceeding!                                *
# ****************************************************************************


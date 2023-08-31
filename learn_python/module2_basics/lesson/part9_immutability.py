"""
Immutability and Memory

Variables are references to objects in memory - think of them as addresses
or "pointers". Python hides this from us because when we use a variable we are
using its value, but understanding how and when operators change existing
objects in memory (mutability) or create new objects in memory (immutability)
is important
"""
from learn_python.module2_basics.lesson.part8_lists import *

# the id() built-in function returns the virtual memory address of the variable!
my_int_address = id(my_int)
assert my_int_address == id(my_int)

# integers are immutable, so when we do math on them Python creates new integers
#  we can see this because the memory address will change:
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
#  the same as comparing their memory addresses with id()
assert appended is my_list

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

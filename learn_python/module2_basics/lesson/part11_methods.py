"""
There are three types of functions in Python:
    * functions
    * operators
    * methods

Basic functions can be defined anywhere and called wherever a reference to the
function or a variable holding the function can be accessed. We have also seen 
examples of many operators - which are just special functions the language binds 
to specific symbols like "*". The final type of function is a method. Methods are 
functions that are bound to, and called on, a specific type of data.

Lets take a look!
"""
from learn_python.module2_basics.lesson.part10_strings import *

assert my_512_bit_integer.bit_length() == 512
# when you see a function invoked like above (e.g. variable.function() )
# think of the variable as the first argument to the function 
# (e.g. function(variable) ) - more on this when we talk about classes!
# 
# when a function is invoked on a variable like this it may be referred to
# as a "method"

# string has a bunch of very useful methods!
assert my_string.upper() == 'HELLO WORLD'

# you can chain methods together, .lower() is called on the return value of 
# .upper()!
assert my_string.upper().lower() == 'hello world'

# here's a useful function that splits strings into a list of strings along
# a delimiter, white space by default:
assert my_string.split() == ['hello', 'world']

# you can also join strings together with a delimiter using:
#  delimiter_str.join(list_of_strings), here we see that join and
#  split are inverses of each other! when you nest a function call like this
#  the innermost function (split() in this case) is evaluated first and its 
#  return value is passed as the argument to the outer function (join in 
#  this case)
assert ' '.join(my_string.split()) == 'hello world'

# anything between parenthesis can be split onto multiple lines, we could
# rewrite the above to be more readable like this:
assert ' '.join(
                       # when written this way you may think it is more easy
    my_string.split()  # to see that the argument to join() is the return value 
                       # of the function call my_string.split()
) == 'hello world'

# read all about the string methods here: 
#   https://docs.python.org/3/library/stdtypes.html#string-methods

# container types like lists also have a bunch of functions, many involve adding 
# or removing elements from the container

my_list = [1, 2, 3, 4, 5]
my_list.append(6)  # add 6 to the end of my_list
assert my_list == [1, 2, 3, 4, 5, 6]
last = my_list.pop()  # pop the last element off of my_list and assign it
assert my_list == [1, 2, 3, 4, 5]
assert last == 6

# what happens when you use an operator like multiply?
#  python invokes the special function __mul__ for you!
assert my_int * 7 == my_int.__mul__(7)

# all operators map to special functions like this! For example, == maps to
# __eq__ and > maps to __gt__ and so on.
assert (my_int == 3) == my_int.__eq__(3)
assert (my_int > 2) == my_int.__gt__(2)

# we'll talk more about this and why it's important when we discuss classes!
#  hint: its because when we define our own custom types we can define these
#  special functions to make our types usable with operators!


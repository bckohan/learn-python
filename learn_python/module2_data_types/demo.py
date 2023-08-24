"""
This file contains examples of the basic data types in python. We use assertion
statements to verify that the statements are accurate. assert <expression> is a
special statement in python that will error out if the <expression> is False.
When executed this file should produce no output because all the assertions are
True!

You can also add an optional string after an assert expression, try this:

    assert False, 'False is not True!'

Assertion statements are used to test your gateway assignments! Check them out
in ./tests

This multi-line string - delineated by triple quotes - is called a docstring 
when it appears at the top of a module like this. It will be put in a special
variable called __doc__. Try this:

    from learn_python.module2_data_types import demo
    print(demo.__doc__)

"""


# ********* Integers *********************************************************
# integers do not have fractional components
my_int = 3

# integers are not limited to the word size of your processor (i.e. 64 bits)!
#  They can be as large as your computer's memory can hold!
my_512_bit_integer = 2**512-1

# math on integers is straight forward:
assert my_int + 1 == 4
assert my_int - 1 == 2  # this is not 3 because my_int + 1 did not modify my_int!

# operators can be combined with assignment by combining the mathematical and
#   assignment operator (=)
my_int += 1  # this is equivalent to my_int = my_int + 1
assert my_int == 4
my_int -= 1
assert my_int == 3
my_int *= 2
assert my_int == 6
my_int /= 2
assert my_int == 3

my_int = 3
# ****************************************************************************


# ********* Booleans *********************************************************
# boolean values are either True or False - note when used as literals True and
#   False must be capitalized!
my_boolean = True
assert my_boolean

#  logical operators are "and", "or" and "not"
#
#       and
#  (True and True) is True
#  (False and True) is False
#
#       or
#  (True or True) is True
#  (False or True) is True
#  (False or False) is False
#
#       not
#  not True is False
#  not False is True

assert not not my_boolean

# parentheses can be used to control order of operations just like in math!
assert not (my_boolean and False)
assert my_boolean or False

# booleans behave like integers when you do math on them!
#  where True == 1 and False == 0
assert True == 1
assert False == 0
assert my_boolean + 1 == 2
assert not my_boolean - 1
assert my_boolean + my_int == 4
# ****************************************************************************


# ********* Floats ***********************************************************
# Floating point numbers are numbers with a decimal point
my_float = 345.6
# you can also specify floats with scientific notation
assert my_float == 345.6 == 3.456e2 == 345.6e0 == 3.456*(10**2)
# floats are considered True when non-zero and used as a boolean
assert my_float
assert not 0.0

# when you do math with floats, you get a float back
assert 4.0 + 2.0 == 6.0
# but if you compare to an integer, python will "coerce" the integer to a float
#  and the comparison will evalutate as you expect
assert 4.0 + 2.0 == 6
assert 6.1 > 6
assert 6.1 > my_int  # remember my_int == 3
# ****************************************************************************


# ********* None *************************************************************
# the "absence" of a value is None
empty = None
assert empty is None  # comparison to None is done with "is"
assert empty == None  # but this will also work!
# ****************************************************************************


# ********* type() ***********************************************************
# not sure what a variable is? use built-in function type() to find out!
assert type(my_int) == int
assert type(my_float) == float
assert type(my_boolean) == bool
assert type(6.1) == float
assert type(6) == int
assert type(True) == bool
assert type('hello world') == str

# None is a special type called NoneType
assert type(None) == type(empty)
# ****************************************************************************


# ********* Casting (aka Coercion) *******************************************
# variables can be coerced to other types! this is also called "type casting"
# to attempt a coercion use the type name as a function!
assert int(6.1) == 6  # for example float -> int loses the decimal

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
from learn_python.module2_data_types import demo
demo_str = str(demo)

# when you divide two integers you get a float!
assert 4/3 == (1 + 1/3)
assert type( int(4) / int(3) ) == float

# unless you do integer (aka floor) division
assert 4 // 3 == 1
assert type(4 // 2) == int

# when you multiply two ints you get an int
assert type(4 * 3) == int
# but when you multiply an int and a float, you get a float
assert type(4 * 3.0) == float
# ****************************************************************************

# ********* Lists ************************************************************
# lists are sequences of values in a contiguous chunk of memory
my_list = [1, 2, 3, 4, 5]
# you can access elements of a list by index
assert my_list[0] == 1
# python also supports negative indexing (i.e. count from the end, 1-indexed)
assert my_list[-1] == 5

# lists are mutable
my_list[0] = 0
assert my_list == [0, 2, 3, 4, 5]

# you can slice lists to get a sub-list
assert my_list[1:3] == [2, 3]

# you can concatenate lists together with +
my_list = [1] + my_list[1:]
assert my_list == [1, 2, 3, 4, 5]

# len() is a built-in function that returns the length of a list
assert len(my_list) == 5

# you might frequently see len() used in slicing, all of the below are
# equivalent. Also in python if we have really long line we can use \
# to break it up into multiple lines
assert \
    my_list[0:5] == \
    my_list[:len(my_list)] == \
    my_list[:] == \
    my_list == \
    [1, 2, 3, 4, 5]

# lists can contain elements of multiple different types
multi_type_list = [1, 'hello', 3.0, True, None, [1, 2, 3]]
assert len(multi_type_list) == 6
assert multi_type_list[-2] is None
assert multi_type_list[-1] == [1, 2, 3]  # including other lists!

# if you have a list of lists, you can think of it as a matrix!
matrix = [
    [1, 2, 3], 
    [4, 5, 6], 
    [7, 8, 9]
]  # lists can also be multi-line without using \
assert matrix[0][0] == 1
assert matrix[1][1] == 5
assert matrix[2][2] == 9
assert matrix[2][0] == 7
assert matrix[0][2] == 3 

# what happens when you multiply a list by an integer? 
#   Probably not what you think if you do a lot of math!
# ****************************************************************************

# ********* Strings **********************************************************
# strings are sequences of characters
# you can use either ' or " to define a one-line string
my_string = 'hello world'
assert my_string == "hello world"

# if you want to use the ' or " character in a string, you can "escape" it with \
#  or conveniently you can use the alternate quote character to define the string:
assert 'hello "world"' == "hello \"world\""
assert "hello 'world'" == 'hello \'world\''

#  most of the immutable (unchanging) list operators are available, including 
# indexing and slicing!

# recall my_string == 'hello world'
assert my_string[0] == 'h'
assert my_string[-1] == 'd'
assert my_string[0:5] == 'hello'
assert my_string[6:] == 'world'
assert my_string[::2] == 'hlowrd'

# assignment to an element is not available because strings are immutable!
#   my_string[0] = 'H' -> this will error out!

# concatenate strings using +
assert 'hello' + ' ' + 'world' == 'hello world'

# the += operator is short for "add and assign" like on integers
my_string += '!'
assert my_string == 'hello world!'

# what else can you do with string opertors? hint try to multiply a string by
# an integer!

# f-strings are a convenient way to combine strings with variables using
#   configurable formatting
# f-strings are prefixed with the letter f, and variables are surrounded by {}
assert f'my_int == {my_int}' == 'my_int == 3'

# f-strings have configurable formatting, for example you can specify the number
# of decimal places to display for a float
assert f'my_float == {my_float:.2f}' == 'my_float == 345.60'

# combining strings with variables has gone through a few iterations in python:
#   optionally read more: https://realpython.com/python-f-strings/
# we used to do f-strings like this:
assert 'my_int == %d' % my_int == 'my_int == 3'
# or like this
assert 'my_int == {}'.format(my_int) == 'my_int == 3'

# lets just chop that last "!" off the end of my_string, by re-assigning it
#  to a slice of itself :-)
assert my_string == 'hello world!'
my_string = my_string[:-1]
assert my_string == 'hello world'

# working with strings is a very common and important task in programming because
# its the predominant way our program talks to humans!
# we will devote an entire module to it later - for now just understand these
# basics!
# ****************************************************************************

# ********* Sets *************************************************************
# sets are unordered collections of **unique** values, you cannot have multiple
#  identical values in a set

# you can specify a set like this
my_set = {1, 2, 3}
#  any duplicate values will be ommitted!
assert my_set == {1, 2, 3} == {1, 2, 3, 1, 2, 3}

# ********* Functions vs Operators *******************************************
# data types have a bunch of functions that can be called on them
#  look at the standard library docs for all the details!
assert my_512_bit_integer.bit_length() == 512
# when you see a function invoked like above (e.g. variable.function() )
#   think of the variable as the first argument to the function 
#   (e.g. function(variable) ) - more on this when we talk about classes!
# 
# when a function is invoked on a variable like this it may be refered to
#  as a "method"

# string has a bunch of very useful functions!
assert my_string.upper() == 'HELLO WORLD'

# you can chain functions together, .lower() is called on the return value of 
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
    my_string.split()  # to see that the argument itself is the return value 
                       # of a function call
) == 'hello world'

# read all about the string methods here: 
#   https://docs.python.org/3/library/stdtypes.html#string-methods

# container types like lists, sets and dictionaries also have a bunch of
# functions, many involve adding or removing elements from the container
my_set.add(5)
assert my_set == {1, 2, 3, 5}
my_set.remove(5)
assert my_set == {1, 2, 3}

my_list.append(6)  # add 6 to the end of my_list
assert my_list == [1, 2, 3, 4, 5, 6]
last = my_list.pop()  # pop the last element off of my_list and assign it
assert my_list == [1, 2, 3, 4, 5]
assert last == 6

# what happens when you use an operator like multiply?
#  python invokes the special function __mul__ for you!
assert my_int * 7 == my_int.__mul__(7) == 3 * 7 == 21

# all operators map to special functions like this! For example, == maps to
# __eq__ and > maps to __gt__ and so on.
assert my_int == 3 and my_int.__eq__(3)
assert my_int > 2 and my_int.__gt__(2)

# we'll talk more about this and why it's important when we discuss classes!
# ****************************************************************************


# ********* Terminology ******************************************************
# when you see a primitive type specified directly as its value it is called a
# "literal"
# 3 is an integer literal
# 'hello world' is a string literal
# [0, 1, 2] is a list literal
# {1, 2, 3} is a set literal
# {1: 'one', 2: 'two'} is a dictionary literal
# True and False are boolean literals
# ****************************************************************************

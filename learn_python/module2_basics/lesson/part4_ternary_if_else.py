"""
Ternary if/else expressions are a shorthand for simple if/else statements that
produce a value. Ternary expressions are composed of three parts:

    1. a condition,
    2. an expression that produces a value to use if that condition is True
    3. an expression that produces a value to use if that conditions is False

    <expression> if <condition> else <expression>

The if true expression is written first so the whole expression reads similar
to an english sentence.
"""
from learn_python.module2_basics.lesson.part3_booleans import *


# as we have already discussed if/else statements are used to control the flow
# of a program:

# this block adds 1 to my_int if my_boolean is True, and subtracts 1 if it is False
if my_boolean:
    my_int += 1
else:
    my_int -= 1

# this is a pretty bulky 4-line statement to just switch between addition and
# subtraction - Ternary if/else expressions are a shorthand that let us write
# this in a single line

# this is equivalent to the above if/else statement, it should be read as:
# add 1 to my_int if my_boolean is True, otherwise add -1
my_int += 1 if my_boolean else -1

# sometimes adding parentheses can make this more readable as a visual cue
# that the ternary expression is a single expression with a result that is
# being passed to the += operator along with my_int
my_int += (1 if my_boolean else -1)

# parenthesis also allow us to split code along multiple lines, some people
# prefer this style:
my_int += (
    1 if my_boolean
    else -1
)  # but now we're back to 4 whole lines! this is a stylistic preference,
   #  use what you like!

# ternary expressions do not support elif statements! They are for very simple
# conditions only - the result of a ternary statement is an expression
# (i.e. a ternary if/else statement produces a value where normal if/else 
# statements switch logic flow)
# Said another way: if/else logic switches are statements and ternary if/else
# expressions are expressions because they produce a value.

# != means not equal and is the inverse of ==
# because ternary expressions are expressions, we can combine them with other
# expressions:
my_int = (3 if my_int != 3 else my_int) * 1

# you might notice that the above statement is just a more complicated way of writing:
my_int = 3

"""
..  youtube:: 2up8aLk9rcY
   :width: 70%
   :align: center
   :url_parameters: ?vq=hd1080

|

`Integers <https://docs.python.org/3/library/functions.html?highlight=int#int>`_ are whole numbers
(they do not have fractional components).

Here are the common numerical operators (also look at the :ref:`cheat sheets <external-resources>`!):

+---------+---------------------------------------------------------------------------------------+
| Operator| Description                                                                           |
+---------+---------------------------------------------------------------------------------------+
| ``+``   | Arithmetic addition: Adds two integers.                                               |
+---------+---------------------------------------------------------------------------------------+
| ``-``   | Arithmetic subtraction: Subtracts right operand from the left.                        |
+---------+---------------------------------------------------------------------------------------+
| ``*``   | Multiplication: Multiplies two integers.                                              |
+---------+---------------------------------------------------------------------------------------+
| ``/``   | Division: Divides left operand by the right one (always returns a float).             |
+---------+---------------------------------------------------------------------------------------+
| ``//``  | Floor Division: Divides and returns the integer value of the quotient.                |
+---------+---------------------------------------------------------------------------------------+
| ``%``   | Modulus: Returns the remainder when left operand is divided by the right operand.     |
+---------+---------------------------------------------------------------------------------------+
| ``**``  | Exponentiation: Raises the left operand to the power of the right operand.            |
+---------+---------------------------------------------------------------------------------------+
| ``<<``  | Left shift: Shifts the bits of the number to the left by the specified number of      |
|         | positions.                                                                            |
+---------+---------------------------------------------------------------------------------------+
| ``>>``  | Right shift: Shifts the bits of the number to the right by the specified number of    |
|         | positions.                                                                            |
+---------+---------------------------------------------------------------------------------------+
| ``&``   | Bitwise AND: Performs a bitwise AND on two integers.                                  |
+---------+---------------------------------------------------------------------------------------+
| ``|``   | Bitwise OR: Performs a bitwise OR on two integers.                                    |
+---------+---------------------------------------------------------------------------------------+
| ``^``   | Bitwise XOR: Performs a bitwise exclusive OR on two integers.                         |
+---------+---------------------------------------------------------------------------------------+
| ``~``   | Bitwise NOT: Inverts all the bits of the integer.                                     |
+---------+---------------------------------------------------------------------------------------+
| ``==``  | Equality: Checks if two integers are equal.                                           |
+---------+---------------------------------------------------------------------------------------+
| ``!=``  | Inequality: Checks if two integers are not equal.                                     |
+---------+---------------------------------------------------------------------------------------+
| ``<``   | Less than: Checks if left integer is less than the right one.                         |
+---------+---------------------------------------------------------------------------------------+
| ``>``   | Greater than: Checks if left integer is greater than the right one.                   |
+---------+---------------------------------------------------------------------------------------+
| ``<=``  | Less than or equal to: Checks if left integer is less than or equal to the right one. |
+---------+---------------------------------------------------------------------------------------+
| ``>=``  | Greater than or equal to: Checks if left integer is greater than or equal to the      |
|         | right one.                                                                            |
+---------+---------------------------------------------------------------------------------------+

.. youtube:: sD-BXi3sbcw
   :width: 50%
   :align: right
   :url_parameters: ?vq=hd1080


If all this talk of binary numbers and bitwise operations is confusing, just remember that all
data in a computer system is represented by a sequence of bits (0s and 1s). Integers and negative
integers are no different. The other thing to remember is that computers are finite. We
do not have an infinite number of bits to play with, so when we represent numbers in a computer
there is a point at which adding 1 to a number will cause it to exceed that limitation. This is
called an integer overflow - and it's actually a feature we rely on to do arithmetic on positive
and negative integers in binary. Checkout the video to the right for all the gory details!
"""
from learn_python.module2_basics.lesson.part1_none import *


my_int = 3  # assignment - my_int now holds the value of 3
assert my_int == 3

# integers in Python are not limited to the word size of your processor 
#  (i.e. 64 bits)! They can be as large as the amount of memory Python has been
# configured to allow - which for all practical purposes can be considered arbitrarily
# large
my_512_bit_integer = 2**512-1
assert my_512_bit_integer == 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084095

# math on integers is straight forward:
assert my_int + 1 == 4
assert my_int - 1 == 2  # this is not 3 because my_int + 1 did not modify my_int!

# operators can be combined with assignment by combining the mathematical and
# assignment operator (=)
my_int += 1  # this is equivalent to my_int = my_int + 1
assert my_int == 4
my_int -= 1
assert my_int == 3
my_int *= 2
assert my_int == 6
my_int /= 2
assert my_int == 3


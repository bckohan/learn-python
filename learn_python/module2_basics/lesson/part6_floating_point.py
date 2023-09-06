"""
Floating point numbers are numbers with fractions (e.g. 2.99792458)!

It is impossible to represent all arbitrary real numbers using a finite number of 1s and 0s!

Python uses the 64 bit IEEE-754 specification for floating point numbers. For all the gory 
details checkout this video.

..  youtube:: dQhj5RGtag0
   :width: 40%
   :align: left

We call them "floating point" numbers because we use a binary version of scientific 
notation where some bits are reserved for the exponent - which allows us
to manipulate where the “point” resides and thus control at which magnitude
our precision resides. We run into trouble when we expect a single float to
be precise at two wildly different magnitudes.

Most processors have a Floating Point Unit (FPU) composed of transistor circuits
optimized for floating point arithmetic. For this reason the size of floats in most computing
systems are determined by the hardware and are typically 64-80 bits long. We do not have 
arbitrarily large floats in Python as we do with integers.

You do not need to know the details! Except to understand that not all numbers
are representable and this can introduce small precision errors in mathematics
that are almost `but not always inconsequential. <https://blog.esciencecenter.nl/floating-point-butterfly-effect-62ebe004200f>`_

`This classic paper explains "What every scientist should know about floating point numbers". <https://dl.acm.org/doi/10.1145/103162.103163>`_
   
|

-------------------------

+---------+----------------------------------------------------------------------------------------+
| Operator| Description                                                                            |
+---------+----------------------------------------------------------------------------------------+
| ``+``   | Arithmetic addition: Adds two floats.                                                  |
+---------+----------------------------------------------------------------------------------------+
| ``-``   | Arithmetic subtraction: Subtracts right operand from the left.                         |
+---------+----------------------------------------------------------------------------------------+
| ``*``   | Multiplication: Multiplies two floats.                                                 |
+---------+----------------------------------------------------------------------------------------+
| ``/``   | Division: Divides left operand by the right one.                                       |
+---------+----------------------------------------------------------------------------------------+
| ``//``  | Floor Division: Divides and returns the largest whole number not greater than the      |
|         | result (as a float).                                                                   |
+---------+----------------------------------------------------------------------------------------+
| ``%``   | Modulus: Returns the remainder when left operand is divided by the right operand.      |
+---------+----------------------------------------------------------------------------------------+
| ``**``  | Exponentiation: Raises the left operand to the power of the right operand.             |
+---------+----------------------------------------------------------------------------------------+
| ``==``  | Equality: Checks if two floats are exactly equal (be careful with this b/c precision). |
+---------+----------------------------------------------------------------------------------------+
| ``!=``  | Inequality: Checks if two floats are not exactly equal.                                |
+---------+----------------------------------------------------------------------------------------+
| ``<``   | Less than: Checks if left float is less than the right one.                            |
+---------+----------------------------------------------------------------------------------------+
| ``>``   | Greater than: Checks if left float is greater than the right one.                      |
+---------+----------------------------------------------------------------------------------------+
| ``<=``  | Less than or equal to: Checks if left float is less than or equal to the right one.    |
+---------+----------------------------------------------------------------------------------------+
| ``>=``  | Greater than or equal to: Checks if left float is greater than or equal to the         |
|         | right one.                                                                             |
+---------+----------------------------------------------------------------------------------------+
"""
from learn_python.module2_basics.lesson.part5_functions import *


my_float = 345.6
# you can also specify floats with scientific notation
assert my_float == 345.6 == 3.456e2 == 345.6e0 == 3.456*(10**2)
# floats are considered True when non-zero and used as a boolean
assert my_float
assert not 0.0

# when you do math with floats, you get a float back
assert 4.0 + 2.0 == 6.0
# but if you compare to an integer, python will "coerce" the integer to a float
#  and the comparison will evaluate as you expect
assert 4.0 + 2.0 == 6
assert 6.1 > 6
assert 6.1 > my_int  # remember my_int == 3

# remember, floats are not infinitely precise! Because they are stored in a
# finite number of bits (usually 64 or 80):
number1 = 0.1
# Lets add a very tiny number to 0.1
number2 = number1 + 1e-308
# we can't expect the same float to maintain precision at two wildly different
# magnitudes!
# logically number1 and number2 should compare as *not equal* right?
# but they are *equal*! because the float does not have enough bits to store
# precision 307 orders of magnitude apart!
assert number1 == number2
# its like we added zero to number2, but we didn't b/c:
assert 1e-308 != 0
# when we don't also have to store 0.1 we have enough bits to store 1e-308
# are you getting a sense of why its called a floating point number?

# this also means that mathematical operations that should produce the exact
# same number might not! And in some rare instances we might encounter
# a significant error in precision at a magnitude we care about. For example
# the standard library math package has functions for sin() and cos():
import math

x = 1e-10
 # in the limit as x -> 0 this should approach 0.5
result1 = (1 - math.cos(x)) / x**2 

# Using an alternative formula to compute the same value
result2 = (2 * math.sin(x/2)**2) / x**2

assert result1 == 0.0   # Expected around 0.5, but the output is 0.0
assert result2 == 0.5   # this one is correct

# what happened here? In the cos formula we subtracted two numbers that are
# very close to each other, this can lead to a catastrophic loss of precision
# that was amplified by our division by another very small number

# You mostly do not need to worry about precision errors and if you do, you 
# will know that you do. This does however, effect normal logic
# operations involving the results of floating point expressions. The small 
# inherent imprecision with floating point computations means it is dangerous
# to compare floats for equality because they might differ by a small but 
# insignificant precision error. It is usually a good practice to compare 
# floating point numbers to within a tolerance. For example:

# math provides an isclose function that compares two floats to within a
# specified tolerance. The below statement returns True if result2 is within 
# 1e-10 of 0.5
assert math.isclose(result2, 0.5, abs_tol=1e-10)

# ****************************************************************************
# Do Gateway 2 tasks 0-9 before proceeding!                                  *
# ****************************************************************************

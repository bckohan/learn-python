"""
.. todo::
    Implement a function called logic_play that accepts two integers as
    arguments and returns their product (the result of multiplying them together)
    if both are even, their quotient (the result of dividing the first by the
    second) if both are odd, and None otherwise. You may assume all inputs will 
    be integers.

.. admonition:: Requirement
    
    You must use the logical operator **and** in your function!

"""
from .task0_is_even import is_even
from .task1_is_odd import is_odd

def logic_play(first, second):
    if is_even(first) and is_even(second):
        return first * second
    elif is_odd(first) and is_odd(second):
        return first / second
    return None

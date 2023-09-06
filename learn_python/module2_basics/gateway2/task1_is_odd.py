"""
is_odd()
========

.. todo::
    Write a function called "is_odd" that returns True if an integer is odd
    and False if it is not. You must use the is_even function you wrote above
    to implement this function. Why do it this way? Because it is more DRY
    (Dont Repeat Yourself) - If we know our is_even function works lets use
    it! Our code will be cleaner and less buggy the more of it we can reuse.

"""
from .task0_is_even import is_even


def is_odd(x):
    return not is_even(x)

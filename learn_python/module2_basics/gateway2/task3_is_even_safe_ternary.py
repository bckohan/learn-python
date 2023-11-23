"""
.. todo::
    Re-implement :ref:`module2-is_even_safe` in a function called 
    "is_even_safe_ternary" that uses a ternary expression to accomplish 
    the same thing in a single statement.
"""
from .task0_is_even import is_even


def is_even_safe_ternary(x):
    return is_even(x) if x is not None else None

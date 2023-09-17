"""
.. todo::
    Because None is a special value in Python that is commonly used to 
    represent uninitialized variables, it is sometimes a good idea to
    check if a variable is None before using it. Implement a function 
    called is_even_safe that works exactly like :ref:`module2-is_even`
    but that checks if the value is None first and if it is returns None.
"""

from .task0_is_even import is_even

def is_even_safe(x):
    if x is not None:
        return is_even(x)
    return None

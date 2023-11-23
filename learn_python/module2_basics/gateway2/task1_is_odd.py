"""
.. todo::
    Write a function called "is_odd" that returns True if an integer is odd
    and False if it is not. You must use the is_even function you wrote above
    to implement this function. 

    
.. admonition:: Requirement

    You must use the :ref:`module2-is_even` function you wrote before in your implementation.

    
.. note:: 

    Why should we use :ref:`module2-is_even` if we can? Because it is more DRY 
    (Dont Repeat Yourself). If we know our :ref:`module2-is_even` function works 
    then let's use it! Our code will be cleaner  and less buggy the more of it we 
    can reuse.

"""
from .task0_is_even import is_even


def is_odd(x):
    return not is_even(x)
    #return x % 2 == 1

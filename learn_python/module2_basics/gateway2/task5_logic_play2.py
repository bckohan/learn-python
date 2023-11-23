"""
.. todo::
    Reimplement :ref:`module2-logic_play` and call it "logic_play2".

.. admonition:: Requirement

    * You cannot use any logical operators (and, or not)
    * You may make a maximum of three function calls
    * Your implementation should not exceed 5 statements.

.. hint::
    * You will need an if statement inside of another if statement.
    * Remember that when a function does not explicitly return anything it returns None

After you've implemented logic_play2 think about which version of logic_play is more clear? 
Which is more efficient? Which is more readable? Which is more maintainable? Cleverness is not
always a virtue in programming and there are always tradeoffs!
"""
from .task1_is_odd import is_odd
from .task0_is_even import is_even

def logic_play2(first, second):
    if is_even(first):
        if is_even(second):
            return first * second
    elif is_odd(second):
        return first / second

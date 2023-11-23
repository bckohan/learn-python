"""
.. todo::
    Define a function called type_divide that takes two arguments and returns
    the result of dividing the first by the second using floor division
    if both arguments are integers and regular division otherwise.
    If the second argument is zero, return None.
"""


def type_divide(x, y):
    if y == 0:
        return None
    if type(x) is int and type(y) is int:
        return x // y
    return x / y

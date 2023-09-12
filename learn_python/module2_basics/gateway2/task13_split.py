"""
.. todo::
    Define a function called split() that accepts two arguments.
    The first will be a list and the second will be an optional index that
    defaults to None. The function should split the list at the index and return
    the both parts of the list. The first part should include all elements up
    to but not including the index. The second part should include all remaining
    elements. If the index is None, it should be determined to be the length of
    the list, floor divided by 2. If the index is negative the order of the two
    lists returned should be switched, with the second part of the list coming
    first.

.. hint::
    You will need to use the built-in function `len() <https://docs.python.org/3/library/functions.html#len>`_
"""

def split(vector, at=None):
    if at is None:
        at = len(vector) // 2
    if at < 0:
        return vector[at*-1:], vector[:at*-1]
    return vector[:at], vector[at:]


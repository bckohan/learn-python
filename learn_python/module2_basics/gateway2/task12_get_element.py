"""
.. todo::
    Define a function called get_element() that accepts two arguments.
    The first will be a list and the second will be an index. The function
    should return the element at that index if the index exists and None
    if the index does not exist. Index may be negative or positive!

.. hint::
    You will need to use the built-in function `len() <https://docs.python.org/3/library/functions.html#len>`_
"""

def get_element(vector, index):
    if abs(index + (1 if index > 0 else 0)) <= len(vector):
        return vector[index]
    return None

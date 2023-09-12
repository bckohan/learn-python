"""
.. todo::
    Implement combine() according to its docstring.

.. hint::
    Checkout the built-in function `zip() <https://docs.python.org/3/library/functions.html#zip>`_,
    but you have to do one other thing because zip() does not return a list type!

"""
def combine(list1, list2):
    """
    Return a single list containing 2-tuples where the i-th element of list1 is
    the first tuple element and the i-th element of list2 is the second tuple
    element. This can be thought of as the inverse of separate().

    For example:

    .. code-block:: python

        combine([1, 2, 3], ['a', 'b', 'c']) == [(1, 'a'), (2, 'b'), (3, 'c')]
    
        
    :param list1: list - the first list
    :param list2: list - the second list
    :return list of tuples: - the combined list of tuples
    """
    return list(zip(list1, list2))

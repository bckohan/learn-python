"""
.. todo:: 
    Implement decimate according to its docstring.

.. hint::
    This is doable in one statement with slicing.

"""
def decimate(vector, factor=10):
    """
    Return a new list reduced in size by the given factor. The elements 
    of the decimated list should be evenly spaced elements of the given list.
    The first element of the returned list should always be the first element 
    of the given list. The size reduction should round up to the nearest whole
    number.

    For example:

    .. code-block:: python

        my_list = [1, 2, 3, 4, 5, 6]
        decimate(my_list, 2) == [1, 3, 5]  # 6/2 = 3
        decimate(my_list, 3) == [1, 4]     # 6/3 = 2
        decimate(my_list, 4) == [1, 5]     # 6/4 = 1.5 -> 2
        decimate(my_list)    == [1]        # 6/10 = 0.6 -> 1

    :param vector: list - the list to decimate
    :param factor: int - the factor to reduce the size of the list by
    """
    return vector[::factor]

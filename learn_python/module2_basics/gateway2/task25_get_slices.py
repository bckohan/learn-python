"""
.. todo::
    Define a function called get_slices() that accepts two arguments.
    The first argument will be a list and the second argument will be a
    list of 2-tuples. The first element of each 2-tuple will be a slice
    start index and the second element will be a slice stop index. Return
    a single list composed of the concatenation of all of the given slice
    indices of the first list argument. For example:

.. code-block:: python

    assert get_slices([0, 1, 2, 3, 4], [(0, 2), (3, None)]) == [0, 1, 3, 4]
    assert get_slices([0, 1, 2, 3, 4], [(0, None), (2, -1)]) == [0, 1, 2, 3, 4, 2, 3]

.. admonition:: Requirement

    Use a for loop and the += list operator.
"""


def get_slices(vector, slices):
    all_slices = []
    for slice in slices:
        all_slices += vector[slice[0]:slice[1]]
    return all_slices

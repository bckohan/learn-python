"""
.. todo::
    Implement separate() according to its docstring.
"""

def separate(list_of_2_tuples):
    """
    Given a list containing tuples of length 2 (2-tuples), return two
    lists where the first list contains the first tuple elements and the
    second list contains the second tuple elements.

    For example:

    .. code-block:: python

        separate([(1, 2), (3, 4)]) == [1, 3], [2, 4]

    :param list_of_2_tuples: list of tuples - the list of 2-tuples to expand
    """
    x, y = [], []
    for tpl in list_of_2_tuples:
        x.append(tpl[0])
        y.append(tpl[1])
    return x, y

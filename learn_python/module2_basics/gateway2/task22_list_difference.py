"""
.. todo::
    Implement the list_difference() function according to its docstring.

.. admonition:: Requirement

    Use set() and type coercion to accomplish this in one statement.
"""


def list_difference(list1, list2):
    """
    Return elements that are in the first list but not the second list.

    .. warning::
        The order of the elements may not reflect their order in the first list.

    :param list1: list - the first list
    :param list2: list - the second list
    :return: a list containing the elements that are in the first list 
        but not the second
    """
    return list(set(list1) - set(list2))

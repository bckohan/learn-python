"""
.. todo::
    Implement list_intersection() according to its docstring.

.. admonition:: Requirement 

    * You may not use sets.
    * You must use for loops.
"""


def list_intersection(list1, list2):
    """
    Return elements that are in both of the given lists. Like set() intersection, 
    but for lists. Duplicate elements are preserved and remain in-order, with the
    first list's elements coming before the second list's elements.
    
    For example:

    .. code-block::

        list_intersection(
            [1, 2, 4, 3],
            [6, 3, 4],
        ) == [4, 3, 3, 4]

    :param lists: list - the first list
    :param list2: list - the second list
    :return: the elements that are in both lists
    """
    intersection = []
    for x in list1:
        if x in list2:
            intersection.append(x)
    for x in list2:
        if x in list1:
            intersection.append(x)
    return intersection

    # return [
    #     *[x for x in list1 if x in list2],
    #     *[x for x in list2 if x in list1]
    # ]

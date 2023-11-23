"""
.. todo::
    Implement list_intersection2() according to its docstring.

    
.. admonition:: Requirement 

    * You must use three list comprehensions and the unpacking operator (*) to
      accomplish this in a single statement.
    * You may not use sets.

"""


def list_intersection2(list1, list2):
    """
    Return elements that are in both of the given lists. Like set() intersection, 
    but for lists. Duplicate elements are preserved and remain in-order, with the
    first list's elements coming before the second list's elements.
    
    For example:

    .. code-block::

        list_intersection(
            [1, 2, 4, 3],
            [2, 3, 4],
        ) == [4, 3, 3, 4]

    :param lists: list - the first list
    :param list2: list - the second list
    :return: a list containing the elements that are in both lists
    """
    return [
        *[x for x in list1 if x in list2],
        *[x for x in list2 if x in list1]
    ]

"""
.. todo:: 
    Define a function called add_to_list that accepts a first argument that is a
    list, followed by a variable number of positional arguments without defaults and
    lastly a keyword argument called mutate with a default value of False.

    The function should add the given elements to the list. If mutate is False (default), 
    the list will not be modified, a new list will be created and returned. If True, the 
    passed in list will be modified and returned (no new list will be created).

    For example:

    .. code-block:: python

        my_list = [1, 2, 3]
        appended = add_to_list(my_list, 4, 5)
        assert appended == [1, 2, 3, 4, 5]
        assert appended is not my_list
        mutated = add_to_list(my_list, 6, 7, 8, mutate=True)
        assert mutated == [1, 2, 3, 6, 7, 8]
        assert mutated is my_list
    
"""


def add_to_list(list1, *elements, mutate=False):
    if mutate:
        list1.extend(elements)
        return list1
    return list1 + list(elements)

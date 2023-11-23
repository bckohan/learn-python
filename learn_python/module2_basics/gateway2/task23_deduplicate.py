"""
.. todo::
    Implement deduplicate() according to its docstring.

.. admonition:: Requirement:

    Your implementation must be a single statement

    
.. hint::
    * use set() and type coercion
    * the order of a set() is undefined
    * checkout the key argument on built-in `sorted() <https://docs.python.org/3/library/functions.html#sorted>`_ 
      and the list method `list.index() <https://docs.python.org/3/tutorial/datastructures.html>`_
    * you will need a ternary if-else expression
"""

def deduplicate(sequence, preserve_order=False):
    """
    Remove any duplicate elements from the given sequence.

    :param sequence: list - the sequence to remove duplicates from
    :param preserve_order: bool - if True, the order of the original sequence
        will be preserved, if False the order of the original sequence is not
    :return: the list with duplicates removed
    """
    return (
        sorted(list(set(sequence)), key=sequence.index)
        if preserve_order else
        list(set(sequence))
    )

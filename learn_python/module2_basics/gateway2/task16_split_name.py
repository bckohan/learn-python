"""
.. todo::
    Implement the split_name() function according to its docstring.

.. admonition:: Requirement

    * You must use the `str.split <https://docs.python.org/3/library/stdtypes.html?highlight=split#str.split>`_ method.
    * You must use the `str.title <https://docs.python.org/3/library/stdtypes.html?highlight=split#str.title>`_ method.
    * You must use the `str.join <https://docs.python.org/3/library/stdtypes.html?highlight=split#str.join>`_ method.

"""

def split_name(name):
    """
    Split the given name into a first, middle and last name. If the name has more than 3 words 
    the first and last words should be the first and last name and the rest should be the middle.
    All returned words will be title case. If a name is missing a middle name, return None, if a
    name is missing a last name, return None.

    .. code-block:: python

        split_name('brian christopher john kohan') == ('Brian', 'Christopher John', 'Kohan')
        split_name('brian kohan') == ('Brian', None, 'Kohan')
        split_name('brian') == ('Brian', None, None)
        split_name('') == (None, None, None)


    :param name: str - the name to split
    :return: 3-tuple - the first, middle and last name - if any name is missing None will be
        returned for that name
    """
    parts = name.split()
    first = None
    middle = None
    last = None
    if parts:
        first = parts[0].title()
    if len(parts) > 1:
        last = parts[-1].title()
    if len(parts) > 2:
        middle = ' '.join(parts[1:-1]).title()
    return first, middle, last

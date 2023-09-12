"""
.. todo::
    Implement the label_names() function according to its docstring.

.. admonition:: Requirement

    * You must use `f-strings <https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals>`_.
    * You must use `list.append <https://docs.python.org/3/tutorial/datastructures.html>`_
    * You must use `str.join <https://docs.python.org/3/library/stdtypes.html?highlight=split#str.join>`_ method.

"""

def label_names(first=None, middle=None, last=None):
    """
    Given a first, middle and last name, return a string of the style:
    first=<first name>, middle=<middle name>, last=<last name>
    If any of the names is None or the empty string, do not include it in the 
    returned label string.

    .. code-block:: python

        label_names('Brian', 'Christopher John', 'Kohan') == 'first=Brian, middle=Christopher John, last=Kohan'
        label_names('Brian', None, 'Kohan') == 'first=Brian, last=Kohan'
        label_names('Brian', None, None) == 'first=Brian'
        label_names(None, None, None) == ''
        label_names('', '', '') == ''


    :param first: str - the first name, or None
    :param middle: str - the middle name, or None
    :param last: str - the last name, or None
    :return str: - the first, middle and last names labeled if they are not None
    """
    labels = []
    if first:
        labels.append(f'first={first}')
    if middle:
        labels.append(f'middle={middle}')
    if last:
        labels.append(f'last={last}')
    return ', '.join(labels)

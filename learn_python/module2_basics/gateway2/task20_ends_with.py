"""
.. todo::
    Implement the ends_with() function according to its docstring.

.. hint::
    * Remember strings are immutable so you can modify the passed in string. When doing
      a case insensitive search, it is easier to convert the passed in strings to a standard
      case before comparing them!
    * Checkout string methods: strip(), rstrip() and lstrip().
"""


def ends_with(string, search):
    """
    Return True if the given string ends with the given search string. The comparison is
    case insensitive and ignores trailing white space!

    .. code-block:: python

        assert ends_with('anna maria  ', 'ria')
        assert ends_with('anna maria', 'anna mAria')
        assert not ends_with('anna maria', ' aria')
        assert ends_with('anna maria', ' maria')
        assert ends_with('Anna Maria', ' maria  ')
        assert not ends_with('anna maria', '  MARIA')

    :param string: str - the name of the constant
    :param search: str - the string to search for on the end of the given string
    :return bool: - True if the string ends with the given search string, False otherwise
    """
    search = search.lower().rstrip()
    return string.lower().rstrip()[-len(search):] == search

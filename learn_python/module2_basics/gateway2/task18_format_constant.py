"""
.. todo::
    Implement the format_constant() function according to its docstring.

.. admonition:: Requirement

    * You must use your implementation of get_decimal from task 11.
    * You may not use a string format specifier (i.e. the part after : in f'{3.14:.2f}')
    * You must use the built-in `round() <https://docs.python.org/3/library/functions.html#round>`_ function.
    * Your implementation must be no more than 3 statements.

.. hint::
    * The {} in f-strings can contain complex expressions, including ternary if-else expressions
      and function calls!
    * What happens when you multiply a string by a positive number? a negative number?
    * Do not worry about the number of statements requirement at first, get it working until the
      the test is failing on the number of statements check, and then see if you can collapse some
      of your statements into a smaller number of lines using f-strings.
"""
from learn_python.module2_basics.gateway2.task11_get_decimal import get_decimal

def format_constant(constant_name=None, constant_value=None, line_length=15, decimals=4):
    """
    Format the given constant into a string of the following structure:
        <constant_name><spaces><constant_value>

    Where:
     
        * constant_name is the given name of the constant
        * spaces is determined by the total line_length minus the length of the constant_name
          and constant_value strings.
        * constant_value is the given value of the constant formatted to no more or less than the
          specified number of decimal places.

    .. code-block:: python

        format_constant('π', 3.141592653589793)             == 'π        3.1416'
        format_constant('e', 2.718281828459045)             == 'e        2.7183'
        format_constant('e', 2.718281828459045, decimals=6) == 'e      2.718282'
        format_constant('Golden Ratio', (1 + 5 ** 0.5) / 2, line_length=30)      == 'Golden Ratio            2.7183'
        format_constant("Kaprekar's Constant", 6174, line_length=30, decimals=0) == "Kaprekar's Constant       6174"
        format_constant("Kaprekar's Constant", 6174, line_length=30) == "Kaprekar's Constant  6174.0000"

    :param constant_name: str - the name of the constant
    :param constant_value: float - the value of the constant
    :param line_length: int - the total length of the line
    :param decimals: int - the number of decimal places to format the constant_value to, using zeros
        if necessary. If 0, do not include the .
    :return str: - the formatted constant string
    """
    value_str = str(round(get_decimal(constant_value), ndigits=decimals))[2:decimals + 2] if decimals else ''
    value_str = f'{int(constant_value)}{"." if decimals else ""}{value_str}{"0" * (decimals - len(value_str))}'
    return f'{constant_name}{" " * (line_length - len(constant_name) - len(value_str))}{value_str}'

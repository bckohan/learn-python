"""
.. todo::
    Implement the format_constant2() function according to its docstring. This is a 
    re-implementation of format_constant(), but with different requirements!

.. admonition:: Requirement

    * You may not use your implementation of get_decimal from task 11.
    * You must use string format specifiers (i.e. the part after : in f'{3.14:.2f}')
    * Your implementation must be no more than 1 statement.
    * You may not use the * operator
    * You may not call format_constant()

.. hint::
    * You will need to use a variable as part of your f-string format specifier, how do you
      do that?
    * Try to do this in two statements first, then see if you can nest the two f-strings!
"""


def format_constant2(constant_name=None, constant_value=None, line_length=15, decimals=4):
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

        format_constant2('π', 3.141592653589793)             == 'π        3.1416'
        format_constant2('e', 2.718281828459045)             == 'e        2.7183'
        format_constant2('e', 2.718281828459045, decimals=6) == 'e      2.718282'
        format_constant2('Golden Ratio', (1 + 5 ** 0.5) / 2, line_length=30)      == 'Golden Ratio            2.7183'
        format_constant2("Kaprekar's Constant", 6174, line_length=30, decimals=0) == "Kaprekar's Constant       6174"
        format_constant2("Kaprekar's Constant", 6174, line_length=30) == "Kaprekar's Constant  6174.0000"

    :param constant_name: str - the name of the constant
    :param constant_value: float - the value of the constant
    :param line_length: int - the total length of the line
    :param decimals: int - the number of decimal places to format the constant_value to, using zeros
        if necessary. If 0, do not include the .
    :return str: - the formatted constant string
    """
    return f'{constant_name}{constant_value:>{line_length-len(constant_name)}.{decimals}f}'
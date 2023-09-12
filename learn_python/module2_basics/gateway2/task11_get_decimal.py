"""
.. todo::
    Implement a function called get_decimal that takes a float or an
    integer as an argument and returns decimal portion of the number. 

    For example:

    .. code-block:: python

        get_decimal(3.14159) == 0.14159
        get_decimal(2.71828) == 0.71828
        get_decimal(-1.1) == -0.1
        get_decimal(0) == 0.0
        get_decimal(5) == 0.0

.. admonition:: Requirement

    * Your implementation must be a single statement. 
    * The return value must be a float even when an integer is passed in.

.. hint::
    Use type coercion.
"""


def get_decimal(x):
    return float(x) - int(x)


# do tasks 10-11 now
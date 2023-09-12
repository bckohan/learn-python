"""
.. todo::
    Define a function called is_close that takes two floats as arguments
    and a third argument that is a tolerance. The function should return
    True if the difference between the two floats is less than the tolerance
    and False otherwise. You should provide a default tolerance of 1e-9.

.. admonition:: Requirement

    You may not call **math.isclose()**

.. hint::
    Checkout the python built-in function `abs() <https://docs.python.org/3/library/functions.html#abs>`_
"""
def is_close(x, y, tol=1e-9):
    return abs(x - y) < abs(tol)

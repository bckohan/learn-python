"""
.. todo::
    Implement the fibonacci() function according to its docstring.

.. admonition:: Requirement

    You must use a while loop.
"""

def fibonacci(length):
    """
    Return a list of the first fibonacci numbers that is length long. Fibonacci number x
    is defined as the sum of the two previous fibonacci numbers. Where x₀ = 0 and x₁ = 1.

    :param length: int - the number of fibonacci numbers to return
    :return: the first fibonacci numbers
    """
    fib = [0, 1]
    while len(fib) < length:
        fib.append(fib[-1] + fib[-2])
    return fib[:length]

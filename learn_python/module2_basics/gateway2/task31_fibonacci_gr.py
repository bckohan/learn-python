"""
.. todo::
    Implement the fibonacci_gr() function according to its docstring.

.. admonition:: Requirement

    You must use a break statement to exit the loop.
"""

GOLDEN_RATIO = (1 + 5 ** 0.5) / 2


def fibonacci_gr(golden_ratio_tol):
    """
    In the limit as n approaches infinity, the ratio of the n+1 fibonacci number
    to the n fibonacci number approaches the golden ratio. This function uses
    a ratio tolerance instead of a length parameter to determine the length of
    the fibonacci sequence to generate.

    :param golden_ratio_tol: float - the tolerance to use to determine the length
        of the fibonacci sequence to generate - stop generating when we are within
        abs(golden_ratio_tol) of the GOLDEN_RATIO (1.61803398875...)
    :return: a list containing the fibonacci sequence
    """

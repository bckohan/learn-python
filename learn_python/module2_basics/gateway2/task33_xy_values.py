"""
.. todo:: Implement xy_values() according to its docstring.

.. admonition:: Requirement

    You must use your float_range() function!

"""
from learn_python.module2_basics.gateway2.task32_float_range import float_range


def xy_values(pdf, start, stop, step=1e-2):
    """
    Return a list of 2 element tuples (2-tuples) where the first element is the
    x-value and the second element is the y-value of the given probability density
    function (pdf) evaluated at the corresponding x-value. The x-values should
    begin at start and end at stop, with each subsequent value being incremented
    by step.

    For example:

    .. code-block:: python

        from functools import partial
        get_distribution(
            normal_distribution,
            -5,
            5,
            1e-2
        ) == [(-5, ), (-4.99, ), (-4.98, ), ..., (4.98, ), (4.99, ), (5, )]

    :param pdf: function - a probability density function that takes a single 
        float argument (x-value) and returns a float (y-value)
    :param start: float - the starting value for x
    :param stop: float - the ending value for x
    :param step: float - the spacing between x values
    :return: list of tuples: - the (x, y) values of the distribution

    """
    return [(x, pdf(x)) for x in float_range(start, stop, step)]

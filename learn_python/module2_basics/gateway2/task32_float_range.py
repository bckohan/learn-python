"""
.. todo::
    Implement float_range() according to its docstring. You may assume that the 
    step argument will never be zero. If stop is < start the range should be in 
    decreasing order.

.. hint::
    * Use built-in abs() and determine directionality from start's relationship to stop
    * Floating point precision error might cause your loop to terminate early unless
      you account for it by comparing to a tolerance - BUT you do not know how small
      the step size will be so you cannot use a fixed tolerance - your tolerance must be
      relative to the step size. For example, if the step size is 1e-12, a tolerance of 1e-9
      is too large and will either cause the loop to terminate early or blow up the size of
      the list depending on your implementation.
"""


def float_range(start, stop, step):
    """
    Python's built-in `range() <https://docs.python.org/3/library/stdtypes.html#typesseq-range>`_
    function only works with integers. This function works similar to range() but with floats. 
    The step-sizes may be fractional, and the stop value is inclusive rather than exclusive as 
    with range().

    For example:

    .. code-block:: python

        float_range(0, 1, 0.1)           ==  [0, 0.1, 0.2, ..., 0.9, 1]
        float_range(0, -1, -0.1)         ==  [0, -0.1, -0.2, ..., -0.9, -1]
        float_range(0, -1.01, -0.1)      ==  [0, -0.1, -0.2, ..., -0.9, -1]
        float_range(0, -1, 0.1)          ==  float_range(0, -1, -0.1)
        float_range(3, 2, -0.5)          ==  [3, 2.5, 2]
        float_range(1e-12, 2e-12, 2e-13) ==  [1e-12, 1.2e-12, 1.4e-12, 1.6e-12, 1.8e-12, 2e-12]
        
        "this last one is a bit tricky b/c floating point precision issues 😈"
        float_range(0.099, 0.297, 0.099) == [0.099, 0.198, 0.297]

    :param start: float - the starting value
    :param stop: float - the ending value (inclusive! - does not include the stop value)
        note, range() is exclusive of the stop value, but float_range() is inclusive
    :param step: float - the spacing between values. This value is insensitive to its
        sign
    """
    step = abs(step) * (-1 if start > stop else 1)
    stop = stop + step/2
    rng = []
    # we use step/2 to account for floating point precision error, using any value less than
    # the step size will always work
    while (step > 0 and start < stop) or (step < 0 and start > stop):
        rng.append(start)
        start += step
    return rng

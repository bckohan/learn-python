"""
.. todo::
    Implement approximate_integral() according to its docstring.

.. hint::
    Use the built-in function `sum() <https://docs.python.org/3/library/functions.html#sum>`_ 
    with even/odd list slices, and dont forget about the x/y tuple indexing!

.. admonition:: Requirement:

    * assert that the length of the curve is non-zero
    * You must use sum()
    * You must use two list slices
    * You must use two list comprehensions
    * Your implementation may not be more than 2 statements.

"""

def approximate_integral(curve):
    """
    Use Simpson's rule to approximate the area under the given curve.

    Simpson's rule uses parabolas to approximate the curve between points:

    ∫f(x)dx = (xₙ - x₀)/(3n) * (f(x₀) + 4f(x₁) + 2f(x₂) + 4f(x₃) + ... + 4f(xₙ₋₁) + f(xₙ))

    :param curve: list - a list of 2-tuple xy-values representing a curve
    :return: float - the area under the curve as computed by simpson's rule
    """
    assert len(curve), 'The curve must not be empty!'
    return (curve[-1][0] - curve[0][0]) / (3*len(curve)) * (
        curve[0][1] + 
        curve[-1][1] + 
        4 * sum([xy[1] for xy in curve[1:-1:2]]) +
        2 * sum([xy[1] for xy in curve[2:-1:2]])
    )

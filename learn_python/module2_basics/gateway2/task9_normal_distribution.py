"""
.. todo::
    Implement normal_distribution according to its docstring.

.. hint::
    * You will need to import three things from math
    * Its possible to write this in a single statement (not including the imports)

.. warning::
    If your test fails., the test for this task will display a plot of your 
    normal distribution so you can see whats wrong. If your VSCode is full-screened, 
    the plot may be hidden behind it. The test suite will pause while the plot window
    is open, and only resume after you close the window.
"""

def normal_distribution(x, σ=1, μ=0):
    """
    Compute the value of the normal distribution at x given σ and μ. 
    
    .. note::
        Python is `unicode <https://home.unicode.org/>`_ by default. This means it can contain 
        all kinds of craaaazy characters! 🤯
    
    .. image:: ../../../learn_python/module2_basics/resources/normal_distrib.svg
        :alt: Definition of the normal distribution.
        :width: 30%

    .. image:: ../../../learn_python/module2_basics/resources/normal_plot.svg
        :alt: Plot of the normal distribution.
        :width: 50%

    |

    :param x: float - the value to compute the normal distribution at
    :param σ: float - the standard deviation of the normal distribution, larger
        values of σ result in a wider distribution, default: 1
    :param μ: float - the mean of the normal distribution (x = μ is the peak 
        of the distribution), default: 0
    """
    from math import pi, sqrt, exp
    return 1 / (σ * sqrt(2 * pi)) * exp(-0.5 * ((x - μ) / σ) ** 2)


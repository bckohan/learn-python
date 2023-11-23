"""
.. todo::
    Implement a function called time_function that invokes the a function (1st argument) 
    with the given arguments and keyword arguments (variable number of args and kwargs) 
    while timing how many seconds the given function call takes to complete.

    Should return a 2-tuple where the first value is the number of seconds the function
    took to complete and the second value is the return value of the function.

.. hint::
    * Use time.perf_counter() to get the current time in seconds before and after
    * Recall - what type is args? what type is kwargs? how do you expand those
        types into function arguments?
"""


def time_function(function, *args, **kwargs):
    from time import perf_counter
    start = perf_counter()
    ret = function(*args, **kwargs)
    return perf_counter() - start, ret

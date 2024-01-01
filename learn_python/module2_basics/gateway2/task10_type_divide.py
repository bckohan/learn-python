"""
.. todo::
    Define a function called type_divide that takes two arguments and returns
    the result of dividing the first by the second using floor division
    if both arguments are integers and regular division otherwise.
    If the second argument is zero, return None.
"""

def type_divide(var1, var2):
    if var2 == 0:
        return None
    if type(var1) is int and type(var2) is int:
        return var1 // var2
    return var1 / var2

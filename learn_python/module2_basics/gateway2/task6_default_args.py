"""
.. todo::
    Define a function called default_args that accepts 4 arguments, each 
    with a default value of your choosing. The function must return 4
    True/False values, one for each argument, where the value is True
    if the argument passed in was equal to the default value and False
    otherwise.
"""
def default_args(w=0, x=1.0, y='2', z=None):
    return w == 0, x == 1.0, y == '2', z is None

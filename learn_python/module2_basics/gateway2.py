"""
Gateway Assignment 2

This assignment is designed to exercise your knowledge of the basics of
Python covered in the module 2 lesson. Take your time and if you get
frustrated ask for help! Some of these tasks can be tricky and some of
the later ones especially are designed to challenge your handle of 
looping, conditionals and sequence indexing. This is the hard part, but
it is the gateway to the fun part! If you get intimidated looking at 
a large block of hard to understand code, take a breath and focus on
each line one by one. 

To run these tests from the command line:

    poetry run pytest -k test_gateway2

The tests will run for each task as you attempt to do the task - if no
implementation is found the test will be skipped. Once you have completed
the gateway assignment you should see that all tests pass with no skipped
tests!
"""


# TODO Task 1
# Write a function called "is_even" that accepts an integer as an 
# argument and returns True if the integer is even and False if it is not.
#   - hint use modulus operator %
def is_even(x):
    return x % 2 == 0


# TODO Task 2
# Write a function called "is_odd" that returns True if an integer is odd
# and False if it is not. You must use the is_even function you wrote above
# to implement this function. Why do it this way? Because it is more DRY
# (Dont Repeat Yourself) - If we know our is_even function works lets use
# it! Our code will be cleaner and less buggy the more of it we can reuse.
def is_odd(x):
    return not is_even(x)


# TODO Task 3
# Because None is a special value in Python that is commonly used to 
# represent uninitialized variables, it is sometimes a good idea to
# check if a variable is None before using it. Implement a function 
# called is_even_safe that works exactly like is_even but that checks
# if the value is None first and if it is returns None
def is_even_safe(x):
    if x is not None:
        return is_even(x)
    return None


# TODO Task 4
# Re-implement is_even_safe in a function called is_even_safe_ternary
# that uses a ternary expression to accomplish the same thing in a single
# statement
def is_even_safe_ternary(x):
    """
    Return True if x is even, False if it is odd and None if it is None.
    """
    return is_even(x) if x is not None else None


# TODO Task 5
# Implement a function called logic_play that accepts two integers as
# arguments and returns their product (the result of multiplying them together)
# if both are even, their quotient (the result of dividing the first by the
# second) if both are odd, and None otherwise. You must use "and" in your
# implementation of this function. You may assume all inputs will be integers.
def logic_play(first, second):
    if is_even(first) and is_even(second):
        return first * second
    elif is_odd(first) and is_odd(second):
        return first / second
    return None


# TODO Task 6
# Reimplement logic_play and call it logic_play2. This time you cannot
# use any logical operators (and, or, not) and you may make a maximum
# of three function calls. Your implementation should not exceed 5 
# statements.
def logic_play2(first, second):
    if is_even(first):
        if is_even(second):
            return first * second
    elif is_odd(second):
        return first / second
    

# Which version of logic_play is more clear? Which is more efficient?
# Which is more readable? Which is more maintainable?
#   Cleverness is not always a virtue in programming and there are
#   always tradeoffs!


# TODO Task 7
# Define a function called default_args that accepts 4 arguments, each 
# with a default value of your choosing. The function must return 4
# True/False values, one for each argument, where the value is True
# if the argument passed in was equal to the default value and False
# otherwise.
def default_args(w=0, x=1.0, y='2', z=None):
    return w == 0, x == 1.0, y == '2', z is None


# TODO Task 8
# Define a function called is_close that takes two floats as arguments
# and a third argument that is a tolerance. The function should return
# True if the difference between the two floats is less than the tolerance
# and False otherwise. You should provide a default tolerance of 1e-9.
# You may not call math.is_close()
#  hint: checkout the python built-in function abs()
def is_close(x, y, tol=1e-9):
    return abs(x - y) < tol


# TODO Remaining Tasks - implement the remaining functions according to 
# their doc strings


def normal_distribution(x, σ, μ):
    """
    Compute the value of the normal distribution at x given σ and μ.

    See ./resources/normal_distrib.png for the definition of the normal
    distribution.

    Hint: you will need to import three things from math
    Hint: its possible to write this in a single line (not including the imports)

    .. note:
        The test for this task will display a plot of your normal distribution,
        if your VSCode is fullscreened, the plot may be hidden behind it. If
        your test is failing the plot will remain open and the other tests will
        not proceed until you have a change to examin the plot to see what is
        incorrect about your implementation. If your implementation is correct
        the plot will show for 5 seconds and then the remaining tests will proceed.

    :param x: float - the value to compute the normal distribution at
    :param σ: float - the standard deviation of the normal distribution
    :param μ: float - the mean of the normal distribution (x = μ is the peak 
        of the distribution)
    """
    #from math import pi, sqrt, exp
    #return 1 / (σ * sqrt(2 * pi)) * exp(-0.5 * ((x - μ) / σ) ** 2)


def are_same_object(object1, object2):
    """
    Returns True if object1 and object2 are the same object in memory,
    False otherwise.
    """
    return object1 is object2


def identity_matrix(size):
    """
    Return the identity matrix of size=n (i.e. n x n):

        0  1  2  ...  n
    0 [[1, 0, 0, ..., 0],
    1  [0, 1, 0, ..., 0],
    2  [0, 0, 1, ..., 0],
       ...
    n  [0, 0, 0, ..., 1]]

    An identity matrix is a square matrix with 1s on the main diagonal and 0s
    everywhere else.

    :param size: int - the number of rows and columns
    :return list of lists - the identity matrix of dimensons size x size
        if size is 0, return an empty list, if size is < 0 return None
    """
    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            if i == j:
                row.append(1)
            else:
                row.append(0)
        matrix.append(row)
    
    if size < 0:
        return None
    return matrix


def identity_matrix_comprehension(size):
    """
    Same output as identity_matrix but this function should be implemented 
    using a single statement - and you can't call identity_matrix()!
    (hint: use a nested list comprehension combined with a ternary if-else expression)

    :param n: int - the size of the identity matrix
    """
    return [[1 if i == j else 0 for j in range(size)] for i in range(size)] if size >= 0 else None


def is_identity(matrix):
    """
    Check if the given matrix is an identity matrix.

    :param matrix: list of lists - the matrix to check
    :return bool - True if matrix is an identity matrix, False otherwise
        if matrix is None or an empty list, return False
    """
    if not matrix:
        return False
    size = len(matrix)
    for row_idx, row in enumerate(matrix):
        if not isinstance(row, (tuple, list)):
            return False
        if len(row) != size:
            return False
        for col_idx, value in enumerate(row):
            if row_idx == col_idx:
                if value != 1:
                    return False
            elif value != 0:
                return False
    return True

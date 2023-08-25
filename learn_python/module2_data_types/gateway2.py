"""
Functions can have doc strings just like modules and classes!

Implement the functions to their doc string specifications!
"""

from math import pi, sqrt, exp

def are_same_object(object1, object2):
    """
    Returns True if object1 and object2 are the same object in memory,
    False otherwise.
    """
    return object1 is object2


def normal_distribution(x, σ, μ):
    """
    Compute the value of the normal distribution at x given σ and μ.

    See ./resources/normal_distrib.png for the definition of the normal
    distribution.

    Hint: you will need to import three things from math
    Hint: its possible to write this in a single line

    :param x: float - the value to compute the normal distribution at
    :param σ: float - the standard deviation of the normal distribution
    :param μ: float - the mean of the normal distribution (x = μ is the peak 
        of the distribution)
    """
    #return 1 / (σ * sqrt(2 * pi)) * exp(-0.5 * ((x - μ) / σ) ** 2)


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

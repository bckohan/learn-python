"""
.. todo::
    Implement the identity_matrix2() function according to its docstring.

.. admonition:: Requirement

    * Your implementation must use list comprehension
    * Your implementation must be a single statement

    
.. hint::
    You will need a double nested list comprehension combined with a ternary if-else expression

"""
def identity_matrix2(size):
    """
    Return the identity matrix of size=n (i.e. n x n):

    ::
    
            0  1  2  ...  n
        0 [[1, 0, 0, ..., 0],
        1  [0, 1, 0, ..., 0],
        2  [0, 0, 1, ..., 0],
        ...
        n  [0, 0, 0, ..., 1]]

    An identity matrix is a square matrix with 1s on the main diagonal and 0s
    everywhere else.

    :param size: int - the number of rows and columns
    :return: the identity matrix of dimensions size x size if size is 0, 
      return an empty list, if size is < 0 return None
    """
    return [[1 if i == j else 0 for j in range(size)] for i in range(size)] if size >= 0 else None

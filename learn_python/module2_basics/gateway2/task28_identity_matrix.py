"""
.. todo::
    Implement the identity_matrix() function according to its docstring.

.. admonition:: Requirement

    Your implementation must use for loops.

    
.. hint::
    * You will need to use nested for loops to iterate over the rows and then
      the columns inside each row (or vice-versa).
    * Checkout the list.append() method.

"""

def identity_matrix(size):
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
    :return: the identity matrix of dimensions size x size
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

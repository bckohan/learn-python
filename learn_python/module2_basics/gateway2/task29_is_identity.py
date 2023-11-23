"""
.. todo::
    Implement the is_identity() function according to its docstring.

    
.. hint::
    You will need to use nested for loops to iterate over the rows and columns.

"""

def is_identity(matrix):
    """
    Check if the given matrix is an identity matrix.

    
    :param matrix: list of lists - the matrix to check
    :return: True if matrix is an identity matrix, False otherwise if matrix is None 
        or an empty list, return False
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


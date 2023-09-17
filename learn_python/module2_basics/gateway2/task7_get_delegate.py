"""
.. todo::
    Define a function called get_delegate that accepts a function as
    an argument and returns that function if it is not None, if it is None
    get_delegate should define and return a nested function called
    default_delegate that itself returns 0.

For example:

.. code-block:: python

    delegate = get_delegate(None)
    assert delegate() == 0
    def five():
        return 5
    assert get_delegate(five)() == 5

"""
def get_delegate(delegate):
    if delegate is None:
        def default_delegate():
            return 0
        return default_delegate
    return delegate

"""
The the absence of a value is ``None``. In most other languages this is called ``null``.

+-------------+--------------------------------------------------------------------------------+
| Operator    | Description                                                                    |
+-------------+--------------------------------------------------------------------------------+
| ``==``      | Equality: Checks if two operands are equal. With `None`, it checks if the      |
|             | other operand is also `None`.                                                  |
+-------------+--------------------------------------------------------------------------------+
| ``!=``      | Inequality: Checks if two operands are not equal. With `None`, it checks if    |
|             | the other operand is not `None`.                                               |
+-------------+--------------------------------------------------------------------------------+
| ``is``      | Identity: Checks if two references point to the same object. Useful to check   |
|             | if a variable is `None` (`if x is None:`).                                     |
+-------------+--------------------------------------------------------------------------------+
| ``is not``  | Non-identity: Checks if two references point to different objects. Useful to   |
|             | check if a variable is not ``None`` (if x is not None:).                       |
+-------------+--------------------------------------------------------------------------------+
"""
import ipdb

empty = None
assert empty is None  # comparison to None is done with "is" - more on this later
assert empty == None  # but == equality operator will also work!

# None evaluates to false when used in a boolean expression:
if None:
    assert False  # this will never execute because None is False

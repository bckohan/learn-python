"""
Sets

Sets are unordered collections of **unique** values, you cannot have multiple 
equivalent values in a set

+-------------+---------------------------------------------------------------------------------------------+
| Operator    | Description                                                                                 |
+-------------+---------------------------------------------------------------------------------------------+
| ``|``       | Union: Returns a set containing all elements from both sets.                                |
+-------------+---------------------------------------------------------------------------------------------+
| ``&``       | Intersection: Returns a set containing only elements that exist in both sets.               |
+-------------+---------------------------------------------------------------------------------------------+
| ``-``       | Difference: Returns a set containing elements that exist in the first set but not in the    |
|             | second set.                                                                                 |
+-------------+---------------------------------------------------------------------------------------------+
| ``^``       | Symmetric Difference: Returns a set containing elements that exist in either of the sets,   |
|             | but not in both.                                                                            |
+-------------+---------------------------------------------------------------------------------------------+
| ``<=``      | Subset: Returns True if the first set is a subset of the second set.                        |
+-------------+---------------------------------------------------------------------------------------------+
| ``<``       | Proper Subset: Returns True if the first set is a proper subset of the second set.          |
+-------------+---------------------------------------------------------------------------------------------+
| ``>=``      | Superset: Returns True if the first set is a superset of the second set.                    |
+-------------+---------------------------------------------------------------------------------------------+
| ``>``       | Proper Superset: Returns True if the first set is a proper superset of the second set.      |
+-------------+---------------------------------------------------------------------------------------------+
| ``==``      | Equality: Checks if two sets have the same elements.                                        |
+-------------+---------------------------------------------------------------------------------------------+
| ``!=``      | Inequality: Checks if two sets have different elements.                                     |
+-------------+---------------------------------------------------------------------------------------------+
| ``in``      | Membership: Checks if an item is present in the set.                                        |
+-------------+---------------------------------------------------------------------------------------------+
| ``not in``  | Non-membership: Checks if an item is not present in the set.                                |
+-------------+---------------------------------------------------------------------------------------------+

+--------------------------+----------------------------------------------------------------------------------------+
| Method                   | Description                                                                            |
+--------------------------+----------------------------------------------------------------------------------------+
| **add**                  | Adds an element to the set.                                                            |
+--------------------------+----------------------------------------------------------------------------------------+
| **clear**                | Removes all elements from the set.                                                     |
+--------------------------+----------------------------------------------------------------------------------------+
| **copy**                 | Returns a shallow copy of the set.                                                     |
+--------------------------+----------------------------------------------------------------------------------------+
| **difference**           | Returns the difference of two or more sets as a new set.                               |
+--------------------------+----------------------------------------------------------------------------------------+
| **discard**              | Removes a specified element from the set. Does not raise an error if the element is    |
|                          | not found.                                                                             |
+--------------------------+----------------------------------------------------------------------------------------+
| **intersection**         | Returns the intersection of two sets as a new set.                                     |
+--------------------------+----------------------------------------------------------------------------------------+
| **isdisjoint**           | Returns True if two sets have no elements in common.                                   |
+--------------------------+----------------------------------------------------------------------------------------+
| **issubset**             | Returns True if another set contains this set.                                         |
+--------------------------+----------------------------------------------------------------------------------------+
| **issuperset**           | Returns True if this set contains another set.                                         |
+--------------------------+----------------------------------------------------------------------------------------+
| **pop**                  | Removes and returns an arbitrary set element. Raises KeyError if the set is empty.     |
+--------------------------+----------------------------------------------------------------------------------------+
| **remove**               | Removes a specified element from the set. Raises KeyError if the element is not found. |
+--------------------------+----------------------------------------------------------------------------------------+
| **symmetric_difference** | Returns the symmetric difference of two sets as a new set.                             |
+--------------------------+----------------------------------------------------------------------------------------+
| **union**                | Returns the union of sets in a new set.                                                |
+--------------------------+----------------------------------------------------------------------------------------+
| **update**               | Updates the set with elements from another set or iterable.                            |
+--------------------------+----------------------------------------------------------------------------------------+

"""
from learn_python.module2_basics.lesson.part13_looping import *


# you can specify a set like this
my_set = {1, 2, 3}
assert type(my_set) == set
# any duplicate values will be omitted!
assert my_set == {1, 2, 3} == {1, 2, 3, 1, 2, 3}

# you can construct a set from a list to remove duplicates!
assert set([1, 2, 3, 1, 2, 3]) == {1, 2, 3}

# sets are handy for set operations like:
#    |  (union):                combine two lists into one list with no duplicates
#    &  (intersection):         get only the shared elements of two lists
#    ^  (symmetric difference): get only the elements that are in one list or the other but not both
#    -  (difference):           get only the elements of one list that are not in the other

assert {1, 2, 3, 6} | {2, 3, 4, 5} == {1, 2, 3, 4, 5, 6}
assert {1, 2, 3, 6} & {2, 3, 4, 5} == {2, 3}
assert {1, 2, 3, 6} - {2, 3, 4, 5} == {1, 6}
assert {1, 2, 3, 6} ^ {2, 3, 4, 5} == {1, 4, 5, 6}

# sets can be created with comprehensions too!
assert {x for x in range(10) if x % 2 == 1} == {1, 3, 5, 7, 9}

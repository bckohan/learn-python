"""
Dictionaries are collections of key-value pairs:
    * values may be anything! including other dictionaries!
    * keys can be any python type that is "hashable" - we'll talk about this
      later but for now just know that most builtin primitive types are 
      hashable

+-------------+---------------------------------------------------------------------------------------------+
| Operator    | Description                                                                                 |
+-------------+---------------------------------------------------------------------------------------------+
| ``[]``      | Accesses the item with the specified key. Raises KeyError if the key is not found.          |
+-------------+---------------------------------------------------------------------------------------------+
| ``in``      | Membership: Checks if a key is present in the dictionary.                                   |
+-------------+---------------------------------------------------------------------------------------------+
| ``not in``  | Non-membership: Checks if a key is not present in the dictionary.                           |
+-------------+---------------------------------------------------------------------------------------------+
| ``==``      | Equality: Checks if two dictionaries have the same key-value pairs.                         |
+-------------+---------------------------------------------------------------------------------------------+
| ``!=``      | Inequality: Checks if two dictionaries have different key-value pairs.                      |
+-------------+---------------------------------------------------------------------------------------------+

+------------------+----------------------------------------------------------------------------------------+
| Method           | Description                                                                            |
+------------------+----------------------------------------------------------------------------------------+
| **clear**        | Removes all items from the dictionary.                                                 |
+------------------+----------------------------------------------------------------------------------------+
| **copy**         | Returns a shallow copy of the dictionary.                                              |
+------------------+----------------------------------------------------------------------------------------+
| **fromkeys**     | Creates a new dictionary with keys from an iterable and values set to a specified      |
|                  | value.                                                                                 |
+------------------+----------------------------------------------------------------------------------------+
| **get**          | Returns the value for a key if it exists in the dictionary.                            |
+------------------+----------------------------------------------------------------------------------------+
| **items**        | Returns a view object that displays a list of dictionary's key-value tuple pairs.      |
+------------------+----------------------------------------------------------------------------------------+
| **keys**         | Returns a view object that displays a list of all the keys in the dictionary.          |
+------------------+----------------------------------------------------------------------------------------+
| **pop**          | Removes and returns the value of the key specified.                                    |
+------------------+----------------------------------------------------------------------------------------+
| **popitem**      | Removes the last inserted key-value pair from the dictionary and returns it.           |
+------------------+----------------------------------------------------------------------------------------+
| **setdefault**   | Returns the value of a specified key. If the key does not exist: inserts the key, with |
|                  | the specified value.                                                                   |
+------------------+----------------------------------------------------------------------------------------+
| **update**       | Updates the dictionary with the specified key-value pairs from another dictionary or   |
|                  | iterable.                                                                              |
+------------------+----------------------------------------------------------------------------------------+
| **values**       | Returns a view object that displays a list of all the values in the dictionary.        |
+------------------+----------------------------------------------------------------------------------------+


"""
from learn_python.module2_basics.lesson.part14_sets import *


my_dict = {
    'a': 1,
    'b': 2,
    'c': 3
}

# you can access values by key
assert my_dict['a'] == 1
assert my_dict['b'] == 2
assert my_dict['c'] == 3

# we can overwrite values by assigning to the key
my_dict['a'] = 0
assert my_dict['a'] == 0

# as with lists, keys do not have to be of the same type, and values can be other dictionaries
complex_dict = {
    0: {
        'key1': None,
        'key2': [1, 2, 3],
        'key3': []
    }
}

assert complex_dict[0] == {
    'key1': None,
    'key2': [1, 2, 3],
    'key3': []
}

# dictionaries are extremely flexible data stores and are used extensively
# in python programs to keep track of structured data! There are also
# a bunch of ways to easily serialize python dictionary data to external data
# formats like json (the most common data interchange format on the internet)


# when iterating over dictionaries you use the .items() method to get
# key-value pairs:
simple_dict = {'a': 1, 'b': 2}
for key, value in simple_dict.items():
    assert key == 'a' or key == 'b'
    assert value == 1 or value == 2

# you can wrap any iterable in enumerate(), for example:
for index, (key, value) in enumerate(simple_dict.items()):
    # since python 3.7 dictionaries iterate in insertion order, so we
    #   know that the below code will work!
    if index == 0:
        assert key == 'a'
        assert value == 1
    elif index == 1:
        assert key == 'b'
        assert value == 2
    else:
        assert False, 'this should never happen!'

# dictionaries have comprehensions too!
assert {
    key: value
    for key, value in simple_dict.items()
    if key != 'a'
} == {'b': 2}

assert {i: str(i) for i in range(3)} == {0: '0', 1: '1', 2: '2'}

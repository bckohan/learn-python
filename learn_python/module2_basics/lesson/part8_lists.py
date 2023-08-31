"""
Lists are sequences of values in a contiguous chunk of memory

+---------+----------------------------------------------------------------------------------------+
| Operator| Description                                                                            |
+---------+----------------------------------------------------------------------------------------+
| +       | Concatenation: Combines two lists.                                                     |
+---------+----------------------------------------------------------------------------------------+
| *       | Repetition: Replicates the list a given number of times.                               |
+---------+----------------------------------------------------------------------------------------+
| ==      | Equality: Checks if two lists have the same elements in the same order.                |
+---------+----------------------------------------------------------------------------------------+
| !=      | Inequality: Checks if two lists are different.                                         |
+---------+----------------------------------------------------------------------------------------+
| <       | Less than: Compares lists lexicographically.                                           |
+---------+----------------------------------------------------------------------------------------+
| >       | Greater than: Compares lists lexicographically.                                        |
+---------+----------------------------------------------------------------------------------------+
| <=      | Less than or equal to: Compares lists lexicographically.                               |
+---------+----------------------------------------------------------------------------------------+
| >=      | Greater than or equal to: Compares lists lexicographically.                            |
+---------+----------------------------------------------------------------------------------------+
| in      | Membership: Checks if an item is present in the list.                                  |
+---------+----------------------------------------------------------------------------------------+
| not in  | Non-membership: Checks if an item is not present in the list.                          |
+---------+----------------------------------------------------------------------------------------+
| del     | Delete: Remove the given element or slice from the list                                |
+---------+----------------------------------------------------------------------------------------+

+----------------+----------------------------------------------------------------------------------------+
| Method         | Description                                                                            |
+----------------+----------------------------------------------------------------------------------------+
| list.append    | Adds an element at the end of the list.                                                |
+----------------+----------------------------------------------------------------------------------------+
| list.clear     | Removes all elements from the list.                                                    |
+----------------+----------------------------------------------------------------------------------------+
| list.copy      | Returns a shallow copy of the list.                                                    |
+----------------+----------------------------------------------------------------------------------------+
| list.count     | Returns the number of elements with the specified value.                               |
+----------------+----------------------------------------------------------------------------------------+
| list.extend    | Adds the elements of a list (or any iterable) to the end of the current list.          |
+----------------+----------------------------------------------------------------------------------------+
| list.index     | Returns the index of the first element with the specified value.                       |
+----------------+----------------------------------------------------------------------------------------+
| list.insert    | Adds an element at a specified position.                                               |
+----------------+----------------------------------------------------------------------------------------+
| list.pop       | Removes and returns the element at a specified position (default is the last item).    |
+----------------+----------------------------------------------------------------------------------------+
| list.remove    | Removes the first item with the specified value.                                       |
+----------------+----------------------------------------------------------------------------------------+
| list.reverse   | Reverses the order of the list.                                                        |
+----------------+----------------------------------------------------------------------------------------+
| list.sort      | Sorts the list in place.                                                               |
+----------------+----------------------------------------------------------------------------------------+

"""
from learn_python.module2_basics.lesson.part7_type_casting import *

my_list = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
# you can access elements of a list by index (starting at 0)
assert my_list[0] == my_list[-10] == 0
assert my_list[1] == my_list[-9] == 1
# python also supports negative indexing (i.e. count from the end, starting at -1)

# lists are mutable, meaning we can change their elements!
my_list[9] = -1
assert my_list == [0, 1, 1, 2, 3, 5, 8, 13, 21, -1]

# you can slice lists to get a sub-list
assert my_list[1:3] == [1, 1]

# when a slice index is omitted it defaults to None, which for the first
# slice index means 0 and the last slice index means the length of the list
assert my_list[:3] == my_list[None:3] == [0, 1, 1]
assert my_list[1:] == my_list[1:None] == [1, 1, 2, 3, 5, 8, 13, 21, -1]
assert my_list[:] == [0, 1, 1, 2, 3, 5, 8, 13, 21, -1]

# you can also slice with a step size, e.g. take every 2nd element:
assert my_list[::2] == [0, 1, 3, 8, 21]

# slicing is forgiving! This means that if you take a slice
# larger than the list, it will just return as much as it can:
assert my_list[:100] == [0, 1, 1, 2, 3, 5, 8, 13, 21, -1]
assert my_list[100:] == []  # start at element 100 which doesn't exist!
assert my_list[-100:] == [0, 1, 1, 2, 3, 5, 8, 13, 21, -1]

# Indexing is not forgiving! If you try to access an index that does not exist
# you will get an error:
# my_list[100] -> this will error out with an IndexError
# my_list[-100] -> this will error out with an IndexError

# you can delete elements by using the del operator
del my_list[-1]
assert my_list == [0, 1, 1, 2, 3, 5, 8, 13, 21]

# del also works on slices!
del my_list[-2:]
assert my_list == [0, 1, 1, 2, 3, 5, 8]

# you can concatenate lists together with +
my_list += [13, 21, 34]
assert my_list == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# len() is a built-in function that returns the length of a list
assert len(my_list) == 10

# you might frequently see len() used in slicing, all of the below are
# equivalent. Also in python if we have really long line we can use \
# to break it up into multiple lines (it is better to avoid writing long lines!)
assert \
    my_list[0:10] == \
    my_list[:len(my_list)] == \
    my_list[:] == \
    my_list == \
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# lists can contain elements of multiple different types
multi_type_list = [
    1,
    'hello',
    3.0,
    True,
    None,
    [1, 2, 3]
] # lists can also be multi-line without using \
assert len(multi_type_list) == 6
assert multi_type_list[-2] is None
assert multi_type_list[-1] == [1, 2, 3]  # including other lists!

# if you have a list of lists, you can think of it as a matrix!
matrix = [
    [1, 2, 3], 
    [4, 5, 6], 
    [7, 8, 9]
]
assert matrix[0][0] == 1
assert matrix[1][1] == 5
assert matrix[2][2] == 9
assert matrix[2][0] == 7
assert matrix[0][2] == 3 

# all sequences including lists can be empty!
my_empty_list = []
assert len(my_empty_list) == 0
# when sequences are empty, they evaluate to False
assert not my_empty_list
# written another way:
assert bool(my_empty_list) is False

# because of this you will frequently see code like:
if my_list:
    pass  # do something with my_list because it is not empty!

# the "in" operator checks if a value is in a sequence
assert 1 in my_list
assert 15 not in my_list  # use "not in" instead of not (x in y)
# but this will still work
assert not (15 in my_list)

# what happens when you multiply a list by an integer? 
#   Probably not what you think if you do a lot of math!

# the sorted() built-in function gives us a quick and easy way to sort an
# iterable (like a list) in ascending order, sorted will work on any iterable
# that contains elements that can be compared to each other using the < operator
assert sorted([3, 2, 1]) == [1, 2, 3]

# what happens when we try to sort a list with multiple types that cannot be
# compared to each other?

# this will error out! Try it!
#   sorted([3, 2, 1, 'hello'])

# reversed() is another built-in function that gives us a quick and easy way
# to reverse the order of an iterable (like a list) - note reversed() does
# not sort the list, it just reverses it! reversed will work on any iterable
# but it does not return a list - it returns a special object that can be
# converted to a list using the list() function
assert list(reversed([4, 7, 2])) == [2, 7, 4]
# ****************************************************************************

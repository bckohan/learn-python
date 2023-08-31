"""
Strings
Strings are sequences of characters you can use either ' or " to define a 
one-line string. Strings in Python are immutable!

+---------+----------------------------------------------------------------------------------------+
| Operator| Description                                                                            |
+---------+----------------------------------------------------------------------------------------+
| +       | Concatenation: Combines two strings.                                                   |
+---------+----------------------------------------------------------------------------------------+
| *       | Repetition: Replicates the string a given number of times.                             |
+---------+----------------------------------------------------------------------------------------+
| ==      | Equality: Checks if two strings have the same sequence of characters.                  |
+---------+----------------------------------------------------------------------------------------+
| !=      | Inequality: Checks if two strings are different.                                       |
+---------+----------------------------------------------------------------------------------------+
| <       | Less than: Compares strings lexicographically (alphabetical order).                    |
+---------+----------------------------------------------------------------------------------------+
| >       | Greater than: Compares strings lexicographically.                                      |
+---------+----------------------------------------------------------------------------------------+
| <=      | Less than or equal to: Compares strings lexicographically.                             |
+---------+----------------------------------------------------------------------------------------+
| >=      | Greater than or equal to: Compares strings lexicographically.                          |
+---------+----------------------------------------------------------------------------------------+
| in      | Membership: Checks if a substring is present in the string.                            |
+---------+----------------------------------------------------------------------------------------+
| not in  | Non-membership: Checks if a substring is not present in the string.                    |
+---------+----------------------------------------------------------------------------------------+

+----------------+----------------------------------------------------------------------------------------+
| Method         | Description                                                                            |
+----------------+----------------------------------------------------------------------------------------+
| str.capitalize | Returns a copy of the string with its first character capitalized and the rest         |
| lowercased.    |                                                                                        |
+----------------+----------------------------------------------------------------------------------------+
| str.center     | Returns a centered string of a specified width.                                        |
+----------------+----------------------------------------------------------------------------------------+
| str.count      | Returns the number of occurrences of a substring in the string.                        |
+----------------+----------------------------------------------------------------------------------------+
| str.endswith   | Returns True if the string ends with the specified suffix, otherwise returns False.    |
+----------------+----------------------------------------------------------------------------------------+
| str.startswith | Returns True if the string starts with the specified prefix, otherwise returns False.  |
+----------------+----------------------------------------------------------------------------------------+
| str.find       | Searches the string for a specified value and returns its position, or -1 if not found.|
+----------------+----------------------------------------------------------------------------------------+
| str.format     | Formats the string using the specified format string and arguments.                    |
+----------------+----------------------------------------------------------------------------------------+
| str.index      | Searches the string for a specified value and returns its position, or raises an error |
|                | if not found.                                                                          |
+----------------+----------------------------------------------------------------------------------------+
| str.join       | Joins the items of an iterable to the end of the string.                               |
+----------------+----------------------------------------------------------------------------------------+
| str.lower      | Converts a string into lower case.                                                     |
+----------------+----------------------------------------------------------------------------------------+
| str.upper      | Converts a string into upper case.                                                     |
+----------------+----------------------------------------------------------------------------------------+
| str.replace    | Replaces a string with another string.                                                 |
+----------------+----------------------------------------------------------------------------------------+
| str.split      | Splits the string at the specified separator and returns a list of substrings.         |
+----------------+----------------------------------------------------------------------------------------+
| str.strip      | Returns a trimmed version of the string.                                               |
+----------------+----------------------------------------------------------------------------------------+
| str.title      | Converts the first character of each word to uppercase and the remaining characters to |
|                | lowercase.                                                                             |
+----------------+----------------------------------------------------------------------------------------+

"""
from learn_python.module2_basics.lesson.part11_looping import *


my_string = 'hello world'
assert my_string == "hello world"

# if you want to use the ' or " character in a string, you can "escape" it with \
#  or conveniently you can use the alternate quote character to define the string:
assert 'hello "world"' == "hello \"world\""
assert "hello 'world'" == 'hello \'world\''

# most of the immutable (unchanging) list operators are available, including 
# indexing and slicing!

# recall my_string == 'hello world'
assert my_string[0] == 'h'
assert my_string[-1] == 'd'
assert my_string[0:5] == 'hello'
assert my_string[6:] == 'world'
assert my_string[::2] == 'hlowrd'  # slice to every other character

# assignment to an element is not available because strings are immutable!
#   my_string[0] = 'H' -> this will error out!

# concatenate strings using +
assert 'hello' + ' ' + 'world' == 'hello world'

# the += operator is short for "add and assign" like on integers
my_string += '!'
assert my_string == 'hello world!'

# what else can you do with string operators? hint try to multiply a string by
# an integer!

# f-strings are a convenient way to combine strings with variables using
#   configurable formatting
# f-strings are prefixed with the letter f, and variables are surrounded by {}
assert f'my_int == {my_int}' == 'my_int == 10'

# f-strings have configurable formatting, for example you can specify the number
# of decimal places to display for a float
assert f'my_float == {my_float:.2f}' == 'my_float == 345.60'
# or pad an integer with zeros
assert f'my_int == {my_int:03d}' == 'my_int == 010'

# the formatting options are numerous and the standard library documentation is
# extensive (https://docs.python.org/3/library/string.html#formatspec) and therefore
# hard to read! I recommend asking chatgpt questions like: 
#   how do I pad an integer with empty spaces in a python f-string

# combining strings with variables has gone through a few iterations in python:
#   optionally read more: https://realpython.com/python-f-strings/
# we used to do f-strings like this:
assert 'my_int == %d' % my_int == 'my_int == 10'
# or like this
assert 'my_int == {}'.format(my_int) == 'my_int == 10'

# f-strings are clearly more readable, but lots of old code is still around that
# uses the old methods!

# lets just chop that last "!" off the end of my_string, by re-assigning it
#  to a slice of itself :-)
assert my_string == 'hello world!'
my_string = my_string[:-1]
assert my_string == 'hello world'

# as with lists, the empty string evaluates to False
assert not ''

# which means you will see code like:
if my_string:
    pass  # do something with my_string because it is not empty!

# working with strings is a very common and important task in programming because
# its the predominant way our program talks to humans!
# we will devote an entire module to it later - for now just understand these
# basics!

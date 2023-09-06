"""
Strings are sequences of characters you can use either ' or " to define a 
one-line string. Strings in Python are immutable!

+-------------+-----------------------------------------------------------------------+-------------------+
| Operator    | Description                                                           | Example           |
+-------------+-----------------------------------------------------------------------+-------------------+
| ``+``       | Concatenation: Combines two strings.                                  | 'a' + 'b' == 'ab' |
+-------------+-----------------------------------------------------------------------+-------------------+
| ``*``       | Repetition: Replicates the string a given number of times.            | 'a' * 3 == 'aaa'  |
+-------------+-----------------------------------------------------------------------+-------------------+
| ``==``      | Equality: Checks if two strings have the same sequence of characters. | 'ab' == 'ab'      |
+-------------+-----------------------------------------------------------------------+-------------------+
| ``!=``      | Inequality: Checks if two strings are different.                      | 'aa' != 'ab'      |
+-------------+-----------------------------------------------------------------------+-------------------+
| ``<``       | Less than: Compares strings lexicographically (alphabetical order).   | 'aa' < 'ab'       |
+-------------+-----------------------------------------------------------------------+-------------------+
| ``>``       | Greater than: Compares strings lexicographically.                     | 'ab' > 'aa'       |
+-------------+-----------------------------------------------------------------------+-------------------+
| ``<=``      | Less than or equal to: Compares strings lexicographically.            | 'aa' <= 'aa'      |
+-------------+-----------------------------------------------------------------------+-------------------+
| ``>=``      | Greater than or equal to: Compares strings lexicographically.         | 'ab' >= 'ab'      |
+-------------+-----------------------------------------------------------------------+-------------------+
| ``in``      | Membership: Checks if a substring is present in the string.           | 'bc' in 'abc'     |
+-------------+-----------------------------------------------------------------------+-------------------+
| ``not in``  | Non-membership: Checks if a substring is not present in the string.   | 'cb' not in 'abc' |
+-------------+-----------------------------------------------------------------------+-------------------+

+----------------+----------------------------------------------------------------------------------------+
| Method         | Description                                                                            |
+----------------+----------------------------------------------------------------------------------------+
| **capitalize** | Returns a copy of the string with its first character capitalized and the rest         |
|                | lowercased.                                                                            |
+----------------+----------------------------------------------------------------------------------------+
| **center**     | Returns a centered string of a specified width.                                        |
+----------------+----------------------------------------------------------------------------------------+
| **count**      | Returns the number of occurrences of a substring in the string.                        |
+----------------+----------------------------------------------------------------------------------------+
| **endswith**   | Returns True if the string ends with the specified suffix, otherwise returns False.    |
+----------------+----------------------------------------------------------------------------------------+
| **startswith** | Returns True if the string starts with the specified prefix, otherwise returns False.  |
+----------------+----------------------------------------------------------------------------------------+
| **find**       | Searches the string for a specified value and returns its position, or -1 if not found.|
+----------------+----------------------------------------------------------------------------------------+
| **format**     | Formats the string using the specified format string and arguments.                    |
+----------------+----------------------------------------------------------------------------------------+
| **index**      | Searches the string for a specified value and returns its position, or raises an error |
|                | if not found.                                                                          |
+----------------+----------------------------------------------------------------------------------------+
| **join**       | Joins the items of an iterable to the end of the string.                               |
+----------------+----------------------------------------------------------------------------------------+
| **lower**      | Converts a string into lower case.                                                     |
+----------------+----------------------------------------------------------------------------------------+
| **upper**      | Converts a string into upper case.                                                     |
+----------------+----------------------------------------------------------------------------------------+
| **replace**    | Replaces a string with another string.                                                 |
+----------------+----------------------------------------------------------------------------------------+
| **split**      | Splits the string at the specified separator and returns a list of substrings.         |
+----------------+----------------------------------------------------------------------------------------+
| **strip**      | Returns a trimmed version of the string.                                               |
+----------------+----------------------------------------------------------------------------------------+
| **title**      | Converts the first character of each word to uppercase and the remaining characters to |
|                | lowercase.                                                                             |
+----------------+----------------------------------------------------------------------------------------+

Some quick references for f-string formatting:

    * `Quick ref for common f-string formatting <https://fstring.help/cheat/>`_
    * `A more extensive quick reference <https://cheatography.com/brianallan/cheat-sheets/python-f-strings-basics/pdf/>`_
    * `And the official format string specifier reference <https://docs.python.org/3/library/string.html#formatstrings>`_
"""
from learn_python.module2_basics.lesson.part9_tuples import *


my_string = 'hello world'
assert my_string == "hello world"

# if you want to use the ' or " character in a string, you can "escape" it with \
# or conveniently you can use the alternate quote character to define the string:
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
assert len(my_string) == 11

# assignment to an element is not available because strings are immutable!
# my_string[0] = 'H' -> this will error out!

# concatenate strings using +
assert 'hello' + ' ' + 'world' == 'hello world'

# the += operator is short for "add and assign" like on integers
my_string += '!'
assert my_string == 'hello world!'

# If two strings literals are next to each other, Python will implicitly concatenate them:
assert my_string == 'hello ' 'world!'

# we could also split this onto multiple lines:
assert my_string == (
    'hello'
    ' '
    'world'
    '!'
)

# what else can you do with string operators? hint try to multiply a string by
# an integer!

# f-strings are a convenient way to combine strings with variables using
# configurable formatting
# f-strings are prefixed with the letter f, and variables are surrounded by {}
assert f'my_int == {my_int}' == 'my_int == 3'

# f-strings have configurable formatting, for example you can specify the number
# of decimal places to display for a float
assert f'my_float == {my_float:.2f}' == 'my_float == 345.60'
# or pad an integer with zeros
assert f'my_int == {my_int:03d}' == 'my_int == 003'
# there are many formatting directives

# You can do almost any kind of formatting you want by passing the right format specifier.
# This can help eliminate complicated string concatenation and formatting logic in code
# which helps keep your code more readable.
# The specifier language is complex, and the standard library documentation is
# extensive (https://docs.python.org/3/library/string.html#formatspec). It can be 
# hard to read! I recommend asking chatgpt questions like: 
#   How do I pad an integer with empty spaces in a python f-string?
# you'd do that like this:
assert f'{5:>5}' == '    5'
assert f'{5:<5}' == '5    '
assert f'{5:.>5}' == '....5'
assert f'{3.1415:.2f}' == '3.14'

# combining strings with variables has gone through a few iterations in python:
# optionally read more: https://realpython.com/python-f-strings/
# we used to do f-strings like this:
assert 'my_int == %d' % my_int == 'my_int == 3'
# or like this
assert 'my_int == {}'.format(my_int) == 'my_int == 3'

# f-strings are clearly more readable, but lots of old code is still around that
# uses the old methods, so you will definitely encounter it in examples or 
# other people's code

# lets just chop that last "!" off the end of my_string, by re-assigning it
# to a slice of itself :-)
assert my_string == 'hello world!'
my_string = my_string[:-1]
assert my_string == 'hello world'

# as with lists, the empty string evaluates to False
assert not ''

# which means you will see code like:
if my_string:
    pass  # do something with my_string because it is not empty!

# working with strings is a very common and important task in programming because
# its the predominant way our program talks to humans! It is also important because
# lots of data in the wild exists in unstructured strings, so we need to know how to
# parse those strings into structured data types our programs can easily work with.
#
# We will devote an entire module to it later - for now just understand these
# basics - they are sufficient for 95% of string related work!

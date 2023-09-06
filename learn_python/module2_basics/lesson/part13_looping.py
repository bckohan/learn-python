"""
Looping, Iteration & Comprehensions

There are two types of loops in python, for loops and while loops
loops let you do something repeatedly until a condition is met.
"""
from learn_python.module2_basics.lesson.part12_immutability import *


# while loops are the most basic type of loop, they repeat until a condition
# is met while <condition>:
while my_int < 10:  # add 1 to my_int until my_int is >= 10
    my_int += 1

assert my_int == 10

# the "break" keyword can be used to exit a loop early, for example the above loop
# is equivalent to:
my_int = 3
while True:
    my_int += 1
    if my_int >= 10:
        break

assert my_int == 10

# careful! if the if condition above was never met, the loop would run forever
#  this is called an "infinite loop" and it will hang your program - if this
#  happens, enter ctrl-c in your terminal to kill the program

# the "continue" keyword can be used to skip the rest of the loop and start the
# next iteration of the loop early
my_int = 0
while my_int < 10:
    my_int += 1
    if my_int % 2 == 0:  # skip even numbers
        continue
    assert my_int % 2 == 1  # what operator is this??


# for loops are more common in python, they iterate over a sequence of values
#  and assign each value to a variable: 
#   for <variable> in <sequence>:

my_other_list = []
for element in my_list:
    my_other_list.append(element)

assert my_other_list == my_list

# continue and break also work inside for loops!

# the built-in range() function is a convenient way to generate a sequence of integers
zero_to_nine = []
for i in range(10):
    zero_to_nine.append(i)

assert zero_to_nine == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# python provides a shorthand for creating lists with loops called a "comprehension":
assert zero_to_nine == [i for i in range(10)]

# when you see a list comprehension, read it as "for each i in range(10), 
#  add i to the list" this is a very common pattern in python!

# you can also use comprehensions to filter elements of a list, by adding a 
# condition to the end, this will only add i to the list if the trailing 
# if condition is True:
assert [i for i in range(10) if i % 2 == 0] == [0, 2, 4, 6, 8]

# we could also add some spaces to this to make it more readable:
assert [
    i for i in range(10)
    if i % 2 == 0
] == [0, 2, 4, 6, 8]

# you might wonder if range(10) is returning a list and if it is why bother with
#  the comprehension?
#  but it is not! range() returns a special type called a "generator" that we'll
#  talk about later, but for now just know that it is a sequence of values that
#  can be iterated over like a list, but it is not a list! you can convert it
#  to a list with the list() function:
assert range(10) != zero_to_nine
assert list(range(10)) == zero_to_nine

# list() will turn any iterable type (or sequence) into a list, for example a 
#  string is an iterable of characters:
assert list('hello') == ['h', 'e', 'l', 'l', 'o']

# the built-in enumerate() function is a convenient way to iterate over a sequence and
#  get the index of each element:
for index, element in enumerate(my_list):  # enumerate() returns a 2-tuple that we can unpack!
    assert element == my_list[index]

# there is also a built-in reversed() function that iterates over a sequence
#  in reverse order:
assert list(reversed([1, 2, 3])) == [3, 2, 1]

"""
Module 2: Basics
================

This module covers the basics of python data types, operators and looping. We 
use assertion statements to verify that the statements are accurate. 
assert <expression> is a special statement in python that will error out if 
the <expression> is False. When executed this file should produce no output 
because all the assertions are True!

You can also add an optional human readable reason after an assert expression, 
try this:

    assert False, 'False is not True!'

Assertion statements are used to test your gateway assignments! Check them out
in ./tests

This multi-line string - delineated by triple quotes - is called a docstring 
when it appears at the top of a module like this. It will be put in a special
variable called __doc__. Try this:

    from learn_python.module2_basics import lesson
    print(lesson.__doc__)
    # also try:
    help(lesson)  # look familiar?

Tools exist to convert docstrings to html or pdf documentation - much of the
python standard library is documented this way, so help() may look very familiar
to what you read on the internet!

The walkthrough in this lesson is designed to immerse you in code, but
as a quick reference these resources are better:

A nice 2-page pdf cheat sheet:
    http://sixthresearcher.com/wp-content/uploads/2016/12/Python3_reference_cheat_sheet.pdf

An extremely well organized cheat sheet web page:    
    https://www.pythoncheatsheet.org/cheatsheet/basics

Extensive cheat sheet w/ popular data science packages:
    https://www.utc.fr/~jlaforet/Suppl/python-cheatsheets.pdf

Python standard library built-in function documentation:
    https://docs.python.org/3/library/functions.html

If in the course of playing around with this file, you would like to revert it to the
original version without your edits you can use git:

    git checkout -- learn_python/module2_basics/lesson.py


What are data types?
--------------------

Data types are both:
    1. Information (values, i.e. bits & bytes stored in memory)
    2. Behavior (cpu instructions - also stored in memory)

Operators & Functions
     Operators are special functions the language supports to make code more readable
       i.e. multiply(2, 3) can be more clearly written 2 * 3

We can define our own data types!
    - Most custom data types are composites of the standard Python data types - meaning
      we create several of them together and add a little extra behavior on top to do 
      useful things
    - Custom data types will be covered in the module on Object Oriented Programming

But today we're going to go through the basics! The code covered below is the backbone
of programming in python and once you're comfortable with it you will be able to do
almost anything you want to do!

Here is the order of this lesson file:

 - Terminology
 - Debugging (pdb/ipdb)
 - None
 - Integers
 - Booleans
 - Ternary if/else statements
 - Functions
 - Floating point numbers
 - type() (dynamic typing)
 - Casting (aka Coercion)
 - Lists
 - Immutability and Memory
 - Tuples
 - Looping, Iteration & Comprehensions
 - Strings
 - Sets
 - Methods vs Operators
 - Dictionaries
 - Unpacking & Variable Function Args


Terminology
~~~~~~~~~~~

(1) Literal
  When you see a primitive type specified directly as its value it is called a
  "literal":
      - 3 is an integer literal
      - 'hello world' is a string literal
      - [0, 1, 2] is a list literal
      - {1, 2, 3} is a set literal
      - {1: 'one', 2: 'two'} is a dictionary literal
      - True and False are boolean literals

(2) Expression
  An expression is a combination of literals, variables, operators and functions.
  Expression must evaluate to a value:
      - 3 + 2 is an expression that evaluates to 5
      - 3 + 2 * 4 is an expression that evaluates to 11
      - a < b is an expression that evaluates to True if a is less than b and False otherwise
      - sqrt(4) is an expression that calls a function that evaluates to 2

(3) Statement
  A statement differs from an expression in that it does not typically evaluate
  to a value, but instead performs some action:
      - a = 3 is a statement that assigns the value 3 to the variable a
      - if a < b: is a statement that controls the flow of the program
      - def my_function(): is a statement that defines a function
      - return a + b is a statement that returns a value from a function
      - assert a == b is a statement that will error out if a is not equal to b

(4) Operator
  An operator is a special function that is used to combine expressions. Operators
  always 'operate' on one or two expressions. For example:
      - 3 + 2       in this expression + is the operator
      - 3 + 2 * 4   in this expression + and * are operators
      - not False   in this expression not is a unary operator

      
Debugging
~~~~~~~~~

You are already familiar with the Python interactive shell. Python also comes
with a debugger (Python de-bugger aka pdb). You can use the debugger to set
"breakpoints" that will allow you to run the script and stop at a given point
inside the python interactive shell. Here's how to do that:

import pdb
pdb.set_trace()  <- the script will pause execution here, try it!

Like ipython there is also an ipdb that is a little easier to work with - let's
use that one instead, it should be installed when you run poetry install.

import ipdb
ipdb.set_trace()

We will cover debugging in more detail in the next module.

You can run all of the code in these emersion lessons using:
  poetry run module2
"""

def run():
    from learn_python.module2_basics.lesson import part16_unpacking

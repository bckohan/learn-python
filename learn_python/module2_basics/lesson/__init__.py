"""

.. image:: ./img/eager-python.png
    :alt: Ready for the basics!
    :width: 35%
    :align: right

This module covers the basics of the Python language. You
will be immersed in code and the code itself will be used to illustrate how
the syntax works. The best way to learn how to code is to read lots of code!
The point of these lessons is not to exhaustively document the language - high
quality documentation already exists and you should use it. The goal here is
to expose you to lots of code in-situ in a way in which a professional Python
project might be organized and then to drill through gateway exercises that give
you immediate pass/fail feedback. 

The lessons in this module consist of commented code containing assertion 
statements that verify that the statements of how the language behaves are accurate. 

assert <expression> is a special statement in Python that will error out if 
the <expression> is False. When executed this module should produce no output 
because all the assertions are True! You can also add an optional human 
readable reason after an assert expression, try this:

    .. code-block:: python
    
        assert False, 'False is not True!'

Assertion statements are used to test your gateway assignments! Check them out
in :code-ref:`./learn_python/tests/module2.py <learn_python/tests/module2.py>`

The lessons are organized into parts. Each part covers a different topic. Read
the code line by line and try to understand what it is doing. If you don't you
can always run the code in the Python interactive shell or debugger and play 
around with it. At certain points you will be asked to complete a set of gateway
exercises.

Documentation
-------------

The code is documented in a way that a professional Python project might be.
:code-ref:`This multi-line string <learn_python/module2_basics/lesson/__init__.py>`
- delineated by triple quotes - is called a docstring when it appears at the
top of a module like this. It will be put in a special variable called __doc__.
Try this, open up an interactive python terminal:

    .. code-block:: console

        ?> poetry run ipython
        Python 3.11.4 (main, Jul 11 2023, 14:04:39) [Clang 14.0.0 (clang-1400.0.29.202)]
        Type 'copyright', 'credits' or 'license' for more information
        IPython 8.18.1 -- An enhanced Interactive Python. Type '?' for help.

        In [1]: 

Then execute these statements:

    .. code-block:: python

        from learn_python.module2_basics import lesson
        # remember when packages (directories) are imported like this it
        # refers to the __init__.py file in the package directory, so this
        # import statement imports learn_python/module2_basics/lesson/__init__.py
        
        print(lesson.__doc__)
        
        # also try:
        help(lesson)  # look familiar?

Tools exist to convert docstrings to html or pdf documentation - much of the
python standard library is documented this way, so 
`help() <https://docs.python.org/3/library/functions.html#help>`_ may look very
familiar to what you read on the internet! sphinx-doc_ is the tool used to
generate html documentation from these docstrings and it helps keep our
documentation DRY_ (Don't Repeat Yourself)! Users may be browsing the internet
or writing code when they have the need to understand how your library works -
the idea behind sphinx-doc_ is to allow that documentation to exist in one
place and be rendered in multiple formats to multiple locations so that when a
user needs it, it is there. We talked a little bit about sphinx-doc_ in the
:ref:`tools module<tools_sphinx-doc>`. sphinx-doc_ renders a markup language
called reStructuredText_ (.rst) to html, pdf, text, or epub formats. So when
you look at :code-ref:`the raw text markup <learn_python/module2_basics/lesson/__init__.py>`
from which this documentation was generated all the weird punctuation is 
rst_ markup that helps sphinx know what should be rendered as a link or a
heading, etc.

.. _external-resources:

External Resources
------------------

The walkthrough in this lesson is designed to immerse you in code, but as a quick reference these resources are better:

    * `A nice 2-page pdf cheat sheet <http://sixthresearcher.com/wp-content/uploads/2016/12/Python3_reference_cheat_sheet.pdf>`_
    * `An extremely well organized cheat sheet web page <https://www.pythoncheatsheet.org/cheatsheet/basics>`_
    * `Extensive cheat sheet w/ popular data science packages <https://www.utc.fr/~jlaforet/Suppl/python-cheatsheets.pdf>`_
    * `Python standard library built-in function documentation <https://docs.python.org/3/library/functions.html>`_
    * `Python standard library built-in data types documentation <https://docs.python.org/3/library/stdtypes.html>`_
    * `Quick ref for common f-string formatting <https://fstring.help/cheat/>`_
    
What are data types?
--------------------

Data types are both:
    1. Information (values, i.e. bits & bytes stored in memory)
    2. Behavior (cpu instructions - also stored in memory)

Operators are special functions the language supports to make code more readable.
    - multiply(2, 3) can be more clearly written 2 * 3

We can define our own data types!
    - Most custom data types are composites of the standard Python data types - meaning
      we create several of them together and add a little extra behavior on top to do 
      useful things
    - Custom data types will be covered in the module on Object Oriented Programming


.. image:: ../../learn_python/module2_basics/resources/DataTypes.svg
   :alt: Python's basic data types
   :width: 75%
   :align: center


Terminology
-----------

#. **Literal**: When you see a primitive type specified directly as its value it is called a "literal":

    .. code-block:: python
        
        3                     # integer literal
        'hello world'         # string literal
        [0, 1, 2]             # list literal
        {1, 2, 3}             # set literal
        {1: 'one', 2: 'two'}  # dictionary literal
        True                  # boolean literals

        
#. **Expression**: An expression is a combination of literals, variables, operators and functions. Expressions must evaluate to a value. Anywhere in a program where a value literal can appear, you may also use an expression!:
      
    .. code-block:: python
        
        3 + 2      # an expression that evaluates to 5
        3 + 2 * 4  # an expression that evaluates to 11
        a < b      # an expression that evaluates to True if a is less than b and False otherwise
        sqrt(4)    # is an expression that calls a function that evaluates to 2

        
#. **Statement**: A statement differs from an expression in that it does not evaluate to a value, but instead performs some action:
      
    .. code-block:: python

        a = 3               # a statement that assigns the value 3 to the variable a
        if a < b:           # a statement that controls the flow of the program
        def my_function():  # a statement that defines a function
        return a + b        # a statement that returns a value from a function
        assert a == b       # a statement that will error out if a is not equal to b

        
#. **Operator**: An operator is a special function that is used to combine expressions. Operators always 'operate' on one or two expressions. For example:
    
    .. code-block:: python

        3 + 2       # in this expression + is the operator
        3 + 2 * 4   # in this expression + and * are operators
        not False   # in this expression not is a unary operator

    .. note::
        When an operator only operates on a single value it is called a *unary operator*.
      
Debugging
---------

You are already familiar with the Python interactive shell. Python also comes
with a `debugger (Python DeBugger aka pdb). <https://docs.python.org/3/library/pdb.html>`_
You can use the debugger to set "breakpoints" that will allow you to run the script and 
stop at a given point inside the Python interactive shell. Here's how to do that:

.. code-block:: python

    import pdb
    pdb.set_trace()  # the script will pause execution here, try it!

Like ipython there is also an `ipdb <https://pypi.org/project/ipdb/>`_ that is a little 
easier to work with - let's use that one instead, it should be installed when you run 
poetry install.

.. code-block:: python

    import ipdb
    ipdb.set_trace()

We will cover debugging in more detail in the next module.

You can run all of the code in these immersion lessons using:
  
.. code-block:: bash

    poetry run module2

When you do this, nothing should happen because all of the assertion statements
are True, so no errors are thrown!

If at any point you want to halt the code at a given line and enter into the
interactive debugger simply add the following statement at the line of code you
are concerned with:

.. code-block:: python

    # I have already imported ipdb for you in the first part and all subsequent
    # parts import the part before them, so ipdb is available.
    ipdb.set_trace()

Then run `poetry run module2`. You will be dropped into the debugger at that line of
code and will be able to access all the variables in the current scope, and execute
statements to test your assumptions about the code.

If in the course of playing around with these lessons, you would like to revert a file
to its original version without your edits you can use git:

.. code-block:: bash

    git checkout -- learn_python/module2_basics/lesson/<filename>.py

"""

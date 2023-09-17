.. _module1:

===============
Module 1: Tools
===============

All you need to code and run Python is Python installed on your system and a text editor. However, 
there are lots of petty annoyances involved with writing, running, documenting, distributing, and 
maintaining Python code. Many tools exist to alleviate these burdens. This module will introduce 
you to a professional cohort of tools we will be using throughout the course. This is a slightly 
different approach to many Python courses where the language is focused on first and the tools are
either introduced later or left to the student to discover. I think this is backwards for several 
reasons:

1. We, as programmers, do not need to be tool experts. A chef, generally does not know how a knife is
   made. They exist to do work for us and ease our suffering. Even a cursory understanding of what 
   exists and what it does for you will make your programming experience easier and more sustainable.
   If a tool requires more than a cursory understanding of it to be useful, it is not a good tool.

2. Bad habits form early. Great tools have a way of forcing good habits on you. Programming at its
   core is the repeated application of patterns seen over and over again. The best way to get good
   at it fast, is to see early and often how great code is put together and great code always uses 
   great tools.

By the end of this module we will understand the basics of what the stack of tools we are using for
this course is doing for us and we will have them installed and ready to serve. We will also fork and
clone the course repository and complete our first programming assignment! The keynote presentation 
covered in the video below can be downloaded :download:`here <../../learn_python/module1/resources/Module1.key>`.

|

..  youtube:: EI1qbU32e5w
   :width: 75%
   :align: center


Tools
=====


GIT - Version Control
---------------------

.. image:: ../../learn_python/module1/resources/git.svg
   :alt: Computer Mental Model
   :width: 75%
   :align: center


Python Virtual Environments
---------------------------

.. image:: ../../learn_python/module1/resources/PythonVirtualEnvironments.svg
   :alt: Computer Mental Model
   :width: 75%
   :align: center


Fork & Clone the Course
=======================

The course repository is located `here <https://github.com/bckohan/learn-python>`_.

:code-ref:`Gateway 1 <learn_python/module1/gateway1.py>`
========================================================

:code-ref:`Part 1 <learn_python/module1/gateway1.py>`
-----------------------------------------------------

.. todo::
   In learn_python/module1 create a python module called gateway1. Write code such that when imported 
   (import learn_python.module1.gateway1) three lines should be printed to the terminal “print 1” 
   “print 2” and “print 3”:

.. code-block:: bash

   > learn-python % poetry run ipython
   Python 3.11.4 (main, Jul 11 2023, 14:04:39) [Clang 14.0.0 (clang-1400.0.29.202)]
   Type 'copyright', 'credits' or 'license' for more information
   IPython 8.14.0 -- An enhanced Interactive Python. Type '?' for help.

   In [1]: from learn_python.module1 import gateway1
   print 1
   print 2
   print 3


Testing
~~~~~~~

Were going to use pytest to test your gateway exercises! To test your implementation of part 1, 
in the learn-python root directory run:

.. code-block:: bash

   poetry run pytest -k test_gateway1_part1

If your part 1 is implemented correctly you will see that 1 test has passed::

   learn-python> poetry run pytest -k test_gateway1_part1
   =================================== test session starts ===================================
   platform darwin -- Python 3.11.4, pytest-7.4.0, pluggy-1.2.0
   rootdir: /Users/bckohan/Development/learn-python-main/learn-python
   configfile: setup.cfg
   collected 42 items / 41 deselected / 1 selected                                           

   learn_python/tests/tests.py .                                                       [100%]

   ============================ 1 passed, 41 deselected in 0.04s =============================


The code that runs our tests lives in learn_python/tests/


:code-ref:`Part 2 <learn_python/module1/gateway1.py>`
-----------------------------------------------------

.. todo::
   Adapt module gateway1 so that when it is run as an executable the “print 2” line is replaced by 
   “Hello World! Python will look for code in these directories:“ followed by a pretty print of 
   the python path. However, when gateway1 is imported as a module it should still print 3 statements 
   like part 1::

      learn-python> poetry run python ./learn_python/module1/gateway1.py
      print 1
      Hello World! Python will look for code in these directories:
      ['/Users/bckohan/Development/learn-python-main/learn-python/learn_python/module1',
      '/Users/bckohan/.pyenv/versions/3.11.4/lib/python311.zip',
      '/Users/bckohan/.pyenv/versions/3.11.4/lib/python3.11',
      '/Users/bckohan/.pyenv/versions/3.11.4/lib/python3.11/lib-dynload',
      '/Users/bckohan/Development/learn-python-main/learn-python/.venv/lib/python3.11/site-packages',
      '/Users/bckohan/Development/learn-python-main/learn-python']
      print 3


.. hint::
   * You will need an if/else statement that checks __name__
   * Google (or ChatGPT!) “python pretty print” and “how to get the python path”

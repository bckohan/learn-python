.. include:: ../refs.rst


Command Reference
=================

There are a number of commands that are part of the course code that you will have to use while
progressing through the gateway exercises. To run these commands in the course Python_ environment
installed by poetry you will need to prefix each command with ``poetry run``. For example, to build
the course documentation, you would run the following command:

.. code-block:: console

   ?> poetry run doc build
   Running Sphinx v7.2.6
   ...
   build succeeded.

   The HTML pages are in build/html.
   /Users/bckohan/Development/learn-python-main/learn-python/docs/build/html

.. note::

   As you complete the gateway exercises you should test them with the `pytest command`_ to make
   sure your solutions are correct, then rebuild the documentation. The documentation will track
   your progress through the course and help you figure out where you left off.

The commands pertinent to the course are listed below. The help outputs (i.e what you see when you
run ``poetry run <command> --help``) are included for each command. You should also try accessing
these helps from the command line!

.. typer:: learn_python.doc:app
   :prog: doc
   :show-nested:
   :make-sections:
   :width: 120

|

.. typer:: learn_python.register:register_app
   :prog: register
   :show-nested:
   :make-sections:
   :width: 120

|

.. typer:: learn_python.register:report_app
   :prog: report
   :show-nested:
   :make-sections:
   :width: 120

|

.. typer:: learn_python.delphi.tutor:delphi_app
   :prog: delphi
   :show-nested:
   :make-sections:
   :width: 120


.. _pytest command:

pytest
------

The course uses the pytest_ Python_ library to run the tests for each exercise. Each time you
want to check your work you should run pytest_. You can run the full course suite of tests simply
by running ``poetry run pytest`` from the root of the course repository. Any gateway exercises you
have not yet attempted will be skipped.

.. code-block:: console

   ?> poetry run pytest
   ============================= test session starts ==============================
   platform darwin -- Python 3.11.4, pytest-7.4.3, pluggy-1.3.0
   rootdir: /Users/bckohan/Development/learn-python-main/learn-python
   configfile: pyproject.toml
   plugins: timeout-2.2.0, anyio-4.1.0
   collected 42 items                                                             

   learn_python/tests/module1.py ss                                         [  4%]
   learn_python/tests/module2.py ssssssssssssssssssssssssssssssssssssssss   [100%]

   ============================= 42 skipped in 0.40s ==============================

To run individual tests you can use the ``-k`` option to pytest_ to select tests by name prefix.
The tests are named ``test_gateway#_testname`` For example to run all tests in gateway 1 you would:

.. code-block:: console
   
   ?> poetry run pytest -k test_gateway1
   ============================= test session starts ==============================
   platform darwin -- Python 3.11.4, pytest-7.4.3, pluggy-1.3.0
   rootdir: /Users/bckohan/Development/learn-python-main/learn-python
   configfile: pyproject.toml
   plugins: timeout-2.2.0, anyio-4.1.0
   collected 42 items / 40 deselected / 2 selected                                

   learn_python/tests/module1.py ss                                         [100%]

   ====================== 2 skipped, 40 deselected in 0.38s =======================

And to run just part1 of gateway1 you would run:

.. code-block:: console
   
   ?> poetry run pytest -k test_gateway1_part1
   ============================= test session starts ==============================
   platform darwin -- Python 3.11.4, pytest-7.4.3, pluggy-1.3.0
   rootdir: /Users/bckohan/Development/learn-python-main/learn-python
   configfile: pyproject.toml
   plugins: timeout-2.2.0, anyio-4.1.0
   collected 42 items / 41 deselected / 1 selected                                

   learn_python/tests/module1.py s                                          [100%]

   ====================== 1 skipped, 41 deselected in 0.39s =======================

pytest_ is an extensive testing library and there are many more options available. You can find
the full documentation for the command line interface `here <https://docs.pytest.org/en/latest/usage.html>`_.

The tests for each module are located under the :code-ref:`learn_python/tests <learn_python/tests/module1.py>`
directory and separated by module into individual files. Each gateway exercise has a corresponding
test function that is named ``test_gateway#_exercisename``. Have a peak at the test code if you're
curious! You could also alter the tests if you wanted to cheat 😂.

.. include:: ../refs.rst


Command Reference
=================

.. code-block:: console

   ?> poetry run doc clean
   Removing everything under 'build'...
   ?> poetry run doc build
   Running Sphinx v7.2.6
   ...
   build succeeded.

   The HTML pages are in build/html.
   /Users/bckohan/Development/learn-python-main/learn-python/docs/build/html

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


pytest
------


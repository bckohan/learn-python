.. include:: refs.rst

.. _module1:

===============
Module 1: Tools
===============

All you need to code and run Python is Python installed on your system and a text editor. However, 
there are lots of petty annoyances involved with writing, running, documenting, distributing, and 
maintaining Python code. Many tools exist to alleviate these burdens. This module will introduce 
you to a professional cohort of tools we will be using throughout the course. It is important to
invest some minimum effort in understanding the tools we use because:

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
   :width: 50%
   :align: center
   :url_parameters: ?start=1&end=107


.. _tools:

Tools
=====

For most of the tools we will be using in this course there are many alternatives. When popular alternatives exist
they are listed in tables in each section. Tools come and go and what is considered state of the art today may be
different tomorrow. Its important to not get bogged down in the minutia of each tool and instead focus on getting
it to do the immediate thing you need it to do. Expertise will come with use and picking up new tools quickly is
a valuable skill.

.. _console:

Terminal
--------

You are probably reading these words in a web browser window. A web browser is a program with a graphical interface. Graphical
interfaces give us visual cues about what they are doing and what they are capable of. Creating a graphical interface requires lots of work
and for simple programs that extra work is prohibitive and often unnecessary. That means, for this course we will have to become
familiar with the other main mode of human/machine interface - the textual interface, aka the command line, aka console, aka terminal.

In textual interfaces, we tell the computer what to do by typing text commands into a terminal window and the computer tells us what it is
doing by printing text back to us. Textual interfaces can also tell us what they are capable of - but they are limited to text documentation 
which is, by its nature, less universal (many languages) and slower to understand than the visual cues of a graphical interface. For these
reasons textual interfaces can be intimidating and are often seen in movies whenever the plot requires a character to demonstrate the mystical
connection "hackers" have with their machines. In reality, textual interfaces are just another tool and they are really quite simple.

Do not worry, to get started with Python you will not need to become a terminal expert - most programmers aren't. We will only be using a few simple commands. But first - some vocabulary:

* **commands** - programs that have textual interfaces that you can execute by typing their name in a terminal. You will create your own commands as part of this course!
* **options, arguments and parameters** - Pieces of information that commands may be initialized with, when you run them, that have some effect on what the command ends up doing. These 
  words are often used interchangeably but may have subtly different meanings depending on how they are provided to a command and the context in which they are used.
* **path** - the location of a file or a directory on the filesystem. Paths are expressed as a series of directories separated by slashes and optionally ending with a filename. (e.g. /Users/bckohan/.zshrc)
* **shell** - the program that executes the commands you type. There are many different shells but the most common are Bash and Bash derivatives.
  Different shells can have slightly different ways of expressing the same intentions (i.e. how the output of one command might be fed into another) but the names of the commands are the same because 
  commands are executable programs that are independent of the shell. Z-shell, which is very similar to Bash, is now the default on OSX platforms and all command line examples in this course will be written 
  for Z-shell. You can think of shells as minimally functional programming languages. They have their own syntax and semantics and they are used to write scripts that run on your computer. The difference is that
  shells are designed to be used interactively and to run commands rather than to be used to write full featured programs. `Read more here. <https://en.wikipedia.org/wiki/Shell_(computing)>`_
* **terminal** - the program that runs a shell and provides the textual interface window. The term terminal comes from the
  middle-early days of computing when graphical interfaces did not yet exist and the only way to interact with a computer was textual via a physical device called a terminal. The terminal 
  program is the modern equivalent of that device that runs as a program within a graphical environment. `Read more here. <https://en.wikipedia.org/wiki/Computer_terminal#Text_terminals>`_
* **POSIX** - a set of standards that promote compatibility between operating systems. The standards include a set of core commands; therefore POSIX compliant operating 
  systems have textual interfaces that are similar enough to bounce between them and feel at home. OSX is POSIX compliant, and so is Linux, which is why many programmers prefer Mac computers. Windows is 
  not POSIX compliant. This means that installing the dependencies for this course will be quite different on Windows and OSX. `Read more here. <https://en.wikipedia.org/wiki/POSIX>`_

Only POSIX commands are documented as part of this course. If you are taking the course on a Windows computer I recommend you install and use a POSIX compliant terminal emulator such as 
`Git Bash <https://gitforwindows.org/>`_.

Relative and Absolute Paths
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a path is proceeded by a slash it is an absolute path. E.g. ``/Users/bkohan/.zshrc``. This path always refers to the same file no matter where you are in the filesystem. Absolute paths start at the top level or ``root`` 
of the filesystem which is denoted by a ``/``. Sometimes however, *we can't know the absolute path to a file when we want to refer to it*. For example, if I want to direct you to the file you are reading right now, I 
can't know where you have downloaded it to on your computer's file system. I can only know the relative path to it from the repository root. Relative paths are paths that do not start with a slash. For example, this 
file, from the repository root, is at ``learn_python/module1/tools.rst``.

Basic Navigation
~~~~~~~~~~~~~~~~

Most of what you do in the terminal will be navigating the filesystem and running commands that do work on the files and directories that reside at the paths you are concerned with. A terminal window
is always tied to a current working directory (cwd). All relative paths will be resolved relative to the cwd. For example if my cwd is ``/Users/bckohan`` and I run ``ls`` (list) I will see the contents
of the ``/Users/bckohan`` directory. If I run ``ls Documents`` I will see the contents of ``/Users/bckohan/Documents``. Below are the basic navigation and file manipulation commands. 


* `cd <https://pubs.opengroup.org/onlinepubs/9699919799/utilities/cd.html>`_ - change working directory.
* `pwd <https://pubs.opengroup.org/onlinepubs/9699919799/utilities/pwd.html>`_ - print working directory.
* `ls <https://pubs.opengroup.org/onlinepubs/9699919799/utilities/pwd.html>`_ - list directory contents.
* `cp <https://pubs.opengroup.org/onlinepubs/9699919799/utilities/cp.html>`_ - copy a file.
* `mv <https://pubs.opengroup.org/onlinepubs/9699919799/utilities/mv.html>`_ - move a file. Like copy, but the original file is deleted.
* `rm <https://pubs.opengroup.org/onlinepubs/9699919799/utilities/rm.html>`_ - delete a file or directory. Be careful, there is no undo!

.. warning::
   
   Errors in specifying paths, or using an absolute path where a relative path should be used or vice-versa are significant sources of errors when using the terminal. If you are encountering errors always
   first ask yourself:

      * Am I in the right working directory to be doing what I'm doing?
      * If my commands take paths as arguments, are the paths I'm using correctly written given my current working directory and what my commands expect?

Special Characters
~~~~~~~~~~~~~~~~~~

Nearly all shells respect the following special characters, which can be thought of as shorthand aliases:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Symbol
     - Description
   * - ``.``
     - The current working directory
   * - ``..``
     - The parent directory - i.e., one directory up the filesystem hierarchy from the current directory. 
       For example, if your cwd is ``/Users/bckohan`` and you run ``ls ..``, you will see the contents of ``/Users``.
   * - ``~``
     - Your home directory. All operating systems have a concept of a home directory. This is the directory 
       that your user account is associated with and where your personal files are stored. On OSX, this is 
       usually ``/Users/<your username>``. Your cwd when the terminal starts is usually your home directory.
   * - ``*``
     - A wildcard that matches any number of characters. For example, ``*.py`` will match all files that end in ``.py``.
   * - ``$``
     - The value of an environment variable. Environment variables are discussed below.
   * - ``#``
     - A comment. Everything after this character on a line is ignored by the shell. Comments are not for interactive shell use, but are handy when you
       combine a bunch of commands into a shell executable file (.sh) files. Comments are useful for documenting your code and for temporarily 
       disabling lines of code without deleting them.
   * - ``\``
     - An escape character. If you want to use a special character literally, you can escape it with a backslash. For example, if you want to create a 
       file called ``*.py`` you can do so with ``touch \*.py``.
   


Running commands
~~~~~~~~~~~~~~~~

To run a command you type its name into the terminal and press enter. The shell will then execute the command and print the output to the terminal. The shell will also print any errors that occur. Arguments
and options are provided to a command by typing them after the command name separated by spaces:

.. code-block:: console

   ?> <command name> <options> <arguments>

Options are usually named, and can be specified with a shorthand single dash ``-`` and single character or a double dash ``--`` and a longer form name. Sometimes options take an argument 
(e.g. ``-o <argument>`` or ``--option <argument>``) and other times they do not (e.g. ``-o`` or ``--option``). When they do not they function as on/off toggles for certain behavior and are sometimes 
referred to as flags. Often both a short form and a long form of an option are available. The longer forms are usually more descriptive and can be useful when coding scripts of commands to convey more 
information about what the command is doing, but the short forms can be more convenient to type when using shells interactively.

Arguments are usually not prefixed with a name, but their meanings are inferred from their position in the command string.

For example, to run the command ``ls`` (list) with the option ``-l`` (print each listing on a new line) and the path to your
Documents directory as the first positional argument you would type:

.. code-block:: console
   
   ?> ls -l ~/Documents
 

.. warning::

   Commands are responsible for parsing their own arguments and options. This means the semantics discussed here are entirely up to the programmer who coded the command. These
   conventions are just that, conventions, and are therefore common but not universal. When you program your own command you are handed the full command string and can process that
   string however you wish. Always check the documentation for a command to see how it expects to be used.



Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Environment variables are variables that are set in the shell environment and are available to all commands that are run in that shell. Environment variables are usually set by the shell configuration
file. On OSX, the default shell is Z-shell and the configuration file is ``~/.zshrc``. You can open this file in a text editor and see the environment variables that are set there. You can also set your
own environment variables in this file. Environment variables are useful for storing information that is useful to many commands. Environment variables are prefixed with ``$`` when you intend to use them in
commands as variables. You can see all the variables currently defined in your shell by running ``env``:

.. code-block:: console

   ?> env

In Z-shell environment variables are set using the export command:

.. code-block:: console

   ?> export <variable name>=<value>

System PATH
~~~~~~~~~~~

The PATH environment variable is a list of directories that the shell will search for commands when you type them. When you type a command, the shell will search the directories in the PATH in order
until it finds a command with the name you typed. If it does not find a command with that name in any of the directories in the PATH it will print an error. The PATH is a colon separated list of
directories. You can print the PATH by running:

.. code-block:: console

   ?> echo $PATH


Other Useful commands
~~~~~~~~~~~~~~~~~~~~~

* `which <https://pubs.opengroup.org/onlinepubs/9699919799/utilities/which.html>`_ - show the absolute path of the command executable
* `grep <https://pubs.opengroup.org/onlinepubs/9699919799/utilities/grep.html>`_ - search for a string in a file or files
* `find <https://pubs.opengroup.org/onlinepubs/9699919799/utilities/find.html>`_ - find files and directories by name
* `cat <https://pubs.opengroup.org/onlinepubs/9699919799/utilities/cat.html>`_ - print the contents of a file to the terminal
* `echo <https://pubs.opengroup.org/onlinepubs/9699919799/utilities/echo.html>`_ - print a string to the terminal (variables will be resolved)
* `env <https://pubs.opengroup.org/onlinepubs/9699919799/utilities/env.html>`_ - print all environment variables

Piping
~~~~~~

Piping is passing the output of one command as the input to another command. Piping is done with the pipe character `|`. For example, to list all pdf files in your Documents directory we could pipe the output of
the `ls` command to the `grep` command and filter on the '.pdf' string:

.. code-block:: console

   ?> ls -l ~/Documents | grep .pdf

Not all commands support piping but many do and if a command operates on free form text it most likely does. 

Argument Substitution
~~~~~~~~~~~~~~~~~~~~~

A similar alternative to piping is passing the output of one command as the arguments to another. This is done by positioning the argument generating command in the position of the arguments of the outer command and surrounding it with backticks (`).
Consider a useful example:

   The ``grep`` command can search for text within files and accepts file paths as arguments. The ``find`` command can be used to find all files that match a certain naming pattern at or below a directory. So we could ask ``grep`` to find all python files under 
   ``Documents`` that contain the string ``learn_python`` like so:

   .. code-block:: console

      ?> grep -l learn_python `find ~/Documents -name "*.py"`

Getting Help
~~~~~~~~~~~~

Most commands will have a standard help option that will print some instructions about how to use the command. This option is usually invoked by either ``-h`` or ``--help``. Try:

.. code-block:: console

   ?> grep --help

On POSIX operating systems more robust documentation is usually available from the manual pages utility. Try:

.. code-block:: console

   ?> man grep


Version Control (git_)
---------------------

The directories that contain the code and other files that comprise a software program are often referred to as code bases.
Code bases are large collections of code (text files) and sometimes media files (images, etc). Version Control Software (VCS) 
enables teams of engineers to work on the same code base. VCS tracks who is changing what files and how and allows engineers to 
work on the same files and then later merge their changes together. VCS also allows engineers to revert to previous versions of 
files and to see who made what changes and when. VCS is an essential tool for collaborative development and can also be a great 
way to backup your code!

In this course we will be using the free industry standard VCS tool: git_.

..  youtube:: EI1qbU32e5w
   :width: 50%
   :align: center
   :url_parameters: ?start=109&end=587

|

Some other common version control systems are listed in the table below:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Version Control Software
     - Description
   * - git_
     - A free and open-source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.
   * - `Subversion (SVN) <https://subversion.apache.org/>`_
     - A centralized version control system characterized by its reliability as a safe haven for valuable data and its simplicity of concept.
   * - `Mercurial <https://www.mercurial-scm.org/>`_
     - A free, distributed source control management tool, primarily implemented in Python, designed to efficiently handle projects of any size.
   * - `CVS (Concurrent Versions System) <https://www.nongnu.org/cvs/>`_
     - An older version control system that is still used in some projects; it keeps track of all work and changes in a set of files.



Repository Hosting (GitHub)
---------------------------

GitHub_ is a freemium web service owned by Microsoft that provides git repositories hosted on the web. GitHub_ is
the most popular git hosting service for open source software development but it is not the only service in town.
GitLab_ is also popular. GitHub_ provides a nice user interface with additional bells and whistles that ease the
use of git and using it or another hosting service is the best way to make your code available to others.


..  youtube:: EI1qbU32e5w
   :width: 50%
   :align: center
   :url_parameters: ?start=588&end=667

|

Some additional repository hosting services are listed in the table below:

.. list-table::
   :header-rows: 1

   * - Service
     - VCS Used
     - Description
   * - `GitHub <https://github.com>`_
     - Git
     - GitHub is a widely-used web-based hosting service for version control using Git. It offers distributed version control and source code management (SCM) functionality of Git, plus its own features.
   * - `GitLab <https://gitlab.com>`_
     - Git
     - GitLab is a web-based Git repository manager with wiki, issue tracking, CI/CD pipeline features, and more.
   * - `Bitbucket <https://bitbucket.org>`_
     - Git, Mercurial
     - Bitbucket is a web-based version control repository hosting service owned by Atlassian, for source code and development projects that use either Mercurial or Git revision control systems.
   * - `SourceForge <https://sourceforge.net>`_
     - Git, Mercurial, SVN
     - SourceForge offers a web-based source code repository. It acts as a centralized location for software developers to control and manage free and open-source software development.
   * - `AWS CodeCommit <https://aws.amazon.com/codecommit>`_
     - Git
     - AWS CodeCommit is a source control service hosted by Amazon Web Services that you can use to privately store and manage assets in the cloud.

.. _python_installation:

Python Installation (PyEnv_)
----------------------------

Python_ is just another software package which means it grows and changes over time and there are always subsequent versions that
will have different features and capabilities. Sometimes code written for one version of Python will not work in follow on versions.
Famously, there were breaking changes in the interpreter from the Python_ 2.x series to the 3.x series that required many developers
to invest significant effort to port their code to the new version. This is why it is important to be able to install and easily switch
between more than one version of Python_ on your system at any given time. This makes Python_ a little different than most software packages
where it is completely fine to just install the latest version and forget about it.

PyEnv_ is an excellent tool for managing multiple versions of Python_ on your system. It is a command line tool that allows you to install
and switch between multiple versions of Python_ easily. It even allows you to mark a directory to use a specific version of Python_ whenever
you run code in that directory.

PyEnv_ is not strictly required for this course but if you plan on doing any Python_ development beyond this course I strongly recommend it.

.. _standard_library:

Python Standard Library
-----------------------

When you install Python_ you get more than just the language. It comes with a bunch of useful Python_ code that
has already been written for you! This is called the Python_ standard library and it contains code that you can
use in your own programs that perform tasks that are common to many programs. For example, the 
`os <https://docs.python.org/3/library/os.html>`_ module contains functions for interacting with the operating 
system and the `math <https://docs.python.org/3/library/math.html>`_ module contains functions for performing 
common mathematical operations.

The stdlib_ is extensively documented.

..  youtube:: EI1qbU32e5w
   :width: 50%
   :align: center
   :url_parameters: ?start=667&end=815


.. _packages:

Python Package Index (PyPI_)
---------------------------

Beyond the standard library - Python_'s popularity is due in large part to the fact that it has a huge ecosystem of 
third party packages that are available for free. These packages are hosted on the Python Package Index (PyPI_) and
can be installed with the ``pip`` command. The PyPI_ is a repository of Python_ packages that is maintained by the 
Python Software Foundation. Anyone in the world can write python code and then upload it as a package to PyPI_!
This means that there are packages for just about anything you can imagine. Some packages are amazing but many 
are terrible and some are even malware, so you do need to be discerning about what you end up using.

..  youtube:: EI1qbU32e5w
   :width: 50%
   :align: center
   :url_parameters: ?start=815&end=985


.. _venv:

Python Virtual Environments
---------------------------

Dependency Hell is the problem introduced by relying on a large ecosystem of third party packages. Most Python_
programs rightly do not reinvent every wheel and instead rely on code written by other people. The problem this
introduces is that most Python_ packages are dependent on a complex web of interconnected dependencies. Your own
project's dependencies have dependencies and so on and so forth. Sometimes different packages have dependencies
on specific versions of other packages and sometimes those versions are incompatible.

Python_ virtual environments are a way to isolate the dependencies of a project from the dependencies of other
projects you might also be working on. They are essentially just a directory devoted to your specific project that
any packages downloaded from PyPi_ will end up in.


..  youtube:: EI1qbU32e5w
   :width: 50%
   :align: center
   :url_parameters: ?start=987&end=1718

|

The directory structure of a Python_ virtual environment looks like the following:

.. image:: ../../learn_python/module1/resources/PythonVirtualEnvironments.svg
   :alt: Computer Mental Model
   :width: 50%
   :align: center


.. _build_tools:

Build Tools (Poetry)
--------------------

There are many tools for managing Python package dependencies and building distributable wheel files. The next generation 
tools all use the `pyproject.toml <https://packaging.python.org/en/latest/guides/writing-pyproject-toml/>`_ standard file 
format for configuration and are therefore theoretically compatible with each other. However, in practice they often have 
differences that might make it difficult to switch between them.

In this course we will be using Poetry_.

..  youtube:: EI1qbU32e5w
   :width: 50%
   :align: center
   :url_parameters: ?start=1718&end=2023

|

Here are some other popular Python_ build tools:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Build Tool
     - Description
   * - Poetry_
     - A tool for dependency management and packaging in Python, using `pyproject.toml` for project configuration. Simplifies package management and dependency resolution.
   * - `Flit <https://flit.readthedocs.io/en/latest/>`_
     - A simple way to put Python packages and modules on PyPI, using `pyproject.toml` for packaging metadata. Ideal for smaller projects.
   * - `PDM <https://pdm.fming.dev/>`_
     - A modern Python package manager with PEP 582 support, using `pyproject.toml` to manage project metadata and dependencies. Provides an easy and intuitive way to manage Python projects.
   * - `Hatch <https://hatch.pypa.io/latest/>`_
     - A modern project, package, and virtual environment manager for Python that leverages `pyproject.toml`. Designed to be easy to use with a high level of configurability.
   * - `Build <https://pypa-build.readthedocs.io/en/latest/>`_
     - A simple, correct PEP 517 build frontend, using `pyproject.toml` to build source archives and wheels. Focused on being a lightweight building tool with minimal dependencies.



Testing (pytest_)
----------------

Testing is a critical part of software development. When you build large programs it will be hard to hold the entirety of the program in your head at any
given time. This means it is difficult to make changes to the program and be confident you did not break any execution paths. This is where automated testing
comes in. Automated testing is the practice of writing code that tests your code. This code is usually written in a separate file from the code it is testing
and not distributed with your library. Test suites are usually run automatically as part of a build process and can be run manually as well. If you have An
extensive test suite when you make changes to your software and all of your tests pass you can be reasonably confident that you can publish your software and
any other code that depends on your code can pull in your update and not break.

When you integrate third party packages as dependencies into your packages you should always check that they have a robust set of tests that are run before they
publish updates. The gateway assignments of this course come with a test suite built using a third party package called pytest_ thats designed to make writing
tests easy. Each time you finish a gateway assignment you will run the test suite!

..  youtube:: EI1qbU32e5w
   :width: 50%
   :align: center
   :url_parameters: ?start=2023&end=2140

|

There are many many packages and tools used to make testing Python code easier. Some additional tools are listed in the table below.

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Testing Tool
     - Description
   * - pytest_
     - A mature full-featured Python testing tool that helps you write better programs. It provides a rich set of features for various kinds of testing.
   * - `Unittest <https://docs.python.org/3/library/unittest.html>`_
     - The built-in testing framework for Python, inspired by JUnit. It supports test automation, sharing of setup and shutdown code, aggregation of tests, etc.
   * - `Nose2 <https://docs.nose2.io/en/latest/>`_
     - An extension of the Unittest test framework, Nose2 adds functionality such as plugins and easy test discovery.
   * - `Tox <https://tox.readthedocs.io/en/latest/>`_
     - A generic virtualenv management and test command-line tool that can be used to check that packages work with different Python versions.
   * - `Hypothesis <https://hypothesis.readthedocs.io/en/latest/>`_
     - A property-based testing tool that lets you write tests that are parameterized by a source of examples, and then checks those tests against a wide range of example inputs.
   * - `Behave <https://behave.readthedocs.io/en/stable/>`_
     - A BDD (Behavior Driven Development) tool for Python. It allows writing tests in a natural language style, backed up by Python code.


.. _editing:

Editing Code (VSCode)
---------------------

Integrated Development Environments or *IDEs* are text editors that have additional features that help
us write computer code. Think Microsoft Word, but for code! There are many IDEs available for Python and other
languages but for this course we are going to be using VSCode_ in all of our examples. You do not strictly have 
to use VSCode_ to take this course - any IDE you can download to your computer will work.

..  youtube:: EI1qbU32e5w
   :width: 50%
   :align: center
   :url_parameters: ?start=2140&end=2266

|

Some other popular IDEs for Python are:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - IDE
     - Description
   * - `PyCharm <https://www.jetbrains.com/pycharm/>`_
     - Advanced Python-specific features, smart code navigation, and integrated tools for professional development.
   * - `Visual Studio Code <https://code.visualstudio.com/>`_
     - Highly customizable, supports multiple languages, and offers extensive extension support.
   * - `Jupyter Notebook <https://jupyter.org/>`_
     - Interactive computing and data visualization in a web-based notebook format.
   * - `Spyder <https://www.spyder-ide.org/>`_
     - Tailored for data science, integrates with many scientific libraries and tools.
   * - `Thonny <https://thonny.org/>`_
     - Simple and beginner-friendly, with a focus on teaching Python.
   * - `Eclipse with PyDev <http://www.pydev.org/>`_
     - Combines the robustness of Eclipse with powerful Python support through the PyDev plugin.
   * - `Sublime Text <https://www.sublimetext.com/>`_
     - A sophisticated text editor known for its speed and minimalistic design.
   * - `Wing IDE <https://wingware.com/>`_
     - Designed for professional Python developers, with powerful debugging and unit testing features.
   * - `Emacs <https://www.gnu.org/software/emacs/>`_
     - A terminal based text editor. Has a rich feature set but with a high learning curve.


.. _generative_ai:

Generative AI
-------------

With Petabytes of code to learn from, computers have been getting better and better at writing code. Most IDEs now have extensions
that you can install that will look at your code as you write it and make very helpful auto-complete style suggestions. These tools
can write whole functions for you or suggest approaches. When integrated into your workflow appropriately these tools can be a massive
productivity boost. We are not going to shy away from these tools in this course and will even use one as a tutor to help you with your
gateway assignments.

When you are first starting out however I suggest not enabling any auto-complete generative AI in your IDE. At least wait until you have
completed the core modules. This will avoid the temptation to use the AI as a crutch and will force you to learn the semantics of the language.

..  youtube:: EI1qbU32e5w
   :width: 50%
   :align: center
   :url_parameters: ?start=2267&end=2435


.. _install:

Install Tools
=============

Four of the tools we covered need to be installed on your local laptop or desktop to run the course. Installing software
onto a computer is simply the process of putting files in the right place - and in some cases letting the operating system
know that the program exists. The files that make up a program consist of executable code, configuration files, documentation 
and media resources. Most operating systems have a standard way of organizing these files but there are usually multiple ways 
to install a program and other programs that will help you do so. If you run into errors installing any of the dependencies please 
refer directly to the tool documentation or ask me!

Mac OSX - Homebrew
------------------

For Mac users I recommend installing the `Homebrew package manager <https://brew.sh/>`_. Homebrew is a command line tool that 
makes installing software packages and updates for programs with lots of interconnected dependencies easy. It will allow us to
install more than one of the tools we need with a single command. Occasionally homebrew packages might conflict with software installed
by other mechanisms. If you'd rather not use Homebrew, refer to each tools documentation for alternative installation instructions.
To install Homebrew open a terminal and run:


.. code-block:: bash

   ?> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"


git
---

git_ can be installed directly using a dmg file from the `git website <https://git-scm.com/downloads>`_ or via homebrew:

.. code-block:: bash

   ?> xcode-select --install
   ?> brew install git

Verify that git is installed by running:

.. code-block:: bash

   ?> git --version

pyenv
-----

.. note::

   I strongly recommend pyenv_ but it is not necessary to take the course and if you do not think you will ever need more 
   than one version of Python on your system you may always install python directly from the 
   `python website <https://www.python.org/downloads/>`_ or via homebrew (brew install python). This also does not preclude
   installing pyenv_ later.

pyenv_ can be installed via homebrew. Afterwards we need to setup our shell to use pyenv_. The echo commands will add the
necessary lines of code to our shell configuration file which set up environment variables that pyenv_ depends on. The 
following commands work for Z shell which is the default shell on OSX.

.. code-block:: bash

   ?> brew install pyenv
   ?> echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
   ?> echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
   ?> echo 'eval "$(pyenv init -)"' >> ~/.zshrc

Verify that pyenv is installed by running:

.. code-block:: bash

   ?> pyenv --version

Install the most recent stable python version. You can list the python versions available to install with:

.. code-block:: bash

   ?> pyenv install --list

As you can see there are a lot. There are many different versions of Python packaged for different kinds of systems
and environments but we are interested in the mainline "vanilla" builds. These will be simply listed as "3.11.4" or "3.10.0".
Determine whatever the most recent stable sub-version is and install it with:

.. code-block:: bash

   ?> pyenv install 3.xx:latest
   ?> pyenv global 3.xx.xx

Verify that the expected version of python is installed by running:

.. code-block:: bash

   ?> python --version

Poetry
------

Poetry_ can be installed via its standalone installer script:

.. code-block:: bash

   ?> curl -sSL https://install.python-poetry.org | python3 -

Verify that poetry is installed by running:

.. code-block:: bash

   ?> poetry --version


VSCode
------

VSCode_ can be installed directly via its `packages <https://code.visualstudio.com/download>`_

VSCode_ requires plugins to add the functionality we need to develop Python code, the course requires the following extension:

* `Python extension <https://marketplace.visualstudio.com/items?itemName=ms-python.python>`_

And these are nice to have:

* `TOML <https://marketplace.visualstudio.com/items?itemName=be5invis.toml>`_
* `HTML & CSS Support <https://marketplace.visualstudio.com/items?itemName=ecmel.vscode-html-css>`_
* `Sphinx <https://marketplace.visualstudio.com/items?itemName=leonhard-s.python-sphinx-highlight>`_
* `RST Support <https://marketplace.visualstudio.com/items?itemName=trond-snekvik.simple-rst>`_
* `SVG Viewer <https://marketplace.visualstudio.com/items?itemName=vitaliymaz.vscode-svg-previewer>`_

There are many extensions available for VSCode_ and you may find others that you like. If you wish VSCode did
something for you that it doesn't, chances are other people have thought the same thing and written an extension for it.

.. gateway:

Fork & Clone the Course
=======================

The course repository is located `here <https://github.com/bckohan/learn-python>`_.

..  youtube:: EI1qbU32e5w
   :width: 50%
   :align: center
   :url_parameters: ?start=2437


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

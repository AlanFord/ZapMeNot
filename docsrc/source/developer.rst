Developer
=========

Most of the development work is done as part of a uv project.  However, uv
is not required.  Most of the uv commands discussed in the following sections
can be performed in various development environments using commands
specific to that environment.

Testing
-------

Test cases packaged with ZapMeNot fall into three categories; 
unit tests, graphics tests, and benchmarks.

Unit Tests
^^^^^^^^^^

These tests are verify that code blocks are functioning as 
intended.  To execute the unit tests, use the following code:

.. code-block :: console 

   cd ZapMeNot
   uv run pytest -m basic

Benchmark Tests
^^^^^^^^^^^^^^^

The benchmarks are not designed to identify errors in ZapMeNot, but
rather to examine the accuracy of the calculations.  The following
code block can be used to execute the benchmarks.  Note the use of the
"-s" option, which ensures that normal console output is retained by
the testing routines.

.. code-block :: console 

   cd ZapMeNot
   uv run pytest -s -m benchmark

Graphics Tests
^^^^^^^^^^^^^^

The graphics tests can be used to verify that the ZapMeNot display
functions are performing as expected.  Some of these test cases will
generate a display of a ZapMeNot geometry; these can be used to verify
that geometries are properly displayed.  Other test cases are used
to trap expected errors.

Note that the graphics tests cases as currently configured will fail
when run on a "headless" server, i.e. a server without graphics hardware.

.. code-block :: console 

   cd ZapMeNot
   uv run pytest -m graphics

Python Version Compatibility
--------

A shell script, run_tests.sh, will run the unit tests using Python
version 3.11 through 3.14.  Uncommenting a line in the file will also
run the graphics tests.  The file uses uv commands, but can be modified as needed.

.. code-block :: console

   cd ZapMeNot
   uv run ./run_tests.sh

Updating A Version
------------------

Following successful testing, the following steps are used to generate a new version of ZapMeNot:

* Update the version number in ZapMeNot/src/zapmenot/__about__.py
* Update the ZapMeNot/docsrc/source/getting-started.rst file with any new features or changes
* Update the ZapMeNot/README.rst file with any new features or changes
* Rebuild the documentation by executing :code:`uv run make html` from the ZapMeNot/docsrc folder
* Build the distribution packages by executing :code:`uv run hatch build` from the ZapMeNot folder

Updating Copyright
------------------

Update the year in the following files:

* `ZapMeNot/docsrc/source/license.rst`
* `ZapMeNot/src/zapmenot/__about__.py`

Update the year in the header of each python source file.
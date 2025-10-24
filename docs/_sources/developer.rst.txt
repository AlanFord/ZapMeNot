Developer
=========

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
   pytest -m basic

Benchmark Tests
^^^^^^^^^^^^^^^

The benchmarks are not designed to identify errors in ZapMeNot, but
rather to examine the accuracy of the calculations.  The following
code block can be used to execute the benchmarks.  Note the use of the
"-s" option, which ensures that normal console output is retained by
the testing routines.

.. code-block :: console 

   cd ZapMeNot
   pytest -s -m benchmark

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
   pytest -m graphics

Coverage
--------

.. code-block :: console

   cd ZapMeNot/coverage
   ./runCoverage.sh

Updating A Version
------------------

Following successful testing, the following steps are used to generate a new version of ZapMeNot:

* Update the version number in ZapMeNot/source/zapmenot/__about__.py
* Update the ZapMeNot/docsrc/source/getting-started.rst file with any new features or changes
* Update the ZapMeNot/README.rst file with any new features or changes
* Update the pyproject.toml file with the new version number
* Optionally update the interSphinx input by executing :code:`update.sh` from the ZapMeNot/docsrc/interSphinx folder
* Rebuild the documentation by executing :code:`make html` from the ZapMeNot/docsrc folder
* Build the distribution packages by executing :code:`hatch build` from the ZapMeNot folder

Updating Copyright
------------------

Update the year in the following files:

* `ZapMeNot/docsrc/source/license.rst`
* `ZapMeNot/src/zapmenot/__about__.py`

Update the year in the header of each python source file.
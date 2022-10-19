Developer
=========

Unit tests
----------

.. code-block :: console 

   cd ZapMeNot
   pytest -m basic

Benchmark tests
---------------

.. code-block :: console 

   cd ZapMeNot
   pytest -s -m benchmark

Graphics tests
--------------

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

Update the version number in the following files:

* `setup.py`
* `setup.cfg`
* `ZapMeNot/docs/source/conf.py`

Make manual and commit to `ZapMeNot/docs/zapmenot.pdf`.

Updating Copyright
------------------

Update the year in the following files:

* `docsrc/source/license.rst`
* `zap_me_not/__about__.py`


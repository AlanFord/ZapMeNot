Developer
=========

Unit tests
----------

:math:`\underline{x}=[  x_{1}, ...,  x_{n}]^{T}`

.. code-block :: console 

   cd ZapMeNot/test
   pytest -m basic

Benchmark tests
---------------

.. code-block :: console 

   cd ZapMeNot/test
   pytest -s -m benchmark

Graphics tests
--------------

.. code-block :: console 

   cd ZapMeNot/test
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

* `LICENCE.txt`
* `README.md`
* `docs/source/conf.py`
* `docs/source/licence.rst`


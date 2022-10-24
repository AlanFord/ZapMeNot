==================
Generating Results
==================

Two approaches are available for calculating dose rates once a ZapMeNot
model has been constructed.

The basic approach is demonstrated in the following code block.  It is
assumed that a model :code:`myModel` has already been constructed with an appropriate
source and detector.  The method :code:`calculate_exposure` returns the exposure in mR/hr.

.. code-block:: python

    # run an existing model
    result = myModel.calculate_exposure()

A more detailed exposure report can be generated with the :code:`generate_summary` method.
:code:`generate_summary` returns a "list of lists" (think of a group of lists).  The lists
include, in order of appearance, the photon energy groups, the photon appearance in each group
(photons/sec), the total energy flux by group (MeV/sec), total
uncollided exposure by energy group (mR/hr), and total exposure by energy group (mR/hr).  These lists
can be easily accessed in the following manner:

.. code-block:: python

    # generate a summary from an existing model
    (energy_groups, intensities, energy_flux, 
        uncollided_exposure, exposure) = myModel.generate_summary()

This provides access to the data for further processing.  Alternatively,
Python packages such as `Pandas`_ can provide powerful data analysis tools
that can be used with the results of the :code:`generate_summary` method.

.. _Pandas: https://pandas.pydata.org

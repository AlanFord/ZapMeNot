Read Me
==============================================================================



`ZapMeNot` is a Python library of functions for point-kernel photon shielding analyses.

Getting Started
---------------
`Quick Start Docs <https://alanford.github.io/ZapMeNot/quickstart.html>`__
`Full documentation <https://alanford.github.io/ZapMeNot/>`__

Version Changelog
-----------------

ZapMeNot is still in its alpha release

Requirements
------------

 - Python 3.4 or above
 - Numpy 1.18.1 or above
 - SciPy 0.14 or above
 - Pytest 5.3.5 or above
 - Pyyaml 5.3 or above
 - PyVista (optional for graphics)
 - vtk (optional for graphics)

Installation:
------------------------------------------------------------------------------

Installing from a local source tree:

:code:`pip install ./ZapMeNot`

You can also install in Development Mode:

:code:`pip install -e ./ZapMeNot`

You can also install from Github:

:code:`pip install git+git://github.com/AlanFord/ZapMeNot.git`

Installing in Anaconda is a bit more complicated. You must first manually install the prerequisites in conda::

    conda install pip
    conda install git
    conda install numpy
    conda install scipy
    conda install pytest
    conda install pyyaml
    pip install git+git://github.com/AlanFord/ZapMeNot.git

This may be simplified in the future as my knowledge of installation packages improves!

Testing:
------------------------------------------------------------------------------
Testing is designed around the use of pytest.  From the root directory of 
the package, the basic unit tests can be run as follows:

:code:`pytest -m basic`

Benchmark cases can be run using the following command.  Note that these
cases are designed to fail PyTest. Each benchmark prints the calculation
results and the difference (in percent) from the corresponding Microshield case.

:code:`pytest -s -m benchmark`

Valuable References
-------------------

    `ZapMeNot Documentation <https://alanford.github.io/ZapMeNot/>`__

    `Github Repo <https://github.com/alanford/zapmenot>`__

    `Download Python <https://www.python.org/downloads/>`__

License
-------

    The `GNU general public license <https://github.com/alanford/zapmenot/blob/master/LICENSE>`__

Quickstart
----------

.. code-block:: python

    from zap_me_not import model,source,shield,detector,material

    sample_sink = model.Model()

    # create the source
    a_source = source.PointSource(x=0, y=0, z=0)
    a_source.add_isotope_curies('Co-60',2.1)
    a_source.add_isotope_curies('Cs-137',0.3)
    sample_sink.add_source(a_source)

    # define the location where the dose will be calculated
    exposure_detector = detector.Detector(x=200, y=40, z=40)
    sample_sink.add_detector(exposure_detector)

    # define a shield and add it to the model
    first_shield = shield.SemiInfiniteXSlab('concrete', x_start=12, x_end=32.1)
    sample_sink.add_shield(first_shield)

    # define a second shield and add it to the model
    second_shield = shield.SemiInfiniteXSlab('iron', x_start=32.1, x_end=33.1)
    sample_sink.add_shield(second_shield)

    # declare which shield material will be used for buildup factor calculations
    buildup_factor_material = material.Material('iron')
    sample_sink.set_buildup_factor_material(buildup_factor_material)

    # (optionally) declare a meterial to fill all non-defined regions
    sample_sink.set_filler_material('air')

    # calculate exposure in mR/hr
    exposure = sample_sink.calculate_exposure()
    print('The exposure is ', exposure, ' mR/hr')


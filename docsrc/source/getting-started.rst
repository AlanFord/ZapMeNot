===============
Getting Started
===============

Introduction
------------


`ZapMeNot` is a Python library of functions used to perform photon (x-ray and gamma) 
shielding analyses using the point-kernel method.  For a quick refresher on the point-kernel method or for more details
about this implementation, see the :doc:`theory-and-methods` section.  For a more in-depth discussion of the point-kernel and other methods
of photon shielding, see `Radiation Shielding by J. K. Shultis and R. E. Faw`_.

.. _Radiation Shielding by J. K. Shultis and R. E. Faw: https://www.ans.org/store/item-350021/

Photon sources in ZapMeNot can be created by specifying a composition of radioisotopes or 
by including specific photon energies and intensities.  Photon energies may range from 15 keV to 15 MeV.  
Source geometries may be point sources, line sources, or a range of volumetric sources.  
The selection of isotopes that may be included in the source is vast,
covering all of the isotopes included in `ICRP Publication 107`_.

.. _ICRP Publication 107: https://www.icrp.org/publication.asp?id=ICRP%20Publication%20107

Installation
------------

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

Quickstart
----------
This is a "quick" introduction to ZapMeNot.  A more detailed description of
building an input file can be found in the :doc:`modeling` section.  A more in-depth
look at output options can be found in the :doc:`results` section.

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

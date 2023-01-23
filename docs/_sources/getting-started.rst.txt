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

There are as many ways to install ZapMeNot as there are ways to install and run Python.  First
up is installing ZapMeNot using pip.

ZapMeNot can be installed directly from Github using pip:

:code:`pip install git+git://github.com/AlanFord/ZapMeNot.git`

ZapMeNot can be installing from a local source tree using pip once the source has been retrieved from Github:

:code:`pip install ./ZapMeNot`

You can also install in Development Mode:

:code:`pip install -e ./ZapMeNot`

At present most ZapMeNot users are running ZapMeNot using either Anaconda or Miniconda.  Both use conda
to create specialized python environment tailored to the work at hand.  After installing either
Anaconda or Miniconda, create a ZapMeNot environment using the following command:

:code:`conda env create -f zapmenot.yml`

where the zapmenot.yml file contains the following:

.. code-block:: yaml

    name: zapmenot
    channels:
    - defaults
    - conda-forge
    dependencies:
    - python=3.9
    - scipy>=0.14
    - numpy>=1.18.1
    - pyyaml>=5.3
    - pip
    - git
    # optional for graphics capability
    - pyvista
    # optional for jupyterlab capability
    - jupyterlab
    - matplotlib
    - panel
    - pythreejs
    - pooch>=1.6.0
    - ipyvtklink
    # required for testing
    - pytest
    - pandas
    # required for developers
    - sphinx-rtd-theme
    - sphinx
    - flake8
    - build

Finally, install the ZapMeNot package from Github:

.. code-block:: bash

    conda activate zapmenot
    pip install git+git://github.com/AlanFord/ZapMeNot.git


Quickstart
----------
This is a "quick" introduction to ZapMeNot.  A more detailed description of
building an input file can be found in the :doc:`modeling` section.  A more in-depth
look at output options can be found in the :doc:`results` section.

.. code-block:: python

    from zapmenot import model,source,shield,detector,material

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

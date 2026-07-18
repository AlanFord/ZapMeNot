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
up is installing ZapMeNot using pip, followed by using Anaconda, and finally using uv.

Installing with Pip
^^^^^^^^^^^^^^^^^^^

You must start with a copy of Python.  ZapMeNot is compatible with Python releases 3.11, 3.12, 3.13, and 3.14.  
ZapMeNot can be installed directly from Github using pip:

:code:`pip install 'ZapMeNot @ git+https://github.com/AlanFord/ZapMeNot.git'`

To install the optional support for `Jupyterlab <https://jupyterlab.readthedocs.io/en/stable/index.html>`__, 
run the command:

:code:`pip install 'ZapMeNot[jupyterlab] @ git+https://github.com/AlanFord/ZapMeNot.git'`

Similarly, to install the optional support for testing the package, run the command:

:code:`pip install 'ZapMeNot[test] @ git+https://github.com/AlanFord/ZapMeNot.git'`

Additional information about running the unit tests can be found in the :doc:`developer` section 

ZapMeNot can be installing from a local source tree using pip once the source has been retrieved from Github:

:code:`pip install ./ZapMeNot`

You can also install in Development Mode:

:code:`pip install -e "./ZapMeNot[dev]"`

Working with Conda
^^^^^^^^^^^^^^^^^^^

At present many ZapMeNot users are running ZapMeNot using either Anaconda, Miniconda, or conda-forge.  All use conda
to create specialized python environment tailored to the work at hand.  

After installing either
Anaconda, Miniconda, or conda-forge, create an appropriate conda environment.  Activate that environment
and then install ZapMeNot using the pip instructions previously discussed.  This does not mesh perfectly
with the conda scheme, but it is workable.

A more complicated, but conda-esque approach is to create a conda environment for ZapMeNot without using pip, 
allowing conda to manage the coordination between ZapMeNot's dependencies and any other packages you may install via conda.
Use the following command:

:code:`conda env create -f zapmenot.yml`

where the zapmenot.yml file contains the following:

.. code-block:: yaml

    name: zapmenot
    channels:
    - conda-forge
    - defaults
    dependencies:
    - python>=3.11.14
    - scipy
    - pyyaml
    - pyvista>=0.45
    # optional for jupyterlab capability
    - jupyterlab>=4.5.9
    - trame>=3.10
    - trame-vtk>=2.8.17
    - trame-vuetify>=3.0
    - ipywidgets>=8.1.7
    # optional for testing
    - pytest>=9.0.3
    - pandas>=2.3
    # required for developers
    - hatch
    - hatchling>=1.27
    - sphinx-rtd-theme>=3.0
    - sphinx-autodoc-typehints>=3.6.1
    - typing-extensions>=4.15.0
    - sphinx>=8.2
    - flake8>=7.2
    - types-PyYAML
    - scipy-stubs
    # replace python-build with "build" if not using the conda-forge channel
    - python-build>=1.2

Next, install the ZapMeNot package from Github using pip:

.. code-block:: bash

    conda activate zapmenot
    pip install 'ZapMeNot @ git+https://github.com/AlanFord/ZapMeNot.git'


Installing with uv
^^^^^^^^^^^^^^^^^^^
uv is a very fast Python package manager (similar to pip) but also manages your Python virtual environment.

There are a number of ways to use uv, as documented at https://docs.astral.sh/uv/.  Let's assume
you are working on a project and have already installed uv.

First, the following command will create a project folder and initialize it with uv:

:code:`uv init my_project`


Next, from within the project folder include ZapMeNot in the project's dependencies:

:code:`uv add 'ZapMeNot @ git+https://github.com/AlanFord/ZapMeNot.git'`

This will install ZapMeNot and all of the supporting Python packages, allowing uv to manage the Python environment
and Python package versions.  The syntax of the command is similar to the pip command discussed earlier.  The uv 
commands for installing the optional support for Jupyterlab and unit testing are structured similarly - create the uv
command by starting with the pip command and replace "pip install" with "uv add".  Done!

You can now build out your ZapMeNot project.  

Once you have your ZapMeNot model written as a python file you can run it using the command from within
your project folder:

:code:`uv run myPythonFile.py`

uv is very powerful and can do much more; addition information on using uv can be found at https://docs.astral.sh/uv/.


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

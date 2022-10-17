====================
Modeling in ZapMeNot
====================

A model in ZapMeNot requires, at a minimum, a source and a detector (a.k.a. a dose point).
The source can be a simple point source, a line source, or a volumetric source (a box, cylinder, etc.).
A point source is defined by an XYZ location and a radioative source composition.  The source composition
can be specified in curies (Ci) of an isotope, becquerels (bq) of an isotope, or by photon energy and intensity.
A complex source can be a combination of all three specification types.
An example of specifying a point source is 

.. code-block:: python

    # create the source
    a_source = source.PointSource(x=0, y=0, z=0)
    a_source.add_isotope_curies('Co-60',2.1)
    
Here is the same point source with a more complicated set of isotopes, including a specific 0.98 MeV
photon with an intensity of 3.14E2 photons/sec:

.. code-block:: python

    # create the source
    a_source = source.PointSource(x=0, y=0, z=0)
    a_source.add_isotope_curies('Co-60',2.1)
    a_source.add_isotope_bq('Cs-137', 1E6)
    a_source.add_photon(0.98, 3.14E2)


A line source specification is similar.  A volumentric source specification is a little more complicated, requiring
physical dimensions, a body material, a material density, and the radioative source composition.
An example of a box source using a default material density is

.. code-block:: python

    # create the source
    a_source = source.BoxSource(box_center=[4, 5, 6],
                                box_dimensions=[10, 10, 10],
                                material_name='iron')
    a_source.add_isotope_curies('Co-60',2.1)


The detector is defined simply by specifying an XYZ location.

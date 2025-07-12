====================
Modeling in ZapMeNot
====================

A model in ZapMeNot requires, at a minimum, a source and a detector (a.k.a. a dose point).
The source can be a simple point source, a line source, or a volumetric source.  Volumetric sources include:

 - BoxSource
 - SphereSource
 - XAlignedCylinderSource
 - YAlignedCylinderSource
 - ZAlignedCylinderSource

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

    # create a point source
    a_source = source.PointSource(x=0, y=0, z=0)
    a_source.add_isotope_curies('Co-60',2.1)
    a_source.add_isotope_bq('Cs-137', 1E6)
    a_source.add_photon(0.98, 3.14E2)


A line source specification is similar.  A volumentric source specification is a little more complicated, requiring
physical dimensions, a body material, a material density, and the radioative source composition.
An example of a box source using a default material density is

.. code-block:: python

    # create a box source
    a_source = source.BoxSource(box_center=[4, 5, 6],
                                box_dimensions=[10, 10, 10],
                                material_name='iron')
    a_source.add_isotope_curies('Co-60',2.1)


The detector is defined simply by specifying an XYZ location.

.. code-block:: python

    # create a detector
    a_detector = detector.Detector(10, 2, 30)

The final step in creating the most basic of models is to, well, create a "model" and add the source
and detector:

.. code-block:: python

    # create a model, adding a source and detector
    myModel = model.Model()
    myModel.add_source(a_source)
    myModel.add_detector(a_detector)
    
One or more radiation shields can be optionally added to the model.  A shield is by definition a three-dimensional
body.  Standard shield types include:

 - Box
 - SemiInfiniteXSlab
 - Sphere
 - CappedCylinder
 - XAlignedCylinder
 - YAlignedCylinder
 - ZAlignedCylinder
 - InfiniteAnnulus
 - XAlignedInfiniteAnnulus
 - YAlignedInfiniteAnnulus
 - ZAlignedInfiniteAnnulus

The CappedCylinder and the InfiniteAnnulus are the moste general, can be oriented in any direction,
and require the most input to create.  The Box is a rectangular parallelpiped having sides aligned with 
the coordinate system axes.  The SemiInfiniteX Slab is, well, a slab of material with a finite thickness
in the X direction, infinite in the other directions.  It can be positiond at any X location.
The Sphere can be freely positioned but has its major axis aligned with the Z direction.  This has some impact
on the quadrature used (more on that later).
For user convenience the "aligned" cylinders and annuli have been included to simplify the input
required to build a model.

There is one more specialized shield - the Shell.  This shield can only be used to surround either a SphereSource 
spherical source or a Sphere shield.  When creating a Shell you will need to specify the object (SphereSource or Sphere) 
it is surrounding as well as the thickness of the Shell.

.. code-block:: python

    # create a model, adding a source and a shell
    myModel = model.Model()
    a_source = source.SphereSource('air', sphere_center=[0,0,10], sphere_radius=40)
    a_shield = shield.Shell('copper', a_source, thickness=10)
    myModel.add_source(a_source)
    myModel.add_shield(a_shield)

Each shield requires a material type and, optionally, a density.  Shields will alter
the calculated doses only when the shields completely or partially interrupt the line-of-sight between the source and
the detector.  The following
code block demonstrates creating two shields and adding them to a model:

.. code-block:: python

    # create a model, adding a source and detector
    myModel = model.Model()
    myModel.add_source(a_source)
    myModel.add_detector(a_detector)
    # add two shields
    shield_1 = shield.SemiInfiniteXSlab("iron", 10, 20)
    shield_2 = shield.Box("concrete", box_center=[31, 0, 0],
                          box_dimensions=[10, 10, 10])
    myModel.add_shield(shield_1)
    myModel.add_shield(shield_2)

Any model with radiation shields (or a volumetric source other than a void) should also specify a buildup factor
material.  This is usually the material that comprises the thickest shield in the model.  When a model has more than
one shield, chose the shield closest to the detector that is thick enough to affect the results.  In cases where the
source is much larger than the shield, the self-shielding of the source material may cause the source material to be the
controlling shield.  

Once the buildup factor material has been identified, add it to the model in the following manner:

.. code-block:: python

    # create a model
    myModel = model.Model()
    myModel.add_source(a_source)
    myModel.add_detector(a_detector)
    myModel.add_shield(shield_1)
    # define the buildup factor material
    myModel.set_buildup_factor_material(material.Material('iron'))

There are two optional features that can make building a model easier.  First, in some cases there may be a significant
amount of air between the source, the shield, and the detector.  The model can be instructed to "fill in the gaps" with air
using the following command:

.. code-block:: python

    # fill in the model with air
    myModel.set_filler_material(material.Material('air'))
    
An astute reader will note that the filler material is not restricted to only air.  If one is modeling a source and detector
immersed in water, the filler material could be specified as 'water'.  There may be unusual cases where one of the solid
materials might be used as the filler material.

The other optional feature is associated with the source definition.  Some common radionuclides found in sources may
emit few or no photons, but significant photons may be emitted by their decay products (a.k.a. their "progeny").  In those
instances where the parent isotope and the progeny may be in secular equilibrium, an option has been included such that
specifying the parent isotope is sufficient to also include the progeny.  Common isotopes where this is useful include
Ba-140, Cs-137, Cd-144, Ru-103, Ru-106, Sr-90, and Sn-113.  The following example shows how to include the progeny:

.. code-block:: python

    # create a point source
    a_source = source.PointSource(x=0, y=0, z=0)
    a_source.add_isotope_curies('Cs-137',2.1)
    a_source.include_key_progeny = True
    
Invoking the "include_key_progeny" method for isotopes other than those listed above will have no effect on the source.



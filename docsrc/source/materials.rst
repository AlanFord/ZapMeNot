Material Library
================

.. index:: single: Material Library


A number of materials are available for use as shielding,
source material, and for buildup factors.  Physical data
for each material is stored in `materialLibrary.yml`.  

Photon cross sections in the form of mass attenuation
coefficients are available for elements with
atomic numbers from 1 (Hydrogen) to 100 (Fermium).  Selected additional
sheilding materials are also provided, including:

 - Aluminum, 2.7 g/cm\ :sup:`3`
 - Iron, 7.874 g/cm\ :sup:`3`
 - Lead, 11.35 g/cm\ :sup:`3`
 - Air, 0.001205 g/cm\ :sup:`3`
 - Concrete, 2.3 g/cm\ :sup:`3`
 - Water, 1.0 g/cm\ :sup:`3`
 - SS304L, 8.0 g/cm\ :sup:`3`
 - UO2, 10.412 g/cm\ :sup:`3` (95% of theoretical density)
 - Resin, 2.01 g/cm\ :sup:`3` (modeled as a mixture of water (6.47 wt%) in concrete (93.53 wt%))

Buildup factors are included in the library for the following
materials.  Additional buildup factors may be added to the library,
while using an existing buildup factor with an atomic
number close to that of the shield is usually sufficient.

.. table:: Materials That include Buildup Factors
   :widths: auto

   +---------------+---------------+
   | Atomic Number |   Material    |
   +===============+===============+
   | 4             |   Beryllium   |
   +---------------+---------------+
   | 5             |   Boron       |
   +---------------+---------------+
   | 6             |   Carbon      |
   +---------------+---------------+
   | 7             |   Nitrogen    |
   +---------------+---------------+
   | 8             |   Oxygen      |
   +---------------+---------------+
   | 11            |   Sodium      |
   +---------------+---------------+
   | 12            |   Magnesium   |
   +---------------+---------------+
   | 13            |   Aluminum    |
   +---------------+---------------+
   | 14            |   Silicon     |
   +---------------+---------------+
   | 15            |   Phosphorus  |
   +---------------+---------------+
   | 16            |   Sulfur      |
   +---------------+---------------+
   | 18            |   Argon       |
   +---------------+---------------+
   | 19            |   Potassium   |
   +---------------+---------------+
   | 20            |   Calcium     |
   +---------------+---------------+
   | 28            |   Iron        |
   +---------------+---------------+
   | 29            |   Copper      |
   +---------------+---------------+
   | 42            |   Molybdenum  |
   +---------------+---------------+
   | 50            |   Tin         |
   +---------------+---------------+
   | 57            |   Lanthanum   |
   +---------------+---------------+
   | 64            |   Gadolinium  |
   +---------------+---------------+
   | 74            |   Tungsten    |
   +---------------+---------------+
   | 82            |   Lead        |
   +---------------+---------------+
   | 92            |   Uranium     |
   +---------------+---------------+
   | N/A           |   Water       |
   +---------------+---------------+
   | N/A           |   Air         |
   +---------------+---------------+
   | N/A           |   Concrete    |
   +---------------+---------------+


The user may add additional materials to the library by
appending data to the file `materialLibrary.yml`.  The data
fields are labeled and the file format is `YAML Version 1.1`_.

.. _YAML Version 1.1: https://pyyaml.org
 
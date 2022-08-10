Isotope Library
===============

.. index:: single: Isotope Library


Photon emmisision data for a large number of radioisotopes are
available for use in building sources.  The isotope library is
based on ICRP Publication 107, "Nuclear Decay Data for Dosimetric Calculations."
Photons with energies below 15 keV are excluded.

Note that some isotopes emit no x-rays or photons, e.g. Sr-90 and Cs-137.
In those cases the progeny may emit significant x-rays or photons.
Other isotopes have progeny with relatively short half-lives and the
progeny and the user may wish to assume the progeny to be in equilibrium with the parent. 
In both of these cases the progeny may already be included in the source.
If not, an option is available to include the progeny of these isotopes
in equilibrium with the parents.  This applies to the isotopes
Ba-140, Cs-137, Cd-144, Ru-103, Ru-106, Sr-90, and Sn-113.

The following table
lists the isotopes included in the library file
`isotopeLibrary.yml`:

.. csv-table:: ZapMeNot Isotopes
   :file: isotopes.csv
   :widths: 12, 60
   :header-rows: 1
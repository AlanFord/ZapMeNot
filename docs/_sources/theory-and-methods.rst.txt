==================
Theory and Methods
==================

Point-Kernel Method
--------------------

ZapMeNot calculates the uncollided photon flux using the point-kernel equation:

:math:`\phi(r) = \frac{S}{4\pi r^{2}}e^{-\mu r}`

where

:math:`\phi(r)` = space dependent uncollided photon flux

:math:`S` = point isotropic source of mono-energetic photons

:math:`r` = distance from source location to flux location

:math:`\mu` = total attenuation coefficient for medium

When multiple materials exist in the model, sum :math:`\mu_{i} r_{i}` over all of
the material regions between the source and the flux location.

Uncollided Photon Exposure Rate
-------------------------------

The exposure rate from uncollided photons can be calculated as:

:math:`D_{u}(r) = \phi(r) \Re`

and

:math:`\Re = 1.835\cdot 10^{-8} E\left ( \frac{\mu _{en}\left ( E \right )}{\rho } \right )_{air}`

where :math:`\Re` has units of R cm\ :sup:`2`, 

:math:`E` is the photon energy in MeV, and 

:math:`\mu _{en}/\rho` is the mass energy deposition coefficient of air in cm\ :sup:`2`/g.

Buildup Factor
--------------

The buildup factor :math:`B(r)` is defined as the ratio of the dose from all photons (collided and uncollided) to
the dose from uncollided photons.  The buildup factor will vary with distance from the source location and the material
traversed.  As such the total exposure from all photons can be calculated as:

:math:`D_{T}(r) = D_{u}(r) B(\mu r)`

where

:math:`D_{T}(r)` = the space dependent dose from collided and uncollided photons

:math:`B(\mu r)` = the space dependent buildup factor

Buildup factors are generally derived from experimental data and are approximated by mathematical functions.  The 
form of approximation used in ZapMeNot is the *geometric progression* (GP) form.  The GP coefficients for calculating
the buildup factor as provided in ANSI/ANS-6.4.3-1991 "Gamma-Ray Attenuation coefficients
and Buildup Factors for Engineering Materials."

Quadrature
----------

The point kernel method can be applied directly for point sources.  However, distributed
sources required an additional level of modeling.  The point kernel method is extended
to distributed sources using the method of numerical quadrature.  Put simply, the 
source volume or area is subdivided into a spatial quadrature and the source within 
a spatial mesh is represented as a point source.  Summing the dose responses 
resulting from the point sources returns the dose response resulting 
from the distributed source. The spatial mesh is not required to be uniform.  The quadrature
weights are normally computed as follows:

:math:`W_{k}=\frac{V_{k}}{\sum_{k=1}^{N}V_{k}}`


where

:math:`W_{k}` = the source mesh weight

:math:`V_{k}` = the volume or area of the k\ :sup:`th` mesh


Multiple Photon Energies
------------------------

A typical photon source will emit photons with a number of discrete photon energies,
each with a unique intensity.  These photon sources are modeled by performing a numerical quadrature
analysis for each photon energy with an associated energy-dependent buildup factor.  Photon energies
are limited to a range of 15 keV to 15 MeV to ensure applicability of the attenuation coefficients
and buildup factors presented in ANSI/ANS-6.4.3-1991 "Gamma-Ray Attenuation coefficients
and Buildup Factors for Engineering Materials."

Frequently the number of discrete photon energies can be in the 100's.  However, many of these photons energies
are low enough that the photon contribution to dose is small.  Many of the photon energies may also have a very low 
intensity due to a small decay branching fraction.  The evaluation is therefore simplified by limiting the number
of discrete photon energies to 40.  A 40 photon energy-group structure is used in the event that a source has more than 
40 discrete photon energies.  The energy-group structure is linearly distributed between the highest and lowest photon energies
in the source.  The photon intensity of each energy group is determined such that the energy flux
of photons within the group is preserved.


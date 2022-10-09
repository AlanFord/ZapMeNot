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

:math:`D = \phi \Re`

and

:math:`\Re = 1.835\cdot 10^{-8} E\left ( \frac{\mu _{en}\left ( E \right )}{\rho } \right )_{air}`

where :math:`\Re` has units of R cm\ :sup:`2`, 

:math:`E` is the photon energy in MeV, and 

:math:`\mu _{en}/\rho` is the mass energy deposition coefficient of air in cm\ :sup:`2`/g.

Buildup Factor
--------------

As it says.

Quadrature
----------

As it says.

Multiple Photon Energies
------------------------

As it says.


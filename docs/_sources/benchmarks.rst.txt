============
Benchmarking
============

ANSI/ANS 6.6.1 Benchmark I.1
----------------------------

This benchmark is described in ANSI/ANS 6.6.1-1979, "American National Standard 
for Calculation and Measurement of Direct and Scattered Gamma Radiation from LWR 
Nuclear Power Plants".

The benchmark models a 1 photon/sec point source of 6.2 MeV photons immersed in an air 
environment.  Doses are calculated at locations 57 feet below the point source and at
horizontal distances ranging from 200 ft to 5,000 ft.  
Air is modeled with a density of 0.00122 g/cm\ :sup:`3`.
Results are provided in the following table.

.. table:: ANSI/ANS 6.6.1-1979 Benchmark I.1 Results
   :widths: auto

   +--------------+---------------+---------------+-----------+-------------+
   | - Distance   | - ANS 6.6.1   | - Microshield | - ZapMeNot| - MCNP5     |
   | - (feet)     | - (mR/hr)     | - (mR/hr)     | - (mR/hr) | - (mR/hr)   |
   +==============+===============+===============+===========+=============+
   | 200          | - 1.04E-11 to | 1.194E-11     | 1.20E-11  | - 1.2067E-11|
   |              | - 1.56E-11    |               |           | - +/- 0.02% |
   +--------------+---------------+---------------+-----------+-------------+
   | 1,000        | - 2.6E-13 to  | 3.332E-13     | 3.30E-13  | - 3.3980E-13|
   |              | - 3.91E-13    |               |           | - +/- 0.06% |
   +--------------+---------------+---------------+-----------+-------------+
   | 3,000        | - 5.86E-15 to | 9.096E-15     | 9.15E-15  | - 9.4131E-15|
   |              | - 9.77E-15    |               |           | - +/- 0.2%  |
   +--------------+---------------+---------------+-----------+-------------+
   | 5,000        | - 4.56E-16 to | 6.997E-16     | 7.00E-16  | - 7.2265E-16|
   |              | - 7.55E-16    |               |           | - +/- 0.44% |
   +--------------+---------------+---------------+-----------+-------------+


ANSI/ANS 6.6.1 Benchmark II.1
-----------------------------

This benchmark is also described in ANSI/ANS 6.6.1-1979.  The source is a 
cylinder of water containing a uniformly distributed source of 0.8 MeV
photons with a source strength of 30 MeV/sec/cm\ :sup:`3`.  The cylinder
is 12 feet in diameter and 35 feed high.  Water density is 1 g/cm\ :sup:`3`
and the air density is 0.00122 g/cm\ :sup:`3`.  Dose rates are
determined at points with a height of 3 feet above the bottom of 
the cylinder and and radial distances from the cylinder centerline
ranging from 20 feet to 500 feet.  Results are provided in the following table.


.. table:: ANSI/ANS 6.6.1-1979 Benchmark II.1 Results
   :widths: auto

   +--------------+---------------+---------------+-----------+-------------+
   | - Distance   | - ANS 6.6.1   | - Microshield | - ZapMeNot| - MCNP5     |
   | - (feet)     | - (mR/hr)     | - (mR/hr)     | - (mR/hr) | - (mR/hr)   |
   +==============+===============+===============+===========+=============+
   | 20           | - 7.81E-02 to | 9.213E-02     | 9.13E-02  | - 7.9002E-02|
   |              | - 1.56E-01    |               |           | - +/- 0.2%  |
   +--------------+---------------+---------------+-----------+-------------+
   | 50           | - 1.56E-02 to | 2.051E-02     | 2.06E-02  | - 1.8210E-02|
   |              | - 2.86E-02    |               |           | - +/- 1.15% |
   +--------------+---------------+---------------+-----------+-------------+
   | 200          | - 9.77E-04 to | 1.178E-03     | 1.19E-03  | - 1.1819E-03|
   |              | - 1.95E-03    |               |           | - +/- 1.92% |
   +--------------+---------------+---------------+-----------+-------------+
   | 500          | - 7.03E-05 to | 1.259E-04     | 1.26E-04  | - 1.3537E-04|
   |              | - 1.56E-04    |               |           | - +/- 2.73% |
   +--------------+---------------+---------------+-----------+-------------+


ESIS Benchmark Problem 1
------------------------

The ESIS benchmarks were originally documented in
“Specification for gamma ray
shielding benchmark applicable to a nuclear 
radwaste facility.” Newsletter #37, 
European Shielding Information Service.
The benchmarks have been use in evaluations of both Microshield and VISIPLAN.

Problem 1 is a cylindrical water-filled steel tank 
surrounded by a concrete wall.  It will be modeled in ZapMeNot
as a cylindrical water source, an annular steel shield, and
an slab concrete shield.  The material densities are
0.00122 g/cm3, 1.0 g/cm3, 7.8 g/cm3, and 2.4 g/cm3 for air, 
water, steel, and concrete, respectively.

The source cylinder is 108.3 cm tall with a diameter of 308 cm.
The steel shield has a radial thickness of 2.54 cm.  The concrete
slab shield is 220 from the centerline of the source cylinder
and has a thickness of 91 cm. The dose rates are calculated on
the inside of the concrete wall at a height of 50.15 cm and
on the outside of the concrete wall at a height of 54.15 cm.

The source is defined in the following table.

.. table:: ESIS Source Strength
   :widths: auto

   +----------+--------------------+
   |  - Energy| - Source           |
   |  - (MeV) | - (photons/sec/cm3)|
   +==========+====================+
   | 0.4      | 4.0E+6             |
   +----------+--------+-----------+
   | 0.8      | 7.0E+6             |
   +----------+--------+-----------+
   | 1.3      | 2.8E+6             |
   +----------+--------+-----------+
   | 1.7      | 8.2E+6             |
   +----------+--------+-----------+
   | 2.2      | 4.0E+4             |
   +----------+--------+-----------+
   | 2.5      | 3.0E+4             |
   +----------+--------+-----------+
   | 3.5      | 1.2E+1             |
   +----------+--------+-----------+

Results are provided in the following table.

.. table:: ESIS Benchmark Problem 1 Results
   :widths: auto

   +--------------+----------------+---------------+-----------+
   | - Radial     | - ESIS Results | - Microshield | - ZapMeNot|
   | - Location   | - (mR/hr)      | - (mR/hr)     | - (mR/hr) |
   +==============+================+===============+===========+
   | Inside Wall  | - 4.54E+04 to  | 6.29E+04      | 6.22E+04  |
   |              | - 8.01E+04     |               |           |
   +--------------+----------------+---------------+-----------+
   | Outside Wall | - 4.9E-01 to   | 1.89E+00      | 1.88E+00  |
   |              | - 2.46E+00     |               |           |
   +--------------+----------------+---------------+-----------+

ESIS Benchmark Problem 2
------------------------

Problem 2 is similar to EIS Benchmark Problem 1.
However, the source is a square tank 273 cm wide by 479.9 cm high.
The tank wall remains at 2.54 cm thick and is surrounded by a concrete wall.
The inside surface of the wall is 228.6 cm from the tank centerline.
The thickness of the wall is 91.4.
It will be modeled in ZapMeNot
as a box water source, a slab steel shield, and
an slab concrete shield.  The material densities continue to be
0.00122 g/cm3, 1.0 g/cm3, 7.8 g/cm3, and 2.4 g/cm3 for air, 
water, steel, and concrete, respectively.

The dose rates are calculated on
the inside and outside of the concrete wall at a height of 240.0 cm.
Results are provided in the following table.

.. table:: ESIS Benchmark Problem 2 Results
   :widths: auto

   +--------------+----------------+---------------+-----------+
   | - Radial     | - ESIS Results | - Microshield | - ZapMeNot|
   | - Location   | - (mR/hr)      | - (mR/hr)     | - (mR/hr) |
   +==============+================+===============+===========+
   | Inside Wall  | - 4.54E+04 to  | 6.29E+04      | 6.22E+04  |
   |              | - 8.01E+04     |               |           |
   +--------------+----------------+---------------+-----------+
   | Outside Wall | - 4.9E-01 to   | 1.89E+00      | 1.88E+00  |
   |              | - 2.46E+00     |               |           |
   +--------------+----------------+---------------+-----------+

Synthetic Benchmark Problem
---------------------------

This is an analytic benchmark designed to evaluate a number of features:

- the use of multiple shields
- older vs modern cross sections
- photon energy group structure

This benchmark includes a point source composed of the following
radioactive materials in the following table.  Additionally, Ba-137m
is assumed to be in secular equilibrium with Cs-137.

.. table:: Synthetic Benchmark Point Source Composition
   :widths: auto

   +---------+------------------+
   | Isotope | uCi              |
   +=========+==================+
   | Co-58   | 22.5             |
   +---------+------------------+
   | Co-60   | 32.4             |
   +---------+------------------+
   | Cs-137  | 150              |
   +---------+------------------+
   | Mn-54   | 12.5             |
   +---------+------------------+
   | Sb-125  | 11.3             |
   +---------+------------------+

The point source is centered in an annular iron shield with an inner
radius of 3 feet and a thickness of 3 inches.  A concentric annular 
concrete shield has an inner radius of 4 feet and a thickness of
18 inches.  The material densities are
0.00122 g/cm3, 7.874 g/cm3, and 2.34 g/cm3 for air, 
steel, and concrete, respectively. 

The following tables contain the resulting dose rates calculated
using ZapMeNot, Microshield7, and MCNP5.  Note that the Microshield
results were generated using the "linear" energy group option.  The default
energy group option resulted in an additional 10% to 15% bias.

The first table contains dose rates determined at the outer surface
of the concrete shield at varying axial distances above the
point source.

The second table contains dose rates determined at the outer surface
of the iron shield at varying axial distances above the point source.

.. table:: Concrete Shield Results
   :widths: auto

   +--------+-----------+------------+-----------+
   | - Z    | - MCNP    | - ZapMeNot | - MS7     |
   | - (cm) | - (mR/hr) | - (mR/hr)  | - (mR/hr) |
   +========+===========+============+===========+
   | 0      | 1.87E-05  | 2.64E-05   | 2.64E-05  |
   +--------+-----------+------------+-----------+
   | 6      | 1.84E-05  | 2.62E-05   | 2.62E-05  |
   +--------+-----------+------------+-----------+
   | 20     | 1.73E-05  | 2.45E-05   | 2.45E-05  |
   +--------+-----------+------------+-----------+
   | 40     | 1.42E-05  | 1.97E-05   | 1.97E-05  |
   +--------+-----------+------------+-----------+
   | 60     | 1.01E-05  | 1.39E-05   | 1.39E-05  |
   +--------+-----------+------------+-----------+
   | 80.7   | 6.24E-06  | 8.54E-06   | 8.53E-06  |
   +--------+-----------+------------+-----------+


.. table:: Iron Shield Results
   :widths: auto

   +--------+-----------+------------+-----------+
   | - Z    | - MCNP    | - ZapMeNot | - MS7     |
   | - (cm) | - (mR/hr) | - (mR/hr)  | - (mR/hr) |
   +========+===========+============+===========+
   | 0      | 1.08E-02  | 1.30E-02   | 1.30E-02  |
   +--------+-----------+------------+-----------+
   | 6      | 1.07E-02  | 1.29E-02   | 1.29E-02  |
   +--------+-----------+------------+-----------+
   | 20     | 9.89E-03  | 1.18E-02   | 1.18E-02  |
   +--------+-----------+------------+-----------+
   | 40     | 7.61E-03  | 9.01E-03   | 9.05E-03  |
   +--------+-----------+------------+-----------+
   | 60     | 5.14E-03  | 5.98E-03   | 6.01E-03  |
   +--------+-----------+------------+-----------+
   | 80.7   | 3.11E-03  | 3.52E-03   | 3.54E-03  |
   +--------+-----------+------------+-----------+


import math

import pytest

from ZapMeNot import model,source,shield,detector,material

pytestmark = pytest.mark.benchmark

#===================================================
# Summary:
# Benchmark 0: ANSI/ANS-6.6.1 Reference Problem I.1
# Benchmark 1: ANSI/ANS-6.6.1 Reference Problem II.1 Case 1
# Benchmark 2: ESIS Problem #1 - Dose Point D2 -Buildup with Steel
# Benchmark 3: ESIS Problem #1 - Dose Point D3 - Buildup with Concrete
# Benchmark 4: ESIS Problem #2 - Dose Point D5 - Steel Buildup
# Benchmark 5: ESIS Problem #2 - Dose Point D6 - Concrete Buildup
# Benchmark 6: User manual case for resin liner source inference
# Benchmark 7: User manual case for resin liner source inference, iron shield

# Benchmark 0 is based on ANSI/ANS-6.6.1 Reference Problem I.1
# The source is located at the origin.
# The x-location of the dose point is variable between 200 and 5000 feet.
# The y-location of the dose point i 57 feet.
# There is no shielding other than air between the source and dose point.
# The air density is 0.00122 g/cm3.
# The source energy is 6.2 MeV.
# The source strength is 1 photon/sec.
# The builup material is air.
# Acceptable Results:
# Distance   	Dose Rate            Microshield 
# (feet)		(Rads/year)          (mrad/hr)
# 200			8.0E-11 to 1.2E-10   1.042E-11
# 1,000			2.0E-12 to 3.0E-12   2.909E-13
# 3,000			4.5E-14 to 7.5E-14   7.941E-15
# 5,000			3.5E-15 to 5.8E-15   6.091E-16
def test_benchmark_0():
	my_model = model.Model()
	my_source = source.PointSource(0,0,0)
	my_source.add_photon(6.2,1)
	my_model.add_source(my_source)
	# in the absence of a fill material option, a sphere shielf of air is used with 
	#   a radius large enough to emcompass the range of detector locations
	my_model.add_shield(shield.Sphere(material_name="air", sphere_radius=6000*12*2.54, \
		              sphere_center=[0,0,0],density=0.00122))
	my_model.set_buildup_factor_material(material.Material('air'))
	print("")
	print('test_benchmark_0')
	for distance in [200, 1000, 3000, 5000]:
		my_model.add_detector(detector.Detector(distance*12*2.54,57*12*2.54,0))
		result = my_model.calculate_exposure()
		# convert from R/sec to mR/hr
		print("At", distance, "ft, dose = ", result*0.877*8766*1e-3, "Rad/yr")

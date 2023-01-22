import math

import pytest

from zapmenot import model,source,shield,detector,material

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

# Benchmark 1 is based on ANSI/ANS-6.6.1 Reference Problem II.1
# The source is a water-filled tank 35 feet high and 12 feet in diameter.
# Uniformly distributed in the water is a source of 0.8 MeV photons.  The
# volumetric source strength is 30 MeV/sec/cm3, or 37.5 photons/sec/cm3.  There is
# no takn wall to be modeled.
# The  detector locations are 20, 50, 200, and 500 feet from the bottom centerline of
# the tank, offset up by 3 feet.
# The water density is 1 g/cm3 and the air density is 0.00122 g/cm3.  The buildup
# reference material is air.
# Acceptable Results:
# Distance   	Dose Rate         Microshield
# (feet)		(Rads/year)       (mR/hr)
# 20			6.0E-1 to 1.2E0   9.213E-02
# 50			1.2E-1 to 2.2E-1  2.051e-02
# 200			7.5E-3 to 1.5E-2  1.178e-03
# 500			5.4E-4 to 1.2E-3  1.259e-04

def test_benchmark_1():
	my_model = model.Model()
	my_source = source.ZAlignedCylinderSource(material_name="water", cylinder_radius=6*12*2.54, \
		       cylinder_center=[0,0,35/2*12*2.54], cylinder_length=35*12*2.54)
	my_source.add_photon(0.8,4.2034E9)
	my_source.points_per_dimension = [16,16,16]
	my_model.add_source(my_source)
	my_model.set_filler_material('air',density=0.00122)
	my_model.set_buildup_factor_material(material.Material('air'))
	print("")
	print('test_benchmark_1')
	results = []
	for case in [[20,9.213E-02], [50,2.051e-02], [200,1.178e-03], [500,1.259e-04]]:
		distance = case[0]
		expected_dose_rate = case[1]
		my_model.add_detector(detector.Detector(distance*12*2.54, 0, 3*12*2.54))
		result = my_model.calculate_exposure()
		diff = (result - expected_dose_rate)/expected_dose_rate * 100
		results.append([result,expected_dose_rate])
		print("At ", distance, " ft, dose = ", result, " mR/hr, ", diff, "%")
	assert True


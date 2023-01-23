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
# Benchmark 6: solidified resin container with concrete shield
# Benchmark 7: solidified resin container with concrete and steel shields

# Benchmark 2 is based on ESIS benchmark shielding problem #1.
# The source is a water-filled tank 108.3 cm high and 308 cm in diameter.
# The tank wall is steel with a thickness of 2.54 cm.
# Uniformly distributed in the water is the following source:
#   Energy         Source
#   (MeV)          (photons/sec/cm3)
#   0.4            4.0E+6
#   0.8            7.0E+6
#   1.3            2.8E+6
#   1.7            8.2E+6
#   2.2            4.0E+4
#   2.5            3.0E+4
#   3.5            1.2E+1
# The  detector location is 220 cm from the tank centerline
# at the bottom of the tank.
# The water density is 1 g/cm3 and the air density is 0.00122 g/cm3.
# The the steel density is 7.8 g/cm3.  The buildup material is
# steel.
# Benchmark acceptable results are 4.54E+1 to 8.01E+1 R/hr.
# Microshield result is 6.294e+04 mR/hr  
def test_benchmark_2():
	myModel = model.Model()
	mySource = source.ZAlignedCylinderSource(material_name="water", cylinder_radius=154, \
		       cylinder_center=[0,0,54.15], cylinder_length=108.3)
	mySource.add_photon(0.4,3.2276e+013)
	mySource.add_photon(0.8,5.6483e+013)
	mySource.add_photon(1.3,2.2593e+013)
	mySource.add_photon(1.7,6.6166e+013)
	mySource.add_photon(2.2,3.2276e+011)
	mySource.add_photon(2.5,2.4207e+011)
	mySource.add_photon(3.5,9.6828e+007)
	mySource.points_per_dimension = [16,16,16]
	myModel.add_source(mySource)
	myModel.add_shield(shield.ZAlignedInfiniteAnnulus("iron", cylinder_inner_radius=154, \
		       cylinder_center=[0,0,54.15], cylinder_outer_radius=154+2.54, density=7.8))
	myModel.set_filler_material('air',density=0.00129)
	myModel.set_buildup_factor_material(material.Material('iron'))
	myModel.add_detector(detector.Detector(220,0,50.15))
	result = myModel.calculate_exposure()
	expected_dose_rate = 6.294e+04
	diff = (result - expected_dose_rate)/expected_dose_rate * 100
	print("")
	print('test_benchmark_2')
	print("At 220 cm, dose = ", result, " mR/hr, ", diff, "%")
	assert True

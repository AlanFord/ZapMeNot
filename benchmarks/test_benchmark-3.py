import math

import pytest

from zap_me_not import model,source,shield,detector,material

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

# Benchmark 3 is based on ESIS benchmark shielding problem #1.
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
# The  detector location is 311 cm from the tank centerline
# at the vertical centerline of the tank.
# A concrete shield wall between tank and detector starts at
# x = 220 cm and ends at x=320 cm.
# The water density is 1 g/cm3 and the air density is 0.00122 g/cm3.
# The the steel density is 7.8 g/cm3.
# The concrete density is 2.4 g/cm3.  
# The buildup material is concrete.
# Benchmark acceptable results are 0.49E-3 to 2.46E-3 R/hr.
# Microshield result is 1.89E-3 R/hr  
def test_benchmark_3():
	my_model = model.Model()
	# my_source = source.ZAlignedCylinderSource(materialName="water", cylinderRadius=154, \
	# 	       cylinderCenter=[0,0,54.15], cylinderLength=108.3)
	my_source = source.ZAlignedCylinderSource(material_name="water", cylinder_radius=154, \
		       cylinder_center=[0,0,54.15], cylinder_length=108.3)
	source_volume = 108.3*(154**2)*math.pi # cycinder volume in cm**3
	my_source.add_photon(0.4,4.0E+6*source_volume)
	my_source.add_photon(0.8,7.0E+6*source_volume)
	my_source.add_photon(1.3,2.8E+6*source_volume)
	my_source.add_photon(1.7,8.2E+6*source_volume)
	my_source.add_photon(2.2,4.0E+4*source_volume)
	my_source.add_photon(2.5,3.0E+4*source_volume)
	my_source.add_photon(3.5,1.2E+1*source_volume)
	my_source.points_per_dimension = [16,16,16]
	my_model.add_source(my_source)
	my_model.add_shield(shield.ZAlignedInfiniteAnnulus("iron", cylinder_inner_radius=154, \
		       cylinder_center=[0,0,54.15], cylinder_outer_radius=154+2.54, density=7.8))
	my_model.add_shield(shield.SemiInfiniteXSlab("concrete", x_start=220, \
		       x_end=311, density=2.4))
	my_model.set_filler_material('air',density=0.00122)
	my_model.set_buildup_factor_material(material.Material('concrete'))
	my_model.add_detector(detector.Detector(311, 0, 54.15))
	result = my_model.calculate_exposure()
	# convert from mR/hr to R/hr
	print("")
	print('test_benchmark_3')
	print("At 311 cm, dose = ", result*1e-3, "R/hr")

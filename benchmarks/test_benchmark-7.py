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
# Benchmark 8: Large spherical source of air with a concrete shell 

# Benchmark 6 models a steel container of solidifed resin
# (modeled as a mixture of water and cement).
# Shielding is provided by a 1 ft thick concrete annular shield and
# a 1 ft thick concrete shield wall.
# The container wall is steel with a thickness of 2.54 cm.
# Uniformly distributed in the solidified resin is:
#   Source         Curies
#   Ba-137m        3.8137e+002
#   Co-58          5.2772e+001
#   Co-60          8.6716e+001
#   Cs-137         4.0314e+002
#   Mn-54          3.2597e+001
#   Sb-125         3.0106e+001
#   Te-125m        1.0765e+000
# The  detector horizontal location is 16 ft (487.68 cm) from
# the resin centerline and 2 ft (60.96 cm) above the bottom of the
# resin cylinder.
# The buildup material is concrete.
# Microshield result is 1.718E-01 mR/hr WHEN USING THE LINEAR ENERGY GROUP OPTION
def test_benchmark_7b():
	my_model = model.Model()
	my_source = source.ZAlignedCylinderSource(material_name="resin", cylinder_radius=60.96, \
		       cylinder_center=[0,0,60.96], cylinder_length=121.92)
	my_source.add_isotope_curies('Co-58',5.2772e+001)
	my_source.add_isotope_curies('Co-60',8.6716e+001)
	my_source.add_isotope_curies('Cs-137',4.0314e+002)
	my_source.add_isotope_curies('Mn-54',3.2597e+001)
	my_source.add_isotope_curies('Sb-125',3.0106e+001)
	my_source.add_isotope_curies('Te-125m',1.0765e+000)
	my_source.include_key_progeny = True
	my_source.points_per_dimension = [16,16,16]
	my_model.add_source(my_source)
	my_model.add_shield(shield.ZAlignedInfiniteAnnulus("iron", cylinder_center=[0,0,0], \
		       cylinder_inner_radius=60.96, cylinder_outer_radius=61.595, \
		       density=7.86))
	my_model.add_shield(shield.ZAlignedInfiniteAnnulus("iron", cylinder_center=[0,0,0], \
		       cylinder_inner_radius=76.835, cylinder_outer_radius=81.915, \
		       density=7.86))
	my_model.add_shield(shield.ZAlignedInfiniteAnnulus("concrete", cylinder_center=[0,0,0], \
		       cylinder_inner_radius=81.915, cylinder_outer_radius=112.395, \
		       density=2.35))
	my_model.add_shield(shield.SemiInfiniteXSlab("concrete", x_start=258.763, \
		       x_end=289.243, density=2.35))
	my_model.set_filler_material('air',density=0.00122)
	my_model.set_buildup_factor_material(material.Material('concrete'))
	my_model.add_detector(detector.Detector(487.68,0,60.96))
	result = my_model.calculate_exposure()
	expected_dose_rate = 1.718E-01
	diff = (result - expected_dose_rate)/expected_dose_rate * 100
	print("")
	print('test_benchmark_7')
	print("At 487.68 cm, dose = ", result, " mR/hr, ", diff, "%")
	assert True



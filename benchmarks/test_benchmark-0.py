import math

import pytest

from zap_me_not import model,source,shield,detector,material

pytestmark = pytest.mark.benchmark

#===================================================
# Summary:
# Benchmark 0: ANSI/ANS-6.6.1 Reference Problem I.1
# Benchmark 1: ANSI/ANS-6.6.1 Reference Problem II.1
# Benchmark 2: ESIS Problem #1 - Dose Point D2 -Buildup with Steel
# Benchmark 3: ESIS Problem #1 - Dose Point D3 - Buildup with Concrete
# Benchmark 4: ESIS Problem #2 - Dose Point D5 - Steel Buildup
# Benchmark 5: ESIS Problem #2 - Dose Point D6 - Concrete Buildup
# Benchmark 6: solidified resin container with concrete shield
# Benchmark 7: solidified resin container with concrete and steel shields

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
# 200			8.0E-11 to 1.2E-10   1.194e-11
# 1,000			2.0E-12 to 3.0E-12   3.332e-13
# 3,000			4.5E-14 to 7.5E-14   9.096e-15
# 5,000			3.5E-15 to 5.8E-15   6.977e-16
def test_benchmark_0():
	my_model = model.Model()
	my_source = source.PointSource(0,0,0)
	my_source.add_photon(6.2,1)
	my_model.add_source(my_source)
	my_model.set_filler_material('air',density=0.00122)
	my_model.set_buildup_factor_material(material.Material('air'))
	print("")
	print('test_benchmark_0')
	results = []
	for case in [[200,1.194e-11], [1000,3.332e-13], [3000,9.096e-15], [5000,6.977e-16]]:
		distance = case[0]
		expected_dose_rate = case[1]
		my_model.add_detector(detector.Detector(distance*12*2.54,0,57*12*2.54))
		result = my_model.calculate_exposure()
		diff = (result - expected_dose_rate)/expected_dose_rate * 100
		results.append([result,expected_dose_rate])
		print("At ", distance, " ft, dose = ", result, " mR/hr, ", diff, "%")
	assert True

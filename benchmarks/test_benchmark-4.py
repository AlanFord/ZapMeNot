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

# Benchmark 4 is based on ESIS benchmark shielding problem #2.
# The source is a rectangular water-filled tank 273 cm wide, 273 cm long,
# and 479.9 cm high.
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
# The  detector horizontal location is 228.6 cm from the tank centerline
# at the vertical centerline of the tank.
# The water density is 1 g/cm3 and the air density is 0.00122 g/cm3.
# The the steel density is 7.8 g/cm3.
# The buildup material is iron.
# Benchmark result is 1.49E+2 R/hr.
# Microshield result is 1.33E+2 R/hr  
def test_benchmark_4():
	myModel = model.Model()
	mySource = source.BoxSource(materialName="water", boxCenter=[0,0,239.95], \
		       boxDimensions=[273,273,479.9])
	sourceVolume = 273*273*479.9 
	mySource.addPhoton(0.4,4.0E+6*sourceVolume)
	mySource.addPhoton(0.8,7.0E+6*sourceVolume)
	mySource.addPhoton(1.3,2.8E+6*sourceVolume)
	mySource.addPhoton(1.7,8.2E+6*sourceVolume)
	mySource.addPhoton(2.2,4.0E+4*sourceVolume)
	mySource.addPhoton(2.5,3.0E+4*sourceVolume)
	mySource.addPhoton(3.5,1.2E+1*sourceVolume)
	mySource.pointsPerDimension = [16,16,16]
	myModel.addSource(mySource)
	myModel.addShield(shield.SemiInfiniteXSlab("iron", xStart=136.5, \
		       xEnd=139.04, density=7.8))
	myModel.setFillerMaterial('air',density=0.00122)
	myModel.setBuildupFactorMaterial(material.Material('iron'))
	myModel.addDetector(detector.Detector(228.6,0,239.95))
	result = myModel.calculateExposure()
	# convert from mR/hr to R/hr
	print("")
	print('test_benchmark_4')
	print("At 228.6 cm, dose = ", result*1e-3, "R/hr")

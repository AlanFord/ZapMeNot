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
	myModel = model.Model()
	mySource = source.PointSource(0,0,0)
	mySource.addPhoton(6.2,1)
	myModel.addSource(mySource)
	# in the absence of a fill material option, a sphere shielf of air is used with 
	#   a radius large enough to emcompass the range of detector locations
	myModel.addShield(shield.Sphere(materialName="air", sphereRadius=6000*12*2.54, \
		              sphereCenter=[0,0,0],density=0.00122))
	myModel.setBuildupFactorMaterial(material.Material('air'))
	print("")
	print('test_benchmark_0')
	for distance in [200, 1000, 3000, 5000]:
		myModel.addDetector(detector.Detector(distance*12*2.54,57*12*2.54,0))
		result = myModel.calculateExposure()
		# convert from R/sec to mR/hr
		print("At", distance, "ft, dose = ", result*0.877*8766*1e-3, "Rad/yr")

# Benchmark 1 is based on ANSI/ANS-6.6.1 Reference Problem II.1
# The source is a water-filled tank 35 feet high and 12 feet in diameter.
# Uniformly distributed in the water is a source of 0.8 MeV photons.  The
# volumetric source strength is 30 MeV/sec/cm3, or 37.5 photons/sec/cm3.  There is
# no takn wall to be modeled.
# The  detector locations are 20, 50, 200, and 500 feet from the bottom centerline of
# the tank, offset to the side by 3 feet.
# The water density is 1 g/cm3 and the air density is 0.00122 g/cm3.  The buildup
# reference material is air.
# Acceptable Results:
# Distance   	Dose Rate         Microshield
# (feet)		(Rads/year)       (mrad/hr)
# 20			6.0E-1 to 1.2E0   8.043E-2
# 50			1.2E-1 to 2.2E-1  1.791E-2
# 200			7.5E-3 to 1.5E-2  1.029E-3
# 500			5.4E-4 to 1.2E-3  1.099E-4
def test_benchmark_1():
	myModel = model.Model()
	# mySource = source.ZAlignedCylinderSource(materialName="water", cylinderRadius=6*12*2.54, \
	# 	       cylinderCenter=[0,0,35/2*12*2.54], cylinderLength=35*12*2.54)
	mySource = source.ZAlignedCylinderSource(materialName="water", cylinderRadius=6*12*2.54, \
		       cylinderCenter=[0,0,35/2*12*2.54], cylinderLength=35*12*2.54)
	sourceVolume = 35*(6**2)*math.pi*((12*2.54)**3) # cycinder volume in cm**3
	mySource.addPhoton(0.8,37.5*sourceVolume)
	mySource.pointsPerDimension = [40,20,40]
	myModel.addSource(mySource)
	myModel.addShield(shield.ZAlignedCylinder("air", cylinderRadius=600*12*2.54, \
		       cylinderCenter=[0,0,0], cylinderLength=100*12*2.54, density=0.00122))
	myModel.setBuildupFactorMaterial(material.Material('air'))
	print("")
	print('test_benchmark_1')
	for distance in [20, 50, 200, 500]:
		myModel.addDetector(detector.Detector(distance*12*2.54,3*12*2.54,0))
		result = myModel.calculateExposure()
		# convert from R/sec to mR/hr
		print("At", distance, "ft, dose = ", result*0.877*8766*1e-3, "Rad/yr")

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
# Microshield result is 6.29E+1 R/hr  
def test_benchmark_2():
	myModel = model.Model()
	# mySource = source.ZAlignedCylinderSource(materialName="water", cylinderRadius=154, \
	# 	       cylinderCenter=[0,0,54.15], cylinderLength=108.3)
	mySource = source.ZAlignedCylinderSource(materialName="water", cylinderRadius=154, \
		       cylinderCenter=[0,0,54.15], cylinderLength=108.3)
	sourceVolume = 108.3*(154**2)*math.pi # cycinder volume in cm**3
	mySource.addPhoton(0.4,4.0E+6*sourceVolume)
	mySource.addPhoton(0.8,7.0E+6*sourceVolume)
	mySource.addPhoton(1.3,2.8E+6*sourceVolume)
	mySource.addPhoton(1.7,8.2E+6*sourceVolume)
	mySource.addPhoton(2.2,4.0E+4*sourceVolume)
	mySource.addPhoton(2.5,3.0E+4*sourceVolume)
	mySource.addPhoton(3.5,1.2E+1*sourceVolume)
	mySource.pointsPerDimension = [16,16,16]
	myModel.addSource(mySource)
	myModel.addShield(shield.ZAlignedInfiniteAnnulus("iron", cylinderInnerRadius=154, \
		       cylinderCenter=[0,0,54.15], cylinderOuterRadius=154+2.54, density=7.8))
	myModel.setFillerMaterial('air',density=0.00122)
	myModel.setBuildupFactorMaterial(material.Material('iron'))
	myModel.addDetector(detector.Detector(220,0,50.15))
	result = myModel.calculateExposure()
	# convert from mR/hr to R/hr
	print("")
	print('test_benchmark_2')
	print("At 220 cm, dose = ", result*1e-3, "R/hr")

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
	myModel = model.Model()
	# mySource = source.ZAlignedCylinderSource(materialName="water", cylinderRadius=154, \
	# 	       cylinderCenter=[0,0,54.15], cylinderLength=108.3)
	mySource = source.ZAlignedCylinderSource(materialName="water", cylinderRadius=154, \
		       cylinderCenter=[0,0,54.15], cylinderLength=108.3)
	sourceVolume = 108.3*(154**2)*math.pi # cycinder volume in cm**3
	mySource.addPhoton(0.4,4.0E+6*sourceVolume)
	mySource.addPhoton(0.8,7.0E+6*sourceVolume)
	mySource.addPhoton(1.3,2.8E+6*sourceVolume)
	mySource.addPhoton(1.7,8.2E+6*sourceVolume)
	mySource.addPhoton(2.2,4.0E+4*sourceVolume)
	mySource.addPhoton(2.5,3.0E+4*sourceVolume)
	mySource.addPhoton(3.5,1.2E+1*sourceVolume)
	mySource.pointsPerDimension = [16,16,16]
	myModel.addSource(mySource)
	myModel.addShield(shield.ZAlignedInfiniteAnnulus("iron", cylinderInnerRadius=154, \
		       cylinderCenter=[0,0,54.15], cylinderOuterRadius=154+2.54, density=7.8))
	myModel.addShield(shield.SemiInfiniteXSlab("concrete", xStart=220, \
		       xEnd=311, density=2.4))
	myModel.setFillerMaterial('air',density=0.00122)
	myModel.setBuildupFactorMaterial(material.Material('concrete'))
	myModel.addDetector(detector.Detector(311, 0, 54.15))
	result = myModel.calculateExposure()
	# convert from mR/hr to R/hr
	print("")
	print('test_benchmark_3')
	print("At 311 cm, dose = ", result*1e-3, "R/hr")

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


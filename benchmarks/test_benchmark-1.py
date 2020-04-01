import math

import pytest

from ZapMeNot import model,source,shield,detector,material

pytestmark = pytest.mark.benchmark

# Benchmark 1 is based on ANSI/ANS-6.6.1 Reference Problem I.1
# The source is located at the origin.
# The x-location of the dose point is variable between 200 and 5000 feet.
# The y-location of the dose point i 57 feet.
# There is no shielding other than air between the source and dose point.
# The air density is 0.00122 g/cm3.
# The source energy is 6.2 MeV.
# The source strength is 1 photon/sec.
# The builup material is air.
# Acceptable Results:
# Distance   	Rads/year
# 200			8.0E-11 to 1.2E-10
# 1,000			2.0E-12 to 3.0E-12
# 3,000			4.5E-14 to 7.5E-14
# 5,000			3.5E-15 to 5.8E-15
def test_benchmark_1():
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
	for distance in [200, 1000, 3000, 5000]:
		myModel.addDetector(detector.Detector(distance*12*2.54,57*12*2.54,0))
		result = myModel.calculateExposure()
		# convert from R/sec to mR/hr
		print("At", distance, "ft, dose = ", result*0.877*8766*1e-3, "Rad/yr")

def test_benchmark_2():
	myModel = model.Model()
	mySource = source.ZAlignedCylinderSource(materialName="water", cylinderRadius=6*12*2.54, \
		       cylinderCenter=[0,0,35/2*12*2.54], cylinderLength=35*12*2.54)
	sourceVolume = 35*(6**2)*math.pi*((12*2.54)**3) # cycinder volume in cm**3
	mySource.addPhoton(0.8,37.5*sourceVolume)
	myModel.addSource(mySource)
	myModel.addShield(shield.ZAlignedCylinder("air", cylinderRadius=600*12*2.54, \
		       cylinderCenter=[0,0,35/2*12*2.54], cylinderLength=36*12*2.54))
	myModel.setBuildupFactorMaterial(material.Material('air'))
	print("")
	for distance in [20, 50, 200, 500]:
		myModel.addDetector(detector.Detector(distance*12*2.54,3*12*2.54,0))
		# print("Detector is at ",myModel.detector.x, myModel.detector.y, myModel.detector.z)
		result = myModel.calculateExposure()
		# convert from R/sec to mR/hr
		print("At", distance, "ft, dose = ", result*0.877*8766*1e-3, "Rad/yr")

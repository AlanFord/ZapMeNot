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
	mySource = source.ZAlignedCylinderSource(material_name="water", cylinder_radius=6*12*2.54, \
		       cylinder_center=[0,0,35/2*12*2.54], cylinder_length=35*12*2.54)
	sourceVolume = 35*(6**2)*math.pi*((12*2.54)**3) # cycinder volume in cm**3
	mySource.add_photon(0.8,37.5*sourceVolume)
	mySource.points_per_dimension = [40,20,40]
	myModel.add_source(mySource)
	myModel.add_shield(shield.ZAlignedCylinder("air", cylinder_radius=600*12*2.54, \
		       cylinder_center=[0,0,0], cylinder_length=100*12*2.54, density=0.00122))
	myModel.set_buildup_factor_material(material.Material('air'))
	print("")
	print('test_benchmark_1')
	for distance in [20, 50, 200, 500]:
		myModel.add_detector(detector.Detector(distance*12*2.54,3*12*2.54,0))
		result = myModel.calculate_exposure()
		# convert from R/sec to mR/hr
		print("At", distance, "ft, dose = ", result*0.877*8766*1e-3, "Rad/yr")


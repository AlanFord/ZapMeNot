import math

import pytest

from ZapMeNot import model,source,shield,detector,material

pytestmark = pytest.mark.basic

#=============================================================
class TestPointSource():

	def test_Case0(self):
		# point source with no shielding
		# reference dose calculated from Principles of Radiation Shielding, A. B. Chilton, J. K. Shultis, R. E. Faw
		myModel = model.Model()
		mySource = source.PointSource(0,0,0)
		photonEnergy = 1.0 # MeV
		photonIntensity = 3E10 # photons/sec
		mySource.addPhoton(photonEnergy,photonIntensity)
		myModel.addSource(mySource)
		myModel.addDetector(detector.Detector(100,0,0))
		result = myModel.calculateExposure()
		photonFlux = photonIntensity/(4*math.pi*100**2) # photons/sec/cm2
		responseFunction = 1.835E-8*1.0*2.787E-02 #
		analyticalDose = photonFlux*responseFunction # R/sec
		# the "other code" gives 440.1 mR/hr at an air density of 1e-12g/cc
		assert result == pytest.approx(analyticalDose*1000*3600) # convert from R/sec to mR/hr

	def test_Case1(self):
		# a point source with infinite yz shields
		myModel = model.Model()
		mySource = source.PointSource(0,0,0)
		mySource.addPhoton(1.0,3e10)
		myModel.addSource(mySource)
		myModel.addShield(shield.SemiInfiniteXSlab(materialName="iron", xStart=10, xEnd=20))
		myModel.addShield(shield.SemiInfiniteXSlab(materialName="concrete", xStart=30, xEnd=40))
		myModel.addDetector(detector.Detector(100,0,0))
		myModel.setBuildupFactorMaterial(material.Material('iron'))
		result = myModel.calculateExposure()
		assert result == pytest.approx(2.218926692201380e-06*1000*3600) # convert from R/sec to mR/hr

	def test_Case2(self):
		# a point source with infinite yz shields
		myModel = model.Model()
		mySource = source.PointSource(0,0,0)
		mySource.addPhoton(1.0,3e10)
		myModel.addSource(mySource)
		myModel.addShield(shield.SemiInfiniteXSlab(materialName="iron", xStart=10, xEnd=20))
		myModel.addDetector(detector.Detector(100,0,0))
		myModel.setBuildupFactorMaterial(material.Material('iron'))
		result = myModel.calculateExposure()
		assert result == pytest.approx(7.057332942044014e-06*1000*3600) # convert from R/sec to mR/hr

	def test_Case3(self):
		# a point source with infinite yz shields
		myModel = model.Model()
		mySource = source.PointSource(0,0,0)
		mySource.addIsotopeBq('Ar-41',3e10)
		myModel.addSource(mySource)
		myModel.addShield(shield.SemiInfiniteXSlab(materialName="iron", xStart=10, xEnd=20))
		myModel.addShield(shield.SemiInfiniteXSlab(materialName="concrete", xStart=30, xEnd=40))
		myModel.addDetector(detector.Detector(100,0,0))
		myModel.setBuildupFactorMaterial(material.Material('iron'))
		result = myModel.calculateExposure()
		assert result == pytest.approx(4.3979088503738596e-06*1000*3600) # convert from R/sec to mR/hr

	def test_Case4(self):
		# a point source with infinite yz shields
		myModel = model.Model()
		mySource = source.PointSource(1,2,3)
		mySource.addIsotopeCuries('Co-60',3)
		myModel.addSource(mySource)
		myModel.addShield(shield.SemiInfiniteXSlab(materialName="iron", xStart=10, xEnd=20))
		myModel.addShield(shield.SemiInfiniteXSlab(materialName="concrete", xStart=30, xEnd=40))
		myModel.addDetector(detector.Detector(80,90,100))
		myModel.setBuildupFactorMaterial(material.Material('iron'))
		result = myModel.calculateExposure()
		assert result == pytest.approx(0.6090081012193129) # convert from R/sec to mR/hr

#=============================================================
class TestLineSource():

	def test_Case0(self):
		# point source with no shielding
		# reference dose calculated from Principles of Radiation Shielding, A. B. Chilton, J. K. Shultis, R. E. Faw
		# from the reference, pages 132, 157, and 159, th dose rate is 64.66 mR/hr
		# the "other code" gives 64.74 mR/hr at an air density of 1e-12g/cc
		myModel = model.Model()
		mySource = source.LineSource([0,0,0],[0,0,1000])
		mySource.pointsPerDimension = 100
		photonEnergy = 1.0 # MeV
		photonIntensity = 3E10 # photons/sec
		mySource.addPhoton(photonEnergy,photonIntensity)
		myModel.addSource(mySource)
		myModel.addDetector(detector.Detector(100,0,0))
		result = myModel.calculateExposure()
		linearPhotonSource = photonIntensity/1000
		photonFlux = linearPhotonSource/100*math.atan(1000/100) # photons/sec/cm2
		responseFunction = 1.835E-8*1.0*2.787E-02/4/math.pi #
		analyticalDose = photonFlux*responseFunction # R/sec
		assert result == pytest.approx(analyticalDose*1000*3600) # convert from R/sec to mR/hr

#=============================================================
class TestZAlignedCylinderSource():

	def test_Case0(self):
		# point source with no shielding
		# reference dose calculated from Principles of Radiation Shielding, A. B. Chilton, J. K. Shultis, R. E. Faw
		# from the reference, pages 132, 157, and 159, th dose rate is 271.8 mR/hr
		# the "other code" gives 271.8 mR/hr at an air density of 1e-12g/cc
		myModel = model.Model()
		mySource = source.ZAlignedCylinderSource(materialName='air', \
			cylinderCenter=[0,0,500],cylinderLength=1000, \
			cylinderRadius=50,density=1e-12)
		mySource.pointsPerDimension = [40,20,400]
		photonEnergy = 1.0 # MeV
		photonIntensity = 3E10 # photons/sec
		mySource.addPhoton(photonEnergy,photonIntensity)
		myModel.addSource(mySource)
		myModel.addDetector(detector.Detector(0,0,1000.01))
		result = myModel.calculateExposure()
		assert result == pytest.approx(271.628) 



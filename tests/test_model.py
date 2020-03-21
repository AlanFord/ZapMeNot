from ZapMeNot import model,source,shield,detector,material
import pytest
#import numpy as np

def test_Case1():
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

def test_Case2():
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

def test_Case3():
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

def test_Case4():
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

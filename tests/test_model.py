from ZapMeNot import model,source,shield,detector,material
import pytest
#import numpy as np

def test_Case1():
	# a point source with infinite yz shields
	myModel = model.Model()
	mySource = source.PointSource(0,0,0)
	mySource.addPhoton(1.0,3e10)
	myModel.addSource(mySource)
	myModel.addShield(shield.XInfiniteSlab("iron", 10, 20))
	myModel.addDetector(detector.Detector(100,0,0))
	myModel.setBuildupFactorMaterial(material.Material('iron'))
	result = myModel.calculateExposure()
	assert result == pytest.approx(7.057332942044014e-06)

def test_Case2():
	# a point source with infinite yz shields
	myModel = model.Model()
	mySource = source.PointSource(1,2,3)
	mySource.addIsotopeCuries('Co-60',3)
	myModel.addSource(mySource)
	myModel.addShield(shield.XInfiniteSlab("iron", 10, 20))
	myModel.addShield(shield.XInfiniteSlab("concrete", 30, 40))
	myModel.addDetector(detector.Detector(80,90,100))
	myModel.setBuildupFactorMaterial(material.Material('iron'))
	result = myModel.calculateExposure()
	assert result == pytest.approx(2.218926692201380e-06)

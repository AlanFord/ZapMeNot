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
		mySource.add_photon(photonEnergy,photonIntensity)
		myModel.add_source(mySource)
		myModel.add_detector(detector.Detector(100,0,0))
		result = myModel.calculate_exposure()
		photonFlux = photonIntensity/(4*math.pi*100**2) # photons/sec/cm2
		responseFunction = 1.835E-8*1.0*2.787E-02 #
		analyticalDose = photonFlux*responseFunction # R/sec
		# the "other code" gives 440.1 mR/hr at an air density of 1e-12g/cc
		assert result == pytest.approx(analyticalDose*1000*3600) # convert from R/sec to mR/hr

	def test_Case1(self):
		# a point source with infinite yz shields
		myModel = model.Model()
		mySource = source.PointSource(0,0,0)
		mySource.add_photon(1.0,3e10)
		myModel.add_source(mySource)
		myModel.add_shield(shield.SemiInfiniteXSlab(material_name="iron", x_start=10, x_end=20))
		myModel.add_shield(shield.SemiInfiniteXSlab(material_name="concrete", x_start=30, x_end=40))
		myModel.add_detector(detector.Detector(100,0,0))
		myModel.set_buildup_factor_material(material.Material('iron'))
		result = myModel.calculate_exposure()
		assert result == pytest.approx(2.218926692201380e-06*1000*3600) # convert from R/sec to mR/hr

	def test_Case2(self):
		# a point source with infinite yz shields
		myModel = model.Model()
		mySource = source.PointSource(0,0,0)
		mySource.add_photon(1.0,3e10)
		myModel.add_source(mySource)
		myModel.add_shield(shield.SemiInfiniteXSlab(material_name="iron", x_start=10, x_end=20))
		myModel.add_detector(detector.Detector(100,0,0))
		myModel.set_buildup_factor_material(material.Material('iron'))
		result = myModel.calculate_exposure()
		assert result == pytest.approx(7.057332942044014e-06*1000*3600) # convert from R/sec to mR/hr

	def test_Case3(self):
		# a point source with infinite yz shields
		myModel = model.Model()
		mySource = source.PointSource(0,0,0)
		mySource.add_isotope_bq('Ar-41',3e10)
		myModel.add_source(mySource)
		myModel.add_shield(shield.SemiInfiniteXSlab(material_name="iron", x_start=10, x_end=20))
		myModel.add_shield(shield.SemiInfiniteXSlab(material_name="concrete", x_start=30, x_end=40))
		myModel.add_detector(detector.Detector(100,0,0))
		myModel.set_buildup_factor_material(material.Material('iron'))
		result = myModel.calculate_exposure()
		assert result == pytest.approx(4.3979088503738596e-06*1000*3600) # convert from R/sec to mR/hr

	def test_Case4(self):
		# a point source with infinite yz shields
		myModel = model.Model()
		mySource = source.PointSource(1,2,3)
		mySource.add_isotope_curies('Co-60',3)
		myModel.add_source(mySource)
		myModel.add_shield(shield.SemiInfiniteXSlab(material_name="iron", x_start=10, x_end=20))
		myModel.add_shield(shield.SemiInfiniteXSlab(material_name="concrete", x_start=30, x_end=40))
		myModel.add_detector(detector.Detector(80,90,100))
		myModel.set_buildup_factor_material(material.Material('iron'))
		result = myModel.calculate_exposure()
		assert result == pytest.approx(0.6090081012193129) # convert from R/sec to mR/hr

#=============================================================
class TestLineSource():

	def test_Case0(self):
		# point source with no shielding
		# reference dose calculated from Principles of Radiation Shielding, A. B. Chilton, J. K. Shultis, R. E. Faw
		# from the reference, pages 132, 157, and 159, th dose rate is 64.66 mR/hr
		# Microshield gives 64.74 mR/hr at an air density of 1e-12g/cc
		myModel = model.Model()
		mySource = source.LineSource([0,0,0],[0,0,1000])
		mySource.points_per_dimension = 100
		photonEnergy = 1.0 # MeV
		photonIntensity = 3E10 # photons/sec
		mySource.add_photon(photonEnergy,photonIntensity)
		myModel.add_source(mySource)
		myModel.add_detector(detector.Detector(100,0,0))
		result = myModel.calculate_exposure()
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
		# Microshield gives 271.8 mR/hr at an air density of 1e-12g/cc
		myModel = model.Model()
		mySource = source.ZAlignedCylinderSource(material_name='air', \
			cylinder_center=[0,0,500],cylinder_length=1000, \
			cylinder_radius=50,density=1e-12)
		mySource.points_per_dimension = [40,20,400]
		photonEnergy = 1.0 # MeV
		photonIntensity = 3E10 # photons/sec
		mySource.add_photon(photonEnergy,photonIntensity)
		myModel.add_source(mySource)
		myModel.add_detector(detector.Detector(0,0,1000.01))
		result = myModel.calculate_exposure()
		assert result == pytest.approx(271.628) 



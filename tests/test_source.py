import pytest
import numpy as np

from zap_me_not import source

pytestmark = pytest.mark.basic


class TestPointSource():

	def test_addIsotopeCuries(self):
		my_source = source.PointSource(1,2,3)
		my_source.add_isotope_curies('Co-60',3.14)
		my_source.add_isotope_curies('Cu-11',8)
		my_list = [('Co-60',3.14*3.7E10), ('Cu-11', 8*3.7E10)]
		assert my_list == my_source.list_isotopes()


	def test_addIsotopeBq(self):
		my_source = source.PointSource(1,2,3)
		my_source.add_isotope_bq('Co-60',3.14E9)
		my_source.add_isotope_bq('Cs-137',1E6)
		my_list = [('Co-60',3.14E9), ('Cs-137',1E6)]
		assert my_list ==my_source.list_isotopes()

	def test_addPhoton(self):
		my_source = source.PointSource(1,2,3)
		my_source.add_photon(0.9876,3.14E2)
		my_source.add_photon(0.02,5)
		my_list = [(0.9876,3.14E2),(0.02,5)]
		assert my_list == my_source.list_unique_photons()

	def test_getPhotonEnergyList(self):
		my_source = source.PointSource(1,2,3)
		my_source.add_isotope_curies('Ar-41',3.14)
		my_source.add_isotope_bq('Br-80m',1E6)
		my_source.add_photon(0.9876,3.14E2)
		a = my_source.get_photon_source_list()
		np.testing.assert_allclose(a, \
			[(0.037052, 390000), \
			 (0.0489, 3200), \
			 (0.9876, 314), \
			 (1.29364, 115204088000.0), \
			 (1.677, 60413600)])

	def test_getSourcePoints(self):
		my_source = source.PointSource(1,2,3)
		np.testing.assert_allclose(my_source.get_source_points(), \
			[(1,2,3)])

#=============================================================

class TestLineSource():

	def test_addIsotopeCuries(self):
		my_source = source.LineSource([1,2,3], [11,12,13])
		my_source.add_isotope_curies('Co-60',3.14)
		my_source.add_isotope_curies('Cu-11',8)
		my_list = [('Co-60',3.14*3.7E10), ('Cu-11', 8*3.7E10)]
		assert my_list == my_source.list_isotopes()


	def test_addIsotopeBq(self):
		my_source = source.LineSource([1,2,3], [11,12,13])
		my_source.add_isotope_bq('Co-60',3.14E9)
		my_source.add_isotope_bq('Cs-137',1E6)
		my_list = [('Co-60',3.14E9), ('Cs-137',1E6)]
		assert my_list == my_source.list_isotopes()

	def test_addPhoton(self):
		my_source = source.LineSource([1,2,3], [11,12,13])
		my_source.add_photon(0.9876,3.14E2)
		my_source.add_photon(0.02,5)
		my_list = [(0.9876,3.14E2),(0.02,5)]
		assert my_list == my_source.list_unique_photons()

	def test_getPhotonEnergyList(self):
		my_source = source.LineSource([1,2,3], [11,12,13])
		my_source.add_isotope_curies('Ar-41',3.14)
		my_source.add_isotope_bq('Br-80m',1E6)
		my_source.add_photon(0.9876,3.14E2)
		a = my_source.get_photon_source_list()
		# the following intensities are adjusted for the default 10 
		# intervals in the line source
		np.testing.assert_allclose(a, \
			[(0.037052, 390000/10), \
			 (0.0489, 3200/10), \
			 (0.9876, 314/10), \
			 (1.29364, 115204088000.0/10), \
			 (1.677, 60413600/10)])

	def test_getSourcePoints(self):
		my_source = source.LineSource([1,2,3], [11,12,13])
		np.testing.assert_allclose(my_source.get_source_points(), \
			[[ 1.5, 2.5, 3.5], \
			 [ 2.5, 3.5, 4.5], \
			 [ 3.5, 4.5, 5.5], \
			 [ 4.5, 5.5, 6.5], \
			 [ 5.5, 6.5, 7.5], \
			 [ 6.5, 7.5, 8.5], \
			 [ 7.5, 8.5, 9.5], \
			 [ 8.5, 9.5,10.5], \
			 [ 9.5,10.5,11.5], \
			 [10.5,11.5,12.5]])

#=============================================================

class TestBoxSource():

	def test_getSourcePoints(self):
		my_source = source.BoxSource(box_center=[4,5,6],box_dimensions=[10,10,10],material_name='iron')
		my_source.points_per_dimension= [1,1,1]
		np.testing.assert_allclose(my_source.get_source_points(), \
			[(4,5,6)])
		my_source.points_per_dimension= [2,2,2]
		np.testing.assert_allclose(my_source.get_source_points(), \
			[[4-2.5,5-2.5,6-2.5], \
			 [4-2.5,5-2.5,6+2.5], \
			 [4-2.5,5+2.5,6-2.5], \
			 [4-2.5,5+2.5,6+2.5], \
			 [4+2.5,5-2.5,6-2.5], \
			 [4+2.5,5-2.5,6+2.5], \
			 [4+2.5,5+2.5,6-2.5], \
			 [4+2.5,5+2.5,6+2.5]])
		my_source.add_isotope_curies('Ar-41',3.14)
		my_source.add_isotope_bq('Br-80m',1E6)
		my_source.add_photon(0.9876,3.14E2)
		a = my_source.get_photon_source_list()
		np.testing.assert_allclose(a, \
			[(0.037052, 390000/8), \
			 (0.0489, 3200/8), \
			 (0.9876, 314/8), \
			 (1.29364, 115204088000.0/8), \
			 (1.677, 60413600/8)])

#=============================================================

class TestXAlignedCylinderSource():

	def test_getSourcePoints(self):
		pass

#=============================================================

class TestYAlignedCylinderSource():

	def test_getSourcePoints(self):
		pass

#=============================================================

class TestZAlignedCylinderSource():

	def test_getSourcePoints(self):
		my_source = source.ZAlignedCylinderSource(cylinder_center=[0,0,0],cylinder_length=10,cylinder_radius=5,material_name='iron')
		my_source.points_per_dimension= [3,3,3]
		sourcePoints = my_source.get_source_points()
		np.testing.assert_allclose(sourcePoints, \
			[[7.2168783649e-01, 1.2500000000e+00, 1.6666666667e+00], \
			[7.2168783649e-01, 1.2500000000e+00, 5], \
			[7.2168783649e-01, 1.2500000000e+00, 8.3333333333e+00], \
			[-1.4433756730e+00, 1.7676253979e-16, 1.6666666667e+00], \
			[-1.4433756730e+00, 1.7676253979e-16, 5], \
			[-1.4433756730e+00, 1.7676253979e-16, 8.3333333333e+00], \
			[7.2168783649e-01, -1.2500000000e+00, 1.6666666667e+00], \
			[7.2168783649e-01, -1.2500000000e+00, 5], \
			[7.2168783649e-01, -1.2500000000e+00, 8.3333333333e+00], \
			[1.7423085626e+00, 3.0177669530e+00, 1.6666666667e+00], \
			[1.7423085626e+00, 3.0177669530e+00, 5], \
			[1.7423085626e+00, 3.0177669530e+00, 8.3333333333e+00], \
			[-3.4846171253e+00, 4.2674252087e-16, 1.6666666667e+00], \
			[-3.4846171253e+00, 4.2674252087e-16, 5], \
			[-3.4846171253e+00, 4.2674252087e-16, 8.3333333333e+00], \
			[1.7423085626e+00, -3.0177669530e+00, 1.6666666667e+00], \
			[1.7423085626e+00, -3.0177669530e+00, 5], \
			[1.7423085626e+00, -3.0177669530e+00, 8.3333333333e+00], \
			[2.2706207262e+00, 3.9328304624e+00, 1.6666666667e+00], \
			[2.2706207262e+00, 3.9328304624e+00, 5], \
			[2.2706207262e+00, 3.9328304624e+00, 8.3333333333e+00], \
			[-4.5412414523e+00, 5.5614168087e-16, 1.6666666667e+00], \
			[-4.5412414523e+00, 5.5614168087e-16, 5], \
			[-4.5412414523e+00, 5.5614168087e-16, 8.3333333333e+00], \
			[2.2706207262e+00, -3.9328304624e+00, 1.6666666667e+00], \
			[2.2706207262e+00, -3.9328304624e+00, 5], \
			[2.2706207262e+00, -3.9328304624e+00, 8.3333333333e+00]])

		my_source.add_isotope_curies('Ar-41',3.14)
		my_source.add_isotope_bq('Br-80m',1E6)
		my_source.add_photon(0.9876,3.14E2)
		a = my_source.get_photon_source_list()
		# the following intensities are adjusted for 3 intervals 
		# intervals in each dimension
		np.testing.assert_allclose(a, \
			[(0.037052, 390000/27), \
			 (0.0489, 3200/27), \
			 (0.9876, 314/27), \
			 (1.29364, 115204088000.0/27), \
			 (1.677, 60413600/27)])





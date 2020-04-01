import pytest
import numpy as np

from ZapMeNot import source

pytestmark = pytest.mark.basic


class TestPointSource():

	def test_addIsotopeCuries(self):
		self.mySource = source.PointSource(1,2,3)
		self.mySource.addIsotopeCuries('Co-60',3.14)
		self.mySource.addIsotopeCuries('Cu-11',8)
		myList = [('Co-60',3.14*3.7E10), ('Cu-11', 8*3.7E10)]
		assert myList == self.mySource.listIsotopes()


	def test_addIsotopeBq(self):
		self.mySource = source.PointSource(1,2,3)
		self.mySource.addIsotopeBq('Co-60',3.14E9)
		self.mySource.addIsotopeBq('Cs-137',1E6)
		myList = [('Co-60',3.14E9), ('Cs-137',1E6)]
		assert myList == self.mySource.listIsotopes()

	def test_addPhoton(self):
		self.mySource = source.PointSource(1,2,3)
		self.mySource.addPhoton(0.9876,3.14E2)
		self.mySource.addPhoton(0.02,5)
		myList = [(0.9876,3.14E2),(0.02,5)]
		assert myList == self.mySource.listUniquePhotons()

	def test_getPhotonEnergyList(self):
		self.mySource = source.PointSource(1,2,3)
		self.mySource.addIsotopeCuries('Ar-41',3.14)
		self.mySource.addIsotopeBq('Br-80m',1E6)
		self.mySource.addPhoton(0.9876,3.14E2)
		a = self.mySource.getPhotonSourceList()
		np.testing.assert_allclose(a, \
			[(0.037052, 390000), \
			 (0.0489, 3200), \
			 (0.9876, 314), \
			 (1.29364, 115204088000.0), \
			 (1.677, 60413600)])

	def test_getSourcePoints(self):
		self.mySource = source.PointSource(1,2,3)
		np.testing.assert_allclose(self.mySource.getSourcePoints(), \
			[(1,2,3)])

#=============================================================

class TestLineSource():

	def test_addIsotopeCuries(self):
		self.mySource = source.LineSource([1,2,3], [11,12,13])
		self.mySource.addIsotopeCuries('Co-60',3.14)
		self.mySource.addIsotopeCuries('Cu-11',8)
		myList = [('Co-60',3.14*3.7E10), ('Cu-11', 8*3.7E10)]
		assert myList == self.mySource.listIsotopes()


	def test_addIsotopeBq(self):
		self.mySource = source.LineSource([1,2,3], [11,12,13])
		self.mySource.addIsotopeBq('Co-60',3.14E9)
		self.mySource.addIsotopeBq('Cs-137',1E6)
		myList = [('Co-60',3.14E9), ('Cs-137',1E6)]
		assert myList == self.mySource.listIsotopes()

	def test_addPhoton(self):
		self.mySource = source.LineSource([1,2,3], [11,12,13])
		self.mySource.addPhoton(0.9876,3.14E2)
		self.mySource.addPhoton(0.02,5)
		myList = [(0.9876,3.14E2),(0.02,5)]
		assert myList == self.mySource.listUniquePhotons()

	def test_getPhotonEnergyList(self):
		self.mySource = source.LineSource([1,2,3], [11,12,13])
		self.mySource.addIsotopeCuries('Ar-41',3.14)
		self.mySource.addIsotopeBq('Br-80m',1E6)
		self.mySource.addPhoton(0.9876,3.14E2)
		a = self.mySource.getPhotonSourceList()
		# the following intensities are adjusted for the default 10 
		# intervals in the line source
		np.testing.assert_allclose(a, \
			[(0.037052, 390000/10), \
			 (0.0489, 3200/10), \
			 (0.9876, 314/10), \
			 (1.29364, 115204088000.0/10), \
			 (1.677, 60413600/10)])

	def test_getSourcePoints(self):
		self.mySource = source.LineSource([1,2,3], [11,12,13])
		np.testing.assert_allclose(self.mySource.getSourcePoints(), \
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
		mySource = source.BoxSource(boxCenter=[4,5,6],boxDimensions=[10,10,10],materialName='iron')
		mySource.pointsPerDimension= [1,1,1]
		np.testing.assert_allclose(mySource.getSourcePoints(), \
			[(4,5,6)])
		mySource.pointsPerDimension= [2,2,2]
		np.testing.assert_allclose(mySource.getSourcePoints(), \
			[[4-2.5,5-2.5,6-2.5], \
			 [4-2.5,5-2.5,6+2.5], \
			 [4-2.5,5+2.5,6-2.5], \
			 [4-2.5,5+2.5,6+2.5], \
			 [4+2.5,5-2.5,6-2.5], \
			 [4+2.5,5-2.5,6+2.5], \
			 [4+2.5,5+2.5,6-2.5], \
			 [4+2.5,5+2.5,6+2.5]])
		mySource.addIsotopeCuries('Ar-41',3.14)
		mySource.addIsotopeBq('Br-80m',1E6)
		mySource.addPhoton(0.9876,3.14E2)
		a = mySource.getPhotonSourceList()
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
		mySource = source.ZAlignedCylinderSource(cylinderCenter=[0,0,0],cylinderLength=10,cylinderRadius=5,materialName='iron')
		mySource.pointsPerDimension= [3,3,3]
		sourcePoints = mySource.getSourcePoints()
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

		mySource.addIsotopeCuries('Ar-41',3.14)
		mySource.addIsotopeBq('Br-80m',1E6)
		mySource.addPhoton(0.9876,3.14E2)
		a = mySource.getPhotonSourceList()
		# the following intensities are adjusted for 3 intervals 
		# intervals in each dimension
		np.testing.assert_allclose(a, \
			[(0.037052, 390000/27), \
			 (0.0489, 3200/27), \
			 (0.9876, 314/27), \
			 (1.29364, 115204088000.0/27), \
			 (1.677, 60413600/27)])





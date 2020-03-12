from ZapMeNot import source
import numpy as np


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


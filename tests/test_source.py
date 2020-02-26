import unittest
from ZapMeNot import source

class testPointSource(unittest.TestCase):

	def setUp(self):
		self.mySource = source.PointSource(1,2,3)

	def test_addIsotopeCuries(self):
		self.mySource.addIsotopeCuries('Co-60',3.14)
		self.mySource.addIsotopeCuries('Cu-11',8)
		myList = [('Co-60',3.14*3.7E10), ('Cu-11', 8*3.7E10)]
		self.assertEqual(myList, self.mySource.listIsotopes())

	def test_addIsotopeBq(self):
		self.mySource.addIsotopeBq('Co-60',3.14E9)
		self.mySource.addIsotopeBq('Cs-137',1E6)
		myList = [('Co-60',3.14E9), ('Cs-137',1E6)]
		self.assertEqual(myList, self.mySource.listIsotopes())

	def test_addPhoton(self):
		self.mySource.addPhoton(0.9876,3.14E2)
		self.mySource.addPhoton(0.02,5)
		myList = [(0.9876,3.14E2),(0.02,5)]
		self.assertEqual(myList, self.mySource.listUniquePhotons())

	def test_getPhotonEnergyList(self):
		self.mySource.addIsotopeCuries('Ar-41',3.14)
		self.mySource.addIsotopeBq('Br-80m',1E6)
		self.mySource.addPhoton(0.9876,3.14E2)
		a = self.mySource.getPhotonSourceList()
		self.assertCountEqual(a, [(1.29364, 115204088000.0), \
			(1.677, 60413599.99999999), (0.037052, 390000.0), \
			(0.0489, 3200.0), (0.9876, 314.0)])

	def test_iteratePoints(self):
		pass

	def test_PointSourceLocations(self):
		pass
import unittest
from ZapMeNot import shield, ray, material

class testXInfiniteSlab(unittest.TestCase):

	def setUp(self):
		self.myShield = shield.SemiInfiniteXSlab("iron", 10, 20)
		start = [0,0,0]
		end = [30,30,30]
		self.aRay = ray.Ray(start, end)

	# test getting a crossing length
	def test_crossing_length(self):
		length = self.myShield.getCrossingLength(self.aRay)
		self.assertAlmostEqual(length,17.320508075688775)

	# test getting a crossing mfp
	def test_get_MFP(self):
		mfp = self.myShield.getCrossingMFP(self.aRay, 0.66)
		self.assertAlmostEqual(mfp,9.923087573149688)

	# test getting a crossing mfp
	def test_get_special_MFP(self):
		start = [0,0,0]
		end = [100,0,0]
		self.aRay = ray.Ray(start, end)
		mfp = self.myShield.getCrossingMFP(self.aRay, 1)
		self.assertAlmostEqual(mfp,4.6905418)




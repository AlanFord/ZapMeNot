import unittest
from ZapMeNot import shield, ray, material

class testXInfiniteSlab(unittest.TestCase):

	def setUp(self):
		self.myShield = shield.XInfiniteSlab("iron", 10, 20)
		self.aRay = ray.Ray()
		self.aRay.start = [0,0,0]
		self.aRay.end = [30,30,30]

	# test getting a crossing length
	def test_crossing_length(self):
		length = self.myShield.getCrossingLength(self.aRay)
		self.assertAlmostEqual(length,17.320508075688775)

	# test getting a crossing mfp
	def test_get_MFP(self):
		mfp = self.myShield.getCrossingMFP(self.aRay, 0.66)
		self.assertAlmostEqual(mfp,9.984366454164944)

	# test getting a crossing mfp
	def test_get_special_MFP(self):
		self.aRay = ray.Ray()
		self.aRay.start = [0,0,0]
		self.aRay.end = [100,0,0]
		mfp = self.myShield.getCrossingMFP(self.aRay, 1)
		self.assertAlmostEqual(mfp,4.6905418)


	# test line/plane collision


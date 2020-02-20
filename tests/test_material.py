import unittest
from ZapMeNot import material

class testMaterial(unittest.TestCase):
	# test response to a bad material name
	def test_a_bad_material_name(self):
		self.assertRaises(ValueError, material.Material, "wanker")

	# test setting a new density
	def test_setDensity(self):
		a = material.Material("air")
		a.setDensity(3.14)
		self.assertEqual(a.density, 3.14)

	# test retrieval of the MFP
	def test_getMfp(self):
		a = material.Material("air")
		b = a.getMfp(0.66, 10)
		self.assertAlmostEqual(b, 0.157455925247154)

	# test retrieval of a mass attenuation coefficient
	# WARNING: result is based on preliminary test dataset!
	# comparison value calculated in Matlab
	def test_getMassAttenCoff(self):
		a = material.Material("air")
		b = a.getMassAttenCoff(0.66)
		self.assertAlmostEqual(b,0.077482)

	# test response to a bad material name
	def test_a_bad_buildupFactorType(self):
		a = material.Material("air")
		self.assertRaises(ValueError, a.getBuildupFactor, 0.66, 10, "Taylor")

	# test calculation of a buildup factor
	def test_getBuildupFactor(self):
		a = material.Material("air")
		b = a.getBuildupFactor(0.66, 10, "GP")
		self.assertAlmostEqual(b,45.214774926711492)


	# test calculation of a buildup factor from coefficients


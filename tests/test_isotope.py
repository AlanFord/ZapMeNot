import unittest
from ZapMeNot import isotope


class testIsotope(unittest.TestCase):
	# test response to a bad isotope name
	def test_a_bad_material_name(self):
		self.assertRaises(ValueError, isotope.Isotope, "wanker")

	# test valid half life in years
	def test_halflifeYears(self):
		a = isotope.Isotope("co-60")
		self.assertAlmostEqual(a.half_life, 5.2713*365.25*24*60*60)

	# test valid half life in days

	# test valid half life in hours
	def test_halflifeMinutes(self):
		a = isotope.Isotope("cu-67")
		self.assertAlmostEqual(a.half_life, 61.83*60*60)

	# test valid half life in minutes
	def test_halflifeMinutes(self):
		a = isotope.Isotope("c-11")
		self.assertAlmostEqual(a.half_life, 20.334*60)

	# test valid half life in seconds

	# test valid photon property read and store
	def test_photon_readAndStore(self):
		a = isotope.Isotope("co-60")
		self.assertEqual(a.photons, [[0.6938, 0.00016312], [1.1732, 1.0], [1.3325, 1.0]])





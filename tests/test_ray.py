import unittest
import math
from ZapMeNot import ray
import numpy as np

class testRay(unittest.TestCase):
	# test length
	def test_ray_length(self):
		a = ray.Ray()
		a.start = np.array([1, 1, 1])
		a.end = np.array([2,2,2])
		self.assertAlmostEqual(a.length(),math.sqrt(3.))
		
	# test unit vector
	def test_ray_unit_vector(self):
		a = ray.Ray()
		a.start = np.array([1, 1, 1])
		a.end = np.array([2,2,2])
		part = 1./math.sqrt(3.)
		self.assertTrue((a.unitVector == np.array([a,a,a])).all)


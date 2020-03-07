import unittest
import math
from ZapMeNot import ray
import numpy as np

class testRay(unittest.TestCase):
	# test length
	def test_ray_length(self):
		start = [1, 1, 1]
		end = [2,2,2]
		a = ray.Ray(start, end)
		self.assertAlmostEqual(a.length,math.sqrt(3.))
		
	# test unit vector
	def test_ray_unit_vector(self):
		start = [1, 1, 1]
		end = [2,2,2]
		a = ray.Ray(start, end)
		part = 1./math.sqrt(3.)
		self.assertTrue((a.dir == np.array([part,part,part])).all)


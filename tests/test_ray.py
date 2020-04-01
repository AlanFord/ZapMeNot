import math

import numpy as np
import pytest

from ZapMeNot import ray

pytestmark = pytest.mark.basic

def test_ray_length():
	start = [1, 1, 1]
	end = [2,2,2]
	a = ray.Ray(start, end)
	assert (a.origin == np.array(start)).all
	assert a.length == pytest.approx(math.sqrt(3.))
	
def test_ray_unit_vector():
	start = [1, 1, 1]
	end = [2,2,2]
	a = ray.Ray(start, end)
	part = 1./math.sqrt(3.)
	# the following creates a vector of numerical tests and then checks to ensure
	# they all came back true
	assert (a.dir == np.array([part,part,part])).all
	assert (a.invdir == np.array([1/part, 1/part, 1/part])).all
	assert (a.sign == np.array([False, False, False])).all





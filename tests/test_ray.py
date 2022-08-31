import math

import numpy as np
import pytest

from zap_me_not import ray

pytestmark = pytest.mark.basic

# test calculation of ray length
# reference: hand calculation
def test_ray_length():
    start = [1, 1, 1]
    end = [2, 2, 2]
    aaa = ray.FiniteLengthRay(start, end)
    assert (aaa.origin == np.array(start)).all
    assert aaa.length == pytest.approx(math.sqrt(3.))

# test calculaton of ray properties dir, invdir, sign
# reference: hand calculation
def test_ray_unit_vector():
    start = [1, 1, 1]
    end = [2, 2, 2]
    aaa = ray.FiniteLengthRay(start, end)
    part = 1./math.sqrt(3.)
    # the following creates a vector of numerical tests and then
    # checks to ensure they all came back true
    assert (aaa.origin == [1, 1, 1]).all
    assert aaa.length == math.sqrt(3.)
    assert (aaa.dir == np.array([part, part, part])).all
    assert (aaa.invdir == np.array([1/part, 1/part, 1/part])).all
    assert (aaa.sign == np.array([False, False, False])).all
    
# test invalid initializations
def test_ray_error_trapping():
    start = [1, 1, 1, 1]
    end = [2, 2, 2]
    with pytest.raises(ValueError):
        aaa = ray.FiniteLengthRay(start, end) # start vector too long
    start = [1, 1, 1]
    end = [2, 2, 2, 2]
    with pytest.raises(ValueError):
        aaa = ray.FiniteLengthRay(start, end) # end vector too long
    start = "start"
    end = [2, 2, 2]
    with pytest.raises(ValueError):
        aaa = ray.FiniteLengthRay(start, end) # non-numeric start
    start = [1, 1, "start"]
    end = [2, 2, 2]
    with pytest.raises(ValueError):
        aaa = ray.FiniteLengthRay(start, end) # non-numeric start
    start = [1, 1, 1]
    end = "end"
    with pytest.raises(ValueError):
        aaa = ray.FiniteLengthRay(start, end) # non-numeric end
    start = [1, 1, 1]
    end = [2, 2, "end"]
    with pytest.raises(ValueError):
        aaa = ray.FiniteLengthRay(start, end) # non-numeric end

def test_ray_properties():
    start = [1, 1, 1]
    end = [2, 2, 2]
    aaa = ray.FiniteLengthRay(start, end)
    aaa.start = [3, 3, 3]
    assert aaa.start == [3, 3, 3]
    with pytest.raises(ValueError):
        aaa.start = "waldo"
    with pytest.raises(ValueError):
        aaa.start = [3, 3, "waldo"]
    aaa.end = [4, 4, 4]
    assert aaa.end == [4, 4, 4]
    with pytest.raises(ValueError):
        aaa.end = "waldo"
    with pytest.raises(ValueError):
        aaa.end = [4, 4, "waldo"]


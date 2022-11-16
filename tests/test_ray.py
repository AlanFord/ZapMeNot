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
    assert all(aaa._origin == np.array(start))
    assert aaa._length == pytest.approx(math.sqrt(3.))


# test calculaton of ray properties dir, invdir, sign
# reference: hand calculation
def test_ray_unit_vector():
    start = [1, 1, 1]
    end = [2, 2, 2]
    aaa = ray.FiniteLengthRay(start, end)
    part = 1./math.sqrt(3.)
    # the following creates a vector of numerical tests and then
    # checks to ensure they all came back true
    assert all(aaa._origin == [1, 1, 1])
    assert aaa._length == math.sqrt(3.)
    assert all(aaa._dir == np.array([part, part, part]))
    assert all(aaa._invdir == np.array([1/part, 1/part, 1/part]))
    assert all(aaa._sign == np.array([False, False, False]))


# test invalid initializations
def test_ray_error_trapping():
    start = [1, 1, 1, 1]
    end = [2, 2, 2]
    with pytest.raises(ValueError):
        aaa = ray.FiniteLengthRay(start, end)  # start vector too long
    start = [1, 1, 1]
    end = [2, 2, 2, 2]
    with pytest.raises(ValueError):
        aaa = ray.FiniteLengthRay(start, end)  # end vector too long
    start = "start"
    end = [2, 2, 2]
    with pytest.raises(ValueError):
        aaa = ray.FiniteLengthRay(start, end)  # non-numeric start
    start = [1, 1, "start"]
    end = [2, 2, 2]
    with pytest.raises(ValueError):
        aaa = ray.FiniteLengthRay(start, end)  # non-numeric start
    start = [1, 1, 1]
    end = "end"
    with pytest.raises(ValueError):
        aaa = ray.FiniteLengthRay(start, end)  # non-numeric end
    start = [1, 1, 1]
    end = [2, 2, "end"]
    with pytest.raises(ValueError):
        aaa = ray.FiniteLengthRay(start, end)  # non-numeric end


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

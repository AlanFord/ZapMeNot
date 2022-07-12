import math
import numpy as np

import pytest

from zap_me_not import material

pytestmark = pytest.mark.basic

# test response to a bad material name
# reference: none required
def test_a_bad_material_name():
	with pytest.raises(ValueError):
		a = material.Material("wanker")

# test setting a new density
# reference: none required
def test_setDensity():
	a = material.Material("air")
	a.density = 3.14
	assert a.density == 3.14

# test retrieval of the MFP
# reference: tests/reference_calculations/test_material/getattenCoeff.m (matlab script)
def test_getMfp():
	a = material.Material("air")
	b = a.get_mfp(0.66, 10)
	assert b == pytest.approx(0.00092827901)

# test retrieval of a mass attenuation coefficient
# reference: tests/reference_calculations/test_material/getattenCoeff.m (matlab script)
def test_getMassAttenCoff():
	a = material.Material("air")
	# test energy out of range
	with pytest.raises(ValueError):
		b = a.get_mass_atten_coeff(300)
	with pytest.raises(ValueError):
		b = a.get_mass_atten_coeff(0.001)
	# test for a valid return value
	b = a.get_mass_atten_coeff(0.66)
	assert b == pytest.approx(0.077035602)

# test response to a request for non-GP buildup factors
# reference: none required
def test_a_bad_buildupFactorType():
	a = material.Material("air")
	with pytest.raises(ValueError):
		b = a.get_buildup_factor(0.66, 10, "Taylor")

# test calculation of a buildup factor
# reference: tests/reference_calculations/test_material/buildupFactor.m (matlab script)
def test_getBuildupFactor():
	a = material.Material("air")
	b = a.get_buildup_factor(0.66, 0, "GP")
	assert b == 1
	b = a.get_buildup_factor(0.66, 10, "GP")
	assert b == pytest.approx(43.237787)

# test calculation of a list of buildup factors
# reference: tests/reference_calculations/test_material/buildupFactor.m (matlab script)
def test_getBuildupFactor2():
	a = material.Material("air")
	mfp_list = [0, 10]
	b = a.get_buildup_factor(0.66, mfp_list, "GP")
	print(b)
	assert b[0] == 1
	assert b[1] == pytest.approx(43.237787)
	assert len(b) == 2

# test calculation of a list of buildup factors
# reference: tests/reference_calculations/test_material/buildupFactor.m (matlab script)
def test_getBuildupFactor3():
	a = material.Material("air")
	mfp_array = np.array([0, 10])
	# print("mfp_array is\n")
	# print(mfp_array)
	# print(type(mfp_array))
	b = a.get_buildup_factor
	b = a.get_buildup_factor(0.66, mfp_array, "GP")
	assert b[0] == 1
	assert b[1] == pytest.approx(43.237787)
	assert len(b) == 2





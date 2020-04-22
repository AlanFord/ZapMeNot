import math

import pytest

from ZapMeNot import material

pytestmark = pytest.mark.basic

# test response to a bad material name
def test_a_bad_material_name():
	with pytest.raises(ValueError):
		a = material.Material("wanker")

# test setting a new density
def test_setDensity():
	a = material.Material("air")
	a.set_density(3.14)
	assert a.density == 3.14

# test retrieval of the MFP
# reference value taken from matlab script getattenCoeff.m
def test_getMfp():
	a = material.Material("air")
	b = a.get_mfp(0.66, 10)
	assert b == pytest.approx(0.00092827901)

# test retrieval of a mass attenuation coefficient
# reference value taken from matlab script getattenCoeff.m
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
def test_a_bad_buildupFactorType():
	a = material.Material("air")
	with pytest.raises(ValueError):
		b = a.get_buildup_factor(0.66, 10, "Taylor")

# test calculation of a buildup factor
# reference value taken from matlab script buildupFactor.m
def test_getBuildupFactor():
	a = material.Material("air")
	b = a.get_buildup_factor(0.66, 0, "GP")
	assert b == 1
	b = a.get_buildup_factor(0.66, 10, "GP")
	assert b == pytest.approx(43.237787)

# test GP function with K ==1
# def test_GP_function():
# 	mfp = 15
# 	X = mfp/(math.pi/4+2)
# 	assert material.Material.GP(1, 2, 0, 1, X, mfp) == 1





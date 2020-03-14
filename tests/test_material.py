from ZapMeNot import material
import pytest

# test response to a bad material name
def test_a_bad_material_name():
	with pytest.raises(ValueError):
		a = material.Material("wanker")

# test setting a new density
def test_setDensity():
	a = material.Material("air")
	a.setDensity(3.14)
	assert a.density == 3.14

# test retrieval of the MFP
def test_getMfp():
	a = material.Material("air")
	b = a.getMfp(0.66, 10)
	assert b == pytest.approx(9.282790078911769e-04)

# test retrieval of a mass attenuation coefficient
# WARNING: result is based on preliminary test dataset!
# comparison value calculated in Matlab
def test_getMassAttenCoff():
	a = material.Material("air")
	b = a.getMassAttenCoff(0.66)
	assert b == pytest.approx(0.077035602314621)

# test response to a bad material name
def test_a_bad_buildupFactorType():
	a = material.Material("air")
	#cassertRaises(ValueError, a.getBuildupFactor, 0.66, 10, "Taylor")
	with pytest.raises(ValueError):
		b = a.getBuildupFactor(0.66, 10, "Taylor")

# test calculation of a buildup factor
def test_getBuildupFactor():
	a = material.Material("air")
	b = a.getBuildupFactor(0.66, 10, "GP")
	assert b == pytest.approx(43.23778738585646)




import math
import numpy as np

import pytest

from zap_me_not import material

pytestmark = pytest.mark.basic

# test response to a good/bad material name
# reference: none required
def test_material_name():
    a = material.Material("water")  # test a valid name
    assert a._name == "water"
    with pytest.raises(ValueError): 
        a = material.Material("wanker")  # non-existant name
    with pytest.raises(ValueError): 
        a = material.Material(32)  # non-alpha name
    with pytest.raises(ValueError): 
        a = material.Material()  # missing name
    a = material.Material("WATER")  # Upper-case name
    assert a._name == "water"
    a = material.Material("Water")  # Mixed-case name
    assert a._name == "water"

# test setting a new density
# reference: none required
def test_setDensity():
    a = material.Material("air")
    a.density = 3.14
    assert a.density == 3.14
    with pytest.raises(ValueError): 
        a.density = -32  # negative value
    with pytest.raises(ValueError): 
        a.density = "notAnumber"  # negative value

# test retrieval of the MFP
# reference: tests/reference_calculations/test_material/getattenCoeff.m (matlab script)
def test_getMfp():
    a = material.Material("air")
    b = a.get_mfp(0.66, 10)
    assert b == pytest.approx(0.00092827901)
    assert a.get_mfp(0.66, 0) == 0  # zero distance
    with pytest.raises(ValueError): 
        b = a.get_mfp()  # missing values
    with pytest.raises(ValueError): 
        b = a.get_mfp(-0.66, 10)  # negative photon energy
    with pytest.raises(ValueError): 
        b = a.get_mfp(0, 10)  # zero photon energy
    with pytest.raises(ValueError): 
        b = a.get_mfp(0.001, 10)  # out-of-bounds photon energy
    with pytest.raises(ValueError): 
        b = a.get_mfp(100, 10)  # out-of-bounds photon energy
    with pytest.raises(ValueError): 
        b = a.get_mfp("waffle", 10)  # non-numeric energy
    with pytest.raises(ValueError): 
        b = a.get_mfp(0.66, -10)  # negative distance
    with pytest.raises(ValueError): 
        b = a.get_mfp(0.66, "waffle")  # non-numeric distance
    with pytest.raises(ValueError): 
        b = a.get_mfp(0.66)  # missing distance

# test retrieval of a mass attenuation coefficient
# reference: tests/reference_calculations/test_material/getattenCoeff.m (matlab script)
def test_getMassAttenCoff():
    a = material.Material("air")
    # test for a valid return value
    b = a.get_mass_atten_coeff(0.66)
    assert b == pytest.approx(0.077035602)
    # test energy out of range
    with pytest.raises(ValueError):
        b = a.get_mass_atten_coeff(300)
    with pytest.raises(ValueError):
        b = a.get_mass_atten_coeff(0.001)
    with pytest.raises(ValueError):
        b = a.get_mass_atten_coeff(0)
    with pytest.raises(ValueError):
        b = a.get_mass_atten_coeff(-0.001
    # test bad argument
    with pytest.raises(ValueError):
        b = a.get_mass_atten_coeff()
    with pytest.raises(ValueError):
        b = a.get_mass_atten_coeff("waldo")

# test retrieval of a mass energy absorption coefficient
# reference: tests/reference_calculations/test_material/getattenCoeff.m (matlab script)
def test_getMassAttenCoff():
    a = material.Material("air")
    # test for a valid return value
    b = a.get_mass_energy_abs_coeff(0.66)
    assert b == pytest.approx(0.077035602) # this is probably wrong
    # test energy out of range
    with pytest.raises(ValueError):
        b = a.get_mass_energy_abs_coeff(300)
    with pytest.raises(ValueError):
        b = a.get_mass_energy_abs_coeff(0.001)
    with pytest.raises(ValueError):
        b = a.get_mass_energy_abs_coeff(-0.001)
    # test bad argument
    with pytest.raises(ValueError):
        b = a.get_mass_energy_abs_coeff()
    with pytest.raises(ValueError):
        b = a.get_mass_energy_abs_coeff("waldo")

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
    b = a.get_buildup_factor(0.66, 0, "GP")   # zero fmp
    assert b == 1
    b = a.get_buildup_factor(0.66, 10, "GP")  # upper case
    assert b == pytest.approx(43.237787)
    b = a.get_buildup_factor(0.66, 10, "gp")  # lower case
    assert b == pytest.approx(43.237787)
    b = a.get_buildup_factor(0.66, 10, "Gp")  # mixed case
    assert b == pytest.approx(43.237787)
    with pytest.raises(ValueError):
        b = a.get_buildup_factor(-0.66, 10, "GP")  # negative energy
    with pytest.raises(ValueError):
        b = a.get_buildup_factor(0, 10, "GP")  # zero energy
    with pytest.raises(ValueError):
        b = a.get_buildup_factor(0.001, 10, "GP")  # out of bounds energy
    with pytest.raises(ValueError):
        b = a.get_buildup_factor(100, 10, "GP")  # out of bounds energy
    with pytest.raises(ValueError):
        b = a.get_buildup_factor("waldo", 10, "GP")  # non-numeric energy
    with pytest.raises(ValueError):
        b = a.get_buildup_factor(0.66, -10, "GP")  # negative mfp
    with pytest.raises(ValueError):
        b = a.get_buildup_factor(0.66, "waldo", "GP")  # non-numeric mfp
    # test large mfp
    b = a.get_buildup_factor(0.66, 40, "GP")
    c = a.get_buildup_factor(0.66, 100, "GP")
    assert b == c  

# test calculation of a list of buildup factors from a list of mfp
# reference: tests/reference_calculations/test_material/buildupFactor.m (matlab script)
def test_getBuildupFactor2():
    a = material.Material("air")
    mfp_list = [0, 10]
    b = a.get_buildup_factor(0.66, mfp_list, "GP")
    print(b)
    assert b[0] == 1
    assert b[1] == pytest.approx(43.237787)
    assert len(b) == 2

# test calculation of a list of buildup factors from an array of mfp
# reference: tests/reference_calculations/test_material/buildupFactor.m (matlab script)
def test_getBuildupFactor3():
    a = material.Material("air")
    mfp_array = np.array([0, 10])
    b = a.get_buildup_factor
    b = a.get_buildup_factor(0.66, mfp_array, "GP")
    assert b[0] == 1
    assert b[1] == pytest.approx(43.237787)
    assert len(b) == 2





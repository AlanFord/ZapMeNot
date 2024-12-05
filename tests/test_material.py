import numpy as np

import pytest

from zapmenot import material

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
# reference: getattenCoeff.m (matlab script)
def test_getMfp():
    a = material.Material("air")
    b = a.get_mfp(0.66, 10)
    assert b == pytest.approx(0.00092827901)
    assert a.get_mfp(0.66, 0) == 0  # zero distance
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


# test retrieval of a mass attenuation coefficient
# reference: getattenCoeff.m (matlab script)
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
        b = a.get_mass_atten_coeff(-0.001)
    # test bad argument
    with pytest.raises(ValueError):
        b = a.get_mass_atten_coeff("waldo")


# test retrieval of a mass energy absorption coefficient
# reference: getMassEnergyAbsCoeff.m (matlab script)
def test_getMassEnergyAbsCoff():
    a = material.Material("air")
    # test for a valid return value
    b = a.get_mass_energy_abs_coeff(0.66)
    assert b == pytest.approx(0.029292858)
    # test energy out of range
    with pytest.raises(ValueError):
        b = a.get_mass_energy_abs_coeff(300)
    with pytest.raises(ValueError):
        b = a.get_mass_energy_abs_coeff(0.001)
    with pytest.raises(ValueError):
        b = a.get_mass_energy_abs_coeff(-0.001)
    # test bad argument
    with pytest.raises(ValueError):
        b = a.get_mass_energy_abs_coeff("waldo")


# test response to a request for non-GP buildup factors
# reference: none required
def test_a_bad_buildupFactorType():
    a = material.Material("air")
    with pytest.raises(ValueError):
        a.get_buildup_factor(0.66, 10, "Taylor")


# test response to a request for non-existant buildup factor
# reference: none required
def test_a_bad_buildupFactorMaterial():
    a = material.Material("actinium")
    with pytest.raises(ValueError):
        a.get_buildup_factor(0.66, 10)


# test calculation of a buildup factor
# reference: buildupFactor.m (matlab script)
def test_getBuildupFactor():
    a = material.Material("air")
    b = a.get_buildup_factor(0.66, 0, "GP")   # zero fmp
    assert b == 1
    b = a.get_buildup_factor(0.66, 10, "GP")  # upper case
    assert b == pytest.approx(43.082281)
    b = a.get_buildup_factor(0.66, 10, "gp")  # lower case
    assert b == pytest.approx(43.082281)
    b = a.get_buildup_factor(0.66, 10, "Gp")  # mixed case
    assert b == pytest.approx(43.082281)
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
    b = a.get_buildup_factor(0.66, 80, "GP")
    c = a.get_buildup_factor(0.66, 100, "GP")
    assert b == c
    # using list of mfps
    d = a.get_buildup_factor(0.66, [10, 10], "GP")
    assert d == pytest.approx([43.082281, 43.082281])


# test extrapolation of buildup factor at mfp > 40
# reference: getExtrapolation.m (matlab script)
def test_getExtrapolation():
    a = material.Material("iron")
    # test extrapolation beyond 40 mfp
    mfparray = np.array([1, 5, 10, 15, 20, 25, 30, 35, 39.9, 40.1,
                        45, 50, 55, 60, 70, 80, 81, 90])
    b = a.get_buildup_factor(2.9, mfparray, "GP")
    matlab_results = [1.634959486477451e+00, 4.526308321088647e+00,
                      8.889077334592749e+00, 1.404816369892699e+01,
                      1.981684391478164e+01, 2.587973642592209e+01,
                      3.213781756702232e+01, 3.884293656055805e+01,
                      4.611990148155270e+01, 4.643028694137963e+01,
                      5.418236914723725e+01, 6.255812904859600e+01,
                      7.140377705332367e+01, 8.071996133878288e+01,
                      1.007700183794541e+02, 1.227255609369946e+02,
                      1.227255609369946e+02, 1.227255609369946e+02]
    assert b == pytest.approx(matlab_results)


# test extrapolation of buildup factor for air at a point where an
# earlier buildup factor extrapolation method failed
# see https://github.com/AlanFord/ZapMeNot/issues/23
# reference: getAirExtrapolation.m (matlab script)
def test_getExtrapolation2():
    a = material.Material("air")
    # test extrapolation beyond 40 mfp
    b = a.get_buildup_factor(0.033865, 45, "GP")
    matlab_result = 8.449318679685693e+01          
    assert b == pytest.approx(matlab_result)


# test calculation of a list of buildup factors from a list of mfp
# reference: buildupFactor.m (matlab script)
def test_getBuildupFactor2():
    a = material.Material("air")
    mfp_list = [0, 10]
    b = a.get_buildup_factor(0.66, mfp_list, "GP")
    assert b[0] == 1
    assert b[1] == pytest.approx(43.082281)
    assert len(b) == 2


# test calculation of a list of buildup factors from an array of mfp
# reference: buildupFactor.m (matlab script)
def test_getBuildupFactor3():
    a = material.Material("air")
    mfp_array = np.array([0, 10])
    b = a.get_buildup_factor
    b = a.get_buildup_factor(0.66, mfp_array, "GP")
    assert b[0] == 1
    assert b[1] == pytest.approx(43.082281)
    assert len(b) == 2

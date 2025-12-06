import math

import pytest
import numpy as np
import pandas as pd

from zapmenot import model, source, shield, detector, material

pytestmark = pytest.mark.basic


# =============================================================
class TestPointSource():

    # point source with no shielding
    # Reference: dose calculated from Principles of Radiation Shielding,
    #     A. B. Chilton, J. K. Shultis, R. E. Faw
    def test_Case0(self):
        myModel = model.Model()
        mySource = source.PointSource(0, 0, 0)
        photonEnergy = 1.0  # MeV
        photonIntensity = 3E10  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(100, 0, 0))
        result = myModel.calculate_exposure()
        photonFlux = photonIntensity/(4*math.pi*100**2)  # photons/sec/cm2
        responseFunction = 1.835E-8*1.0*2.787E-02
        analyticalDose = photonFlux*responseFunction  # R/sec
        # the "other code" gives 440.1 mR/hr at an air density of 1e-12g/cc
        # convert from R/sec to mR/hr
        assert result == pytest.approx(analyticalDose*1000*3600)

    # a point source with infinite yz shields
    # Reference:
    # tests/reference_calculations/test_model/test_Case1.m (matlab script)
    def test_Case1(self):
        myModel = model.Model()
        mySource = source.PointSource(0, 0, 0)
        mySource.add_photon(1.0, 3e10)
        myModel.add_source(mySource)
        myModel.add_shield(shield.SemiInfiniteXSlab(material_name="iron",
                           x_start=10, x_end=20))
        myModel.add_shield(shield.SemiInfiniteXSlab(material_name="concrete",
                           x_start=30, x_end=40))
        myModel.add_detector(detector.Detector(100, 0, 0))
        myModel.set_buildup_factor_material(material.Material('iron'))
        result = myModel.calculate_exposure()
        assert result == pytest.approx(
            2.218926692201381e-06*1000*3600)  # convert from R/sec to mR/hr

    # a point source (single photon) with a single infinite yz shield
    # Reference:
    # tests/reference_calculations/test_model/test_Case2.m (matlab script)
    def test_Case2(self):
        myModel = model.Model()
        mySource = source.PointSource(0, 0, 0)
        mySource.add_photon(1.0, 3e10)
        myModel.add_source(mySource)
        myModel.add_shield(shield.SemiInfiniteXSlab(material_name="iron",
                           x_start=10, x_end=20))
        myModel.add_detector(detector.Detector(100, 0, 0))
        myModel.set_buildup_factor_material(material.Material('iron'))
        result = myModel.calculate_exposure()
        assert result == pytest.approx(
            7.057332942044014e-06*1000*3600)  # convert from R/sec to mR/hr

    # a point source (multiple photons) with two separate infinite yz shields,
    #   on-axis source/detector
    # Reference:
    # tests/reference_calculations/test_model/test_Case3.m (matlab script)
    def test_Case3(self):
        myModel = model.Model()
        mySource = source.PointSource(0, 0, 0)
        mySource.add_isotope_bq('Ar-41', 3e10)
        myModel.add_source(mySource)
        myModel.add_shield(shield.SemiInfiniteXSlab(material_name="iron",
                           x_start=10, x_end=20))
        myModel.add_shield(shield.SemiInfiniteXSlab(material_name="concrete",
                           x_start=30, x_end=40))
        myModel.add_detector(detector.Detector(100, 0, 0))
        myModel.set_buildup_factor_material(material.Material('iron'))
        result = myModel.calculate_exposure()
        assert result == pytest.approx(
            4.417449715326903e-06*1000*3600)  # convert from R/sec to mR/hr

    # a point source (multiple photons) with two separate infinite yz shields,
    #   off-axis source/detector
    # Reference:
    # tests/reference_calculations/test_model/test_Case4.m (matlab script)
    def test_Case4(self):
        myModel = model.Model()
        mySource = source.PointSource(1, 2, 3)
        mySource.add_isotope_curies('Co-60', 3)
        myModel.add_source(mySource)
        myModel.add_shield(shield.SemiInfiniteXSlab(material_name="iron",
                           x_start=10, x_end=20))
        myModel.add_shield(shield.SemiInfiniteXSlab(material_name="concrete",
                           x_start=30, x_end=40))
        myModel.add_detector(detector.Detector(80, 90, 100))
        myModel.set_buildup_factor_material(material.Material('iron'))
        result = myModel.calculate_exposure()
        assert result == pytest.approx(
            1.699537209509012e-07*1000*3600)  # convert from R/sec to mR/hr

    # a point source (no photons) with two separate infinite yz shields,
    #   off-axis source/detector
    def test_Case5(self):
        myModel = model.Model()
        mySource = source.PointSource(1, 2, 3)
        mySource.add_isotope_curies('Sr-90', 3)
        myModel.add_source(mySource)
        myModel.add_shield(shield.SemiInfiniteXSlab(material_name="iron",
                           x_start=10, x_end=20))
        myModel.add_shield(shield.SemiInfiniteXSlab(material_name="concrete",
                           x_start=30, x_end=40))
        myModel.add_detector(detector.Detector(80, 90, 100))
        myModel.set_buildup_factor_material(material.Material('iron'))
        result = myModel.calculate_exposure()
        assert result == 0

    # a point source coincident with a detector
    def test_Case6(self):
        myModel = model.Model()
        mySource = source.PointSource(1, 2, 3)
        mySource.add_isotope_curies('Co-60', 3)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(1, 2, 3))
        with pytest.raises(ValueError):
            myModel.calculate_exposure()


# =============================================================
class TestLineSource():

    # line source with no shielding
    # reference dose calculated from Principles of Radiation Shielding,
    #   A. B. Chilton, J. K. Shultis, R. E. Faw
    # from the reference, pages 132, 157, and 159, th dose rate is 64.66 mR/hr
    # Microshield gives 64.74 mR/hr at an air density of 1e-12g/cc
    def test_Case0(self):
        myModel = model.Model()
        mySource = source.LineSource([0, 0, 0], [0, 0, 1000])
        mySource.points_per_dimension = [100, 1, 1]
        photonEnergy = 1.0  # MeV
        photonIntensity = 3E10  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(100, 0, 0))
        result = myModel.calculate_exposure()
        linearPhotonSource = photonIntensity/1000
        photonFlux = linearPhotonSource / \
            100*math.atan(1000/100)  # photons/sec/cm2
        responseFunction = 1.835E-8*1.0*2.787E-02/4/math.pi
        analyticalDose = photonFlux*responseFunction  # R/sec
        assert result == pytest.approx(
            analyticalDose*1000*3600)  # convert from R/sec to mR/hr


# =============================================================
class TestSphericalSource():

    # spherical source with no shielding
    # air density of 1E-10 g/cm3, similating void
    # 10 cm radius with radial and angular quadratures of 10
    # dose point is 20 cm from sphere origin
    # sphere center located at coordinates [4, 5, 6], so
    #   dose point is at [4, 5, 26] for dose point on the Z axis
    #   and [24, 5, 6] for dose point on the X axis
    # Source is 1 Bq of 1 MeV photons
    #
    # Microshield dose (unknown quadrature method) result is 3.875e-07 mR/hr.
    # Matlab dose result is 3.868745387518610e-07 mR/hr (see testSphereDose1.m).
    def test_Case0(self):
        myModel = model.Model()
        mySource = source.SphereSource("air", sphere_radius=10,
                                       sphere_center=[4, 5, 6], density=0)
        mySource.points_per_dimension = [10, 10, 10]
        photonEnergy = 1.0  # MeV
        photonIntensity = 1  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(4, 5, 26))
        result = myModel.calculate_exposure()
        assert result == pytest.approx(3.868745387518610e-07)


# =============================================================
class TestZAlignedCylinderSource():

    # line source with no shielding
    # reference dose calculated from Principles of Radiation Shielding,
    #   A. B. Chilton, J. K. Shultis, R. E. Faw
    # from the reference, pages 132, 157, and 159, the dose rate is 271.8 mR/hr
    # Microshield gives 271.8 mR/hr at an air density of 1e-12g/cc
    def test_Case0(self):
        myModel = model.Model()
        mySource = source.ZAlignedCylinderSource(
            material_name='air',
            cylinder_center=[0, 0, 500], cylinder_length=1000,
            cylinder_radius=50, density=1e-12)
        mySource.points_per_dimension = [40, 20, 400]
        photonEnergy = 1.0  # MeV
        photonIntensity = 3E10  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(0, 0, 1000.01))
        result = myModel.calculate_exposure()
        assert result == pytest.approx(271.628)


def test_filler_material():
    myModel = model.Model()
    myModel.set_filler_material("air", 0.1)
    assert myModel.filler_material.name == "air"
    assert myModel.filler_material.density == 0.1
    myModel.set_filler_material("air", 0)
    assert myModel.filler_material.name == "air"
    assert myModel.filler_material.density == 0  # zero density
    myModel.set_filler_material("air")
    assert myModel.filler_material.density == 0.001205
    with pytest.raises(ValueError):
        myModel.set_filler_material("smush")  # invalid material name
    with pytest.raises(ValueError):
        myModel.set_filler_material(0.3)  # missing material name
    with pytest.raises(ValueError):
        myModel.set_filler_material("air", "void")  # non-numeric density
    with pytest.raises(ValueError):
        myModel.set_filler_material("air", -0.4)  # negative density


def test_add_source():
    myModel = model.Model()
    with pytest.raises(ValueError):
        mySource = []
        myModel.add_source(mySource)  # invalid source


def test_add_shield():
    myModel = model.Model()
    with pytest.raises(ValueError):
        myShield = []
        myModel.add_shield(myShield)  # invalid shield


def test_add_detector():
    myModel = model.Model()
    with pytest.raises(ValueError):
        myDetector = model.Model()
        myModel.add_detector(myDetector)  # invalid detector


def test_set_buildup_material():
    myModel = model.Model()
    with pytest.raises(ValueError):
        myMaterial = []
        myModel.set_buildup_factor_material(myMaterial)  # invalid material


def test_bad_model():
    myModel = model.Model()
    myModel.add_detector(detector.Detector(100, 0, 0))
    myModel.set_buildup_factor_material(material.Material('iron'))
    with pytest.raises(ValueError):
        myModel.calculate_exposure()  # missing source


def test_bad_model2():
    myModel = model.Model()
    mySource = source.PointSource(0, 0, 0)
    mySource.add_photon(1.0, 3e10)
    myModel.add_source(mySource)
    myModel.set_buildup_factor_material(material.Material('iron'))
    with pytest.raises(ValueError):
        myModel.calculate_exposure()  # missing detector


# a point source (multiple photons) with two separate infinite yz shields,
#   on-axis source/detector
# Reference:
# tests/reference_calculations/test_model/test_Case3.m (matlab script)
def test_generate_summary():
    myModel = model.Model()
    mySource = source.PointSource(0, 0, 0)
    mySource.add_isotope_bq('Ar-41', 3e10)
    myModel.add_source(mySource)
    myModel.add_shield(shield.SemiInfiniteXSlab(material_name="iron",
                       x_start=10, x_end=20))
    myModel.add_shield(shield.SemiInfiniteXSlab(material_name="concrete",
                       x_start=30, x_end=40))
    myModel.add_detector(detector.Detector(100, 0, 0))
    myModel.set_buildup_factor_material(material.Material('iron'))
    result = myModel.calculate_exposure()
    assert result == pytest.approx(
        4.417449715326903e-06*1000*3600)  # convert from R/sec to mR/hr
    expected_summary = [[1.29364, 29748000000, 1371.11990617,
                         6.61910474907e-07*1000*3600,
                         4.41321334734e-06*1000*3600],
                        [1.677, 15468960, 1.76805726932,
                         7.99508312077e-10*1000*3600,
                         4.2363679878e-09*1000*3600]]
    summary = myModel.generate_summary()
    np.testing.assert_allclose(expected_summary, summary)
    df = pd.DataFrame(summary, columns=[
        'MeV', 'photons/sec', 'Uncollided MeV/cm2/sec',
        'Uncollided mR/hr', 'Collided mR/hr'])
    print("")
    print(df)


# a point source with infinite yz shields
# Reference:
# tests/reference_calculations/test_model/test_Case1.m (matlab script)
def test_generate_summary_single_photon():
    myModel = model.Model()
    mySource = source.PointSource(0, 0, 0)
    mySource.add_photon(1.0, 3e10)
    myModel.add_source(mySource)
    myModel.add_shield(shield.SemiInfiniteXSlab(material_name="iron",
                                                x_start=10, x_end=20))
    myModel.add_shield(shield.SemiInfiniteXSlab(material_name="concrete",
                       x_start=30, x_end=40))
    myModel.add_detector(detector.Detector(100, 0, 0))
    myModel.set_buildup_factor_material(material.Material('iron'))
    result = myModel.calculate_exposure()
    assert result == pytest.approx(
        2.218926692201380e-06*1000*3600)  # convert from R/sec to mR/hr
    # the summary should generate a list containing one list of the following:
    # energy (MeV), photon emission rate (photons/sec),
    # uncollided energy flux (MeV/sec), uncollided exposure (mR/hr),
    #   and total exposure (mR/hr)
    expected_summary = [[1.0, 3.0E10, 5.066988280960838e+02,
                         2.591331278213446e-07*1000*3600,
                         2.218926692201381e-06*1000*3600]]
    summary = myModel.generate_summary()
    np.testing.assert_allclose(expected_summary, summary)


def test_generate_summary_no_photon():
    myModel = model.Model()
    mySource = source.PointSource(0, 0, 0)
    mySource.add_isotope_curies('Sr-90', 3)
    myModel.add_source(mySource)
    myModel.add_detector(detector.Detector(100, 0, 0))
    result = myModel.calculate_exposure()
    assert result == pytest.approx(0)  # convert from R/sec to mR/hr
    expected_summary = []
    summary = myModel.generate_summary()
    np.testing.assert_allclose(expected_summary, summary)


def test_replaceable_source():
    # spherical source with no shielding
    # air density of 1E-10 g/cm3, similating void
    # 10 cm radius with radial and angular quadratures of 10
    # dose point is 20 cm from sphere origin
    # sphere center located at coordinates [4, 5, 6], so
    #   dose point is at [4, 5, 26] for dose point on the Z axis
    #   and [24, 5, 6] for dose point on the X axis
    # Source is 1 Bq of 1 MeV photons
    #
    # build a model with a source that will be replaced
    myModel = model.Model()
    myModel.add_detector(detector.Detector(4, 5, 26))
    # create the first source that will be replaced
    mySource = source.SphereSource("air", sphere_radius=15,
                                    sphere_center=[4, 5, 6], density=0)
    mySource.points_per_dimension = [10, 10, 10]
    photonEnergy = 1.0  # MeV
    photonIntensity = 1  # photons/sec
    mySource.add_photon(photonEnergy, photonIntensity)
    myModel.add_source(mySource)
    result = myModel.calculate_exposure()

    # replace the source with a new source
    # Microshield dose (unknown quadrature method) result is 3.875e-07 mR/hr.
    # Matlab dose result is 3.868745387518610e-07 mR/hr (see testSphereDose1.m).
    mySource = source.SphereSource("air", sphere_radius=10,
                                    sphere_center=[4, 5, 6], density=0)
    mySource.points_per_dimension = [10, 10, 10]
    photonEnergy = 1.0  # MeV
    photonIntensity = 1  # photons/sec
    mySource.add_photon(photonEnergy, photonIntensity)
    myModel.add_source(mySource)
    result = myModel.calculate_exposure()
    assert result == pytest.approx(3.868745387518610e-07)

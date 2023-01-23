import math

import pytest

from zapmenot import model, source, shield, detector, material

pytestmark = pytest.mark.benchmark


# ===================================================
# Summary:
# source composition:
# co-58:   22.5 uCi
# co-60:   32.4 uCi
# cs-137:  150 uCi
# mn-54:   12.5 uCi
# sb-125:  11.3 uCi
# Shields include a cylindrical steel shield with and
# inner radius of 3 ft and a thickness of 3 inches as
# well as a concrete shield with an inner radius of 
# 4 ft and a thickness of 18 inches.  The dose point is
# 14 ft from the source location.
# The buildup material is concrete.
def test_benchmark_synth():
    my_model = model.Model()
    my_source = source.PointSource(0, 0, 0)
    my_source.add_isotope_curies('Co-58', 22.5e-6)
    my_source.add_isotope_curies('Co-60', 32.4e-6)
    my_source.add_isotope_curies('Cs-137', 150.e-6)
    my_source.add_isotope_curies('Mn-54', 12.5e-6)
    my_source.add_isotope_curies('Sb-125', 11.3e-6)
    # my_source.add_isotope_curies('Te-125m',1.0765e+000)
    my_source.include_key_progeny = True
    my_model.add_source(my_source)
    inner_radius = 3 * 12 * 2.54
    outer_radius = inner_radius + (3 * 2.54)
    my_model.add_shield(shield.ZAlignedInfiniteAnnulus("iron",
                        cylinder_center=[0, 0, 0],
                        cylinder_inner_radius=inner_radius,
                        cylinder_outer_radius=outer_radius,
                        density=7.874))
    inner_radius = 4 * 12 * 2.54
    outer_radius = inner_radius + (18 * 2.54)
    my_model.add_shield(shield.ZAlignedInfiniteAnnulus("concrete",
                        cylinder_center=[0, 0, 0],
                        cylinder_inner_radius=inner_radius,
                        cylinder_outer_radius=outer_radius,
                        density=2.34))
    my_model.set_filler_material('air', density=0.00122)
    my_model.set_buildup_factor_material(material.Material('concrete'))
    my_model.add_detector(detector.Detector(426.72, 0, 0))
    result = my_model.calculate_exposure()
    print("")
    print('test_benchmark_SYNTH')
    print("Just outside the concrete shield")
    my_model.add_detector(detector.Detector(167.64, 0, 0))
    result = my_model.calculate_exposure()
    print("At z= 0 cm, dose = ", result, " mR/hr, ")
    my_model.add_detector(detector.Detector(167.64, 0, 6))
    result = my_model.calculate_exposure()
    print("At z= 6 cm, dose = ", result, " mR/hr, ")
    my_model.add_detector(detector.Detector(167.64, 0, 20))
    result = my_model.calculate_exposure()
    print("At z= 20 cm, dose = ", result, " mR/hr, ")
    my_model.add_detector(detector.Detector(167.64, 0, 40))
    result = my_model.calculate_exposure()
    print("At z= 40 cm, dose = ", result, " mR/hr, ")
    my_model.add_detector(detector.Detector(167.64, 0, 60))
    result = my_model.calculate_exposure()
    print("At z= 60 cm, dose = ", result, " mR/hr, ")
    my_model.add_detector(detector.Detector(167.64, 0, 80.7))
    result = my_model.calculate_exposure()
    print("At z= 80.7 cm, dose = ", result, " mR/hr, ")
    #
    print("Just outside the iron shield")
    my_model.set_buildup_factor_material(material.Material('iron'))
    my_model.add_detector(detector.Detector(99.06, 0, 0))
    result = my_model.calculate_exposure()
    print("At z= 0 cm, dose = ", result, " mR/hr, ")
    my_model.add_detector(detector.Detector(99.06, 0, 6))
    result = my_model.calculate_exposure()
    print("At z= 6 cm, dose = ", result, " mR/hr, ")
    my_model.add_detector(detector.Detector(99.06, 0, 20))
    result = my_model.calculate_exposure()
    print("At z= 20 cm, dose = ", result, " mR/hr, ")
    my_model.add_detector(detector.Detector(99.06, 0, 40))
    result = my_model.calculate_exposure()
    print("At z= 40 cm, dose = ", result, " mR/hr, ")
    my_model.add_detector(detector.Detector(99.06, 0, 60))
    result = my_model.calculate_exposure()
    print("At z= 60 cm, dose = ", result, " mR/hr, ")
    my_model.add_detector(detector.Detector(99.06, 0, 80.7))
    result = my_model.calculate_exposure()
    print("At z= 80.7 cm, dose = ", result, " mR/hr, ")

    assert True

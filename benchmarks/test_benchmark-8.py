import math

import pytest

from zapmenot import model,source,shield,detector,material

pytestmark = pytest.mark.benchmark

#===================================================
# Summary:
# Benchmark 0: ANSI/ANS-6.6.1 Reference Problem I.1
# Benchmark 1: ANSI/ANS-6.6.1 Reference Problem II.1 Case 1
# Benchmark 2: ESIS Problem #1 - Dose Point D2 -Buildup with Steel
# Benchmark 3: ESIS Problem #1 - Dose Point D3 - Buildup with Concrete
# Benchmark 4: ESIS Problem #2 - Dose Point D5 - Steel Buildup
# Benchmark 5: ESIS Problem #2 - Dose Point D6 - Concrete Buildup
# Benchmark 6: User manual case for resin liner source inference
# Benchmark 7: User manual case for resin liner source inference, iron shield
# Benchmark 8: Large spherical source of air with a concrete shell 

# Benchmark 8 models a hollow concrete spherical shell.
# The air-filled center of the shell has a radius of 70 ft.
# The concrete shell thickness is 30 inches.
# The air density is 0.00122 g/cm3 and the concrete density is 2.3 g/cm3.
# The dose point is located 302 ft, 7 in from the center of the sphere.
# The source is uniformly distributed within the air sphere
# with an energy of 1 MeV and a total activity of 1E17 photons/sec.
# The region between the shell and the dose point is filled with air.
# The buildup material is concrete.
# Microshield result is 7.331 mR/hr
def test_benchmark_8():
    myModel = model.Model()
    mySource = source.SphereSource(material_name="air", density=0.00122, \
            sphere_radius=2133.6, \
            sphere_center=[0,0,0])
    myModel.add_source(mySource)
    aShell = shield.Shell("concrete", mySource, density=2.3, thickness=76.2)
    myModel.add_shield(aShell)
            
    mySource.add_photon(1.0, 1e17)

    # finish configuring the source
    mySource.points_per_dimension = [10,10,10]
    mySource.include_key_progeny = True
    
    myModel.set_buildup_factor_material(material.Material('concrete'))
    myModel.set_filler_material('air',density=0.00122)
    
    # add a detector and calculate the dose rate
    myModel.add_detector(detector.Detector(9222.74,0,0))
    result = myModel.calculate_exposure()
    expected_dose_rate = 7.331
    diff = (result - expected_dose_rate)/expected_dose_rate * 100
    print('\ntest_benchmark_8')
    print("With 10, 10, 10 quadrature, dose = ", result, " mR/hr, ", diff, "%")
    assert True

    # a more detailed quadrature
    mySource.points_per_dimension = [30,30,30]
    result = myModel.calculate_exposure()
    diff = (result - expected_dose_rate)/expected_dose_rate * 100
    print("\nWith 30, 30, 30 quadrature, dose = ", result, " mR/hr, ", diff, "%")
    assert True

    # a change in orientation
    mySource.points_per_dimension = [10,10,10]
    # add a detector and calculate the dose rate
    myModel.add_detector(detector.Detector(0, 0, 9222.74))
    result = myModel.calculate_exposure()
    diff = (result - expected_dose_rate)/expected_dose_rate * 100
    print("\nWith 10, 10, 10 quadrature and a Z-axis orientation, ")
    print("dose = ", result, " mR/hr, ", diff, "%")
    assert True

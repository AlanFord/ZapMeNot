import pytest

from zapmenot import model, source, shield, detector, material

pytestmark = pytest.mark.basic


def test_lead_buildup_factor():

    # test for issue #14
    sample_sink = model.Model()

    a_source = source.PointSource(x=0, y=0, z=0)
    a_source.add_isotope_curies('Tc-99', 2.1)
    # a_source.add_isotope_curies('Cs-137', 0.3)
    print(a_source.get_photon_source_list())

    sample_sink.add_source(a_source)

    exposure_detector = detector.Detector(x=200, y=40, z=40)
    sample_sink.add_detector(exposure_detector)

    first_shield = shield.SemiInfiniteXSlab('lead', x_start=12, x_end=32.1)
    sample_sink.add_shield(first_shield)

    second_shield = shield.SemiInfiniteXSlab('iron', x_start=32.1, x_end=33.1)
    sample_sink.add_shield(second_shield)

    buildup_factor_material = material.Material('lead')
    sample_sink.set_buildup_factor_material(buildup_factor_material)

    sample_sink.set_filler_material('air')

    exposure = sample_sink.calculate_exposure()
    print('The exposure is ', exposure, ' mR/hr')

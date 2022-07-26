import pytest
import numpy as np

from zap_me_not import source

pytestmark = pytest.mark.basic


class TestPointSource():

    # test set/retrieve of isotopes in Curies
    # reference: manual calculation
    def test_addIsotopeCuries(self):
        my_source = source.PointSource(1,2,3)
        my_source.add_isotope_curies('Co-60',3.14)
        my_source.add_isotope_curies('Cu-11',8)
        my_list = [('Co-60',3.14*3.7E10), ('Cu-11', 8*3.7E10)]
        assert my_list == my_source.list_isotopes()


    # test set/retrieve of isotopes in Bq
    # reference: manual calculation
    def test_addIsotopeBq(self):
        my_source = source.PointSource(1,2,3)
        my_source.add_isotope_bq('Co-60',3.14E9)
        my_source.add_isotope_bq('Cs-137',1E6)
        my_list = [('Co-60',3.14E9), ('Cs-137',1E6)]
        assert my_list == my_source.list_isotopes()

    # test addition of key progeny
    # reference: manual calculation
    def test_addIsotopeBq(self):
        my_source = source.PointSource(1,2,3)
        my_source.add_isotope_bq('Co-60',3.14E9)
        my_source.add_isotope_bq('Cs-137',1E6)
        my_source.include_key_progeny = True
        my_list = [('Co-60',3.14E9), ('Cs-137',1E6)]
        assert my_list == my_source.list_isotopes()


    # test set/retrieve of Photons
    # reference: manual calculation
    def test_addPhoton(self):
        my_source = source.PointSource(1,2,3)
        my_source.add_photon(0.9876,3.14E2)
        my_source.add_photon(0.02,5)
        my_list = [(0.9876,3.14E2),(0.02,5)]
        assert my_list == my_source.list_discrete_photons()

    # test retrieval of photon energies/intensities from photon library
    # reference: manual calculation and isotope library
    def test_getPhotonEnergyList(self):
        my_source = source.PointSource(1,2,3)
        my_source.add_isotope_curies('Ar-41',3.14)
        my_source.add_isotope_bq('Br-80m',1E6)
        my_source.add_photon(0.9876,3.14E2)
        a = my_source._get_photon_source_list()
        np.testing.assert_allclose(a, \
            [(0.037052, (3.90540e-01)*1e6), \
             (0.04885, (3.26673e-03)*1e6), \
             (0.9876, 3.14E2), \
             (1.29364, 9.91600e-01 * 3.7e10 * 3.14), \
             (1.677, 5.15632e-04 * 3.7e10 * 3.14)])

    # test retrieval of photon energies/intensities from photon library
    # reference: manual calculation and isotope library
    def test_getProgenyPhotonEnergyList(self):
        my_source = source.PointSource(1,2,3)
        my_source.add_isotope_curies('Sr-90',3.14)
        my_source.add_isotope_bq('Br-80m',1E6)
        my_source.add_photon(0.9876,3.14E2)
        my_source.include_key_progeny = True
        a = my_source._get_photon_source_list()
        np.testing.assert_allclose(a, \
            [(1.56498e-02, 2.15532e-05 * 3.7e10 * 3.14), \
             (1.57372e-02, 4.12457e-05 * 3.7e10 * 3.14), \
             (1.76171e-02, 3.25276e-06 * 3.7e10 * 3.14), \
             (1.76312e-02, 6.33401e-06 * 3.7e10 * 3.14), \
             (1.77689e-02, 1.35593e-08 * 3.7e10 * 3.14), \
             (1.77715e-02, 1.92601e-08 * 3.7e10 * 3.14), \
             (1.79234e-02, 5.32648e-07 * 3.7e10 * 3.14), \
             (1.79252e-02, 1.02298e-06 * 3.7e10 * 3.14), \
             (1.79553e-02, 1.91513e-10 * 3.7e10 * 3.14), \
             (1.79555e-02, 2.70221e-10 * 3.7e10 * 3.14), \
             (0.037052, (3.90540e-01)*1e6), \
             (0.04885, (3.26673e-03)*1e6), \
             (0.9876, 3.14E2), \
             (2.18624e+00, 1.40000e-08 * 3.7e10 * 3.14)])

    # test binning of large photon sets
    def test_binSources(self):
        my_source = source.PointSource(1,2,3)
        my_source.add_isotope_bq('Ac-223',1) # A whole lot'a photons
        a = my_source._get_photon_source_list()
        # print(a)

        
    # test binning of large photon sets
    def test_binOptions(self):
        my_source = source.PointSource(1,2,3)
        my_source.grouping = "discrete"
        assert my_source.grouping == source.GroupOption.DISCRETE
        my_source.grouping = "group"
        assert my_source.grouping == source.GroupOption.GROUP
        my_source.grouping = "hybrid"
        assert my_source.grouping == source.GroupOption.HYBRID


    # test set/retrieval of source points
    # reference: manual calculation
    def test_getSourcePoints(self):
        my_source = source.PointSource(1,2,3)
        np.testing.assert_allclose(my_source._get_source_points(), \
            [(1,2,3)])

#=============================================================

class TestLineSource():

    # test set/retrieve of isotopes in Curies
    # reference: manual calculation
    def test_addIsotopeCuries(self):
        my_source = source.LineSource([1,2,3], [11,12,13])
        my_source.add_isotope_curies('Co-60',3.14)
        my_source.add_isotope_curies('Cu-11',8)
        my_list = [('Co-60',3.14*3.7E10), ('Cu-11', 8*3.7E10)]
        assert my_list == my_source.list_isotopes()


    # test set/retrieve of isotopes in Bq
    # reference: manual calculation
    def test_addIsotopeBq(self):
        my_source = source.LineSource([1,2,3], [11,12,13])
        my_source.add_isotope_bq('Co-60',3.14E9)
        my_source.add_isotope_bq('Cs-137',1E6)
        my_list = [('Co-60',3.14E9), ('Cs-137',1E6)]
        assert my_list == my_source.list_isotopes()

    # test set/retrieve of isotopes in Photons
    # reference: manual calculation
    def test_addPhoton(self):
        my_source = source.LineSource([1,2,3], [11,12,13])
        my_source.add_photon(0.9876,3.14E2)
        my_source.add_photon(0.02,5)
        my_list = [(0.9876,3.14E2),(0.02,5)]
        assert my_list == my_source.list_discrete_photons()

    # test retrieval of photon energies/intensities from photon library
    # reference: manual calculation and isotope library
    def test_getPhotonEnergyList(self):
        my_source = source.LineSource([1,2,3], [11,12,13])
        my_source.add_isotope_curies('Ar-41',3.14)
        my_source.add_isotope_bq('Br-80m',1E6)
        my_source.add_photon(0.9876,3.14E2)
        a = my_source._get_photon_source_list()
        # the following intensities are adjusted for the default 10 
        # intervals in the line source
        np.testing.assert_allclose(a, \
            [(0.037052, (3.90540e-01)*1e6/10), \
             (0.04885, (3.26673e-03)*1e6/10), \
             (0.9876, 3.14E2/10), \
             (1.29364, 9.91600e-01 * 3.7e10 * 3.14 /10), \
             (1.677, 5.15632e-04 * 3.7e10 * 3.14 /10)])

    # test set/retrieval of source points
    # reference: manual calculation
    def test_getSourcePoints(self):
        my_source = source.LineSource([1,2,3], [11,12,13])
        np.testing.assert_allclose(my_source._get_source_points(), \
            [[ 1.5, 2.5, 3.5], \
             [ 2.5, 3.5, 4.5], \
             [ 3.5, 4.5, 5.5], \
             [ 4.5, 5.5, 6.5], \
             [ 5.5, 6.5, 7.5], \
             [ 6.5, 7.5, 8.5], \
             [ 7.5, 8.5, 9.5], \
             [ 8.5, 9.5,10.5], \
             [ 9.5,10.5,11.5], \
             [10.5,11.5,12.5]])

#=============================================================

class TestBoxSource():

    # test source point locations and set/retrieve of photon source energies
    # reference: manual calculation and isotope library
    def test_getSourcePoints(self):
        my_source = source.BoxSource(box_center=[4,5,6],box_dimensions=[10,10,10],material_name='iron')
        my_source.points_per_dimension= [1,1,1]
        np.testing.assert_allclose(my_source._get_source_points(), \
            [(4,5,6)])
        my_source.points_per_dimension= [2,2,2]
        np.testing.assert_allclose(my_source._get_source_points(), \
            [[4-2.5,5-2.5,6-2.5], \
             [4-2.5,5-2.5,6+2.5], \
             [4-2.5,5+2.5,6-2.5], \
             [4-2.5,5+2.5,6+2.5], \
             [4+2.5,5-2.5,6-2.5], \
             [4+2.5,5-2.5,6+2.5], \
             [4+2.5,5+2.5,6-2.5], \
             [4+2.5,5+2.5,6+2.5]])
        my_source.add_isotope_curies('Ar-41',3.14)
        my_source.add_isotope_bq('Br-80m',1E6)
        my_source.add_photon(0.9876,3.14E2)
        a = my_source._get_photon_source_list()
        np.testing.assert_allclose(a, \
            [(0.037052, (3.90540e-01)*1e6/8), \
             (0.04885, (3.26673e-03)*1e6/8), \
             (0.9876, 3.14E2/8), \
             (1.29364, 9.91600e-01 * 3.7e10 * 3.14 /8), \
             (1.677, 5.15632e-04 * 3.7e10 * 3.14 /8)])

#=============================================================

class TestXAlignedCylinderSource():

    def test_getSourcePoints(self):
        pass

#=============================================================

class TestYAlignedCylinderSource():

    def test_getSourcePoints(self):
        pass

#=============================================================

class TestZAlignedCylinderSource():

    # test source point locations and set/retrieve of photon source energies
    # reference: tests/reference_calculations/test_source/cylinder_unit_test.m (matlab script)
    # reference: isotope library
    def test_getSourcePoints(self):
        my_source = source.ZAlignedCylinderSource(cylinder_center=[0,0,0],cylinder_length=10,cylinder_radius=5,material_name='iron')
        my_source.points_per_dimension= [3,3,3]
        sourcePoints = my_source._get_source_points()
        np.testing.assert_allclose(sourcePoints, \
            [[7.2168783649e-01, 1.2500000000e+00, 1.6666666667e+00], \
            [7.2168783649e-01, 1.2500000000e+00, 5], \
            [7.2168783649e-01, 1.2500000000e+00, 8.3333333333e+00], \
            [-1.4433756730e+00, 1.7676253979e-16, 1.6666666667e+00], \
            [-1.4433756730e+00, 1.7676253979e-16, 5], \
            [-1.4433756730e+00, 1.7676253979e-16, 8.3333333333e+00], \
            [7.2168783649e-01, -1.2500000000e+00, 1.6666666667e+00], \
            [7.2168783649e-01, -1.2500000000e+00, 5], \
            [7.2168783649e-01, -1.2500000000e+00, 8.3333333333e+00], \
            [1.7423085626e+00, 3.0177669530e+00, 1.6666666667e+00], \
            [1.7423085626e+00, 3.0177669530e+00, 5], \
            [1.7423085626e+00, 3.0177669530e+00, 8.3333333333e+00], \
            [-3.4846171253e+00, 4.2674252087e-16, 1.6666666667e+00], \
            [-3.4846171253e+00, 4.2674252087e-16, 5], \
            [-3.4846171253e+00, 4.2674252087e-16, 8.3333333333e+00], \
            [1.7423085626e+00, -3.0177669530e+00, 1.6666666667e+00], \
            [1.7423085626e+00, -3.0177669530e+00, 5], \
            [1.7423085626e+00, -3.0177669530e+00, 8.3333333333e+00], \
            [2.2706207262e+00, 3.9328304624e+00, 1.6666666667e+00], \
            [2.2706207262e+00, 3.9328304624e+00, 5], \
            [2.2706207262e+00, 3.9328304624e+00, 8.3333333333e+00], \
            [-4.5412414523e+00, 5.5614168087e-16, 1.6666666667e+00], \
            [-4.5412414523e+00, 5.5614168087e-16, 5], \
            [-4.5412414523e+00, 5.5614168087e-16, 8.3333333333e+00], \
            [2.2706207262e+00, -3.9328304624e+00, 1.6666666667e+00], \
            [2.2706207262e+00, -3.9328304624e+00, 5], \
            [2.2706207262e+00, -3.9328304624e+00, 8.3333333333e+00]])

        my_source.add_isotope_curies('Ar-41',3.14)
        my_source.add_isotope_bq('Br-80m',1E6)
        my_source.add_photon(0.9876,3.14E2)
        a = my_source._get_photon_source_list()
        # the following intensities are adjusted for 3 intervals 
        # intervals in each dimension
        np.testing.assert_allclose(a, \
            [(0.037052, (3.90540e-01)*1e6/27), \
             (0.04885, (3.26673e-03)*1e6/27), \
             (0.9876, 3.14E2/27), \
             (1.29364, 9.91600e-01 * 3.7e10 * 3.14 /27), \
             (1.677, 5.15632e-04 * 3.7e10 * 3.14 /27)])





import pytest
import numpy as np

from zapmenot import source

pytestmark = pytest.mark.basic


class TestGenericSourceFeatures():

    # setup routine for subsequent tests
    @pytest.fixture(scope="function")
    def create_source(self):
        my_source = source.PointSource(1, 2, 3)
        return my_source

    # test set/retrieve of isotopes in Curies
    # reference: manual calculation
    def test_addIsotopeCuries(self, create_source):
        create_source.add_isotope_curies('Co-60', 3.14)
        create_source.add_isotope_curies('Cu-11', 8)
        my_list = [('Co-60', 3.14*3.7E10), ('Cu-11', 8*3.7E10)]
        assert my_list == create_source.list_isotopes()

    # test set/retrieve of isotopes in Bq
    # reference: manual calculation
    def test_addIsotopeBq(self, create_source):
        create_source.add_isotope_bq('Co-60', 3.14E9)
        create_source.add_isotope_bq('Cs-137', 1E6)
        my_list = [('Co-60', 3.14E9), ('Cs-137', 1E6)]
        assert my_list == create_source.list_isotopes()

    # test addition of key progeny
    # reference: manual calculation
    def test_include_key_progeny(self, create_source):
        create_source.add_isotope_bq('Co-60', 3.14E9)
        create_source.add_isotope_bq('Cs-137', 1E6)
        create_source.include_key_progeny = True
        my_list = [('Co-60', 3.14E9), ('Cs-137', 1E6)]
        assert my_list == create_source.list_isotopes()

    # test set/retrieve of Photons
    # reference: manual calculation
    def test_addPhoton(self, create_source):
        create_source.add_photon(0.9876, 3.14E2)
        create_source.add_photon(0.02, 5)
        my_list = [(0.9876, 3.14E2), (0.02, 5)]
        assert my_list == create_source.list_discrete_photons()

    # test retrieval of photon energies/intensities from photon library
    # reference: manual calculation and isotope library
    def test_getPhotonEnergyList(self, create_source):
        create_source.add_isotope_curies('Ar-41', 3.14)
        create_source.add_isotope_bq('Br-80m', 1E6)
        create_source.add_photon(0.9876, 3.14E2)
        a = create_source.get_photon_source_list()
        np.testing.assert_allclose(a,
                                   [(0.037052, (3.90540e-01)*1e6),
                                    (0.04885, (3.26673e-03)*1e6),
                                    (0.9876, 3.14E2),
                                    (1.29364, 9.91600e-01 * 3.7e10 * 3.14),
                                    (1.677, 5.15632e-04 * 3.7e10 * 3.14)])

    # test retrieval of photon energies/intensities from photon library
    # reference: manual calculation and isotope library
    def test_getProgenyPhotonEnergyList(self, create_source):
        create_source.add_isotope_curies('Sr-90', 3.14)
        create_source.add_isotope_bq('Br-80m', 1E6)
        create_source.add_photon(0.9876, 3.14E2)
        create_source.include_key_progeny = True
        a = create_source.get_photon_source_list()
        np.testing.assert_allclose(a,
                                   [(1.56498e-02, 2.15532e-05 * 3.7e10 * 3.14),
                                    (1.57372e-02, 4.12457e-05 * 3.7e10 * 3.14),
                                    (1.76171e-02, 3.25276e-06 * 3.7e10 * 3.14),
                                    (1.76312e-02, 6.33401e-06 * 3.7e10 * 3.14),
                                    (1.77689e-02, 1.35593e-08 * 3.7e10 * 3.14),
                                    (1.77715e-02, 1.92601e-08 * 3.7e10 * 3.14),
                                    (1.79234e-02, 5.32648e-07 * 3.7e10 * 3.14),
                                    (1.79252e-02, 1.02298e-06 * 3.7e10 * 3.14),
                                    (1.79553e-02, 1.91513e-10 * 3.7e10 * 3.14),
                                    (1.79555e-02, 2.70221e-10 * 3.7e10 * 3.14),
                                    (0.037052, (3.90540e-01)*1e6),
                                    (0.04885, (3.26673e-03)*1e6),
                                    (0.9876, 3.14E2),
                                    (2.18624e+00,
                                     1.40000e-08 * 3.7e10 * 3.14)])

    # test binning of large photon sets
    # reference: manual calculation and isotope library
    def test_binSources(self, create_source):
        create_source.add_isotope_bq('Ac-223', 1)  # A whole lot'a photons
        a = create_source.get_photon_source_list()
        np.testing.assert_allclose(a,
                                   [[1.7469949E-02, 1.0045970E-02],
                                    [3.8215385E-02, 5.1480000E-04],
                                    [5.3241176E-02, 5.0490000E-04],
                                    [6.8039216E-02, 5.0490000E-04],
                                    [8.5893078E-02, 3.0383270E-02],
                                    [9.8586524E-02, 1.4786456E-02],
                                    [1.2204762E-01, 2.0790000E-03],
                                    [1.3186667E-01, 2.9700000E-04],
                                    [1.7559231E-01, 1.2870000E-03],
                                    [1.9228919E-01, 7.3260000E-03],
                                    [2.1269063E-01, 6.3360000E-03],
                                    [2.2970000E-01, 6.9300000E-04],
                                    [2.4369063E-01, 3.1680000E-03],
                                    [2.6920000E-01, 9.9000000E-04],
                                    [2.8310976E-01, 4.0590000E-03],
                                    [3.0458571E-01, 2.0790000E-03],
                                    [3.2361667E-01, 5.9400000E-04],
                                    [3.3584375E-01, 1.5840000E-03],
                                    [3.5740000E-01, 1.7820000E-03],
                                    [3.7305455E-01, 2.1780000E-03],
                                    [4.3420000E-01, 5.2470000E-03],
                                    [4.6220000E-01, 3.9600000E-04],
                                    [4.7520000E-01, 2.6730000E-03],
                                    [5.1575000E-01, 1.1880000E-03],
                                    [5.3000000E-01, 2.9700000E-04]])

    # test set/retrieval of photon binning option
    # reference: none needed
    def test_binOptions(self, create_source):
        create_source.grouping = "discrete"
        assert create_source.grouping == source.GroupOption.DISCRETE
        create_source.grouping = "group"
        assert create_source.grouping == source.GroupOption.GROUP
        create_source.grouping = "hybrid"
        assert create_source.grouping == source.GroupOption.HYBRID

    # test binning of small number of photons
    def test_bins(self, create_source):
        create_source.add_isotope_bq('Co-60', 1)
        photons = [[3.47140e-01, 7.50000e-05],
                   [8.26100e-01, 7.60000e-05],
                   [1.17323e+00, 9.98500e-01],
                   [1.33249e+00, 9.99826e-01],
                   [2.15857e+00, 1.20000e-05],
                   [2.50569e+00, 2.00000e-08]]
        create_source.grouping = "discrete"
        np.testing.assert_allclose(create_source.get_photon_source_list(),
                                   photons)
        assert create_source.grouping == source.GroupOption.DISCRETE
        create_source.grouping = "group"
        np.testing.assert_allclose(create_source.get_photon_source_list(),
                                   photons)
        create_source.grouping = "hybrid"
        np.testing.assert_allclose(create_source.get_photon_source_list(),
                                   photons)

# =============================================================


class TestPointSource():

    # setup routine for subsequent tests
    @pytest.fixture(scope="class")
    def create_source(self):
        my_source = source.PointSource(1, 2, 3)
        return my_source

    def test_init(self, create_source):
        assert create_source._x == 1
        assert create_source._y == 2
        assert create_source._z == 3
        assert create_source.points_per_dimension == [1]
        # test attribute of shield class
        assert create_source.material.name == "air"
        # test attribute of source class
        assert create_source._include_key_progeny is False

    # test set/retrieval of source points
    # reference: manual calculation
    def test_getSourcePoints(self, create_source):
        np.testing.assert_allclose(create_source._get_source_points(),
                                   [(1, 2, 3)])

    def test_getSourcePointWeights(self, create_source):
        assert create_source._get_source_point_weights() == [1.0]

    def test_infinite(self, create_source):
        assert create_source.is_infinite() is False

# =============================================================


class TestLineSource():

    # setup routine for subsequent tests
    @pytest.fixture(scope="class")
    def create_source(self):
        my_source = source.LineSource([1, 2, 3], [11, 12, 13])
        my_source.points_per_dimension = 5
        return my_source

    def test_init(self, create_source):
        assert all(create_source.origin == [1, 2, 3])
        assert all(create_source.end == [11, 12, 13])
        assert create_source._length == pytest.approx(10 * np.sqrt(3))
        single = np.sqrt(1./3.)
        assert all(create_source._dir == [single, single, single])
        assert create_source.points_per_dimension == [5]
        # test attribute of shield class
        assert create_source.material.name == "air"
        # test attribute of source class
        assert create_source._include_key_progeny is False

    # test set/retrieval of source points
    # reference: manual calculation
    def test_getSourcePoints(self, create_source):
        np.testing.assert_allclose(create_source._get_source_points(),
                                   [[2, 3, 4],
                                    [4, 5, 6],
                                    [6, 7, 8],
                                    [8, 9, 10],
                                    [10, 11, 12]])

    def test_getSourcePointWeights(self, create_source):
        assert create_source._get_source_point_weights() == [1.0 / 5] * 5

    def test_infinite(self, create_source):
        assert create_source.is_infinite() is False

    def test_points_per_dimension(self, create_source):
        with pytest.raises(ValueError):
            create_source.points_per_dimension = "sunny day"
        with pytest.raises(ValueError):
            create_source.points_per_dimension = 0
        with pytest.raises(ValueError):
            create_source.points_per_dimension = -1
        with pytest.raises(ValueError):
            create_source.points_per_dimension = [4, 3, 1.1]

# =============================================================


class TestBoxSource():

    # setup routine for subsequent tests
    @pytest.fixture(scope="function")
    def create_source(self):
        my_source = source.BoxSource(box_center=[4, 5, 6],
                                     box_dimensions=[10, 10, 10],
                                     material_name='iron', density=1.2)
        return my_source

    def test_init(self, create_source):
        # test attribute of shield class
        assert all(create_source.box_center == [4, 5, 6])
        assert all(create_source.box_dimensions == [10, 10, 10])
        assert create_source.material.name == "iron"
        assert create_source.material.density == 1.2
        # test attribute of source class
        assert create_source._include_key_progeny is False
        assert create_source.points_per_dimension == [10, 10, 10]

    # test source point locations and set/retrieve of photon source energies
    # reference: manual calculation and isotope library
    def test_getSourcePoints(self, create_source):
        create_source.points_per_dimension = [1, 1, 1]
        np.testing.assert_allclose(create_source._get_source_points(),
                                   [(4, 5, 6)])
        create_source.points_per_dimension = [2, 2, 2]
        np.testing.assert_allclose(create_source._get_source_points(),
                                   [[4-2.5, 5-2.5, 6-2.5],
                                    [4-2.5, 5-2.5, 6+2.5],
                                    [4-2.5, 5+2.5, 6-2.5],
                                    [4-2.5, 5+2.5, 6+2.5],
                                    [4+2.5, 5-2.5, 6-2.5],
                                    [4+2.5, 5-2.5, 6+2.5],
                                    [4+2.5, 5+2.5, 6-2.5],
                                    [4+2.5, 5+2.5, 6+2.5]])
        create_source.add_isotope_curies('Ar-41', 3.14)
        create_source.add_isotope_bq('Br-80m', 1E6)
        create_source.add_photon(0.9876, 3.14E2)
        a = create_source.get_photon_source_list()
        np.testing.assert_allclose(a,
                                   [(0.037052, (3.90540e-01) * 1e6),
                                    (0.04885, (3.26673e-03) * 1e6),
                                    (0.9876, 3.14E2),
                                    (1.29364, 9.91600e-01 * 3.7e10 * 3.14),
                                    (1.677, 5.15632e-04 * 3.7e10 * 3.14)])

    def test_getSourcePointWeights(self, create_source):
        the_list = np.array([1.0 / 1000] * 1000)
        np.testing.assert_allclose(create_source._get_source_point_weights(), the_list)

    # test invalid number of entries in source points per dimension
    def test_getSourcePoints2(self, create_source):
        create_source.points_per_dimension = [1, 1]
        with pytest.raises(ValueError):
            create_source._get_source_points()

# =============================================================


class TestXAlignedCylinderSource():

    # setup routine for subsequent tests
    @pytest.fixture(scope="function")
    def create_source(self):
        my_source = source.XAlignedCylinderSource(
            cylinder_center=[-1, 2, 3],
            cylinder_length=10, cylinder_radius=5, material_name='iron',
            density=1.2)
        my_source.points_per_dimension = [3, 3, 3]
        return my_source

    def test_init(self, create_source):
        # test attribute of shield class
        assert create_source.radius == 5
        assert create_source.length == 10
        assert all(create_source.origin == [-6, 2, 3])
        assert all(create_source.end == [4, 2, 3])
        assert all(create_source.dir == [1, 0, 0])
        assert create_source.material.name == "iron"
        assert create_source.material.density == 1.2
        # test attribute of source class
        assert create_source._include_key_progeny is False
        assert create_source.points_per_dimension == [3, 3, 3]

    # test source point locations and set/retrieve of photon source energies
    # reference: cylinder_unit_test.m (matlab script)
    # reference: isotope library
    def test_getSourcePoints(self, create_source):
        sourcePoints = create_source._get_source_points()
        np.testing.assert_allclose(
            sourcePoints,
            [[-4.333333333333333,   3.250000000000000,   2.278312163512968],
             [-1.000000000000000,   3.250000000000000,   2.278312163512968],
             [2.333333333333334,   3.250000000000000,   2.278312163512968],
             [-4.333333333333333,   2.000000000000000,   4.443375672974065],
             [-1.000000000000000,   2.000000000000000,   4.443375672974065],
             [2.333333333333334,   2.000000000000000,   4.443375672974065],
             [-4.333333333333333,   0.750000000000000,   2.278312163512968],
             [-1.000000000000000,   0.750000000000000,   2.278312163512968],
             [2.333333333333334,   0.750000000000000,   2.278312163512968],
             [-4.333333333333333,   5.017766952966369,   1.257691437353310],
             [-1.000000000000000,   5.017766952966369,   1.257691437353310],
             [2.333333333333334,   5.017766952966369,   1.257691437353310],
             [-4.333333333333333,   2.000000000000000,   6.484617125293379],
             [-1.000000000000000,   2.000000000000000,   6.484617125293379],
             [2.333333333333334,   2.000000000000000,   6.484617125293379],
             [-4.333333333333333,  -1.017766952966369,   1.257691437353310],
             [-1.000000000000000,  -1.017766952966369,   1.257691437353310],
             [2.333333333333334,  -1.017766952966369,   1.257691437353310],
             [-4.333333333333333,   5.932830462427466,   0.729379273840342],
             [-1.000000000000000,   5.932830462427466,   0.729379273840342],
             [2.333333333333334,   5.932830462427466,   0.729379273840342],
             [-4.333333333333333,   2.000000000000000,   7.541241452319316],
             [-1.000000000000000,   2.000000000000000,   7.541241452319316],
             [2.333333333333334,   2.000000000000000,   7.541241452319316],
             [-4.333333333333333,  -1.932830462427466,   0.729379273840342],
             [-1.000000000000000,  -1.932830462427466,   0.729379273840342],
             [2.333333333333334,  -1.932830462427466,   0.729379273840342]])

    def test_getSourcePointWeights(self, create_source):
        the_list = np.array([1.0 / 27] * 27)
        np.testing.assert_allclose(create_source._get_source_point_weights(), the_list)

    # test invalid number of entries in source points per dimension
    def test_getSourcePoints2(self, create_source):
        create_source.points_per_dimension = [1, 1]
        with pytest.raises(ValueError):
            create_source._get_source_points()

# =============================================================


class TestYAlignedCylinderSource():

    # setup routine for subsequent tests
    @pytest.fixture(scope="function")
    def create_source(self):
        my_source = source.YAlignedCylinderSource(
            cylinder_center=[-1, 2, 3],
            cylinder_length=10, cylinder_radius=5, material_name='iron',
            density=1.2)
        my_source.points_per_dimension = [3, 3, 3]
        return my_source

    def test_init(self, create_source):
        # test attribute of shield class
        assert create_source.radius == 5
        assert create_source.length == 10
        assert all(create_source.origin == [-1, -3, 3])
        assert all(create_source.end == [-1, 7, 3])
        assert all(create_source.dir == [0, 1, 0])
        assert create_source.material.name == "iron"
        assert create_source.material.density == 1.2
        # test attribute of source class
        assert create_source._include_key_progeny is False
        assert create_source.points_per_dimension == [3, 3, 3]

    # test source point locations and set/retrieve of photon source energies
    # reference: cylinder_unit_test.m (matlab script)
    # reference: isotope library
    def test_getSourcePoints(self, create_source):
        sourcePoints = create_source._get_source_points()
        np.testing.assert_allclose(
            sourcePoints,
            [[-0.278312163512968,  -1.333333333333333,   1.750000000000000],
             [-0.278312163512968,   2.000000000000000,   1.750000000000000],
             [-0.278312163512968,   5.333333333333334,   1.750000000000000],
             [-2.443375672974065,  -1.333333333333333,   3.000000000000000],
             [-2.443375672974065,   2.000000000000000,   3.000000000000000],
             [-2.443375672974065,   5.333333333333334,   3.000000000000000],
             [-0.278312163512968,  -1.333333333333333,   4.250000000000000],
             [-0.278312163512968,   2.000000000000000,   4.250000000000000],
             [-0.278312163512968,   5.333333333333334,   4.250000000000000],
             [0.742308562646690,  -1.333333333333333,  -0.017766952966369],
             [0.742308562646690,   2.000000000000000,  -0.017766952966369],
             [0.742308562646690,   5.333333333333334,  -0.017766952966369],
             [-4.484617125293379,  -1.333333333333333,   3.000000000000000],
             [-4.484617125293379,   2.000000000000000,   3.000000000000000],
             [-4.484617125293379,   5.333333333333334,   3.000000000000000],
             [0.742308562646690,  -1.333333333333333,   6.017766952966369],
             [0.742308562646690,   2.000000000000000,   6.017766952966369],
             [0.742308562646690,   5.333333333333334,   6.017766952966369],
             [1.270620726159658,  -1.333333333333333,  -0.932830462427466],
             [1.270620726159658,   2.000000000000000,  -0.932830462427466],
             [1.270620726159658,   5.333333333333334,  -0.932830462427466],
             [-5.541241452319316,  -1.333333333333333,   3.000000000000000],
             [-5.541241452319316,   2.000000000000000,   3.000000000000000],
             [-5.541241452319316,   5.333333333333334,   3.000000000000000],
             [1.270620726159658,  -1.333333333333333,   6.932830462427466],
             [1.270620726159658,   2.000000000000000,   6.932830462427466],
             [1.270620726159658,   5.333333333333334,   6.932830462427466]])

    def test_getSourcePointWeights(self, create_source):
        the_list = np.array([1.0 / 27] * 27)
        np.testing.assert_allclose(create_source._get_source_point_weights(), the_list)

    # test invalid number of entries in source points per dimension
    def test_getSourcePoints2(self, create_source):
        create_source.points_per_dimension = [1, 1]
        with pytest.raises(ValueError):
            create_source._get_source_points()

# =============================================================


class TestZAlignedCylinderSource():

    # setup routine for subsequent tests
    @pytest.fixture(scope="function")
    def create_source(self):
        my_source = source.ZAlignedCylinderSource(
            cylinder_center=[-1, 2, 3],
            cylinder_length=10, cylinder_radius=5, material_name='iron',
            density=1.2)
        my_source.points_per_dimension = [3, 3, 3]
        return my_source

    def test_init(self, create_source):
        # test attribute of shield class
        assert create_source.radius == 5
        assert create_source.length == 10
        assert all(create_source.origin == [-1, 2, -2])
        assert all(create_source.end == [-1, 2, 8])
        assert all(create_source.dir == [0, 0, 1])
        assert create_source.material.name == "iron"
        assert create_source.material.density == 1.2
        # test attribute of source class
        assert create_source._include_key_progeny is False
        assert create_source.points_per_dimension == [3, 3, 3]

    # test source point locations and set/retrieve of photon source energies
    # reference: cylinder_unit_test.m (matlab script)
    # reference: isotope library
    def test_getSourcePoints(self, create_source):
        sourcePoints = create_source._get_source_points()
        np.testing.assert_allclose(
            sourcePoints,
            [[-0.278312163512968,   3.250000000000000,  -0.333333333333333],
             [-0.278312163512968,   3.250000000000000,   3.000000000000000],
             [-0.278312163512968,   3.250000000000000,   6.333333333333334],
             [-2.443375672974065,   2.000000000000000,  -0.333333333333333],
             [-2.443375672974065,   2.000000000000000,   3.000000000000000],
             [-2.443375672974065,   2.000000000000000,   6.333333333333334],
             [-0.278312163512968,   0.750000000000000,  -0.333333333333333],
             [-0.278312163512968,   0.750000000000000,   3.000000000000000],
             [-0.278312163512968,   0.750000000000000,   6.333333333333334],
             [0.742308562646690,   5.017766952966369,  -0.333333333333333],
             [0.742308562646690,   5.017766952966369,   3.000000000000000],
             [0.742308562646690,   5.017766952966369,   6.333333333333334],
             [-4.484617125293379,   2.000000000000000,  -0.333333333333333],
             [-4.484617125293379,   2.000000000000000,   3.000000000000000],
             [-4.484617125293379,   2.000000000000000,   6.333333333333334],
             [0.742308562646690,  -1.017766952966369,  -0.333333333333333],
             [0.742308562646690,  -1.017766952966369,   3.000000000000000],
             [0.742308562646690,  -1.017766952966369,   6.333333333333334],
             [1.270620726159658,   5.932830462427466,  -0.333333333333333],
             [1.270620726159658,   5.932830462427466,   3.000000000000000],
             [1.270620726159658,   5.932830462427466,   6.333333333333334],
             [-5.541241452319316,   2.000000000000000,  -0.333333333333333],
             [-5.541241452319316,   2.000000000000000,   3.000000000000000],
             [-5.541241452319316,   2.000000000000000,   6.333333333333334],
             [1.270620726159658,  -1.932830462427466,  -0.333333333333333],
             [1.270620726159658,  -1.932830462427466,   3.000000000000000],
             [1.270620726159658,  -1.932830462427466,   6.333333333333334]])

    def test_getSourcePointWeights(self, create_source):
        the_list = np.array([1.0 / 27] * 27)
        np.testing.assert_allclose(create_source._get_source_point_weights(), the_list)

    # test invalid number of entries in source points per dimension
    def test_getSourcePoints2(self, create_source):
        create_source.points_per_dimension = [1, 1]
        with pytest.raises(ValueError):
            create_source._get_source_points()

# =============================================================


class TestSphericalSource():

    # setup routine for subsequent tests
    @pytest.fixture(scope="function")
    def create_source(self):
        my_source = source.SphereSource("air", density=1.2, sphere_radius=10,
                                        sphere_center=[4, 5, 6])
        return my_source

    def test_init(self, create_source):
        # test attribute of shield class
        assert create_source.center == [4, 5, 6]
        assert create_source.radius == 10
        assert create_source.material.name == "air"
        assert create_source.material.density == 1.2
        # test attribute of source class
        assert create_source._include_key_progeny is False
        assert create_source.points_per_dimension == [10, 10, 10]

    def test_StaticFunctions(self):
        # ---------------------------------
        # test _rquad static function
        # ---------------------------------
        r, w = source._rquad(8, 2)
        # the reference values were generated with the matlab
        # script "testRquad.m"
        r_reference = [0.0714910350400932,
                       0.184228296416716,
                       0.330447728175639,
                       0.494402921815511,
                       0.658348008522798,
                       0.804524831511260,
                       0.917099382514349,
                       0.983902240448079]
        w_reference = [0.000468517784034696,
                       0.00447452171301442,
                       0.0172468637802350,
                       0.0408144263885439,
                       0.0684471834216533,
                       0.0852847691719388,
                       0.0768180932672225,
                       0.0397789578066907]
        np.testing.assert_allclose(r, r_reference)
        np.testing.assert_allclose(w, w_reference)

        r, w = source._rquad(8, 0)
        # the reference values were generated with the matlab
        # script "testRquad.m"
        r_reference = [0.0198550717512318,
                       0.101666761293187,
                       0.237233795041835,
                       0.408282678752175,
                       0.591717321247825,
                       0.762766204958165,
                       0.898333238706814,
                       0.980144928248768]
        w_reference = [0.0506142681451881,
                       0.111190517226687,
                       0.156853322938944,
                       0.181341891689181,
                       0.181341891689181,
                       0.156853322938944,
                       0.111190517226687,
                       0.0506142681451879]
        np.testing.assert_allclose(r, r_reference)
        np.testing.assert_allclose(w, w_reference)

        r, w = source._rquad(1, 2)
        # the reference values were generated with the matlab
        # script "testRquad.m"
        r_reference = [0.750000000000000]
        w_reference = [0.333333333333333]
        np.testing.assert_allclose(r, r_reference)
        np.testing.assert_allclose(w, w_reference)

        r, w = source._rquad(1, 0)
        # the reference values were generated with the matlab
        # script "testRquad.m"
        r_reference = [0.500000000000000]
        w_reference = [1.000000000000000]
        np.testing.assert_allclose(r, r_reference)
        np.testing.assert_allclose(w, w_reference)

        # ---------------------------------
        # test _spherequad static function
        # ---------------------------------
        # the reference values were generated with the matlab
        # script "testSphereQuadrature.m"
        r, t, p, w = source._spherequad(4, 5, 6, 10)
        # the reference values were generated with matlab
        r_reference = [2.04148582103227]*5 + [4.82952704895633]*5 \
            + [7.61399262448138]*5 + [9.51499450553003]*5
        r_reference = r_reference*6
        t_reference = [2.70495770436427, 2.13941584994667, 1.57079632679490,
                       1.00217680364312, 0.436634949225523]
        t_reference = t_reference*24
        p_reference = [0]*20 + [1.04719755119660]*20 + [2.09439510239320]*20 \
            + [3.14159265358979]*20 + [4.18879020478639]*20 \
            + [5.23598775598299]*20
        w_reference = [2.56848672807022, 5.18873739280356, 6.16723408367606,
                       5.18873739280357, 2.56848672807022, 17.0287025348515,
                       34.4005926243964, 40.8878868346816, 34.4005926243964,
                       17.0287025348515, 35.5934532943715, 71.9042384097783,
                       85.4640033424298, 71.9042384097783, 35.5934532943715,
                       27.5124420571997, 55.5793554661617, 66.0605595216787,
                       55.5793554661618, 27.5124420571997]
        w_reference = w_reference*6
        np.testing.assert_allclose(r, r_reference)
        np.testing.assert_allclose(t, t_reference)
        np.testing.assert_allclose(p, p_reference)
        np.testing.assert_allclose(w, w_reference)

        r, t, p, w = source._spherequad(1, 1, 1, 10)
        # the reference values were generated with the matlab
        # script "testSphereQuadrature.m"
        r_reference = [7.500000000000000]
        t_reference = [1.570796326794897]
        p_reference = [0]
        w_reference = [4.188790204786391e+03]
        np.testing.assert_allclose(r, r_reference)
        np.testing.assert_allclose(t, t_reference)
        np.testing.assert_allclose(p, p_reference)
        np.testing.assert_allclose(w, w_reference)

    # ---------------------------------
    # test source point locations and set/retrieve of photon source energies
    # reference: manual calculation and isotope library
    def test_getSourcePoints(self, create_source):
        create_source.points_per_dimension = [4, 5, 6]
        # the reference values were generated with the matlab
        # script "testSphereQuadrature.m"
        r_reference = [2.04148582103227]*5 + [4.82952704895633]*5 \
            + [7.61399262448138]*5 + [9.51499450553003]*5
        r_reference = r_reference*6
        t_reference = [2.70495770436427, 2.13941584994667, 1.57079632679490,
                       1.00217680364312, 0.436634949225523]
        t_reference = t_reference*24
        p_reference = [0]*20 + [1.04719755119660]*20 + [2.09439510239320]*20 \
            + [3.14159265358979]*20 + [4.18879020478639]*20 \
            + [5.23598775598299]*20
        x = r_reference*np.sin(t_reference) * \
            np.cos(p_reference)
        y = r_reference*np.sin(t_reference) * \
            np.sin(p_reference)
        z = r_reference*np.cos(t_reference)
        bigly = np.array([x, y, z]).transpose()
        # now let's relocate the center from (0,0,0) to (4,5,6)
        bigly = bigly + [4, 5, 6]
        np.testing.assert_allclose(create_source._get_source_points(),
                                   bigly)  # , rtol=0.99, atol=1e-14)

        create_source.add_isotope_curies('Ar-41', 3.14)
        create_source.add_isotope_bq('Br-80m', 1E6)
        create_source.add_photon(0.9876, 3.14E2)
        a = create_source.get_photon_source_list()
        np.testing.assert_allclose(a,
                                   [(0.037052, (3.90540e-01) * 1e6),
                                    (0.04885, (3.26673e-03) * 1e6),
                                    (0.9876, 3.14E2),
                                    (1.29364, 9.91600e-01 * 3.7e10 * 3.14),
                                    (1.677, 5.15632e-04 * 3.7e10 * 3.14)])

    def test_getSourcePointWeights(self, create_source):
        create_source.points_per_dimension = [4, 5, 6]
        # the reference values were generated with the matlab
        # script "testSphereQuadrature.m"
        w_reference = [2.56848672807022, 5.18873739280356, 6.16723408367606,
                       5.18873739280357, 2.56848672807022, 17.0287025348515,
                       34.4005926243964, 40.8878868346816, 34.4005926243964,
                       17.0287025348515, 35.5934532943715, 71.9042384097783,
                       85.4640033424298, 71.9042384097783, 35.5934532943715,
                       27.5124420571997, 55.5793554661617, 66.0605595216787,
                       55.5793554661618, 27.5124420571997]
        w_reference = w_reference*6
        # note that these raw weights from _spherequad are the volumes of each
        # quadrature section.  To generate weights used by ZapMeNot, the
        # weights must be scaled by the average weight.
        volume = (4./3.)*np.pi*(10**3)
        w_reference = [x / volume for x in w_reference]

        a = create_source._get_source_point_weights()
        np.testing.assert_allclose(a, w_reference)

    # test invalid number of entries in source points per dimension
    def test_getSourcePoints2(self, create_source):
        with pytest.raises(ValueError):
            create_source.points_per_dimension = [1, 1]

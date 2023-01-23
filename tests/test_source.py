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
                                     material_name='iron')
        return my_source

    def test_init(self, create_source):
        # test attribute of shield class
        assert all(create_source.box_center == [4, 5, 6])
        assert all(create_source.box_dimensions == [10, 10, 10])
        assert create_source.material.name == "iron"
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
        the_list = [1.0 / 1000] * 1000
        assert create_source._get_source_point_weights() == the_list

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
            cylinder_center=[0, 0, 0],
            cylinder_length=10, cylinder_radius=5, material_name='iron')
        my_source.points_per_dimension = [3, 3, 3]
        return my_source

    def test_init(self, create_source):
        # test attribute of shield class
        assert create_source.radius == 5
        assert create_source.length == 10
        assert all(create_source.origin == [-5, 0, 0])
        assert all(create_source.end == [5, 0, 0])
        assert all(create_source.dir == [1, 0, 0])
        assert create_source.material.name == "iron"
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
            [[1.6666666667E00, 1.2500000000E00, -7.2168783649E-01],
             [5.0000000000E00, 1.2500000000E00, -7.2168783649E-01],
             [8.3333333333E00, 1.2500000000E00, -7.2168783649E-01],
             [1.6666666667E00, 1.7676253979E-16, 1.4433756730E00],
             [5.0000000000E00, 1.7676253979E-16, 1.4433756730E00],
             [8.3333333333E00, 1.7676253979E-16, 1.4433756730E00],
             [1.6666666667E00, -1.2500000000E00, -7.2168783649E-01],
             [5.0000000000E00, -1.2500000000E00, -7.2168783649E-01],
             [8.3333333333E00, -1.2500000000E00, -7.2168783649E-01],
             [1.6666666667E00, 3.0177669530E00, -1.7423085626E00],
             [5.0000000000E00, 3.0177669530E00, -1.7423085626E00],
             [8.3333333333E00, 3.0177669530E00, -1.7423085626E00],
             [1.6666666667E00, 4.2674252087E-16, 3.4846171253E00],
             [5.0000000000E00, 4.2674252087E-16, 3.4846171253E00],
             [8.3333333333E00, 4.2674252087E-16, 3.4846171253E00],
             [1.6666666667E00, -3.0177669530E00, -1.7423085626E00],
             [5.0000000000E00, -3.0177669530E00, -1.7423085626E00],
             [8.3333333333E00, -3.0177669530E00, -1.7423085626E00],
             [1.6666666667E00, 3.9328304624E00, -2.2706207262E00],
             [5.0000000000E00, 3.9328304624E00, -2.2706207262E00],
             [8.3333333333E00, 3.9328304624E00, -2.2706207262E00],
             [1.6666666667E00, 5.5614168087E-16, 4.5412414523E00],
             [5.0000000000E00, 5.5614168087E-16, 4.5412414523E00],
             [8.3333333333E00, 5.5614168087E-16, 4.5412414523E00],
             [1.6666666667E00, -3.9328304624E00, -2.2706207262E00],
             [5.0000000000E00, -3.9328304624E00, -2.2706207262E00],
             [8.3333333333E00, -3.9328304624E00, -2.2706207262E00]])

    def test_getSourcePointWeights(self, create_source):
        the_list = [1.0 / 27] * 27
        assert create_source._get_source_point_weights() == the_list

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
            cylinder_center=[0, 0, 0],
            cylinder_length=10, cylinder_radius=5, material_name='iron')
        my_source.points_per_dimension = [3, 3, 3]
        return my_source

    def test_init(self, create_source):
        # test attribute of shield class
        assert create_source.radius == 5
        assert create_source.length == 10
        assert all(create_source.origin == [0, -5, 0])
        assert all(create_source.end == [0, 5, 0])
        assert all(create_source.dir == [0, 1, 0])
        assert create_source.material.name == "iron"
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
            [[7.2168783649E-01, 1.6666666667E00, -1.2500000000E00],
             [7.2168783649E-01, 5.0000000000E00, -1.2500000000E00],
             [7.2168783649E-01, 8.3333333333E00, -1.2500000000E00],
             [-1.4433756730E00, 1.6666666667E00, -1.7676253979E-16],
             [-1.4433756730E00, 5.0000000000E00, -1.7676253979E-16],
             [-1.4433756730E00, 8.3333333333E00, -1.7676253979E-16],
             [7.2168783649E-01, 1.6666666667E00, 1.2500000000E00],
             [7.2168783649E-01, 5.0000000000E00, 1.2500000000E00],
             [7.2168783649E-01, 8.3333333333E00, 1.2500000000E00],
             [1.7423085626E00, 1.6666666667E00, -3.0177669530E00],
             [1.7423085626E00, 5.0000000000E00, -3.0177669530E00],
             [1.7423085626E00, 8.3333333333E00, -3.0177669530E00],
             [-3.4846171253E00, 1.6666666667E00, -4.2674252087E-16],
             [-3.4846171253E00, 5.0000000000E00, -4.2674252087E-16],
             [-3.4846171253E00, 8.3333333333E00, -4.2674252087E-16],
             [1.7423085626E00, 1.6666666667E00, 3.0177669530E00],
             [1.7423085626E00, 5.0000000000E00, 3.0177669530E00],
             [1.7423085626E00, 8.3333333333E00, 3.0177669530E00],
             [2.2706207262E00, 1.6666666667E00, -3.9328304624E00],
             [2.2706207262E00, 5.0000000000E00, -3.9328304624E00],
             [2.2706207262E00, 8.3333333333E00, -3.9328304624E00],
             [-4.5412414523E00, 1.6666666667E00, -5.5614168087E-16],
             [-4.5412414523E00, 5.0000000000E00, -5.5614168087E-16],
             [-4.5412414523E00, 8.3333333333E00, -5.5614168087E-16],
             [2.2706207262E00, 1.6666666667E00, 3.9328304624E00],
             [2.2706207262E00, 5.0000000000E00, 3.9328304624E00],
             [2.2706207262E00, 8.3333333333E00, 3.9328304624E00]])

    def test_getSourcePointWeights(self, create_source):
        the_list = [1.0 / 27] * 27
        assert create_source._get_source_point_weights() == the_list

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
            cylinder_center=[0, 0, 0],
            cylinder_length=10, cylinder_radius=5, material_name='iron')
        my_source.points_per_dimension = [3, 3, 3]
        return my_source

    def test_init(self, create_source):
        # test attribute of shield class
        assert create_source.radius == 5
        assert create_source.length == 10
        assert all(create_source.origin == [0, 0, -5])
        assert all(create_source.end == [0, 0, 5])
        assert all(create_source.dir == [0, 0, 1])
        assert create_source.material.name == "iron"
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
            [[7.2168783649e-01, 1.2500000000e+00, 1.6666666667e+00],
             [7.2168783649e-01, 1.2500000000e+00, 5],
             [7.2168783649e-01, 1.2500000000e+00, 8.3333333333e+00],
             [-1.4433756730e+00, 1.7676253979e-16, 1.6666666667e+00],
             [-1.4433756730e+00, 1.7676253979e-16, 5],
             [-1.4433756730e+00, 1.7676253979e-16, 8.3333333333e+00],
             [7.2168783649e-01, -1.2500000000e+00, 1.6666666667e+00],
             [7.2168783649e-01, -1.2500000000e+00, 5],
             [7.2168783649e-01, -1.2500000000e+00, 8.3333333333e+00],
             [1.7423085626e+00, 3.0177669530e+00, 1.6666666667e+00],
             [1.7423085626e+00, 3.0177669530e+00, 5],
             [1.7423085626e+00, 3.0177669530e+00, 8.3333333333e+00],
             [-3.4846171253e+00, 4.2674252087e-16, 1.6666666667e+00],
             [-3.4846171253e+00, 4.2674252087e-16, 5],
             [-3.4846171253e+00, 4.2674252087e-16, 8.3333333333e+00],
             [1.7423085626e+00, -3.0177669530e+00, 1.6666666667e+00],
             [1.7423085626e+00, -3.0177669530e+00, 5],
             [1.7423085626e+00, -3.0177669530e+00, 8.3333333333e+00],
             [2.2706207262e+00, 3.9328304624e+00, 1.6666666667e+00],
             [2.2706207262e+00, 3.9328304624e+00, 5],
             [2.2706207262e+00, 3.9328304624e+00, 8.3333333333e+00],
             [-4.5412414523e+00, 5.5614168087e-16, 1.6666666667e+00],
             [-4.5412414523e+00, 5.5614168087e-16, 5],
             [-4.5412414523e+00, 5.5614168087e-16, 8.3333333333e+00],
             [2.2706207262e+00, -3.9328304624e+00, 1.6666666667e+00],
             [2.2706207262e+00, -3.9328304624e+00, 5],
             [2.2706207262e+00, -3.9328304624e+00, 8.3333333333e+00]])

    def test_getSourcePointWeights(self, create_source):
        the_list = [1.0 / 27] * 27
        assert create_source._get_source_point_weights() == the_list

    # test invalid number of entries in source points per dimension
    def test_getSourcePoints2(self, create_source):
        create_source.points_per_dimension = [1, 1]
        with pytest.raises(ValueError):
            create_source._get_source_points()

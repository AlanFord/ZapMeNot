import math

import pytest

from zap_me_not import shield, ray, material

pytestmark = pytest.mark.basic


# test set/retrieve common shield properties
# reference: none
def test_GeneralShieldFeatures():
    myShield = shield.SemiInfiniteXSlab("iron", 10, 20, density=0.123)
    assert myShield.material.name == "iron"
    assert myShield.material.density == 0.123


# =============================================================
class TestSemiInfiniteXSlab():

    # setup routine for subsequent tests
    @pytest.fixture(scope="class")
    def create_shield(self):
        myShield = shield.SemiInfiniteXSlab("iron", 10, 20)
        return myShield

    def test_init(self, create_shield):
        assert create_shield.x_start == 10
        assert create_shield.x_end == 20

    # setup routine for subsequent tests
    @pytest.fixture(scope="class")
    def create_ray(self):
        start = [0, 0, 0]
        end = [30, 30, 30]
        aRay = ray.FiniteLengthRay(start, end)
        return aRay

    # test arguements used to create a slab shield
    # reference: setup function create_shield()
    def test_size(self, create_shield):
        assert create_shield.material.name == "iron"
        assert create_shield.x_start == 10
        assert create_shield.x_end == 20

    # test getting a crossing length
    # reference: test_shield/slabCrossingLength.m (matlab script)
    def test_crossing_length1(self, create_shield, create_ray):
        length = create_shield._get_crossing_length(create_ray)
        assert length == pytest.approx(17.320508)

    # test getting a crossing length after reversing the directio of the ray
    # reference: test_shield/slabCrossingLength.m (matlab script)
    def test_crossing_length2(self, create_shield, create_ray):
        a = create_ray.start
        create_ray.start = create_ray.end
        create_ray.end = a
        length = create_shield._get_crossing_length(create_ray)
        assert length == pytest.approx(17.320508)

    # test crossing length for a ray that misses the shield
    # reference: none
    def test_crossing_length3(self, create_shield):
        # ray misses the slab
        length = create_shield._get_crossing_length(ray.FiniteLengthRay(
                [30, 0, 0], [30, 0, 30]))
        assert length == 0

    # test crossing length for ray originating inside shield
    # reference: hand calculation based on previous result from
    #     test_shield\slabCrossingLength.m (matlab script)
    def test_crossing_length4(self, create_shield):
        # two rays that start inside the slab and traverse outwards
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([15, 15, 15], [30, 30, 30]))
        assert length == pytest.approx(17.320508/2)

    # test crossing length for ray originating inside shield
    # reference: hand calculation based on previous result from
    #     test_shield/slabCrossingLength.m (matlab script)
    def test_crossing_length5(self, create_shield):
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([30, 30, 30], [15, 15, 15]))
        assert length == pytest.approx(17.320508/2)

    # test crossing length for ray terminating inside shield
    # reference: hand calculation based on previous result from
    #     test_shield\slabCrossingLength.m (matlab script)
    def test_crossing_length6(self, create_shield):
        # ray start outside the slab and ends inside the slab
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([0, 0, 0], [15, 15, 15]))
        assert length == pytest.approx(17.320508/2)

    # test crossing length for ray entirely inside shield
    # reference: hand calculation
    def test_crossing_length7(self, create_shield):
        # ray contained entirely within the slab
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([11, 11, 11], [16, 16, 16]))
        assert length == pytest.approx(math.sqrt(25*3))

    # test getting a crossing mfp
    # reference:  NEED A REFERENCE
    def test_get_MFP(self, create_shield, create_ray):
        mfp = create_shield.get_crossing_mfp(create_ray, 0.66)
        assert mfp == pytest.approx(9.923087573149688)

    # test getting a crossing mfp
    # reference:  materialLibrary.yml and hand calc
    def test_get_special_MFP(self, create_shield):
        start = [0, 0, 0]
        end = [100, 0, 0]
        aRay = ray.FiniteLengthRay(start, end)
        mfp = create_shield.get_crossing_mfp(aRay, 1)
        # data extracted from materialLibrary.yml for iron at 1 MeV
        xsec = 5.957E-02
        density = 7.874
        calculated_mfp = xsec*density*10  # 10 cm width of shield
        assert mfp == pytest.approx(calculated_mfp)

    def test_infinite(self, create_shield):
        assert create_shield.is_infinite() is True


# =============================================================
# class TestSphere():

# 	@pytest.fixture(scope="class")
# 	def create_shield(self):
# 		myShield = shield.Sphere("iron", sphere_radius=10, sphere_center=[0,0,0])
# 		return myShield

#   def test_init(self, create_shield):
#       assert create_shield.inner_radius == 2
#       assert create_shield.outer_radius == 4
#       assert all(create_shield.origin == [0, 0, -50])
#       assert all(create_shield.dir == [0, 0, 1])

# 	def test_crossing_length0(self, create_shield):
# 		# basic ray crossing
# 		length = create_shield.get_crossing_length(
#           ray.FiniteLengthRay([-10, -10, -10], [10, 10, 10]))
# 		assert length == pytest.approx(20)

# 	def test_crossing_length1(self, create_shield):
# 		# try reversing the direction
# 		length = create_shield.get_crossing_length(
#           ray.FiniteLengthRay([10, 10, 10], [-10, -10, -10]))
# 		assert length == pytest.approx(20)

# 	def test_crossing_length2(self, create_shield):
# 		# ray misses the sphere
# 		length = create_shield.get_crossing_length(
#           ray.FiniteLengthRay([-15, -15, -15], [-15, -15, 15]))
# 		assert length == 0

# 	def test_crossing_length3(self, create_shield):
# 		# ray starts inside the sphere and traverse outwards
# 		length = create_shield.get_crossing_length(
#           ray.FiniteLengthRay([-1, -1, -1], [10, 10, 10]))
# 		assert length == 10+math.sqrt(3)

# 	def test_crossing_length4(self, create_shield):
# 		# ray starts outside the sphere and ends inside the sphere
# 		length = create_shield.get_crossing_length(
#           ray.FiniteLengthRay([10, 10, 10], [-1, -1, -1]))
# 		assert length == pytest.approx(10+math.sqrt(3))

# 	def test_crossing_length5(self, create_shield):
# 		# ray contained entirely within the sphere
# 		length = create_shield.get_crossing_length(
#           ray.FiniteLengthRay([1, 1, 1], [-1, -1, -1]))
# 		assert length == 2*math.sqrt(3)

# 	# test getting a crossing mfp
# 	def test_get_special_MFP(self, create_shield):
# 		start = [0, 0, 0]
# 		end = [100, 0, 0]
# 		aRay = ray.FiniteLengthRay(start, end)
# 		mfp = create_shield.get_crossing_mfp(aRay, 1)
# 		# data extracted from materialLibrary.yml for iron at 1 MeV
# 		xsec = 5.957E-02
# 		density = 7.874
# 		calculated_mfp = xsec*density*10 # 10 cm crossing width of shield
# 		assert mfp == pytest.approx(calculated_mfp)

#   def test_infinite(self, create_shield):
#       assert create_shield.is_infinite() is False


# =============================================================
class TestBox():

    @pytest.fixture(scope="class")
    def create_shield(self):
        myShield = shield.Box("iron", box_center=[1, 0, 0],
                              box_dimensions=[10, 10, 10])
        return myShield

    def test_init(self, create_shield):
        assert all(create_shield.box_center == [1, 0, 0])
        assert all(create_shield.box_dimensions == [10, 10, 10])

    # test getting a crossing length
    def test_crossing_length0(self, create_shield):
        # test a pure diagonal crossing
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([-4, -5, -5], [16, 15, 15]))
        assert length == math.sqrt(3*(10**2))

    def test_crossing_length1(self, create_shield):
        # basic ray crossing
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([-10, 3, 3], [20, 3, 3]))
        assert length == 10

    def test_crossing_length2(self, create_shield):
        # try reversing the direction
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([20, 3, 3], [-10, 3, 3]))
        assert length == 10

    def test_crossing_length3(self, create_shield):
        # ray misses the box
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([30, 0, 0], [30, 0, 30]))
        assert length == 0

    def test_crossing_length4(self, create_shield):
        # two rays that start inside the box and traverse outwards
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([3, 3, 3], [21, 3, 3]))
        assert length == 3

    def test_crossing_length5(self, create_shield):
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([3, 3, 3], [-19, 3, 3]))
        assert length == 7

    def test_crossing_length6(self, create_shield):
        # ray start outside the box and ends inside the box
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([21, 3, 3], [3, 3, 3]))
        assert length == 3

    def test_crossing_length7(self, create_shield):
        # ray contained entirely within the box
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([2, 3, 3], [-3, 3, 3]))
        assert length == 5

    # test getting a crossing mfp
    def test_get_special_MFP(self, create_shield):
        start = [1, 0, 0]
        end = [101, 0, 0]
        aRay = ray.FiniteLengthRay(start, end)
        mfp = create_shield.get_crossing_mfp(aRay, 1)
        # data extracted from materialLibrary.yml for iron at 1 MeV
        xsec = 5.957E-02
        density = 7.874
        calculated_mfp = xsec*density*5  # 5 cm crossing width of shield
        assert mfp == pytest.approx(calculated_mfp)

    def test_infinite(self, create_shield):
        assert create_shield.is_infinite() is False


# =============================================================
class TestInfiniteAnnulus():

    @pytest.fixture(scope="class")
    def create_shield(self):
        myShield = shield.InfiniteAnnulus("iron", cylinder_origin=[0, 0, -50],
                                          cylinder_axis=[0, 0, 1],
                                          cylinder_inner_radius=2,
                                          cylinder_outer_radius=4, density=2)
        return myShield

    def test_init(self, create_shield):
        assert create_shield.inner_radius == 2
        assert create_shield.outer_radius == 4
        assert all(create_shield.origin == [0, 0, -50])
        assert all(create_shield.dir == [0, 0, 1])

    def test_density(self, create_shield):
        assert create_shield.material.density == 2

    def test_crossing_length0(self, create_shield):
        # complete miss
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([10, 0, 0], [15, 0, 00]))
        assert length == 0

    def test_crossing_length1(self, create_shield):
        # completely inside annulus
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([2.5, 0, -8], [3.5, 0, 8]))
        assert length == math.sqrt(1+16**2)

    def test_crossing_length2(self, create_shield):
        # side-to-side
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([-20, 0, 0], [20, 0, 0]))
        assert length == 4

    def test_crossing_length3(self, create_shield):
        # and back again
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([20, 0, 0], [-20, 0, 0]))
        assert length == 4

    def test_crossing_length4(self, create_shield):
        # completely inside annulus (miss)
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([1, 0, -60], [1.5, 0, 60]))
        assert length == 0

    def test_crossing_length5(self, create_shield):
        # and back again
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([1.5, 0, 60], [1, 0, -60]))
        assert length == 0

    def test_crossing_length8(self, create_shield):
        # outside to inside annulus
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([-20, 0, 0], [-3.5, 0, 0]))
        assert length == 0.5

    def test_crossing_length9(self, create_shield):
        # and back again
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([-3.5, 0, 0], [-20, 0, 0]))
        assert length == 0.5

    def test_crossing_length10(self, create_shield):
        # center to inside annulus
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([1, 0, 55], [2.5, 0, 55]))
        assert length == 0.5

    def test_crossing_length11(self, create_shield):
        # and back again
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([2.5, 0, 55], [1, 0, 55]))
        assert length == 0.5

    # test getting a crossing mfp
    def test_get_special_MFP(self, create_shield):
        start = [0, 0, 0]
        end = [100, 0, 0]
        aRay = ray.FiniteLengthRay(start, end)
        mfp = create_shield.get_crossing_mfp(aRay, 1)
        # data extracted from materialLibrary.yml for iron at 1 MeV
        xsec = 5.957E-02
        density = 2  # specified in the setup
        calculated_mfp = xsec*density*2  # 2 cm crossing width of shield
        assert mfp == pytest.approx(calculated_mfp)

    def test_infinite(self, create_shield):
        assert create_shield.is_infinite() is True


# =============================================================
class TestYAlignedInfiniteAnnulus():

    @pytest.fixture(scope="class")
    def create_shield(self):
        myShield = shield.YAlignedInfiniteAnnulus("iron", cylinder_center=[0, 0, -50],
                                          cylinder_inner_radius=2,
                                          cylinder_outer_radius=4, density=2)
        return myShield

    def test_init(self, create_shield):
        assert create_shield.inner_radius == 2
        assert create_shield.outer_radius == 4
        assert all(create_shield.origin == [0, 0, -50])
        assert all(create_shield.dir == [0, 1, 0])


# =============================================================
class TestXAlignedInfiniteAnnulus():

    @pytest.fixture(scope="class")
    def create_shield(self):
        myShield = shield.XAlignedInfiniteAnnulus("iron", cylinder_center=[0, 0, -50],
                                          cylinder_inner_radius=2,
                                          cylinder_outer_radius=4, density=2)
        return myShield

    def test_init(self, create_shield):
        assert create_shield.inner_radius == 2
        assert create_shield.outer_radius == 4
        assert all(create_shield.origin == [0, 0, -50])
        assert all(create_shield.dir == [1, 0, 0])


# =============================================================
class TestZAlignedInfiniteAnnulus():

    @pytest.fixture(scope="class")
    def create_shield(self):
        myShield = shield.ZAlignedInfiniteAnnulus("iron", cylinder_center=[0, 0, -50],
                                          cylinder_inner_radius=2,
                                          cylinder_outer_radius=4, density=2)
        return myShield

    def test_init(self, create_shield):
        assert create_shield.inner_radius == 2
        assert create_shield.outer_radius == 4
        assert all(create_shield.origin == [0, 0, -50])
        assert all(create_shield.dir == [0, 0, 1])


# =============================================================
class TestCappedCylinder():

    @pytest.fixture(scope="class")
    def create_shield(self):
        myShield = shield.CappedCylinder("iron",
                                         cylinder_start=[0, 0, -50],
                                         cylinder_end=[0, 0, 50],
                                         cylinder_radius=10)
        return myShield

    def test_init(self, create_shield):
        assert create_shield.radius == 10
        assert all(create_shield.origin == [0, 0, -50])
        assert all(create_shield.end == [0, 0, 50])
        assert create_shield.length == 100
        assert all(create_shield.dir == [0, 0, 1])

    def test_crossing_length0(self, create_shield):
        # complete miss
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([15, 0, -60], [15, 0, 60]))
        assert length == 0

    def test_crossing_length1(self, create_shield):
        # completely inside
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([0, 0, -8], [0, 0, 8]))
        assert length == 16

    def test_crossing_length2(self, create_shield):
        # side-to-side
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([-20, 0, 0], [20, 0, 0]))
        assert length == 20

    def test_crossing_length3(self, create_shield):
        # and back again
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([20, 0, 0], [-20, 0, 0]))
        assert length == 20

    def test_crossing_length4(self, create_shield):
        # end-to-end
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([0, 0, -60], [0, 0, 60]))
        assert length == 100

    def test_crossing_length5(self, create_shield):
        # and back again
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([0, 0, 60], [0, 0, -60]))
        assert length == 100

    def test_crossing_length6(self, create_shield):
        # side-to-end
        pass

    def test_crossing_length7(self, create_shield):
        # end-to-side
        pass

    def test_crossing_length8(self, create_shield):
        # outside to inside wall
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([-20, 0, 0], [-5, 0, 0]))
        assert length == 5

    def test_crossing_length9(self, create_shield):
        # and back again
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([-5, 0, 0], [-20, 0, 0]))
        assert length == 5

    def test_crossing_length10(self, create_shield):
        # outside to inside cap
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([1, 1, 55], [1, 1, 45]))
        assert length == 5

    def test_crossing_length11(self, create_shield):
        # and back again
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([1, 1, 45], [1, 1, 55]))
        assert length == 5

    # test getting a crossing mfp
    def test_get_special_MFP(self, create_shield):
        start = [0, 0, 0]
        end = [100, 0, 0]
        aRay = ray.FiniteLengthRay(start, end)
        mfp = create_shield.get_crossing_mfp(aRay, 1)
        # data extracted from materialLibrary.yml for iron at 1 MeV
        xsec = 5.957E-02
        density = 7.874
        calculated_mfp = xsec*density*10  # 10 cm crossing width of shield
        assert mfp == pytest.approx(calculated_mfp)

    def test_infinite(self, create_shield):
        assert create_shield.is_infinite() is False


# =============================================================
class TestYAlignedCylinder():

    @pytest.fixture(scope="class")
    def create_shield(self):
        myShield = shield.YAlignedCylinder("iron",
                                           cylinder_center=[0, 0, 0],
                                           cylinder_length=100,
                                           cylinder_radius=10)
        return myShield

    def test_init(self, create_shield):
        assert create_shield.radius == 10
        assert all(create_shield.origin == [0, -50, 0])
        assert all(create_shield.end == [0, 50, 0])
        assert create_shield.length == 100
        assert all(create_shield.dir == [0, 1, 0])

    def test_crossing_length(self, create_shield):
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([2, -60, 2], [2, 60, 2]))
        assert length == 100

    def test_infinite(self, create_shield):
        assert create_shield.is_infinite() is False


# =============================================================
class TestXAlignedCylinder():

    @pytest.fixture(scope="class")
    def create_shield(self):
        myShield = shield.XAlignedCylinder("iron",
                                           cylinder_center=[0, 0, 0],
                                           cylinder_length=100,
                                           cylinder_radius=10)
        return myShield

    def test_init(self, create_shield):
        assert create_shield.radius == 10
        assert all(create_shield.origin == [-50, 0, 0])
        assert all(create_shield.end == [50, 0, 0])
        assert create_shield.length == 100
        assert all(create_shield.dir == [1, 0, 0])

    def test_crossing_length(self, create_shield):
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([-60, 2, 2], [60, 2, 2]))
        assert length == 100

    def test_infinite(self, create_shield):
        assert create_shield.is_infinite() is False


# =============================================================
class TestZAlignedCylinder():

    @pytest.fixture(scope="class")
    def create_shield(self):
        myShield = shield.ZAlignedCylinder("iron",
                                           cylinder_center=[0, 0, 0],
                                           cylinder_length=100,
                                           cylinder_radius=10)
        return myShield

    def test_init(self, create_shield):
        assert create_shield.radius == 10
        assert all(create_shield.origin == [0, 0, -50])
        assert all(create_shield.end == [0, 0, 50])
        assert create_shield.length == 100
        assert all(create_shield.dir == [0, 0, 1])

    def test_crossing_length(self, create_shield):
        length = create_shield._get_crossing_length(
            ray.FiniteLengthRay([2, 2, -60], [2, 2, 60]))
        assert length == 100

    def test_infinite(self, create_shield):
        assert create_shield.is_infinite() is False

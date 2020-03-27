import pytest
import math
from ZapMeNot import shield, ray, material

def test_GeneralShieldFeatures():
	myShield = shield.SemiInfiniteXSlab(materialName="iron", xStart=10, xEnd=20, density=0.123)
	assert myShield.material.name == "iron"
	assert myShield.material.density == 0.123

#=============================================================
class TestSemiInfiniteXSlab():

	@pytest.fixture(scope="class")
	def create_shield(self):
		myShield = shield.SemiInfiniteXSlab(materialName="iron", xStart=10, xEnd=20)
		return myShield

	@pytest.fixture(scope="class")
	def create_ray(self):
		start = [0,0,0]
		end = [30,30,30]
		aRay = ray.Ray(start, end)
		return aRay

	# test arguments
	def test_size(self,create_shield):
		assert create_shield.material.name == "iron"
		assert create_shield.xStart == 10
		assert create_shield.xEnd == 20

	# test getting a crossing length
	# reference value taken from matlab script slabCrossingLength.m
	def test_crossing_length1(self, create_shield, create_ray):
		length = create_shield.getCrossingLength(create_ray)
		assert length == pytest.approx(17.320508)

	def test_crossing_length2(self, create_shield, create_ray):
		# try reversing the direction
		a=create_ray.start
		create_ray.start=create_ray.end
		create_ray.end=a
		length = create_shield.getCrossingLength(create_ray)
		assert length == pytest.approx(17.320508)

	def test_crossing_length3(self, create_shield, create_ray):
		# ray misses the slab
		length = create_shield.getCrossingLength(ray.Ray([30,0,0], [30,0,30]))
		assert length == 0

	def test_crossing_length4(self, create_shield, create_ray):
		# two rays that start inside the slab and traverse outwards
		length = create_shield.getCrossingLength(ray.Ray([15,15,15], [30,30,30]))
		assert length == pytest.approx(17.320508/2)

	def test_crossing_length5(self, create_shield, create_ray):
		length = create_shield.getCrossingLength(ray.Ray([30,30,30], [15,15,15]))
		assert length == pytest.approx(17.320508/2)

	def test_crossing_length6(self, create_shield, create_ray):
		# ray start outside the slab and ends inside the slab
		length = create_shield.getCrossingLength(ray.Ray([0,0,0], [15,15,15]))
		assert length == pytest.approx(17.320508/2)

	def test_crossing_length7(self, create_shield, create_ray):
		# ray contained entirely within the slab
		length = create_shield.getCrossingLength(ray.Ray([11,11,11], [16,16,16]))
		assert length == pytest.approx(math.sqrt(25*3))

	# test getting a crossing mfp
	def test_get_MFP(self, create_shield, create_ray):
		mfp = create_shield.getCrossingMFP(create_ray, 0.66)
		assert mfp == pytest.approx(9.923087573149688)

	# test getting a crossing mfp
	def test_get_special_MFP(self, create_shield):
		start = [0,0,0]
		end = [100,0,0]
		aRay = ray.Ray(start, end)
		mfp = create_shield.getCrossingMFP(aRay, 1)
		# data extracted from materialLibrary.yml for iron at 1 MeV
		xsec = 5.957E-02
		density = 7.874
		calculated_mfp = xsec*density*10 # 10 cm width of shield
		assert mfp == pytest.approx(calculated_mfp)

# #=============================================================
class TestSphere():

	@pytest.fixture(scope="class")
	def create_shield(self):
		myShield = shield.Sphere(materialName="iron", sphereCenter=[0,0,0],sphereRadius=10)
		return myShield

	@pytest.fixture(scope="class")
	def create_ray(self):
		start = [-15,0,0]
		end = [30,0,0]
		aRay = ray.Ray(start, end)
		return aRay

	def test_crossing_length(self, create_shield, create_ray):
		length = create_shield.getCrossingLength(create_ray)
		assert length == pytest.approx(20)

# #=============================================================
class TestBox():

	@pytest.fixture(scope="class")
	def create_shield(self):
		myShield = shield.Box(materialName="iron", boxCenter=[0,0,0],boxDimensions=[13,14,15])
		return myShield

	@pytest.fixture(scope="class")
	def create_ray(self):
		start = [-10,0,0]
		end = [30,0,0]
		aRay = ray.Ray(start, end)
		return aRay

	def test_crossing_length(self, create_shield, create_ray):
		length = create_shield.getCrossingLength(create_ray)
		assert length == pytest.approx(13)

#=============================================================
class TestCappedCylinder():

	@pytest.fixture(scope="class")
	def create_shield(self):
		myShield = shield.CappedCylinder(materialName="iron", cylinderStart=[0,0,-50],cylinderEnd=[0,0,50],cylinderRadius=10)
		return myShield

	def test_crossing_length(self, create_shield):
		start = [-10,20,0]
		end = [30,20,0]
		aRay = ray.Ray(start, end)
		length = create_shield.getCrossingLength(aRay)
		assert length == pytest.approx(0)

		start = [-30,0,0]
		end = [30,0,0]
		aRay = ray.Ray(start, end)
		length = create_shield.getCrossingLength(aRay)
		assert length == pytest.approx(20)
		
		start = [0,0,0]
		end = [30,0,0]
		bRay = ray.Ray(start, end)
		length = create_shield.getCrossingLength(bRay)
		assert length == pytest.approx(10)


#=============================================================
class TestYAlignedCylinder():

	@pytest.fixture(scope="class")
	def create_shield(self):
		myShield = shield.YAlignedCylinder(materialName="iron", cylinderCenter=[0,0,0],cylinderLength=100,cylinderRadius=10)
		return myShield

	@pytest.fixture(scope="class")
	def create_ray(self):
		start = [-10,20,0]
		end = [30,20,0]
		aRay = ray.Ray(start, end)
		return aRay

	def test_crossing_length(self, create_shield, create_ray):
		length = create_shield.getCrossingLength(create_ray)
		assert length == pytest.approx(20)

#=============================================================
class TestXAlignedCylinder():

	@pytest.fixture(scope="class")
	def create_shield(self):
		myShield = shield.XAlignedCylinder(materialName="iron", cylinderCenter=[0,0,0],cylinderLength=100,cylinderRadius=10)
		return myShield

	@pytest.fixture(scope="class")
	def create_ray(self):
		start = [20,-10,0]
		end = [20,30,0]
		aRay = ray.Ray(start, end)
		return aRay

	def test_crossing_length(self, create_shield, create_ray):
		length = create_shield.getCrossingLength(create_ray)
		assert length == pytest.approx(20)

#=============================================================
class TestZAlignedCylinder():

	@pytest.fixture(scope="class")
	def create_shield(self):
		myShield = shield.ZAlignedCylinder(materialName="iron", cylinderCenter=[0,0,0],cylinderLength=100,cylinderRadius=10)
		return myShield

	@pytest.fixture(scope="class")
	def create_ray(self):
		start = [-10,0,20]
		end = [30,0,20]
		aRay = ray.Ray(start, end)
		return aRay

	def test_crossing_length(self, create_shield, create_ray):
		length = create_shield.getCrossingLength(create_ray)
		assert length == pytest.approx(20)







import pytest
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
	def test_crossing_length(self, create_shield, create_ray):
		length = create_shield.getCrossingLength(create_ray)
		assert length == pytest.approx(17.320508075688775)

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
		assert mfp == pytest.approx(4.6905418)

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







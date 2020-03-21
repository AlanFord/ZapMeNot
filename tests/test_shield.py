import pytest
from ZapMeNot import shield, ray, material

def test_GeneralShieldFeatures():
	myShield = shield.SemiInfiniteXSlab(materialName="iron", xStart=10, xEnd=20, density=0.123)
	assert myShield.material.name == "iron"
	assert myShield.material.density == 0.123

class testSemiInfiniteXSlab():

	@pytest.fixture(scope="class")
	def create_shield(self):
		self.myShield = shield.SemiInfiniteXSlab("iron", 10, 20)
		start = [0,0,0]
		end = [30,30,30]
		self.aRay = ray.Ray(start, end)

	# test arguments
	def test_size(self, create_shield):
		assert self.material.name == "iron"
		assert self.xStart == 10
		assert self.xEnd == 20

	# test getting a crossing length
	def test_crossing_length(self, create_shield):
		length = self.myShield.getCrossingLength(self.aRay)
		assert length == pytest.approx(17.320508075688775)

	# test getting a crossing mfp
	def test_get_MFP(self, create_shield):
		mfp = self.myShield.getCrossingMFP(self.aRay, 0.66)
		assert mfp == pytest.approx(9.923087573149688)

	# test getting a crossing mfp
	def test_get_special_MFP(self, create_shield):
		start = [0,0,0]
		end = [100,0,0]
		self.aRay = ray.Ray(start, end)
		mfp = self.myShield.getCrossingMFP(self.aRay, 1)
		assert mfp == pytest.approx(4.6905418)

class testYAlignedCylinder():

	@pytest.fixture(scope="class")
	def create_shield(self):
		self.myShield = shield.YAlignedCylinder(materialName="iron", cylinderCenter=[0,0,0],cylinderLength=100,cylinderRadius=10)
		start = [-10,20,0]
		end = [30,20,0]
		self.aRay = ray.Ray(start, end)

	def test_crossing_length(self, create_shield):
		length = self.myShield.getCrossingLength(self.aRay)
		assert length == pytest.approx(20)







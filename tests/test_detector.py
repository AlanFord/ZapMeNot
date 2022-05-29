import pytest

from zap_me_not import detector

pytestmark = pytest.mark.basic

# test set/retrieve detector location
# reference: none required
def test_detector():
	a = detector.Detector(1,2,3)
	assert a.x == 1
	assert a.y == 2
	assert a.z == 3
	assert a.location == (1,2,3)

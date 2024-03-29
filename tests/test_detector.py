import pytest

from zapmenot import detector

pytestmark = pytest.mark.basic


# test set/retrieve detector location
# reference: none required
def test_detector_set_retrieve():
    a = detector.Detector(1, 2, 3)
    assert a.x == 1
    assert a.y == 2
    assert a.z == 3
    assert a.location == (1, 2, 3)


def test_detector_invalid_args():
    with pytest.raises(ValueError):
        detector.Detector('a', 2, 3)
    with pytest.raises(ValueError):
        detector.Detector(1, 'b', 3)
    with pytest.raises(ValueError):
        detector.Detector(1, 2, 'c')

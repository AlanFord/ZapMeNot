import numpy as np
import numbers
from collections.abc import Iterable


class FiniteLengthRay:
    """Represents a ray in three-space.

    The FiniteLengthRay object has a defined starting point, a defined end,
    and a resulting direction.

    Parameters
    ----------
    start : :class:`list` or :class:`tuple`
        Defines the starting point of the ray in cartesian coordinates.
    end : :class:`list` or :class:`tuple`
        Defines the ending point of the ray in cartesian coordinates.

    Attributes
    ----------
    start
    end
    origin : :class:`numpy.ndarray`
        A vector implemenation of the starting point.
    length : float
        The length of the ray.
    dir : :class:`numpy.ndarray`
        A numpy vector holding the vector normal of the ray.
    sign : :class:`numpy.ndarray`
        Indicates the signs of the components of :py:obj:`dir`.
    """
    def __init__(self, start, end):
        if not FiniteLengthRay._is_validate_vector(start):
            raise ValueError("Invalid ray start")
        if not FiniteLengthRay._is_validate_vector(end):
            raise ValueError("Invalid ray end")
        self._start = start
        self._end = end
        self._regularize()

    @property
    def start(self):
        """:class:`list` : A list defining the starting point of the ray in
        cartesian coordinates."""
        return self._start

    @start.setter
    def start(self, value):
        if not FiniteLengthRay._is_validate_vector(value):
            raise ValueError("Invalid ray start")
        self._start = value
        self._regularize()

    @property
    def end(self):
        """:class:`list` : A list defining the ending point of the ray in
        cartesian coordinates."""
        return self._end

    @end.setter
    def end(self, value):
        if not FiniteLengthRay._is_validate_vector(value):
            raise ValueError("Invalid ray end")
        self._end = value
        self._regularize()

    def _regularize(self):
        self.origin = np.array(self._start)
        v = np.array(self._end) - self.origin
        self.length = np.linalg.norm(v)
        # direction doesn't matter if the length is zero
        if self.length == 0:
            self.dir = np.zeros(3)
        else:
            self.dir = v / self.length
        with np.errstate(divide='ignore'):
            self.invdir = 1/self.dir  # vector is opposite of vector dir
        self.sign = [0, 0, 0]
        self.sign[0] = int((self.invdir[0] < 0))
        self.sign[1] = int((self.invdir[1] < 0))
        self.sign[2] = int((self.invdir[2] < 0))

    @staticmethod
    def _is_validate_vector(vector):
        # vector should be a list
        if not (isinstance(vector, Iterable)):
            return False
        # vector should have a length of 3
        if not (len(vector) == 3):
            return False
        # each element should be a number
        if not all([isinstance(item, numbers.Number) for item in vector]):
            return False
        return True

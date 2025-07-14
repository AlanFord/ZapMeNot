'''
ZapMeNot - a point kernel photon shielding library
Copyright (C) 2019-2025  C. Alan Ford

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

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
    """

    '''
    Attributes
    ----------
    _start
    _end
    _origin : :class:`numpy.ndarray`
        A vector implemenation of the starting point.
    _length : float
        The length of the ray.
    _dir : :class:`numpy.ndarray`
        A numpy vector holding the vector normal of the ray.
    _invdir : :class:`numpy.ndarray`
        A numpy vector holding the inverse of the vector _dir.
    _sign : :class:`numpy.ndarray`
        Indicates the signs of the components of :py:obj:`dir`.
    '''

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
        """Calculates the mean free path for a given distance and photon energy

        Parameters
        ----------
        energy : float
            The photon energy in MeV
        distance : float
            The distance through the material in cm
        """

        self._origin = np.array(self._start)
        v = np.array(self._end) - self._origin
        self._length = np.linalg.norm(v)
        # direction doesn't matter if the length is zero
        if self._length == 0:
            self._dir = np.zeros(3)
        else:
            self._dir = v / self._length
        with np.errstate(divide='ignore'):
            self._invdir = 1/self._dir  # vector is opposite of vector dir
        self._sign = [0, 0, 0]
        self._sign[0] = int((self._invdir[0] < 0))
        self._sign[1] = int((self._invdir[1] < 0))
        self._sign[2] = int((self._invdir[2] < 0))

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

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

import numbers
import importlib
from typing import Tuple, Optional, Any

pyvista_spec = importlib.util.find_spec("pyvista")
pyvista_found = pyvista_spec is not None
if pyvista_found:
    import pyvista


class Detector:
    """A location used to calculate exposure

    Parameters
    ----------
    x : float
        X coordinate of detector location in cartesian coordinates
    y : float
        Y coordinate of detector location in cartesian coordinates
    z : float
        Z coordinate of detector location in cartesian coordinates
    """

    '''
    Attributes
    ----------
    _location
    '''

    def __init__(self, x: float, y: float, z: float) -> None:
        if isinstance(x, numbers.Number) and \
            isinstance(y, numbers.Number) and \
                isinstance(z, numbers.Number):
            self.x: float = x
            self.y: float = y
            self.z: float = z
            self._location: Tuple[float, float, float] = (x, y, z)
        else:
            raise ValueError(f"Invalid coordinates: {x}, {y}, {z}")

    @property
    def location(self) -> Tuple[float, float, float]:
        """:class:`tuple` : The detector location in cartesian coordinates"""
        return self._location

    def draw(self) -> Optional[Any]:
        """Creates a display object

        Returns
        -------
        :class:`pyvista.PolyData`
            A degenerate line object representing the detector.
        """
        if pyvista_found:
            # this returns a degenerate line, equivalent to a point
            return pyvista.Line((self.x, self.y, self.z),
                                (self.x, self.y, self.z))

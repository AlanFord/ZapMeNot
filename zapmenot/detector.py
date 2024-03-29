import numbers
import importlib
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

    def __init__(self, x, y, z):
        if isinstance(x, numbers.Number) and \
            isinstance(y, numbers.Number) and \
                isinstance(z, numbers.Number):
            self.x = x
            self.y = y
            self.z = z
            self._location = (x, y, z)
        else:
            raise ValueError("Invalid coordinates:" + str(x) + ", " + str(y) +
                             ", " + str(z))

    @property
    def location(self):
        """:class:`tuple` : The detector location in cartesian coordinates"""
        return self._location

    def draw(self):
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

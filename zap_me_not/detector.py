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

    Attributes
    ----------
    location
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self._location = (x, y, z)

    @property
    def location(self):
        """:class:`tuple` : The detector location in cartesian coordinates"""
        return self._location
     
    def vtk(self):
        """Creates a display object

        Returns
        -------
        :class:`pyvista.PolyData`
            A small sphere object representing the detector.
        """
        if pyvista_found:
            return pyvista.Sphere(center=(self.x, self.y, self.z), radius=10)


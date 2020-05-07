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
     

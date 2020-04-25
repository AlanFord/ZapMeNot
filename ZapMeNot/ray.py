import numpy as np


class FiniteLengthRay:
    '''
    The FiniteLengthRay object represents a ray in three-space
    with a defined starting point, a defined end, and a resulting
    direction.

    Args:
        start (list): A list or tuple defining the starting point of the ray in cartesian coordinates
        end (list): A list or tuple defining the ending point of the ray in cartesian coordinates.

    Attributes:
        length(float): The length of the ray
        dir(:class:`numpy.ndarray`): A numpy vector holding the vector normal of the ray
    '''
    def __init__(self, start, end):
        self._start = start
        self._end = end
        self._regularize()

    @property
    def start(self):
        """list: A list defining the starting point of the ray in cartesian coordinates."""
        return self._start
    
    @start.setter
    def start(self, value):
        self._start = value
        self._regularize()

    @property
    def end(self):
         """list: A list defining the ending point of the ray in cartesian coordinates."""
         return self._end

    @end.setter
    def end(self, value):
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
        print("dir is ",self.dir)
        with np.errstate(divide='ignore'):
            self.invdir = 1/self.dir  # vector is opposite of vector dir
        self.sign = [0, 0, 0]
        self.sign[0] = int((self.invdir[0] < 0))
        self.sign[1] = int((self.invdir[1] < 0))
        self.sign[2] = int((self.invdir[2] < 0))

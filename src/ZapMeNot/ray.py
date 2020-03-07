import numpy as np

class Ray:
	def __init__(self, start, end):
		self.start = start
		self.end = end
		self.origin = np.array(start)
		v = np.array(self.end) - self.origin
		self.length = np.linalg.norm(v)
		self.dir = v / self.length
		with np.errstate(divide='ignore'):
			self.invdir = 1/self.dir  # vector is opposite of vector dir
		self.sign = [0,0,0]
		self.sign[0] = int((self.invdir[0] < 0))
		self.sign[1] = int((self.invdir[1] < 0))
		self.sign[2] = int((self.invdir[2] < 0))



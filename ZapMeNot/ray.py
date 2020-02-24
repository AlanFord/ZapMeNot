import numpy as np

class Ray:
	def __init__(self):
		self.start = np.array([0,0,0])
		self.end = np.array([0,0,0])

	def length(self):
		return np.linalg.norm(self.end - self.start)

	def unitVector(self):
		a = self.end - self.start
		return  a / np.linalg.norm(a)



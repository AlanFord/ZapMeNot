import numpy as np

class Ray:
	def __init__(self):
		self.start = [0,0,0]
		self.end = [0,0,0]

	def length(self):
		return np.linalg.norm(np.array(self.end) - np.array(self.start))

	def unitVector(self):
		a = np.array(self.end) - np.array(self.start)
		return  (a / np.linalg.norm(a))



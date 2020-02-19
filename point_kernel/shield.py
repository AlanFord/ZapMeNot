import numpy as np
import abc

class Shield:
	'''Abtract class to model a shield.'''

	def __init__(self, materialName="void"):
		'''Initialize the Shield with a void material 
		and photon list'''
		self.material=Material(materialName)

	@abc.abstractproperty
	def getCrossingLength(self,vector):
		'''returns a  crossing length'''
		pass

	@abc.abstractproperty
	def getCrossingMFP(self,vector, photonEnergy):
		'''returns the crossing mfp'''
		pass

	def LinePlaneCollision(self, planeNormal, planePoint, rayDirection, rayPoint, epsilon=1e-6):
	 
		ndotu = planeNormal.dot(rayDirection)
		if abs(ndotu) < epsilon:
			raise RuntimeError("no intersection or line is within plane")
	 
		w = rayPoint - planePoint
		si = -planeNormal.dot(w) / ndotu
		Psi = w + si * rayDirection + planePoint
		return Psi



class XInfiniteSlab:
	''' Infinite slab shield perpendicular to the X axis'''

	def __init__(self, materialName, xStart, xEnd):
		'''Initialize material composition and location of the slab shield'''
		super.__init__(materialName)
		self.xStart = xStart
		self.xEnd = xEnd

	def getCrossingLength(self,vector):
		'''returns a  crossing length'''
		rayPoint = np.array(vector[1])
		rayNormal = np.array(vector[2])
		# get one crossing point
		planeNormal = np.array([1,0,0])
		planePoint = np.array([xStart,0,0])
		firstPoint = self.LinePlaneCollision(planeNormal, planePoint, rayDirection, rayPoint)
		# get second crossing point
		planeNormal = np.array([1,0,0])
		planePoint = np.array([xEnd,0,0])
		secondPoint = self.LinePlaneCollision(planeNormal, planePoint, rayDirection, rayPoint)
		# let numpy do the heavy lifting
		return np.linalg.norm(secondPoint-firstPoint)

	def getCrossingMFP(self,vector, photonEnergy):
		'''returns the crossing mfp'''
		distance = getCrossingLength(vector)
		return material.getMfp(photonEnergy, distance)


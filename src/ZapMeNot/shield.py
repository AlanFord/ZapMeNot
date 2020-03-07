import numpy as np
import abc
from ZapMeNot import material
# import material

class Shield:
	'''Abtract class to model a shield.'''

	def __init__(self, materialName, density=None, **kwargs):
		'''Initialize the Shield with a void material 
		and photon list'''
		self.material=material.Material(materialName)
		if density != None:
			self.material.setDensity(density)
		super().__init__(**kwargs)

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



class SemiInfiniteXSlab(Shield):
	''' Infinite slab shield perpendicular to the X axis'''

	def __init__(self, materialName, xStart, xEnd):
		'''Initialize material composition and location of the slab shield'''
		super().__init__(materialName)
		self.xStart = xStart
		self.xEnd = xEnd

	def getCrossingLength(self,ray):
		'''returns a  crossing length'''
		rayPoint = ray.origin
		rayUnitVector = ray.dir
		planeNormal = np.array([1,0,0])
		# get one crossing point
		planePoint = np.array([self.xStart,0,0])
		firstPoint = self.LinePlaneCollision(planeNormal, planePoint, rayUnitVector, rayPoint)
		# get second crossing point
		planePoint = np.array([self.xEnd,0,0])
		secondPoint = self.LinePlaneCollision(planeNormal, planePoint, rayUnitVector, rayPoint)
		# let numpy do the heavy lifting
		return np.linalg.norm(secondPoint-firstPoint)

	def getCrossingMFP(self,vector, photonEnergy):
		'''returns the crossing mfp'''
		distance = self.getCrossingLength(vector)
		return self.material.getMfp(photonEnergy, distance)

class Box(Shield):
	'''Axis-Aligned rectangular box'''
	def __init__(self, materialName, boxCenter, boxDimensions):
		'''Initialize material composition and location of the slab shield'''
		super().__init__(materialName)
		self.boxCenter = np.array(boxCenter)
		self.boxDimensions = np.array(boxDimensions)

	def getCrossingMFP(self,vector, photonEnergy):
		'''returns the crossing mfp'''
		distance = self.getCrossingLength(vector)
		return self.material.getMfp(photonEnergy, distance)

	def getCrossingLength(self,ray):
		'''returns a  crossing length'''
		rayPoint = ray.origin
		rayUnitVector = ray.dir
		planeNormal = np.array([1,0,0])
		# get a list of crossing points
		crossings = intersectAABox(ray)
		# two crossings indicates a full-shield crossing
		# one crossing indicates that either (common) the source is
		#    in the shield or (uncommon) the dose point is in the
		#    shield
		# zero crossings can indicate that either both source and
		#    dose points are in the shield or that the shield is
		#    missed entirely
		if len(crossings) != 2:
			if contains(ray.origin):
				crossings.insert(0,ray.origin)
			if len(crossings) != 2:
				if contains(np.array(ray.end)):
					crossings.append(np.array(ray.end))
			if len(crossings) != 2:
				raise ValueError("Shield doesn't have 2 crossings")
		# let numpy do the heavy lifting
		return np.linalg.norm(crossings[1]-crossings[2])

	def contains(self,point):
		x = point[0]
		y = point[1]
		z = point[2]
		xmin = self.boxCenter[0]-self.boxDimensions[0]
		xmax = self.boxCenter[0]+self.boxDimensions[0]
		ymin = self.boxCenter[1]-self.boxDimensions[1]
		ymax = self.boxCenter[1]+self.boxDimensions[1]
		zmin = self.boxCenter[2]-self.boxDimensions[2]
		zmax = self.boxCenter[2]+self.boxDimensions[2]
		if (xmin<=x and x<=xmax and ymin<=y and y<=ymax and zmin<=z and z<=zmax):
			return true
		return false


	def intersectAABox(self, ray):
		'returns 0, 1, or 2 points of intersection'
		results = []
		bounds = [self.boxCenter - (self.boxDimensions/2), self.boxCenter + (self.boxDimensions/2)]
		tmin =  (bounds[  ray.sign[0]][0] - ray.origin[0]) * ray.invdir[0]
		tmax =  (bounds[1-ray.sign[0]][0] - ray.origin[0]) * ray.invdir[0]
		tymin = (bounds[  ray.sign[1]][1] - ray.origin[1]) * ray.invdir[1]
		tymax = (bounds[1-ray.sign[1]][1] - ray.origin[1]) * ray.invdir[1]


		if ((tmin > tymax) or (tymin > tmax)):
			return results

		if (tymin > tmin):
			tmin = tymin;
		if (tymax < tmax):
			tmax = tymax

		tzmin = (bounds[  ray.sign[2]][2] - ray.origin[2]) * ray.invdir[2]
		tzmax = (bounds[1-ray.sign[2]][2] - ray.origin[2]) * ray.invdir[2]

		if ((tmin > tzmax) or (tzmin > tmax)):
			return results

		if (tzmin > tmin): 
			tmin = tzmin

		if (tzmax < tmax): 
			tmax = tzmax
	 
		if (tmin >= 0 and tmin<=ray.length):
			results.append(ray.origin + ray.dir*tmin)
		if (tmax >= 0 and tmax<=ray.length):
			results.append(ray.origin + ray.dir*tmax)

		return results



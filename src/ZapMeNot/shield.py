import numpy as np
import abc
from ZapMeNot import material
import math
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

class Sphere(Shield):
	def __init__(self, materialName='', sphereCenter=[0,0,0], sphereRadius=1):
		'''Initialize material composition and location of the slab shield'''
		super().__init__(materialName)
		self.center = np.array(sphereCenter)
		self.radius = np.array(sphereRadius)

	def getCrossingMFP(self,vector, photonEnergy):
		'''returns the crossing mfp'''
		distance = self.getCrossingLength(vector)
		return self.material.getMfp(photonEnergy, distance)

	def getCrossingLength(self,ray):
		L = self.origin - ray.origin
		tca = np.dot(L, ray.dir)
		if tca < 0:
			return 0
		dSquared = np.dot(L,L)-tca**2
		if dSquared<0 or dSquared>self.radius**2:
			return 0
		thc = np.sqrt(self.radius**2 - dSquared)
		return thc*2

	def contains(self,point):
		vector = point - self.center
		if np.cross(vector,vector) > self.radius**2:
			return False
		return True


class Box(Shield):
	'''Axis-Aligned rectangular box'''
	def __init__(self, materialName='', boxCenter=[0,0,0], boxDimensions=[0,0,0]):
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
		return np.linalg.norm(crossings[0]-crossings[1])

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

class CappedCylinder(Shield):
	'''General Cylinder'''
	def __init__(self, materialName='', cylinderStart=[0,0,0], cylinderEnd=[0,0,0], cylinderRadius=1):
		'''Initialize material composition and location of the shield'''
		super().__init__(materialName)
		self.radius = cylinderRadius
		self.origin = np.array(cylinderStart)
		self.end = np.array(cylinderEnd)
		self.length = np.linalg.norm(self.end - self.origin)
		self.dir = (self.end - self.origin)/self.length

	def getCrossingMFP(self,vector, photonEnergy):
		'''returns the crossing mfp'''
		distance = self.getCrossingLength(vector)
		return self.material.getMfp(photonEnergy, distance)

	def getCrossingLength(self,ray):
		'''returns a  crossing length'''
		# get a list of crossing points
		crossings = self.intersect(ray)
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
		return np.linalg.norm(crossings[0]-crossings[1])

	def contains(self,point):
		# determine scalar projection of point on cylinder centerline
		rando = np.dot(point-self.origin, self.dir)
		if rando < 0 or rando > self.length:
			return False
		# check the radial distance from cylinder centerline
		parto = (self.origin+self.dir*rando) - point
		if np.dot(parto,parto) > self.radius**2:
			return False
		return True

	def intersect(self, ray):
		# based on https://mrl.nyu.edu/~dzorin/rend05/lecture2.pdf
		# and
		# https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-plane-and-ray-disk-intersection
		results = []
		# test for 
		deltap = ray.origin - self.origin
		part1 = ray.dir -(np.dot(ray.dir, self.dir)*self.dir)
		part2 = deltap - (np.dot(deltap, self.dir)*self.dir)
		a = np.dot(part1, part1)
		b = 2*np.dot(part1, part2)
		c = np.dot(part2, part2) - self.radius**2
		zoro = b**2 - 4*a*c
		if (zoro > 0):
			# roots are real, thee are two intersections on an "infinite" cylinder
			meo = math.sqrt(zoro)
			t1 = (-b + meo)/(2*a)
			t2 = (-b - meo)/(2*a)
			# check to see if the intersections occur in the finite length of the cylinder
			for t in [t1,t2]:
				intersection = ray.origin + ray.dir*t
				loc = np.dot(intersection-self.origin, self.dir)
				if loc >=0 and loc < self.length:
					results.append(intersection)
		# check to see if there are intersections on the caps
		denom = np.dot(self.dir,ray.dir)
		if (denom > 1e-6):
			for testPoint in [self.origin, self.end]:
				t = np.dot(testPoint-ray.origin, self.dir)
				if t>= 0:
					strike = ray.origin + ray.dir*t
					v = strike - testPoint
					if np.dot(v,v) <= self.radius**2:
						results.append(strike)
		return results

class YAlignedCylinder(CappedCylinder):
	'''Y Axis-Aligned cylinder of finite length'''
	def __init__(self, materialName='', cylinderCenter=[0,0,0], cylinderLength=10, cylinderRadius=1):
		'''Initialize material composition and location of the shield'''
		cylinderStart = [cylinderCenter[0],cylinderCenter[1]-cylinderLength/2,cylinderCenter[2]]
		cylinderEnd   = [cylinderCenter[0],cylinderCenter[1]+cylinderLength/2,cylinderCenter[2]]
		super().__init__(materialName,cylinderStart=cylinderStart,cylinderEnd=cylinderEnd,cylinderRadius=cylinderRadius)

class XAlignedCylinder(CappedCylinder):
	'''Y Axis-Aligned cylinder of finite length'''
	def __init__(self, materialName='', cylinderCenter=[0,0,0], cylinderLength=10, cylinderRadius=1):
		'''Initialize material composition and location of the shield'''
		cylinderStart = [cylinderCenter[0]-cylinderLength/2,cylinderCenter[1],cylinderCenter[2]]
		cylinderEnd   = [cylinderCenter[0]+cylinderLength/2,cylinderCenter[1],cylinderCenter[2]]
		super().__init__(materialName,cylinderStart=cylinderStart,cylinderEnd=cylinderEnd,cylinderRadius=cylinderRadius)

class ZAlignedCylinder(CappedCylinder):
	'''Y Axis-Aligned cylinder of finite length'''
	def __init__(self, materialName='', cylinderCenter=[0,0,0], cylinderLength=10, cylinderRadius=1):
		'''Initialize material composition and location of the shield'''
		cylinderStart = [cylinderCenter[0],cylinderCenter[1],cylinderCenter[2]-cylinderLength/2]
		cylinderEnd   = [cylinderCenter[0],cylinderCenter[1],cylinderCenter[2]+cylinderLength/2]
		super().__init__(materialName,cylinderStart=cylinderStart,cylinderEnd=cylinderEnd,cylinderRadius=cylinderRadius)






import numpy as np
import abc
from ZapMeNot import material
import math
# import material

# -----------------------------------------------------------

class Shield:
	'''Abtract class to model a shield.'''

	def __init__(self, materialName=None, density=None, **kwargs):
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

	def LinePlaneCollision(self, planeNormal, planePoint, rayOrigin, rayNormal, epsilon=1e-6):	 
		# based on 
		# https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-plane-and-ray-disk-intersection
		ndotu = planeNormal.dot(rayNormal)
		if abs(ndotu) < epsilon:
			return None
		w = planePoint - rayOrigin
		t = w.dot(planeNormal)/ndotu
		return t

# -----------------------------------------------------------

class SemiInfiniteXSlab(Shield):
	''' Infinite slab shield perpendicular to the X axis'''

	def __init__(self, materialName, xStart, xEnd, density=None):
		'''Initialize material composition and location of the slab shield'''
		super().__init__(materialName=materialName, density=density)
		self.xStart = xStart
		self.xEnd = xEnd

	def getCrossingLength(self,ray):
		'''returns a  crossing length'''
		rayOrigin = ray.origin
		rayUnitVector = ray.dir
		planeNormal = np.array([1,0,0])
		# get length to one crossing point
		planePoint = np.array([self.xStart,0,0])
		firstLength = self.LinePlaneCollision(planeNormal, planePoint, rayOrigin, rayUnitVector)
		if firstLength == None:
			# ray is parallel to plane
			return 0
		# get length to second crossing point
		planePoint = np.array([self.xEnd,0,0])
		secondLength = self.LinePlaneCollision(planeNormal, planePoint, rayOrigin, rayUnitVector)
		if secondLength == None:
			# ray is parallel to plane
			return 0
		if (firstLength<0 and secondLength<0):
			# ray starts and ends entirely on one side of the shield
			return 0
		if (firstLength>ray.length and secondLength>ray.length):
			# ray starts and ends entirely on one side of the shield
			return 0
		# remainder of cases have some sort of partial or full crossing
		t0 = min(firstLength, secondLength)
		t1 = max(firstLength, secondLength)
		if ((t0<0) and (t1>ray.length)):
			# ray is intirely within the slab
			return ray.length
		if ((t0<0) and (t1<ray.length)):
			# ray start in slab and crosses out
			return t1
		if ((t0>0) and (t1>ray.length)):
			# ray starts outside slab and ends inside slab
			return ray.length - t0
		# we are left with a full crossing
		return t1 - t0

	def getCrossingMFP(self,vector, photonEnergy):
		'''returns the crossing mfp'''
		distance = self.getCrossingLength(vector)
		return self.material.getMfp(photonEnergy, distance)

# -----------------------------------------------------------

class Sphere(Shield):
	def __init__(self, materialName, sphereCenter, sphereRadius, density=None):
		'''Initialize material composition and location of the slab shield'''
		super().__init__(materialName=materialName, density=density)
		self.center = np.array(sphereCenter)
		self.radius = np.array(sphereRadius)

	def getCrossingMFP(self,vector, photonEnergy):
		'''returns the crossing mfp'''
		distance = self.getCrossingLength(vector)
		return self.material.getMfp(photonEnergy, distance)

	def getCrossingLength(self,ray):
		# based on 
		# http://viclw17.github.io/2018/07/16/raytracing-ray-sphere-intersection/
		a = np.dot(ray.dir, ray.dir)
		b = 2 * np.dot(ray.dir, ray.origin - self.center)
		c = np.dot(ray.origin-self.center, ray.origin-self.center)- self.radius**2
		discriminant = b**2 - 4*a*c
		if discriminant <= 0:
			# sphere is missed or tangent
			return 0
		root = np.sqrt(discriminant)
		t0 = (-b -root)/(2*a)
		t1 = (-b +root)/(2*a)
		bigList = []
		for aLength in [t0, t1]:
			if (aLength>=0 and aLength<=ray.length):
				bigList.append(aLength)
		if len(bigList) != 2:
			# if not 2 intersections, look for ray endpoints inside the sphere
			if self.contains(ray.origin):
				bigList.append(0)
			if self.contains(ray.end):
				bigList.append(ray.length)
		if len(bigList) ==0:
			# ray misses the sphere
			return 0
		if len(bigList) !=2:
			# this shouldn't occur
			raise ValueError("Shield doesn't have 2 crossings")
		return abs(bigList[1]-bigList[0])

	def contains(self,point):
		vector = point - self.center
		if np.dot(vector,vector) > self.radius**2:
			return False
		return True

# -----------------------------------------------------------

class Box(Shield):
	'''Axis-Aligned rectangular box'''
	def __init__(self, materialName, boxCenter, boxDimensions, density=None):
		'''Initialize material composition and location of the slab shield'''
		super().__init__(materialName=materialName, density=density)
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
		crossings = self.intersectAABox(ray)
		# two crossings indicates a full-shield crossing
		# one crossing indicates that either (common) the source is
		#    in the shield or (uncommon) the dose point is in the
		#    shield
		# zero crossings can indicate that either both source and
		#    dose points are in the shield or that the shield is
		#    missed entirely
		if len(crossings) != 2:
			# check for start/end of ray within the box
			if self.contains(ray.origin):
				crossings.insert(0,ray.origin)
			if self.contains(np.array(ray.end)):
				crossings.append(np.array(ray.end))
		if len(crossings) == 0:
			# likely it's a complete miss
			return 0
		if len(crossings) != 2:
			# shouldn't ever get here
			raise ValueError("Shield doesn't have 2 crossings")
		# let numpy do the heavy lifting
		return np.linalg.norm(crossings[0]-crossings[1])

	def contains(self,point):
		x = point[0]
		y = point[1]
		z = point[2]
		xmin = self.boxCenter[0]-self.boxDimensions[0]/2
		xmax = self.boxCenter[0]+self.boxDimensions[0]/2
		ymin = self.boxCenter[1]-self.boxDimensions[1]/2
		ymax = self.boxCenter[1]+self.boxDimensions[1]/2
		zmin = self.boxCenter[2]-self.boxDimensions[2]/2
		zmax = self.boxCenter[2]+self.boxDimensions[2]/2
		if (xmin<=x and x<=xmax and ymin<=y and y<=ymax and zmin<=z and z<=zmax):
			return True
		return False

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

# -----------------------------------------------------------

class InfiniteAnnulus(Shield):
	def __init__(self, materialName, cylinderOrigin, cylinderAxis, cylinderInnerRadius, cylinderOuterRadius, density=None):
		'''Initialize material composition and location of the shield'''
		super().__init__(materialName=materialName, density=density)
		self.innerRadius = cylinderInnerRadius
		self.outerRadius = cylinderOuterRadius
		self.origin = np.array(cylinderOrigin)
		axis = np.array(cylinderAxis)
		self.dir = axis/np.linalg.norm(axis)

	def getCrossingMFP(self,vector, photonEnergy):
		'''returns the crossing mfp'''
		distance = self.getCrossingLength(vector)
		return self.material.getMfp(photonEnergy, distance)

	def getCrossingLength(self,ray):
		'''returns a  crossing length'''
		# get a list of crossing points
		crossings = self.intersect(ray)
		# zero crossings can indicate that either both source and
		#    dose points are in the shield or that the shield is
		#    missed entirely
		# one crossing indicates that either (common) the source is
		#    in the shield or (uncommon) the dose point is in the
		#    shield
		# two crossings indicates a single in/out or out/in crossing
		# four crossings indicate a full-shield crossing
		if len(crossings) not in [2,4]:
			if self.contains(ray.origin):
				crossings.append(0)
			if self.contains(np.array(ray.end)):
				crossings.append(ray.length)
		if len(crossings) == 0:
			return 0
		if len(crossings) not in [2,4]:
			raise ValueError("Shield doesn't have valid crossings")
		crossings.sort()
		if len(crossings) == 2:
			return crossings[1]-crossings[0]
		if len(crossings) == 4:
			# let numpy do the heavy lifting
			return (crossings[1]-crossings[0]) + (crossings[3] - crossings[2])

	def contains(self,point):
		# determine scalar projection of point on cylinder centerline
		rando = np.dot(point-self.origin, self.dir)
		# check the radial distance from cylinder centerline
		parto = (self.origin+self.dir*rando) - point
		if (np.dot(parto,parto) < self.innerRadius**2) or (np.dot(parto,parto) > self.outerRadius**2):
			return False
		return True

	def intersect(self, ray):
		# returns a list of >>DISTANCES<< olong the ray vector
		#
		# based on https://mrl.nyu.edu/~dzorin/rend05/lecture2.pdf
		# and
		# https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-plane-and-ray-disk-intersection
		results = []
		for radius in [self.innerRadius, self.outerRadius]:
			deltap = ray.origin - self.origin
			part1 = ray.dir -(np.dot(ray.dir, self.dir)*self.dir)
			part2 = deltap - (np.dot(deltap, self.dir)*self.dir)
			a = np.dot(part1, part1)
			b = 2*np.dot(part1, part2)
			c = np.dot(part2, part2) - radius**2
			zoro = b**2 - 4*a*c
			if (zoro > 0):
				# roots are real, then are two intersections on an "infinite" cylinder
				meo = math.sqrt(zoro)
				t1 = (-b + meo)/(2*a)
				t2 = (-b - meo)/(2*a)
				# check to see if the intersections occur in the finite length of the cylinder
				for t in [t1,t2]:
					# discard line/cylinder intersections outside of the length of the ray
					if t >=0 and t <=ray.length:
						results.append(t)
		return results
# -----------------------------------------------------------

class YAlignedInfiniteAnnulus(InfiniteAnnulus):
	'''Y Axis-Aligned cylinder of finite length'''
	def __init__(self, materialName, cylinderCenter, cylinderInnerRadius, cylinderOuterRadius, density=None):
		'''Initialize material composition and location of the shield'''
		super().__init__(materialName=materialName, density=density,cylinderOrigin=cylinderCenter, \
			cylinderInnerRadius=cylinderInnerRadius,cylinderOuterRadius=cylinderOuterRadius, cylinderAxis=[0,1,0])

# -----------------------------------------------------------

class XAlignedInfiniteAnnulus(InfiniteAnnulus):
	'''X Axis-Aligned cylinder of finite length'''
	def __init__(self, materialName, cylinderCenter, cylinderInnerRadius, cylinderOuterRadius, density=None):
		'''Initialize material composition and location of the shield'''
		super().__init__(materialName=materialName, density=density,cylinderOrigin=cylinderCenter, \
			cylinderInnerRadius=cylinderInnerRadius,cylinderOuterRadius=cylinderOuterRadius, cylinderAxis=[1,0,0])

# -----------------------------------------------------------

class ZAlignedInfiniteAnnulus(InfiniteAnnulus):
	'''Z Axis-Aligned cylinder of finite length'''
	def __init__(self, materialName, cylinderCenter, cylinderInnerRadius, cylinderOuterRadius, density=None):
		'''Initialize material composition and location of the shield'''
		super().__init__(materialName=materialName, density=density,cylinderOrigin=cylinderCenter, \
			cylinderInnerRadius=cylinderInnerRadius,cylinderOuterRadius=cylinderOuterRadius, cylinderAxis=[0,0,1])

# -----------------------------------------------------------

class CappedCylinder(Shield):
	'''General Cylinder'''
	def __init__(self, materialName, cylinderStart, cylinderEnd, cylinderRadius, density=None):
		'''Initialize material composition and location of the shield'''
		super().__init__(materialName=materialName, density=density)
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
			# check for start/end of ray within the cylinder
			if self.contains(ray.origin):
				crossings.insert(0,ray.origin)
			if self.contains(np.array(ray.end)):
				crossings.append(np.array(ray.end))
		if len(crossings) == 0:
			# likely it's a complete miss
			return 0
		if len(crossings) != 2:
			# shouldn't ever get here
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
			# roots are real, then are two intersections on an "infinite" cylinder
			meo = math.sqrt(zoro)
			t1 = (-b + meo)/(2*a)
			t2 = (-b - meo)/(2*a)
			# check to see if the intersections occur in the finite length of the cylinder
			for t in [t1,t2]:
				# discard line/cylinder intersections outside of the length of the ray
				if t >=0 and t <=ray.length:
					intersection = ray.origin + ray.dir*t
					loc = np.dot(intersection-self.origin, self.dir)
					# keep only intersections within the finite length of the cylinder
					if loc >=0 and loc < self.length:
						results.append(intersection)
		# check to see if there are intersections on the caps
		for diskCenter in [self.origin, self.end]:
			t = self.LinePlaneCollision(self.dir, diskCenter, ray.origin, ray.dir)
			if t != None and t>=0 and t<=ray.length:
				point = ray.origin + ray.dir*t
				radial = point - diskCenter
				if radial.dot(radial) < self.radius**2:
					results.append(point)
		return results

# -----------------------------------------------------------

class YAlignedCylinder(CappedCylinder):
	'''Y Axis-Aligned cylinder of finite length'''
	def __init__(self, materialName, cylinderCenter, cylinderLength, cylinderRadius, density=None):
		'''Initialize material composition and location of the shield'''
		cylinderStart = [cylinderCenter[0],cylinderCenter[1]-cylinderLength/2,cylinderCenter[2]]
		cylinderEnd   = [cylinderCenter[0],cylinderCenter[1]+cylinderLength/2,cylinderCenter[2]]
		super().__init__(materialName=materialName, density=density,cylinderStart=cylinderStart,cylinderEnd=cylinderEnd,cylinderRadius=cylinderRadius)

# -----------------------------------------------------------

class XAlignedCylinder(CappedCylinder):
	'''X Axis-Aligned cylinder of finite length'''
	def __init__(self, materialName, cylinderCenter, cylinderLength, cylinderRadius, density=None):
		'''Initialize material composition and location of the shield'''
		cylinderStart = [cylinderCenter[0]-cylinderLength/2,cylinderCenter[1],cylinderCenter[2]]
		cylinderEnd   = [cylinderCenter[0]+cylinderLength/2,cylinderCenter[1],cylinderCenter[2]]
		super().__init__(materialName=materialName, density=density,cylinderStart=cylinderStart,cylinderEnd=cylinderEnd,cylinderRadius=cylinderRadius)

# -----------------------------------------------------------

class ZAlignedCylinder(CappedCylinder):
	'''Z Axis-Aligned cylinder of finite length'''
	def __init__(self, materialName, cylinderCenter, cylinderLength, cylinderRadius, density=None):
		'''Initialize material composition and location of the shield'''
		cylinderStart = [cylinderCenter[0],cylinderCenter[1],cylinderCenter[2]-cylinderLength/2]
		cylinderEnd   = [cylinderCenter[0],cylinderCenter[1],cylinderCenter[2]+cylinderLength/2]
		super().__init__(materialName=materialName, density=density,cylinderStart=cylinderStart,cylinderEnd=cylinderEnd,cylinderRadius=cylinderRadius)






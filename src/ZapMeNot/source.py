from ZapMeNot import shield, isotope
import abc
import numpy as np

class Source(metaclass=abc.ABCMeta):
	'''Abtract class to model a radiation source.  Maintains a list of
	isotopes and can returna list of point source locations within the
	body of the Source'''

	def __init__(self, **kwargs):
		'''Initialize the Source with empty strings for the isotope list 
		and photon list'''
		self.isotopeList=[]   # LIST of isotopes and activities (Bq)
		self.uniquePhotons=[] # LIST of unique photons and activities (Bq)
		self.pointsPerDimension=[10,10,10]
		super().__init__(**kwargs)

	def addIsotopeCuries(self, newIsotope, curies):
		"add an isotope and activity to the isotope list"
		self.isotopeList.append( (newIsotope, curies*3.7E10) ) # LIST of tuples, isotope object and activity

	def addIsotopeBq(self, newIsotope, becquerels):
		"add an isotope and activity to the isotope list"
		self.isotopeList.append( (newIsotope, becquerels) ) # LIST of tuples, isotope object and activity
		
	def addPhoton(self, energy, becquerels):
		"add a photon and activity to the photon list"
		self.uniquePhotons.append( (energy, becquerels) )

	def listIsotopes(self):
		# echo back a list of the isotopes currently stored
		return self.isotopeList

	def listUniquePhotons(self):
		return self.uniquePhotons

	def getPhotonSourceList(self):
		"returns a list of unique photon energies and activities"
		photonDict = dict()
		keys = photonDict.keys()
		# test to see if photon energy is already on the list
		# and then add photon emmision rate (intensity*Bq)
		for nextIsotope in self.isotopeList: #nextIsotope will be a tuple of name and Bq
			isotopeDetail = isotope.Isotope(nextIsotope[0])
			for photon in isotopeDetail.photons:
				if photon[0] in keys:
					photonDict[photon[0]] = photonDict[photon[0]] + photon[1]*nextIsotope[1]
				else :
					photonDict[photon[0]] = photon[1]*nextIsotope[1]
		for photon in self.uniquePhotons:
			if photon[0] in keys:
				photonDict[photon[0]] = photonDict[photon[0]] + photon[1]
			else :
				photonDict[photon[0]] = photon[1]
		photonList = []
		scalingFactor = np.prod(self.pointsPerDimension)
		for key,value in photonDict.items():
			photonList.append((key,value/scalingFactor))
		return sorted(photonList)

	@abc.abstractproperty
	def getSourcePoints(self):
		pass

# -----------------------------------------------------------

class PointSource(Source, shield.Shield):
	'''Modeling a point source of radiation.'''
	def __init__(self,x=0,y=0,z=0, **kwargs):
		'''Initialize with an x,y,z location in space'''
		"Initialize"
		self.x = x
		self.y = y
		self.z = z
		# let the point source have a dummy material of air at a zero density
		kwargs['materialName'] = 'air'
		kwargs['density'] = 0
		super().__init__(**kwargs)
		self.pointsPerDimension=[1,1,1]

	def getSourcePoints(self):
		return[(self.x,self.y,self.z)]

	def getCrossingLength(self,vector):
		'''returns a  crossing length'''
		return 0

	def getCrossingMFP(self,vector, photonEnergy):
		'''returns the crossing mfp'''
		return 0

# -----------------------------------------------------------

class SphereSource(Source, shield.Sphere):
	'''Axis-Aligned rectangular box source'''
	# initialize with boxCenter, boxDimensions, material(optional), density(optional)

	def __init__(self,**kwargs):
		'''Initialize with an x,y,z location in space'''
		# let the point source have a dummy material of air at a zero density
		kwargs['materialName'] = 'air'
		# kwargs['density'] = 0
		super().__init__(**kwargs)

	def getSourcePoints(self):

		# calculate the radius of each "equal area" annular region
		totalVolume = 4/3*pi()*self.radius**3
		annularVolume = totalVolume/self.pointsPerDimension[0]
		oldRadius = 0
		annularLocations = []
		for i in range(self.pointsPerDimension[0]):
			newRadius = math.sqrt((runningArea+annularArea)/math.pi)
			annularLocations.append((newRadius+oldRadius)/2)
			oldRadius = newRadius

		angleIncrement = 2*math.py/self.pointsPerDimension[1]
		startAngle = angleIncrement/2
		angleLocations = []
		for i in range(self.pointsPerDimension[1]):
			angleLocations.append(startAngle+ (i*angleIncrement))

		lengthIncrement = self.length/self.pointsPerDimension[2]
		startLength = lengthIncrement/2
		lengthLocations = []
		for i in range(self.pointsPerDimension[2]):
			lengthLocations.append(startLength+ (i*lengthIncrement))


		# iterate through each dimension, building a list of source points
		sourcePoints = []
		for radialLocation in annularLocations:
			r = radialLocation
			for angleLocation in angleLocations:
				theta = angleLocation
				for lengthLocation in lengthLocations:
					z = lengthLocation
					# convert cylintrical to rectangular coordinates
					x = r * math.cos(theta)
					y = r * math.sin(theta)
					sourcePoints.append([x,y,z])
		return sourcePoints

# -----------------------------------------------------------

class BoxSource(Source, shield.Box):
	'''Axis-Aligned rectangular box source'''
	# initialize with boxCenter, boxDimensions, material(optional), density(optional)

	def __init__(self,**kwargs):
		'''Initialize with an x,y,z location in space'''
		# let the point source have a dummy material of air at a zero density
		kwargs['materialName'] = 'air'
		# kwargs['density'] = 0
		super().__init__(**kwargs)

	def getSourcePoints(self):
		sourcePoints = []
		meshWidth = self.boxDimensions/self.pointsPerDimension
		print(meshWidth)
		startPoint = self.boxCenter-(self.boxDimensions)/2+(meshWidth/2)
		for i in range(self.pointsPerDimension[0]):
			x = startPoint[0]+meshWidth[0]*i
			for j in range(self.pointsPerDimension[1]):
				y = startPoint[1]+meshWidth[1]*j
				for k in range(self.pointsPerDimension[2]):
					z = startPoint[2]+meshWidth[2]*k
					sourcePoints.append([x,y,z])
		return sourcePoints

# -----------------------------------------------------------

class ZAlignedCylinderSource(Source, shield.ZAlignedCylinder):
	'''Axis-Aligned rectangular box source'''
	# initialize with cylinderCenter, cylinderLength, cylinderRadius, material(optional), density(optional)

	def __init__(self,**kwargs):
		'''Initialize with an x,y,z location in space'''
		# let the point source have a dummy material of air at a zero density
		kwargs['materialName'] = 'air'
		# kwargs['density'] = 0
		super().__init__(**kwargs)

	def getSourcePoints(self):

		# calculate the radius of each "equal area" annular region
		totalArea = pi()*self.radius**2
		annularArea = totalArea/self.pointsPerDimension[0]
		oldRadius = 0
		annularLocations = []
		for i in range(self.pointsPerDimension[0]):
			newRadius = math.sqrt((runningArea+annularArea)/math.pi)
			annularLocations.append((newRadius+oldRadius)/2)
			oldRadius = newRadius

		angleIncrement = 2*math.py/self.pointsPerDimension[1]
		startAngle = angleIncrement/2
		angleLocations = []
		for i in range(self.pointsPerDimension[1]):
			angleLocations.append(startAngle+ (i*angleIncrement))

		lengthIncrement = self.length/self.pointsPerDimension[2]
		startLength = lengthIncrement/2
		lengthLocations = []
		for i in range(self.pointsPerDimension[2]):
			lengthLocations.append(startLength+ (i*lengthIncrement))


		# iterate through each dimension, building a list of source points
		sourcePoints = []
		for radialLocation in annularLocations:
			r = radialLocation
			for angleLocation in angleLocations:
				theta = angleLocation
				for lengthLocation in lengthLocations:
					z = lengthLocation
					# convert cylintrical to rectangular coordinates
					x = r * math.cos(theta)
					y = r * math.sin(theta)
					sourcePoints.append([x,y,z])
		return sourcePoints

# -----------------------------------------------------------

class YAlignedCylinderSource(Source, shield.YAlignedCylinder):
	'''Axis-Aligned rectangular box source'''
	# initialize with cylinderCenter, cylinderLength, cylinderRadius, material(optional), density(optional)

	def __init__(self,**kwargs):
		'''Initialize with an x,y,z location in space'''
		# let the point source have a dummy material of air at a zero density
		kwargs['materialName'] = 'air'
		# kwargs['density'] = 0
		super().__init__(**kwargs)

	def getSourcePoints(self):

		# calculate the radius of each "equal area" annular region
		totalArea = pi()*self.radius**2
		annularArea = totalArea/self.pointsPerDimension[0]
		oldRadius = 0
		annularLocations = []
		for i in range(self.pointsPerDimension[0]):
			newRadius = math.sqrt((runningArea+annularArea)/math.pi)
			annularLocations.append((newRadius+oldRadius)/2)
			oldRadius = newRadius

		angleIncrement = 2*math.py/self.pointsPerDimension[1]
		startAngle = angleIncrement/2
		angleLocations = []
		for i in range(self.pointsPerDimension[1]):
			angleLocations.append(startAngle+ (i*angleIncrement))

		lengthIncrement = self.length/self.pointsPerDimension[2]
		startLength = lengthIncrement/2
		lengthLocations = []
		for i in range(self.pointsPerDimension[2]):
			lengthLocations.append(startLength+ (i*lengthIncrement))


		# iterate through each dimension, building a list of source points
		sourcePoints = []
		for radialLocation in annularLocations:
			r = radialLocation
			for angleLocation in angleLocations:
				theta = angleLocation
				for lengthLocation in lengthLocations:
					y = lengthLocation
					# convert cylintrical to rectangular coordinates
					x = r * math.cos(theta)
					z = r * math.sin(theta)
					sourcePoints.append([x,y,z])
		return sourcePoints

# -----------------------------------------------------------

class XAlignedCylinderSource(Source, shield.YAlignedCylinder):
	'''Axis-Aligned rectangular box source'''
	# initialize with cylinderCenter, cylinderLength, cylinderRadius, material(optional), density(optional)

	def __init__(self,**kwargs):
		'''Initialize with an x,y,z location in space'''
		# let the point source have a dummy material of air at a zero density
		kwargs['materialName'] = 'air'
		# kwargs['density'] = 0
		super().__init__(**kwargs)

	def getSourcePoints(self):

		# calculate the radius of each "equal area" annular region
		totalArea = pi()*self.radius**2
		annularArea = totalArea/self.pointsPerDimension[0]
		oldRadius = 0
		annularLocations = []
		for i in range(self.pointsPerDimension[0]):
			newRadius = math.sqrt((runningArea+annularArea)/math.pi)
			annularLocations.append((newRadius+oldRadius)/2)
			oldRadius = newRadius

		angleIncrement = 2*math.py/self.pointsPerDimension[1]
		startAngle = angleIncrement/2
		angleLocations = []
		for i in range(self.pointsPerDimension[1]):
			angleLocations.append(startAngle+ (i*angleIncrement))

		lengthIncrement = self.length/self.pointsPerDimension[2]
		startLength = lengthIncrement/2
		lengthLocations = []
		for i in range(self.pointsPerDimension[2]):
			lengthLocations.append(startLength+ (i*lengthIncrement))


		# iterate through each dimension, building a list of source points
		sourcePoints = []
		for radialLocation in annularLocations:
			r = radialLocation
			for angleLocation in angleLocations:
				theta = angleLocation
				for lengthLocation in lengthLocations:
					x = lengthLocation
					# convert cylintrical to rectangular coordinates
					y = r * math.cos(theta)
					z = r * math.sin(theta)
					sourcePoints.append([x,y,z])
		return sourcePoints















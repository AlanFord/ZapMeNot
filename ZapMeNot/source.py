from ZapMeNot import shield, isotope
import abc

class Source(metaclass=abc.ABCMeta):
	'''Abtract class to model a radiation source.  Maintains a list of
	isotopes and can returna list of point source locations within the
	body of the Source'''

	def __init__(self):
		'''Initialize the Source with empty strings for the isotope list 
		and photon list'''
		self.isotopeList=[]   # LIST of isotopes and activities (Bq)
		self.uniquePhotons=[] # LIST of unique photons and activities (Bq)

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

	@abc.abstractproperty
	def interateSourcePoints(self):
		pass

	def getPhotonSourceList(self):
		"returns a dict of unique photon energies and activities"
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
		for key,value in photonDict.items():
			photonList.append((key,value))
		return photonList

	def __iter__(self):
		return SourceIterator(self.getPhotonEnergyList())

# -----------------------------------------------------------

class SourceIterator:
	def __init__(self, dictOfPhotons):
		self.dictionary = dictOfPhotons
		self.keys = self.dictionary.keys()
		self.index = 0

	def __next__(self):
		if self.index == len(self.keys):
			raise StopIteration()
		retValue = self.dictionary(self.keys[self.index])
		self.index += 1
		return retValue

# -----------------------------------------------------------

class PointSource(Source, shield.Shield):
	'''Modeling a point source of radiation.'''
	def __init__(self,x=0,y=0,z=0):
		'''Initialize with an x,y,z location in space'''
		"Initialize"
		self.x = x
		self.y = y
		self.z = z
		super().__init__()

	def interateSourcePoints(self):
		pass

# -----------------------------------------------------------

# class LineSource(Source):
# 	"""Modeling a finite-length line source of radiation."""
# 	pass

# class PlaneSource(Source):
# 	"""Modeling a finite-area planar source of radiation."""
# 	pass
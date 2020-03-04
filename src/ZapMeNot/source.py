from ZapMeNot import shield, isotope
import abc

class Source(metaclass=abc.ABCMeta):
	'''Abtract class to model a radiation source.  Maintains a list of
	isotopes and can returna list of point source locations within the
	body of the Source'''

	def __init__(self, **kwargs):
		'''Initialize the Source with empty strings for the isotope list 
		and photon list'''
		self.isotopeList=[]   # LIST of isotopes and activities (Bq)
		self.uniquePhotons=[] # LIST of unique photons and activities (Bq)
		super().__init__(**kwargs)
		print("Initializing Source")

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
		for key,value in photonDict.items():
			photonList.append((key,value))
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
		print("Initializing PointSource")

	def getSourcePoints(self):
		return[(self.x,self.y,self.z)]

	def getCrossingLength(self,vector):
		'''returns a  crossing length'''
		return 0

	def getCrossingMFP(self,vector, photonEnergy):
		'''returns the crossing mfp'''
		return 0

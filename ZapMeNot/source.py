from shield import Shield
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
		self.isotopeList.add( (newIsotope, curies*3.7E10) ) # LIST of tuples, isotope object and activity

	def addIsotopeCuries(self, newIsotope, becquerels):
		"add an isotope and activity to the isotope list"
		self.isotopeList.add( (newIsotope, bequerells) ) # LIST of tuples, isotope object and activity
		
	def addPhoton(self, energy, becquerels):
		"add a photon and activity to the photon list"
		self.photonList.add( (energy, bequerells) )

	def listIsotopes(self):
		"echo back a list of the isotopes currently stored"
		return self.isotopeList

	@abc.abstractproperty
	def interateSourcePoints(self):
		pass

	def getPhotonEnergyList()
		"returns a dict of unique photon energies and activities"
		photonDict = dict()
		keys = dict.keys()
		# test to see if photon energy is already on the list
		# and then add photon emmision rate (intensity*Bq)
		for isotope in isotopeList:
			for photon in isotope.photons:
				if photon(0) in keys:
					dict(photon(0)) = dict(photon(0)) + photon(1)*isotope(2)
				else :
					dict(photon(0)) = photon(1)*isotope(2)
		for photon in photonList:
			if photon(0) in keys:
				dict(photon(0)) = dict(photon(0)) + photon(1)
			else :
				dict(photon(0)) = photon(1)
		return photonDict





class PointSource(Source, Shield):
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

class LineSource(Source):
	"""Modeling a finite-length line source of radiation."""
	pass

class PlaneSource(Source):
	"""Modeling a finite-area planar source of radiation."""
	pass
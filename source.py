from shield import Shield
import abc

class Source(Shield, metaclass=abc.ABCMeta):
	"""Abtract class to model a radiation source."""

	def __init__(self):
		self.isotopeList=[]
		self.uniquePhotons=[]

	def addIsotopeCuries(self, name, curies):
		self.isotopeList.add( (newIsotope, curies*3.7E10) )
		
	def addPhoton(self, energy, bequerells):
		self.photonList.add( (energy, bequerells) )

	def listIsotopes(self):
		return self.isotopeList

	@abc.abstractproperty
	def interateSourcePoints(self):
		pass


class PointSource(Source):
	"""Modeling a point source of radiation."""
	def __init__(self,x=0,y=0,z=0):
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
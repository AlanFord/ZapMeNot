from ZapMeNot import model,source,shield,detector,ray,material
import math

class Model:
	def __init__(self):
		self.source = None
		self.shieldList = []
		self.detector = None
		self.buildupFactorMaterial = None
		self.conversionFactor = 1.835E-8 # used to calculate exposure from flux, MeV, and linear energy absorption coeff

	def addSource(self, newSource):
		self.source = newSource
		# don't forget that sources are shields too!
		self.shieldList.append(newSource)

	def addShield(self, newShield):
		self.shieldList.append(newShield)

	def addDetector(self, newDetector):
		self.detector = newDetector

	def setBuildupFactorMaterial(self, newMaterial):
		self.buildupFactorMaterial = newMaterial
	
	def calculateExposure(self):
		# flux by photon energy
		fluxByPhotonEnergy = []
		# get a list of photons (energy/intensity [gamma/sec]) from the source
		spectrum= self.source.getPhotonSourceList()
		sourcePoints = self.source.getSourcePoints()
		# iterate through the photons 
		for photon in spectrum:
			uncollidedFlux = 0
			totalFlux = 0
			photonEnergy = photon[0]
			photonYield = photon[1]
			# iterate through the source points
			for nextPoint in sourcePoints:
				# determine the vector from source to detector
				vector = ray.Ray()
				vector.start = nextPoint
				vector.end = self.detector.location
				# vector = (nextPoint, self.detector.location)
				# iterate through the shield list
				totalMFP = 0.0
				for shield in self.shieldList:
					mfp = shield.getCrossingMFP(vector, photonEnergy)
					totalMFP += mfp
				totalFluxReductionFactor = math.exp(-totalMFP)
				buildupFactor = self.buildupFactorMaterial.getBuildupFactor(photonEnergy, totalMFP)
				uncollidedPointFlux = photonYield * totalFluxReductionFactor * (1/(4*math.pi*vector.length()**2))
				totalPointFlux = uncollidedPointFlux*buildupFactor
				uncollidedFlux += uncollidedPointFlux
				totalFlux += totalPointFlux
			fluxByPhotonEnergy.append([photonEnergy,uncollidedFlux,totalFlux])

		air = material.Material('air')
		results = 0	
		for photon in fluxByPhotonEnergy:
			photon.append(photon[2]*photon[0]*self.conversionFactor*air.getMassEnergyAbsCoff(photon[0]))
		# sum exposure over all photons
		exposureTotal = 0
		for photon in fluxByPhotonEnergy:
			exposureTotal += photon[3]
		return exposureTotal*1000*3600 # convert from R/sec to mR/hr

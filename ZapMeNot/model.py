class model:
	def __init__(self):
		self.source = None
		self.shieldList = []
		self.detector = None
		self.buildupFactorMaterial = None

	
	def calculateExposure(self):
		# flux by photon energy
		fluxByPhotonEnergy = {}
		# get a list of photons (energy/intensity [gamma/sec]) from the source
		spectrum= source.getSpectrum()
		for photon in spectrum
		# get a list of source points
		sourcePoints = source.getSourcePoints()
		# iterate through the photons 
		for photon in spectrum
			# iterate through the source points
			for nextPoint in sourcePoints
				# determine the vector from source to detector
				vector = (nextPoint, self.detector.location)
				# iterate through the shield list
				totalMFP = 0.0
				totalFluxReductionFactor = 0.0
				for shield in shieldList
					mfp, fluxReductionFactor = shield.getCrossingMFP(vector, photon.energy)
					totalMFP = totalMFP + mfp
					totalFluxReductionFactor = totalFluxReductionFactor * fluxReductionFactor
				# calculate buildup factor for this photon and source point
				# calculate uncollided flux from buildup factor and flux reduction factor
				# add to uncollided flux sum for this photon
			# calculate exposure for this photon
		# sum exposure over all photons
		# return exposure (and maybe dose)

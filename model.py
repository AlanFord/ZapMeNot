class model:
	def __init__():
		self.source = []
		self.shieldList = []
		self.detector = None
		self.buildupFactorMaterial = None

	
	def calculateDose():
		pass
		# for each energy in energyGroupList
			# for each point in source point list
				# get point source density
				# for each shield in shield list
					# get mfp
					# gget shielding reduction factor
					# running product of shielding reduction factors
				# sum mfp
				# get uncolidedFluxAtDetector
				# get dose
				# get buildup factor
				# calculate running sum of doseWithBuildupFactor
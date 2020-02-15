import numpy as np
import yaml

class Material:
	library = None

	def __init__(self,name="void"):
		#initialize the class library if it has not already been done
		if Material.library is None:
			stream = open("materials.yml", 'r')
			Material.library = yaml.load(stream, Loader=yaml.FullLoader)

		# check to see if the name is in the library
		if name not in Material.library.keys():
			print("name not found!")

		# initialize the object
		self.name = name
		self.properties = Material.library.get(self.name)
		self.density = self.properties.get("density")
		self.energy_bins = np.array(self.properties.get("energy"))
		self.mass_atten_coff = np.array(self.properties.get("mass-atten-coff"))
		self.gp_coeff = np.array(self.properties.get("gp-coeff"))

	def setDensity(density):
		self.density = density

	def getMfp(energy, distance):
		pass

	def getPhotonRemovalFactor(energy, distance):
		mfp = getMfp(energy, distance)


	def getBuildupFactor(energy, mfp):
		pass



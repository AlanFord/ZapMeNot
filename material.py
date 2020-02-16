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
			raise ValueError("Material not found in the Material Library")

		# initialize the object
		self.name = name
		properties = Material.library.get(self.name)
		self.density = properties.get("density")
		self.energy_bins = np.array(properties.get("energy"))
		self.mass_atten_coff = np.array(properties.get("mass-atten-coff"))
		self.gp_coeff = np.array(properties.get("gp-coeff"))

	def setDensity(self, density):
		self.density = density

	def getMfp(self, energy, distance):
		return distance * self.density / self.getMassAttenCoff(energy)

	def getMassAttenCoff(self, energy):
		if (energy < self.energy_bins[0]) or (energy > self.energy_bins[-1]):
			raise ValueError("Photon energy is out of range")
		return np.interp(energy, self.energy_bins, self.mass_atten_coff)

	def getBuildupFactor(self, energy, mfp, type="GP"):
		if type == "GP":
			# find the bounding array indices
			if (energy < self.energy_bins[0]) or (energy > self.energy_bins[-1]):
				raise ValueError("Photon energy is out of range")
			upper_index = np.searchsorted(self.energy_bins, energy)
			if upper_index == 0:
				upper_index = 1
			lower_index = upper_index -1
			b = self.gp_coeff[upper_index][0]
			c = self.gp_coeff[upper_index][1]
			a = self.gp_coeff[upper_index][2]
			X = self.gp_coeff[upper_index][3]
			d = self.gp_coeff[upper_index][4]
			highGP = self.GP(a,b,c,d,X,mfp)
			b = self.gp_coeff[lower_index][0]
			c = self.gp_coeff[lower_index][1]
			a = self.gp_coeff[lower_index][2]
			X = self.gp_coeff[lower_index][3]
			d = self.gp_coeff[lower_index][4]
			lowGP = self.GP(a,b,c,d,X,mfp)
			# linear interpolation
			upper_energy = self.energy_bins[upper_index]
			lower_energy = self.energy_bins[lower_index]
			return (energy - lower_energy)/(upper_energy-lower_energy)*(highGP-lowGP) + lowGP
		else:
			raise ValueError("Only GP Buildup Factors are currently supported")

	def GP(self, a, b, c, d, X, mfp):
		K = (c * (mfp**a)) + (d * (np.tanh(mfp/X -2) - np.tanh(-2))) / (1 - np.tanh(-2))
		#print(K)
		if K == 1:
			return 1 + (b-1) * mfp
		else:
			return 1 + (b-1)*((K**mfp) - 1)/(K -1)
	



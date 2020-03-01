import numpy as np
import yaml
import pkg_resources

class Material:
	library = None

	def __init__(self,name="void"):
		#initialize the class library if it has not already been done
		if Material.library is None:
			path = 'materialLibrary.yml'
			filepath = pkg_resources.resource_filename(__name__, path)
			stream = open(filepath, 'r')
			Material.library = yaml.load(stream, Loader=yaml.FullLoader)
			stream.close()

		# check to see if the name is in the library
		if name not in Material.library.keys():
			raise ValueError("Material not found in the Material Library")

		# initialize the object
		self.name = name
		properties = Material.library.get(self.name)
		self.density = properties.get("density")
		self.atten_energy_bins = np.array(properties.get("mass-atten-coff-energy"))
		self.mass_atten_coff = np.array(properties.get("mass-atten-coff"))
		self.enAbs_energy_bins = np.array(properties.get("mass-en-abs-coff-energy"))
		self.mass_enAbs_coff = np.array(properties.get("mass-en-abs-coff"))
		self.gp_energy_bins = np.array(properties.get("gp-coff-energy"))
		gp_array = np.array(properties.get("gp-coeff"))
		self.gp_b = gp_array[:,0]
		self.gp_c = gp_array[:,1]
		self.gp_a = gp_array[:,2]
		self.gp_X = gp_array[:,3]
		self.gp_d = gp_array[:,4]

	def setDensity(self, density):
		self.density = density

	def getMfp(self, energy, distance):
		return distance * self.density * self.getMassAttenCoff(energy)

	def getMassAttenCoff(self, energy):
		if (energy < self.atten_energy_bins[0]) or (energy > self.atten_energy_bins[-1]):
			raise ValueError("Photon energy is out of range")
		return np.interp(energy, self.atten_energy_bins, self.mass_atten_coff)

	def getMassEnergyAbsCoff(self, energy):
		if (energy < self.enAbs_energy_bins[0]) or (energy > self.enAbs_energy_bins[-1]):
			raise ValueError("Photon energy is out of range")
		return np.interp(energy, self.enAbs_energy_bins, self.mass_enAbs_coff)

	def getBuildupFactor(self, energy, mfp, type="GP"):
		if type == "GP":
			# find the bounding array indices
			if (energy < self.gp_energy_bins[0]) or (energy > self.gp_energy_bins[-1]):
				raise ValueError("Photon energy is out of range")
			b = np.interp(energy, self.gp_energy_bins, self.gp_b)
			c = np.interp(energy, self.gp_energy_bins, self.gp_c)
			a = np.interp(energy, self.gp_energy_bins, self.gp_a)
			X = np.interp(energy, self.gp_energy_bins, self.gp_X)
			d = np.interp(energy, self.gp_energy_bins, self.gp_d)
			return self.GP(a,b,c,d,X,mfp)
		else:
			raise ValueError("Only GP Buildup Factors are currently supported")

	def GP(self, a, b, c, d, X, mfp):
		K = (c * (mfp**a)) + (d * (np.tanh(mfp/X -2) - np.tanh(-2))) / (1 - np.tanh(-2))
		if K == 1:
			return 1 + (b-1) * mfp
		else:
			return 1 + (b-1)*((K**mfp) - 1)/(K -1)
	



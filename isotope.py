class Isotope:
	library = None

	def __init__(self,name):
		#initialize the class library if it has not already been done
		if Isotope.library is None:
			stream = open("isotopes.yml", 'r')
			Isotope.library = yaml.load(stream, Loader=yaml.FullLoader)
			stream.close()

		# check to see if the name is in the library
		if name not in Material.library.keys():
			raise ValueError("Isotope not found in the Isotope Library")

		# initialize the object
		self.name = name
		properties = Isotope.Library.get(self.name)
		# convert the half-life to units of seconds
		half_life = properties.get("half-life")
		half_life_units = properties.get("half-life-units")
		self.half_life = convert_half_life(half_life,half_life_units)

		# photon energies and intensities are stored as a list of tuples
		self.photons = properties.get("photon-intensity")

	def convert_half_life(value,units):
		if units == "minute":
			return value*60
		if units == "hour":
			return value*60*60
		if units == "day":
			return value*60*60*24
		if units == "year":
			return value*60*60*24*365.25
		# if all else fails, raise an error
		raise ValueError("Half-life units are not recognized")


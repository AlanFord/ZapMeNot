# program to read and parse decay.data
import yaml

def float_representer(dumper, value):
    text = '{0:.5e}'.format(value)
    return dumper.represent_scalar(u'tag:yaml.org,2002:float', text)
yaml.add_representer(float, float_representer)

# open and read the decay data
stream = open("decay.data", 'r')
isotopeLibrary = {}
while True:
	data = stream.readline() #read the title card and throw it away
	if not data:
		break
	while True:
		currentIsotope = {}
		# read data until we run out
		data = stream.readline()
		tokens = data.split()
		if tokens[0] == "-1":
			break
		stream.readline()
		stream.readline()
		nuclide = tokens[1]
		halflifeUnits = int(tokens[2])
		halflife = float(tokens[3])
		if halflifeUnits == 1:
			halflifeUnits = "second"
		elif halflifeUnits == 2:
			halflifeUnits = "minute"
		elif halflifeUnits == 3:
			halflifeUnits = "hour"
		elif halflifeUnits == 4:
			halflifeUnits = "day"
		elif halflifeUnits == 5:
			halflifeUnits = "year"
		elif halflifeUnits == 6:
			halflifeUnits = "stable"
		elif halflifeUnits == 7:
			halflifeUnits = "year"
			halflife = halflife * 1E3
		elif halflifeUnits == 8:
			halflifeUnits = "year"
			halflife = halflife * 1E6
		elif halflifeUnits == 9:
			halflifeUnits = "year"
			halflife = halflife * 1E9
		else:
			raise ValueError("Unknown halflife units")
		# build the dictionary entry for the current isotope
		currentIsotope.update({"half-life" : halflife})
		currentIsotope.update({"half-life-units" : halflifeUnits})
		# add the current isotope to the library dictionary
		isotopeLibrary.update({nuclide : currentIsotope})
stream.close()

# -------------------------------------------------------------
# open and read the photon data
stream = open("gamma.data", 'r')
finalLibrary = {}
while True:
	# read data until we run out
	data = stream.readline()
	if not data:
		break
	tokens = data.split()
	nuclide = tokens[0]
	nuclide_int = int(nuclide)
	# create an isotope name in the form of "Np-237m"
	abbreviation = tokens[6].capitalize()
	Z = nuclide_int//10000  # atomic number
	A = (nuclide_int-(Z*10000))//10  # atomic mass number
	I = int(nuclide_int) - (Z*10000 + A*10) # metastable state
	if I > 0:
		metastable_state = chr(108+I)
	else:
		metastable_state = ""
	name = abbreviation + "-" + str(A) + metastable_state
	# now we read enough lines to capture all of the photons, 6 per line
	photon_count = tokens[1]
	photon_count = int(photon_count.rstrip(photon_count[-1]))
	number_read = 0
	print(name + ": " + str(photon_count) + " photons")
	photonIntensities = []
	while True:
		data = stream.readline()
		tokens = data.split()
		photons_per_line = len(tokens)//2  # two tokens for each 
		for x in range(photons_per_line):
			photon_energy = tokens[0]
			photon_intensity = tokens[1]
			# check for valid photon energy
			if float(photon_energy) >15:  # flag photons > 15 MeV
				print("Skipping nuclide "+nuclide + ": photon energy = "+ photon_energy +", intensity = " + photon_intensity)
				#raise ValueError("Photon energy above 15 MeV")
			if float(photon_energy) > 15.01e-3: # limit photons to > 15.01 keV
				photonIntensities.append([float(photon_energy),float(photon_intensity)])
			else:
				print("dropping photon with energy = " + photon_energy + " MeV")
			del(tokens[0])
			del(tokens[0])
		number_read = number_read + photons_per_line
		if (number_read == photon_count):
			break
	if len(photonIntensities) == 0:
		print("Zero photons remaining for this isotope")
		
	# build the dictionary entry for the current isotope
	currentIsotope = isotopeLibrary[nuclide]
	# discard anything that is "observationaly stable" with some photon emission
	if currentIsotope["half-life-units"] != "stable":
		currentIsotope.update({"photon-energy-units" : "MeV"})
		currentIsotope.update({"photon-intensity" : photonIntensities})
		# add the current isotope to the library dictionary
		finalLibrary.update({name : currentIsotope})
		
yamlStream = open('spankynewIsotopeLibrary.yml', 'wt')
yaml.dump(finalLibrary, yamlStream, default_flow_style=False, explicit_start=True, explicit_end=True)
stream.close()
yamlStream.close()
	
		

	

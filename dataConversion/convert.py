import yaml

def float_representer(dumper, value):
    text = '{0:.5e}'.format(value)
    return dumper.represent_scalar(u'tag:yaml.org,2002:float', text)
yaml.add_representer(float, float_representer)

def convert():
	stream = open("ICRP38.RAD", 'r')
	isotopeLibrary = {}
	while True:
		currentIsotope = {}
		photonIntensities = []
		data = stream.readline()
		if not data:
			break
		tokens = data.split()
		name = tokens[0]
		emissionCount = int(tokens[-1])

		part1 = data[0:15]
		tokens = part1.split()
		halflife = float(tokens[1])

		part2 = data[15:-1]
		tokens = part2.split()
		halflifeUnits = tokens[0]

		print(name)
		print(halflifeUnits)

		if halflifeUnits == 'm':
			halflifeUnits = "minute"
		elif halflifeUnits == 'h':
			halflifeUnits = "hour"
		elif halflifeUnits == 's':
			halflifeUnits = "second"
		elif halflifeUnits == 'y':
			halflifeUnits = "year"
		elif halflifeUnits == 'd':
			halflifeUnits = "day"
		elif halflifeUnits == 'us':
			halflifeUnits = "usecond"
		elif halflifeUnits == 'ms':
			halflifeUnits = "msecond"
		else:
			raise ValueError("Unknown units")


		for i in range (0, emissionCount):
			data = stream.readline()
			tokens = data.split()
			if int(tokens[0]) <=3:
				if float(tokens[2]) >= 20.0e-3: # limit photons to >= 20 keV
					photonIntensities.append([float(tokens[2]),float(tokens[1])/100.])
		# build the dictionary entry for the current isotope
		currentIsotope.update({"half-life" : halflife})
		currentIsotope.update({"half-life-units" : halflifeUnits})
		currentIsotope.update({"photon-energy-units" : "MeV"})
		currentIsotope.update({"photon-intensity" : photonIntensities})
		# add the current isotope to the library dictionary
		isotopeLibrary.update({name : currentIsotope})
	yamlStream = open('newIsotopeLibrary.yml', 'wt')
	yaml.dump(isotopeLibrary, yamlStream, default_flow_style=False, explicit_start=True, explicit_end=True)
	stream.close()
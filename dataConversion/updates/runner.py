# program to read and parse decay.data
import yaml

# first we build a dictionary of element by abreviation and number
stream = open("names", 'r')
# read and throw away 6 lines
for x in range(6):
	data = stream.readline()
elementLibrary = {}
while True:
	data = stream.readline()
	if not data:
		break
	mass = data[0:2]
	abbreviation = data[3:4]
	elementLibrary.update({mass : abbreviation})
	# read and throw away 4 lines
	for x in range(4):
		data = stream.readline()

# open and read the decay data
stream = open("decay.data", 'r')
stream.readline() #read the title card and throw it away
isotopeLibrary = {}
while True:
	currentIsotope = {}
	# read data until we run out
	data = stream.readline()
	if not data:
		break
	tokens = data.split()
	nuclide = int(tokens[1])
	Z = nuclide//10000  # atomic number
	A = (nuclide-(Z*10000))//10  # atomic mass number
	I = int(nuclide - (Z*10000 + A*10) # metastable state
	abbreviation = elementLibrary.get(Z, default = None)
	if abbreviation = 'None'
		raise ValueError("Unknown element")
	name = capitalize(abbreviation)+"-"+A+char(108+I)
	halflife_units = tokens[2]
	halflife = tokens[3]
	if halflifeUnits == 1:
		halflifeUnits = "second"
	elif halflifeUnits == 2:
		halflifeUnits = "minute"
	elif halflifeUnits == 3
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

# -------------------------------------------------------------
# open and read the photon data
stream = open("gamma.data", 'r')
while True:
	# read data until we run out
	data = stream.readline()
	if not data:
		break
	tokens = data.split()
	nuclide = int(tokens[0])
	# create an isotope name in the form of "Np-237m"
	abbreviation = capitalize(tokens[6])
	Z = nuclide//10000  # atomic number
	A = (nuclide-(Z*10000))//10  # atomic mass number
	I = int(nuclide - (Z*10000 + A*10) # metastable state
	name = abbreviation + "-" + A + char(108+I)
	# now we read enough lines to capture all of the photons, 6 per line
	photon_count = tokens[1]
	photon_count = int(photon_count.rstrip(photon_count[-1]))
	number_read = 0
	while True:
		data = stream.readline()
		tokens = data.split()
		photons_per_line = len(tokens)//2  # two tokens for each photon
		for x in photons_per_line:
			photon_energy = tokens[0]
			photon_rate = tokens[1]
			##### DO SOMETHING WITH THE DATA
			del(tokens[0:1])
		number_read = number_read + photons_per_line
		if (number_read == photon_count)
			break
			
			
	# write out data for this isotope
		

	

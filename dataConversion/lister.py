from collections import defaultdict

stream = open("ICRP38.RAD", 'r')
isotope_list = []
while True:

	# read an isotope header line
	data = stream.readline()
	if not data:
		break
	tokens = data.split()
	name = tokens[0]
	isotope_list.append(name)

	# get the number of photons for the current isotope
	emission_count = int(tokens[-1])
	# read one line for each photon released (and ignore)
	for i in range (0, emission_count):
		stream.readline()
stream.close()

# sort the complete list of isotopes
# isotope_list.sort()

# create a dictionary of elements
element_names = []
for isotope_name in isotope_list:
	tokens = isotope_name.split('-')
	element_names.append(tokens[0])
# eliminate duplicates
element_names = list(dict.fromkeys(element_names))
element_names.sort()

my_dict = defaultdict(list)
for element_name in element_names:
	my_dict[element_name]

# add a list of masses to each element in the dictionary
for isotope_name in isotope_list:
	tokens = isotope_name.split('-')
	element_name = tokens[0]
	isotope_weight = tokens[1]
	short_list = my_dict[element_name] 
	short_list.append(isotope_weight)
	my_dict[element_name] = short_list

print('Element,Mass Number')
for item in my_dict.items():
	parkey = item[1]
	# parkey.sort()
	weights = ', '.join(parkey)
	line = item[0]+',"'+weights+'"'
	print(line)

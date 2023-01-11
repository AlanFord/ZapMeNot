# program to parse the attenuation coefficients
# data unified from ANS 6.4.3 and QADS
import yaml

def float_representer(dumper, value):
    text = '{0:.5e}'.format(value)
    return dumper.represent_scalar(u'tag:yaml.org,2002:float', text)

def parse_floats(rad_stream, num_count):
    floats = []
	for x in range(0, num_count):
		card = rad_stream.readline().strip


yaml.add_representer(float, float_representer)
finalLibrary = {}
rad_stream = open("attenCoefs", 'r')
# read the title card
rad_stream.readline()
# read the number of energy points
energyPointsNo = float(rad_stream.readline().strip())

while True:
	data = rad_stream.readline() 
	if not data:
		break

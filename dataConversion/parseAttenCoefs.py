# program to parse the attenuation coefficients
# data unified from ANS 6.4.3 and QADS
import yaml

def float_representer(dumper, value):
    text = '{0:.5e}'.format(value)
    return dumper.represent_scalar(u'tag:yaml.org,2002:float', text)

def parse_floats(rad_stream, num_count):
    floats = []
    while True:
        card = rad_stream.readline().strip()
        if not card:
            return None
        floats.extend(card.split())
        if len(floats) >= num_count:
            results = [float(i) for i in floats]
            return results

def read_the_densities(fileName):
    densityLibrary = {}
    # process the densities
    density_stream = open(fileName, 'r')
    # remove the cruft
    density_stream.readline()
    density_stream.readline()
    density_stream.readline()
    density_stream.readline()
    while True:
        # read an element card
        data = density_stream.readline()
        if not data:
            break
        pieces = data.strip().split()
        elementName = pieces[0].lower()
        density = float(pieces[1])
        # add the current element to the density dictionary
        densityLibrary.update({elementName : density})
    density_stream.close()
    return densityLibrary

def read_the_buildupFactors(fileName):
    bfLibrary = {}
    # process the buildup factors
    bf_stream = open(fileName, 'r')
    while True:
        # read a card
        data = bf_stream.readline()
        if not data:
            break
        pieces = data.strip().split()
        # search for the string MEDIUM and AIR in AIR RESPONSE
        if ("MEDIUM," in pieces) and ("AIR" in pieces):
            material = pieces[0].lower()
            print(material)
            bf_stream.readline()
            bf_stream.readline()
            bf_stream.readline()
            energyList = []
            coefficientList = []
            while True:
                # read a card
                data = bf_stream.readline()
                if not data:
                    break
                data = data.strip()
                if len(data) == 0:
                    break
                data = data.split()
                energy = float(data[0])
                energyList.append(energy)
                B = float(data[1])
                C = float(data[2])
                A = float(data[3])
                XK = float(data[4])
                D = float(data[5])
                coefficientList.append([B, C, A, XK, D])
            currentElement = {}
            currentElement.update({"gp-coff-energy" : energyList})
            currentElement.update({"gp-coeff" : coefficientList})
            # add the current material to the library dictionary
            bfLibrary.update({material : currentElement})
    print(bfLibrary)
    bf_stream.close()
    return bfLibrary
    

if __name__ == "__main__":
    yaml.add_representer(float, float_representer)
    finalLibrary = {}
    
    # retrieve the element densities
    densityLibrary = read_the_densities("densities.txt")
    
    #retrieve the buildup factors
    bfLibrary = read_the_buildupFactors("GP.COE")

    # process the attenuation coefficients
    rad_stream = open("ATTEN.COE", 'r')
    # read the title card
    rad_stream.readline()
    # read the number of energy points
    energyPointsNo = float(rad_stream.readline().strip())

    # read the energy points
    energies = parse_floats(rad_stream, energyPointsNo)

    # now chomp down through the attenuation coefficients
    while True:
        # read the element card
        data = rad_stream.readline()
        if not data:
            break
        elementName = data.strip().split()
        elementName = elementName[-1].lower()
        # get the numbers
        xsecs = parse_floats(rad_stream, energyPointsNo)
        # build the dictionary entry for the current element
        currentElement = {}
        currentElement.update({"density" : densityLibrary[elementName]})
        currentElement.update({"density-units" : "g/cm3"})
        currentElement.update({"energy-units" : "MeV"})
        currentElement.update({"mass-atten-coff-energy" : energies})
        currentElement.update({"mass-atten-coff-units" : "cm2/g"})
        currentElement.update({"mass-atten-coff" : xsecs})
        if elementName in bfLibrary.keys():
            currentElement.update({"gp-coff-energy" : bfLibrary[elementName]["gp-coff-energy"]})
            currentElement.update({"gp-coeff" : bfLibrary[elementName]["gp-coeff"]})
        else:
            currentElement.update({"gp-coff-energy" : None})
            currentElement.update({"gp-coeff" : None})
        # add the current element to the library dictionary
        finalLibrary.update({elementName : currentElement})
        
    # write out the yaml library		
    yamlStream = open('moreMats.yml', 'wt')
    yaml.dump(finalLibrary, yamlStream, default_flow_style=False, explicit_start=True, explicit_end=True)
    print("All Done!")
    rad_stream.close()
    yamlStream.close()

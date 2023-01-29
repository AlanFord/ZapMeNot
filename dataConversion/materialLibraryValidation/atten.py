"""
atten.py: script to evaluate the mass attenuation
coefficient files attenuat and materialLibrary.yml,
comparing both the energy mesh and mass attenuation
coefficients for consistency.

Requires the 'attenuat' file from the SCALE software
package available from https://rsicc.ornl.gov/Default.aspx
"""
import yaml

try:
    from yaml import CLoader as MyLoader
except ImportError:
    from yaml import FullLoader as MyLoader


def main():
    # load the materialLibrary
    materialDictionary = readMaterialLibrary()
    # load the attenuat library
    attenuatDictionary = readAttenuatFile()
    keysUnderTest = materialDictionary.keys()
    anyFailure = False
    lastKey = None
    # loop through the keys in the attenuatDictionary
    for key in attenuatDictionary.keys():
        lastKey = key
        # check if key exists in the material dictionary
        if key not in keysUnderTest:
            print(key, " is missing")
            continue
        first = compareSimpleLists(attenuatDictionary[key]["mass-atten-coff-energy"],
                             materialDictionary[key]["mass-atten-coff-energy"])
        second = compareSimpleLists(attenuatDictionary[key]["mass-atten-coff"],
                              materialDictionary[key]["mass-atten-coff"])
        if not (first and second):
            print(key, " does not match")
            anyFailure = True
    print("Last element evaluated was ", lastKey)
    if anyFailure:
        print("Discrepancies were identified")
    else:
        print("Data are identical")


def compareSimpleLists(reference, underTest):
    """
    Compares list of numbers to determine
    if the lists are identical (within a
    relative difference of one part in 1E6)
    """
    if len(reference) != len(underTest):
        print("Lengths don't match")
    for i in range(len(reference)):
        first = float(reference[i])
        second = float(underTest[i])
        if first == second:
            continue
        if first != 0.0:
            denominator = first
        else:
            denominator = second
        diff = abs((first - second) / denominator)
        if diff >= 1e-6:
            return False
    return True


def readMaterialLibrary():
    path = 'materialLibrary.yml'
    stream = open(path, 'r')
    dictionary = yaml.load(stream, Loader=MyLoader)
    stream.close()
    return dictionary


def readAttenuatFile():
    path = 'attenuat'
    stream = open(path, 'r')
    # read the title card
    stream.readline()
    # read the number of points on the energy grid
    stream.readline()
    energies = ""
    for i in range(4):
        energies = energies + stream.readline()
    energies = energies.strip().split()
    dictionary = {}
    while True:
        try:
            elementName = stream.readline().strip().split()
            if len(elementName) == 0:
                # we have run out of data
                return dictionary
            elementName = elementName[-1]
            # read the xsecs
            xsecs = ""
            for i in range(4):
                xsecs = xsecs + stream.readline()
            xsecs = xsecs.strip().split()
            element = {}
            element["mass-atten-coff-energy"] = energies
            element["mass-atten-coff"] = xsecs
            dictionary[elementName] = element
        except IOError:
            return dictionary


if __name__ == '__main__':
    main()

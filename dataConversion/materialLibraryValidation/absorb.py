"""
absorb.py: script to extract the mass absorption
coefficient for air from materialLibrary.yml.

Requires the ABSORB.COE file from the ANS653 software
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
    (energyCOE, xsecsCOE) = readAbsorbFile()
    # extract the data for air
    air = materialDictionary["air"]
    # retrieve the absorption data
    energyMesh = air["mass-en-abs-coff-energy"]
    xsecs = air["mass-en-abs-coff"]
    if len(energyMesh) != len(xsecs):
        print("missmatched data")
        return
    if len(energyMesh) != len(energyCOE):
        print("data sets don't match")
        return
    anyFailure = False
    first = compareSimpleLists(energyCOE, energyMesh)
    second = compareSimpleLists(xsecsCOE, xsecs)
    if not (first and second):
        print("Discrepancies were identified")
    else:
        print("Data are identical")


def readMaterialLibrary():
    path = 'materialLibrary.yml'
    stream = open(path, 'r')
    dictionary = yaml.load(stream, Loader=MyLoader)
    stream.close()
    return dictionary


def readAbsorbFile():
    path = 'ABSORB.COE'
    stream = open(path, 'r')
    # read the title cards
    for i in range(143):
        stream.readline()
    # read the data cards
    energy = []
    xsecs = []
    for i in range(27):
        dataValues = stream.readline().strip().split()
        energy.append(dataValues[0])
        xsecs.append(dataValues[1])
    return energy, xsecs


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


if __name__ == '__main__':
    main()

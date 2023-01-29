"""
buildup.py: script to evaluate the buildup factor
coefficients in materialLibrary.yml,
evaluating both the energy mesh and
coefficients for consistency.

Requires the GP.COE and HIGHZ.GP files from the ANS653 software
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
    # retrieve the buildup factors
    bfLibrary = read_the_buildupFactors("GP.COE")
    highZbfLibrary = read_the_buildupFactors("HIGHZ.GP")
    anyFailure = False
    # loop through the keys in the materialDictionary
    for key in materialDictionary.keys():
        lastKey = key
        print("checking: ", key)
        # skip materials that don't have buildup factor data
        if "gp-coeff" not in materialDictionary[key].keys():
            print(key, "is missing a gp_coeff key")
            continue
        if materialDictionary[key]["gp-coeff"] is None:
            print("not available")
            continue
        # check if key exists in the GP dictionaries
        key2 = key
        if key == "sulfur":
            key2 = "sulphur"
        if key2 in highZbfLibrary.keys():
            print("Using High Z")
            energies = highZbfLibrary[key2]["gp-coff-energy"]
            coefficients = highZbfLibrary[key2]["gp-coeff"]
        elif key2 in bfLibrary.keys():
            print("Using Std")
            energies = bfLibrary[key2]["gp-coff-energy"]
            coefficients = bfLibrary[key2]["gp-coeff"]
        else:
            print("material ", key, "not found in the GP and HIGHHZ libraries")
            continue
        lastKey = key
        # compare the energy grids
        first = compareSimpleLists(energies,
                                   materialDictionary[key]["gp-coff-energy"])
        # compare the coefficients
        second = compare2DLists(coefficients,
                                materialDictionary[key]["gp-coeff"])
        if not (first and second):
            print(key, " contains differences")
            anyFailure = True
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
        print("Energy Grid Lengths don't match", len(reference), len(underTest))
        return False
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
            print("1D Error, i=", i)
            return False
    return True


def compare2DLists(reference, underTest):
    """
    Compares "list of lists" of numbers to determine
    if the lists are identical (within a
    relative difference of one part in 1E6)
    """
    if len(reference) != len(underTest):
        print("Coefficient Table Lengths don't match", len(reference), len(underTest))
    # get the table width
    width = len(reference[0])
    result = True
    for i in range(len(reference)):
        for j in range(width):
            first = float(reference[i][j])
            second = float(underTest[i][j])
            if first == second:
                continue
            if first != 0.0:
                denominator = first
            else:
                denominator = second
            diff = abs((first - second) / denominator)
            if diff >= 1e-6:
                # print("2D Error, i=", i)
                print("2D Error, i=", i, "j=", j)
                # print(first, second)
                result = False
    return result


def readMaterialLibrary():
    path = 'materialLibrary.yml'
    stream = open(path, 'r')
    dictionary = yaml.load(stream, Loader=MyLoader)
    stream.close()
    return dictionary


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
        if (("MEDIUM," in pieces) or ("MEDUM," in pieces)) and ("AIR" in pieces):
            material = pieces[0].lower()
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
                data = data.strip().strip("\x1a")
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
            currentElement.update({"gp-coff-energy": energyList})
            currentElement.update({"gp-coeff": coefficientList})
            # add the current material to the library dictionary
            bfLibrary.update({material: currentElement})
    bf_stream.close()
    return bfLibrary


if __name__ == '__main__':
    main()

"""
validateKeys.py: script to verify that all maerials
in materialLibrary.yml contain the required keys
"""
import yaml

try:
    from yaml import CLoader as MyLoader
except ImportError:
    from yaml import FullLoader as MyLoader


def main():
    # load the materialLibrary
    materialDictionary = readMaterialLibrary()
    for material in materialDictionary.keys():
        for tag in ["density", "density-units", "energy-units",
                    "mass-atten-coff-units", "mass-atten-coff-energy",
                    "mass-atten-coff", "gp-coeff", "gp-coff-energy"]:
            try:
                # retrieve required keys from each material
                materialDictionary[material][tag]
            except Exception:
                print("Key ", tag, " is missing from ", material)


def readMaterialLibrary():
    path = 'materialLibrary.yml'
    stream = open(path, 'r')
    dictionary = yaml.load(stream, Loader=MyLoader)
    stream.close()
    return dictionary


if __name__ == '__main__':
    main()

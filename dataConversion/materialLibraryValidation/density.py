"""
density.py: script to extract the material densities
from materialLibrary.yml for verification
"""
import yaml

try:
    from yaml import CLoader as MyLoader
except ImportError:
    from yaml import FullLoader as MyLoader


def main():
    # load the materialLibrary
    dictionary = readMaterialLibrary()
    # loop through the keys in the material library
    for key in dictionary.keys():
        print("material: ", key, "   density: ",
              dictionary[key]["density"])
    print("Successful Termination")


def readMaterialLibrary():
    path = 'materialLibrary.yml'
    stream = open(path, 'r')
    dictionary = yaml.load(stream, Loader=MyLoader)
    stream.close()
    return dictionary


if __name__ == '__main__':
    main()

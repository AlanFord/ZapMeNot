import yaml
import pkg_resources

def convert_half_life(value, units):
    if units == "usecond":
        retval = value/1.0E6
    elif units == "msecond":
        retval = value/1000.
    elif units == "second":
        retval = value
    elif units == "minute":
        retval = value*60
    elif units == "hour":
        retval = value*60*60
    elif units == "day":
        retval = value*60*60*24
    elif units == "year":
        retval = value*60*60*24*365.25
    # if all else fails, raise an error
    else:
        raise ValueError("Half-life units are not recognized")
    return retval

class Isotope:
    library = None

    def __init__(self, name):
        # initialize the class library if it has not already been done
        if Isotope.library is None:
            path = 'isotopeLibrary.yml'
            filepath = pkg_resources.resource_filename(__name__, path)
            stream = open(filepath, 'r')
            Isotope.library = yaml.load(stream, Loader=yaml.FullLoader)
            stream.close()

        # check to see if the name is in the library
        name = name.lower().capitalize()
        if name not in Isotope.library.keys():
            raise ValueError("Isotope not found in the Isotope Library")

        # initialize the object
        self.name = name
        properties = Isotope.library.get(self.name)  # dict() of properties
        # convert the half-life to units of seconds
        half_life = properties.get("half-life")
        half_life_units = properties.get("half-life-units")
        self.half_life = convert_half_life(half_life, half_life_units)

        # photon energies and intensities are stored as a list of tuples
        # 2D list of photon energies and intensities
        self.photons = properties.get("photon-intensity")

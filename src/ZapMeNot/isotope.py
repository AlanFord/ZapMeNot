import yaml
import pkg_resources


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
        self.half_life = self.convert_half_life(half_life, half_life_units)

        # photon energies and intensities are stored as a list of tuples
        # 2D list of photon energies and intensities
        self.photons = properties.get("photon-intensity")

    def convert_half_life(self, value, units):
        if units == "usecond":
            return value/1.0E6
        if units == "msecond":
            return value/1000.
        if units == "second":
            return value
        if units == "minute":
            return value*60
        if units == "hour":
            return value*60*60
        if units == "day":
            return value*60*60*24
        if units == "year":
            return value*60*60*24*365.25
        # if all else fails, raise an error
        raise ValueError("Half-life units are not recognized")

import yaml
import pkg_resources


class Isotope:
    """Encaplsulates isotope data from the IsotopeLibrary.yml file.

    The object is intended to make available the half life and photon
    intensities of the requested isotope.

    Parameters
    ----------
    name : :class:`str`
        The isotope to be extracted from the isotope library.

    Attributes
    ----------
    name
    half_life
    photons
    key_progeny
    """
    _library = None

    def __init__(self, name):
        # initialize the class library if it has not already been done
        if Isotope._library is None:
            path = 'isotopeLibrary.yml'
            filepath = pkg_resources.resource_filename(__name__, path)
            stream = open(filepath, 'r')
            Isotope._library = yaml.load(stream, Loader=yaml.FullLoader)
            stream.close()

        # check to see if the name is in the library
        if not isinstance(name, str):
            raise ValueError("Isotope name is not a string: " + str(name))
        name = name.lower().capitalize()
        if name not in Isotope._library.keys():
            raise ValueError("Isotope not found in the Isotope Library")

        # initialize the object
        self._name = name
        properties = Isotope._library.get(self._name)  # dict() of properties
        # convert the half-life to units of seconds
        half_life = properties.get("half-life")
        half_life_units = properties.get("half-life-units")
        self._half_life = Isotope._convert_half_life(
            half_life, half_life_units)
        self._key_progeny = properties.get("key_progeny")

        # photon energies and intensities are stored as a list of tuples
        # 2D list of photon energies and intensities
        self._photons = properties.get("photon-intensity")

    @property
    def photons(self):
        """:class:`list` of :class:`list` : A list of photon energies and
        intensities."""
        return self._photons

    @property
    def name(self):
        """:class:`str` : The name of the isotope."""
        return self._name

    @property
    def half_life(self):
        """:class:`str` : The half life of the isotope in seconds."""
        return self._half_life

    @property
    def key_progeny(self):
        """:class:`dict` : The list of progeny that can be in secular or
        transient equilibrium."""
        return self._key_progeny

    @staticmethod
    def _convert_half_life(value, units):
        """Converts a half life to units of seconds.

        Input units can be microseconds, milliseconds, seconds,
        minutes, hours, days, or years.

        Parameters
        ----------
        value : float
            The half life to be converted
        units : :class:`str`
            The units of the input half life

        Raises
        ------
        ValueError
            Half-life units are not recognized

        Returns
        -------
        float
            Half life in seconds
        """
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

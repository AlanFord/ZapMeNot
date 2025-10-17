'''
ZapMeNot - a point kernel photon shielding library
Copyright (C) 2019-2025  C. Alan Ford

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import yaml

try:
    from yaml import CLoader as MyLoader, CDumper as MyDumper
except ImportError:
    from yaml import FullLoader as MyLoader, SafeDumper as MyDumper

try:
    from importlib import resources as impresources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as impresources

class Isotope:
    """Encapsulates isotope data from the IsotopeLibrary.yml file.

    The object is intended to make available the half life and photon
    intensities of the requested isotope.

    Parameters
    ----------
    name : :class:`str`
        The isotope to be extracted from the isotope library.
    """

    '''
    Attributes
    ----------
    _name
    _half_life
    _photons
    _key_progeny
    _library
    '''

    _library = None

    def __init__(self, name):
        # initialize the class library if it has not already been done
        if Isotope._library is None:
            path = 'isotopeLibrary.yml'
            try:
                inp_file = (impresources.files(__package__) / path)
                stream = inp_file.open("rt") # or "rt" as text file with universal newlines
            except AttributeError:
                # Python < PY3.9, fall back to method deprecated in PY3.11.
                stream = impresources.open_text(__package__, path)
            Isotope._library = yaml.load(stream, Loader=MyLoader)
            stream.close()

        # check to see if the name is in the library
        if not isinstance(name, str):
            raise ValueError(f"Isotope name is not a string: {name}")
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
        """:class:`list` of :class:`list` : A list of photon energies (in MeV) and
        intensities per decay."""
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

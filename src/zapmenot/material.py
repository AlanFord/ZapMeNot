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

from scipy.interpolate import Akima1DInterpolator
import numpy as np
import numbers
import yaml
from typing import Optional, Union, Dict, Any, ClassVar

try:
    from yaml import CLoader as MyLoader, CDumper as MyDumper
except ImportError:
    from yaml import FullLoader as MyLoader, SafeDumper as MyDumper

try:
    from importlib import resources as impresources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as impresources

class Material:
    r"""Encapsulates the data in the MaterialLibrary.yml file.

    Makes available the mean free path, mass
    energy absorption coefficient, the mass attenuation coefficient,
    and the exposure buildup factor of the requested material.

    Parameters
    ----------
    name : :class: `str`
        The material to be extracted from the material library
    """

    r'''
    Attributes
    ----------
    _library
    _name
    _density : float
        Density of the material in g/cm\ :sup:`3`
    '''

    _library: ClassVar[Optional[Dict[str, Any]]] = None

    def __init__(self, name: str) -> None:
        if not isinstance(name, str):
            raise ValueError(f"Material name is not a string: {name}")

        # initialize the class library if it has not already been done
        if Material._library is None:
            path = 'materialLibrary.yml'
            try:
                inp_file = (impresources.files(__package__) / path)
                stream = inp_file.open("rt") # or "rt" as text file with universal newlines
            except AttributeError:
                # Python < PY3.9, fall back to method deprecated in PY3.11.
                stream = impresources.open_text(__package__, path)
            Material._library = yaml.load(stream, Loader=MyLoader)
            stream.close()

        # check to see if the name is in the library
        name = name.lower()
        if name not in Material._library.keys():
            raise ValueError("Material not found in the Material Library")

        # initialize the object
        self._name: str = name
        properties: Dict[str, Any] = Material._library.get(self._name)
        self._density: float = properties.get("density")
        self._atten_energy_bins: np.ndarray = np.array(
            properties.get("mass-atten-coff-energy"))
        self._mass_atten_coff: np.ndarray = np.array(properties.get("mass-atten-coff"))
        # the mass energy absorption coefficient is optional for a material
        self._en_abs_energy_bins: np.ndarray = np.array(
            properties.get("mass-en-abs-coff-energy"))
        self._mass_en_abs_coff: np.ndarray = np.array(properties.get("mass-en-abs-coff"))
        # the buildup factor data is optional for a material
        self._gp_energy_bins: np.ndarray = np.array(properties.get("gp-coff-energy"))
        gp_data = properties.get("gp-coeff")
        if gp_data is None:
            self._gp_b: Optional[np.ndarray] = None
            self._gp_c: Optional[np.ndarray] = None
            self._gp_a: Optional[np.ndarray] = None
            self._gp_X: Optional[np.ndarray] = None
            self._gp_d: Optional[np.ndarray] = None
            self._bi: Optional[Akima1DInterpolator] = None
            self._ci: Optional[Akima1DInterpolator] = None
            self._ai: Optional[Akima1DInterpolator] = None
            self._Xi: Optional[Akima1DInterpolator] = None
            self._di: Optional[Akima1DInterpolator] = None
        else:
            gp_array = np.array(gp_data)
            self._gp_b = gp_array[:, 0]
            self._gp_c = gp_array[:, 1]
            self._gp_a = gp_array[:, 2]
            self._gp_X = gp_array[:, 3]
            self._gp_d = gp_array[:, 4]
            # here we are building interpolators based on the Akima method.
            # For more information on the use of Akima method on G-P coefficients,
            # see https://www.nrc.gov/docs/ML1905/ML19059A414.pdf
            # "QAD-CGGP2 and G33-GP2: Revised Version of QAD-CGGP and G33-GP"
            logE = np.log(self._gp_energy_bins)
            self._bi = Akima1DInterpolator(logE, self._gp_b)
            self._ci = Akima1DInterpolator(logE, self._gp_c)
            self._ai = Akima1DInterpolator(logE, self._gp_a)
            self._Xi = Akima1DInterpolator(logE, self._gp_X)
            self._di = Akima1DInterpolator(logE, self._gp_d)

    @property
    def name(self) -> str:
        """:class:`str` : The name of the material"""
        return self._name

    @property
    def density(self) -> float:
        r""":class:`float` : The density of the material in g/cm\ :sup:`3` """
        return self._density

    @density.setter
    def density(self, value: float) -> None:
        if not isinstance(value, numbers.Number):
            raise ValueError("Invalid density")
        if value < 0:
            raise ValueError("Invalid density")
        self._density = value

    def get_mfp(self, energy: float, distance: float) -> float:
        """Calculates the mean free path for a given distance and photon energy

        Parameters
        ----------
        energy : :class:`float`
            The photon energy in MeV
        distance : :class:`float`
            The distance through the material in cm

        Returns
        -------
        :class:`float`
            The mean free path in the material
        """
        if not isinstance(energy, numbers.Number):
            raise ValueError(f"Invalid energy: {energy}")
        if not isinstance(distance, numbers.Number) or \
           distance < 0:
            raise ValueError(f"Invalid distance: {distance}")
        if distance == 0:
            return 0
        else:
            return distance * self._density * self.get_mass_atten_coeff(energy)

    def get_mass_atten_coeff(self, energy: float) -> float:
        r"""Calculates the mass attenuation coefficient at the given energy

        Parameters
        ----------
        energy : :class:`float`
            The photon energy in MeV

        Raises
        ------
        ValueError
            Photon energy is out of range

        Returns
        -------
        :class:`float`
            The mass attenuation coefficient in cm\ :sup:`2`/g
        """
        if not isinstance(energy, numbers.Number):
            raise ValueError(f"Invalid energy: {energy}")

        if (energy < self._atten_energy_bins[0]) or \
                (energy > self._atten_energy_bins[-1]):
            raise ValueError("Photon energy is out of range")

        return np.power(10.0, np.interp(np.log10(energy),
                                        np.log10(self._atten_energy_bins),
                                        np.log10(self._mass_atten_coff)))

    def get_mass_energy_abs_coeff(self, energy: float) -> float:
        r"""Calculates the mass energy absorption coefficient at the given energy

        Parameters
        ----------
        energy : :class:`float`
            The photon energy in MeV

        Raises
        ------
        ValueError
            Photon energy is out of range

        Returns
        -------
        :class:`float`
            The mass energy absorption coefficient in cm\ :sup:`2`/g
        """
        if not isinstance(energy, numbers.Number):
            raise ValueError(f"Invalid energy: {energy}")

        if (energy < self._en_abs_energy_bins[0]) or \
                (energy > self._en_abs_energy_bins[-1]):
            raise ValueError("Photon energy is out of range")

        return np.power(10.0, np.interp(np.log10(energy),
                                        np.log10(self._en_abs_energy_bins),
                                        np.log10(self._mass_en_abs_coff)))

    def get_buildup_factor(self, energy: float, mfps: Union[float, np.ndarray], formula: str = "GP") -> Union[float, np.ndarray]:
        """Calculates the photon buildup factor at the given energy and mfp

        Parameters
        ----------
        energy : :class:`float`
            The photon energy in MeV
        mfps : :class:`float`, :class:`list`, or :class:`numpy.ndarray`
            One or more mean free path values through the material
        formula : :class:`str`
            The format of the buildup factor (only 'GP' is currently supported)

        Raises
        ------
        ValueError
            Photon energy is out of range
        ValueError
            Only GP buildup factors are currently supported

        Returns
        -------
        :class:`float` or :class:`numpy.ndarray`
            A vector of photon exposure buildup factors in air, one for
            each specified mfp
        """
        if self._gp_b is None:
            raise ValueError("Material has no buildup factor data available")
        if not isinstance(formula, str):
            raise ValueError(f"Buildup factor type is not a string: {formula}")
        if formula.upper() != "GP":
            raise ValueError("Only GP Buildup Factors are currently supported")
        if not isinstance(energy, numbers.Number):
            raise ValueError(f"Invalid energy: {energy}")

        try:
            mfp = np.array(mfps, dtype=float)
        except Exception:
            raise ValueError("mfps have invalid array structure")
        # mfps must be non-negative
        if np.amin(mfp) < 0:
            raise ValueError("negative mfp")

        # find the bounding array indices
        if (energy < self._gp_energy_bins[0]) or \
                (energy > self._gp_energy_bins[-1]):
            raise ValueError("Photon energy is out of range")
        logE = np.log(energy)
        b = self._bi(logE)
        c = self._ci(logE)
        a = self._ai(logE)
        X = self._Xi(logE)
        d = self._di(logE)

        bf = Material._GP(a, b, c, d, X, mfp)
        return bf

    @staticmethod
    def _GP(a: float, b: float, c: float, d: float, X: float, mfp: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Calculates the photon buildup factor using Geometric Progression

        Parameters
        ----------
        a : float
            A GP fitting coefficient
        b : float
            A GP fitting coefficient
        c : float
            A GP fitting coefficient
        d : float
            A GP fitting coefficient
        X : float
            A GP fitting coefficient
        mfp : float (for a single mfp) or a numpy array (for several mfp's)
            The mean free path through the material in cm

        Returns
        -------
        float or :class:`numpy.ndarray`
            Vector of photon exposure buildup factors in air

        Important Details
        -----------------
        The number of mean free paths (mfp) used to calculate the buildup
        factor is limited to a value of 40 or less.  This is an inherent
        limitation of the source document, ANS-6.4.3-1991.  In normal use this
        limitation is only expected to be encountered in cases involving low
        energy photons (with a relatively small mean free path) and
        thick shields.  In those instances the uncolided flux should be very
        small.  Even with a larger buildup factor the contribution of these
        photons to exposure should be minimal and other higher energy photons
        should dominate.  The exception would be xrays combined with very thick
        shiekding.  In those cases a higher-order shielding code
        should be used.
        """
        # if called with a single value of mfp, convert it to a numpy array
        if np.shape(mfp) == ():
            mfps = np.asarray([mfp])
        else:
            mfps = mfp
        #ensure all values in the mpfs array are limited to a range of 0 to 80
        mfps[mfps > 80] = 80
        mfps[mfps < 0] = 0
        # initialize the array of K values to 0
        K = np.zeros(mfps.size)  # default values for mfps = 0 -> buildup factor = 1
        # cases that do not need extrapolation in fmp
        K[np.logical_and(mfps > 0, mfps <= 40)] = (c * (mfps[np.logical_and(mfps > 0, mfps <= 40)]**a)) + \
            (d * (np.tanh(mfps[np.logical_and(mfps > 0, mfps <= 40)]/X - 2) - np.tanh(-2))) / \
            (1 - np.tanh(-2))
        # cases that do need extrapolation ( i.e. mfp > 40)
        if np.any(mfps > 40):
            K35 = (c * (35**a)) + (d * (np.tanh(35/X - 2) - np.tanh(-2))) / \
                (1 - np.tanh(-2))
            K40 = (c * (40**a)) + (d * (np.tanh(40/X - 2) - np.tanh(-2))) / \
                (1 - np.tanh(-2))
            if np.abs(K40-K35) < 1E-4:
                K[mfps > 40] = K40
            else:
                Xi = np.zeros(mfps.size)
                Xi[mfps > 40] = (np.float_power(mfps[mfps > 40]/35., 0.1) -1) / \
                                (np.float_power(40./35., 0.1) -1)
                fm = 0.8
                exponent = np.zeros(mfps.size)
                exponent[mfps > 40] = np.float_power(Xi[mfps > 40], fm)
                if np.abs(K35-1) < 1E-4:
                    ratio = 1E4   # a dummy large value
                else:
                    ratio = (K40-1)/(K35-1)
                if ratio >= 0 and ratio <= 1:
                    K[mfps > 40] = 1 + (K35-1) * np.float_power(ratio, Xi[mfps > 40])
                else:
                    K[mfps > 40] = K35 * np.float_power(K40/K35, exponent[mfps > 40])

        answers = np.ones(mfps.size)  # set default values to 1
        answers[K == 1] = 1 + (b-1) * mfps[K == 1]
        answers[K != 1] = 1 + \
            (b-1)*((np.power(K[K != 1], mfps[K != 1])) - 1)/(K[K != 1] - 1)
        # if the mfp argument was a single value, return a single value
        if np.shape(mfp) == ():
            return answers[0]
        else:
            return answers

from scipy.interpolate import Akima1DInterpolator
import numpy as np
import yaml
import pkg_resources

class Material:
    """Encaplsulates the data in the MaterialLibrary.yml file.

    Makes available the mean free path, mass
    energy absorption coefficient, the mass attenuation coefficient,
    and the exposure buildup factor of the requested material.

    Parameters
    ----------
    name : str
        The material to be extracted from the material library
    
    Attributes
    ----------
    name
    density : float
        Density of the material in g/cm\ :sup:`3`
    """
    _library = None

    def __init__(self, name):
        if name is None:
            raise ValueError("Material type not specified")

        # initialize the class library if it has not already been done
        if Material._library is None:
            path = 'materialLibrary.yml'
            filepath = pkg_resources.resource_filename(__name__, path)
            stream = open(filepath, 'r')
            Material._library = yaml.load(stream, Loader=yaml.FullLoader)
            stream.close()

        # check to see if the name is in the library
        name = name.lower()
        if name not in Material._library.keys():
            raise ValueError("Material not found in the Material Library")

        # initialize the object
        self._name = name
        properties = Material._library.get(self._name)
        self.density = properties.get("density")
        self._atten_energy_bins = np.array(
            properties.get("mass-atten-coff-energy"))
        self._mass_atten_coff = np.array(properties.get("mass-atten-coff"))
        self._en_abs_energy_bins = np.array(
            properties.get("mass-en-abs-coff-energy"))
        self._mass_en_abs_coff = np.array(properties.get("mass-en-abs-coff"))
        self._gp_energy_bins = np.array(properties.get("gp-coff-energy"))
        gp_array = np.array(properties.get("gp-coeff"))
        self._gp_b = gp_array[:, 0]
        self._gp_c = gp_array[:, 1]
        self._gp_a = gp_array[:, 2]
        self._gp_X = gp_array[:, 3]
        self._gp_d = gp_array[:, 4]
        # here we are building interpolators based on the Akima method.
        # For more information on the use of Akima method on G-P coefficients,
        # see https://www.nrc.gov/docs/ML1905/ML19059A414.pdf
        # "QAD-CGGP2 and G33-GP2: Revised Version of QAD-CGGP and G33-GP"
        self._bi = Akima1DInterpolator(self._gp_energy_bins, self._gp_b)
        self._ci = Akima1DInterpolator(self._gp_energy_bins, self._gp_c)
        self._ai = Akima1DInterpolator(self._gp_energy_bins, self._gp_a)
        self._Xi = Akima1DInterpolator(self._gp_energy_bins, self._gp_X)
        self._di = Akima1DInterpolator(self._gp_energy_bins, self._gp_d)
    
    @property
    def name(self):
        """str : The name of the material"""
        return self._name

    def get_mfp(self, energy, distance):
        """Calculates the mean free path for a given distance and photon energy

        Parameters
        ----------
        energy : float
            The photon energy in MeV
        distance : float
            The distance through the material in cm

        Returns
        -------
        float
            The mean free path in the material
        """
        return distance * self.density * self.get_mass_atten_coeff(energy)

    def get_mass_atten_coeff(self, energy):
        """Calculates the mass attenuation coefficient at the given energy

        Parameters
        ----------
        energy : float
            The photon energy in MeV

        Raises
        ------
        ValueError
            Photon energy is out of range

        Returns
        -------
        float
            The mass attenuation coefficient in cm\ :sup:`2`/g
        """
        if (energy < self._atten_energy_bins[0]) or \
                (energy > self._atten_energy_bins[-1]):
            raise ValueError("Photon energy is out of range")
        return np.power(10.0, np.interp(np.log10(energy),
                                        np.log10(self._atten_energy_bins),
                                        np.log10(self._mass_atten_coff)))

    def get_mass_energy_abs_coeff(self, energy):
        """Calculates the mass energy absorption coefficient at the given energy

        Parameters
        ----------
        energy : float
            The photon energy in MeV

        Raises
        ------
        ValueError
            Photon energy is out of range

        Returns
        -------
        float
            The mass energy absorption coefficient in cm\ :sup:`2`/g
        """
        if (energy < self._en_abs_energy_bins[0]) or \
                (energy > self._en_abs_energy_bins[-1]):
            raise ValueError("Photon energy is out of range")
        return np.power(10.0, np.interp(np.log10(energy),
                                        np.log10(self._en_abs_energy_bins),
                                        np.log10(self._mass_en_abs_coff)))

    def get_buildup_factor(self, energy, mfp, formula="GP"):
        """Calculates the photon buildup factor at the given energy and mfp

        Parameters
        ----------
        energy : float
            The photon energy in MeV
        mfp : float
            The mean free path through the material in cm
            formula (str): The format of the buildup factor

        Raises
        ------
        ValueError
            Photon energy is out of range
        ValueError
            Only GP buildup factors are currently supported

        Returns
        -------
        float
            The photon buildup factor for exposure in air
        """
        if mfp == 0:
            return 1
        if formula == "GP":
            # find the bounding array indices
            if (energy < self._gp_energy_bins[0]) or \
                    (energy > self._gp_energy_bins[-1]):
                raise ValueError("Photon energy is out of range")

            b = self._bi(energy)
            c = self._ci(energy)
            a = self._ai(energy)
            X = self._Xi(energy)
            d = self._di(energy)

            return Material._GP(a, b, c, d, X, mfp)
        raise ValueError("Only GP Buildup Factors are currently supported")

    @staticmethod
    def _GP(a, b, c, d, X, mfp):
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
        mfp : float
            The mean free path through the material in cm

        Returns
        -------
        float
            The photon buildup factor for exposure in air
        """
        K = (c * (mfp**a)) + (d * (np.tanh(mfp/X - 2) - np.tanh(-2))) / \
            (1 - np.tanh(-2))
        if K == 1:
            return 1 + (b-1) * mfp
        return 1 + (b-1)*((K**mfp) - 1)/(K - 1)

import abc
import math
import numpy as np
from enum import Enum

from . import shield, isotope

import importlib
pyvista_spec = importlib.util.find_spec("pyvista")
pyvista_found = pyvista_spec is not None
if pyvista_found:
    import pyvista

# -----------------------------------------------------------


class GroupOption(Enum):
    """Set of possible energy group options.  The options
    include 'group', 'discrete', and 'hybrid'.
    """
    GROUP = "group"
    HYBRID = "hybrid"
    DISCRETE = "discrete"

# -----------------------------------------------------------


class Source(abc.ABC):
    """Abtract class to model a radiation source.

    Maintains a list of isotopes and can return a list of point source
    locations within the body of the Source.

    Parameters
    ----------
    **kwargs
        Arbitrary keyword arguments.
    """
    '''
    Attributes
    ----------
    _points_per_dimension : :class:`list` of integers
        The number of source points to be used in each dimension when modeling
        the uniform source distribution throughout the body of the source.
        Typically a list of three integers for three-dimensional sources, one
        integer for one dimensional sources, and not significant for point
        sources.
    '''
    def __init__(self, **kwargs):
        '''Initialize the Source with empty strings for the isotope list
        and photon list'''
        self._isotope_list = []   # LIST of isotopes and activities (Bq)
        self._unique_photons = []  # LIST of unique photons and activities (Bq)
        self._points_per_dimension = [10, 10, 10]
        self._include_key_progeny = False
        self._max_photon_energies = 30
        self._grouping_option = GroupOption.HYBRID
        super().__init__(**kwargs)

    @property
    def grouping(self):
        """:class:`GroupOption` : State defining the photon energy group
        option."""
        return self._grouping_option

    @grouping.setter
    def grouping(self, value):
        """:class:`GroupOption` : State defining the photon energy group
        option."""
        if value == GroupOption.HYBRID.value:
            self._grouping_option = GroupOption.HYBRID
        elif value == GroupOption.GROUP.value:
            self._grouping_option = GroupOption.GROUP
        elif value == GroupOption.DISCRETE.value:
            self._grouping_option = GroupOption.DISCRETE
        else:
            raise ValueError("Invalid grouping option " + str(value))

    @property
    def include_key_progeny(self):
        """bool : State defining if key progeny should be included."""
        return self._include_key_progeny

    @include_key_progeny.setter
    def include_key_progeny(self, value):
        """bool : State defining if key progeny should be included."""
        self._include_key_progeny = value

    def add_isotope_curies(self, new_isotope, curies):
        """Adds an isotope and activity in curies to the isotope list

        Parameters
        ----------
        new_isotope : :class:`zapmenot.isotope.Isotope`
            The isotope to be added to the source.
        curies : float
            The activity in curies.
        """
        self._isotope_list.append((new_isotope, curies*3.7E10))

    def add_isotope_bq(self, new_isotope, becquerels):
        """Adds an isotope and activity in becquerels to the isotope list

        Parameters
        ----------
        new_isotope : :class:`zapmenot.isotope.Isotope`
            The isotope to be added to the source.
        becquerels : float
            The activity in becquerels.
        """
        self._isotope_list.append((new_isotope, becquerels))

    def add_photon(self, energy, intensity):
        """Adds a photon and intensity to the photon list

        Parameters
        ----------
        energy : float
            The photon energy in MeV.
        intensity : float
            The intensity in photons/sec.
        """
        self._unique_photons.append((energy, intensity))

    def list_isotopes(self):
        """Returns a list of isotopes in the source

        Returns
        -------
        :class:`list` of :class:`tuple`
            List of isotope tuples, each tuple containing a
            Isotope object and an activity in Bq.
        """
        return self._isotope_list

    def list_discrete_photons(self):
        """Returns a list of individual photons in the source.

        The list includes only those photons that have been added
        individually to the source.  It does not include the photons
        that result from the isotopes added to the source.

        Returns
        -------
        :class:`list` of :class:`tuple`
            List of photon tuples, each tuple containing a
            photon energy in MeV and an activity in Bq.
        """
        return self._unique_photons

    # def _get_distributed_source_list(self):
    #     """Returns a list of photons in the source

    #     This list of photons combines the Isotopes and the
    #     unique_photons specified in the Source definition.
    #     The photon intensities are scaled to **one source point**.

    #     Returns
    #     -------
    #     :class:`list` of :class:`tuple`
    #         List of photon tuples, each tuple containing a
    #         photon energy in MeV and an activity in **Bq//source point**.
    #     """
    #     list = self.get_photon_source_list()
    #     scaling_factor = np.prod(self._points_per_dimension)

    def get_photon_source_list(self):
        """Returns a list of photons in the source

        This list of photons combines the Isotopes and the
        unique_photons specified in the Source definition.
        The photon intensities are scaled to
        **an integral over the source volume**.

        Returns
        -------
        :class:`list` of :class:`tuple`
            List of photon tuples, each tuple containing a
            photon energy in MeV and an activity in **Bq**.
        """
        photon_dict = dict()
        keys = photon_dict.keys()

        temporary_isotope_list = self._isotope_list[:]
        # add key progeny if required
        if self._include_key_progeny is True:
            for next_isotope in self._isotope_list:
                isotope_detail = isotope.Isotope(next_isotope[0])
                if isotope_detail.key_progeny is not None:
                    for key, value in isotope_detail.key_progeny.items():
                        temporary_isotope_list.append(
                           (key, next_isotope[1]*value))

        # search isotope list for photons to be added to the photon list
        # next_isotope will be a tuple of name and Bq
        for next_isotope in temporary_isotope_list:
            isotope_detail = isotope.Isotope(next_isotope[0])
            if isotope_detail.photons is not None:
                for photon in isotope_detail.photons:
                    # test to see if photon energy is already on the list
                    # and then add photon emission rate (intensity*Bq).
                    if photon[0] in keys:
                        photon_dict[photon[0]] = photon_dict[photon[0]] + \
                            photon[1]*next_isotope[1]
                    else:
                        photon_dict[photon[0]] = photon[1]*next_isotope[1]
        for photon in self._unique_photons:
            # test to see if photon energy is already on the list
            # and then add photon emission rate.
            if photon[0] in keys:
                photon_dict[photon[0]] = photon_dict[photon[0]] + photon[1]
            else:
                photon_dict[photon[0]] = photon[1]
        photon_list = []
        # scaling_factor = np.prod(self._points_per_dimension)
        for key, value in photon_dict.items():
            photon_list.append((key, value))
        photon_list = sorted(photon_list)
        if self._grouping_option == GroupOption.GROUP or \
                ((self._grouping_option == GroupOption.HYBRID) and
                    (len(photon_list) > self._max_photon_energies)):
            # group the photons
            minEnergy = photon_list[0][0]
            maxEnergy = photon_list[-1][0]
            (groupEnergies, stepSize) = np.linspace(
                minEnergy, maxEnergy, self._max_photon_energies, retstep=True)
            binBoundaries = groupEnergies + (stepSize/2)
            binBoundaries = \
                np.concatenate([np.array([binBoundaries[0]-stepSize]),
                                binBoundaries])
            # Returns the appropriate bin for each photon
            binplace = np.digitize(photon_list, binBoundaries)[:, 0]
            # convert the photon list to an array for further processing
            photonArray = np.array(photon_list)
            returnValue = np.zeros((self._max_photon_energies, 2))
            for i in range(1, self._max_photon_energies+1):
                # determine which photons are in each bin
                subset = photonArray[np.where(binplace == i)]
                csum = np.sum(subset[:, 1])  # total emission rate
                if (csum != 0):
                    returnValue[i-1, 0] = \
                        np.sum(subset[:, 0]*subset[:, 1])/csum
                    returnValue[i-1, 1] = csum
            # keep only groups with non-zero intensity
            returnValue = returnValue[np.all(returnValue, axis=1)]
            photon_list = returnValue.tolist()
        return photon_list

    @abc.abstractmethod
    def _get_source_points(self):
        """Generates a list of point sources within the Source geometry.
        """
        pass

    @abc.abstractmethod
    def _get_source_point_weights(self):
        '''
        Returns a list of quadrature weights for the quadrature locations
        within the source volume.  Note that the weights should sum to 1.0,
        each weight representing the fraction of the source associated with
        a particular quadrature point.  When a uniform weighting is required,
        the weights should have constant values that sum to 1.0.
        '''
        pass

    @property
    def points_per_dimension(self):
        """list of integers : Number of source points per dimension."""
        return self._points_per_dimension

    @points_per_dimension.setter
    def points_per_dimension(self, value):
        """list of integers : Number of source points per dimension."""
        try:
            iter(value)
        except TypeError:
            # not iterable; make it so
            value = [value]
        # verify the list includes only integers
        if not all(isinstance(item, int) for item in value):
            raise ValueError(
                "Number of Source Points per Dimension is/are non-integer")
        if not all(item > 0 for item in value):
            raise ValueError(
                "Source Points per Dimension must be positive integers")
        self._points_per_dimension = value


# -----------------------------------------------------------


class LineSource(Source, shield.Shield):
    """Models a line radiation source

    Parameters
    ----------
    start : :class:`list`
        Cartiesian X, Y, and Z coordinates of the starting point of the
        line source.
    end : :class:`list`
        Cartiesian X, Y, and Z coordinates of the ending point of the
        line source.
    """
    '''
    Attributes
    ----------
    material : :class: `material.Material`
        Material properties of the shield
    origin : :class:`numpy.ndarray`
        Vector location of one end of the line source.
    end : :class:`numpy.ndarray`
        Vector location of one end of the line source.
    '''
    def __init__(self, start, end, **kwargs):
        "Initialize"
        self.origin = np.array(start)
        self.end = np.array(end)
        self._length = np.linalg.norm(self.end - self.origin)
        self._dir = (self.end - self.origin)/self._length
        # let the point source have a dummy material of air at a zero density
        kwargs['material_name'] = 'air'
        kwargs['density'] = 0
        super().__init__(**kwargs)
        # initialize points_per_dimension after super() to force a
        # single dimension
        self._points_per_dimension = [10]

    def is_infinite(self):
        """Returns true if any dimension is infinite, false otherwise
        """
        return False

    def _get_source_point_weights(self):
        '''
        Returns a list of quadrature weights for the quadrature locations
        within the source volume.  Note that the weights should sum to 1.0,
        each weight representing the fraction of the source associated with
        a particular quadrature point.  When a uniform weighting is required,
        the weights should have constant values that sum to 1.0.
        '''
        return [1.0 / np.prod(self._points_per_dimension)] * \
            np.prod(self._points_per_dimension)

    def _get_source_points(self):
        """Generates a list of point sources within the Source geometry.

        Returns
        -------
        :class:`list` of :class:`numpy.adarray`
            A list of vector locations within the Source body
        """
        #
        # Note: the Line source is unique in that it only has one dimension
        # (i.e. not three).  Hence it is possible that the user will set the
        # "points_er_dimension" to be a non-iterable numerical value.
        try:
            iter(self._points_per_dimension)
        except TypeError:
            # not iterable; make it so
            self._points_per_dimension = [self._points_per_dimension]

        spacings = np.linspace(1, self._points_per_dimension[0],
                               self._points_per_dimension[0])
        mesh_width = self._length/self._points_per_dimension[0]
        spacings = spacings*mesh_width
        spacings = spacings-(mesh_width/2)
        source_points = []
        for dist in spacings:
            location = self.origin+self._dir*dist
            source_points.append(location)
        return source_points

    def _get_crossing_length(self, ray):
        """Calculates the linear intersection length of a ray and the shield

        Parameters
        ----------
        ray : :class:`zapmenot.ray.FiniteLengthRay`
            The finite length ray that is checked for intersections with
            the shield.

        Returns
        -------
        int
            Always returns 0
        """
        return 0

    def get_crossing_mfp(self, ray, photon_energy):
        """Calculates the mfp equivalent if a ray intersects the shield

        Parameters
        ----------
        ray : :class:`zapmenot.ray.FiniteLengthRay`
            The finite length ray that is checked for intersections with
            the shield.
        photon_energy : float
            The photon energy in MeV

        Returns
        -------
        int
            Always returns 0
        """
        return 0

    def draw(self):
        """Creates a display object

        Returns
        -------
        :class:`pyvista.PolyData`
            A line object representing the line source.
        """
        if pyvista_found:
            return pyvista.Line(pointa=self.origin, pointb=self.end)

# -----------------------------------------------------------


class PointSource(Source, shield.Shield):
    """Models a point radiation source

    Parameters
    ----------
    x : float
        Cartesian X coordinate of the point source.
    y : float
        Cartesian Y coordinate of the point source.
    z : float
        Cartesian Z coordinate of the point source.
    """
    '''
    Attributes
    ----------
    material : :class: `zapmenot.material.Material`
        Material properties of the shield
    inner_radius : float
        Radius of the annulus inner surface.
    outer_radius : float
        Radius of the annulus outer surface.
    origin : :class:`numpy.ndarray`
        Vector location of a point on the annulus centerline.
    dir : :class:`numpy.ndarray`
        Vector normal of the annulus centerline.
    '''
    def __init__(self, x, y, z, **kwargs):
        '''Initialize with an x,y,z location in space'''
        self._x = x
        self._y = y
        self._z = z
        # let the point source have a dummy material of air at a zero density
        kwargs['material_name'] = 'air'
        kwargs['density'] = 0
        super().__init__(**kwargs)
        self._points_per_dimension = [1]

    def is_infinite(self):
        """Returns true if any dimension is infinite, false otherwise
        """
        return False

    def _get_source_point_weights(self):
        '''
        Returns a list of quadrature weights for the quadrature locations
        within the source volume.  Note that the weights should sum to 1.0,
        each weight representing the fraction of the source associated with
        a particular quadrature point.  When a uniform weighting is required,
        the weights should have constant values that sum to 1.0.
        '''
        return [1.0 / np.prod(self._points_per_dimension)] * \
            np.prod(self._points_per_dimension)

    def _get_source_points(self):
        """Generates a list of point sources within the Source geometry.

        Returns
        -------
        :class:`list` of :class:`numpy.adarray`
            A list of vector locations within the Source body.  In this class
            the list is only a single entry.
        """
        return [(self._x, self._y, self._z)]

    def _get_crossing_length(self, ray):
        """Calculates the linear intersection length of a ray and the shield

        Parameters
        ----------
        ray : :class:`zapmenot.ray.FiniteLengthRay`
            The finite length ray that is checked for intersections with
            the shield.

        Returns
        -------
        int
            Always returns 0
        """
        return 0

    def get_crossing_mfp(self, ray, photon_energy):
        """Calculates the mfp equivalent if a ray intersects the shield

        Parameters
        ----------
        ray : :class:`zapmenot.ray.FiniteLengthRay`
            The finite length ray that is checked for intersections with
            the shield.
            Always returns 0 for the Point source.
        photon_energy : float
            The photon energy in MeV

        Returns
        -------
        int
            Always returns 0
        """
        return 0

    def draw(self):
        """Creates a display object

        Returns
        -------
        :class:`pyvista.PolyData`
            A degenerate line object representing the point source.
        """
        if pyvista_found:
            # this returns a degenerate line, equivalent to a point
            return pyvista.Line((self._x, self._y, self._z),
                                (self._x, self._y, self._z))


# -----------------------------------------------------------


class SphereSource(Source, shield.Sphere):
    '''Models a Spherical source
    Parameters
    ----------
    material_name : :obj:`material.Material`
        Shield material type
    sphere_center : list
        list of floats (x, y, and z coordinates).
    sphere_radius : float
        radius of the shield.
    density : float, optional
        Material density in g/cm3.

    Attributes
    ----------
    material : :class: `material.Material`
        Material properties of the shield
    center : list
        list of floats (x, y, and z coordinates).
    radius : float
        radius of the sphere.
    '''

    def __init__(self, material_name, sphere_center, sphere_radius,
                 density=None, **kwargs):
        kwargs['material_name'] = material_name
        kwargs['sphere_center'] = sphere_center
        kwargs['sphere_radius'] = sphere_radius
        kwargs['density'] = density
        super().__init__(**kwargs)
        self.points_per_dimension = [10, 10, 10]  # triggers quadrature calcs

    @property
    def points_per_dimension(self):
        """list of integers : Number of source points per dimension."""
        return Source.points_per_dimension.fget(self)

    @points_per_dimension.setter
    def points_per_dimension(self, value):
        """list of integers : Number of source points per dimension."""
        # verify there are three values in the list
        if len(value) != 3:
            raise ValueError(
                "Source Points per Dimension needs three entries")
        Source.points_per_dimension.fset(self, value)
        # update the quadrature and weights
        nR = self._points_per_dimension[0]
        nTheta = self._points_per_dimension[1]
        nPhi = self._points_per_dimension[2]
        r, t, p, w = _spherequad(nR, nTheta, nPhi, self.radius)
        # the weights generated by _spherequad represent the volume
        # associated with each quadrature point.  The weights needed
        #  by ZapMeNot are the FRACTION of
        # the sphere's volume represented by each quadrature point.
        totalVolume = 4/3*math.pi*self.radius**3
        self.weights = w / totalVolume
        self.rLocations = r
        self.thetaLocations = t
        self.phiLocations = p

    def _get_source_point_weights(self):
        '''
        Returns a list of quadrature weights for the quadrature locations
        within the source volume.  Note that the weights should sum to 1.0,
        each weight representing the fraction of the source associated with
        a particular quadrature point.  When a uniform weighting is required,
        the weights should have constant values that sum to 1.0.
        '''
        return self.weights

    def _get_source_points(self):
        """Generates a list of point sources within the Source geometry.

        Returns
        -------
        :class:`list` of :class:`numpy.adarray`
            A list of vector locations within the Source body.
        """
        x = self.rLocations*np.sin(self.thetaLocations) * \
            np.cos(self.phiLocations)
        y = self.rLocations*np.sin(self.thetaLocations) * \
            np.sin(self.phiLocations)
        z = self.rLocations*np.cos(self.thetaLocations)
        bigly = np.array([x, y, z]).transpose() + self.center
        return bigly.tolist()


# -----------------------------------------------------------


class BoxSource(Source, shield.Box):
    """Models a Axis-Aligned rectangular box source

    Parameters
    ----------
    material_name : :class:`zapmenot.material.Material`
        Shield material type
    box_center : :class:`list`
        X, Y, and Z coordinates of the box center.
    box_dimensions : :class:`list`
        X, Y, and Z dimensions of the box.
    density : float, optional
        Material density in g/cm3.
    """
    '''
    Attributes
    ----------
    material : :class: `material.Material`
        Material properties of the shield
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_source_point_weights(self):
        '''
        Returns a list of quadrature weights for the quadrature locations
        within the source volume.  Note that the weights should sum to 1.0,
        each weight representing the fraction of the source associated with
        a particular quadrature point.  When a uniform weighting is required,
        the weights should have constant values that sum to 1.0.
        '''
        return [1.0 / np.prod(self._points_per_dimension)] * \
            np.prod(self._points_per_dimension)

    def _get_source_points(self):
        """Generates a list of point sources within the Source geometry.

        Returns
        -------
        :class:`list` of :class:`numpy.adarray`
            A list of vector locations within the Source body.
        """
        source_points = []
        # verify there are three values in the list
        if len(self._points_per_dimension) != 3:
            raise ValueError(
                "Source Points per Dimension needs three entries")
        mesh_width = self.box_dimensions/self._points_per_dimension
        start_point = self.box_center-(self.box_dimensions)/2+(mesh_width/2)
        for i in range(self._points_per_dimension[0]):
            x = start_point[0]+mesh_width[0]*i
            for j in range(self._points_per_dimension[1]):
                y = start_point[1]+mesh_width[1]*j
                for k in range(self._points_per_dimension[2]):
                    z = start_point[2]+mesh_width[2]*k
                    source_points.append([x, y, z])
        return source_points

# -----------------------------------------------------------


class ZAlignedCylinderSource(Source, shield.ZAlignedCylinder):
    """Models a cylindrical source axis-aligned with the Z axis.

    Parameters
    ----------
    material_name : :obj:`material.Material`
        Shield material type
    cylinder_center : :obj:`list`
        X, Y, and Z coordinates of the center of the cylinder.
    cylinder_length : float
        The length of the cylinder.
    cylinder_radius : float
        Radius of the cylinder.
    density : float, optional
        Material density in g/cm3.

    """
    # initialize with cylinderCenter, cylinderLength, cylinderRadius,
    # material(optional), density(optional)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_source_point_weights(self):
        '''
        Returns a list of quadrature weights for the quadrature locations
        within the source volume.  Note that the weights should sum to 1.0,
        each weight representing the fraction of the source associated with
        a particular quadrature point.  When a uniform weighting is required,
        the weights should have constant values that sum to 1.0.
        '''
        return [1.0 / np.prod(self._points_per_dimension)] * \
            np.prod(self._points_per_dimension)

    def _get_source_points(self):
        """Generates a list of point sources within the Source geometry.

        Returns
        -------
        :class:`list` of :class:`numpy.adarray`
            A list of vector locations within the Source body.
        """
        # verify there are three values in the list
        if len(self._points_per_dimension) != 3:
            raise ValueError(
                "Source Points per Dimension needs three entries")
        source_points = _generic_cylinder_source_points(
            self._points_per_dimension,
            self.length, self.radius)
        # no rotation is needed
        # shift the point set to the specified cylinder center
        source_points += (self.origin + self.end)/2
        return source_points

# -----------------------------------------------------------


class YAlignedCylinderSource(Source, shield.YAlignedCylinder):
    """Models a cylindrical source axis-aligned with the Y axis.

    Parameters
    ----------
    material_name : :obj:`material.Material`
        Shield material type
    cylinder_center : :obj:`list`
        X, Y, and Z coordinates of the center of the cylinder.
    cylinder_length : float
        The length of the cylinder.
    cylinder_radius : float
        Radius of the cylinder.
    density : float, optional
        Material density in g/cm3.

    """
    # initialize with cylinderCenter, cylinderLength, cylinderRadius,
    # material(optional), density(optional)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_source_point_weights(self):
        '''
        Returns a list of quadrature weights for the quadrature locations
        within the source volume.  Note that the weights should sum to 1.0,
        each weight representing the fraction of the source associated with
        a particular quadrature point.  When a uniform weighting is required,
        the weights should have constant values that sum to 1.0.
        '''
        return [1.0 / np.prod(self._points_per_dimension)] * \
            np.prod(self._points_per_dimension)

    def _get_source_points(self):
        """Generates a list of point sources within the Source geometry.

        Returns
        -------
        :class:`list` of :class:`numpy.adarray`
            A list of vector locations within the Source body.
        """
        # verify there are three values in the list
        if len(self._points_per_dimension) != 3:
            raise ValueError(
                "Source Points per Dimension needs three entries")
        some_points = np.array(_generic_cylinder_source_points(
            self._points_per_dimension,
            self.length, self.radius))
        # rotate the point set from the Z-axis to the Y-axis
        # (y replaced by z; z replaced by -y)
        source_points = np.empty_like(some_points)
        source_points[:, 0] = some_points[:, 0]
        source_points[:, 1] = some_points[:, 2]
        source_points[:, 2] = -some_points[:, 1]
        # shift the point set to the specified cylinder center
        source_points += (self.origin + self.end)/2
        return source_points

# -----------------------------------------------------------


class XAlignedCylinderSource(Source, shield.XAlignedCylinder):
    """Models a cylindrical source axis-aligned with the X axis.

    Parameters
    ----------
    material_name : :obj:`material.Material`
        Shield material type
    cylinder_center : :obj:`list`
        X, Y, and Z coordinates of the center of the cylinder.
    cylinder_length : float
        The length of the cylinder.
    cylinder_radius : float
        Radius of the cylinder.
    density : float, optional
        Material density in g/cm3.

    """
    # initialize with cylinderCenter, cylinderLength, cylinderRadius,
    # material(optional), density(optional)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_source_point_weights(self):
        '''
        Returns a list of quadrature weights for the quadrature locations
        within the source volume.  Note that the weights should sum to 1.0,
        each weight representing the fraction of the source associated with
        a particular quadrature point.  When a uniform weighting is required,
        the weights should have constant values that sum to 1.0.
        '''
        return [1.0 / np.prod(self._points_per_dimension)] * \
            np.prod(self._points_per_dimension)

    def _get_source_points(self):
        """Generates a list of point sources within the Source geometry.

        Returns
        -------
        :class:`list` of :class:`numpy.adarray`
            A list of vector locations within the Source body.
        """
        # verify there are three values in the list
        if len(self._points_per_dimension) != 3:
            raise ValueError(
                "Source Points per Dimension needs three entries")
        some_points = np.array(_generic_cylinder_source_points(
            self._points_per_dimension,
            self.length, self.radius))
        # rotate the point set from the Z-axis to the Y-axis
        # (x replaced by z; z replaced by -x)
        source_points = np.empty_like(some_points)
        source_points[:, 0] = some_points[:, 2]
        source_points[:, 1] = some_points[:, 1]
        source_points[:, 2] = -some_points[:, 0]
        # shift the point set to the specified cylinder center
        source_points += (self.origin + self.end)/2
        return source_points


def _generic_cylinder_source_points(points_per_dimension, length, radius):
    """Generates a list of point sources within a Z-aligned
    cylinder centered on the origin.

    Returns
    -------
    :class:`list` of :class:`numpy.adarray`
        A list of vector locations within the Source body.

    Arguments
    ----------
    points_per_dimension : :obj:`list`
        list of number of quadrature points per dimension: r, theta, z
    length : float
        The length of the cylinder.
    radius : float
        The radius of the cylinder.
    """
    # calculate the radius of each "equal area" annular region
    total_area = math.pi*radius**2
    annular_area = total_area/points_per_dimension[0]
    old_radius = 0
    running_area = 0
    annular_locations = []
    for i in range(points_per_dimension[0]):
        new_radius = math.sqrt((running_area+annular_area)/math.pi)
        annular_locations.append((new_radius+old_radius)/2)
        old_radius = new_radius
        running_area = running_area+annular_area

    angle_increment = 2*math.pi/points_per_dimension[1]
    start_angle = angle_increment/2
    angle_locations = []
    for i in range(points_per_dimension[1]):
        angle_locations.append(start_angle + (i*angle_increment))

    length_increment = length/points_per_dimension[2]
    start_location = -(length/2) + length_increment/2
    length_locations = []
    for i in range(points_per_dimension[2]):
        length_locations.append(start_location + (i*length_increment))

    # iterate through each dimension, building a list of source points
    source_points = []
    for radial_location in annular_locations:
        r = radial_location
        for angle_location in angle_locations:
            theta = angle_location
            for length_location in length_locations:
                z = length_location
                # convert cylindrical to rectangular coordinates
                x = r * math.cos(theta)
                y = r * math.sin(theta)
                source_points.append([x, y, z])
    return source_points


def _spherequad(nr, nTheta, nPhi, rad):
    '''
    R,T,P,W =_spherequad(NR,NT,NP,RAD) computes the product grid nodes in
    r, theta, and phi in spherical and the corresponding quadrature weights
    for a sphere of radius RAD>0. NR is the number of radial nodes, NT is
    the number of theta angle nodes in [0,pi], and NP is the number of phi
    angle nodes in [0, 2*pi]. The sphere radius RAD can be set to infinity,
    however, the functions to be integrated must decay exponentially with
    radius to obtain a reasonable numerical approximation.

    Source adapted from:
    https://www.mathworks.com/matlabcentral/fileexchange/10750
    Written by: Greg von Winckel - 04/13/2006
    Contact: gregvw(at)math(dot)unm(dot)edu
    URL: http://www.math.unm.edu/~gregvw
    '''
    r, wr = _rquad(nr, 2)         # radial weights and nodes (mapped Jacobi)

    if rad == float('inf'):        # infinite radius sphere
        wr = wr/(1-r)**4           # singular map of sphere radius
        r = r/(1-r)
    else:                        # finite radius sphere
        wr = wr*rad**3             # Scale sphere radius
        r = r*rad
    x, wt = _rquad(nTheta, 0)

    t = np.arccos((2*x-1))  # theta weights and nodes (mapped Legendre)
    wt = 2*wt

    p = 2*np.pi*np.linspace(0, nPhi-1, nPhi)/nPhi  # phi nodes (Gauss-Fourier)
    wp = 2*np.pi*np.ones(nPhi)/nPhi        # phi weights
    rr, tt, pp = np.meshgrid(r, t, p)   # Compute the product grid

    r = rr.flatten('F')
    t = tt.flatten('F')
    p = pp.flatten('F')

    wt = wt[:, np.newaxis]
    wr = wr[:, np.newaxis]
    wp = wp[:, np.newaxis]

    w = np.reshape(
        np.dot(np.reshape(np.dot(wt, wr.transpose()), (nr*nTheta, 1), 'F'),
               wp.transpose()), (nr*nTheta*nPhi, 1), 'F')
    w = w.reshape(-1)
    return r, t, p, w


def _rquad(N, k):
    '''
    Functional routine used by _spherequad
    '''
    k1 = k+1
    k2 = k+2
    n = np.arange(1, N+1)
    nnk = 2*n+k
    A = np.insert(np.full(N, k**2) / (nnk*(nnk+2)), 0, k/k2)
    n = np.arange(2, N+1)
    nnk = nnk[1:N+1]
    B1 = 4*k1/(k2*k2*(k+3))
    nk = n+k
    nnk2 = nnk*nnk
    B = 4*(n*nk)**2/(nnk2*nnk2-nnk2)
    ab = np.column_stack((A, np.concatenate(([(2**k1)/k1], [B1], B))))
    s = np.sqrt(ab[1:N, 1])
    [X, V] = np.linalg.eig(np.diag(ab[0:N, 0], 0)+np.diag(s, -1)+np.diag(s, 1))
    indexes = np.argsort(X)
    X = np.sort(X)
    V = V[:, indexes]
    x = (X+1)/2
    w = (1/2)**(k1)*ab[0, 1]*V[0]**2
    return x, w

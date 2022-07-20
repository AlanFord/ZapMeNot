import abc
import math
import pyvista

import numpy as np

from . import shield, isotope

from enum import Enum

class GroupOption(Enum):
    GROUP = "group"
    HYBRID = "hybrid"
    DISCRETE = "discrete"

class Source(metaclass=abc.ABCMeta):
    """Abtract class to model a radiation source.  

    Maintains a list of isotopes and can return a list of point source 
    locations within the body of the Source.

    Parameters
    ----------
    **kwargs
        Arbitrary keyword arguments.

    Attributes
    ----------
    points_per_dimension : :class:`list` of integers
        The number of source points to be used in each dimension when modeling
        the uniform source distribution throughout the body of the source.  Typically
        a list of three integers for three-dimensional sources, one integer
        for one diensional sources, and not significant for point sources.

    """

    def __init__(self, **kwargs):
        '''Initialize the Source with empty strings for the isotope list
        and photon list'''
        self._isotope_list = []   # LIST of isotopes and activities (Bq)
        self._unique_photons = []  # LIST of unique photons and activities (Bq)
        self.points_per_dimension = [10, 10, 10]
        self._include_key_progeny = False
        self._max_photon_energies = 30
        self._grouping_option = GroupOption.HYBRID
        super().__init__(**kwargs)

    @property
    def grouping(self):
        """:class:`GroupOption` : State defining the photon energy group option."""
        return self._grouping_option

    @grouping.setter
    def grouping(self, value):
        """:class:`GroupOption` : State defining the photon energy group option."""
        if value == GroupOption.HYBRID.value:
            self._grouping_option = GroupOption.HYBRID
        elif value == GroupOption.GROUP.value:
            self._grouping_option = GroupOption.GROUP
        elif value == GroupOption.DISCRETE.value:
            self._grouping_option = GroupOption.DISCRETE
        else:
            raise ValueError("Invalid grouping option "+ str(value))

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
        new_isotope : :class:`zap_me_not.isotope.Isotope`
            The isotope to be added to the source.
        curies : float
            The activity in curies.
        """
        self._isotope_list.append((new_isotope, curies*3.7E10))

    def add_isotope_bq(self, new_isotope, becquerels):
        """Adds an isotope and activity in becquerels to the isotope list

        Parameters
        ----------
        new_isotope : :class:`zap_me_not.isotope.Isotope`
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

    def _get_photon_source_list(self):
        """Returns a list of photons in the source

        This list of photons combines the Isotopes and the
        unique_photons specified in the Source definition.
        The photon intensities are scaled to **one source point**.

        Returns
        -------
        :class:`list` of :class:`tuple`
            List of photon tuples, each tuple containing a
            photon energy in MeV and an activity in **Bq//source point**.
        """
        photon_dict = dict()
        keys = photon_dict.keys()
        
        temporary_isotope_list = self._isotope_list[:]
        # add key progeny if required
        if self._include_key_progeny == True:
            for next_isotope in self._isotope_list: 			
                isotope_detail = isotope.Isotope(next_isotope[0])
                if isotope_detail.key_progeny != None:
                    for key, value in isotope_detail.key_progeny.items():
                        temporary_isotope_list.append((key, next_isotope[1]*value))

        # search isotope list for photons to be added to the photon list
        # next_isotope will be a tuple of name and Bq
        for next_isotope in temporary_isotope_list:
            isotope_detail = isotope.Isotope(next_isotope[0])
            if isotope_detail.photons != None:
                for photon in isotope_detail.photons:
                    # test to see if photon energy is already on the list
                    # and then add photon emmision rate (intensity*Bq).
                    if photon[0] in keys:
                        photon_dict[photon[0]] = photon_dict[photon[0]] + \
                            photon[1]*next_isotope[1]
                    else:
                        photon_dict[photon[0]] = photon[1]*next_isotope[1]
        for photon in self._unique_photons:
            # test to see if photon energy is already on the list
            # and then add photon emmision rate.
            if photon[0] in keys:
                photon_dict[photon[0]] = photon_dict[photon[0]] + photon[1]
            else:
                photon_dict[photon[0]] = photon[1]
        photon_list = []
        scaling_factor = np.prod(self.points_per_dimension)
        for key, value in photon_dict.items():
            photon_list.append((key, value/scaling_factor))
        photon_list = sorted(photon_list)
        if self._grouping_option == GroupOption.GROUP or ((self._grouping_option == GroupOption.HYBRID) and (len(photon_list) > self._max_photon_energies)):
            # group the photons
            minEnergy = photon_list[0][0]
            maxEnergy = photon_list[-1][0]
            (groupEnergies, stepSize) = np.linspace(minEnergy, maxEnergy, self._max_photon_energies, retstep=True)
            binBoundaries = groupEnergies + (stepSize/2)
            binBoundaries = np.concatenate([np.array([binBoundaries[0]-stepSize]),binBoundaries])
            binplace = np.digitize(photon_list, binBoundaries)[:,0] # Returns the appropriate bin for each photon
            photonArray = np.array(photon_list) # convert the photon list to an array for further processing
            returnValue = np.zeros((self._max_photon_energies,2))
            for i in range(1,self._max_photon_energies+1):
                # determine which photons are in each bin
                subset = photonArray[np.where(binplace == i)]
                csum = np.sum(subset[:,1]) # total emission rate
                if (csum != 0):
                    returnValue[i-1,0] = np.sum(subset[:,0]*subset[:,1])/csum
                    returnValue[i-1,1] = csum
            returnValue = returnValue[np.all(returnValue, axis=1)] # keep only groups with non-zero intensity
            photon_list = returnValue.tolist()
        return photon_list

    @abc.abstractmethod
    def _get_source_points(self):
        pass

# -----------------------------------------------------------


class LineSource(Source, shield.Shield):
    """Models a line radiation source 

    Parameters
    ----------
    start : :class:`list`
        Cartiesian X, Y, and Z coordinates of the starting point of the line source.
    end : :class:`list`
        Cartiesian X, Y, and Z coordinates of the ending point of the line source.
    **kwargs
        Arbitrary keyword arguments.

    Attributes
    ----------
    material : :class: `material.Material`
        Material properties of the shield
    origin : :class:`numpy.ndarray`
        Vector location of one end of the line source.
    end : :class:`numpy.ndarray`
        Vector location of one end of the line source.
    """

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
        self.points_per_dimension = 10

    def _get_source_points(self):
        """Generates a list of point sources within the Source geometry.

        Returns
        -------
        :class:`list` of :class:`numpy.adarray`
            A list of vector locations within the Source body
        """
        spacings = np.linspace(1, self.points_per_dimension,
                               self.points_per_dimension)
        mesh_width = self._length/self.points_per_dimension
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
        ray : :class:`zap_me_not.ray.FiniteLengthRay`
            The finite length ray that is checked for intersections with the shield.

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
        ray : :class:`zap_me_not.ray.FiniteLengthRay`
            The finite length ray that is checked for intersections with the shield.
        photon_energy : float
            The photon energy in MeV

        Returns
        -------
        int
            Always returns 0
        """
        return 0

# -----------------------------------------------------------


class PointSource(Source, shield.Shield):
    """Models a point radiation source

    Parameters
    ----------
    x : float
        Cartiesian X coordinate of the point source.
    y : float
        Cartiesian Y coordinate of the point source.
    z : float
        Cartiesian Z coordinate of the point source.
    **kwargs
        Arbitrary keyword arguments.

    Attributes
    ----------
    material : :class: `zap_me_not.material.Material`
        Material properties of the shield
    inner_radius : float
        Radius of the annulus inner surface.
    outer_radius : float
        Radius of the annulus outer surface.
    origin : :class:`numpy.ndarray`
        Vector location of a point on the annulus centerline.
    dir : :class:`numpy.ndarray`
        Vector normal of the annulus centerline.
    """

    def __init__(self, x, y, z, **kwargs):
        '''Initialize with an x,y,z location in space'''
        self._x = x
        self._y = y
        self._z = z
        # let the point source have a dummy material of air at a zero density
        kwargs['material_name'] = 'air'
        kwargs['density'] = 0
        super().__init__(**kwargs)
        self.points_per_dimension = 1

    def _get_source_points(self):
        """Generates a list of point sources within the Source geometry.

        Returns
        -------
        :class:`list` of :class:`numpy.adarray`
            A list of vector locations within the Source body.  In this class the
            list is only a single entry.
        """
        return[(self._x, self._y, self._z)]

    def _get_crossing_length(self, ray):
        """Calculates the linear intersection length of a ray and the shield

        Parameters
        ----------
        ray : :class:`zap_me_not.ray.FiniteLengthRay`
            The finite length ray that is checked for intersections with the shield.

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
        ray : :class:`zap_me_not.ray.FiniteLengthRay`
            The finite length ray that is checked for intersections with the shield.
            Always returns 0 for the Point source.
        photon_energy : float
            The photon energy in MeV
            
        Returns
        -------
        int
            Always returns 0
        """
        return 0

    def vtk(self):
        """Creates a display object

        Returns
        -------
        :class:`pyvista.PolyData`
            A small sphere object representing the point source.
        """
        return pyvista.Sphere(center=(self._x, self._y, self._z), radius=1)


# -----------------------------------------------------------


# class SphereSource(Source, shield.Sphere):
#     '''Axis-Aligned rectangular box source'''
#     # initialize with box_center, box_dimensions, material(optional),
#     # density(optional)

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

#     def _get_source_points(self):

#         # calculate the radius of each "equal area" annular region
#         totalVolume = 4/3*math.pi*self.radius**3
#         old_radius = 0
#         annular_locations = []
#         for i in range(self.points_per_dimension[0]):
#             new_radius = math.sqrt((running_area+annular_area)/math.pi)
#             annular_locations.append((new_radius+old_radius)/2)
#             old_radius = new_radius

#         angle_increment = 2*math.pi/self.points_per_dimension[1]
#         start_angle = angle_increment/2
#         angle_locations = []
#         for i in range(self.points_per_dimension[1]):
#             angle_locations.append(start_angle + (i*angle_increment))

#         length_increment = self.length/self.points_per_dimension[2]
#         start_length = length_increment/2
#         length_locations = []
#         for i in range(self.points_per_dimension[2]):
#             length_locations.append(start_length + (i*length_increment))

#         # iterate through each dimension, building a list of source points
#         source_points = []
#         for radial_location in annular_locations:
#             r = radial_location
#             for angle_location in angle_locations:
#                 theta = angle_location
#                 for length_location in length_locations:
#                     z = length_location
#                     # convert cylintrical to rectangular coordinates
#                     x = r * math.cos(theta)
#                     y = r * math.sin(theta)
#                     source_points.append([x, y, z])
#         return source_points

# -----------------------------------------------------------


class BoxSource(Source, shield.Box):
    """Models a Axis-Aligned rectangular box source

    Parameters
    ----------
    material_name : :class:`zap_me_not.material.Material`
        Shield material type
    box_center : :class:`list`
        X, Y, and Z coordinates of the box center.
    box_dimensions : :class:`list`
        X, Y, and Z dimensions of the box.
    density : float, optional
        Material density in g/cm3.

    Attributes
    ----------
    material : :class: `material.Material`
        Material properties of the shield
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_source_points(self):
        """Generates a list of point sources within the Source geometry.

        Returns
        -------
        :class:`list` of :class:`numpy.adarray`
            A list of vector locations within the Source body.
        """
        source_points = []
        mesh_width = self.box_dimensions/self.points_per_dimension
        start_point = self.box_center-(self.box_dimensions)/2+(mesh_width/2)
        for i in range(self.points_per_dimension[0]):
            x = start_point[0]+mesh_width[0]*i
            for j in range(self.points_per_dimension[1]):
                y = start_point[1]+mesh_width[1]*j
                for k in range(self.points_per_dimension[2]):
                    z = start_point[2]+mesh_width[2]*k
                    source_points.append([x, y, z])
        return source_points

# -----------------------------------------------------------


class ZAlignedCylinderSource(Source, shield.ZAlignedCylinder):
    """Models a cylindrical source axis-aligned with the Z axis.

    Parameters
    ----------
    **kwargs
        Arbitrary keyword arguments.

    """
    # initialize with cylinderCenter, cylinderLength, cylinderRadius,
    # material(optional), density(optional)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_source_points(self):
        """Generates a list of point sources within the Source geometry.

        Returns
        -------
        :class:`list` of :class:`numpy.adarray`
            A list of vector locations within the Source body.
        """

        # calculate the radius of each "equal area" annular region
        total_area = math.pi*self.radius**2
        annular_area = total_area/self.points_per_dimension[0]
        old_radius = 0
        running_area = 0
        annular_locations = []
        for i in range(self.points_per_dimension[0]):
            new_radius = math.sqrt((running_area+annular_area)/math.pi)
            annular_locations.append((new_radius+old_radius)/2)
            old_radius = new_radius
            running_area = running_area+annular_area

        angle_increment = 2*math.pi/self.points_per_dimension[1]
        start_angle = angle_increment/2
        angle_locations = []
        for i in range(self.points_per_dimension[1]):
            angle_locations.append(start_angle + (i*angle_increment))

        length_increment = self.length/self.points_per_dimension[2]
        start_length = length_increment/2
        length_locations = []
        for i in range(self.points_per_dimension[2]):
            length_locations.append(start_length + (i*length_increment))

        # iterate through each dimension, building a list of source points
        source_points = []
        for radial_location in annular_locations:
            r = radial_location
            for angle_location in angle_locations:
                theta = angle_location
                for length_location in length_locations:
                    z = length_location
                    # convert cylintrical to rectangular coordinates
                    x = r * math.cos(theta)
                    y = r * math.sin(theta)
                    source_points.append([x, y, z])
        return source_points

# -----------------------------------------------------------


class YAlignedCylinderSource(Source, shield.YAlignedCylinder):
    """Models a cylindrical source axis-aligned with the Y axis.

    Parameters
    ----------
    **kwargs
        Arbitrary keyword arguments.

    """
    # initialize with cylinderCenter, cylinderLength, cylinderRadius,
    # material(optional), density(optional)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_source_points(self):
        """Generates a list of point sources within the Source geometry.

        Returns
        -------
        :class:`list` of :class:`numpy.adarray`
            A list of vector locations within the Source body.
        """

        # calculate the radius of each "equal area" annular region
        total_area = math.pi*self.radius**2
        annular_area = total_area/self.points_per_dimension[0]
        old_radius = 0
        running_area = 0
        annular_locations = []
        for i in range(self.points_per_dimension[0]):
            new_radius = math.sqrt((running_area+annular_area)/math.pi)
            annular_locations.append((new_radius+old_radius)/2)
            old_radius = new_radius
            running_area = running_area+annular_area

        angle_increment = 2*math.pi/self.points_per_dimension[1]
        start_angle = angle_increment/2
        angle_locations = []
        for i in range(self.points_per_dimension[1]):
            angle_locations.append(start_angle + (i*angle_increment))

        length_increment = self.length/self.points_per_dimension[2]
        start_length = length_increment/2
        length_locations = []
        for i in range(self.points_per_dimension[2]):
            length_locations.append(start_length + (i*length_increment))

        # iterate through each dimension, building a list of source points
        source_points = []
        for radial_location in annular_locations:
            r = radial_location
            for angle_location in angle_locations:
                theta = angle_location
                for length_location in length_locations:
                    y = length_location
                    # convert cylintrical to rectangular coordinates
                    x = r * math.cos(theta)
                    z = r * math.sin(theta)
                    source_points.append([x, y, z])
        return source_points

# -----------------------------------------------------------


class XAlignedCylinderSource(Source, shield.YAlignedCylinder):
    """Models a cylindrical source axis-aligned with the X axis.

    Parameters
    ----------
    **kwargs
        Arbitrary keyword arguments.

    """
    # initialize with cylinderCenter, cylinderLength, cylinderRadius,
    # material(optional), density(optional)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_source_points(self):
        """Generates a list of point sources within the Source geometry.

        Returns
        -------
        :class:`list` of :class:`numpy.adarray`
            A list of vector locations within the Source body.
        """

        # calculate the radius of each "equal area" annular region
        total_area = math.pi*self.radius**2
        annular_area = total_area/self.points_per_dimension[0]
        old_radius = 0
        running_area = 0
        annular_locations = []
        for i in range(self.points_per_dimension[0]):
            new_radius = math.sqrt((running_area+annular_area)/math.pi)
            annular_locations.append((new_radius+old_radius)/2)
            old_radius = new_radius
            running_area = running_area+annular_area

        angle_increment = 2*math.pi/self.points_per_dimension[1]
        start_angle = angle_increment/2
        angle_locations = []
        for i in range(self.points_per_dimension[1]):
            angle_locations.append(start_angle + (i*angle_increment))

        length_increment = self.length/self.points_per_dimension[2]
        start_length = length_increment/2
        length_locations = []
        for i in range(self.points_per_dimension[2]):
            length_locations.append(start_length + (i*length_increment))

        # iterate through each dimension, building a list of source points
        source_points = []
        for radial_location in annular_locations:
            r = radial_location
            for angle_location in angle_locations:
                theta = angle_location
                for length_location in length_locations:
                    x = length_location
                    # convert cylintrical to rectangular coordinates
                    y = r * math.cos(theta)
                    z = r * math.sin(theta)
                    source_points.append([x, y, z])
        return source_points

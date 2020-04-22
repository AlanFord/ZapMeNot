import abc
import math

import numpy as np

from ZapMeNot import shield, isotope


class Source(metaclass=abc.ABCMeta):
    '''Abtract class to model a radiation source.  Maintains a list of
    isotopes and can returna list of point source locations within the
    body of the Source'''

    def __init__(self, **kwargs):
        '''Initialize the Source with empty strings for the isotope list
        and photon list'''
        self.isotope_list = []   # LIST of isotopes and activities (Bq)
        self.unique_photons = []  # LIST of unique photons and activities (Bq)
        self.points_per_dimension = [10, 10, 10]
        super().__init__(**kwargs)

    def add_isotope_curies(self, new_isotope, curies):
        "add an isotope and activity to the isotope list"
        # LIST of tuples, isotope object and activity
        self.isotope_list.append((new_isotope, curies*3.7E10))

    def add_isotope_bq(self, new_isotope, becquerels):
        "add an isotope and activity to the isotope list"
        # LIST of tuples, isotope object and activity
        self.isotope_list.append((new_isotope, becquerels))

    def add_photon(self, energy, becquerels):
        "add a photon and activity to the photon list"
        self.unique_photons.append((energy, becquerels))

    def list_isotopes(self):
        # echo back a list of the isotopes currently stored
        return self.isotope_list

    def list_unique_photons(self):
        return self.unique_photons

    def get_photon_source_list(self):
        "returns a list of unique photon energies and activities"
        photon_dict = dict()
        keys = photon_dict.keys()
        # test to see if photon energy is already on the list
        # and then add photon emmision rate (intensity*Bq).

        # next_isotope will be a tuple of name and Bq
        for next_isotope in self.isotope_list:
            isotope_detail = isotope.Isotope(next_isotope[0])
            for photon in isotope_detail.photons:
                if photon[0] in keys:
                    photon_dict[photon[0]] = photon_dict[photon[0]] + \
                        photon[1]*next_isotope[1]
                else:
                    photon_dict[photon[0]] = photon[1]*next_isotope[1]
        for photon in self.unique_photons:
            if photon[0] in keys:
                photon_dict[photon[0]] = photon_dict[photon[0]] + photon[1]
            else:
                photon_dict[photon[0]] = photon[1]
        photon_list = []
        scaling_factor = np.prod(self.points_per_dimension)
        for key, value in photon_dict.items():
            photon_list.append((key, value/scaling_factor))
        return sorted(photon_list)

    @abc.abstractmethod
    def get_source_points(self):
        pass

# -----------------------------------------------------------


class LineSource(Source, shield.Shield):
    '''Modeling a point source of radiation.'''

    def __init__(self, start, end, **kwargs):
        "Initialize"
        self.origin = np.array(start)
        self.end = np.array(end)
        self.length = np.linalg.norm(self.end - self.origin)
        self.dir = (self.end - self.origin)/self.length
        # let the point source have a dummy material of air at a zero density
        kwargs['material_name'] = 'air'
        kwargs['density'] = 0
        super().__init__(**kwargs)
        # initialize points_per_dimension after super() to force a
        # single dimension
        self.points_per_dimension = 10

    def get_source_points(self):
        spacings = np.linspace(1, self.points_per_dimension,
                               self.points_per_dimension)
        mesh_width = self.length/self.points_per_dimension
        spacings = spacings*mesh_width
        spacings = spacings-(mesh_width/2)
        source_points = []
        for dist in spacings:
            location = self.origin+self.dir*dist
            source_points.append(location)
        return source_points

    def get_crossing_length(self, ray):
        '''returns a  crossing length'''
        return 0

    def get_crossing_mfp(self, ray, photon_energy):
        '''returns the crossing mfp'''
        return 0

# -----------------------------------------------------------


class PointSource(Source, shield.Shield):
    '''Modeling a point source of radiation.'''

    def __init__(self, x, y, z, **kwargs):
        '''Initialize with an x,y,z location in space'''
        self.x = x
        self.y = y
        self.z = z
        # let the point source have a dummy material of air at a zero density
        kwargs['material_name'] = 'air'
        kwargs['density'] = 0
        super().__init__(**kwargs)
        self.points_per_dimension = 1

    def get_source_points(self):
        return[(self.x, self.y, self.z)]

    def get_crossing_length(self, ray):
        '''returns a  crossing length'''
        return 0

    def get_crossing_mfp(self, ray, photon_energy):
        '''returns the crossing mfp'''
        return 0

# -----------------------------------------------------------


# class SphereSource(Source, shield.Sphere):
#     '''Axis-Aligned rectangular box source'''
#     # initialize with box_center, box_dimensions, material(optional),
#     # density(optional)

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

#     def get_source_points(self):

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
    '''Axis-Aligned rectangular box source'''
    # initialize with box_center, box_dimensions, material(optional),
    # density(optional)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_source_points(self):
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
    '''Axis-Aligned rectangular box source'''
    # initialize with cylinderCenter, cylinderLength, cylinderRadius,
    # material(optional), density(optional)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_source_points(self):

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
    '''Axis-Aligned rectangular box source'''
    # initialize with cylinderCenter, cylinderLength, cylinderRadius,
    # material(optional), density(optional)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_source_points(self):

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
    '''Axis-Aligned rectangular box source'''
    # initialize with cylinderCenter, cylinderLength, cylinderRadius,
    # material(optional), density(optional)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_source_points(self):

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

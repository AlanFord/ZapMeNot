import abc
import math

import numpy as np

from ZapMeNot import material
# import material

# -----------------------------------------------------------


class Shield:
    '''Abtract class to model a shield.'''

    def __init__(self, material_name=None, density=None, **kwargs):
        '''Initialize the Shield with a void material
        and photon list'''
        self.material = material.Material(material_name)
        if density is not None:
            self.material.set_density(density)
        super().__init__(**kwargs)

    @abc.abstractmethod
    def get_crossing_length(self, ray):
        '''returns a  crossing length'''

    @abc.abstractmethod
    def get_crossing_mfp(self, ray, photon_energy):
        '''returns the crossing mfp'''

    @staticmethod
    def line_plane_collision(plane_normal, plane_point, ray_origin,
                             ray_normal, epsilon=1e-6):
        # based on
        # https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-plane-and-ray-disk-intersection
        ndotu = plane_normal.dot(ray_normal)
        if abs(ndotu) < epsilon:
            return None
        w = plane_point - ray_origin
        t = w.dot(plane_normal)/ndotu
        return t

# -----------------------------------------------------------


class SemiInfiniteXSlab(Shield):
    ''' Infinite slab shield perpendicular to the X axis'''

    def __init__(self, material_name, x_start, x_end, density=None):
        '''Initialize material composition and location of the slab shield'''
        super().__init__(material_name=material_name, density=density)
        self.x_start = x_start
        self.x_end = x_end

    def get_crossing_length(self, ray):
        '''returns a  crossing length'''
        ray_origin = ray.origin
        ray_unit_vector = ray.dir
        plane_normal = np.array([1, 0, 0])
        # get length to one crossing point
        plane_point = np.array([self.x_start, 0, 0])
        first_length = self.line_plane_collision(
            plane_normal, plane_point, ray_origin, ray_unit_vector)
        if first_length is None:
            # ray is parallel to plane
            return 0
        # get length to second crossing point
        plane_point = np.array([self.x_end, 0, 0])
        second_length = self.line_plane_collision(
            plane_normal, plane_point, ray_origin, ray_unit_vector)
        if second_length is None:
            # ray is parallel to plane
            return 0
        if (first_length < 0 and second_length < 0):
            # ray starts and ends entirely on one side of the shield
            return 0
        if (first_length > ray.length and second_length > ray.length):
            # ray starts and ends entirely on one side of the shield
            return 0
        # remainder of cases have some sort of partial or full crossing
        t0 = min(first_length, second_length)
        t1 = max(first_length, second_length)
        if ((t0 < 0) and (t1 > ray.length)):
            # ray is intirely within the slab
            return ray.length
        if ((t0 < 0) and (t1 < ray.length)):
            # ray start in slab and crosses out
            return t1
        if ((t0 > 0) and (t1 > ray.length)):
            # ray starts outside slab and ends inside slab
            return ray.length - t0
        # we are left with a full crossing
        return t1 - t0

    def get_crossing_mfp(self, ray, photon_energy):
        '''returns the crossing mfp'''
        distance = self.get_crossing_length(ray)
        return self.material.get_mfp(photon_energy, distance)

# -----------------------------------------------------------


class Sphere(Shield):
    def __init__(self, material_name, sphere_center, sphere_radius, density=None):
        '''Initialize material composition and location of the slab shield'''
        super().__init__(material_name=material_name, density=density)
        self.center = np.array(sphere_center)
        self.radius = np.array(sphere_radius)

    def get_crossing_mfp(self, ray, photon_energy):
        '''returns the crossing mfp'''
        distance = self.get_crossing_length(ray)
        return self.material.get_mfp(photon_energy, distance)

    def get_crossing_length(self, ray):
        # based on
        # http://viclw17.github.io/2018/07/16/raytracing-ray-sphere-intersection/
        a = np.dot(ray.dir, ray.dir)
        b = 2 * np.dot(ray.dir, ray.origin - self.center)
        c = np.dot(ray.origin-self.center, ray.origin -
                   self.center) - self.radius**2
        discriminant = b**2 - 4*a*c
        if discriminant <= 0:
            # sphere is missed or tangent
            return 0
        root = np.sqrt(discriminant)
        t0 = (-b - root)/(2*a)
        t1 = (-b + root)/(2*a)
        big_list = []
        for a_length in [t0, t1]:
            if (a_length >= 0) and (a_length <= ray.length):
                big_list.append(a_length)
        if len(big_list) != 2:
            # if not 2 intersections, look for ray endpoints inside the sphere
            if self.contains(ray.origin):
                big_list.append(0)
            if self.contains(ray.end):
                big_list.append(ray.length)
        if len(big_list) == 0:
            # ray misses the sphere
            return 0
        if len(big_list) != 2:
            # this shouldn't occur
            raise ValueError("Shield doesn't have 2 crossings")
        return abs(big_list[1]-big_list[0])

    def contains(self, point):
        ray = point - self.center
        if np.dot(ray, ray) > self.radius**2:
            return False
        return True

# -----------------------------------------------------------


class Box(Shield):
    '''Axis-Aligned rectangular box'''

    def __init__(self, material_name, box_center, box_dimensions, density=None):
        '''Initialize material composition and location of the slab shield'''
        super().__init__(material_name=material_name, density=density)
        self.box_center = np.array(box_center)
        self.box_dimensions = np.array(box_dimensions)

    def get_crossing_mfp(self, ray, photon_energy):
        '''returns the crossing mfp'''
        distance = self.get_crossing_length(ray)
        return self.material.get_mfp(photon_energy, distance)

    def get_crossing_length(self, ray):
        '''returns a  crossing length'''
        # get a list of crossing points
        crossings = self.intersect_axis_aligned_box(ray)
        # two crossings indicates a full-shield crossing
        # one crossing indicates that either (common) the source is
        #    in the shield or (uncommon) the dose point is in the
        #    shield
        # zero crossings can indicate that either both source and
        #    dose points are in the shield or that the shield is
        #    missed entirely
        if len(crossings) != 2:
            # check for start/end of ray within the box
            if self.contains(ray.origin):
                crossings.insert(0, ray.origin)
            if self.contains(np.array(ray.end)):
                crossings.append(np.array(ray.end))
        if len(crossings) == 0:
            # likely it's a complete miss
            return 0
        if len(crossings) != 2:
            # shouldn't ever get here
            raise ValueError("Shield doesn't have 2 crossings")
        # let numpy do the heavy lifting
        return np.linalg.norm(crossings[0]-crossings[1])

    def contains(self, point):
        x = point[0]
        y = point[1]
        z = point[2]
        xmin = self.box_center[0]-self.box_dimensions[0]/2
        xmax = self.box_center[0]+self.box_dimensions[0]/2
        ymin = self.box_center[1]-self.box_dimensions[1]/2
        ymax = self.box_center[1]+self.box_dimensions[1]/2
        zmin = self.box_center[2]-self.box_dimensions[2]/2
        zmax = self.box_center[2]+self.box_dimensions[2]/2
        if (xmin <= x and x <= xmax and ymin <= y and y <= ymax and zmin <= z
                and z <= zmax):
            return True
        return False

    def intersect_axis_aligned_box(self, ray):
        'returns 0, 1, or 2 points of intersection'
        results = []
        bounds = [self.box_center - (self.box_dimensions/2),
                  self.box_center + (self.box_dimensions/2)]
        tmin = (bounds[ray.sign[0]][0] - ray.origin[0]) * ray.invdir[0]
        tmax = (bounds[1-ray.sign[0]][0] - ray.origin[0]) * ray.invdir[0]
        tymin = (bounds[ray.sign[1]][1] - ray.origin[1]) * ray.invdir[1]
        tymax = (bounds[1-ray.sign[1]][1] - ray.origin[1]) * ray.invdir[1]

        if (tmin > tymax) or (tymin > tmax):
            return results

        if tymin > tmin:
            tmin = tymin
        if tymax < tmax:
            tmax = tymax

        tzmin = (bounds[ray.sign[2]][2] - ray.origin[2]) * ray.invdir[2]
        tzmax = (bounds[1-ray.sign[2]][2] - ray.origin[2]) * ray.invdir[2]

        if ((tmin > tzmax) or (tzmin > tmax)):
            return results

        if tzmin > tmin:
            tmin = tzmin

        if tzmax < tmax:
            tmax = tzmax

        if (tmin >= 0) and (tmin <= ray.length):
            results.append(ray.origin + ray.dir*tmin)
        if (tmax >= 0) and (tmax <= ray.length):
            results.append(ray.origin + ray.dir*tmax)

        return results

# -----------------------------------------------------------


class InfiniteAnnulus(Shield):
    def __init__(self, material_name, cylinder_origin, cylinder_axis,
                 cylinder_inner_radius, cylinder_outer_radius, density=None):
        '''Initialize material composition and location of the shield'''
        super().__init__(material_name=material_name, density=density)
        self.inner_radius = cylinder_inner_radius
        self.outer_radius = cylinder_outer_radius
        self.origin = np.array(cylinder_origin)
        axis = np.array(cylinder_axis)
        self.dir = axis/np.linalg.norm(axis)

    def get_crossing_mfp(self, ray, photon_energy):
        '''returns the crossing mfp'''
        distance = self.get_crossing_length(ray)
        return self.material.get_mfp(photon_energy, distance)

    def get_crossing_length(self, ray):
        '''returns a  crossing length'''
        # get a list of crossing points
        crossings = self.intersect(ray)
        # zero crossings can indicate that either both source and
        #    dose points are in the shield or that the shield is
        #    missed entirely
        # one crossing indicates that either (common) the source is
        #    in the shield or (uncommon) the dose point is in the
        #    shield
        # two crossings indicates a single in/out or out/in crossing
        # four crossings indicate a full-shield crossing
        if len(crossings) not in [2, 4]:
            if self.contains(ray.origin):
                crossings.append(0)
            if self.contains(np.array(ray.end)):
                crossings.append(ray.length)
        if len(crossings) == 0:
            return 0
        if len(crossings) not in [2, 4]:
            raise ValueError("Shield doesn't have valid crossings")
        crossings.sort()
        if len(crossings) == 2:
            return crossings[1]-crossings[0]
        # let numpy do the heavy lifting
        return (crossings[1]-crossings[0]) + (crossings[3] - crossings[2])

    def contains(self, point):
        # determine scalar projection of point on cylinder centerline
        rando = np.dot(point-self.origin, self.dir)
        # check the radial distance from cylinder centerline
        parto = (self.origin+self.dir*rando) - point
        if (np.dot(parto, parto) < self.inner_radius**2) or \
                (np.dot(parto, parto) > self.outer_radius**2):
            return False
        return True

    def intersect(self, ray):
        # returns a list of >>DISTANCES<< olong the ray vector
        #
        # based on https://mrl.nyu.edu/~dzorin/rend05/lecture2.pdf
        # and
        # https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-plane-and-ray-disk-intersection
        results = []
        for radius in [self.inner_radius, self.outer_radius]:
            deltap = ray.origin - self.origin
            part1 = ray.dir - (np.dot(ray.dir, self.dir)*self.dir)
            part2 = deltap - (np.dot(deltap, self.dir)*self.dir)
            a = np.dot(part1, part1)
            b = 2*np.dot(part1, part2)
            c = np.dot(part2, part2) - radius**2
            zoro = b**2 - 4*a*c
            if zoro > 0:
                # roots are real, then are two intersections on an
                # "infinite" cylinder
                meo = math.sqrt(zoro)
                t1 = (-b + meo)/(2*a)
                t2 = (-b - meo)/(2*a)
                # check to see if the intersections occur in the finite
                # length of the cylinder
                for t in [t1, t2]:
                    # discard line/cylinder intersections outside of the
                    # length of the ray
                    if t >= 0 and t <= ray.length:
                        results.append(t)
        return results
# -----------------------------------------------------------


class YAlignedInfiniteAnnulus(InfiniteAnnulus):
    '''Y Axis-Aligned cylinder of finite length'''

    def __init__(self, material_name, cylinder_center, cylinder_inner_radius,
                 cylinder_outer_radius, density=None):
        '''Initialize material composition and location of the shield'''
        super().__init__(material_name=material_name, density=density,
                         cylinder_origin=cylinder_center,
                         cylinder_inner_radius=cylinder_inner_radius,
                         cylinder_outer_radius=cylinder_outer_radius,
                         cylinder_axis=[0, 1, 0])

# -----------------------------------------------------------


class XAlignedInfiniteAnnulus(InfiniteAnnulus):
    '''X Axis-Aligned cylinder of finite length'''

    def __init__(self, material_name, cylinder_center, cylinder_inner_radius,
                 cylinder_outer_radius, density=None):
        '''Initialize material composition and location of the shield'''
        super().__init__(material_name=material_name, density=density,
                         cylinder_origin=cylinder_center,
                         cylinder_inner_radius=cylinder_inner_radius,
                         cylinder_outer_radius=cylinder_outer_radius,
                         cylinder_axis=[1, 0, 0])

# -----------------------------------------------------------


class ZAlignedInfiniteAnnulus(InfiniteAnnulus):
    '''Z Axis-Aligned cylinder of finite length'''

    def __init__(self, material_name, cylinder_center, cylinder_inner_radius,
                 cylinder_outer_radius, density=None):
        '''Initialize material composition and location of the shield'''
        super().__init__(material_name=material_name, density=density,
                         cylinder_origin=cylinder_center,
                         cylinder_inner_radius=cylinder_inner_radius,
                         cylinder_outer_radius=cylinder_outer_radius,
                         cylinder_axis=[0, 0, 1])

# -----------------------------------------------------------


class CappedCylinder(Shield):
    '''General Cylinder'''

    def __init__(self, material_name, cylinder_start, cylinder_end,
                 cylinder_radius, density=None):
        '''Initialize material composition and location of the shield'''
        super().__init__(material_name=material_name, density=density)
        self.radius = cylinder_radius
        self.origin = np.array(cylinder_start)
        self.end = np.array(cylinder_end)
        self.length = np.linalg.norm(self.end - self.origin)
        self.dir = (self.end - self.origin)/self.length

    def get_crossing_mfp(self, ray, photon_energy):
        '''returns the crossing mfp'''
        distance = self.get_crossing_length(ray)
        return self.material.get_mfp(photon_energy, distance)

    def get_crossing_length(self, ray):
        '''returns a  crossing length'''
        # get a list of crossing points
        crossings = self.intersect(ray)
        # two crossings indicates a full-shield crossing
        # one crossing indicates that either (common) the source is
        #    in the shield or (uncommon) the dose point is in the
        #    shield
        # zero crossings can indicate that either both source and
        #    dose points are in the shield or that the shield is
        #    missed entirely
        if len(crossings) != 2:
            # check for start/end of ray within the cylinder
            if self.contains(ray.origin):
                crossings.insert(0, ray.origin)
            if self.contains(np.array(ray.end)):
                crossings.append(np.array(ray.end))
        if len(crossings) == 0:
            # likely it's a complete miss
            return 0
        if len(crossings) != 2:
            # shouldn't ever get here
            raise ValueError("Shield doesn't have 2 crossings")
        # let numpy do the heavy lifting
        return np.linalg.norm(crossings[0]-crossings[1])

    def contains(self, point):
        # determine scalar projection of point on cylinder centerline
        rando = np.dot(point-self.origin, self.dir)
        if rando < 0 or rando > self.length:
            return False
        # check the radial distance from cylinder centerline
        parto = (self.origin+self.dir*rando) - point
        if np.dot(parto, parto) > self.radius**2:
            return False
        return True

    def intersect(self, ray):
        # based on https://mrl.nyu.edu/~dzorin/rend05/lecture2.pdf
        # and
        # https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-plane-and-ray-disk-intersection
        results = []
        # test for
        deltap = ray.origin - self.origin
        part1 = ray.dir - (np.dot(ray.dir, self.dir)*self.dir)
        part2 = deltap - (np.dot(deltap, self.dir)*self.dir)
        a = np.dot(part1, part1)
        b = 2*np.dot(part1, part2)
        c = np.dot(part2, part2) - self.radius**2
        zoro = b**2 - 4*a*c
        if zoro > 0:
            # roots are real, then are two intersections on an
            # "infinite" cylinder
            meo = math.sqrt(zoro)
            t1 = (-b + meo)/(2*a)
            t2 = (-b - meo)/(2*a)
            # check to see if the intersections occur in the finite length
            # of the cylinder
            for t in [t1, t2]:
                # discard line/cylinder intersections outside of the
                # length of the ray
                if t >= 0 and t <= ray.length:
                    intersection = ray.origin + ray.dir*t
                    loc = np.dot(intersection-self.origin, self.dir)
                    # keep only intersections within the finite length
                    # of the cylinder
                    if loc >= 0 and loc < self.length:
                        results.append(intersection)
        # check to see if there are intersections on the caps
        for disk_center in [self.origin, self.end]:
            t = self.line_plane_collision(
                self.dir, disk_center, ray.origin, ray.dir)
            if t is not None and t >= 0 and t <= ray.length:
                point = ray.origin + ray.dir*t
                radial = point - disk_center
                if radial.dot(radial) < self.radius**2:
                    results.append(point)
        return results

# -----------------------------------------------------------


class YAlignedCylinder(CappedCylinder):
    '''Y Axis-Aligned cylinder of finite length'''

    def __init__(self, material_name, cylinder_center, cylinder_length,
                 cylinder_radius, density=None):
        '''Initialize material composition and location of the shield'''
        cylinder_start = [cylinder_center[0],
                          cylinder_center[1]-cylinder_length/2, cylinder_center[2]]
        cylinder_end = [cylinder_center[0], cylinder_center[1] +
                        cylinder_length/2, cylinder_center[2]]
        super().__init__(material_name=material_name, density=density,
                         cylinder_start=cylinder_start, cylinder_end=cylinder_end,
                         cylinder_radius=cylinder_radius)

# -----------------------------------------------------------


class XAlignedCylinder(CappedCylinder):
    '''X Axis-Aligned cylinder of finite length'''

    def __init__(self, material_name, cylinder_center, cylinder_length,
                 cylinder_radius, density=None):
        '''Initialize material composition and location of the shield'''
        cylinder_start = [cylinder_center[0]-cylinder_length /
                          2, cylinder_center[1], cylinder_center[2]]
        cylinder_end = [cylinder_center[0]+cylinder_length /
                        2, cylinder_center[1], cylinder_center[2]]
        super().__init__(material_name=material_name, density=density,
                         cylinder_start=cylinder_start, cylinder_end=cylinder_end,
                         cylinder_radius=cylinder_radius)

# -----------------------------------------------------------


class ZAlignedCylinder(CappedCylinder):
    '''Z Axis-Aligned cylinder of finite length'''

    def __init__(self, material_name, cylinder_center, cylinder_length,
                 cylinder_radius, density=None):
        '''Initialize material composition and location of the shield'''
        cylinder_start = [cylinder_center[0], cylinder_center[1],
                          cylinder_center[2]-cylinder_length/2]
        cylinder_end = [cylinder_center[0], cylinder_center[1],
                        cylinder_center[2]+cylinder_length/2]
        super().__init__(material_name=material_name, density=density,
                         cylinder_start=cylinder_start, cylinder_end=cylinder_end,
                         cylinder_radius=cylinder_radius)

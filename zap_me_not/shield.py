import abc
import math
import numbers

import numpy as np

from . import material, ray

import importlib
pyvista_spec = importlib.util.find_spec("pyvista")
pyvista_found = pyvista_spec is not None
if pyvista_found:
    import pyvista

# -----------------------------------------------------------


class Shield(abc.ABC):
    """Abtract class to model a photon shield.

    Parameters
    ----------
    material_name : :obj:`material.Material`, optional
        Shield material type
    density : float, optional
        Material density in g/cm3
    **kwargs
        Arbitrary keyword arguments.
    """
    '''
    Attributes
    ----------
    material : :class: `material.Material`
        Material properties of the shield
    '''

    def __init__(self, material_name=None, density=None, **kwargs):
        # the material name is validated by the Material class
        self.material = material.Material(material_name)
        if density is not None:
            if not isinstance(density, numbers.Number):
                raise ValueError("Invalid density: " + str(density))
            self.material.density = density
        super().__init__(**kwargs)

    @abc.abstractmethod
    def is_infinite(self):
        """Returns true if any dimension is infinite, false otherwise
        """

    @abc.abstractmethod
    def _get_crossing_length(self, a_ray):
        """Calculates the linear intersection length of a ray and the shield

        Parameters
        ----------
        a_ray : :class:`ray.FiniteLengthRay`
            The finite length ray that is checked for intersections
            with the shield.
        """
        if not isinstance(a_ray, ray.FiniteLengthRay):
            raise ValueError("Invalid ray object")

    @abc.abstractmethod
    def get_crossing_mfp(self, a_ray, photon_energy):
        """Calculates the mfp equivalent if a ray intersects the shield

        Parameters
        ----------
        a_ray : :class:`ray.FiniteLengthRay`
            The finite length ray that is checked for intersections
            with the shield.
        photon_energy : float
            The photon energy in MeV
        """
        if not isinstance(a_ray, ray.FiniteLengthRay):
            raise ValueError("Invalid ray object")
        if not isinstance(photon_energy, numbers.Number):
            raise ValueError("Invalid photon energy")

    @staticmethod
    def _line_plane_collision(plane_normal, plane_point, ray_origin,
                              ray_normal, epsilon=1e-6):
        """Calculates the distance from the ray origin to the intersection
           with a plane

        Parameters
        ----------
        plane_normal : :class:`numpy.ndarray`
            A vector normal to the plane
        plane_point : :class:`numpy.ndarray`
            Vector location of an arbitrary point on the plane
        ray_origin : :class:`numpy.ndarray`
            The vector location of the ray origin
        ray_normal : :class:`numpy.ndarray`
            The vector normal of the ray
        photon_energy : float
            The photon energy in MeV

        Notes
        -----
        This work is based on
        <https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-plane-and-ray-disk-intersection>
        """
        ndotu = plane_normal.dot(ray_normal)
        if abs(ndotu) < epsilon:
            return None
        w = plane_point - ray_origin
        t = w.dot(plane_normal)/ndotu
        return t

# -----------------------------------------------------------


class SemiInfiniteXSlab(Shield):
    """A semi-infinite slab shield perpendicular to the X axis.

    Parameters
    ----------
    material_name : :obj:`material.Material`
        Shield material type
    x_start : float
        X axis location of the inner edge of the shield.
    x_end : float
        X axis location of the outer edge of the shield.
    density : float, optional
        Material density in g/cm3.
    """
    '''
    Attributes
    ----------
    material : :class: `material.Material`
        Material properties of the shield
    x_start : float
        X axis location of the inner edge of the shield.
    x_end : float
        X axis location of the outer edge of the shield.
    '''

    def __init__(self, material_name, x_start, x_end, density=None):
        super().__init__(material_name=material_name, density=density)
        self.x_start = x_start
        self.x_end = x_end

    def is_infinite(self):
        """Returns true if any dimension is infinite, false otherwise
        """
        return True

    def _get_crossing_length(self, ray):
        """Calculates the linear intersection length of a ray and the shield

        Parameters
        ----------
        ray : :class:`ray.FiniteLengthRay`
            The finite length ray that is checked for intersections with
            the shield.
        """
        super()._get_crossing_length(ray)  # validate the arguments
        ray_origin = ray._origin
        ray_unit_vector = ray._dir
        plane_normal = np.array([1, 0, 0])
        # get length to one crossing point
        plane_point = np.array([self.x_start, 0, 0])
        first_length = self._line_plane_collision(
            plane_normal, plane_point, ray_origin, ray_unit_vector)
        if first_length is None:
            # ray is parallel to plane
            return 0
        # get length to second crossing point
        plane_point = np.array([self.x_end, 0, 0])
        second_length = self._line_plane_collision(
            plane_normal, plane_point, ray_origin, ray_unit_vector)
        if second_length is None:
            # ray is parallel to plane
            return 0
        if (first_length < 0 and second_length < 0):
            # ray starts and ends entirely on one side of the shield
            return 0
        if (first_length > ray._length and second_length > ray._length):
            # ray starts and ends entirely on one side of the shield
            return 0
        # remainder of cases have some sort of partial or full crossing
        t0 = min(first_length, second_length)
        t1 = max(first_length, second_length)
        if ((t0 < 0) and (t1 > ray._length)):
            # ray is intirely within the slab
            return ray._length
        if ((t0 < 0) and (t1 < ray._length)):
            # ray start in slab and crosses out
            return t1
        if ((t0 > 0) and (t1 > ray._length)):
            # ray starts outside slab and ends inside slab
            return ray._length - t0
        # we are left with a full crossing
        return t1 - t0

    def get_crossing_mfp(self, ray, photon_energy):
        """Calculates the mfp equivalent if a ray intersects the shield

        Parameters
        ----------
        ray : :class:`ray.FiniteLengthRay`
            The finite length ray that is checked for intersections with
            the shield.
        photon_energy : float
            The photon energy in MeV
        """
        # validate the arguments
        super().get_crossing_mfp(ray, photon_energy)
        distance = self._get_crossing_length(ray)
        return self.material.get_mfp(photon_energy, distance)

    def vtk(self):
        """Creates a display object

        Returns
        -------
        :class:`pyvista.PolyData`
            A box object representing the slab shield.
        """
        if pyvista_found:
            return pyvista.Box(bounds=(self.x_start, self.x_end, -1000, 1000,
                                       -1000, 1000))

    def _projection(self, x, y, z):
        # project a point onto the surface of the infinite shield
        # this is a semi-infinite slab, with a finite X width,
        # so return two x values at the specified y and z
        return [(self.x_start, y, z), (self.x_end, y, z)]
# -----------------------------------------------------------


# class Sphere(Shield):
#     def __init__(self, material_name, sphere_center, sphere_radius, density=None):
#         '''Initialize material composition and location of the slab shield'''
#         super().__init__(material_name=material_name, density=density)
#         self.center = np.array(sphere_center)
#         self.radius = np.array(sphere_radius)

#     def get_crossing_mfp(self, ray, photon_energy):
#         '''returns the crossing mfp'''
#         super().get_crossing_mfp(ray, photon_energy)    # validate the arguments
#         distance = self._get_crossing_length(ray)
#         return self.material.get_mfp(photon_energy, distance)

#     def _get_crossing_length(self, ray):
#         # based on
#         # http://viclw17.github.io/2018/07/16/raytracing-ray-sphere-intersection/
#         super()._get_crossing_length(ray)  # validate the arguments
#         a = np.dot(ray._dir, ray._dir)
#         b = 2 * np.dot(ray._dir, ray._origin - self.center)
#         c = np.dot(ray._origin-self.center, ray._origin -
#                    self.center) - self.radius**2
#         discriminant = b**2 - 4*a*c
#         if discriminant <= 0:
#             # sphere is missed or tangent
#             return 0
#         root = np.sqrt(discriminant)
#         t0 = (-b - root)/(2*a)
#         t1 = (-b + root)/(2*a)
#         big_list = []
#         for a_length in [t0, t1]:
#             if (a_length >= 0) and (a_length <= ray._length):
#                 big_list.append(a_length)
#         if len(big_list) != 2:
#             # if not 2 intersections, look for ray endpoints inside the sphere
#             if self.contains(ray._origin):
#                 big_list.append(0)
#             if self.contains(ray._end):
#                 big_list.append(ray._length)
#         if len(big_list) == 0:
#             # ray misses the sphere
#             return 0
#         if len(big_list) != 2:
#             # this shouldn't occur
#             raise ValueError("Shield doesn't have 2 crossings")
#         return abs(big_list[1]-big_list[0])

#     def contains(self, point):
#         ray = point - self.center
#         if np.dot(ray, ray) > self.radius**2:
#             return False
#         return True

# -----------------------------------------------------------


class Box(Shield):
    """A rectangular polyhedron shield.

    All sides of the box shield must be axis-aligned.

    Parameters
    ----------
    material_name : :obj:`material.Material`
        Shield material type
    box_center : :obj:`list`
        X, Y, and Z coordinates of the box center.
    box_dimensions : :obj:`list`
        X, Y, and Z dimensions of the box.
    density : float, optional
        Material density in g/cm3.
    """
    '''
    Attributes
    ----------
    material : :class:material.Material
        Material properties of the shield
    box_center : :class:numpy.ndarray
        Vector location of the center of the box in cartesian coordiantes.
    box_dimensions :  :class:numpy.ndarray
        Vector holding the dimensions of the box.
    '''

    def __init__(self, material_name, box_center, box_dimensions,
                 density=None):
        super().__init__(material_name=material_name, density=density)
        self.box_center = np.array(box_center)
        self.box_dimensions = np.array(box_dimensions)

    def is_infinite(self):
        """Returns true if any dimension is infinite, false otherwise
        """
        return False

    def get_crossing_mfp(self, ray, photon_energy):
        """Calculates the mfp equivalent if a ray intersects the shield

        Parameters
        ----------
        ray : :class:`ray.FiniteLengthRay`
            The finite length ray that is checked for intersections with
            the shield.
        photon_energy : float
            The photon energy in MeV
        """
        # validate the arguments
        super().get_crossing_mfp(ray, photon_energy)
        distance = self._get_crossing_length(ray)
        return self.material.get_mfp(photon_energy, distance)

    def _get_crossing_length(self, ray):
        """Calculates the linear intersection length of a ray and the shield

        Parameters
        ----------
        ray : :class:`ray.FiniteLengthRay`
            The finite length ray that is checked for intersections with
            the shield.
        """
        super()._get_crossing_length(ray)  # validate the arguments
        crossings = self._intersect_axis_aligned_box(ray)
        # two crossings indicates a full-shield crossing
        # one crossing indicates that either (common) the source is
        #    in the shield or (uncommon) the dose point is in the
        #    shield
        # zero crossings can indicate that either both source and
        #    dose points are in the shield or that the shield is
        #    missed entirely
        if len(crossings) != 2:
            # check for start/end of ray within the box
            if self._contains(ray._origin):
                crossings.insert(0, ray._origin)
            if self._contains(np.array(ray._end)):
                crossings.append(np.array(ray._end))
        if len(crossings) == 0:
            # likely it's a complete miss
            return 0
        if len(crossings) != 2:
            # shouldn't ever get here
            raise ValueError("Shield doesn't have 2 crossings")
        # let numpy do the heavy lifting
        return np.linalg.norm(crossings[0]-crossings[1])

    def _contains(self, point):
        """Determines if the shield contains a point

        Parameters
        ----------
        point : :obj:`list`
            The X, Y, and Z cartesian coordinates of a point.

        Returns
        -------
        boolean
            True if the box contains the point, false otherwise
        """
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

    def _intersect_axis_aligned_box(self, ray):
        """Calculates a list of point where a ray intersects the
           axis-aligned box

        Parameters
        ----------
        ray : :obj:`ray.Ray`
            A ray object that may intersect the box.

        Returns
        -------
        :obj:`list`
            List of vector locations of intersection points.  These will
            include the ray endpoints if they are located within the shield.
        """
        'returns 0, 1, or 2 points of intersection'
        results = []
        bounds = [self.box_center - (self.box_dimensions/2),
                  self.box_center + (self.box_dimensions/2)]
        tmin = (bounds[ray._sign[0]][0] - ray._origin[0]) * ray._invdir[0]
        tmax = (bounds[1-ray._sign[0]][0] - ray._origin[0]) * ray._invdir[0]
        tymin = (bounds[ray._sign[1]][1] - ray._origin[1]) * ray._invdir[1]
        tymax = (bounds[1-ray._sign[1]][1] - ray._origin[1]) * ray._invdir[1]

        if (tmin > tymax) or (tymin > tmax):
            return results

        if tymin > tmin:
            tmin = tymin
        if tymax < tmax:
            tmax = tymax

        tzmin = (bounds[ray._sign[2]][2] - ray._origin[2]) * ray._invdir[2]
        tzmax = (bounds[1-ray._sign[2]][2] - ray._origin[2]) * ray._invdir[2]

        if ((tmin > tzmax) or (tzmin > tmax)):
            return results

        if tzmin > tmin:
            tmin = tzmin

        if tzmax < tmax:
            tmax = tzmax

        if (tmin >= 0) and (tmin <= ray._length):
            results.append(ray._origin + ray._dir*tmin)
        if (tmax >= 0) and (tmax <= ray._length):
            results.append(ray._origin + ray._dir*tmax)

        return results

    def vtk(self):
        """Creates a display object

        Returns
        -------
        :class:`pyvista.PolyData`
            A box object representing the box shield.
        """
        if pyvista_found:
            xmin = self.box_center[0]-self.box_dimensions[0]/2
            xmax = self.box_center[0]+self.box_dimensions[0]/2
            ymin = self.box_center[1]-self.box_dimensions[1]/2
            ymax = self.box_center[1]+self.box_dimensions[1]/2
            zmin = self.box_center[2]-self.box_dimensions[2]/2
            zmax = self.box_center[2]+self.box_dimensions[2]/2
            return pyvista.Box(bounds=(xmin, xmax, ymin, ymax, zmin, zmax))

# -----------------------------------------------------------


class InfiniteAnnulus(Shield):
    """An annular shield of infinite length

    Parameters
    ----------
    material_name : :obj:`material.Material`
        Shield material type
    cylinder_origin : :obj:`list`
        X, Y, and Z coordinates of the point on the cylinder centerline.
    cylinder_axis : :obj:`list`
        X, Y, and Z vector components of the cylinder axis.
    cylinder_inner_radius : float
        Radius of the annulus inner surface.
    cylinder_outer_radius : float
        Radius of the annulus outer surface.
    density : float, optional
        Material density in g/cm3.
    """
    '''
    Attributes
    ----------
    material : :class: `material.Material`
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

    def __init__(self, material_name, cylinder_origin, cylinder_axis,
                 cylinder_inner_radius, cylinder_outer_radius, density=None):
        super().__init__(material_name=material_name, density=density)
        self.inner_radius = cylinder_inner_radius
        self.outer_radius = cylinder_outer_radius
        self.origin = np.array(cylinder_origin)
        axis = np.array(cylinder_axis)
        self.dir = axis/np.linalg.norm(axis)

    def is_infinite(self):
        """Returns true if any dimension is infinite, false otherwise
        """
        return True

    def get_crossing_mfp(self, ray, photon_energy):
        """Calculates the mfp equivalent if a ray intersects the shield

        Parameters
        ----------
        ray : :class:`ray.FiniteLengthRay`
            The finite length ray that is checked for intersections
            with the shield.
        photon_energy : float
            The photon energy in MeV
        """
        # validate the arguments
        super().get_crossing_mfp(ray, photon_energy)
        distance = self._get_crossing_length(ray)
        return self.material.get_mfp(photon_energy, distance)

    def _get_crossing_length(self, ray):
        """Calculates the linear intersection length of a ray and the shield

        Parameters
        ----------
        ray : :class:`ray.FiniteLengthRay`
            The finite length ray that is checked for intersections
            with the shield.
        """
        super()._get_crossing_length(ray)  # validate the arguments
        # get a list of crossing points
        crossings = self._intersect(ray)
        # zero crossings can indicate that either both source and
        #    dose points are in the shield or that the shield is
        #    missed entirely
        # one crossing indicates that either (common) the source is
        #    in the shield or (uncommon) the dose point is in the
        #    shield
        # two crossings indicates a single in/out or out/in crossing
        # four crossings indicate a full-shield crossing
        if len(crossings) not in [2, 4]:
            if self._contains(ray._origin):
                crossings.append(0)
            if self._contains(np.array(ray._end)):
                crossings.append(ray._length)
        if len(crossings) == 0:
            return 0
        if len(crossings) not in [2, 4]:
            raise ValueError("Shield doesn't have valid crossings")
        crossings.sort()
        if len(crossings) == 2:
            return crossings[1]-crossings[0]
        # let numpy do the heavy lifting
        return (crossings[1]-crossings[0]) + (crossings[3] - crossings[2])

    def _contains(self, point):
        """Determines if the shield contains a point

        Parameters
        ----------
        point : :obj:`list`
            The X, Y, and Z cartesian coordinates of a point.

        Returns
        -------
        boolean
            True if the shield contains the point, false otherwise
        """
        # determine scalar projection of point on cylinder centerline
        rando = np.dot(point-self.origin, self.dir)
        # check the radial distance from cylinder centerline
        parto = (self.origin+self.dir*rando) - point
        if (np.dot(parto, parto) < self.inner_radius**2) or \
                (np.dot(parto, parto) > self.outer_radius**2):
            return False
        return True

    def _intersect(self, ray):
        """Calculates a list of points where a ray intersects the shield

        Parameters
        ----------
        ray : :obj:`ray.Ray`
            A ray object that may intersect the box.

        Returns
        -------
        :obj:`list`
            List of distances along the ray, measured from the ray origin,
            where the ray intersects the annulus.  Will include the ray
            endpoints if they are within the annular shield.
        Notes
        -----
        This work is based on
        <https://mrl.nyu.edu/~dzorin/rend05/lecture2.pdf>
        and
        <https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-plane-and-ray-disk-intersection>
        """
        results = []
        for radius in [self.inner_radius, self.outer_radius]:
            deltap = ray._origin - self.origin
            part1 = ray._dir - (np.dot(ray._dir, self.dir)*self.dir)
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
                    if t >= 0 and t <= ray._length:
                        results.append(t)
        return results

    def vtk(self):
        """Creates a display object

        Returns
        -------
        :class:`pyvista.PolyData`
            A boolean object representing the annular cylinder shield.
        """
        if pyvista_found:
            # define an imaginary bottom of the shield at a distance
            # of -2000 from the origin
            bottom = self.dir*(-2000.)
            disc = pyvista.Disc(center=(bottom[0], bottom[1], bottom[2]),
                                inner=self.inner_radius,
                                outer=self.outer_radius, c_res=50)
            cyl1 = disc.extrude(self.dir*4000, capping=True)
            return cyl1

    def _projection(self, x, y, z):
        # TODO: generalize this by using a degenerate cylinder
        #
        # project a point onto the surface of the infinite shield
        # this is a unconstrained annulus.
        # Given the range of possible geometries, this
        # routine will return a single x,y,z tuple representing
        # the interesection of the annulus axis with the plane of
        # the point.  Three possible intersections with the x, y,
        # and z planes of the point.  The closest point will
        # be returned.  This should permit the annulus to be displayed
        # without overly extending the region displayed.
        normal = [1, 0, 0]
        plane_point = [x, y, z]
        t = self._line_plane_collision(normal, plane_point, self.origin,
                                       self.dir)
        point1 = self.origin + self.dir*t
        normal = [0, 1, 0]
        t = self._line_plane_collision(normal, plane_point, self.origin,
                                       self.dir)
        point2 = self.origin + self.dir*t
        normal = [0, 0, 1]
        t = self._line_plane_collision(normal, plane_point, self.origin,
                                       self.dir)
        point3 = self.origin + self.dir*t
        dist1 = abs(point1 - plane_point)
        dist2 = abs(point2 - plane_point)
        dist3 = abs(point3 - plane_point)
        return min(dist1, dist2, dist3)

# -----------------------------------------------------------


class YAlignedInfiniteAnnulus(InfiniteAnnulus):
    """An annular shield of infinite length aligned with the Y axis

    Parameters
    ----------
    material_name : :obj:`material.Material`
        Shield material type
    cylinder_center : :obj:`list`
        X, Y, and Z coordinates of the point on the cylinder centerline.
    cylinder_inner_radius : float
        Radius of the annulus inner surface.
    cylinder_outer_radius : float
        Radius of the annulus outer surface.
    density : float, optional
        Material density in g/cm3.
    """
    '''
    Attributes
    ----------
    material : :class: `material.Material`
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

    def __init__(self, material_name, cylinder_center, cylinder_inner_radius,
                 cylinder_outer_radius, density=None):
        super().__init__(material_name=material_name, density=density,
                         cylinder_origin=cylinder_center,
                         cylinder_inner_radius=cylinder_inner_radius,
                         cylinder_outer_radius=cylinder_outer_radius,
                         cylinder_axis=[0, 1, 0])

    def _projection(self, x, y, z):
        # project a point onto the surface of the infinite shield
        # this is a y-aligned annulus
        # so return four x,z values at the specified y
        centerX = self.cylinder_center[0]
        centerZ = self.cylinder_center[2]
        point1 = (centerX+self.cylinder_outer_radius,
                  y, centerZ)
        point2 = (centerX-self.cylinder_outer_radiusx,
                  y, centerZ)
        point3 = (centerX,
                  y, centerZ+self.cylinder_outer_radius)
        point4 = (centerX,
                  y, centerZ-self.cylinder_outer_radius)
        return [[point1, point2, point3, point4]]

# -----------------------------------------------------------


class XAlignedInfiniteAnnulus(InfiniteAnnulus):
    """An annular shield of infinite length aligned with the X axis

    Parameters
    ----------
    material_name : :obj:`material.Material`
        Shield material type
    cylinder_center : :obj:`list`
        X, Y, and Z coordinates of the point on the cylinder centerline.
    cylinder_inner_radius : float
        Radius of the annulus inner surface.
    cylinder_outer_radius : float
        Radius of the annulus outer surface.
    density : float, optional
        Material density in g/cm3.
    """
    '''
    Attributes
    ----------
    material : :class: `material.Material`
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
    def __init__(self, material_name, cylinder_center, cylinder_inner_radius,
                 cylinder_outer_radius, density=None):
        super().__init__(material_name=material_name, density=density,
                         cylinder_origin=cylinder_center,
                         cylinder_inner_radius=cylinder_inner_radius,
                         cylinder_outer_radius=cylinder_outer_radius,
                         cylinder_axis=[1, 0, 0])

    def _projection(self, x, y, z):
        # project a point onto the surface of the infinite shield
        # this is a x-aligned annulus
        # so return four y,z values at the specified x
        centerY = self.cylinder_center[1]
        centerZ = self.cylinder_center[2]
        point1 = (x,
                  centerY+self.cylinder_outer_radius, centerZ)
        point2 = (x,
                  centerY-self.cylinder_outer_radius, centerZ)
        point3 = (x,
                  centerY, centerZ+self.cylinder_outer_radius)
        point4 = (x,
                  centerY, centerZ-self.cylinder_outer_radius)
        return [[point1, point2, point3, point4]]

# -----------------------------------------------------------


class ZAlignedInfiniteAnnulus(InfiniteAnnulus):
    """An annular shield of infinite length aligned with the Z axis

    Parameters
    ----------
    material_name : :obj:`material.Material`
        Shield material type
    cylinder_center : :obj:`list`
        X, Y, and Z coordinates of the point on the cylinder centerline.
    cylinder_inner_radius : float
        Radius of the annulus inner surface.
    cylinder_outer_radius : float
        Radius of the annulus outer surface.
    density : float, optional
        Material density in g/cm3.
    """
    '''
    Attributes
    ----------
    material : :class: `material.Material`
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

    def __init__(self, material_name, cylinder_center, cylinder_inner_radius,
                 cylinder_outer_radius, density=None):
        super().__init__(material_name=material_name, density=density,
                         cylinder_origin=cylinder_center,
                         cylinder_inner_radius=cylinder_inner_radius,
                         cylinder_outer_radius=cylinder_outer_radius,
                         cylinder_axis=[0, 0, 1])

    def _projection(self, x, y, z):
        # project a point onto the surface of the infinite shield
        # this is a z-aligned annulus
        # so return four x,y values at the specified z
        centerX = self.cylinder_center[0]
        centerY = self.cylinder_center[1]
        point1 = (centerX+self.cylinder_outer_radius,
                  centerY, z)
        point2 = (centerX-self.cylinder_outer_radius,
                  centerY, z)
        point3 = (centerX,
                  centerY+self.cylinder_outer_radius, z)
        point4 = (centerX,
                  centerY-self.cylinder_outer_radius, z)
        return [[point1, point2, point3, point4]]

# -----------------------------------------------------------


class CappedCylinder(Shield):
    """A cylindrical shield of finite length

    Parameters
    ----------
    material_name : :obj:`material.Material`
        Shield material type
    cylinder_start : :obj:`list`
        X, Y, and Z coordinates of the center of one cylinder end.
    cylinder_end : :obj:`list`
        X, Y, and Z coordinates of the center of another cylinder end.
    cylinder_radius : float
        Radius of the cylinder.
    density : float, optional
        Material density in g/cm3.
    """
    '''
    Attributes
    ----------
    material : :class: `material.Material`
        Material properties of the shield
    radius : float
        Radius of the cylinder.
    origin : :class:`numpy.ndarray`
        Vector location corresponding to `cylinder_start`.
    end : :class:`numpy.ndarray`
        Vector location corresponding to `cylinder_end`.
    length : float
        Length of the cylinder.
    dir : :class:`numpy.ndarray`
        Vector normal of the cylinder centerline.
    '''

    def __init__(self, material_name, cylinder_start, cylinder_end,
                 cylinder_radius, density=None):
        super().__init__(material_name=material_name, density=density)
        self.radius = cylinder_radius
        self.origin = np.array(cylinder_start)
        self.end = np.array(cylinder_end)
        self.length = np.linalg.norm(self.end - self.origin)
        self.dir = (self.end - self.origin)/self.length

    def is_infinite(self):
        """Returns true if any dimension is infinite, false otherwise
        """
        return False

    def get_crossing_mfp(self, ray, photon_energy):
        """Calculates the mfp equivalent if a ray intersects the shield

        Parameters
        ----------
        ray : :class:`ray.FiniteLengthRay`
            The finite length ray that is checked for intersections
            with the shield.
        photon_energy : float
            The photon energy in MeV
        """
        # validate the arguments
        super().get_crossing_mfp(ray, photon_energy)
        distance = self._get_crossing_length(ray)
        return self.material.get_mfp(photon_energy, distance)

    def _get_crossing_length(self, ray):
        """Calculates the linear intersection length of a ray and the shield

        Parameters
        ----------
        ray : :class:`ray.FiniteLengthRay`
            The finite length ray that is checked for intersections
            with the shield.
        """
        super()._get_crossing_length(ray)  # validate the arguments
        # get a list of crossing points
        crossings = self._intersect(ray)
        # two crossings indicates a full-shield crossing
        # one crossing indicates that either (common) the source is
        #    in the shield or (uncommon) the dose point is in the
        #    shield
        # zero crossings can indicate that either both source and
        #    dose points are in the shield or that the shield is
        #    missed entirely
        if len(crossings) != 2:
            # check for start/end of ray within the cylinder
            if self._contains(ray._origin):
                crossings.insert(0, ray._origin)
            if self._contains(np.array(ray._end)):
                crossings.append(np.array(ray._end))
        if len(crossings) == 0:
            # likely it's a complete miss
            return 0
        if len(crossings) != 2:
            # shouldn't ever get here
            raise ValueError("Shield doesn't have 2 crossings")
        # let numpy do the heavy lifting
        return np.linalg.norm(crossings[0]-crossings[1])

    def _contains(self, point):
        """Determines if the shield contains a point

        Parameters
        ----------
        point : :obj:`list`
            The X, Y, and Z cartesian coordinates of a point.

        Returns
        -------
        boolean
            True if the shield contains the point, false otherwise
        """
        # determine scalar projection of point on cylinder centerline
        rando = np.dot(point-self.origin, self.dir)
        if rando < 0 or rando > self.length:
            return False
        # check the radial distance from cylinder centerline
        parto = (self.origin+self.dir*rando) - point
        if np.dot(parto, parto) > self.radius**2:
            return False
        return True

    def _intersect(self, ray):
        """Calculates a list of points where a ray intersects the shield

        Parameters
        ----------
        ray : :obj:`ray.Ray`
            A ray object that may intersect the box.

        Returns
        -------
        :obj:`list`
            List of points along the ray
            where the ray intersects the annulus.  Will include the ray
            endpoints if they are within the annular shield.
        Notes
        -----
        This work is based on
        <https://mrl.nyu.edu/~dzorin/rend05/lecture2.pdf>
        and
        <https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-plane-and-ray-disk-intersection>
        """
        results = []
        # test for
        deltap = ray._origin - self.origin
        part1 = ray._dir - (np.dot(ray._dir, self.dir)*self.dir)
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
                if t >= 0 and t <= ray._length:
                    intersection = ray._origin + ray._dir*t
                    loc = np.dot(intersection-self.origin, self.dir)
                    # keep only intersections within the finite length
                    # of the cylinder
                    if loc >= 0 and loc < self.length:
                        results.append(intersection)
        # check to see if there are intersections on the caps
        for disk_center in [self.origin, self.end]:
            t = self._line_plane_collision(
                self.dir, disk_center, ray._origin, ray._dir)
            if t is not None and t >= 0 and t <= ray._length:
                point = ray._origin + ray._dir*t
                radial = point - disk_center
                if radial.dot(radial) < self.radius**2:
                    results.append(point)
        return results

    def vtk(self):
        """Creates a display object

        Returns
        -------
        :class:`pyvista.PolyData`
            A cylinder object representing the capped cylinder shield.
        """
        if pyvista_found:
            center = (self.origin + self.end) / 2
            return pyvista.Cylinder(center=(center[0], center[1], center[2]),
                                    direction=self.dir, height=self.length,
                                    radius=self.radius)

# -----------------------------------------------------------


class YAlignedCylinder(CappedCylinder):
    """A cylindrical shield of finite length aligned with the Y axis

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
    '''
    Attributes
    ----------
    material : :class: `material.Material`
        Material properties of the shield
    radius : float
        Radius of the cylinder.
    origin : :class:`numpy.ndarray`
        Vector location corresponding to `cylinder_start`.
    end : :class:`numpy.ndarray`
        Vector location corresponding to `cylinder_end`.
    length : float
        Length of the cylinder.
    dir : :class:`numpy.ndarray`
        Vector normal of the cylinder centerline.
    '''

    def __init__(self, material_name, cylinder_center, cylinder_length,
                 cylinder_radius, density=None):
        cylinder_start = [cylinder_center[0],
                          cylinder_center[1]-cylinder_length/2,
                          cylinder_center[2]]
        cylinder_end = [cylinder_center[0], cylinder_center[1] +
                        cylinder_length/2, cylinder_center[2]]
        super().__init__(material_name=material_name, density=density,
                         cylinder_start=cylinder_start,
                         cylinder_end=cylinder_end,
                         cylinder_radius=cylinder_radius)

# -----------------------------------------------------------


class XAlignedCylinder(CappedCylinder):
    """A cylindrical shield of finite length aligned with the X axis

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
    '''
    Attributes
    ----------
    material : :class: `material.Material`
        Material properties of the shield
    radius : float
        Radius of the cylinder.
    origin : :class:`numpy.ndarray`
        Vector location corresponding to `cylinder_start`.
    end : :class:`numpy.ndarray`
        Vector location corresponding to `cylinder_end`.
    length : float
        Length of the cylinder.
    dir : :class:`numpy.ndarray`
        Vector normal of the cylinder centerline.
    '''

    def __init__(self, material_name, cylinder_center, cylinder_length,
                 cylinder_radius, density=None):
        cylinder_start = [cylinder_center[0]-cylinder_length / 2,
                          cylinder_center[1],
                          cylinder_center[2]]
        cylinder_end = [cylinder_center[0]+cylinder_length / 2,
                        cylinder_center[1],
                        cylinder_center[2]]
        super().__init__(material_name=material_name, density=density,
                         cylinder_start=cylinder_start,
                         cylinder_end=cylinder_end,
                         cylinder_radius=cylinder_radius)

# -----------------------------------------------------------


class ZAlignedCylinder(CappedCylinder):
    """A cylindrical shield of finite length aligned with the Z axis

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
    '''
    Attributes
    ----------
    material : :class: `material.Material`
        Material properties of the shield
    radius : float
        Radius of the cylinder.
    origin : :class:`numpy.ndarray`
        Vector location corresponding to `cylinder_start`.
    end : :class:`numpy.ndarray`
        Vector location corresponding to `cylinder_end`.
    length : float
        Length of the cylinder.
    dir : :class:`numpy.ndarray`
        Vector normal of the cylinder centerline.
    '''

    def __init__(self, material_name, cylinder_center, cylinder_length,
                 cylinder_radius, density=None):
        cylinder_start = [cylinder_center[0],
                          cylinder_center[1],
                          cylinder_center[2]-cylinder_length/2]
        cylinder_end = [cylinder_center[0],
                        cylinder_center[1],
                        cylinder_center[2]+cylinder_length/2]
        super().__init__(material_name=material_name, density=density,
                         cylinder_start=cylinder_start,
                         cylinder_end=cylinder_end,
                         cylinder_radius=cylinder_radius)

import abc
import math
import numbers
import copy
from typing import Optional, List, Tuple, Any

import numpy as np

from . import material, ray

import importlib
pyvista_spec = importlib.util.find_spec("pyvista")
pyvista_found = pyvista_spec is not None
if pyvista_found:
    import pyvista
''' '''
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


# -----------------------------------------------------------


class Shield(abc.ABC):
    """Abtract class to model a photon shield.
    """

    def __init__(self, material_name: Optional[str] = None,
                 density: Optional[float] = None) -> None:
        """Create a photon shield.

        Parameters
        ----------
        material_name
            Name of the material composing the shield.
        density
            Material density in g/cm3.
        """
        # the material name is validated by the Material class
        self.material: material.Material = material.Material(material_name)
        if density is not None:
            if not isinstance(density, numbers.Number):
                raise ValueError(f"Invalid density: {density}")
            self.material.density = density
        super().__init__()

    @abc.abstractmethod
    def is_hollow(self) -> bool:
        """Returns true if the body is annular or hollow, false otherwise
        """

    @abc.abstractmethod
    def _get_crossing_length(self, a_ray: ray.FiniteLengthRay) -> float:
        """Calculates the linear intersection length of a ray and the shield

        Parameters
        ----------
        a_ray
            The finite length ray that is checked for intersections
            with the shield.
        """
        if not isinstance(a_ray, ray.FiniteLengthRay):
            raise ValueError("Invalid ray object")
        return 0.0

    @abc.abstractmethod
    def get_crossing_mfp(self, a_ray: ray.FiniteLengthRay,
                         photon_energy: float) -> float:
        """Calculates the mfp equivalent if a ray intersects the shield

        Parameters
        ----------
        a_ray
            The finite length ray that is checked for intersections
            with the shield.
        photon_energy
            The photon energy in MeV
        """
        if not isinstance(a_ray, ray.FiniteLengthRay):
            raise ValueError("Invalid ray object")
        if not isinstance(photon_energy, numbers.Number):
            raise ValueError("Invalid photon energy")
        return 0.0

    @abc.abstractmethod
    def draw(self) -> pyvista.PolyData | None:
        """Creates a display object

        Returns
        -------
            A display object representing the shield.
        """
        pass

    @staticmethod
    def _line_plane_collision(plane_normal: np.ndarray,
                              plane_point: np.ndarray,
                              ray_origin: np.ndarray,
                              ray_normal: np.ndarray,
                              epsilon: float = 1e-6) -> Optional[float]:
        """Calculates the distance from the ray origin to the intersection
           with a plane

        Parameters
        ----------
        plane_normal
            A vector normal to the plane
        plane_point
            Vector location of an arbitrary point on the plane
        ray_origin
            The vector location of the ray origin
        ray_normal
            The vector normal of the ray
        photon_energy
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

    @staticmethod
    def _ray_sphere_intersection(ray: ray.FiniteLengthRay,
                                 sphere: "Sphere") -> float:
        # based on
        # https://viclw17.github.io/2018/07/16/raytracing-ray-sphere-intersection
        a = np.dot(ray._dir, ray._dir)
        b = 2 * np.dot(ray._dir, ray._origin - sphere.center)
        c = np.dot(ray._origin-sphere.center, ray._origin -
                   sphere.center) - sphere.radius**2
        discriminant = b**2 - 4*a*c
        if discriminant <= 0:
            # sphere is missed or tangent
            return 0
        root = np.sqrt(discriminant)
        t0 = (-b - root)/(2*a)
        t1 = (-b + root)/(2*a)
        big_list = []
        for a_length in [t0, t1]:
            if (a_length >= 0) and (a_length <= ray._length):
                big_list.append(a_length)
        if len(big_list) != 2:
            # if not 2 intersections, look for ray endpoints inside the sphere
            if sphere._contains(ray._origin):
                big_list.append(0)
            if sphere._contains(np.array(ray._end)):
                big_list.append(ray._length)
        if len(big_list) == 0:
            # ray misses the sphere
            return 0
        if len(big_list) != 2:
            # this shouldn't occur
            raise ValueError("Sphere doesn't have 2 crossings")
        return abs(big_list[1]-big_list[0])

# -----------------------------------------------------------


class SemiInfiniteShield(Shield):
    """Abtract class to model a photon shield.
    """
    @abc.abstractmethod
    def _projection(self, x: float, y: float,
                    z: float) -> List[Tuple[float, float, float]]:
        # project a point onto the surface of the infinite shield
        # this is a semi-infinite slab, with a finite X width,
        # so return two x values at the specified y and z
        pass


class SemiInfiniteXSlab(SemiInfiniteShield):
    """A semi-infinite slab shield perpendicular to the X axis.
    """

    def __init__(self, material_name: str, x_start: float, x_end: float,
                 density: Optional[float] = None) -> None:
        """Create a SemiInfiniteXSlab shield.

        Parameters
        ----------
        material_name
            Name of the material composing the shield.
        x_start
            X axis location of the inner edge of the shield.
        x_end
            X axis location of the outer edge of the shield.
        density
            Material density in g/cm3.
        """
        super().__init__(material_name=material_name, density=density)
        self.x_start: float = x_start
        self.x_end: float = x_end

    def is_hollow(self) -> bool:
        """Returns true if the body is annular or hollow, false otherwise
        """
        return False

    def _get_crossing_length(self, ray: ray.FiniteLengthRay) -> float:
        """Calculates the linear intersection length of a ray and the shield

        Parameters
        ----------
        a_ray
            The finite length ray that is checked for intersections
            with the shield.
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

    def get_crossing_mfp(self, ray: ray.FiniteLengthRay,
                         photon_energy: float) -> float:
        """Calculates the mfp equivalent if a ray intersects the shield

        Parameters
        ----------
        a_ray
            The finite length ray that is checked for intersections
            with the shield.
        photon_energy
            The photon energy in MeV
        """
        # validate the arguments
        super().get_crossing_mfp(ray, photon_energy)
        distance = self._get_crossing_length(ray)
        return self.material.get_mfp(photon_energy, distance)

    def draw(self) -> pyvista.PolyData | None:
        """Creates a display object

        Returns
        -------
            A display object representing the shield.
        """
        if pyvista_found:
            return pyvista.Box(bounds=(self.x_start, self.x_end, -1000, 1000,
                                       -1000, 1000))
        return None

    def _projection(self, x: float, y: float,
                    z: float) -> List[Tuple[float, float, float]]:
        # project a point onto the surface of the infinite shield
        # this is a semi-infinite slab, with a finite X width,
        # so return two x values at the specified y and z
        return [(self.x_start, y, z), (self.x_end, y, z)]
# -----------------------------------------------------------


class Sphere(Shield):
    """A spherical shield.
    """
    '''
    Attributes
    ----------
    material : :class: `material.Material`
        Material properties of the shield
    center : list
        list of floats (x, y, and z coordinates).
    radius : float
        radius of the sphere.
    '''
    def __init__(self, material_name: str, sphere_center: List[float],
                 sphere_radius: float,
                 density: Optional[float] = None) -> None:
        '''Create a spherical shield.

        Parameters
        ----------
        material_name
            Name of the material composing the shield.
        sphere_center
            Vector location of the center of the sphere in
            cartesian coordinates.
        sphere_radius
            Radius of the shield.
        density
            Material density in g/cm3.
        '''
        super().__init__(material_name=material_name, density=density)
        self.center: List[float] = sphere_center
        self.radius: float = sphere_radius

    def is_hollow(self) -> bool:
        """Returns true if the body is annular or hollow, false otherwise
        """
        return False

    def get_crossing_mfp(self, ray: ray.FiniteLengthRay,
                         photon_energy: float) -> float:
        """Calculates the mfp equivalent if a ray intersects the shield

        Parameters
        ----------
        ray
            The finite length ray that is checked for intersections with
            the shield.
        photon_energy
            The photon energy in MeV

        Returns
        -------
            Mean free path in centimeters.
        """
        super().get_crossing_mfp(ray, photon_energy)  # validate the arguments
        distance = self._get_crossing_length(ray)
        return self.material.get_mfp(photon_energy, distance)

    def _get_crossing_length(self, ray: ray.FiniteLengthRay) -> float:
        return self._ray_sphere_intersection(ray, self)

    def _contains(self, point: np.ndarray) -> bool:
        """Determines if the shield contains a point

        Parameters
        ----------
        point
            The X, Y, and Z cartesian coordinates of a point.

        Returns
        -------
            True if the box contains the point, false otherwise
        """
        ray = point - self.center
        if np.dot(ray, ray) > self.radius**2:
            return False
        return True

    def draw(self) -> pyvista.PolyData | None:
        """Creates a display object

        Returns
        -------
            A display object representing the shield.
        """
        if pyvista_found:
            return pyvista.Sphere(radius=float(self.radius),
                                  center=self.center)
        return None

# -----------------------------------------------------------


class Shell(Shield):
    """A shell that surrounds a spherical shield or source."""

    def __init__(self, material_name: str, sphere: Sphere, thickness: float,
                 density: Optional[float] = None) -> None:
        """Create a Shell shield.

        Parameters
        ----------
        material_name
            Name of the material composing the shield.
        sphere
            The spherical shield or source that defines the
            inner boundary of the shell.
        thickness
            The thickness of the shell.
        density
            Material density in g/cm3.
        """
        super().__init__(material_name=material_name, density=density)
        if thickness <= 0:
            raise ValueError("Shell has zero or negative thickness")
        if not isinstance(sphere, Sphere):
            raise ValueError("Shell must contain a spherical shield or source")

        self.inner_sphere: Sphere = copy.deepcopy(sphere)
        self.outer_sphere: Sphere = Sphere(material_name, sphere.center,
                                           sphere.radius + thickness,
                                           density)

    def is_hollow(self) -> bool:
        """Returns true if the body is annular or hollow, false otherwise
        """
        return True

    def get_crossing_mfp(self, ray: ray.FiniteLengthRay,
                         photon_energy: float) -> float:
        """Calculates the mfp equivalent if a ray intersects the shield

        Parameters
        ----------
        ray
            The finite length ray that is checked for intersections with
            the shield.
        photon_energy
            The photon energy in MeV

        Returns
        -------
            Mean free path in centimeters.
        """
        super().get_crossing_mfp(ray, photon_energy)  # validate the arguments
        distance = self._get_crossing_length(ray)
        return self.outer_sphere.material.get_mfp(photon_energy, distance)

    def _get_crossing_length(self, ray: ray.FiniteLengthRay) -> float:
        outer_surface_crossing = \
            self._ray_sphere_intersection(ray, self.outer_sphere)
        inner_surface_crossing = \
            self._ray_sphere_intersection(ray, self.inner_sphere)
        crossing_length = outer_surface_crossing - inner_surface_crossing
        if crossing_length < 0:
            crossing_length = 0
        return crossing_length

    def _contains(self, point: np.ndarray) -> bool:
        '''
        Returns true if the point is contained within the shell,
        otherwise false
        '''
        if self.outer_sphere._contains(point) and \
                not self.inner_sphere._contains(point):
            return True
        else:
            return False

    def draw(self) -> pyvista.PolyData | None:
        """Creates a display object

        Returns
        -------
            A display object representing the shield.
        """
        if pyvista_found:
            sphere_a = pyvista.Sphere(radius=float(self.outer_sphere.radius),
                                      center=self.outer_sphere.center)
            sphere_b = pyvista.Sphere(radius=float(self.inner_sphere.radius),
                                      center=self.inner_sphere.center)
            sphere_b.flip_faces(inplace=True)
            shell = sphere_a.merge(sphere_b)
            return shell
        return None
# -----------------------------------------------------------


class Box(Shield):
    """A rectangular polyhedron shield.
       All sides of the box shield must be axis-aligned.
    """

    def __init__(self, material_name: str, box_center: list[float],
                 box_dimensions: list[float],
                 density: Optional[float] = None) -> None:
        """Create a Box shield.

        Parameters
        ----------
        material_name
            Name of the material composing the shield.
        box_center
            Vector location of the center of the box in cartesian coordiantes.
        box_dimensions
            Vector holding the dimensions of the box.
        density
            Material density in g/cm3.
        """
        super().__init__(material_name=material_name, density=density)
        self.box_center: np.ndarray = np.array(box_center)
        self.box_dimensions: np.ndarray = np.array(box_dimensions)

    def is_hollow(self) -> bool:
        """Returns true if the body is annular or hollow, false otherwise
        """
        return False

    def get_crossing_mfp(self, ray: ray.FiniteLengthRay,
                         photon_energy: float) -> float:
        """Calculates the mfp equivalent if a ray intersects the shield

        Parameters
        ----------
        ray
            The finite length ray that is checked for intersections with
            the shield.
        photon_energy
            The photon energy in MeV

        Returns
        -------
            Mean free path in centimeters.
        """
        # validate the arguments
        super().get_crossing_mfp(ray, photon_energy)
        distance = self._get_crossing_length(ray)
        return self.material.get_mfp(photon_energy, distance)

    def draw(self) -> pyvista.PolyData | None:
        """Creates a display object

        Returns
        -------
            A display object representing the shield.
        """
        if pyvista_found:
            xmin = self.box_center[0]-self.box_dimensions[0]/2
            xmax = self.box_center[0]+self.box_dimensions[0]/2
            ymin = self.box_center[1]-self.box_dimensions[1]/2
            ymax = self.box_center[1]+self.box_dimensions[1]/2
            zmin = self.box_center[2]-self.box_dimensions[2]/2
            zmax = self.box_center[2]+self.box_dimensions[2]/2
            return pyvista.Box(bounds=(xmin, xmax, ymin, ymax, zmin, zmax))
        return None

    def _get_crossing_length(self, ray: ray.FiniteLengthRay) -> float:
        """Calculates the linear intersection length of a ray and the shield

        Parameters
        ----------
        ray
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
        return float(np.linalg.norm(crossings[0]-crossings[1]))

    def _contains(self, point: np.ndarray) -> bool:
        """Determines if the shield contains a point

        Parameters
        ----------
        point
            The X, Y, and Z cartesian coordinates of a point.

        Returns
        -------
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

    def _intersect_axis_aligned_box(self, ray: ray.FiniteLengthRay) \
            -> List[np.ndarray]:
        """Calculates a list of point where a ray intersects the
           axis-aligned box

        Parameters
        ----------
        ray
            A ray object that may intersect the box.

        Returns
        -------
            List of vector locations of intersection points.  These will
            include the ray endpoints if they are located within the shield.
        """
        'returns 0, 1, or 2 points of intersection'
        results: List[np.ndarray] = []
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

# -----------------------------------------------------------


class InfiniteAnnulus(SemiInfiniteShield):
    """An annular shield of infinite length
    """

    def __init__(self, material_name: str, cylinder_origin: list[float],
                 cylinder_axis: list[float],
                 cylinder_inner_radius: float,
                 cylinder_outer_radius: float,
                 density: Optional[float] = None) -> None:
        """Create an InfiniteAnnulus shield.

        Parameters
        ----------
        material_name
            Name of the material composing the shield.
        cylinder_origin
            X, Y, and Z coordinates of the point on the cylinder centerline.
        cylinder_axis
            X, Y, and Z vector components of the cylinder axis.
        cylinder_inner_radius
            Radius of the annulus inner surface.
        cylinder_outer_radius
            Radius of the annulus outer surface.
        density
            Material density in g/cm3.
        """
        super().__init__(material_name=material_name, density=density)
        self.inner_radius: float = cylinder_inner_radius
        self.outer_radius: float = cylinder_outer_radius
        self.origin: np.ndarray = np.array(cylinder_origin)
        axis = np.array(cylinder_axis)
        self.dir: np.ndarray = axis/np.linalg.norm(axis)

    def is_hollow(self) -> bool:
        """Returns true if the body is annular or hollow, false otherwise
        """
        return True

    def get_crossing_mfp(self, ray: ray.FiniteLengthRay,
                         photon_energy: float) -> float:
        """Calculates the mfp equivalent if a ray intersects the shield

        Parameters
        ----------
        ray
            The finite length ray that is checked for intersections with
            the shield.
        photon_energy
            The photon energy in MeV

        Returns
        -------
            Mean free path in centimeters.
        """
        # validate the arguments
        super().get_crossing_mfp(ray, photon_energy)
        distance = self._get_crossing_length(ray)
        return self.material.get_mfp(photon_energy, distance)

    def _get_crossing_length(self, ray: ray.FiniteLengthRay) -> float:
        """Calculates the linear intersection length of a ray and the shield

        Parameters
        ----------
        ray
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

    def _contains(self, point: np.ndarray) -> bool:
        """Determines if the shield contains a point

        Parameters
        ----------
        point
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

    def _intersect(self, ray: ray.FiniteLengthRay) -> List[float]:
        """Calculates a list of points where a ray intersects the shield

        Parameters
        ----------
        ray : :obj:`ray.Ray`
            A ray object that may intersect the box.

        Returns
        -------
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

    def draw(self) -> pyvista.PolyData | None:
        """Creates a display object

        Returns
        -------
            A display object representing the shield.
        """
        if pyvista_found:
            # define an imaginary bottom of the shield at a distance
            # of -2000 from the origin
            bottom = self.dir*(-2000.)
            disc = pyvista.Disc(center=(bottom[0], bottom[1], bottom[2]),
                                normal=self.dir,
                                inner=self.inner_radius,
                                outer=self.outer_radius, c_res=50)
            cyl1 = disc.extrude(self.dir*4000, capping=True)
            return cyl1
        return None

    def _projection(self, x: float, y: float, z: float) -> \
            List[Tuple[float, float, float]]:
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
        intersection_list = []
        t = self._line_plane_collision(np.array(normal),
                                       np.array(plane_point),
                                       self.origin,
                                       self.dir)
        if t is not None:
            intersection_list.append(self.origin + self.dir*t)
        normal = [0, 1, 0]
        t = self._line_plane_collision(np.array(normal),
                                       np.array(plane_point),
                                       self.origin,
                                       self.dir)
        if t is not None:
            intersection_list.append(self.origin + self.dir*t)
        normal = [0, 0, 1]
        t = self._line_plane_collision(np.array(normal),
                                       np.array(plane_point),
                                       self.origin,
                                       self.dir)
        if t is not None:
            intersection_list.append(self.origin + self.dir*t)
        min_collision_distance = None
        for intersection in intersection_list:
            distance = np.linalg.norm(intersection - plane_point)
            if min_collision_distance is None or \
               (distance < min_collision_distance):
                min_collision_distance = distance
                collision_point = intersection
        fakeElipsisRadius = 2 * self.outer_radius
        # generate a bounding box centered at "center" and
        # a width of 2*outer_radius
        box = [(collision_point - [fakeElipsisRadius, 0, 0]).astype(float),
               (collision_point + [fakeElipsisRadius, 0, 0]).astype(float),
               (collision_point - [0, fakeElipsisRadius, 0]).astype(float),
               (collision_point + [0, fakeElipsisRadius, 0]).astype(float),
               (collision_point - [0, 0, fakeElipsisRadius]).astype(float),
               (collision_point + [0, 0, fakeElipsisRadius]).astype(float)]
        tuple_list = \
            [tuple(sublist) for sublist in box]
        return tuple_list

# -----------------------------------------------------------


class YAlignedInfiniteAnnulus(InfiniteAnnulus):
    """An annular shield of infinite length aligned with the Y axis
    """

    def __init__(self, material_name: str, cylinder_center: list[float],
                 cylinder_inner_radius: float,
                 cylinder_outer_radius: float,
                 density: Optional[float] = None) -> None:
        """Create an YAlignedInfiniteAnnulus shield.

        Parameters
        ----------
        material_name
            Name of the material composing the shield.
        cylinder_center
            X, Y, and Z coordinates of the point on the cylinder centerline.
        cylinder_inner_radius
            Radius of the annulus inner surface.
        cylinder_outer_radius
            Radius of the annulus outer surface.
        density
            Material density in g/cm3.
        """
        super().__init__(material_name=material_name, density=density,
                         cylinder_origin=cylinder_center,
                         cylinder_inner_radius=cylinder_inner_radius,
                         cylinder_outer_radius=cylinder_outer_radius,
                         cylinder_axis=[0, 1, 0])

# -----------------------------------------------------------


class XAlignedInfiniteAnnulus(InfiniteAnnulus):
    """An annular shield of infinite length aligned with the X axis
    """
    def __init__(self, material_name: str, cylinder_center: list[float],
                 cylinder_inner_radius: float,
                 cylinder_outer_radius: float,
                 density: Optional[float] = None) -> None:
        """Create an XAlignedInfiniteAnnulus shield.

        Parameters
        ----------
        material_name
            Name of the material composing the shield.
        cylinder_center
            X, Y, and Z coordinates of the point on the cylinder centerline.
        cylinder_inner_radius
            Radius of the annulus inner surface.
        cylinder_outer_radius
            Radius of the annulus outer surface.
        density
            Material density in g/cm3.
        """
        super().__init__(material_name=material_name, density=density,
                         cylinder_origin=cylinder_center,
                         cylinder_inner_radius=cylinder_inner_radius,
                         cylinder_outer_radius=cylinder_outer_radius,
                         cylinder_axis=[1, 0, 0])

# -----------------------------------------------------------


class ZAlignedInfiniteAnnulus(InfiniteAnnulus):
    """An annular shield of infinite length aligned with the Z axis
    """

    def __init__(self, material_name: str, cylinder_center: list[float],
                 cylinder_inner_radius: float,
                 cylinder_outer_radius: float,
                 density: Optional[float] = None) -> None:
        """Create an ZAlignedInfiniteAnnulus shield.

        Parameters
        ----------
        material_name
            Name of the material composing the shield.
        cylinder_center
            X, Y, and Z coordinates of the point on the cylinder centerline.
        cylinder_inner_radius
            Radius of the annulus inner surface.
        cylinder_outer_radius
            Radius of the annulus outer surface.
        density
            Material density in g/cm3.
        """
        super().__init__(material_name=material_name, density=density,
                         cylinder_origin=cylinder_center,
                         cylinder_inner_radius=cylinder_inner_radius,
                         cylinder_outer_radius=cylinder_outer_radius,
                         cylinder_axis=[0, 0, 1])

# -----------------------------------------------------------


class CappedCylinder(Shield):
    """A cylindrical shield of finite length
    """

    def __init__(self, material_name: str, cylinder_start: list[float],
                 cylinder_end: list[float],
                 cylinder_radius: float,
                 density: Optional[float] = None) -> None:
        """Create an CappedCylinder shield.

        Parameters
        ----------
        material_name
            Name of the material composing the shield.
        cylinder_start
            X, Y, and Z coordinates of the center of one cylinder end.
        cylinder_end
            X, Y, and Z coordinates of the center of another cylinder end.
        cylinder_radius
            Radius of the cylinder.
        density
            Material density in g/cm3.
        """
        super().__init__(material_name=material_name, density=density)
        self.radius: float = cylinder_radius
        self.origin: np.ndarray = np.array(cylinder_start)
        self.end: np.ndarray = np.array(cylinder_end)
        self.length: float = float(np.linalg.norm(self.end - self.origin))
        self.dir: np.ndarray = (self.end - self.origin)/self.length

    def is_hollow(self) -> bool:
        """Returns true if the body is annular or hollow, false otherwise
        """
        return False

    def get_crossing_mfp(self, ray: ray.FiniteLengthRay,
                         photon_energy: float) -> float:
        """Calculates the mfp equivalent if a ray intersects the shield

        Parameters
        ----------
        ray
            The finite length ray that is checked for intersections with
            the shield.
        photon_energy
            The photon energy in MeV

        Returns
        -------
            Mean free path in centimeters.
        """
        # validate the arguments
        super().get_crossing_mfp(ray, photon_energy)
        distance = self._get_crossing_length(ray)
        return self.material.get_mfp(photon_energy, distance)

    def _get_crossing_length(self, ray: ray.FiniteLengthRay) -> float:
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
        return float(np.linalg.norm(crossings[0]-crossings[1]))

    def _contains(self, point: np.ndarray) -> bool:
        """Determines if the shield contains a point

        Parameters
        ----------
        point : :obj:`list`
            The X, Y, and Z cartesian coordinates of a point.

        Returns
        -------
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

    def _intersect(self, ray: ray.FiniteLengthRay) -> List[np.ndarray]:
        """Calculates a list of points where a ray intersects the shield

        Parameters
        ----------
        ray : :obj:`ray.Ray`
            A ray object that may intersect the box.

        Returns
        -------
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

    def draw(self) -> pyvista.PolyData | None:
        """Creates a display object

        Returns
        -------
            A display object representing the shield.
        """
        if pyvista_found:
            center = (self.origin + self.end) / 2
            return pyvista.Cylinder(center=(center[0], center[1], center[2]),
                                    direction=self.dir, height=self.length,
                                    radius=self.radius)
        return None

# -----------------------------------------------------------


class YAlignedCylinder(CappedCylinder):
    """A cylindrical shield of finite length aligned with the Y axis
    """

    def __init__(self, material_name: str, cylinder_center: list[float],
                 cylinder_length: float, cylinder_radius: float,
                 density: Optional[float] = None) -> None:
        """Create an YAlignedCylinder shield.

        Parameters
        ----------
        material_name
            Name of the material composing the shield.
        cylinder_center
            X, Y, and Z coordinates of the center of the cylinder.
        cylinder_length
            The length of the cylinder.
        cylinder_radius
            The radius of the cylinder.
        density
            Material density in g/cm3.
        """
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
    """

    def __init__(self, material_name: str, cylinder_center: list[float],
                 cylinder_length: float, cylinder_radius: float,
                 density: Optional[float] = None) -> None:
        """Create an XAlignedCylinder shield.

        Parameters
        ----------
        material_name
            Name of the material composing the shield.
        cylinder_center
            X, Y, and Z coordinates of the center of the cylinder.
        cylinder_length
            The length of the cylinder.
        cylinder_radius
            The radius of the cylinder.
        density
            Material density in g/cm3.
        """
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
    """

    def __init__(self, material_name: str,
                 cylinder_center: list[float],
                 cylinder_length: float, cylinder_radius: float,
                 density: Optional[float] = None) -> None:
        """Create an ZAlignedCylinder shield.

        Parameters
        ----------
        material_name
            Name of the material composing the shield.
        cylinder_center
            X, Y, and Z coordinates of the center of the cylinder.
        cylinder_length
            The length of the cylinder.
        cylinder_radius
            The radius of the cylinder.
        density
            Material density in g/cm3.
        """
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

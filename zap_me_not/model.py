import math
import numpy as np
import numbers
from . import ray, material, source, shield, detector

import importlib
pyvista_spec = importlib.util.find_spec("pyvista")
pyvista_found = pyvista_spec is not None
if pyvista_found:
    import pyvista


class Model:
    """Performs point-kernel shielding analysis.

    The Model class combines various shielding elements to perform
    the point-kernel photon shielding analysis.  These elements include
    sources, shields, and detectors.
    """
    '''
    Attributes
    ----------
    source : :class:`zap_me_not.source.Source`
        The source distribution (point, line, or volume) included in the model.

    shield_list : :class:`list` of :class:`zap_me_not.shield.Shield`
        A list of shields (including the source volume) contained in the model.

    detector : :class:`zap_me_not.detector.Detector`
        The single detector in the model used to determine the exposure.

    filler_material : :class:`zap_me_not.material.Material`
        The (optional) material used as fill around the formal shields.

    buildup_factor_material : :class:`zap_me_not.material.Material`
        The material used to calculate the exposure buildup factor.
    '''

    def __init__(self):
        self.source = None
        self.shield_list = []
        self.detector = None
        self.filler_material = None
        self.buildup_factor_material = None
        # used to calculate exposure (R/sec) from flux (photon/cm2 sec),
        # photon energy (MeV),
        # and linear energy absorption coeff (cm2/g)
        # aka, "flux to exposure conversion factor"
        # for more information, see "Radiation Shielding", J. K. Shultis
        #  and R.E. Faw, 2000, page 141.
        # This value is based on a value of energy deposition
        # per ion in air of 33.85 [ICRU Report 39, 1979].
        self._conversion_factor = 1.835E-8

    def set_filler_material(self, filler_material, density=None):
        r"""Set the filler material used by the model

        Parameters
        ----------
        filler_material : str
            The material to be used.
        density : float, optional
            The density of the material in g/cm\ :sup:`3`.
        """
        if not isinstance(filler_material, str):
            raise ValueError("Invalid filler material")
        self.filler_material = material.Material(filler_material)
        if density is not None:
            if not isinstance(density, numbers.Number):
                raise ValueError("Invalid density: " + str(density))
            self.filler_material.density = density

    def add_source(self, new_source):
        """Set the source used by the model.

        Parameters
        ----------
        new_source : :class:`zap_me_not.source.Source`
            The source to be used.
        """
        if not isinstance(new_source, source.Source):
            raise ValueError("Invalid source")

        self.source = new_source
        # don't forget that sources are shields too!
        self.shield_list.append(new_source)

    def add_shield(self, new_shield):
        """Add a shield to the collection of shields used by the model.

        Parameters
        ----------
        new_shield : :class:`zap_me_not.shield.Shield`
            The shield to be added.
        """
        if not isinstance(new_shield, shield.Shield):
            raise ValueError("Invalid shield")
        self.shield_list.append(new_shield)

    def add_detector(self, new_detector):
        """Set the detector used by the model.

        Parameters
        ----------
        new_detector : :class:`zap_me_not.detector.Detector`
            The detector to be used in the model.
        """
        if not isinstance(new_detector, detector.Detector):
            raise ValueError("Invalid detector")
        self.detector = new_detector

    def set_buildup_factor_material(self, new_material):
        """Set the material used to calculation exposure buildup factors.

        Parameters
        ----------
        new_material : :class:`zap_me_not.material.Material`
            The material to be used in buildup factor calculations.
        """
        if not isinstance(new_material, material.Material):
            raise ValueError("Invalid buildup factor material")
        self.buildup_factor_material = new_material

    def calculate_exposure(self):
        """Calculates the exposure at the detector location.

        Note:  Significant use of Numpy arrays to speed up evaluating the
        dose from each source point.  A "for loop" is used to loop
        through photon energies, but many of the iterations through
        all source points is performed using matrix math.

        Returns
        -------
        float
            The exposure in units of mR/hr.
        """
        results_by_photon_energy = self.generate_summary()
        if len(results_by_photon_energy) == 0:
            return 0  # may occur if source has no photons
        elif len(results_by_photon_energy) == 1:
            return results_by_photon_energy[0][4]  # mR/hr
        else:
            # sum exposure over all photons
            an_array = np.array(results_by_photon_energy)
            integral_results = np.sum(an_array[:, 4])
            return integral_results  # mR/hr

    def generate_summary(self):
        """Calculates the energy flux and exposure at the detector location.

        Note:  Significant use of Numpy arrays to speed up evaluating the
        dose from each source point.  A "for loop" is used to loop
        through photon energies, but many of the iterations through
        all source points is performed using matrix math.

        Returns
        -------
        :class:`list` of :class:`list`
            List, by photon energy, of photon energy, photon emmission rate,
            uncollided energy flux, uncollided exposure, and total exposure
        """
        # build an array of shield crossing lengths.
        # The first index is the source point.
        # The second index is the shield (including the source body).
        # The total transit distance in the "filler" material (if any)
        # is determined by subtracting the sum of the shield crossing
        # lengths from the total ray length.
        if self.source is None:
            raise ValueError("Model is missing a source")
        if self.detector is None:
            raise ValueError("Model is missing a detector")
        source_points = self.source._get_source_points()
        source_point_weights = self.source._get_source_point_weights()
        crossing_distances = np.zeros((len(source_points),
                                       len(self.shield_list)))
        total_distance = np.zeros((len(source_points)))
        for index, nextPoint in enumerate(source_points):
            vector = ray.FiniteLengthRay(nextPoint, self.detector.location)
            total_distance[index] = vector._length
            # check to see if source point and detector are coincident
            if total_distance[index] == 0.0:
                raise ValueError("detector and source are coincident")
            for index2, thisShield in enumerate(self.shield_list):
                crossing_distances[index, index2] = \
                    thisShield._get_crossing_length(vector)
        gaps = total_distance - np.sum(crossing_distances, axis=1)
        if np.amin(gaps) < 0:
                raise ValueError("Looks like shields and/or sources overlap")

        results_by_photon_energy = []
        # get a list of photons (energy & intensity) from the source
        spectrum = self.source.get_photon_source_list()

        air = material.Material('air')

        # iterate through the photon list
        for photon in spectrum:
            photon_energy = photon[0]
            # photon source strength
            photon_yield = photon[1]

            dose_coeff = air.get_mass_energy_abs_coeff(photon_energy)

            # determine the xsecs
            xsecs = np.zeros((len(self.shield_list)))
            for index, thisShield in enumerate(self.shield_list):
                xsecs[index] = thisShield.material.density * \
                    thisShield.material.get_mass_atten_coeff(photon_energy)
            # determine an array of mean free paths, one per source point
            total_mfp = crossing_distances * xsecs
            total_mfp = np.sum(total_mfp, axis=1)
            # add the gaps if required
            if self.filler_material is not None:
                gap_xsec = self.filler_material.density * \
                    self.filler_material.get_mass_atten_coeff(photon_energy)
                total_mfp = total_mfp + (gaps * gap_xsec)
            uncollided_flux_factor = np.exp(-total_mfp)
            if (self.buildup_factor_material is not None):
                buildup_factor = \
                    self.buildup_factor_material.get_buildup_factor(
                        photon_energy, total_mfp)
            else:
                buildup_factor = 1.0
            uncollided_point_energy_flux = photon_yield * \
                np.asarray(source_point_weights) \
                * uncollided_flux_factor * photon_energy * \
                (1/(4*math.pi*np.power(total_distance, 2)))
            total_uncollided_energy_flux = np.sum(uncollided_point_energy_flux)

            uncollided_point_exposure = uncollided_point_energy_flux * \
                self._conversion_factor * dose_coeff * 1000 * 3600  # mR/hr
            total_uncollided_exposure = np.sum(uncollided_point_exposure)

            collided_point_exposure = uncollided_point_exposure * \
                buildup_factor
            total_collided_exposure = np.sum(collided_point_exposure)

            results_by_photon_energy.append(
                [photon_energy, photon_yield, total_uncollided_energy_flux,
                 total_uncollided_exposure, total_collided_exposure])

        return results_by_photon_energy

    def display(self):
        """Produces a graphic display of the model.
        """
        if pyvista_found:
            # find the bounding box for all objects
            bounds = self._findBounds()
            pl = pyvista.Plotter()
            self._trimBlocks(pl, bounds)
            self._addPoints(pl, bounds)
            pl.show_bounds(grid='front', location='outer', all_edges=True)
            pl.add_legend(face=None, size=(0.1, 0.1))
            pl.show()

    def _trimBlocks(self, pl, bounds):
        shieldColor = 'blue'
        for thisShield in self.shield_list:
            if thisShield.is_infinite():
                clip1 = thisShield.vtk().clip_closed_surface(
                    normal='-z', origin=[0, 0, bounds[5]])
                clip2 = clip1.clip_closed_surface(
                    normal='z', origin=[0, 0, bounds[4]])
                clip3 = clip2.clip_closed_surface(
                    normal='-y', origin=[0, bounds[3], 0])
                clip4 = clip3.clip_closed_surface(
                    normal='y', origin=[0, bounds[2], 0])
                clip5 = clip4.clip_closed_surface(
                    normal='-x', origin=[bounds[1], 0, 0])
                clip6 = clip5.clip_closed_surface(
                    normal='x', origin=[bounds[0], 0, 0])
                pl.add_mesh(clip6, color=shieldColor)
            else:
                pl.add_mesh(thisShield.vtk(), color=shieldColor)

    def _findBounds(self):
        blocks = pyvista.MultiBlock()
        # add finite shields to the
        for thisShield in self.shield_list:
            if not thisShield.is_infinite():
                blocks.append(thisShield.vtk())
            else:
                # project the detector location onto the infinite surface
                # to get points to add to the geometry
                points = thisShield._projection(self.detector.x,
                                                self.detector.y,
                                                self.detector.z)
                for point in points:
                    blocks.append(pyvista.Line(point, point))
        # >>>aren't all sources also shields?  Then the next line is redundant
        # TODO: figure out if the next line is necessary
        # blocks.append(self.source.vtk())
        blocks.append(self.detector.vtk())
        # check for a zero width in any direction
        bounds = blocks.bounds
        x_width = abs(bounds[1] - bounds[0])
        y_width = abs(bounds[3] - bounds[2])
        z_width = abs(bounds[5] - bounds[4])
        max_width = max(x_width, y_width, z_width)
        min_width = max_width * 0.25
        if x_width < min_width:
            bounds[0] = bounds[0] - min_width/2
            bounds[1] = bounds[1] + min_width/2
        if y_width < min_width:
            bounds[2] = bounds[2] - min_width/2
            bounds[3] = bounds[3] + min_width/2
        if z_width < min_width:
            bounds[4] = bounds[4] - min_width/2
            bounds[5] = bounds[5] + min_width/2
        # increase the display bounds by a smidge to avoid
        #   inadvertent clipping
        bounds = [x * 1.01 for x in bounds]
        return bounds

    def _addPoints(self, pl, bounds):
        # the goal here is to add 'points' to the display, but they
        # must be represented as spheres to have some physical
        # volume to display.  Points will be displayed with a radius
        # of 5% of the smallest dimension of the bounding box.

        # A problem can occur if the bounding box has a width of 0 in one
        # or more of three dimensions.  An exception is thrown if bounds
        # in all three directions are of zero width.  Otherwise the zero
        # is ignored and the next largest dimension is used to size the
        # point representation.

        point_ratio = 0.05
        sourceColor = 'red'
        detectorColor = 'yellow'
        widths = [abs(bounds[1] - bounds[0]),
                  abs(bounds[3] - bounds[2]),
                  abs(bounds[5] - bounds[4])]
        good_widths = []
        for width in widths:
            if width > 0:
                good_widths.append(width)
        if len(good_widths) == 0:
            raise ValueError("detector and source are coincident")
        # determine a good radius for the points
        point_radius = min(good_widths) * point_ratio
        # check if the source is a point source
        if len(self.source._get_source_points()) == 1:
            body = pyvista.Sphere(center=(self.source._x,
                                          self.source._y,
                                          self.source._z),
                                  radius=point_radius)
            pl.add_mesh(
                body, line_width=5, color=sourceColor,
                label='source')
        body = pyvista.Sphere(center=(self.detector.x,
                                      self.detector.y,
                                      self.detector.z),
                              radius=point_radius)
        pl.add_mesh(
            body, line_width=5, color=detectorColor,
            label='detector')
        # pl.set_background(color='white')

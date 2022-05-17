import math
import pyvista

from . import ray, material

class Model:
    """Performs point-kernel shielding analysis.

    The Model class combines various shielding elements to perform
    the point-kernel photon shielding analysis.  These elements include
    sources, shields, and detectors.

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


    """
    def __init__(self):
        self.source = None
        self.shield_list = []
        self.detector = None
        self.filler_material = None
        self.buildup_factor_material = None
        # used to calculate exposure (R/sec) from flux (photon/cm2 sec), photon energy (MeV),
        # and linear energy absorption coeff (cm2/g)
        # aka, "flux to exposure conversion factor"
        # for more information, see "Radiation Shielding", J. K. Shultis and R.E. Faw, 2000
        # page 141.  This value is based on a value of energy deposition
        # per ion in air of 33.85 [ICRU Report 39, 1979].
        self._conversion_factor = 1.835E-8

    def set_filler_material(self, filler_material, density=None):
        """Set the filler material used by the model

        Parameters
        ----------
        filler_material : :class:`zap_me_not.material.Material`
            The material to be used.
        density : float, optional
            The density of the material in g/cm\ :sup:`3`.
        """
        self.filler_material = material.Material(filler_material)
        if density is not None:
            self.filler_material.density = density

    def add_source(self, new_source):
        """Set the source used by the model.

        Parameters
        ----------
        new_source : :class:`zap_me_not.source.Source`
            The source to be used.
        """
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
        self.shield_list.append(new_shield)

    def add_detector(self, new_detector):
        """Set the detector used by the model.

        Parameters
        ----------
        new_detector : :class:`zap_me_not.detector.Detector`
            The detector to be used in the model.
        """
        self.detector = new_detector

    def set_buildup_factor_material(self, new_material):
        """Set the material used to calculation exposure buildup factors.

        Parameters
        ----------
        new_material : :class:`zap_me_not.material.Material`
            The material to be used in buildup factor calculations.
        """
        self.buildup_factor_material = new_material

    def calculate_exposure(self):
        """Calculates the exposure at the detector location.

        Returns
        -------
        float
            The exposure in units of mR/hr.
        """

        # flux by photon energy
        flux_by_photon_energy = []
        # get a list of photons (energy/intensity per source point [gamma/sec])
        # from the source
        spectrum = self.source._get_photon_source_list()
        source_points = self.source._get_source_points()
        # iterate through the photons
        for photon in spectrum:
            uncollided_flux = 0
            total_flux = 0
            photon_energy = photon[0]  # eneregy of the current photon
            # photon source strength >>PER SOURCE POINT<<
            photon_yield = photon[1]
            # iterate through the source points
            for nextPoint in source_points:
                # determine the vector from source to detector
                vector = ray.FiniteLengthRay(nextPoint, self.detector.location)
                # vector = (nextPoint, self.detector.location)
                # iterate through the shield list
                total_mfp = 0.0
                shield_crossing_distance = 0.0
                if self.filler_material is not None:
                    for shield in self.shield_list:
                        distance = shield._get_crossing_length(vector)
                        shield_crossing_distance += distance
                    total_mfp += self.filler_material.get_mfp(
                        photon_energy, vector.length - shield_crossing_distance)
                for shield in self.shield_list:
                    mfp = shield.get_crossing_mfp(vector, photon_energy)
                    total_mfp += mfp
                total_flux_reduction_factor = math.exp(-total_mfp)
                if (self.buildup_factor_material is not None):
                    buildup_factor = \
                        self.buildup_factor_material.get_buildup_factor(photon_energy, total_mfp)
                else:
                    buildup_factor = 1.0
                uncollided_point_flux = photon_yield * \
                    total_flux_reduction_factor * (1/(4*math.pi*vector.length**2))
                total_point_flux = uncollided_point_flux*buildup_factor
                uncollided_flux += uncollided_point_flux
                total_flux += total_point_flux
            flux_by_photon_energy.append(
                [photon_energy, uncollided_flux, total_flux])

        air = material.Material('air')
        for photon in flux_by_photon_energy:
            photon.append(
                photon[2]*photon[0]*self._conversion_factor *
                air.get_mass_energy_abs_coeff(photon[0]))
        # sum exposure over all photons
        exposure_total = 0
        for photon in flux_by_photon_energy:
            exposure_total += photon[3]
        return exposure_total*1000*3600  # convert from R/sec to mR/hr

    def display(self):
        """Produces a graphic display of the model.
        """
        # basic test of pyvista plotter
        sourceColor = 'red'
        detectorColor = 'yellow'
        shieldColor = 'blue'
        # find the bounding box for all finite bodies
        blocks = pyvista.MultiBlock()
        for shield in self.shield_list:
            if not shield.is_infinite():
                blocks.append(shield.vtk())
        blocks.append(self.source.vtk())
        blocks.append(self.detector.vtk())
        pl = pyvista.Plotter()
        for shield in self.shield_list:
            pl.add_mesh(shield.vtk().clip_box(blocks.bounds,invert=False), color=shieldColor)
        # pl.add_axes(color='black', xlabel='X', labels_off=False)
        pl.add_mesh(self.source.vtk(),line_width=5,color=sourceColor,label='source')
        pl.add_mesh(self.detector.vtk(), line_width=5, color=detectorColor,label='detector')
        pl.set_background(color='white')
        pl.show_bounds(grid='front', location='outer',all_edges=True)
        # pl.add_legend(face=None,size=(0.1, 0.1))
        pl.show()


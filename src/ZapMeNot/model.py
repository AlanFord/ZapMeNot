from ZapMeNot import ray, material
import math


class Model:
    def __init__(self):
        self.source = None
        self.shieldList = []
        self.detector = None
        self.fillerMaterial = None
        self.buildupFactorMaterial = None
        # used to calculate exposure from flux, MeV,
        # and linear energy absorption coeff
        self.conversionFactor = 1.835E-8

    def set_filler_material(self, fillerMaterial, density=None):
        self.fillerMaterial = material.Material(fillerMaterial)
        if density is not None:
            self.fillerMaterial.set_density(density)

    def add_source(self, newSource):
        self.source = newSource
        # don't forget that sources are shields too!
        self.shieldList.append(newSource)

    def add_shield(self, newShield):
        self.shieldList.append(newShield)

    def add_detector(self, newDetector):
        self.detector = newDetector

    def set_buildup_factor_material(self, newMaterial):
        self.buildupFactorMaterial = newMaterial

    def calculate_exposure(self):
        # flux by photon energy
        fluxByPhotonEnergy = []
        # get a list of photons (energy/intensity per source point [gamma/sec])
        # from the source
        spectrum = self.source.get_photon_source_list()
        sourcePoints = self.source.get_source_points()
        # iterate through the photons
        for photon in spectrum:
            uncollidedFlux = 0
            totalFlux = 0
            photonEnergy = photon[0]  # eneregy of the current photon
            # photon source strength >>PER SOURCE POINT<<
            photonYield = photon[1]
            # iterate through the source points
            for nextPoint in sourcePoints:
                # determine the vector from source to detector
                vector = ray.FiniteLengthRay(nextPoint, self.detector.location)
                # vector = (nextPoint, self.detector.location)
                # iterate through the shield list
                totalMFP = 0.0
                shieldCrossingDistance = 0.0
                if self.fillerMaterial is not None:
                    for shield in self.shieldList:
                        distance = shield.get_crossing_length(vector)
                        shieldCrossingDistance += distance
                    totalMFP += self.fillerMaterial.get_mfp(
                        photonEnergy, vector.length - shieldCrossingDistance)
                for shield in self.shieldList:
                    mfp = shield.get_crossing_mfp(vector, photonEnergy)
                    totalMFP += mfp
                totalFluxReductionFactor = math.exp(-totalMFP)
                if (self.buildupFactorMaterial is not None):
                    buildupFactor = \
                        self.buildupFactorMaterial.get_buildup_factor(photonEnergy, totalMFP)
                else:
                    buildupFactor = 1.0
                uncollidedPointFlux = photonYield * \
                    totalFluxReductionFactor * (1/(4*math.pi*vector.length**2))
                totalPointFlux = uncollidedPointFlux*buildupFactor
                uncollidedFlux += uncollidedPointFlux
                totalFlux += totalPointFlux
            fluxByPhotonEnergy.append(
                [photonEnergy, uncollidedFlux, totalFlux])

        air = material.Material('air')
        for photon in fluxByPhotonEnergy:
            photon.append(
                photon[2]*photon[0]*self.conversionFactor *
                air.get_mass_energy_abs_coeff(photon[0]))
        # sum exposure over all photons
        exposureTotal = 0
        for photon in fluxByPhotonEnergy:
            exposureTotal += photon[3]
        return exposureTotal*1000*3600  # convert from R/sec to mR/hr

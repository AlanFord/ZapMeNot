import pytest

from zap_me_not import model, source, shield, detector

pytestmark = pytest.mark.graphics

# =============================================================


class TestDisplay():
    def test_PointSource_BoxShield(self):
        # test of model display and a point source and finite shield
        myModel = model.Model()
        mySource = source.PointSource(0, 0, 10)
        photonEnergy = 1.0  # MeV
        photonIntensity = 3E10  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(100, 0, 0))
        myModel.add_shield(shield.Box(
            "iron", box_center=[15, 0, 0], box_dimensions=[10, 30, 30]))
        myModel.display()

    def test_PointSource_SemiInfiniteXSlabShield(self):
        # test of model display and a point source and infinite shield
        myModel = model.Model()
        mySource = source.PointSource(0, 0, 10)
        photonEnergy = 1.0  # MeV
        photonIntensity = 3E10  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(100, 0, 0))
        myModel.add_shield(shield.SemiInfiniteXSlab(
            "iron", x_start=5, x_end=20,))
        myModel.display()

    def test_PointSource_MixedShield(self):
        # test of model display and a point source and multiple shields
        myModel = model.Model()
        mySource = source.PointSource(0, 0, 10)
        photonEnergy = 1.0  # MeV
        photonIntensity = 3E10  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(100, 0, 0))
        myModel.add_shield(shield.Box(
            "iron", box_center=[15, 0, 0], box_dimensions=[10, 30, 30]))
        myModel.add_shield(shield.CappedCylinder(
            "concrete", cylinder_start=[40, 0, -20], cylinder_end=[50, 0, 20],
            cylinder_radius=15))
        myModel.display()

    def test_PointSource_NoShield(self):
        # test of model display and a point source and no shield
        myModel = model.Model()
        mySource = source.PointSource(0, 0, 10)
        photonEnergy = 1.0  # MeV
        photonIntensity = 3E10  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(100, 0, 0))
        myModel.display()

    # a point source coincident with a detector
    def test_coincidentDetector(self):
        myModel = model.Model()
        mySource = source.PointSource(1, 2, 3)
        mySource.add_isotope_curies('Co-60', 3)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(1, 2, 3))
        with pytest.raises(ValueError):
            myModel.display()

    def test_CylinderSource_BoxShield(self):
        myModel = model.Model()
        mySource = source.XAlignedCylinderSource(
            cylinder_center=[0, 0, 0],
            cylinder_length=10, cylinder_radius=5, material_name='iron')
        photonEnergy = 1.0  # MeV
        photonIntensity = 3E10  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(100, 0, 0))
        myModel.add_shield(shield.Box(
            "iron", box_center=[15, 0, 0], box_dimensions=[10, 10, 10]))
        myModel.display()

    def test_PointSource_InfiniteAnnulusShield(self):
        myModel = model.Model()
        mySource = source.PointSource(0, 0, 0)
        photonEnergy = 1.0  # MeV
        photonIntensity = 3E10  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(100, 0, 0))
        myModel.add_shield(shield.InfiniteAnnulus(
            "iron", cylinder_origin=[50, 0, 0],
            cylinder_axis=[10, 10, 10],
            cylinder_inner_radius=15,
            cylinder_outer_radius=25))
        myModel.display()

    def test_BoxSource_InfiniteAnnulusShield(self):
        myModel = model.Model()
        mySource = source.BoxSource(material_name="iron",
                                    box_center=[100, 0, 0],
                                    box_dimensions=[30, 30, 30])
        photonEnergy = 1.0  # MeV
        photonIntensity = 3E10  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(0, 0, 0))
        myModel.add_shield(shield.InfiniteAnnulus(
            "iron", cylinder_origin=[50, 0, 0],
            cylinder_axis=[10, 10, 10],
            cylinder_inner_radius=15,
            cylinder_outer_radius=25))
        myModel.display()

    def test_XAlignedCylinderSource_CappedCylinderShield(self):
        myModel = model.Model()
        mySource = source.XAlignedCylinderSource(
            cylinder_center=[0, 0, 0],
            cylinder_length=10, cylinder_radius=5, material_name='iron')
        photonEnergy = 1.0  # MeV
        photonIntensity = 3E10  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(100, 0, 0))
        myModel.add_shield(shield.CappedCylinder(
            "iron", cylinder_start=[15, -10, 0], cylinder_end=[15, -15, 23],
            cylinder_radius=8))
        myModel.display()

    def test_XAlignedCylinderSource_YAlignedInfiniteAnnulusShield(self):
        myModel = model.Model()
        mySource = source.XAlignedCylinderSource(
            cylinder_center=[0, 0, 0],
            cylinder_length=10, cylinder_radius=5, material_name='iron')
        photonEnergy = 1.0  # MeV
        photonIntensity = 3E10  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(100, 0, 0))
        myModel.add_shield(shield.YAlignedInfiniteAnnulus(
            "iron", cylinder_center=[15, -10, 0], cylinder_inner_radius=15,
            cylinder_outer_radius=20))
        myModel.display()

    def test_XAlignedCylinderSource_XAlignedInfiniteAnnulusShield(self):
        myModel = model.Model()
        mySource = source.XAlignedCylinderSource(
            cylinder_center=[0, 0, 0],
            cylinder_length=10, cylinder_radius=5, material_name='iron')
        photonEnergy = 1.0  # MeV
        photonIntensity = 3E10  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(100, 0, 0))
        myModel.add_shield(shield.XAlignedInfiniteAnnulus(
            "iron", cylinder_center=[15, -10, 0], cylinder_inner_radius=15,
            cylinder_outer_radius=20))
        myModel.display()

    def test_XAlignedCylinderSource_ZAlignedInfiniteAnnulusShield(self):
        myModel = model.Model()
        mySource = source.XAlignedCylinderSource(
            cylinder_center=[0, 0, 0],
            cylinder_length=10, cylinder_radius=5, material_name='iron')
        photonEnergy = 1.0  # MeV
        photonIntensity = 3E10  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(100, 0, 0))
        myModel.add_shield(shield.ZAlignedInfiniteAnnulus(
            "iron", cylinder_center=[15, -10, 0], cylinder_inner_radius=15,
            cylinder_outer_radius=20))
        myModel.display()

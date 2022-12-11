import pytest

from zap_me_not import model, source, shield, detector

pytestmark = pytest.mark.graphics

# =============================================================
"""
class TestVTK():
    def test_Case0(self):
            # basic test of pyvista - plot a cylinder
            cylinder = pyvista.Cylinder(
                center=[1, 2, 3], direction=[1, 1, 1], radius=1, height=2)
            cylinder.plot(show_edges=False, line_width=5, cpos='xy')

    def test_Case1(self):
        # basic test of pyvista plotter
        cylinder = pyvista.Cylinder(
            center=[0, 0, 0], direction=[0, 0, 1], radius=1, height=2)
        pl = pyvista.Plotter()
        pl.add_axes(color='black', xlabel='X', labels_off=False)
        pl.add_mesh(cylinder,line_width=5)
        detector = pyvista.Sphere(center=(4.5, 4.5, 4.5), radius=0.1)
        pl.add_mesh(detector, line_width=5)
        pl.set_background(color='white')
        pl.show()

    def test_Case2(self):
        # test of boolean capabilities (will be used for annular bodies)
        cube = pyvista.Cube().triangulate().subdivide(3)
        sphere = pyvista.Sphere(radius=0.6)
        result = cube.boolean_difference(sphere)
        #result.plot(color='tan')
        pl = pyvista.Plotter()
        pl.add_mesh(result,line_width=5,color='tan',style='wireframe')
        pl.show()
"""


class TestModel():

    def test_PointSourceFiniteShield(self):
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

    def test_PointSourceInfiniteShield(self):
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

    def test_PointSourceMixedShield(self):
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

    def test_PointSourceNoShield(self):
        # test of model display and a point source and no shield
        myModel = model.Model()
        mySource = source.PointSource(0, 0, 10)
        photonEnergy = 1.0  # MeV
        photonIntensity = 3E10  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(100, 0, 0))
        myModel.display()


"""
    def test_CylinderSourceNoShield(self):
        myModel = model.Model()
        mySource = source.PointSource(0, 0, 0)
        photonEnergy = 1.0  # MeV
        photonIntensity = 3E10  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(100, 0, 0))
        myModel.add_shield(shield.Box(
            "iron", box_center=[15, 0, 0], box_dimensions=[10, 10, 10]))
        myModel.display()

    def test_CylinderSourceAnnularShield(self):
        myModel = model.Model()
        mySource = source.PointSource(0, 0, 0)
        photonEnergy = 1.0  # MeV
        photonIntensity = 3E10  # photons/sec
        mySource.add_photon(photonEnergy, photonIntensity)
        myModel.add_source(mySource)
        myModel.add_detector(detector.Detector(100, 0, 0))
        myModel.add_shield(shield.Box(
            "iron", box_center=[15, 0, 0], box_dimensions=[10, 10, 10]))
        myModel.display()
"""

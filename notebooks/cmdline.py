import sys
sys.path.insert(0,'/Users/alan/Desktop/github/ZapMeNot')
from zap_me_not import model, source, shield, detector, material

my_source = source.PointSource(0, 0, 0)
my_source.add_photon(0.4,3.0E+4)
tank_model = model.Model()
tank_model.add_source(my_source)
tank_model.add_detector(detector.Detector(10, 10, 10))
tank_model.calculate_exposure()

tank_model.display()

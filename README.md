# ZapMeNot
## A Python library for simple point-kernel photon shielding analyses.

This is very-much a work in progress - not ready for prime-time.

### Prerequisites (or at least what was used in development)
* Python 3.4 or above
* Pyyaml 5.3
* Numpy 1.18.1

### Using the Library

I envision the library will be used either with a GUI front-end of the user's choice or driven by a short Python
script such as the following:

```
sample_sink = PointKernelModel()
sample_sink.addSource(PointSource([('Co-60',2.1),('Cs-137',0.3)], x=0, y=0, z=0)
sample_sink.addDosePoint(x=200, y=40, z=40)
sample_sink.addShield(InfiniteXSlab('Concrete', xStart=12, xEnd=32.1)
sample_sink.addShield(nfiniteXSlab('Iron', xStart=32.1, xEnd=33.1)
exposure = sample_sink.calculateExposure()
```


### Testing

A command like the following will run a unit test module from the parent directory:

```
python -m unittest tests.test_material
```


To run all of the unit tests
```
python -m unittest discover
```



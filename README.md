# ZapMeNot
## A Python library for simple point-kernel photon shielding analyses.

This is very-much a work in progress - not ready for prime-time.

### Prerequisites (or at least what was used in development)
* Python 3.4 or above
* Numpy 1.18.1
* Pytest 5.3.5
* Pyyaml 5.3

### Using the Library

I envision the library will be used either with a GUI front-end of the user's choice or driven by a short Python
script such as the following:

```
sample_sink = Model()
sample_sink.addSource(PointSource([('Co-60',2.1),('Cs-137',0.3)], x=0, y=0, z=0)
sample_sink.addDosePoint(x=200, y=40, z=40)
sample_sink.addShield(InfiniteXSlab('Concrete', xStart=12, xEnd=32.1)
sample_sink.addShield(nfiniteXSlab('Iron', xStart=32.1, xEnd=33.1)
exposure = sample_sink.calculateExposure()
```


### Testing

To run all of the unit tests

```
pytest
```



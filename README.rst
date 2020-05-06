ZapMeNot
==============================================================================



A Python library for simple point-kernel photon shielding analyses.

Links
-----

 - The source: https://github.com/AlanFord/ZapMeNot

Requirements for installing:
------------------------------------------------------------------------------

 - Python 3.4 or above
 - Numpy 1.18.1 or above
 - SciPy 0.14 or above
 - Pytest 5.3.5 or above
 - Pyyaml 5.3 or above

Installation:
------------------------------------------------------------------------------

Installing from a local source tree:

`pip install ./ZapMeNot`

You can also install in Development Mode:

`pip install -e ./ZapMeNot`

Contributions:
------------------------------------------------------------------------------

Contributions are always welcome. Significant contributions
to this library were generously provided by Dominion Energy.

Quickstart
------------------------------------------------------------------------------

.. code-block:: python

    import zap_me_not
    
    sample_sink = Model()
    sample_sink.addSource(PointSource([('Co-60',2.1),('Cs-137',0.3)], x=0, y=0, z=0)
    sample_sink.addDosePoint(x=200, y=40, z=40)
    sample_sink.addShield(InfiniteXSlab('Concrete', xStart=12, xEnd=32.1)
    sample_sink.addShield(nfiniteXSlab('Iron', xStart=32.1, xEnd=33.1)
    exposure = sample_sink.calculateExposure()


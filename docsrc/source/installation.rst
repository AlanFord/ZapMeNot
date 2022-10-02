============
Installation
============


Installing from a local source tree:

:code:`pip install ./ZapMeNot`

You can also install in Development Mode:

:code:`pip install -e ./ZapMeNot`

You can also install from Github:

:code:`pip install git+git://github.com/AlanFord/ZapMeNot.git`

Installing in Anaconda is a bit more complicated. You must first manually install the prerequisites in conda::

    conda install pip
    conda install git
    conda install numpy
    conda install scipy
    conda install pytest
    conda install pyyaml
    pip install git+git://github.com/AlanFord/ZapMeNot.git

This may be simplified in the future as my knowledge of installation packages improves!

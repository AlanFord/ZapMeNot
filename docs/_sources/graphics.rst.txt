==================
We Want Pictures!
==================
Checking a model geometry can be challenging.  To make the process a little easier
the ZapMeNot library includes the ability to display an interactive view of
the geometry, include source, shields, and detector.  The `Pyvista`_ package is
required to support graphics.

.. _Pyvista: https://docs.pyvista.org

Graphics from a ZapMeNot Python Script
--------------------------------------

Once you have a model built and populated with a source, detector, and (optionally)
shields, the following command can be used to display the model:

.. code-block:: python

    # display a model
    myModel.display()

Provided you are using a an operating system with graphics capability (i.e. not just a console)
ZapMeNot will display something similar to the following graphic.  In this example the source
is a point source shown in red, the detector is shown in yellow, and two shields are shown
in blue.

.. image:: display.png

The display can be rotated, moved, zoomed, and more by using a mouse or `keyboard shortcuts`_.

.. _keyboard shortcuts: https://docs.pyvista.org/api/plotting/plotting.html

Graphics in a JupyterLab Notebook
--------------------------------------

A convenient way to document a ZapMeNot analysis is to use a `JupyterLab notebook`_.
Jupyterlab introduces just one additional wrinkle - optionally selecting a `graphics backend`_
for displaying graphics.  The `panel` backend tends to be compatible with the
ZapMeNot feature set.

.. _JupyterLab notebook: https://jupyter.org

.. _graphics backend: https://docs.pyvista.org/user-guide/jupyter/index.html

Here's a screenshot of a JupyterLab notebook.  Your display may look different, depending
on your workstation configuration.

.. image:: jupyterlab.png

Going Headless For Fun and Profit
---------------------------------

It is possible to display the model on a headless linux server (one with no graphics card)
by building your ZapMeNot model in a `JupyterLab notebook`_.  Beyond selecting a suitable
backend, it's also usually necessary to use `xvfb`_.  This requires a couple of steps, so follow along!

First, it's necessary to ensure that xvfb has been installed.  Here's the command for Ubuntu (your system may be different):

:code:`sudo apt install libgl1-mesa-glx xvfb`

Next, add the following lines after the other import statements at the beginning of your JupyterLab notebook:

.. code-block:: python

    from pyvista.utilities import xvfb
    xvfb.start_xvfb()
    pyvista.set_jupyter_backend('panel')


.. _xvfb: https://www.x.org/releases/X11R7.6/doc/man/man1/Xvfb.1.xhtml


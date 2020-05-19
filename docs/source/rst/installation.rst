Installation
############

This section explains 1) how the package can be installed, 2) how optional dependencies can add further functionality and 3) how a full installation with all optional dependencies can be performed.


1. Required
===========

The package is available on the `Python Package Index (PyPI) <https://pypi.org>`__ under the name `unified-plotting <https://pypi.org/project/unified-plotting>`__.

- It is compatible with `Python 3.6 to 3.8 <https://www.python.org/downloads>`_.
- It can be downloaded and installed with Python's default package manager `pip <https://pypi.org/project/pip>`__.
- You may also want to consider using an environment manager like `virtualenv <https://virtualenv.pypa.io>`__ or `conda <https://docs.conda.io>`__. Such tools allow to create a `virtual environment <https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments>`__ into which pip can install the package in an isolated fashion instead of globally on your system. Thereby it does not interfere with the installation of other projects, which may in an unlucky case require a different version of some shared dependency.

.. code-block:: console

   $ pip install unified-plotting


2. Optional
===========

The following are optional dependencies, i.e. they are not required to use the package but provide additional functionality you might also like to use.

Orca
----

The package contains the subpackage ``unified_plotting.plotly`` which uses `Plotly <https://plotly.com/python>`_ to generate figures. Plotly requires `Orca <https://github.com/plotly/orca>`__ to enable `static image export <https://plotly.com/python/static-image-export>`__. This means, if you use a function from ``unified_plotting.plotly`` to generate a figure, then the plot can only be exported as an image file when Orca is installed. For example, the method ``fig.export_svg(...)`` can export an SVG file when Orca is installed but will raise an error if Orca can not be found on your system.

`Recommended installation <https://github.com/plotly/orca#installation>`__ with package manager `conda <https://docs.conda.io>`__ from channel `plotly <https://anaconda.org/plotly/plotly-orca>`__:

.. code-block:: console

   $ conda install -y -c plotly plotly-orca



Jupyter notebook
----------------

The package provides support for displaying plots in `Jupyter notebooks <https://jupyter.org>`__. They provide a nice browser-based user interface for interactive development of Python code, which is very popular in data science and machine learning communities, partly because of their support for inline plots.

`Recommended installation <https://jupyter.org/install>`__ with package manager `conda <https://docs.conda.io>`__ from channel `conda-forge <https://anaconda.org/conda-forge/notebook>`__:

.. code-block:: console

   $ conda install -y -c conda-forge notebook

Caution: Some plots may not show up in the notebook with default settings. Instead a blank area is shown. The reason is a parameter called ``iopub_data_rate_limit`` in Jupyter's `config system <https://jupyter-notebook.readthedocs.io/en/stable/config.html>`__. Its value `is chosen rather low by default <https://github.com/jupyter/notebook/issues/2287>`__. Plots that contain much data can therefore be blocked. This problem can be solved by increasing the parameter, which can be done in two ways: 1) permanently change it with a config file in the directory ``~/.jupyter`` or 2) temporarily change it when opening a notebook by adding an optional argument to the start-up command:

.. code-block:: console

   $ jupyter notebook --NotebookApp.iopub_data_rate_limit=1.0e12



Graph libraries
---------------

This package supports the visualization of graph objects from several graph libraries in Python. If you want to use one of these, here is how you can install them:

- `graph-tool <https://graph-tool.skewed.de/>`__

  .. code-block:: console

     $ conda install -y -c conda-forge graph-tool

- `igraph <https://igraph.org/>`__

  .. code-block:: console

     $ conda install -y -c conda-forge igraph

- `NetworKit <https://networkit.github.io/>`__

  .. code-block:: console

     $ conda install -y -c conda-forge networkit

- `NetworkX <https://networkx.github.io/>`__

  .. code-block:: console

     $ conda install -y -c conda-forge networkx

- `Pyntacle <http://pyntacle.css-mendel.it/>`__

  .. code-block:: console

     $ conda install -y -c bfxcss -c conda-forge pyntacle

- `SNAP <http://snap.stanford.edu/>`__

  .. code-block:: console

     $ pip install snap-stanford



3. Full installation with all optional dependencies
===================================================

This guide was tested on Ubuntu 18.04 LTS. It may need minor modifications on other operating systems, e.g. installing missing system libraries with the system's package manager.

What happens? First a new `conda <https://docs.conda.io>`__ environment is created with Python 3.6 in it (needed only for Pyntacle, otherwise you can use ``python=3.8``). Then this environment is activated. Finally, the required and all optional dependencies are installed into the active environment.

.. code-block:: console

   # Create a new environment
   conda create -y --name myEnvForPlotting python=3.6
   
   # Activate it
   conda activate myEnvForPlotting
   
   # Install the package, including its required dependencies
   pip install unified-plotting
   
   # Install optional dependencies
   conda install -y -c bfxcss -c conda-forge pyntacle
   conda install -y -c plotly plotly-orca
   conda install -y -c conda-forge graph-tool igraph networkit networkx notebook
   pip install snap-stanford

Unified Plotting
################

Welcome! You've found the documentation of the Python 3 package `unified-plotting <https://pypi.org/project/unified_plotting>`__.

`TL;DR <https://en.wiktionary.org/wiki/tl;dr>`__ - Let's start right away with a small code example:

.. code-block:: python

   import networkx as nx
   import unified_plotting as up
   
   fig = up.matplotlib.scatter(x=[1, 2, 3, 4, 5, 6], y=[1, 1, 2, 3, 5, 8], show_line=True)
   fig.export_png('fibonacci.png')
   
   fig = up.plotly.scatter_3d(x=[1, 2, 1, 2], y=[2, 4, 4, 2], z=[2, 3, 5, 8], show_interpolation_rbf=True)
   fig.export_html('interpolation.html')
   
   fig = up.javascript.network_d3(nx.les_miserables_graph())
   fig.export_html('les_miserables.html')


.. raw:: html

   <p style="margin-bottom:0.5ex;">
     Output:
   </p>
   <p style="margin-left:1em;margin-bottom:1em">
     <a class="reference download internal" href="_static/media/fibonacci.png"><code class="xref download docutils literal notranslate"><span class="pre">fibonacci.png</span></code></a>
     &larr; static scatter plot
     <br>
     <a class="reference download internal" href="_static/media/interpolation.html"><code class="xref download docutils literal notranslate"><span class="pre">interpolation.html</span></code></a>
     &larr; interactive 3D scatter plot
     <br>
     <a class="reference download internal" href="_static/media/les_miserables.html"><code class="xref download docutils literal notranslate"><span class="pre">les_miserables.html</span></code></a>
     &larr; interactive network visualization
   </p>

Alternatives to such file output: 1) Displaying in browser 2) Embedding in notebook 3) Text representation


What is this package?
=====================

`unified-plotting <https://pypi.org/project/unified_plotting>`__ is an open-source software package for quick and easy plotting in Python 3. It provides a simple, unified interface to access Matplotlib, Plotly, d3.js and other data visualization libraries. The main goal is to reduce the complexity of generating various plots of two common types of data:

1. **Tabular data** (a.k.a. **vector data**, **array data**)
  
  - Meaning: Some lists with same length, which could be arranged as a table with numbers or strings as entries.
  - Examples
  
    - Quickstart: `Plotting vector data <code/examples/quickstart/vector_data.ipynb>`_
    - Archetypical: `Machine learning datasets <code/examples/gallery/computer_science/machine_learning_datasets.ipynb>`_
    - Libraries: `Plots with Matplotlib <code/examples/plot_overview/matplotlib.ipynb>`_, `Plots with Plotly <code/examples/plot_overview/plotly.ipynb>`_, `Plots with JavaScript <code/examples/plot_overview/javascript.ipynb>`_
    - Many more in the :doc:`examples <rst/examples/index>` section
  
2. **Linked data** (a.k.a. **graph data**, **network data**)
  
  - Meaning: Some objects and relationships between them, thought of as nodes connected by edges.
  - Examples 
  
    - Quickstart: `Plotting graph data <code/examples/quickstart/graph_data.ipynb>`_
    - Archetypical: `Les misérables graph <code/examples/plot_overview/javascript.ipynb#Dataset-3:-Graph-as-NetworkX-object>`_ with node images
    - Real-world: `Neighboring country graph <code/examples/gallery/social_science/neighboring_country_graph.ipynb>`_ with variable node sizes
    - Many more in the :doc:`examples <rst/examples/index>` section

More about :doc:`What ...? <rst/questions/what>`


Why is it relevant?
===================

Creating plots is a frequent but often tedious task, which can be greatly simplified to become less cumbersome and time consuming. Existing plotting libraries for Python are rich in capabilities and options, yet all this flexibility makes their usage more complicated. The effect is that it introduces a cognitive overhead that can limit their actual application in practical settings. By lowering the complexity of creating common plot types, data may get visualized more often and in a greater diversity of representations, potentially leading to better insights and decisions.

More about :doc:`Why ...? <rst/questions/why>`


When should it be used?
=======================

Whenever you deal with vector data (e.g. when using `Pandas <https://pandas.pydata.org>`__, `NumPy <https://numpy.org>`__, `scikit-learn <https://scikit-learn.org>`__, `DSV files <https://en.wikipedia.org/wiki/Delimiter-separated_values>`__) or graph data (e.g. when using `NetworkX <https://networkx.github.io>`__, `igraph <https://igraph.org>`__, `graph-tool <https://graph-tool.skewed.de>`__) this package enables you to quickly translate it into static and interactive visual representations (e.g. for `exploratory data analysis <https://en.wikipedia.org/wiki/Exploratory_data_analysis>`__ or `visual analytics <https://en.wikipedia.org/wiki/Visual_analytics>`__).


Who may benefit from it?
========================

This package may help anybody who wants to quickly generate decent looking plots with Python 3, without having to memorize or repeatedly look up API details of different plotting packages. It may also help in cases where precision is needed, such as exact plot, margin, font, marker and line sizes specified in a desired size unit such as inch, mm or pt (1 inch = 25.4 mm = 72 pt), which behind the scenes needs quite some trickery for certain libraries.

More about :doc:`Who ...? <rst/questions/who>`


How can you get started?
========================

- The :doc:`installation guide <rst/installation>` explains how to download and install the package.

- The :doc:`quickstart examples <rst/examples/quickstart>` provide a first impression of the package. The code can also be used as a check whether your local installation works.

- The :doc:`plot overview examples <rst/examples/plot_overview>` give a tour of all plotting functions provided by this package. They can be used to see the range of available features and may serve as copy-and-paste templates.

- The :doc:`configuration overview examples <rst/examples/config_overview>` explain the configuration system, which allows to define global plotting options and reusable styles that can be shared with others.

- The :doc:`graphical user interface demo <rst/gui>` introduces the browser-based GUI that is part of this package. It enables the input of data and generation of all plot types without writing a line of code.

- The :doc:`format specification <rst/format_specifications>` defines special purpose data formats used by this library. Currently this is restricted to the JSON graph format (JGF) for defining linked data, i.e. graphs with properties.

- The :doc:`API documentation <rst/api/index>` is the single source of truth for all details about each plotting function available in this package.


Where is everything located?
============================

The :doc:`package reference page <rst/package_references>` contains links to all parts of this project, which includes source code (tests, docs, examples), packaged code for distribution and documentation.


Table of website contents
=========================

.. toctree::
   :maxdepth: 1

   rst/package_references
   rst/installation
   rst/examples/index
   rst/gui
   rst/format_specifications
   rst/api/index

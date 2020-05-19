:orphan:

What ...?
#########

What is the aim of this package?
================================

The general aim is to minimize the gap between the idea of a plot in a human mind and its expression in code for a machine. In practice this requires simplification and unification of the user interfaces provided by different plotting libraries. There is also an additional desire to preserve as much freedom of expression as possible. Together these two conflicting aims are attempted to be solved by providing 1) an API consisting mainly of simple function calls and 2) a lot of optional arguments for styling almost any visual element if needed. A consistent naming scheme across plot types and libraries adds to achieving both goals.


What features does it provide?
==============================

This package delivers a unified, high-level API that allows you to easily access several data visualization libraries by simple function calls. More than 20 different plot types are currently supported. All functions come with a range of optional arguments to fine-tune the plot style if desired. 

Once a plot is created, it may be used for different purposes. To reflect this idea, the result of a function call is always a figure object which comes with methods that have unified names and arguments. They allow to 1) display the plot as static or interactive visualization, 2) export it in various file formats and 3) represent it in web-servable text formats such as SVG or HTML. For a quick example, see `using figure objects <code/examples/quickstart/figure_object.ipynb>`_.

For further convenience, there is a central configuration system to globally define styles that act on each plot and can be exported and imported for later reuse and sharing. More information can be found in the :doc:`configuration overview examples <../../rst/examples/config_overview>`.


What tasks does it solve?
=========================

The basic task solved by this package is to quickly transform data into many different plots in Python 3 with as little code and cognitive overhead as possible. It can be used interactively in a `Python shell <https://docs.python.org/3/tutorial/interpreter.html#interactive-mode>`__ (with plot display in a browser) or `Jupyter notebook <https://jupyter.org>`__ (with plot display inline in the notebook), or non-interactively in Python scripts, modules or packages (with file exports). Therefore it can be of value in different settings, ranging from quick interactive data exploration to incorporating plotting features into other codebases without polluting them with verbose low-level constructs.


What types of output can be generated?
======================================

The input of tabular data (e.g. collection of lists, DataFrame, CSV file) or linked data (e.g. dict in JSON graph format, graph object) can first be translated into a figure object and then either be displayed (browser, Jupyter Notebook) or exported as static images (raster formats like PNG and JPG, vector formats like SVG) and dynamic web documents (HTML/CSS/JavaScript).


What exactly is it built upon?
==============================

Each plot in this package relies on a third party visualization library and eases the access to it or sometimes extends it by novel features (most notably in graph visualization with JavaScript libraries):

- Python 3 libraries
    - `Matplotlib <https://matplotlib.org>`__
    - `Plotly <https://plot.ly>`__ (uses d3.js)
- JavaScript libraries -- used in Python 3, generating HTML output viewed offline in a browser
    - `d3.js <https://d3js.org>`__ 
    - `vis.js <https://visjs.org>`__
    - `3d-force-graph <https://github.com/vasturiano/3d-force-graph>`__ (uses d3.js)
    - `SlickGrid <https://slickgrid.net>`__
    - `parcoords-es <https://github.com/BigFatDog/parcoords-es>`__ (uses d3.js)

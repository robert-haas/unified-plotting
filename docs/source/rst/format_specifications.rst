Format specifications
=====================

.. _jgf-format:

JSON Graph Format (JGF)
-----------------------

This format is used to specify the input for all **network visualizations** in this package.

`JGF <https://github.com/jsongraph/json-graph-specification>`__ is a `JSON-based data format <https://en.wikipedia.org/wiki/JSON>`__ for representing either a **single graph** or a collection of **multiple graphs**. It was designed to be easily extensible by defining metadata with domain-specific meaning. Accordingly, this package uses the JGF format as basis and defines freely chosen metadata properties on top of it. The plotting functions of this package recognize these metadata properties and their values can be set by the user in order to control the appearance of different visual elements (e.g. background color, node sizes or edge opacities).


I) Basis: JGF
~~~~~~~~~~~~~

The main part of this data format is specified on the `JGF website <https://github.com/jsongraph/json-graph-specification>`__. The same information is provided here in a slightly rearranged manner with additional comments. JGF distinguishes four types of objects, each coming with some pre-defined properties:

1. **graphs object**: a ``JSON array`` of multiple **graph objects**

2. **graph object**: a ``JSON object`` that represents a single graph and which contains following properties

  - **label** (optional): a ``JSON string`` to name the graph
  - **directed** (optional, default ``JSON false``): ``JSON false`` if the graph is undirected, ``JSON true`` if the graph is directed
  - **type** (optional, currently ignored): a ``JSON string`` to classify the graph
  - **metadata** (optional): a ``JSON object`` to provide custom data for a graph. See **graph metadata** below for a list of properties that are defined for this package and recognized by it.
  - **nodes** (required): a ``JSON array`` of **node objects**
  - **edges** (required): a ``JSON array`` of **edge objects**

3. **node object**: represents a single node within a graph

  - **id** (required): a ``JSON string`` that needs to be unique among all node ids within a graph object.

    .. note::
       This package detects if a node has an id that is already used by another node (which comes earlier in the node list). Such a **node is ignored** as if it were not part of the given data.
  - **label** (optional): a ``JSON string`` to name the node
  - **metadata** (optional): a ``JSON object`` to provide custom data for a node. See **node metadata** below for a list of properties that are defined for this package and recognized by it.

4. **edge object**: represents a single edge within a graph between two of its nodes

  - **source** (required): a ``JSON string`` that needs to be a node id within the graph object.
  - **target** (required): a ``JSON string`` that needs to be a node id within the graph object.

    .. note::
       This package detects if an edge has a source or target that is not a node id. Such an **edge is ignored** as if it were not part of the given data.
  - **relation** (optional, currently ignored): a ``JSON string`` that describes the interaction between source and target node
  - **directed** (optional, currently ignored): ``JSON false`` for an undirected edge, ``JSON true`` for a directed edge (currently ignored by this package)
  - **label** (optional): a ``JSON string`` to name the edge
  - **metadata** (optional): a ``JSON object`` to provide custom data for an edge. See **edge metadata** below for a list of properties that are defined for this package and recognized by it.


Example for defining a single graph in Python

.. code-block:: Python

  data = {
    "graph": {
      "label": "Hello, graph!",
      "directed": True,
      "nodes": [
        {"id": "1", "label": "Hello, node!"},
        {"id": "2"},
        {"id": "3"}
      ],
      "edges": [
        {"source": "1", "target": "2"},
        {"source": "2", "target": "3", "label": "Hello, edge!"}
      ]
    }
  }


Example for defining multiple graphs in Python

.. code-block:: Python

  data = {
    "graphs": [
      {
        "label": "First graph",
        "nodes": [
          {"id": "a"},
          {"id": "b"},
          {"id": "c"},
          {"id": "d"}
        ],
        "edges": [
          {"source": "a", "target": "b"},
          {"source": "b", "target": "c"},
          {"source": "b", "target": "d"}
        ]
      },
      {
        "label": "Second graph",
        "nodes": [
          {"id": "1"},
          {"id": "2"}
        ],
        "edges": [
          {"source": "1", "target": "2"}
        ]
      },
      {
        "label": "Third graph",
        "nodes": [
          {"id": "uno"}
        ]
      }
    ]
  }


II) Extension: Metadata properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following metadata properties can optionally be provided with the graph data in order to modify the appearance of the graph, its nodes and its edges when visualized with this package. For maximum flexibility, all of these properties are defined as ``JSON string`` type and internally converted to appropriate formats during data parsing (e.g. ``node_size`` is a quantitative property and therefore converted to a floating-point number). Passing numerical properties as numerical values will also work.

1. **graph metadata**

  - **arrow_color**
  - **arrow_size**
  - **background_color**
  - **node_color**
  - **node_opacity**
  - **node_size**
  - **node_shape**
  - **node_border_color**
  - **node_border_size**
  - **node_label_color**
  - **node_label_size**
  - **node_hover**: Plain or HTML text displayed on hovering over any node
  - **node_click**: Plain or HTML text displayed on clicking any node
  - **node_image**: URL or data URL refering to an image that shall be displayed inside every node
  - **node_x**: x coordinate to fix every node at, can be released in the UI
  - **node_y**: y coordinate to fix every node at, can be released in the UI
  - **node_z**: z coordinate to fix every node at, can be released in the UI (ignored in 2D plots, only active in 3D)
  - **edge_color**
  - **edge_opacity**
  - **edge_size**
  - **edge_label_color**
  - **edge_label_size**
  - **edge_hover**: Plain or HTML text displayed on hovering over any edge
  - **edge_click**: Plain or HTML text displayed on clicking any edge

2. **node metadata**

  - **color**
  - **opacity**
  - **size**
  - **shape**
  - **border_color**
  - **border_size**
  - **label_color**
  - **label_size**
  - **hover**: Plain or HTML text displayed on hovering over this node
  - **click**: Plain or HTML text displayed on clicking this node
  - **image**: URL or data URL refering to an image that shall be displayed inside this node
  - **x**: x coordinate to fix this node at, can be released in the UI
  - **y**: y coordinate to fix this node at, can be released in the UI
  - **z**: z coordinate to fix this node at, can be released in the UI (ignored in 2D plots, only active in 3D)

3. **edge metadata**

  - **color**
  - **opacity**
  - **size**
  - **label_color**
  - **label_size**
  - **hover**: Plain or HTML text displayed on hovering over this edge
  - **click**: Plain or HTML text displayed on clicking this edge


Example for defining a single graph with metadata in Python

.. code-block:: Python

  data = {
    "graph": {
      "label": "Hello, graph!",
      "directed": True,
      "metadata": {
        "background_color": "#e9f5f5",
        "node_size": "15",
        "node_shape": "rectangle",
        "node_hover": "You hovered over a node!",
        "node_click": "You clicked on a node!",
        "edge_color": "orange",
        "edge_size": "4",
        "edge_hover": "You hovered over an edge!",
        "edge_click": "You clicked on an edge!",
      },
      "nodes": [
        {
          "id": "Anton",
          "label": "Hello node",
          "metadata": {"size": "20", "color": "red", "shape": "hexagon"}
        },
        {
          "id": "Berta",
          "metadata": {"shape": "circle", "color": "green"}
        },
        {
          "id": "Charlotte",
          "metadata": {"size": "25", "color": "blue", "opacity": "0.3"}
        },
        {
          "id": "Dora",
        },
      ],
      "edges": [
        {
          "source": "Anton",
          "target": "Berta",
          "metadata": {"size": "3", "color": "magenta", "opacity": "0.3"}
        },
        {
          "source": "Berta",
          "target": "Charlotte",
        },
        {
          "source": "Dora",
          "target": "Charlotte",
        },
        {
          "source": "Anton",
          "target": "Dora",
        }
      ]
    }
  }

.. _supported-graph-libraries:

Auto-conversion of external graph objects to JGF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This package supports six popular Python graph libraries which are listed below.
More specifically, the plotting functions of this package accept the different
graph objects of of these libraries directly as input.
Internally the plotting functions first convert the graph objects
into JGF and then proceed as if JGF data was provided by the user.
The responsible conversion functions are located in the
:py:mod:`unified_plotting.utilities.format_conversion` module and
can also be accessed by the user, e.g. to inspect the resulting
JGF object and check whether everything is converted as expected.

- `graph-tool <https://graph-tool.skewed.de/>`__

  - Conversion: :py:mod:`unified_plotting.utilities.format_conversion.graphtool_to_jgf`

- `igraph <https://igraph.org/>`__

  - Conversion: :py:mod:`unified_plotting.utilities.format_conversion.igraph_to_jgf`

- `NetworKit <https://networkit.github.io/>`__

  - Conversion: :py:mod:`unified_plotting.utilities.format_conversion.networkit_to_jgf`

- `NetworkX <https://networkx.github.io/>`__

  - Conversion: :py:mod:`unified_plotting.utilities.format_conversion.networkx_to_jgf`

- `Pyntacle <http://pyntacle.css-mendel.it/>`__

  - Conversion: :py:mod:`unified_plotting.utilities.format_conversion.pyntacle_to_jgf`

- `SNAP <http://snap.stanford.edu/>`__

  - Conversion: :py:mod:`unified_plotting.utilities.format_conversion.snap_to_jgf`

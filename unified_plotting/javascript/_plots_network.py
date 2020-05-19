"""JavaScript plots for graph data."""

from .._unified_arguments import shared_preprocessing as _shared_preprocessing
from . import _data_structures, _template_system


def network_d3(data,
               network_height=450, details_height=100,
               show_details=False, show_details_toggle_button=True,
               show_menu=True, show_menu_toggle_button=True,
               show_node=True, node_size_factor=1.0,
               node_size_data_source='size', use_node_size_normalization=False,
               node_size_normalization_min=5.0, node_size_normalization_max=75.0,
               node_drag_fix=False, node_hover_neighborhood=False, node_hover_tooltip=True,
               show_node_image=True, node_image_size_factor=1.0,
               show_node_label=True, show_node_label_border=True, node_label_data_source='id',
               node_label_size_factor=1.0, node_label_rotation=0.0, node_label_font='Arial',
               show_edge=True, edge_size_factor=1.0,
               edge_size_data_source='size', use_edge_size_normalization=False,
               edge_size_normalization_min=0.2, edge_size_normalization_max=5.0,
               edge_curvature=0.3, edge_hover_tooltip=True,
               show_edge_label=False, show_edge_label_border=True, edge_label_data_source='id',
               edge_label_size_factor=1.0, edge_label_rotation=0.0, edge_label_font='Arial',
               zoom_factor=0.75, large_network_threshold=500,
               layout_algorithm_active=True,
               use_many_body_force=True, many_body_force_strength=-70.0,
               many_body_force_theta=0.9,
               use_many_body_force_min_distance=False, many_body_force_min_distance=10.0,
               use_many_body_force_max_distance=False, many_body_force_max_distance=1000.0,
               use_links_force=True, links_force_distance=50.0, links_force_strength=0.5,
               use_collision_force=False, collision_force_radius=25.0,
               collision_force_strength=0.7,
               use_x_positioning_force=False, x_positioning_force_strength=0.2,
               use_y_positioning_force=False, y_positioning_force_strength=0.2,
               use_centering_force=True):
    """Create an interactive network plot from JSON graph format (JGF) data with d3.v5.js.

    Parameters
    ----------
    data : str, dict or graph object
        Graph data in :ref:`JSON graph format (JGF) <jgf-format>` as JSON string (*str*),
        JSON object (*dict*),
        :ref:`graph object of a supported graph library <supported-graph-libraries>`,
        or a list of multiple graphs, each defined in any of the previous ways.
        If the provided data contains multiple graphs, only the first one is shown on load,
        while the other ones can be chosen in the data selection menu in order to be displayed.
    network_height : int
        Height of the network container in pixels (px).
    details_height : int
        Height of the details container in pixels (px).
    show_details : bool
        If True, the details container is shown on load, otherwise hidden.
    show_details_toggle_button : bool
        If True, a button is shown that allows to toggle the visibility of the details container.
    show_menu : bool
        If True, the menu container is shown on load, otherwise hidden.
    show_menu_toggle_button : bool
        If True, a button is shown that allows to toggle the visibility of the menu container.
    show_node : bool
        If True, nodes are shown on load, otherwise hidden.
    node_size_factor : float
        A scaling factor that modifies node size.
    node_size_data_source : str
        Name of the numerical node property that is used as source for node size on load.
    use_node_size_normalization : bool
        If True, node sizes are normalized to lie in an interval between a
        chosen min and max value.
    node_size_normalization_min : float
        Minimum value for node size if node size normalization is active.
    node_size_normalization_max : float
        Maximum value for node size if node size normalization is active.
    node_drag_fix : bool
        If True, the position of a node becomes fixed after dragging it, i.e. the
        layout algorithm does not change its position but the user can drag it again.
    node_hover_neighborhood : bool
        If True, hovering a node leads to highlighting its neighborhood which consists of
        all incident edges and adjacent nodes.
    node_hover_tooltip : bool
        If True, hovering a node leads to popping up a tooltip if the hover property in the
        metadata of this node contains a non-empty string or HTML text.
    show_node_image : bool
        If True, node images are shown on load for all nodes whose image property in the metadata
        contains a valid image URL from which an image can be fetched.
    node_image_size_factor : float
        A scaling factor that modifies node image size.
    show_node_label : bool
        If True, node labels are shown on load, otherwise hidden.
    show_node_label_border : bool
        If True, node labels have a small border in the color of the background to better
        separate the text from other visual elements like edges or nodes.
    node_label_data_source : str
        Name of the node property that is used as source for node label text on load.
    node_label_size_factor : float
        A scaling factor that modifies node label size.
    node_label_rotation : float
        An angle that modifies node label orientation.
    node_label_font : str
        Name of the font that is used for node labels.
    show_edge : bool
        If True, edges are shown on load, otherwise hidden.
    edge_size_factor : float
        A scaling factor that modifies edge size (=edge width).
    edge_size_data_source : str
        Name of the edge property that is used as source for edge size on load.
    use_edge_size_normalization : bool
        If True, edge sizes are normalized to lie in an interval between a
        chosen min and max value.
    edge_size_normalization_min : float
        Minimum value for edge size if node size normalization is active.
    edge_size_normalization_max : float
        Maximum value for edge size if node size normalization is active.
    edge_curvature : float
        A factor that modifies edge curvature, where 0.0 means straight lines.
    edge_hover_tooltip : bool
        If True, hovering an edge leads to popping up a tooltip if the hover property in the
        metadata of this edge contains a non-empty string or HTML text.
    show_edge_label : bool
        If True, edge labels are shown on load, otherwise hidden.
    show_edge_label_border : bool
        If True, edge labels have a small border in the color of the background to better
        separate the text from other visual elements like edges or nodes.
    edge_label_data_source : str
        Name of the edge property that is used as source for edge label text on load.
    edge_label_size_factor : float
        A scaling factor that modifies edge label size.
    edge_label_rotation : float
        An angle that modifies edge label orientation.
    edge_label_font : str
        Name of the font that is used for edge labels.
    zoom_factor : float
        Factor that modifies how close the camera is to the drawing area on load.
    large_network_threshold : int
        Number that determines from when on a network is considered to be large, which
        means that before visualizing it an initial layout is calculated without moving anything.
    layout_algorithm_active : bool
        If True, the layout algorithm is active on load and leads to movement, otherwise inactive.
    use_many_body_force : bool
        If True, many body force is active in the layout algorithm.
        This force acts between any pair of nodes but can be restricted to only act on nodes
        within a certain distance.
    many_body_force_strength : float
        Number that determines the strength of the force. It can be positive to cause attraction
        or negative (usual case) to cause repulsion between nodes.
    many_body_force_theta : float
        Number that determines the accuracy of the Barnes–Hut approximation of the
        many-body simulation where nodes are grouped instead of treated individually
        to improve performance.
    use_many_body_force_min_distance : bool
        If True, a minimum distance between nodes is used in the many-body force calculation.
        This effectively leads to an upper bound on the strength of the force between any two
        nodes and avoids instability.
    many_body_force_min_distance : float
        Number that determines the minimum distance between nodes over which the many-body force
        is active.
    use_many_body_force_max_distance : bool
        If True, a maximum distance between nodes is used in the many-body force calculation.
        This can improve performance but results in a more localized layout.
    many_body_force_max_distance : float
        Number that determines the maximum distance between nodes over which the many-body force
        is active.
    use_links_force : bool
        If True, link force is active in the layout algorithm.
        This force acts between pairs of nodes that are connected by an edge. It pushes them
        together or apart in order to come close to a certain distance between connected nodes.
    links_force_distance : float
        Number that determines the preferred distance between connected nodes.
    links_force_strength : float
        Number that determines the strength of the links force.
    use_collision_force : bool
        If True, collision force is active in the layout algorithm.
        This force treats nodes as circles instead of points and acts on pairs of nodes that
        overlap in order to push them apart.
    collision_force_radius : float
        Number that determines the radius of the circle around each node.
    collision_force_strength : float
        Number that determines the strength of the force.
    use_x_positioning_force : bool
        If True, x-positioning force is active in the layout algorithm.
        This force modifies the x position of each node towards 0.0, effectively pushing them
        towards the y-axis.
    x_positioning_force_strength : float
        Number that indicates the strength of the force.
    use_y_positioning_force : bool
        This force modifies the y position of each node towards 0.0, effectively pushing them
        towards the x-axis.
    y_positioning_force_strength : float
        Number that indicates the strength of the force.
    use_centering_force : bool
        This force attracts each node towards the center of the coordinate system at (0, 0)
        to keep the graph in the display area. It may lead to unexpected repulsion effects
        if all nodes are fixed and then a single one is released by dragging it.

    Returns
    -------
    A :ref:`Figure <js-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://d3js.org
    - https://github.com/d3/d3-force

    """
    # Argument processing
    data = _shared_preprocessing.prepare_graph_data(data)

    # Transformation
    site_template = _template_system.load('templates/network_d3.html')
    insert_data = {
        'DEFINE_D3': _template_system.load('third_party/d3/d3.v5.min.def.js'),

        'DATA': _template_system.to_json(data),
        'NETWORK_HEIGHT': _template_system.to_json(network_height),
        'DETAILS_HEIGHT': _template_system.to_json(details_height),
        'SHOW_DETAILS': _template_system.to_json(show_details),
        'SHOW_DETAILS_TOGGLE_BUTTON': _template_system.to_json(show_details_toggle_button),
        'SHOW_MENU': _template_system.to_json(show_menu),
        'SHOW_MENU_TOGGLE_BUTTON': _template_system.to_json(show_menu_toggle_button),

        'SHOW_NODE': _template_system.to_json(show_node),
        'NODE_SIZE_FACTOR': _template_system.to_json(node_size_factor),
        'NODE_SIZE_DATA_SOURCE': _template_system.to_json(node_size_data_source),
        'USE_NODE_SIZE_NORMALIZATION': _template_system.to_json(use_node_size_normalization),
        'NODE_SIZE_NORMALIZATION_MIN': _template_system.to_json(node_size_normalization_min),
        'NODE_SIZE_NORMALIZATION_MAX': _template_system.to_json(node_size_normalization_max),
        'NODE_DRAG_FIX': _template_system.to_json(node_drag_fix),
        'NODE_HOVER_NEIGHBORHOOD': _template_system.to_json(node_hover_neighborhood),
        'NODE_HOVER_TOOLTIP': _template_system.to_json(node_hover_tooltip),

        'SHOW_NODE_IMAGE': _template_system.to_json(show_node_image),
        'NODE_IMAGE_SIZE_FACTOR': _template_system.to_json(node_image_size_factor),

        'SHOW_NODE_LABEL': _template_system.to_json(show_node_label),
        'SHOW_NODE_LABEL_BORDER': _template_system.to_json(show_node_label_border),
        'NODE_LABEL_DATA_SOURCE': _template_system.to_json(node_label_data_source),
        'NODE_LABEL_SIZE_FACTOR': _template_system.to_json(node_label_size_factor),
        'NODE_LABEL_ROTATION': _template_system.to_json(node_label_rotation),
        'NODE_LABEL_FONT': _template_system.to_json(node_label_font),

        'SHOW_EDGE': _template_system.to_json(show_edge),
        'EDGE_SIZE_FACTOR': _template_system.to_json(edge_size_factor),
        'EDGE_SIZE_DATA_SOURCE': _template_system.to_json(edge_size_data_source),
        'USE_EDGE_SIZE_NORMALIZATION': _template_system.to_json(use_edge_size_normalization),
        'EDGE_SIZE_NORMALIZATION_MIN': _template_system.to_json(edge_size_normalization_min),
        'EDGE_SIZE_NORMALIZATION_MAX': _template_system.to_json(edge_size_normalization_max),
        'EDGE_CURVATURE': _template_system.to_json(edge_curvature),
        'EDGE_HOVER_TOOLTIP': _template_system.to_json(edge_hover_tooltip),

        'SHOW_EDGE_LABEL': _template_system.to_json(show_edge_label),
        'SHOW_EDGE_LABEL_BORDER': _template_system.to_json(show_edge_label_border),
        'EDGE_LABEL_DATA_SOURCE': _template_system.to_json(edge_label_data_source),
        'EDGE_LABEL_SIZE_FACTOR': _template_system.to_json(edge_label_size_factor),
        'EDGE_LABEL_ROTATION': _template_system.to_json(edge_label_rotation),
        'EDGE_LABEL_FONT': _template_system.to_json(edge_label_font),

        'ZOOM_FACTOR': _template_system.to_json(zoom_factor),
        'LARGE_NETWORK_THRESHOLD': _template_system.to_json(large_network_threshold),

        'LAYOUT_ALGORITHM_ACTIVE': _template_system.to_json(layout_algorithm_active),
        'USE_MANY_BODY_FORCE': _template_system.to_json(use_many_body_force),
        'MANY_BODY_FORCE_STRENGTH': _template_system.to_json(many_body_force_strength),
        'MANY_BODY_FORCE_THETA': _template_system.to_json(many_body_force_theta),
        'USE_MANY_BODY_FORCE_MIN_DISTANCE': _template_system.to_json(
            use_many_body_force_min_distance),
        'MANY_BODY_FORCE_MIN_DISTANCE': _template_system.to_json(many_body_force_min_distance),
        'USE_MANY_BODY_FORCE_MAX_DISTANCE': _template_system.to_json(
            use_many_body_force_max_distance),
        'MANY_BODY_FORCE_MAX_DISTANCE': _template_system.to_json(many_body_force_max_distance),
        'USE_LINKS_FORCE': _template_system.to_json(use_links_force),
        'LINKS_FORCE_DISTANCE': _template_system.to_json(links_force_distance),
        'LINKS_FORCE_STRENGTH': _template_system.to_json(links_force_strength),
        'USE_COLLISION_FORCE': _template_system.to_json(use_collision_force),
        'COLLISION_FORCE_RADIUS': _template_system.to_json(collision_force_radius),
        'COLLISION_FORCE_STRENGTH': _template_system.to_json(collision_force_strength),
        'USE_X_POSITIONING_FORCE': _template_system.to_json(use_x_positioning_force),
        'X_POSITIONING_FORCE_STRENGTH': _template_system.to_json(x_positioning_force_strength),
        'USE_Y_POSITIONING_FORCE': _template_system.to_json(use_y_positioning_force),
        'Y_POSITIONING_FORCE_STRENGTH': _template_system.to_json(y_positioning_force_strength),
        'USE_CENTERING_FORCE': _template_system.to_json(use_centering_force),
    }
    site_template = _template_system.insert(site_template, insert_data)
    fig = _data_structures.Figure(site_template)
    return fig


def network_vis(data,
                network_height=450, details_height=100,
                show_details=False, show_details_toggle_button=True,
                show_menu=True, show_menu_toggle_button=True,
                show_node=True, node_size_factor=1.0,
                node_size_data_source='size', use_node_size_normalization=False,
                node_size_normalization_min=5.0, node_size_normalization_max=75.0,
                node_drag_fix=False, node_hover_neighborhood=False, node_hover_tooltip=True,
                show_node_image=True, node_image_size_factor=1.0,
                show_node_label=True, show_node_label_border=True, node_label_data_source='id',
                node_label_size_factor=1.0, node_label_rotation=0.0, node_label_font='Arial',
                show_edge=True, edge_size_factor=1.0,
                edge_size_data_source='size', use_edge_size_normalization=False,
                edge_size_normalization_min=0.2, edge_size_normalization_max=5.0,
                edge_curvature=0.3, edge_hover_tooltip=True,
                show_edge_label=False, show_edge_label_border=True, edge_label_data_source='id',
                edge_label_size_factor=1.0, edge_label_rotation=0.0, edge_label_font='Arial',
                zoom_factor=0.75, large_network_threshold=500,
                layout_algorithm_active=True, layout_algorithm='barnesHut',
                gravitational_constant=-2000.0, central_gravity=0.1, spring_length=70.0,
                spring_constant=0.1, avoid_overlap=0.0):
    """Create an interactive network plot from JSON graph format (JGF) data with vis.js.

    Note
    ----
    This plot differs from other network plots in following aspects:

    - Nodes do not have a border. Edges do not come with labels. Accordingly, this plot ignores
      following properties defined in the JSON graph format:

      - Graph metadata: ``node_border_color``, ``node_border_size``, ``edge_label_color``,
        ``edge_label_size``
      - Node metadata: ``border_color``, ``border_size``
      - Edge metadata: ``label_color``, ``label_size``

    - If nodes are hidden, then node labels and node images are hidden too.
    - Hovering over a node does not support neighborhood highlighting yet.
    - Node labels can not be rotated (and edge labels are not available yet).
    - There is no control over the initial zoom factor yet.

    Note
    ----
    This network plot currently differs from other network plots in following aspects:

    - vis.js does not support setting the opacity of nodes and edges.
      It also does not support setting arrow colors different from the edge color.
      Accordingly, this plot ignores following properties defined in the JSON graph format:
      - Graph metadata: ``arrow_color``, ``node_opacity``, ``edge_opacity``
      - Node metadata: ``opacity``
      - Edge metadata: ``opacity``

    - Node and edge opacity can not be set.
    - Node and edge labels can not be rotated.
    - Node and edge label borders may not be visible if zoomed closely.
    - If edges are hidden, then edge labels are hidden too.
    - If multiple self-loops (=edges that have the same source and target node) are present for
      a single node, they are drawn on top of each other and may not be distinguishable.
    - The initial zoom can not be controlled yet.

    Parameters
    ----------
    data : str, dict or graph object
        Graph data in :ref:`JSON graph format (JGF) <jgf-format>` as JSON string (*str*),
        JSON object (*dict*),
        :ref:`graph object of a supported graph library <supported-graph-libraries>`,
        or a list of multiple graphs, each defined in any of the previous ways.
        If the provided data contains multiple graphs, only the first one is shown on load,
        while the other ones can be chosen in the data selection menu in order to be displayed.
    network_height : int
        Height of the network container in pixels (px).
    details_height : int
        Height of the details container in pixels (px).
    show_details : bool
        If True, the details container is shown on load, otherwise hidden.
    show_details_toggle_button : bool
        If True, a button is shown that allows to toggle the visibility of the details container.
    show_menu : bool
        If True, the menu container is shown on load, otherwise hidden.
    show_menu_toggle_button : bool
        If True, a button is shown that allows to toggle the visibility of the menu container.
    show_node : bool
        If True, nodes are shown on load, otherwise hidden.
    node_size_factor : float
        A scaling factor that modifies node size.
    node_size_data_source : str
        Name of the numerical node property that is used as source for node size on load.
    use_node_size_normalization : bool
        If True, node sizes are normalized to lie in an interval between a
        chosen min and max value.
    node_size_normalization_min : float
        Minimum value for node size if node size normalization is active.
    node_size_normalization_max : float
        Maximum value for node size if node size normalization is active.
    node_drag_fix : bool
        If True, the position of a node becomes fixed after dragging it, i.e. the
        layout algorithm does not change its position but the user can drag it again.
    node_hover_neighborhood : bool
        If True, hovering a node leads to highlighting its neighborhood which consists of
        all incident edges and adjacent nodes.
    node_hover_tooltip : bool
        If True, hovering a node leads to popping up a tooltip if the hover property in the
        metadata of this node contains a non-empty string or HTML text.
    show_node_image : bool
        If True, node images are shown on load for all nodes whose image property in the metadata
        contains a valid image URL from which an image can be fetched.
    node_image_size_factor : float
        A scaling factor that modifies node image size.
    show_node_label : bool
        If True, node labels are shown on load, otherwise hidden.
    show_node_label_border : bool
        If True, node labels have a small border in the color of the background to better
        separate the text from other visual elements like edges or nodes.
    node_label_data_source : str
        Name of the node property that is used as source for node label text on load.
    node_label_size_factor : float
        A scaling factor that modifies node label size.
    node_label_rotation : float
        An angle that modifies node label orientation.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    node_label_font : str
        Name of the font that is used for node labels.
    show_edge : bool
        If True, edges are shown on load, otherwise hidden.
    edge_size_factor : float
        A scaling factor that modifies edge size (=edge width).
    edge_size_data_source : str
        Name of the edge property that is used as source for edge size on load.
    use_edge_size_normalization : bool
        If True, edge sizes are normalized to lie in an interval between a
        chosen min and max value.
    edge_size_normalization_min : float
        Minimum value for edge size if node size normalization is active.
    edge_size_normalization_max : float
        Maximum value for edge size if node size normalization is active.
    edge_curvature : float
        A factor that modifies edge curvature, where 0.0 means straight lines.
    edge_hover_tooltip : bool
        If True, hovering an edge leads to popping up a tooltip if the hover property in the
        metadata of this edge contains a non-empty string or HTML text.
    show_edge_label : bool
        If True, edge labels are shown on load, otherwise hidden.
    show_edge_label_border : bool
        If True, edge labels have a small border in the color of the background to better
        separate the text from other visual elements like edges or nodes.
    edge_label_data_source : str
        Name of the edge property that is used as source for edge label text on load.
    edge_label_size_factor : float
        A scaling factor that modifies edge label size.
    edge_label_rotation : float
        An angle that modifies edge label orientation.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    edge_label_font : str
        Name of the font that is used for edge labels.
    zoom_factor : float
        Factor that modifies how close the camera is to the drawing area on load.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    large_network_threshold : int
        Number that determines from when on a network is considered to be large, which
        means that before visualizing it an initial layout is calculated without moving anything.
        Caution: This feature is currently not available.
    layout_algorithm_active : bool
        If True, the layout algorithm is active on load and leads to movement, otherwise inactive.
    layout_algorithm : str
        Name of the used layout algorithm (vis.js term: "solver" of the "physics simulation").
        Possible values: "barnesHut", "forceAtlas2Based", "repulsion", "hierarchicalRepulsion"
    gravitational_constant : float
        Number that determines the strength of the many-body force acting between all pairs of
        nodes. It can be positive to cause attraction or negative (usual case) to cause repulsion.
        Only active if layout_algorithm is "barnesHut" or "forceAtlas2Based".
    central_gravity : float
        Number that determines the strength of the centering force that pulls the network
        towards the center of the coordinate system (0,0) to keep it in the display area.
    spring_length : float
        Number that determines the desired distance in the links force (vis.js terminology: edges
        are modeled as "springs") that acts between connected pairs of nodes.
    spring_constant : float
        Number that determines the strength of the links force.
    avoid_overlap : float
        Number that determines the strength of the collision force that acts between nodes
        if they come too close together.
        Only active if layout_algorithm is "barnesHut", "forceAtlas2Based" or
        "hierarchicalRepulsion".

    Returns
    -------
    A :ref:`Figure <js-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://visjs.org
    - https://visjs.github.io/vis-network/docs/network

    """
    # Argument processing
    data = _shared_preprocessing.prepare_graph_data(data)

    # Transformation
    site_template = _template_system.load('templates/network_vis.html')
    insert_data = {
        'DEFINE_VIS': _template_system.load(
            'third_party/vis-network/vis-network.min.def.js'),

        'DATA': _template_system.to_json(data),
        'NETWORK_HEIGHT': _template_system.to_json(network_height),
        'DETAILS_HEIGHT': _template_system.to_json(details_height),
        'SHOW_DETAILS': _template_system.to_json(show_details),
        'SHOW_DETAILS_TOGGLE_BUTTON': _template_system.to_json(show_details_toggle_button),
        'SHOW_MENU': _template_system.to_json(show_menu),
        'SHOW_MENU_TOGGLE_BUTTON': _template_system.to_json(show_menu_toggle_button),

        'SHOW_NODE': _template_system.to_json(show_node),
        'NODE_SIZE_FACTOR': _template_system.to_json(node_size_factor),
        'NODE_SIZE_DATA_SOURCE': _template_system.to_json(node_size_data_source),
        'USE_NODE_SIZE_NORMALIZATION': _template_system.to_json(use_node_size_normalization),
        'NODE_SIZE_NORMALIZATION_MIN': _template_system.to_json(node_size_normalization_min),
        'NODE_SIZE_NORMALIZATION_MAX': _template_system.to_json(node_size_normalization_max),
        'NODE_DRAG_FIX': _template_system.to_json(node_drag_fix),
        'NODE_HOVER_NEIGHBORHOOD': _template_system.to_json(node_hover_neighborhood),
        'NODE_HOVER_TOOLTIP': _template_system.to_json(node_hover_tooltip),

        'SHOW_NODE_IMAGE': _template_system.to_json(show_node_image),
        'NODE_IMAGE_SIZE_FACTOR': _template_system.to_json(node_image_size_factor),

        'SHOW_NODE_LABEL': _template_system.to_json(show_node_label),
        'SHOW_NODE_LABEL_BORDER': _template_system.to_json(show_node_label_border),
        'NODE_LABEL_DATA_SOURCE': _template_system.to_json(node_label_data_source),
        'NODE_LABEL_SIZE_FACTOR': _template_system.to_json(node_label_size_factor),
        'NODE_LABEL_ROTATION': _template_system.to_json(node_label_rotation),
        'NODE_LABEL_FONT': _template_system.to_json(node_label_font),

        'SHOW_EDGE': _template_system.to_json(show_edge),
        'EDGE_SIZE_FACTOR': _template_system.to_json(edge_size_factor),
        'EDGE_SIZE_DATA_SOURCE': _template_system.to_json(edge_size_data_source),
        'USE_EDGE_SIZE_NORMALIZATION': _template_system.to_json(use_edge_size_normalization),
        'EDGE_SIZE_NORMALIZATION_MIN': _template_system.to_json(edge_size_normalization_min),
        'EDGE_SIZE_NORMALIZATION_MAX': _template_system.to_json(edge_size_normalization_max),
        'EDGE_CURVATURE': _template_system.to_json(edge_curvature),
        'EDGE_HOVER_TOOLTIP': _template_system.to_json(edge_hover_tooltip),

        'SHOW_EDGE_LABEL': _template_system.to_json(show_edge_label),
        'SHOW_EDGE_LABEL_BORDER': _template_system.to_json(show_edge_label_border),
        'EDGE_LABEL_DATA_SOURCE': _template_system.to_json(edge_label_data_source),
        'EDGE_LABEL_SIZE_FACTOR': _template_system.to_json(edge_label_size_factor),
        'EDGE_LABEL_ROTATION': _template_system.to_json(edge_label_rotation),
        'EDGE_LABEL_FONT': _template_system.to_json(edge_label_font),

        'ZOOM_FACTOR': _template_system.to_json(zoom_factor),
        'LARGE_NETWORK_THRESHOLD': _template_system.to_json(large_network_threshold),

        'LAYOUT_ALGORITHM_ACTIVE': _template_system.to_json(layout_algorithm_active),
        'LAYOUT_ALGORITHM': _template_system.to_json(layout_algorithm),
        'GRAVITATIONLAL_CONSTANT': _template_system.to_json(gravitational_constant),
        'CENTRAL_GRAVITY': _template_system.to_json(central_gravity),
        'SPRING_LENGTH': _template_system.to_json(spring_length),
        'SPRING_CONSTANT': _template_system.to_json(spring_constant),
        'AVOID_OVERLAP': _template_system.to_json(avoid_overlap),
    }
    site_template = _template_system.insert(site_template, insert_data)
    fig = _data_structures.Figure(site_template)
    return fig


def network_webgl(data,
                  network_height=450, details_height=100,
                  show_details=False, show_details_toggle_button=True,
                  show_menu=True, show_menu_toggle_button=True,
                  show_node=True, node_size_factor=1.0,
                  node_size_data_source='size', use_node_size_normalization=False,
                  node_size_normalization_min=5.0, node_size_normalization_max=75.0,
                  node_drag_fix=False, node_hover_neighborhood=False, node_hover_tooltip=True,
                  show_node_image=True, node_image_size_factor=1.0,
                  show_node_label=True, show_node_label_border=True, node_label_data_source='id',
                  node_label_size_factor=1.0, node_label_rotation=0.0, node_label_font='Arial',
                  show_edge=True, edge_size_factor=1.0,
                  edge_size_data_source='size', use_edge_size_normalization=False,
                  edge_size_normalization_min=0.2, edge_size_normalization_max=5.0,
                  edge_curvature=0.3, edge_hover_tooltip=True,
                  show_edge_label=False, show_edge_label_border=True, edge_label_data_source='id',
                  edge_label_size_factor=1.0, edge_label_rotation=0.0, edge_label_font='Arial',
                  zoom_factor=0.75, large_network_threshold=200,
                  layout_algorithm_active=True,
                  use_many_body_force=True, many_body_force_strength=-70.0,
                  many_body_force_theta=0.9,
                  use_many_body_force_min_distance=False, many_body_force_min_distance=10.0,
                  use_many_body_force_max_distance=False, many_body_force_max_distance=1000.0,
                  use_links_force=True, links_force_distance=50.0, links_force_strength=0.5,
                  use_x_positioning_force=False, x_positioning_force_strength=0.2,
                  use_y_positioning_force=False, y_positioning_force_strength=0.2,
                  use_z_positioning_force=False, z_positioning_force_strength=0.2,
                  use_centering_force=True):
    """Create an interactive network plot from JSON graph format (JGF) data with 3d-force-graph.js.

    Note
    ----
    This plot differs from other network plots in following aspects:

    - Nodes do not have a border. Edges do not come with labels. Accordingly, this plot ignores
      following properties defined in the JSON graph format:

      - Graph metadata: ``node_border_color``, ``node_border_size``, ``edge_label_color``,
        ``edge_label_size``
      - Node metadata: ``border_color``, ``border_size``
      - Edge metadata: ``label_color``, ``label_size``

    - If nodes are hidden, then node labels and node images are hidden too.
    - Hovering over a node does not support neighborhood highlighting yet.
    - Node labels can not be rotated (and edge labels are not available yet).
    - There is no control over the initial zoom factor yet.

    Parameters
    ----------
    data : str, dict or graph object
        Graph data in :ref:`JSON graph format (JGF) <jgf-format>` as JSON string (*str*),
        JSON object (*dict*),
        :ref:`graph object of a supported graph library <supported-graph-libraries>`,
        or a list of multiple graphs, each defined in any of the previous ways.
        If the provided data contains multiple graphs, only the first one is shown on load,
        while the other ones can be chosen in the data selection menu in order to be displayed.
    network_height : int
        Height of the network container in pixels (px).
    details_height : int
        Height of the details container in pixels (px).
    show_details : bool
        If True, the details container is shown on load, otherwise hidden.
    show_details_toggle_button : bool
        If True, a button is shown that allows to toggle the visibility of the details container.
    show_menu : bool
        If True, the menu container is shown on load, otherwise hidden.
    show_menu_toggle_button : bool
        If True, a button is shown that allows to toggle the visibility of the menu container.
    show_node : bool
        If True, nodes are shown on load, otherwise hidden.
    node_size_factor : float
        A scaling factor that modifies node size.
    node_size_data_source : str
        Name of the numerical node property that is used as source for node size on load.
    use_node_size_normalization : bool
        If True, node sizes are normalized to lie in an interval between a
        chosen min and max value.
    node_size_normalization_min : float
        Minimum value for node size if node size normalization is active.
    node_size_normalization_max : float
        Maximum value for node size if node size normalization is active.
    node_drag_fix : bool
        If True, the position of a node becomes fixed after dragging it, i.e. the
        layout algorithm does not change its position but the user can drag it again.
    node_hover_neighborhood : bool
        If True, hovering a node leads to highlighting its neighborhood which consists of
        all incident edges and adjacent nodes.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    node_hover_tooltip : bool
        If True, hovering a node leads to popping up a tooltip if the hover property in the
        metadata of this node contains a non-empty string or HTML text.
    show_node_image : bool
        If True, node images are shown on load for all nodes whose image property in the metadata
        contains a valid image URL from which an image can be fetched.
    node_image_size_factor : float
        A scaling factor that modifies node image size.
    show_node_label : bool
        If True, node labels are shown on load, otherwise hidden.
    show_node_label_border : bool
        If True, node labels have a small border in the color of the background to better
        separate the text from other visual elements like edges or nodes.
    node_label_data_source : str
        Name of the node property that is used as source for node label text on load.
    node_label_size_factor : float
        A scaling factor that modifies node label size.
    node_label_rotation : float
        An angle that modifies node label orientation.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    node_label_font : str
        Name of the font that is used for node labels.
    show_edge : bool
        If True, edges are shown on load, otherwise hidden.
    edge_size_factor : float
        A scaling factor that modifies edge size (=edge width).
    edge_size_data_source : str
        Name of the edge property that is used as source for edge size on load.
    use_edge_size_normalization : bool
        If True, edge sizes are normalized to lie in an interval between a
        chosen min and max value.
    edge_size_normalization_min : float
        Minimum value for edge size if node size normalization is active.
    edge_size_normalization_max : float
        Maximum value for edge size if node size normalization is active.
    edge_curvature : float
        A factor that modifies edge curvature, where 0.0 means straight lines.
    edge_hover_tooltip : bool
        If True, hovering an edge leads to popping up a tooltip if the hover property in the
        metadata of this edge contains a non-empty string or HTML text.
    show_edge_label : bool
        If True, edge labels are shown on load, otherwise hidden.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    show_edge_label_border : bool
        If True, edge labels have a small border in the color of the background to better
        separate the text from other visual elements like edges or nodes.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    edge_label_data_source : str
        Name of the edge property that is used as source for edge label text on load.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    edge_label_size_factor : float
        A scaling factor that modifies edge label size.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    edge_label_rotation : float
        An angle that modifies edge label orientation.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    edge_label_font : str
        Name of the font that is used for edge labels.
    zoom_factor : float
        Factor that modifies how close the camera is to the drawing area on load.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    large_network_threshold : int
        Number that determines from when on a network is considered to be large, which
        means that before visualizing it an initial layout is calculated without moving anything.
    layout_algorithm_active : bool
        If True, the layout algorithm is active on load and leads to movement, otherwise inactive.
    use_many_body_force : bool
        If True, many body force is active in the layout algorithm.
        This force acts between any pair of nodes but can be restricted to only act on nodes
        within a certain distance.
    many_body_force_strength : float
        Number that determines the strength of the force. It can be positive to cause attraction
        or negative (usual case) to cause repulsion between nodes.
    many_body_force_theta : float
        Number that determines the accuracy of the Barnes–Hut approximation of the
        many-body simulation where nodes are grouped instead of treated individually
        to improve performance.
    use_many_body_force_min_distance : bool
        If True, a minimum distance between nodes is used in the many-body force calculation.
        This effectively leads to an upper bound on the strength of the force between any two
        nodes and avoids instability.
    many_body_force_min_distance : float
        Number that determines the minimum distance between nodes over which the many-body force
        is active.
    use_many_body_force_max_distance : bool
        If True, a maximum distance between nodes is used in the many-body force calculation.
        This can improve performance but results in a more localized layout.
    many_body_force_max_distance : float
        Number that determines the maximum distance between nodes over which the many-body force
        is active.
    use_links_force : bool
        If True, link force is active in the layout algorithm.
        This force acts between pairs of nodes that are connected by an edge. It pushes them
        together or apart in order to come close to a certain distance between connected nodes.
    links_force_distance : float
        Number that determines the preferred distance between connected nodes.
    links_force_strength : float
        Number that determines the strength of the links force.
    use_collision_force : bool
        If True, collision force is active in the layout algorithm.
        This force treats nodes as circles instead of points and acts on pairs of nodes that
        overlap in order to push them apart.
    collision_force_radius : float
        Number that determines the radius of the circle around each node.
    collision_force_strength : float
        Number that determines the strength of the force.
    use_x_positioning_force : bool
        If True, x-positioning force is active in the layout algorithm.
        This force modifies the x position of each node towards 0.0, effectively pushing them
        towards the yz-plane.
    x_positioning_force_strength : float
        Number that indicates the strength of the force.
    use_y_positioning_force : bool
        This force modifies the y position of each node towards 0.0, effectively pushing them
        towards the xz-plane.
    y_positioning_force_strength : float
        Number that indicates the strength of the force.
    use_z_positioning_force : bool
        If True, z-positioning force is active in the layout algorithm.
        This force modifies the z position of each node towards 0.0, effectively pushing them
        towards the xy-plane.
    z_positioning_force_strength : float
        Number that indicates the strength of the force.
    use_centering_force : bool
        This force attracts each node towards the center of the coordinate system at (0, 0, 0)
        to keep the graph in the display area. It may lead to unexpected repulsion effects
        if all nodes are fixed and then a single one is released by dragging it.

    Returns
    -------
    A :ref:`Figure <js-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://github.com/vasturiano/3d-force-graph

    """
    # Argument processing
    data = _shared_preprocessing.prepare_graph_data(data)

    # Transformation
    site_template = _template_system.load('templates/network_webgl.html')
    insert_data = {
        'DEFINE_THREE': _template_system.load('third_party/three/three.min.def.js'),
        'DEFINE_3D_FORCE_GRAPH': _template_system.load(
            'third_party/3d-force-graph/3d-force-graph.min.def.js'),

        'DATA': _template_system.to_json(data),
        'NETWORK_HEIGHT': _template_system.to_json(network_height),
        'DETAILS_HEIGHT': _template_system.to_json(details_height),
        'SHOW_DETAILS': _template_system.to_json(show_details),
        'SHOW_DETAILS_TOGGLE_BUTTON': _template_system.to_json(show_details_toggle_button),
        'SHOW_MENU': _template_system.to_json(show_menu),
        'SHOW_MENU_TOGGLE_BUTTON': _template_system.to_json(show_menu_toggle_button),

        'SHOW_NODE': _template_system.to_json(show_node),
        'NODE_SIZE_FACTOR': _template_system.to_json(node_size_factor),
        'NODE_SIZE_DATA_SOURCE': _template_system.to_json(node_size_data_source),
        'USE_NODE_SIZE_NORMALIZATION': _template_system.to_json(use_node_size_normalization),
        'NODE_SIZE_NORMALIZATION_MIN': _template_system.to_json(node_size_normalization_min),
        'NODE_SIZE_NORMALIZATION_MAX': _template_system.to_json(node_size_normalization_max),
        'NODE_DRAG_FIX': _template_system.to_json(node_drag_fix),
        'NODE_HOVER_NEIGHBORHOOD': _template_system.to_json(node_hover_neighborhood),
        'NODE_HOVER_TOOLTIP': _template_system.to_json(node_hover_tooltip),

        'SHOW_NODE_IMAGE': _template_system.to_json(show_node_image),
        'NODE_IMAGE_SIZE_FACTOR': _template_system.to_json(node_image_size_factor),

        'SHOW_NODE_LABEL': _template_system.to_json(show_node_label),
        'SHOW_NODE_LABEL_BORDER': _template_system.to_json(show_node_label_border),
        'NODE_LABEL_DATA_SOURCE': _template_system.to_json(node_label_data_source),
        'NODE_LABEL_SIZE_FACTOR': _template_system.to_json(node_label_size_factor),
        'NODE_LABEL_ROTATION': _template_system.to_json(node_label_rotation),
        'NODE_LABEL_FONT': _template_system.to_json(node_label_font),

        'SHOW_EDGE': _template_system.to_json(show_edge),
        'EDGE_SIZE_FACTOR': _template_system.to_json(edge_size_factor),
        'EDGE_SIZE_DATA_SOURCE': _template_system.to_json(edge_size_data_source),
        'USE_EDGE_SIZE_NORMALIZATION': _template_system.to_json(use_edge_size_normalization),
        'EDGE_SIZE_NORMALIZATION_MIN': _template_system.to_json(edge_size_normalization_min),
        'EDGE_SIZE_NORMALIZATION_MAX': _template_system.to_json(edge_size_normalization_max),
        'EDGE_CURVATURE': _template_system.to_json(edge_curvature),
        'EDGE_HOVER_TOOLTIP': _template_system.to_json(edge_hover_tooltip),

        'SHOW_EDGE_LABEL': _template_system.to_json(show_edge_label),
        'SHOW_EDGE_LABEL_BORDER': _template_system.to_json(show_edge_label_border),
        'EDGE_LABEL_DATA_SOURCE': _template_system.to_json(edge_label_data_source),
        'EDGE_LABEL_SIZE_FACTOR': _template_system.to_json(edge_label_size_factor),
        'EDGE_LABEL_ROTATION': _template_system.to_json(edge_label_rotation),
        'EDGE_LABEL_FONT': _template_system.to_json(edge_label_font),

        'ZOOM_FACTOR': _template_system.to_json(zoom_factor),
        'LARGE_NETWORK_THRESHOLD': _template_system.to_json(large_network_threshold),

        'LAYOUT_ALGORITHM_ACTIVE': _template_system.to_json(layout_algorithm_active),
        'USE_MANY_BODY_FORCE': _template_system.to_json(use_many_body_force),
        'MANY_BODY_FORCE_STRENGTH': _template_system.to_json(many_body_force_strength),
        'MANY_BODY_FORCE_THETA': _template_system.to_json(many_body_force_theta),
        'USE_MANY_BODY_FORCE_MIN_DISTANCE': _template_system.to_json(
            use_many_body_force_min_distance),
        'MANY_BODY_FORCE_MIN_DISTANCE': _template_system.to_json(many_body_force_min_distance),
        'USE_MANY_BODY_FORCE_MAX_DISTANCE': _template_system.to_json(
            use_many_body_force_max_distance),
        'MANY_BODY_FORCE_MAX_DISTANCE': _template_system.to_json(many_body_force_max_distance),
        'USE_LINKS_FORCE': _template_system.to_json(use_links_force),
        'LINKS_FORCE_DISTANCE': _template_system.to_json(links_force_distance),
        'LINKS_FORCE_STRENGTH': _template_system.to_json(links_force_strength),
        'USE_X_POSITIONING_FORCE': _template_system.to_json(use_x_positioning_force),
        'X_POSITIONING_FORCE_STRENGTH': _template_system.to_json(x_positioning_force_strength),
        'USE_Y_POSITIONING_FORCE': _template_system.to_json(use_y_positioning_force),
        'Y_POSITIONING_FORCE_STRENGTH': _template_system.to_json(y_positioning_force_strength),
        'USE_Z_POSITIONING_FORCE': _template_system.to_json(use_z_positioning_force),
        'Z_POSITIONING_FORCE_STRENGTH': _template_system.to_json(z_positioning_force_strength),
        'USE_CENTERING_FORCE': _template_system.to_json(use_centering_force),
    }
    site_template = _template_system.insert(site_template, insert_data)
    fig = _data_structures.Figure(site_template)
    return fig

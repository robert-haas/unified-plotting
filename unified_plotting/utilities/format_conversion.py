"""Conversion of various graph and vector data formats."""

from copy import deepcopy as _deepcopy


def _prepare_jgf_dict():
    data = {'graph': {'nodes': [], 'edges': []}}
    data_graph = data['graph']
    data_nodes = data['graph']['nodes']
    data_edges = data['graph']['edges']
    return data, data_graph, data_nodes, data_edges


def _insert_graph_data(data_graph, graph_directed, graph_metadata_dict):
    data_graph['directed'] = graph_directed
    if isinstance(graph_metadata_dict, dict) and graph_metadata_dict:
        # keys belonging to data level
        for key in ('label', 'type'):
            if key in graph_metadata_dict:
                data_graph[key] = graph_metadata_dict.pop(key)
        # keys belonging to metadata level
        if graph_metadata_dict:
            data_graph['metadata'] = graph_metadata_dict


def _insert_node_data(data_nodes, node_id, node_metadata_dict):
    node_dict = {'id': node_id}
    if isinstance(node_metadata_dict, dict) and node_metadata_dict:
        # keys belonging to data level
        for key in ('label', ):
            if key in node_metadata_dict:
                node_dict[key] = node_metadata_dict.pop(key)
        # keys belonging to metadata level
        if node_metadata_dict:
            node_dict['metadata'] = node_metadata_dict
    data_nodes.append(node_dict)


def _insert_edge_data(data_edges, edge_source_id, edge_target_id, edge_metadata_dict):
    edge_dict = {
        'source': edge_source_id,
        'target': edge_target_id,
    }
    if isinstance(edge_metadata_dict, dict) and edge_metadata_dict:
        # keys belonging to data level
        for key in ('id', 'label', 'relation', 'directed'):
            if key in edge_metadata_dict:
                edge_dict[key] = edge_metadata_dict.pop(key)
        # keys belonging to metadata level
        if edge_metadata_dict:
            edge_dict['metadata'] = edge_metadata_dict
    data_edges.append(edge_dict)


def graphtool_to_jgf(graph_object):
    """Convert a graph-tool graph object to JSON graph format (JGF)."""
    # TODO: Ignoring 0 and 0.0 values because they represent missing values, will create problems
    data, data_graph, data_nodes, data_edges = _prepare_jgf_dict()

    # 1) Graph properties
    graph_directed = graph_object.is_directed()
    graph_metadata_dict = {key: graph_object.graph_properties[key]  # key syntax is necessary
                           for key in graph_object.graph_properties.keys()}
    _insert_graph_data(data_graph, graph_directed, graph_metadata_dict)

    # 2) Nodes and their properties
    for node_object in graph_object.vertices():
        node_id = str(node_object)
        node_metadata_dict = {}
        for key, value_array in graph_object.vertex_properties.items():
            val = value_array[node_object]
            if isinstance(val, (str, int, float)) and val not in ('', 0, 0.0):
                node_metadata_dict[key] = val
        _insert_node_data(data_nodes, node_id, node_metadata_dict)

    # 3) Edges and their properties
    for edge_object in graph_object.edges():
        edge_source_id = str(edge_object.source())
        edge_target_id = str(edge_object.target())
        edge_metadata_dict = {}
        for key, value_array in graph_object.edge_properties.items():
            val = value_array[edge_object]
            if val not in ('', 0, 0.0):
                edge_metadata_dict[key] = val
        _insert_edge_data(data_edges, edge_source_id, edge_target_id, edge_metadata_dict)
    return data


def igraph_to_jgf(graph_object):
    """Convert an igraph graph object to JSON graph format (JGF)."""
    data, data_graph, data_nodes, data_edges = _prepare_jgf_dict()

    # 1) Graph properties
    graph_directed = graph_object.is_directed()
    graph_metadata_dict = {attr: graph_object[attr] for attr in graph_object.attributes()}
    _insert_graph_data(data_graph, graph_directed, graph_metadata_dict)

    # 2) Nodes and their properties
    for node_object in graph_object.vs:
        node_id = str(node_object.index)
        node_metadata_dict = {key: val for key, val in node_object.attributes().items()
                              if val is not None}
        _insert_node_data(data_nodes, node_id, node_metadata_dict)

    # 3) Edges and their properties
    for edge_object in graph_object.es:
        edge_source_id = str(edge_object.source)
        edge_target_id = str(edge_object.target)
        edge_metadata_dict = {key: val for key, val in edge_object.attributes().items()
                              if val is not None}
        _insert_edge_data(data_edges, edge_source_id, edge_target_id, edge_metadata_dict)
    return data


def networkit_to_jgf(graph_object):
    """Convert a NetworKit graph object to JSON graph format (JGF)."""
    # Argument processing
    graph_metadata, node_metadata, edge_metadata = {}, {}, {}
    if isinstance(graph_object, list):
        if len(graph_object) >= 2:
            graph_metadata = graph_object[1]
        if len(graph_object) >= 3:
            node_metadata = graph_object[2]
            if isinstance(node_metadata, dict):
                node_metadata = {str(key): val for key, val in node_metadata.items()}
            else:
                node_metadata = {}
        if len(graph_object) >= 4:
            edge_metadata = graph_object[3]
            if isinstance(edge_metadata, dict):
                edge_metadata = {str(key): val for key, val in edge_metadata.items()}
            else:
                edge_metadata = {}
        graph_object = graph_object[0]

    # Transformation
    data, data_graph, data_nodes, data_edges = _prepare_jgf_dict()

    # 1) Graph properties
    # Note: graph.getName() was dropped - https://github.com/networkit/networkit/pull/421
    graph_directed = graph_object.isDirected()
    graph_metadata_dict = graph_metadata
    _insert_graph_data(data_graph, graph_directed, graph_metadata_dict)

    # 2) Nodes and their properties
    def parse_node(node):
        node_id = str(node)
        node_metadata_dict = node_metadata.get(node_id, {})
        _insert_node_data(data_nodes, node_id, node_metadata_dict)

    graph_object.forNodes(parse_node)

    # 3) Edges and their properties
    def parse_edge(source_node, target_node, edge_weight, edge_id):
        edge_source_id = str(source_node)
        edge_target_id = str(target_node)
        used_edge_id = '({}, {})'.format(edge_source_id, edge_target_id)
        edge_metadata_dict = edge_metadata.get(used_edge_id, {})
        _insert_edge_data(data_edges, edge_source_id, edge_target_id, edge_metadata_dict)

    graph_object.forEdges(parse_edge)
    return data


def networkx_to_jgf(graph_object):
    """Convert a NetworkX graph object to JSON graph format (JGF)."""
    data, data_graph, data_nodes, data_edges = _prepare_jgf_dict()

    # Copy to prevent side effects (preferably deep, otherwise shallow)
    try:
        graph_object = _deepcopy(graph_object)
    except Exception:
        graph_object = graph_object.copy()

    # 1) Graph properties
    graph_directed = graph_object.is_directed()
    graph_metadata_dict = dict(graph_object.graph)
    _insert_graph_data(data_graph, graph_directed, graph_metadata_dict)

    # 2) Nodes and their properties
    for node_object in graph_object.nodes:
        node_id = str(node_object)
        node_metadata_dict = graph_object.nodes[node_object]
        _insert_node_data(data_nodes, node_id, node_metadata_dict)

    # 3) Edges and their properties
    for edge_object in graph_object.edges:
        edge_source_id = str(edge_object[0])
        edge_target_id = str(edge_object[1])
        edge_metadata_dict = graph_object.edges[edge_object]
        _insert_edge_data(data_edges, edge_source_id, edge_target_id, edge_metadata_dict)
    return data


def pyntacle_to_jgf(graph_object):
    """Convert a Pyntacle graph object to JSON graph format (JGF)."""
    # Internally it uses igraph objects, therefore the same conversion method can be used
    return igraph_to_jgf(graph_object)


def snap_to_jgf(graph_object):
    """Convert a SNAP graph object to JSON graph format (JGF)."""
    import snap
    data, data_graph, data_nodes, data_edges = _prepare_jgf_dict()

    def get_node_attributes_empty(graph_object, node_id):
        return {}

    def get_node_attributes_filled(graph_object, node_id):
        node_attr_dict = {}
        int_attribute_vec = snap.TStrV()
        flt_attribute_vec = snap.TStrV()
        str_attribute_vec = snap.TStrV()
        graph_object.IntAttrNameNI(node_id, int_attribute_vec)
        graph_object.FltAttrNameNI(node_id, flt_attribute_vec)
        graph_object.StrAttrNameNI(node_id, str_attribute_vec)
        for int_attr in int_attribute_vec:
            node_attr_dict[int_attr] = graph_object.GetIntAttrDatN(node_id, int_attr)
        for flt_attr in flt_attribute_vec:
            node_attr_dict[flt_attr] = graph_object.GetFltAttrDatN(node_id, flt_attr)
        for str_attr in str_attribute_vec:
            node_attr_dict[str_attr] = graph_object.GetStrAttrDatN(node_id, str_attr)
        return node_attr_dict

    def get_edge_attributes_empty(graph_object, edge_id):
        return {}

    def get_edge_attributes_filled(graph_object, edge_id):
        edge_attr_dict = {}
        int_attribute_vec = snap.TStrV()
        flt_attribute_vec = snap.TStrV()
        str_attribute_vec = snap.TStrV()
        graph_object.IntAttrNameEI(edge_id, int_attribute_vec)
        graph_object.FltAttrNameEI(edge_id, flt_attribute_vec)
        graph_object.StrAttrNameEI(edge_id, str_attribute_vec)
        for int_attr in int_attribute_vec:
            edge_attr_dict[int_attr] = graph_object.GetIntAttrDatE(edge_id, int_attr)
        for flt_attr in flt_attribute_vec:
            edge_attr_dict[flt_attr] = graph_object.GetFltAttrDatE(edge_id, flt_attr)
        for str_attr in str_attribute_vec:
            edge_attr_dict[str_attr] = graph_object.GetStrAttrDatE(edge_id, str_attr)
        return edge_attr_dict

    if 'snap.PNEANet' in str(type(graph_object)):
        get_node_attributes = get_node_attributes_filled
        get_edge_attributes = get_edge_attributes_filled
    else:
        get_node_attributes = get_node_attributes_empty
        get_edge_attributes = get_edge_attributes_empty

    # 1) Graph properties
    _gt = str(type(graph_object))
    graph_directed = 'snap.PNGraph' in _gt or 'snap.PDirNet' in _gt or 'snap.PNEANet' in _gt
    graph_metadata_dict = {}  # Note: Seems to not be available in SNAP
    _insert_graph_data(data_graph, graph_directed, graph_metadata_dict)

    # 2) Nodes and their properties
    for node_object in graph_object.Nodes():
        node_id = str(node_object.GetId())
        node_metadata_dict = get_node_attributes(graph_object, node_object.GetId())
        _insert_node_data(data_nodes, node_id, node_metadata_dict)

    # 3) Edges and their properties
    for edge_object in graph_object.Edges():
        edge_source_id = str(edge_object.GetSrcNId())
        edge_target_id = str(edge_object.GetDstNId())
        edge_metadata_dict = get_edge_attributes(graph_object, edge_object.GetId())
        _insert_edge_data(data_edges, edge_source_id, edge_target_id, edge_metadata_dict)
    return data


def dataframe_to_vector_data(df):
    """Convert a Pandas dataframe to vector data (list of lists)."""
    column_names = list(df.columns)
    data = [df[col] for col in column_names]
    return data, column_names

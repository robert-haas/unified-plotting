import os
from copy import deepcopy

import pandas as pd
import pytest

import unified_plotting as up
from network_data_loading import (TESTDATA_GRAPH_TOOL, TESTDATA_IGRAPH, TESTDATA_JGF,
                                  TESTDATA_NETWORKIT, TESTDATA_NETWORKX, TESTDATA_PYNTACLE,
                                  TESTDATA_SNAP)
from shared_data_loading import (IN_DIR, TESTDATA, TESTDATA_PDF_FILES, TESTDATA_PNG_FILES,
                                 TESTDATA_SMALL, TESTDATA_SVG_FILES)
from unified_plotting.utilities import base64, format_conversion


# Common preliminaries

def create_output_filepath(my_outdir, name):
    return os.path.join(my_outdir, 'javascript_' + name)


def export_all_available_formats(fig, filepath):
    fig.export_html(filepath)


# Tests with pytest

# n-dimensional plots

@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_pc_table_export(my_outdir, name, x, y, z):
    fig = up.javascript.parallel_coordinates_table(data=[x, y, z])
    filepath = create_output_filepath(my_outdir, 'pc_table_' + name)
    export_all_available_formats(fig, filepath)


def test_pc_table_from_file(my_outdir):
    # CSV file with header row
    filepath = os.path.join(IN_DIR, 'uci_wine.csv')
    fig = up.javascript.parallel_coordinates_table(filepath)
    filepath = create_output_filepath(my_outdir, 'javascript_pc_table_csv_file_wine')
    export_all_available_formats(fig, filepath)

    # CSV file without header row
    filepath = os.path.join(IN_DIR, 'iris_with_header.csv')
    fig = up.javascript.parallel_coordinates_table(filepath)
    filepath = create_output_filepath(my_outdir, 'javascript_pc_table_csv_file_iris')
    export_all_available_formats(fig, filepath)

    # Invalid CSV
    with pytest.raises(ValueError):
        filepath = os.path.join(IN_DIR, 'dg.json.csv')
        up.javascript.parallel_coordinates_table(filepath)


def test_pc_table_from_dataframe(my_outdir):
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [11, 22, 33], 'z': [333, 222, 111]})
    up.javascript.parallel_coordinates_table(df)
    up.javascript.parallel_coordinates_table(data=df)
    with pytest.raises(ValueError):
        df.x = list(df.x) + [42]
        up.javascript.parallel_coordinates_table(df)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_pc_table_parameters(name, x, y, z):
    # default
    up.javascript.parallel_coordinates_table([x, y, z])
    up.javascript.parallel_coordinates_table(data=[x, y, z])
    with pytest.raises(ValueError):
        up.javascript.parallel_coordinates_table([x, y+[42], z])
    with pytest.raises(ValueError):
        up.javascript.parallel_coordinates_table(data=[x, y+[42], z])

    # different data types
    up.javascript.parallel_coordinates_table(data=[[1, 2, 3]])
    up.javascript.parallel_coordinates_table(data=[['a', 'b', 'c']])
    up.javascript.parallel_coordinates_table(data=[[1, 2, 3], ['a', 'b', 'c']])
    up.javascript.parallel_coordinates_table(data=[['a', 'b', 'c'], [1, 2, 3]])
    up.javascript.parallel_coordinates_table(data=[['a', 'b', 'c'], [1, 2, 3], ['d', 'e', 'f']])

    # name
    up.javascript.parallel_coordinates_table(data=[x, y, z], name=['c1'])
    up.javascript.parallel_coordinates_table(data=[x, y, z], name=['c1', 'c2', 'c3'])
    up.javascript.parallel_coordinates_table(data=[x, y, z], name=['c1', 'c2', 'c3', 'c4'])

    # column_html
    up.javascript.parallel_coordinates_table(
        data=[x, y, z], name=['c1', 'c2', 'c3'], column_html='c1')
    up.javascript.parallel_coordinates_table(
        data=[x, y, z], name=['c1', 'c2', 'c3'], column_html=['c1', 'c3'])
    with pytest.raises(ValueError):
        up.javascript.parallel_coordinates_table(
            data=[x, y, z], name=['c1', 'c2', 'c3'], column_html='c4')
    with pytest.raises(ValueError):
        up.javascript.parallel_coordinates_table(
            data=[x, y, z], name=['c1', 'c2', 'c3'], column_html=['c1', 'c4'])

    # column_hidden
    up.javascript.parallel_coordinates_table(
        data=[x, y, z], name=['c1', 'c2', 'c3'], column_hidden='c1')
    up.javascript.parallel_coordinates_table(
        data=[x, y, z], name=['c1', 'c2', 'c3'], column_hidden=['c1', 'c3'])
    with pytest.raises(ValueError):
        up.javascript.parallel_coordinates_table(
            data=[x, y, z], name=['c1', 'c2', 'c3'], column_hidden='c4')
    with pytest.raises(ValueError):
        up.javascript.parallel_coordinates_table(
            data=[x, y, z], name=['c1', 'c2', 'c3'], column_hidden=['c1', 'c4'])

    # column_shown
    up.javascript.parallel_coordinates_table(
        data=[x, y, z], name=['c1', 'c2', 'c3'], column_shown='c1')
    up.javascript.parallel_coordinates_table(
        data=[x, y, z], name=['c1', 'c2', 'c3'], column_shown=['c1', 'c3'])
    with pytest.raises(ValueError):
        up.javascript.parallel_coordinates_table(
            data=[x, y, z], name=['c1', 'c2', 'c3'], column_shown='c4')
    with pytest.raises(ValueError):
        up.javascript.parallel_coordinates_table(
            data=[x, y, z], name=['c1', 'c2', 'c3'], column_shown=['c1', 'c4'])

    # Various visual properties
    up.javascript.parallel_coordinates_table(
        data=[x, y, z], name=['c1', 'c2', 'c3'], column_shown=['c1', 'c3'],
        show_menu=False, show_menu_toggle_button=False,
        parallel_coordinates_height=200, table_height=100,
        table_cell_width=40, table_cell_height=10,
        opacity=1, line_width=0.3, smoothness=0.2,
        color='c3', colormap='rainbow', colormap_reversed=True)
    with pytest.raises(ValueError):
        up.javascript.parallel_coordinates_table(data=[x, y, z], colormap='nonsense')
    with pytest.raises(ValueError):
        up.javascript.parallel_coordinates_table(data=[x, y, z], color='nonsense')

    # Colormaps
    d3_colormaps = [
        'Blues', 'Greens', 'Greys', 'Oranges', 'Purples', 'Reds', 'Turbo', 'Viridis', 'Inferno',
        'Magma', 'Plasma', 'Cividis', 'Warm', 'Cool', 'Cubehelix', 'BuGn', 'BuPu', 'GnBu', 'OrRd',
        'PuBuGn', 'PuBu', 'PuRd', 'RdPu', 'YlGnBu', 'YlGn', 'YlOrBr', 'YlOrRd', 'BrBG', 'PRGn',
        'PiYG', 'PuOr', 'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral', 'Rainbow', 'Sinebow']
    for cm in d3_colormaps:
        up.javascript.parallel_coordinates_table(data=[x, y, z], colormap=cm)
        up.javascript.parallel_coordinates_table(data=[x, y, z], colormap=cm.lower())


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_table_export(my_outdir, name, x, y, z):
    fig = up.javascript.table(data=[x, y, z])
    filepath = create_output_filepath(my_outdir, 'table_' + name)
    export_all_available_formats(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_table_parameters(name, x, y, z):
    # default
    up.javascript.table([x, y, z])
    up.javascript.table(data=[x, y, z])
    with pytest.raises(ValueError):
        up.javascript.table([x, y+[42], z])
    with pytest.raises(ValueError):
        up.javascript.table(data=[x, y+[42], z])

    # Pandas dataframe
    df = pd.DataFrame({'x': x, 'y': y, 'z': z})
    up.javascript.table(df)
    up.javascript.table(data=df)
    with pytest.raises(ValueError):
        df.x = list(df.x) + [42]
        up.javascript.table(df)

    # different data types
    up.javascript.table(data=[[1, 2, 3]])
    up.javascript.table(data=[['a', 'b', 'c']])
    up.javascript.table(data=[[1, 2, 3], ['a', 'b', 'c']])
    up.javascript.table(data=[['a', 'b', 'c'], [1, 2, 3]])
    up.javascript.table(data=[['a', 'b', 'c'], [1, 2, 3], ['d', 'e', 'f']])

    # name
    up.javascript.table(data=[x, y, z], name=['c1'])
    up.javascript.table(data=[x, y, z], name=['c1', 'c2', 'c3'])
    up.javascript.table(data=[x, y, z], name=['c1', 'c2', 'c3', 'c4'])

    # column_html
    up.javascript.table(
        data=[x, y, z], name=['c1', 'c2', 'c3'], column_html='c1')
    up.javascript.table(
        data=[x, y, z], name=['c1', 'c2', 'c3'], column_html=['c1', 'c3'])
    with pytest.raises(ValueError):
        up.javascript.table(
            data=[x, y, z], name=['c1', 'c2', 'c3'], column_html='c4')
    with pytest.raises(ValueError):
        up.javascript.table(
            data=[x, y, z], name=['c1', 'c2', 'c3'], column_html=['c1', 'c4'])

    # Various visual properties
    up.javascript.table(
        data=[x, y, z], name=['c1', 'c2', 'c3'],
        table_height=100, table_cell_width=40, table_cell_height=10)


# Network plots

def test_network_format_single_jgf(my_outdir):
    single_jgf_string = """{
        "graph": {
            "label": "JGF example",
            "nodes": [{"id": 0}, {"id": 1}],
            "edges": [{"source": 0, "target": 1}, {"source": 0, "target": 1}]
        }
    }"""
    single_jgf_object = {
        'graph': {
            'label': 'JGF example',
            'nodes': [{'id': 0}, {'id': 1}],
            'edges': [{'source': 0, 'target': 1}, {'source': 0, 'target': 1}],
        }
    }

    data = single_jgf_string
    fig = up.javascript.network_d3(data)
    filepath = create_output_filepath(my_outdir, 'network_format_single_jgf_str_d3')
    export_all_available_formats(fig, filepath)

    data = single_jgf_object
    fig = up.javascript.network_d3(data)
    filepath = create_output_filepath(my_outdir, 'network_format_single_jgf_obj_d3')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_vis(data)
    filepath = create_output_filepath(my_outdir, 'network_format_single_jgf_vis')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_webgl(data)
    filepath = create_output_filepath(my_outdir, 'network_format_single_jgf_webgl')
    export_all_available_formats(fig, filepath)


def test_network_format_single_jgf_from_file(my_outdir):
    data = os.path.join(IN_DIR, 'jgf_graph_single.json')
    fig = up.javascript.network_d3(data)
    filepath = create_output_filepath(my_outdir, 'network_format_single_jgf_file_d3')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_vis(data)
    filepath = create_output_filepath(my_outdir, 'network_format_single_jgf_file_vis')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_webgl(data)
    filepath = create_output_filepath(my_outdir, 'network_format_single_jgf_file_webgl')
    export_all_available_formats(fig, filepath)


def test_network_format_single_graph(my_outdir):
    data = TESTDATA_NETWORKX['undirected']
    fig = up.javascript.network_d3(data)
    filepath = create_output_filepath(my_outdir, 'network_format_single_nx_graph_d3')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_vis(data)
    filepath = create_output_filepath(my_outdir, 'network_format_single_nx_graph_vis')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_webgl(data)
    filepath = create_output_filepath(my_outdir, 'network_format_single_nx_graph_webgl')
    export_all_available_formats(fig, filepath)


def test_network_format_multiple_jgf(my_outdir):
    multiple_jgf = {
        'graphs': [
            {
                'nodes': [{'id': 0}, {'id': 1}],
                'edges': [{'source': 0, 'target': 1}, {'source': 0, 'target': 1}],
            },
            {
                'nodes': [{'id': 0}, {'id': 1}, {'id': 2}],
                'edges': [{'source': 0, 'target': 1}, {'source': 0, 'target': 2}],
            },
            '{"graph": {"label": "JGF example","nodes": [{"id": 0}, {"id": 1}],"edges": [{"source": 0, "target": 1}, {"source": 0, "target": 1}]}}',
            {
                'nodes': [{'id': 0}, {'id': 1}, {'id': 2}, {'id': 3}],
                'edges': [{'source': 0, 'target': 1}, {'source': 0, 'target': 3}],
            },
            """{
        "graph": {
            "label": "JGF example",
            "nodes": [{"id": 0}, {"id": 1}],
            "edges": [{"source": 0, "target": 1}, {"source": 0, "target": 1}]
        }
    }"""
        ]
    }
    data = multiple_jgf
    fig = up.javascript.network_d3(data)
    filepath = create_output_filepath(my_outdir, 'network_format_multiple_jgf_d3')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_vis(data)
    filepath = create_output_filepath(my_outdir, 'network_format_multiple_jgf_vis')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_webgl(data)
    filepath = create_output_filepath(my_outdir, 'network_format_multiple_jgf_webgl')
    export_all_available_formats(fig, filepath)


def test_network_format_multiple_jgf_from_file(my_outdir):
    data = os.path.join(IN_DIR, 'jgf_graph_multiple.json')
    fig = up.javascript.network_d3(data)
    filepath = create_output_filepath(my_outdir, 'network_format_multiple_jgf_file_d3')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_vis(data)
    filepath = create_output_filepath(my_outdir, 'network_format_multiple_jgf_file_vis')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_webgl(data)
    filepath = create_output_filepath(my_outdir, 'network_format_multiple_jgf_file_webgl')
    export_all_available_formats(fig, filepath)


@pytest.mark.only_with_graph_libraries
def test_network_format_multiple_graph_and_jgf(my_outdir):
    jgf_graph_empty = {
        'graph': {
            'label': 'Empty JGF',
            'nodes': [],
            'edges': [],
        }
    }
    jgf_graph_one_node = {
        'graph': {
            'label': 'JGF with 1 node',
            'nodes': [{'id': 0}],
            'edges': [],
        }
    }
    jgf_graph_two_nodes = {
        'graph': {
            'label': 'JGF with 2 nodes',
            'nodes': [{'id': 0}, {'id': 1}],
            'edges': [],
        }
    }
    jgf_graph_two_nodes_and_multiedge = {
        'graph': {
            'label': 'JGF with 2 nodes and 2 undirected edges (multiedge)',
            'nodes': [{'id': 0}, {'id': 1}],
            'edges': [{'source': 0, 'target': 1}, {'source': 0, 'target': 1}],
        }
    }
    data = [
        jgf_graph_empty,
        jgf_graph_one_node,
        jgf_graph_two_nodes,
        jgf_graph_two_nodes_and_multiedge,
        TESTDATA_JGF['undirected attributed'],
        TESTDATA_JGF['directed attributed'],
        TESTDATA_GRAPH_TOOL['undirected attributed'],
        TESTDATA_GRAPH_TOOL['directed attributed'],
        TESTDATA_IGRAPH['undirected attributed'],
        TESTDATA_IGRAPH['directed attributed'],
        TESTDATA_NETWORKIT['undirected'],
        TESTDATA_NETWORKIT['directed'],
        TESTDATA_NETWORKX['undirected attributed'],
        TESTDATA_NETWORKX['directed attributed'],
        TESTDATA_PYNTACLE['undirected attributed'],
        TESTDATA_PYNTACLE['directed attributed'],
        TESTDATA_SNAP['undirected'],
        TESTDATA_SNAP['directed'],
    ]
    fig = up.javascript.network_d3(data)
    filepath = create_output_filepath(my_outdir, 'network_format_multiple_graph_and_jgf_d3')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_vis(data)
    filepath = create_output_filepath(my_outdir, 'network_format_multiple_graph_and_jgf_vis')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_webgl(data)
    filepath = create_output_filepath(my_outdir, 'network_format_multiple_graph_and_jgf_webgl')
    export_all_available_formats(fig, filepath)


def test_network_format_fail_on_invalid_data():
    def d3_fails(data):
        with pytest.raises(ValueError):
            up.javascript.network_d3(data)

    def vis_fails(data):
        with pytest.raises(ValueError):
            up.javascript.network_vis(data)

    def webgl_fails(data):
        with pytest.raises(ValueError):
            up.javascript.network_webgl(data)

    jgf_graph = {
        'graph': {
            'nodes': [{'id': 0}],
            'edges': [],
        }
    }

    for nonsense_item in [1, 'a', None, [], [1], ['a'], {}, {'a': 1}, {1: 'a'}]:
        data = nonsense_item
        d3_fails(data)
        vis_fails(data)
        webgl_fails(data)

        data = [nonsense_item, nonsense_item, nonsense_item]
        d3_fails(data)
        vis_fails(data)
        webgl_fails(data)

        data = [jgf_graph, nonsense_item]
        d3_fails(data)
        vis_fails(data)
        webgl_fails(data)

        data = [nonsense_item, jgf_graph]
        d3_fails(data)
        vis_fails(data)
        webgl_fails(data)


@pytest.mark.only_with_graph_libraries
def test_network_library_conversion_and_result_equivalence(my_outdir):
    if TESTDATA_GRAPH_TOOL is None:
        raise ValueError('Data generation with graph-tool failed. Is the package installed?')
    if TESTDATA_IGRAPH is None:
        raise ValueError('Data generation with igraph failed. Is the package installed?')
    if TESTDATA_NETWORKIT is None:  # no attributes
        raise ValueError('Data generation with NetworKit failed. Is the package installed?')
    if TESTDATA_NETWORKX is None:
        raise ValueError('Data generation with NetworkX failed. Is the package installed?')
    if TESTDATA_PYNTACLE is None:  # igraph
        raise ValueError('Data generation with Pyntacle failed. Is the package installed?')
    if TESTDATA_SNAP is None:  # only directed can have attributes, no graph attributes
        raise ValueError('Data generation with SNAP failed. Is the package installed?')

    # undirected graphs
    jgf_gt = format_conversion.graphtool_to_jgf(TESTDATA_GRAPH_TOOL['undirected'])
    jgf_ig = format_conversion.igraph_to_jgf(TESTDATA_IGRAPH['undirected'])
    jgf_nk = format_conversion.networkit_to_jgf(TESTDATA_NETWORKIT['undirected'])
    jgf_nx = format_conversion.networkx_to_jgf(TESTDATA_NETWORKX['undirected'])
    jgf_pn = format_conversion.pyntacle_to_jgf(TESTDATA_PYNTACLE['undirected'])
    jgf_sn = format_conversion.snap_to_jgf(TESTDATA_SNAP['undirected'])
    # assert jgf_gt == jgf_ig == jgf_nk == jgf_nx == jgf_pn == jgf_sn  # source/target arbitrary

    fig = up.javascript.network_d3(jgf_gt)
    filepath = create_output_filepath(my_outdir, 'network_graphtool_d3_undirected')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(jgf_ig)
    filepath = create_output_filepath(my_outdir, 'network_igraph_d3_undirected')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(jgf_nk)
    filepath = create_output_filepath(my_outdir, 'network_networkit_d3_undirected')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(jgf_nx)
    filepath = create_output_filepath(my_outdir, 'network_networkx_d3_undirected')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(jgf_pn)
    filepath = create_output_filepath(my_outdir, 'network_pyntacle_d3_undirected')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(jgf_sn)
    filepath = create_output_filepath(my_outdir, 'network_snap_d3_undirected')
    export_all_available_formats(fig, filepath)

    # directed graphs
    jgf_gt = format_conversion.graphtool_to_jgf(TESTDATA_GRAPH_TOOL['directed'])
    jgf_ig = format_conversion.igraph_to_jgf(TESTDATA_IGRAPH['directed'])
    jgf_nk = format_conversion.networkit_to_jgf(TESTDATA_NETWORKIT['directed'])
    jgf_nx = format_conversion.networkx_to_jgf(TESTDATA_NETWORKX['directed'])
    jgf_pn = format_conversion.pyntacle_to_jgf(TESTDATA_PYNTACLE['directed'])
    jgf_sn = format_conversion.snap_to_jgf(TESTDATA_SNAP['directed'])
    assert jgf_gt == jgf_ig == jgf_nk == jgf_nx == jgf_pn == jgf_sn

    fig = up.javascript.network_d3(jgf_gt)
    filepath = create_output_filepath(my_outdir, 'network_graphtool_d3_directed')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(jgf_ig)
    filepath = create_output_filepath(my_outdir, 'network_igraph_d3_directed')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(jgf_nk)
    filepath = create_output_filepath(my_outdir, 'network_networkit_d3_directed')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(jgf_nx)
    filepath = create_output_filepath(my_outdir, 'network_networkx_d3_directed')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(jgf_pn)
    filepath = create_output_filepath(my_outdir, 'network_pyntacle_d3_directed')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(jgf_sn)
    filepath = create_output_filepath(my_outdir, 'network_snap_d3_directed')
    export_all_available_formats(fig, filepath)

    # undirected graphs with attributes
    jgf_gt = format_conversion.graphtool_to_jgf(TESTDATA_GRAPH_TOOL['undirected attributed'])
    jgf_ig = format_conversion.igraph_to_jgf(TESTDATA_IGRAPH['undirected attributed'])
    jgf_nx = format_conversion.networkx_to_jgf(TESTDATA_NETWORKX['undirected attributed'])
    jgf_pn = format_conversion.pyntacle_to_jgf(TESTDATA_PYNTACLE['undirected attributed'])
    # assert jgf_gt == jgf_ig == jgf_nx == jgf_pn  # source/target arbitrary

    fig = up.javascript.network_d3(jgf_gt)
    filepath = create_output_filepath(my_outdir, 'network_graphtool_d3_undirected_attributed')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(jgf_ig)
    filepath = create_output_filepath(my_outdir, 'network_igraph_d3_undirected_attributed')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(jgf_nx)
    filepath = create_output_filepath(my_outdir, 'network_networkx_d3_undirected_attributed')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(jgf_pn)
    filepath = create_output_filepath(my_outdir, 'network_pyntacle_d3_undirected_attributed')
    export_all_available_formats(fig, filepath)

    # directed graphs with attributes
    jgf_gt = format_conversion.graphtool_to_jgf(TESTDATA_GRAPH_TOOL['directed attributed'])
    jgf_ig = format_conversion.igraph_to_jgf(TESTDATA_IGRAPH['directed attributed'])
    jgf_nx = format_conversion.networkx_to_jgf(TESTDATA_NETWORKX['directed attributed'])
    jgf_pn = format_conversion.pyntacle_to_jgf(TESTDATA_PYNTACLE['directed attributed'])
    jgf_sn = format_conversion.snap_to_jgf(TESTDATA_SNAP['directed attributed'])
    assert jgf_gt == jgf_ig == jgf_nx == jgf_pn  # jgf_sn does not have graph properties

    fig = up.javascript.network_d3(jgf_gt)
    filepath = create_output_filepath(my_outdir, 'network_graphtool_d3_directed_attributed')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(jgf_ig)
    filepath = create_output_filepath(my_outdir, 'network_igraph_d3_directed_attributed')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(jgf_nx)
    filepath = create_output_filepath(my_outdir, 'network_networkx_d3_directed_attributed')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(jgf_pn)
    filepath = create_output_filepath(my_outdir, 'network_pyntacle_d3_directed_attributed')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(jgf_sn)
    filepath = create_output_filepath(my_outdir, 'network_snap_d3_directed_attributed')
    export_all_available_formats(fig, filepath)


@pytest.mark.only_with_graph_libraries
def test_network_library_networkit_with_metadata_via_list_with_dicts(my_outdir):
    if TESTDATA_NETWORKIT is None:  # no attributes
        raise ValueError('Data generation with NetworKit failed. Is the package installed?')

    graph = TESTDATA_NETWORKIT['undirected']
    graph_metadata = {'background_color': 'gray', 'node_color': 'red', 'edge_color': 'blue'}

    node_metadata = {}

    def parse_node(node):
        node_metadata[node] = {'size': 50, 'opacity': 0.5}
    graph.forNodes(parse_node)

    edge_metadata = {}

    def parse_edge(s, t, ea, eb):
        edge_metadata['({}, {})'.format(s, t)] = {'size': 10}
    graph.forEdges(parse_edge)

    d0 = graph
    d1 = [graph, graph_metadata]
    d2 = [graph, graph_metadata, node_metadata]
    d3 = [graph, graph_metadata, node_metadata, edge_metadata]

    fig = up.javascript.network_d3(d0)
    filepath = create_output_filepath(my_outdir, 'network_networkit_d3_extra_data_0')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(d1)
    filepath = create_output_filepath(my_outdir, 'network_networkit_d3_extra_data_1')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(d2)
    filepath = create_output_filepath(my_outdir, 'network_networkit_d3_extra_data_2')
    export_all_available_formats(fig, filepath)

    fig = up.javascript.network_d3(d3)
    filepath = create_output_filepath(my_outdir, 'network_networkit_d3_extra_data_3')
    export_all_available_formats(fig, filepath)


def test_network_each_keyword_argument(my_outdir):
    # Note: All outputs were inspected manually, all bugs were resolved and all shortcomings
    # documented in the docstrings. This becomes necessary again in case of major code changes
    # and can hardly be automated (with reasonable effort).
    data_undirected = {
        "graph": {
            "label": "a graph",
            "metadata": {
                "arrow_color": "green",
                "arrow_size": 10,
                "background_color": "#ffe",
                "node_shape": "hexagon",
                "node_size": 60,
                "node_color": "gray",
                "node_opacity": 1.0,
                "node_hover": "hovered node",
                "node_click": "clicked node",
                "edge_size": 1,
                "edge_color": "magenta",
                "edge_opacity": 1.0,
                "edge_hover": "hovered edge",
                "edge_click": "clicked edge",
            },
            "nodes": [
                {"id": 1, "label": "node a", "metadata": {"size": 20, "shape": "circle"}},
                {"id": 2, "label": "node b", "metadata": {"size": 30, "shape": "rectangle",
                 "color": "red", "opacity": 0.5, "x": -100.0, "y": 10.0}},
                {"id": 3},
                {"id": 4, "label": "node d", "metadata": {"size": 5,
                 "color": "green", "opacity": 0.25, "x": 100.0, "y": 80.0}},
                {"id": 5, "label": "node e", "metadata": {"shape": "hexagon",
                 "color": "blue", "opacity": 0.1, "x": 50.0, "y": 80.0}},
                {"id": 6, "metadata": {"image": "data:image/png;base64,{}".format(
                    base64.file_to_base64_text(os.path.join(IN_DIR, 'rectangle_30x10.png')))}},
                {"id": 7, "metadata": {"image": "data:image/png;base64,{}".format(
                    base64.file_to_base64_text(os.path.join(IN_DIR, 'rectangle_10x10.png')))}},
            ],
            "edges": [
                {"source": 1, "target": 2},
                {"source": 1, "target": 2, "metadata": {"size": 1, "color": "black"}},
                {"source": 1, "target": 2, "metadata": {"size": 1, "color": "gray"}},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 3, "target": 3, "metadata": {"color": "blue"}},
                {"source": 3, "target": 3,
                 "metadata": {"color": "orange", "size": 3, "opacity": 0.2}},
                {"source": 4, "target": 1, "metadata": {"opacity": 0.5}},
                {"source": 1, "target": 5},
                {"source": 2, "target": 6},
                {"source": 6, "target": 7},
            ]
        }
    }
    data_directed = deepcopy(data_undirected)
    data_directed['graph']['directed'] = True

    def create_d3_plot(directed, key, val):
        base_name = 'network_kwarg_{}_{}_{}_{}'
        fig = up.javascript.network_d3(data, **{key: val})
        filename = base_name.format(str(key), str(val), directed, 'd3')
        filepath = create_output_filepath(my_outdir, filename)
        export_all_available_formats(fig, filepath)

    def create_webgl_plot(directed, key, val):
        base_name = 'network_kwarg_{}_{}_{}_{}'
        fig = up.javascript.network_webgl(data, **{key: val})
        filename = base_name.format(str(key), str(val), directed, 'webgl')
        filepath = create_output_filepath(my_outdir, filename)
        export_all_available_formats(fig, filepath)

    def create_vis_plot(directed, key, val):
        base_name = 'network_kwarg_{}_{}_{}_{}'
        fig = up.javascript.network_vis(data, **{key: val})
        filename = base_name.format(str(key), str(val), directed, 'vis')
        filepath = create_output_filepath(my_outdir, filename)
        export_all_available_formats(fig, filepath)

    kwargs_all = dict(
        network_height=40,
        details_height=40,
        show_details=True,
        show_menu=False,
        show_node=False,
        node_size_factor=2.0,
        node_size_data_source='label_size',
        use_node_size_normalization=True,
        node_size_normalization_min=1.0,
        node_size_normalization_max=200.0,
        node_drag_fix=True,
        node_hover_neighborhood=True,
        node_hover_tooltip=False,
        show_node_image=False,
        node_image_size_factor=2.0,
        show_node_label=False,
        show_node_label_border=False,
        node_label_data_source='size',
        node_label_size_factor=2.0,
        node_label_rotation=30,
        node_label_font='mono',
        show_edge=False,
        edge_size_factor=5.0,
        edge_size_data_source='label_size',
        use_edge_size_normalization=True,
        edge_size_normalization_min=2.0,
        edge_size_normalization_max=20.0,
        edge_curvature=-1.2,
        edge_hover_tooltip=False,
        show_edge_label=True,
        show_edge_label_border=False,
        edge_label_data_source='size',
        edge_label_size_factor=5.0,
        edge_label_rotation=30.0,
        edge_label_font='mono',
        zoom_factor=3.0,
        large_network_threshold=2,
        layout_algorithm_active=False,
    )

    kwargs_d3_specific = dict(
        use_many_body_force=False,
        many_body_force_strength=-500.0,
        many_body_force_theta=0.01,
        use_many_body_force_min_distance=True,
        many_body_force_min_distance=1000.0,
        use_many_body_force_max_distance=True,
        many_body_force_max_distance=10.0,
        use_links_force=False,
        links_force_distance=500.0,
        links_force_strength=1.0,
        use_collision_force=True,
        collision_force_radius=10.0,
        collision_force_strength=0.01,
        use_x_positioning_force=True,
        x_positioning_force_strength=1.0,
        use_y_positioning_force=True,
        y_positioning_force_strength=1.0,
        use_centering_force=False,
    )

    kwargs_webgl_specific = dict(
        use_many_body_force=False,
        many_body_force_strength=-500.0,
        many_body_force_theta=0.01,
        use_many_body_force_min_distance=True,
        many_body_force_min_distance=1000.0,
        use_many_body_force_max_distance=True,
        many_body_force_max_distance=10.0,
        use_links_force=False,
        links_force_distance=500.0,
        links_force_strength=1.0,
        use_x_positioning_force=True,
        x_positioning_force_strength=1.0,
        use_y_positioning_force=True,
        y_positioning_force_strength=1.0,
        use_centering_force=False,
        z_positioning_force_strength=1.0,
        use_z_positioning_force=True,
    )

    kwargs_vis_specific = dict(
        layout_algorithm='forceAtlas2Based',
        gravitational_constant=-100000.0,
        central_gravity=10.0,
        spring_length=300.0,
        spring_constant=0.2,
        avoid_overlap=0.0
    )

    for directed, data in zip(['directed', 'undirected'], [data_directed, data_undirected]):
        for key, val in kwargs_all.items():
            create_d3_plot(directed, key, val)
            create_webgl_plot(directed, key, val)
            create_vis_plot(directed, key, val)
        for key, val in kwargs_d3_specific.items():
            create_d3_plot(directed, key, val)
        for key, val in kwargs_webgl_specific.items():
            create_webgl_plot(directed, key, val)
        for key, val in kwargs_vis_specific.items():
            create_vis_plot(directed, key, val)


def test_network_each_data_property(my_outdir):
    # Note: All outputs were inspected manually, all bugs were resolved and all shortcomings
    # documented in the docstrings and below here. This becomes necessary again in case of
    # major code changes and can hardly be automated (with reasonable effort).
    """
1. **graph metadata**
  - arrow_color: d3, vis FAILS (not supported), webgl
  - arrow_size: d3, vis, webgl
  - background_color: d3, vis, webgl
  - node_color: d3, vis, webgl
  - node_opacity: d3, vis FAILS (not supported), webgl
  - node_size: d3, vis, webgl
  - node_shape: d3, vis (if no image), webgl
  - node_border_color: d3, vis, webgl FAILS (no border used)
  - node_border_size: d3, vis, webgl FAILS (no border used)
  - node_label_color: d3, vis, webgl
  - node_label_size: d3, vis, webgl
  - node_hover: d3, vis, webgl
  - node_click: d3, vis, webgl
  - node_image: d3, vis, webgl
  - node_x: d3, vis, webgl
  - node_y: d3, vis, webgl
  - node_z: webgl
  - edge_color: d3, vis, webgl
  - edge_opacity: d3, vis FAILS (not supported), webgl
  - edge_size: d3, vis, webgl
  - edge_label_color: d3, vis, webgl FAILS (no labels used)
  - edge_label_size: d3, vis, webgl FAILS (no labels used)
  - edge_hover: d3, vis, webgl
  - edge_click: d3, vis, webgl

2. **node metadata**
  - color: d3, vis, webgl
  - opacity: d3, vis FAILS (not supported), webgl
  - size: d3, vis, webgl
  - shape: d3, vis (if no image), webgl
  - border_color: d3, vis, webgl FAILS (no border used)
  - border_size: d3, vis, webgl FAILS (no border used)
  - label_color: d3, vis, webgl
  - label_size: d3, vis, webgl
  - hover: d3, vis, webgl
  - click: d3, vis, webgl
  - image: d3, vis, webgl
  - x: d3, vis, webgl
  - y: d3, vis, webgl
  - z: webgl

3. **edge metadata**
  - color: d3, vis, webgl
  - opacity: d3, vis FAILS (not supported), webgl
  - size: d3, vis, webgl
  - label_color: d3, vis, webgl FAILS (no labels)
  - label_size: d3, vis, webgl FAILS (no labels)
  - hover: d3, vis, webgl
  - click: d3, vis, webgl
"""

    plotting_functions = [
        ('d3', up.javascript.network_d3),
        ('vis', up.javascript.network_vis),
        ('webgl', up.javascript.network_webgl),
    ]
    base_name = 'network_darg_{}_{}'

    # all in one
    base_distance = 50.0
    data = {
        "graph": {
            "directed": True,
            "metadata": {
              "arrow_color": "yellow",
              "arrow_size": 30,
              "background_color": "lightgray",
              "node_color": "red",
              "node_opacity": 0.1,
              "node_size": 15,
              "node_shape": "hexagon",
              "node_border_color": "#fff",
              "node_border_size": 7,
              "node_label_color": "orange",
              "node_label_size": 5,
              "node_hover": "General node hover",
              "node_click": "General node click",
              "node_image": "data:image/png;base64,{}".format(
                  base64.file_to_base64_text(os.path.join(IN_DIR, 'rectangle_10x10.png'))),
              "node_x": 0.0,
              "node_y": 0.0,
              "node_z": 0.0,
              "edge_color": "blue",
              "edge_opacity": 0.2,
              "edge_size": 4,
              "edge_label_color": "blue",
              "edge_label_size": 5,
              "edge_hover": "General edge hover",
              "edge_click": "General edge click",
            },
            "nodes": [
                {"id": 1, "label": "Node 1 special label", "metadata": {
                   "color": "#ff00ff",
                   "opacity": 0.75,
                   "size": 30,
                   "shape": "rectangle",
                   "border_color": "#aa00aa",
                   "border_size": 2,
                   "label_color": "#ff00ff",
                   "label_size": 30,
                   "hover": "Node $id special <span style='color:red'>hover</span> with HTML",
                   "click": "Node $id special <span style='color:orange'>click</span> with HTML",
                   "image": "data:image/png;base64,{}".format(
                       base64.file_to_base64_text(os.path.join(IN_DIR, 'rectangle_30x10.png'))),
                   "x": base_distance,
                   "y": base_distance * 2,
                   "z": base_distance,
                }},
                {"id": 2, "label": "node b", "metadata": {
                  "shape": "circle",
                  "size": 40,
                  "image": "data:image/png;base64,{}".format(
                       base64.file_to_base64_text(os.path.join(IN_DIR, 'rectangle_30x10.png'))),
                  "x": base_distance * 2,
                  "y": base_distance / 2,
                }},
                {"id": 3},
                {"id": 4, "label": "node d", "metadata": {
                  "size": 70,
                  "x": base_distance * 4,
                  "y": base_distance,
                }},
                {"id": 5, "label": "node e", "metadata": {
                  "shape": "hexagon",
                  "image": "data:image/png;base64,{}".format(
                       base64.file_to_base64_text(os.path.join(IN_DIR, 'rectangle_10x30.png'))),
                  "x": base_distance * 5,
                  "y": base_distance * 3,
                }},
            ],
            "edges": [
                {"source": 1, "target": 2, "label": "Edge 1 special label", "metadata": {
                  "color": "#ff00ff",
                  "opacity": 0.75,
                  "size": 1,
                  "label_color": "#ff00ff",
                  "label_size": 30,
                  "hover": "Edge $id special <span style='color:blue'>hover</span> with HTML",
                  "click": "Edge $id special <span style='color:green'>click</span> with HTML",
                }},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data, show_edge_label=True)
        filepath = create_output_filepath(my_outdir, base_name.format('all', func_name))
        export_all_available_formats(fig, filepath)

    # background
    data = {
        "graph": {
            "directed": True,
            "metadata": {"background_color": "lightgray"},
            "nodes": [
                {"id": 1, "label": "node a", "metadata": {"size": 30}},
                {"id": 2, "label": "node b", "metadata": {"size": 40}},
                {"id": 3},
                {"id": 4, "label": "node d", "metadata": {"size": 4}},
                {"id": 5, "label": "node e", "metadata": {"shape": "hexagon"}},
            ],
            "edges": [
                {"source": 1, "target": 2},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = create_output_filepath(my_outdir, base_name.format('background', func_name))
        export_all_available_formats(fig, filepath)

    # node label
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1, "label": "node a", "metadata": {"size": 30}},
                {"id": 2, "label": "node b", "metadata": {"size": 40}},
                {"id": 3},
                {"id": 4, "label": "node d", "metadata": {"size": 4}},
                {"id": 5, "label": "node e", "metadata": {"shape": "hexagon"}},
            ],
            "edges": [
                {"source": 1, "target": 2},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = create_output_filepath(my_outdir, base_name.format('node_label', func_name))
        export_all_available_formats(fig, filepath)

    # node and edge label
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1, "label": "node a"},
                {"id": 2, "label": "node b"},
                {"id": 3},
                {"id": 4, "label": "node d"},
                {"id": 5, "label": "node e"},
            ],
            "edges": [
                {"source": 1, "target": 2, "label": "e12"},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4, "label": "e34"},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = create_output_filepath(
            my_outdir, base_name.format('node_label_and_edge_label', func_name))
        export_all_available_formats(fig, filepath)

    # node color
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1, "metadata": {"color": "#f00"}},
                {"id": 2, "metadata": {"color": "green"}},
                {"id": 3},
                {"id": 4, "metadata": {"color": "#0000ff"}},
                {"id": 5, "metadata": {"color": "WRONG"}},
            ],
            "edges": [
                {"source": 1, "target": 2},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = create_output_filepath(my_outdir, base_name.format('node_color', func_name))
        export_all_available_formats(fig, filepath)

    # node opacity
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1, "metadata": {"opacity": 0.1}},
                {"id": 2, "metadata": {"opacity": 0.5}},
                {"id": 3},
                {"id": 4, "metadata": {"opacity": 1.0}},
                {"id": 5, "metadata": {"opacity": "WRONG"}},
            ],
            "edges": [
                {"source": 1, "target": 2},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = create_output_filepath(my_outdir, base_name.format('node_opacity', func_name))
        export_all_available_formats(fig, filepath)

    # node size
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1, "metadata": {"size": 20}},
                {"id": 2, "metadata": {"size": 30}},
                {"id": 3},
                {"id": 4, "metadata": {"size": 4}},
                {"id": 5, "metadata": {"size": "WRONG"}},
            ],
            "edges": [
                {"source": 1, "target": 2},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = create_output_filepath(my_outdir, base_name.format('node_size', func_name))
        export_all_available_formats(fig, filepath)

    # node shape
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1, "metadata": {"shape": "circle"}},
                {"id": 2, "metadata": {"shape": "rectangle"}},
                {"id": 3},
                {"id": 4, "metadata": {"shape": "hexagon"}},
                {"id": 5, "metadata": {"shape": "WRONG"}},
            ],
            "edges": [
                {"source": 1, "target": 2},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = create_output_filepath(my_outdir, base_name.format('node_shape', func_name))
        export_all_available_formats(fig, filepath)

    # node border color and border size
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1,
                 "metadata": {"shape": "hexagon", "border_color": "red", "border_size": 3}},
                {"id": 2,
                 "metadata": {"shape": "circle", "border_color": "green", "border_size": 3}},
                {"id": 3,
                 "metadata": {"border_color": "green", "border_size": 3}},
                {"id": 4,
                 "metadata": {"shape": "rectangle", "border_color": "blue", "border_size": 3}},
                {"id": 5,
                 "metadata": {"border_color": "WRONG", "border_size": "WRONG"}},
                {"id": 6},
            ],
            "edges": [
                {"source": 1, "target": 2},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
                {"source": 1, "target": 6},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = create_output_filepath(
            my_outdir, base_name.format('node_border_color_and_size', func_name))
        export_all_available_formats(fig, filepath)

    # node image
    png10x10 = base64.file_to_base64_text(os.path.join(IN_DIR, 'rectangle_10x10.png'))
    png30x10 = base64.file_to_base64_text(os.path.join(IN_DIR, 'rectangle_30x10.png'))
    png10x30 = base64.file_to_base64_text(os.path.join(IN_DIR, 'rectangle_10x30.png'))
    png100x50 = base64.file_to_base64_text(os.path.join(IN_DIR, 'rectangle_100x50.png'))
    svg10x10 = base64.file_to_base64_text(os.path.join(IN_DIR, 'rectangle_10x10.svg'))
    svg30x10 = base64.file_to_base64_text(os.path.join(IN_DIR, 'rectangle_30x10.svg'))
    svg10x30 = base64.file_to_base64_text(os.path.join(IN_DIR, 'rectangle_10x30.svg'))
    svg100x50 = base64.file_to_base64_text(os.path.join(IN_DIR, 'rectangle_100x50.svg'))
    png_prefix = 'data:image/png;base64,'
    svg_prefix = 'data:image/svg+xml;base64,'

    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1, "metadata": {"shape": "circle", "image": png_prefix+png10x10}},
                {"id": 2, "metadata": {"shape": "rectangle", "image": png_prefix+png10x10}},
                {"id": 3, "metadata": {"shape": "hexagon", "image": png_prefix+png10x10}},
                {"id": 4, "metadata": {"shape": "circle", "image": png_prefix+png30x10}},
                {"id": 5, "metadata": {"shape": "rectangle", "image": png_prefix+png30x10}},
                {"id": 6, "metadata": {"shape": "hexagon", "image": png_prefix+png30x10}},
                {"id": 7, "metadata": {"shape": "circle", "image": png_prefix+png10x30}},
                {"id": 8, "metadata": {"shape": "rectangle", "image": png_prefix+png10x30}},
                {"id": 9, "metadata": {"shape": "hexagon", "image": png_prefix+png10x30}},
                {"id": 10, "metadata": {"shape": "circle", "image": png_prefix+png100x50}},
                {"id": 11, "metadata": {"shape": "rectangle", "image": png_prefix+png100x50}},
                {"id": 12, "metadata": {"shape": "hexagon", "image": png_prefix+png100x50}},

                {"id": 13, "metadata": {"shape": "circle", "image": svg_prefix+svg10x10}},
                {"id": 14, "metadata": {"shape": "rectangle", "image": svg_prefix+svg10x10}},
                {"id": 15, "metadata": {"shape": "hexagon", "image": svg_prefix+svg10x10}},
                {"id": 16, "metadata": {"shape": "circle", "image": svg_prefix+svg30x10}},
                {"id": 17, "metadata": {"shape": "rectangle", "image": svg_prefix+svg30x10}},
                {"id": 18, "metadata": {"shape": "hexagon", "image": svg_prefix+svg30x10}},
                {"id": 19, "metadata": {"shape": "circle", "image": svg_prefix+svg10x30}},
                {"id": 20, "metadata": {"shape": "rectangle", "image": svg_prefix+svg10x30}},
                {"id": 21, "metadata": {"shape": "hexagon", "image": svg_prefix+svg10x30}},
                {"id": 22, "metadata": {"shape": "circle", "image": svg_prefix+svg100x50}},
                {"id": 23, "metadata": {"shape": "rectangle", "image": svg_prefix+svg100x50}},
                {"id": 24, "metadata": {"shape": "hexagon", "image": svg_prefix+svg100x50}},
                {"id": 25, "metadata": {"shape": "circle", "image": 'WRONG'}},
                {"id": 26, "metadata": {"shape": "rectangle", "image": 'WRONG'}},
                {"id": 27, "metadata": {"shape": "hexagon", "image": 'WRONG'}},
                {"id": 28, "metadata": {"image": 'WRONG'}},
                {"id": 29, "metadata": {"shape": "WRONG", "image": svg_prefix+svg30x10}},
            ],
            "edges": [
                {"source": 1, "target": 2},
                {"source": 2, "target": 3},
                {"source": 3, "target": 1},
                {"source": 1, "target": 13},

                {"source": 4, "target": 5},
                {"source": 5, "target": 6},
                {"source": 6, "target": 4},
                {"source": 4, "target": 16},

                {"source": 7, "target": 8},
                {"source": 8, "target": 9},
                {"source": 9, "target": 7},
                {"source": 7, "target": 19},

                {"source": 10, "target": 11},
                {"source": 11, "target": 12},
                {"source": 12, "target": 10},
                {"source": 10, "target": 22},

                {"source": 13, "target": 14},
                {"source": 14, "target": 15},
                {"source": 15, "target": 13},

                {"source": 16, "target": 17},
                {"source": 17, "target": 18},
                {"source": 18, "target": 16},

                {"source": 19, "target": 20},
                {"source": 20, "target": 21},
                {"source": 21, "target": 19},

                {"source": 22, "target": 23},
                {"source": 23, "target": 24},
                {"source": 24, "target": 22},

                {"source": 25, "target": 26},
                {"source": 26, "target": 27},
                {"source": 27, "target": 28},
                {"source": 28, "target": 29},
                {"source": 29, "target": 25},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = create_output_filepath(
            my_outdir, base_name.format('node_image_and_shape', func_name))
        export_all_available_formats(fig, filepath)

    # node and edge hover
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1, "metadata": {
                    "hover": ("Test node 1 hover which is an example of a long text that goes on"
                              + "   and on"*50
                              + "andon"*200)}},
                {"id": 2, "metadata": {"hover": "Test node 2 hover"}},
                {"id": 3},
                {"id": 4, "metadata": {"hover": "Test node 4 hover"}},
                {"id": 5},
            ],
            "edges": [
                {"source": 1, "target": 2, "metadata": {"hover": "Test edge (1,2) hover"}},
                {"source": 2, "target": 3, "metadata": {"hover": "Test edge (2,3) hover"}},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1, "metadata": {"hover": "Test edge (4,1) hover"}},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = create_output_filepath(
            my_outdir, base_name.format('node_and_edge_hover', func_name))
        export_all_available_formats(fig, filepath)

    # node and edge click
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1, "metadata": {"click": "Test node 1 click"}},
                {"id": 2, "metadata": {"click": "Test node 2 click"}},
                {"id": 3},
                {"id": 4, "metadata": {
                    "click": "Test node 4 click <ul><li>a: 1</li><li>e: 5</li></ul>"}},
                {"id": 5},
            ],
            "edges": [
                {"source": 1, "target": 2,
                 "metadata": {"click": "Test edge (1,2) click"}},
                {"source": 2, "target": 3,
                 "metadata": {"click": "Test edge (2,3) click"}},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1,
                 "metadata":
                 {"click": "Test edge (4,1) click <ul><li>a: 1</li><li>b: 2</li></ul>"}},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = create_output_filepath(
            my_outdir, base_name.format('node_and_edge_click', func_name))
        export_all_available_formats(fig, filepath)

    # ----------------------------------------------------------------------------------------
    # edge label
    for directed in [True, False]:
        data = {
            "graph": {
                "directed": directed,
                "nodes": [
                    {"id": 1},
                    {"id": 2},
                    {"id": 3},
                    {"id": 4},
                    {"id": 5},
                ],
                "edges": [
                    {"source": 1, "target": 2, "label": "e12"},
                    {"source": 2, "target": 3, "label": "e23"},
                    {"source": 3, "target": 4},
                    {"source": 4, "target": 1, "label": "e41"},
                    {"source": 1, "target": 5, "label": 42},
                ]
            }
        }
        for func_name, func in plotting_functions:
            fig = func(data)
            suffix = 'directed' if directed else 'undirected'
            filepath = create_output_filepath(
                my_outdir, base_name.format('edge_label_'+suffix, func_name))
            export_all_available_formats(fig, filepath)

    # edge color
    for directed in [True, False]:
        data = {
            "graph": {
                "directed": directed,
                "nodes": [
                    {"id": 1},
                    {"id": 2},
                    {"id": 3},
                    {"id": 4},
                    {"id": 5},
                ],
                "edges": [
                    {"source": 1, "target": 2, "metadata": {"color": "#f00"}},
                    {"source": 2, "target": 3, "metadata": {"color": "blue"}},
                    {"source": 3, "target": 4},
                    {"source": 4, "target": 1, "metadata": {"color": "#00ff00"}},
                    {"source": 1, "target": 5, "metadata": {"color": "WRONG"}},
                ]
            }
        }
        for func_name, func in plotting_functions:
            fig = func(data)
            suffix = 'directed' if directed else 'undirected'
            filepath = create_output_filepath(
                my_outdir, base_name.format('edge_color_'+suffix, func_name))
            export_all_available_formats(fig, filepath)

    # edge opacity
    for directed in [True, False]:
        data = {
            "graph": {
                "directed": directed,
                "nodes": [
                    {"id": 1},
                    {"id": 2},
                    {"id": 3},
                    {"id": 4},
                    {"id": 5},
                ],
                "edges": [
                    {"source": 1, "target": 2, "metadata": {"opacity": 0.1}},
                    {"source": 2, "target": 3, "metadata": {"opacity": 0.5}},
                    {"source": 3, "target": 4},
                    {"source": 4, "target": 1, "metadata": {"opacity": 1.0}},
                    {"source": 1, "target": 5, "metadata": {"opacity": "WRONG"}},
                ]
            }
        }
        for func_name, func in plotting_functions:
            fig = func(data)
            suffix = 'directed' if directed else 'undirected'
            filepath = create_output_filepath(
                my_outdir, base_name.format('edge_opacity_'+suffix, func_name))
            export_all_available_formats(fig, filepath)

    # edge size
    for directed in [True, False]:
        data = {
            "graph": {
                "directed": directed,
                "nodes": [
                    {"id": 1},
                    {"id": 2},
                    {"id": 3},
                    {"id": 4},
                    {"id": 5},
                ],
                "edges": [
                    {"source": 1, "target": 2, "metadata": {"size": 1}},
                    {"source": 2, "target": 3, "metadata": {"size": 2}},
                    {"source": 3, "target": 4},
                    {"source": 4, "target": 1, "metadata": {"size": 3}},
                    {"source": 1, "target": 5, "metadata": {"size": "WRONG"}},
                ]
            }
        }
        for func_name, func in plotting_functions:
            fig = func(data)
            suffix = 'directed' if directed else 'undirected'
            filepath = create_output_filepath(
                my_outdir, base_name.format('edge_size_'+suffix, func_name))
            export_all_available_formats(fig, filepath)


# Images

@pytest.mark.parametrize('name, in_filepath', TESTDATA_PDF_FILES)
def test_image_viewer_file_pdf(my_outdir, name, in_filepath):
    fig = up.javascript.image_viewer(in_filepath, height=400, width=400)
    out_filepath = create_output_filepath(my_outdir, 'image_viewer_file_' + name)
    export_all_available_formats(fig, out_filepath)


@pytest.mark.parametrize('name, in_filepath', TESTDATA_PNG_FILES)
def test_image_viewer_file_png(my_outdir, name, in_filepath):
    fig = up.javascript.image_viewer(in_filepath)
    out_filepath = create_output_filepath(my_outdir, 'image_viewer_file_' + name)
    export_all_available_formats(fig, out_filepath)


@pytest.mark.parametrize('name, in_filepath', TESTDATA_SVG_FILES)
def test_image_viewer_file_svg(my_outdir, name, in_filepath):
    fig = up.javascript.image_viewer(in_filepath)
    out_filepath = create_output_filepath(my_outdir, 'image_viewer_file_' + name)
    export_all_available_formats(fig, out_filepath)


def test_image_viewer_url(my_outdir):
    print('This test requires a web connection')
    plotting_specs = [
        {},
        {'width': 400}, {'max_width': 400}, {'min_width': 400},
        {'height': 400}, {'max_height': 400}, {'min_height': 400},
        {'border': False}, {'resizable': False},
    ]
    for width, height in [(50, 200), (600, 600)]:
        url = 'http://placehold.it/{w}x{h}&text=test_image_{w}x{h}'.format(w=width, h=height)
        for kwargs in plotting_specs:
            fig = up.javascript.image_viewer(url, mime_type='image/png', **kwargs)
            name = 'image_viewer_url_{}_{}_{}'.format(width, height, kwargs)
            out_filepath = create_output_filepath(my_outdir, name)
            export_all_available_formats(fig, out_filepath)
    # Error on failed MIME type auto-detection
    with pytest.raises(ValueError):
        url = 'http://placehold.it/10x10'
        fig = up.javascript.image_viewer(url)


def test_image_viewer_svg(my_outdir):
    svg_text = '''<svg xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="150" height="150" fill="black"/>
  <circle cx="85" cy="85" r="50" fill="white"/>
  <text x="55" y="90" class="small" fill="blue">an SVG</text>
</svg>'''
    fig = up.javascript.image_viewer(data=svg_text, mime_type='image/svg+xml')
    name = 'image_viewer_svg'
    out_filepath = create_output_filepath(my_outdir, name)
    export_all_available_formats(fig, out_filepath)

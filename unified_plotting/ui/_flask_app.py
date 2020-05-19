"""Flask app for providing a graphical-user interface."""

import json as _json

import flask as _flask
from flask import request as _request

import unified_plotting as _up

from .._unified_arguments.arguments import UNIFIED_ARGS as _UNIFIED_ARGS
from . import _example_data, _templates


def _prepare_html_once(html_template, vector_args, network_args, jgf_example1, jgf_example2):
    """Prepare HTML text for a HTML form object that reflects the given arguments."""
    arg_template = """
        <p>
            <label for="arg_{arg_name}">{arg_name}</label>
            <input type="text" id="arg_{arg_name}" class="style-input" name="{arg_name}">
        </p>"""
    vec_arg = ''
    for arg_name in vector_args:
        vec_arg += arg_template.format(arg_name=arg_name)
    net_arg = ''
    for arg_name in network_args:
        net_arg += arg_template.format(arg_name=arg_name)
    html_form = html_template.format(
        style_vector=vec_arg,
        style_graph=net_arg,
        jgf_data1=jgf_example1,
        jgf_data2=jgf_example2,
    )
    return html_form


_VECTOR_ARGS = ['color'] + [arg for arg in _UNIFIED_ARGS if arg not in ['fig', 'ax']]

_GRAPH_ARGS = [
    'network_height', 'details_height', 'show_details', 'show_details_toggle_button',
    'show_menu', 'show_menu_toggle_button', 'show_node', 'node_size_factor',
    'node_size_data_source', 'use_node_size_normalization', 'node_size_normalization_min',
    'node_size_normalization_max', 'node_drag_fix', 'node_hover_neighborhood',
    'node_hover_tooltip', 'show_node_image', 'node_image_size_factor', 'show_node_label',
    'show_node_label_border', 'node_label_data_source', 'node_label_size_factor',
    'node_label_rotation', 'node_label_font', 'show_edge', 'edge_size_factor',
    'edge_size_data_source', 'use_edge_size_normalization', 'edge_size_normalization_min',
    'edge_size_normalization_max', 'edge_curvature', 'edge_hover_tooltip', 'show_edge_label',
    'show_edge_label_border', 'edge_label_data_source', 'edge_label_size_factor',
    'edge_label_rotation', 'edge_label_font', 'zoom_factor', 'large_network_threshold',
    'layout_algorithm_active']

_HTML_FORM = _prepare_html_once(
    _templates.HTML_MAIN, _VECTOR_ARGS, _GRAPH_ARGS, _example_data.JGF1, _example_data.JGF2)


def _empty_to_none(given):
    """Convert a given value to None if it is an empty string."""
    if given == '':
        return None
    return given


def _str_to_val(given):
    """Convert a given string to a bool, float, list or str object."""
    # bool
    try:
        if given.lower() in ['true', 'yes']:
            return True
        if given.lower() in ['false', 'no']:
            return False
    except Exception:
        pass
    # float
    try:
        return float(given)
    except Exception:
        pass
    # float list
    try:
        return [float(item.strip()) for item in given.split(',')]
    except Exception:
        pass
    # otherwise str
    return given


def _str_to_num_list(given):
    """Convert a given string to a list of float values."""
    try:
        result = []
        for item in given.split(','):
            val = item.strip()
            try:
                val = float(val)
            except Exception:
                pass
            result.append(val)
    except Exception:
        result = given
    return result


def _get_vector_data():
    """Get vector data from data retrieved from a HTML form."""
    num_vectors = int(_request.form.get('num-vectors'))
    data, name = [], []
    for i in range(1, num_vectors+1):
        data_i = _str_to_num_list(_request.form.get('vec{}'.format(i)))
        name_i = _request.form.get('vec{}-name'.format(i))
        if data_i:
            data.append(data_i)
            name.append(name_i)
    if len(data) > 0:
        while len(data) < 3:
            data.append(None)
            name.append(None)
    return data, name


def _get_graph_data():
    """Get graph data from data retrieved from a HTML form."""
    data = _request.form.get('jgf-text')
    try:
        data = _json.dumps(_json.loads(data))
    except Exception:
        pass
    return data


def _get_vector_style():
    """Get vector style from data retrieved from a HTML form."""
    return {arg: _str_to_val(_empty_to_none(_request.form.get(arg)))
            for arg in _VECTOR_ARGS}


def _get_graph_style():
    """Get graph style from data retrieved from a HTML form."""
    return {arg: _str_to_val(_empty_to_none(_request.form.get(arg)))
            for arg in _GRAPH_ARGS}


def _get_vector_method():
    """Get vector method from data retrieved from a HTML form."""
    library = _request.form.get('library')
    if library == 'Matplotlib':
        plot_type = _request.form.get('plot-type-matplotlib')
        output_format = _request.form.get('output-format-matplotlib')
        func = getattr(_up.matplotlib, plot_type)
    elif library == "Plotly":
        plot_type = _request.form.get('plot-type-plotly')
        output_format = _request.form.get('output-format-plotly')
        func = getattr(_up.plotly, plot_type)
    else:
        plot_type = _request.form.get('plot-type-javascript')
        output_format = _request.form.get('output-format-javascript')
        func = getattr(_up.javascript, plot_type)
    return func, output_format


def _get_graph_method():
    """Get graph style from data retrieved from a HTML form."""
    library = _request.form.get('graph-library')
    if library == 'JavaScript':
        plot_type = _request.form.get('graph-plot-type-javascript')
        output_format = _request.form.get('graph-format-javascript')
        func = getattr(_up.javascript, plot_type)
    return func, output_format


def _plot_vector_data(data, name, kwargs, func, output_format):
    """Plot user-given vector data and provide it in HTML format."""
    try:
        data_2d = dict(x=data[0], y=data[1], x_title=name[0], y_title=name[1])
    except Exception:
        data_2d = None

    try:
        data_3d = dict(x=data[0], y=data[1], z=data[2],
                       x_title=name[0], y_title=name[1], z_title=name[2])
    except Exception:
        data_3d = None

    try:
        data_nd = dict(data=[vec for vec in data if vec is not None], name=name)
    except Exception:
        data_nd = None

    for used_data in [data_2d, data_3d, data_nd]:
        try:
            inp = {key: val for key, val in list(used_data.items()) + list(kwargs.items())
                   if val is not None}
            fig = func(**inp)
            if output_format == 'html':
                html_text = fig.html_text
            else:
                try:
                    html_text = getattr(fig, '{}_img_element'.format(output_format))
                except Exception:
                    html_text = getattr(fig, '{}_object_element'.format(output_format))
            break
        except Exception as excp:
            html_text = 'Plotting failed with following error:<br>'
            html_text += str(excp)
    return html_text


def _plot_graph_data(data, kwargs, func, output_format):
    """Plot user-given graph data and provide it in HTML format."""
    used_kwargs = {key: val for key, val in kwargs.items() if val is not None}
    fig = func(data, **used_kwargs)
    if output_format == 'html':
        html_text = fig.html_text
    return html_text


MY_FLASK_APP = _flask.Flask(__name__)


@MY_FLASK_APP.route('/', methods=['GET', 'POST'])
def index():
    """Respond to GET and POST requests on the main HTTP endpoint."""
    if _request.method == 'GET':
        html_text = _templates.HTML_BASE.format(_HTML_FORM)
    elif _request.method == 'POST':
        data_type = _request.form.get('data-type')
        if data_type == 'vector':
            data, name = _get_vector_data()
            if len(data) == 0:
                html_text = _templates.HTML_BASE.format('Error: No data was provided.')
            else:
                kwargs = _get_vector_style()
                func, output_format = _get_vector_method()
                html_text = _plot_vector_data(data, name, kwargs, func, output_format)
        else:
            data = _get_graph_data()
            if len(data) == 0:
                html_text = _templates.HTML_BASE.format('Error: No data was provided.')
            else:
                kwargs = _get_graph_style()
                func, output_format = _get_graph_method()
                html_text = _plot_graph_data(data, kwargs, func, output_format)
    return html_text

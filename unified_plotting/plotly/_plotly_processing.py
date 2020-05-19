"""Plotly-specific processing of function arguments."""

from collections.abc import Iterable as _Iterable
from math import log10 as _log10
from numbers import Number as _Number

from .. import _logging
from .._config import config as _config
from .._unified_arguments import arguments as _args
from .._unified_arguments import colormaps as _colormaps
from .._unified_arguments import shared_preprocessing as _shared_preprocessing
from .._unified_arguments import shared_processing as _shared_processing
from .._unified_arguments.injection import _parse_spec_kwargs


# Common

def _pt_to_px(given):
    """Convert from points (pt) to pixels (px) where 1 in = 72 pt = 96 px, hence factor 96/72."""
    return float(given) * 1.3333333333333333  # *96/72


def _convert_font_size(given):
    """Convert font sizes given in pt to fit to width, height and margins handled in px."""
    try:
        return _pt_to_px(given)
    except Exception:
        message = 'Failed to convert font size from points (pt) to pixels (px): {}.'.format(given)
        raise ValueError(message)


# I) Plot size

def set_plot_size(kwargs, layout):
    """Set plot size in layout object.

    References
    ----------
    - https://plotly.com/python/reference/#layout-width
    - https://plotly.com/python/reference/#layout-height

    """
    names = [
        'width_mm', 'width_in', 'width_pt', 'height_mm', 'height_in', 'height_pt',
        'dpi',
        'margin_auto',
        'margin_left_mm', 'margin_left_in', 'margin_left_pt', 'margin_left_rel',
        'margin_right_mm', 'margin_right_in', 'margin_right_pt', 'margin_right_rel',
        'margin_top_mm', 'margin_top_in', 'margin_top_pt', 'margin_top_rel',
        'margin_bottom_mm', 'margin_bottom_in', 'margin_bottom_pt', 'margin_bottom_rel',
    ]
    pre_kwargs = {key: kwargs[key] for key in names}
    post_kwargs = _parse_spec_kwargs(_args.plot_size_and_resolution, kwargs)
    used_kwargs = _shared_processing.select_plot_size_kwargs(pre_kwargs, post_kwargs)
    return used_kwargs


# II) Plot color

def set_plot_color(kwargs, layout):
    """Set paper and plot color in layout object.

    References
    ----------
    - https://plotly.com/python/reference/#layout-plot_bgcolor
    - https://plotly.com/python/reference/#layout-paper_bgcolor

    """
    given = _parse_spec_kwargs(_args.plot_color, kwargs)

    # Plot background color
    if given['plot_background_color'] is not None:
        layout['plot_bgcolor'] = convert_color(given['plot_background_color'])
    else:
        # Plotly's default was white, later lightblue. Best would be transparent.
        layout['plot_bgcolor'] = 'white'
    # Paper background color
    if given['paper_background_color'] is not None:
        layout['paper_bgcolor'] = convert_color(given['paper_background_color'])


def set_plot_color_3d(kwargs, layout):
    """Set paper and plot color in layout object for 3D plots.

    References
    ----------
    - https://plotly.com/python/reference/#layout-scene-bgcolor
    - https://plotly.com/python/reference/#layout-scene-xaxis-backgroundcolor
    - https://plotly.com/python/reference/#layout-scene-yaxis-backgroundcolor
    - https://plotly.com/python/reference/#layout-scene-zaxis-backgroundcolor
    - https://plotly.com/python/reference/#layout-paper_bgcolor

    """
    # Note: 3D needs separate treatment because layout['plot_bgcolor'] works only for 2D plots

    given = _parse_spec_kwargs(_args.plot_color, kwargs)

    if given['plot_background_color'] is not None:
        for axis_name in ('xaxis', 'yaxis', 'zaxis'):
            layout['scene'][axis_name]['backgroundcolor'] = \
                convert_color(given['plot_background_color'])
    else:
        # Plotly's default was white, later lightblue. Best would be transparent.
        for axis_name in ('xaxis', 'yaxis', 'zaxis'):
            layout['scene'][axis_name]['backgroundcolor'] = 'white'
    if given['paper_background_color'] is not None:
        layout['paper_bgcolor'] = convert_color(given['paper_background_color'])


# III) Plot title

def set_title(kwargs, layout):
    """Set title properties (on/off, font, size, color) in layout object.

    References
    ----------
    - https://plotly.com/python/reference/#layout-title

    """
    given = _parse_spec_kwargs(_args.plot_title, kwargs)
    if given['show_title']:
        if given['title_position'] == 'left':
            x_pos = 0.05
        elif given['title_position'] == 'center':
            x_pos = 0.5
        elif given['title_position'] == 'right':
            x_pos = 0.95
        layout['title'] = dict(
            text=given['title'],
            x=x_pos,
            xanchor=given['title_position'],
            font=dict(
                family=given['title_font'],
                size=_convert_font_size(given['title_size']),
                color=given['title_color'],
            )
        )


# IV) Axes

def convert_axis_aspect_ratio(axis_aspect_ratio):
    """Convert the given aspect ratio of x, y and z to a format that can be used by Plotly."""
    if axis_aspect_ratio is None:
        axis_aspect_ratio_spec = dict(x=1.0, y=1.0, z=1.0)
    else:
        try:
            x_ratio, y_ratio, z_ratio = axis_aspect_ratio
            axis_aspect_ratio_spec = dict(x=x_ratio, y=y_ratio, z=z_ratio)
        except Exception:
            message = (
                'The provided axis_aspect_ratio could not be interpreted as '
                'vector with three entries.')
            raise ValueError(message) from None
    return axis_aspect_ratio_spec


def _convert_axis_scale(axis_scale):
    """Convert the given axis scale (e.g. "log") to one that can be used by Plotly.

    References
    ----------
    - https://plotly.com/python/reference/#layout-xaxis-type

    """
    possible_axis_scale = [None, 'lin', 'linear', 'log', 'logarithmic', 'cat', 'categorical']
    _shared_preprocessing.check_categorical_argument(
        axis_scale, 'axis_scale', possible_axis_scale)

    if axis_scale is None:
        returned_axis_scale = None
    elif axis_scale in ('linear', 'lin'):
        returned_axis_scale = 'linear'
    elif axis_scale in ('logarithmic', 'log'):
        returned_axis_scale = 'log'
    elif axis_scale in ('categorical', 'cat'):
        returned_axis_scale = 'category'
    else:
        raise ValueError('Invalid value for axis scale: "{}". Possible values: {}'.format(
            axis_scale, possible_axis_scale))
    return returned_axis_scale


def _convert_axis_range(axis_range, axis_scale):
    """Convert the given axis range (=start & stop value) to one that can be used by Plotly.

    Caution: Dependence on whether the scale is linear or logarithmic.

    References
    ----------
    - https://plotly.com/python/reference/#layout-xaxis-range

    """
    if axis_range is None:
        axis_range_auto = True
        axis_range_values = None
    else:
        if not isinstance(axis_range, list) or len(axis_range) != 2 or \
                not isinstance(axis_range[0], _Number) or not isinstance(axis_range[1], _Number):
            raise ValueError('Invalid value for axis_range: "{}". '
                             'Expected a list of two numbers.'.format(axis_scale))
        start, stop = axis_range
        if start > stop:
            raise ValueError('Invalid axis range: Start value ({}) is bigger than '
                             'stop value ({}).'.format(start, stop))

        # Plotly: "If the axis `type` is "log", then you must take the log of your desired range."
        if axis_scale == 'log':
            try:
                start = _log10(start)
            except ValueError:
                raise ValueError('Start value {} is not possible for a logarithmic axis. '
                                 'It needs to be greater than zero.'.format(start))
            try:
                stop = _log10(stop)
            except ValueError:
                raise ValueError('Stop value {} is not possible for a logarithmic axis. '
                                 'It needs to be greater than zero.'.format(stop))
        axis_range_auto = False
        axis_range_values = [start, stop]
    return axis_range_auto, axis_range_values


def _convert_tick_pos_and_label(tick_position, label):
    """Convert the given tick positions to ones that can be used by Plotly.

    References
    ----------
    - https://plotly.com/python/reference/#layout-xaxis-tickmode
    - https://plotly.com/python/reference/#layout-xaxis-tickvals
    - https://plotly.com/python/reference/#layout-xaxis-ticktext

    """
    def to_list_of_numbers(values, label):
        try:
            values = list(values)
            assert all(isinstance(val, _Number) for val in values)
        except Exception:
            message = (
                '{} needs to be an Iterable of numbers, '
                'e.g. a list, tuple, NumPy array or Pandas Series.'.format(label))
            raise ValueError(message) from None
        return values

    def to_list_of_strings(values, label):
        try:
            # Note: '' can cause unexpected visualizations in Plotly, hence use of ' '
            values = [' ' if item is None else str(item) for item in values]
        except Exception:
            message = (
                '{} needs to be an Iterable, '
                'e.g. a list, tuple, NumPy array or Pandas Series.'.format(label))
            raise ValueError(message) from None
        return values

    if tick_position is None and label is None:
        tick_mode = 'auto'
        tick_values = None
        tick_text = None
    else:
        # https://github.com/plotly/plotly.js/issues/2885
        tick_mode = None  # 'array' would be correct but fails in case of log axis, None works
        if tick_position is None:
            try:
                tick_values = list(range(len(label)))
            except TypeError:
                tick_values = None
        else:
            tick_values = to_list_of_numbers(tick_position, 'Tick position')
        if label is None:
            tick_text = None
        else:
            tick_text = to_list_of_strings(label, 'Label')
    return tick_mode, tick_values, tick_text


def _convert_tick_direction(tick_direction):
    """Convert the given tick direction to one that can be used by Plotly.

    References
    ----------
    - https://plotly.com/python/reference/#layout-xaxis-ticks

    """
    if tick_direction is None:
        returned_tick_direction = None
    else:
        possible_values = ['in', 'out']
        _shared_preprocessing.check_categorical_argument(
            tick_direction, 'tick_direction', possible_values)

        if tick_direction == 'in':
            returned_tick_direction = 'inside'
        elif tick_direction == 'out':
            returned_tick_direction = 'outside'
    return returned_tick_direction


def set_x_axis(kwargs, layout):
    """Set axis properties: title, labels, spine, ticks.

    References
    ----------
    - https://plotly.com/python/reference/#layout-xaxis

    Examples
    --------
    - https://plotly.com/python/axes
    - https://github.com/plotly/plotly.js/issues/296

    """
    given = _parse_spec_kwargs(_args.x_axis, kwargs)

    if given['x_axis_offset'] != 0 and given['x_axis_offset'] is not None:
        _logging.warn_user('Axis offset is currently not available in Plotly.')
    if given['x_title_offset'] != 0 and given['x_title_offset'] is not None:
        _logging.warn_user('Title offset is currently not available in Plotly.')
    if given['x_label_offset'] != 0 and given['x_label_offset'] is not None:
        _logging.warn_user('Label offset is currently not available in Plotly.')

    # 1) On/Off
    # - Axis
    if not given['show_x_axis']:
        given['show_x_spine'] = False
        given['show_x_title'] = False
        given['show_x_tick'] = False
        given['show_x_label'] = False

    # - Spine
    show_spine = given['show_x_spine']

    # - Title
    if given['show_x_title']:
        axis_title = given['x_title']
    else:
        axis_title = ''

    # - Ticks
    if given['show_x_tick']:
        ticks_direction = 'outside'
    else:
        ticks_direction = ''

    # - Labels
    show_label = given['show_x_label']

    # 2) Color
    # - Axis
    if given['x_axis_color'] is not None:
        given['x_spine_color'] = given['x_axis_color']
        given['x_title_color'] = given['x_axis_color']
        given['x_tick_color'] = given['x_axis_color']
        given['x_label_color'] = given['x_axis_color']

    # - Spine
    spine_color = given['x_spine_color']

    # - Title
    title_dict = dict(
        color=given['x_title_color'],
    )

    # - Ticks
    tick_color = given['x_tick_color']

    # - Labels
    labels_dict = dict(color=given['x_label_color'])

    # 3) Font
    # - Title
    title_dict['family'] = given['x_title_font']
    title_dict['size'] = _convert_font_size(given['x_title_size'])

    # - Labels
    labels_dict['family'] = given['x_label_font']
    labels_dict['size'] = _convert_font_size(given['x_label_size'])

    # 4) Other properties
    # - Axis
    axis_scale = _convert_axis_scale(given['x_axis_scale'])
    axis_range_auto, axis_range_values = _convert_axis_range(given['x_axis_range'], axis_scale)

    # - Ticks
    tick_mode, tick_values, tick_text = _convert_tick_pos_and_label(
        given['x_tick_position'], given['x_label'])
    ticks_length = given['x_tick_length']
    ticks_width = given['x_tick_width']
    if given['show_x_tick']:
        ticks_direction = _convert_tick_direction(given['x_tick_direction'])

    # - Labels
    if given['x_label_rotation'] is not None:
        labels_angle = -given['x_label_rotation']
    else:
        labels_angle = 'auto'

    x_axis_options = dict(
        # Axis
        title=axis_title,
        titlefont=title_dict,
        autorange=axis_range_auto,
        range=axis_range_values,
        # Spine
        showline=show_spine,
        linecolor=spine_color,
        zeroline=False,
        # Labels
        showticklabels=show_label,
        tickfont=labels_dict,
        # Ticks
        ticks=ticks_direction,
        tickcolor=tick_color,
        ticklen=ticks_length,
        tickwidth=ticks_width,
    )
    if axis_scale is not None:
        x_axis_options['type'] = axis_scale
    if labels_angle != 'auto':
        x_axis_options['tickangle'] = labels_angle
    if tick_mode != 'auto':
        x_axis_options['tickmode'] = tick_mode
        x_axis_options['tickvals'] = tick_values
        x_axis_options['ticktext'] = tick_text

    if 'xaxis' not in layout:
        layout['xaxis'] = dict()
    layout['xaxis'].update(x_axis_options)


def set_y_axis(kwargs, layout):
    """Set axis properties: title, labels, spine, ticks.

    References
    ----------
    - https://plotly.com/python/reference/#layout-yaxis
    - https://github.com/plotly/plotly.js/issues/296

    Examples
    --------
    - https://plotly.com/python/axes/

    """
    given = _parse_spec_kwargs(_args.y_axis, kwargs)

    if given['y_axis_offset'] != 0 and given['y_axis_offset'] is not None:
        _logging.warn_user('Axis offset is currently not available in Plotly.')
    if given['y_title_offset'] != 0 and given['y_title_offset'] is not None:
        _logging.warn_user('Title offset is currently not available in Plotly.')
    if given['y_label_offset'] != 0 and given['y_label_offset'] is not None:
        _logging.warn_user('Label offset is currently not available in Plotly.')

    # 1) On/Off
    # - Axis
    if not given['show_y_axis']:
        given['show_y_spine'] = False
        given['show_y_title'] = False
        given['show_y_tick'] = False
        given['show_y_label'] = False

    # - Spine
    show_spine = given['show_y_spine']

    # - Title
    if given['show_y_title']:
        axis_title = given['y_title']
    else:
        axis_title = ''

    # - Ticks
    if given['show_y_tick']:
        ticks_direction = 'outside'
    else:
        ticks_direction = ''

    # - Labels
    show_label = given['show_y_label']

    # 2) Color
    # - Axis
    if given['y_axis_color'] is not None:
        given['y_spine_color'] = given['y_axis_color']
        given['y_title_color'] = given['y_axis_color']
        given['y_tick_color'] = given['y_axis_color']
        given['y_label_color'] = given['y_axis_color']

    # - Spine
    spine_color = given['y_spine_color']

    # - Title
    title_dict = dict(
        color=given['y_title_color'],
    )

    # - Ticks
    tick_color = given['y_tick_color']

    # - Labels
    labels_dict = dict(color=given['y_label_color'])

    # 3) Font
    # - Title
    title_dict['family'] = given['y_title_font']
    title_dict['size'] = _convert_font_size(given['y_title_size'])

    # - Labels
    labels_dict['family'] = given['y_label_font']
    labels_dict['size'] = _convert_font_size(given['y_label_size'])

    # 4) Other properties
    # - Axis
    axis_scale = _convert_axis_scale(given['y_axis_scale'])
    axis_range_auto, axis_range_values = _convert_axis_range(given['y_axis_range'], axis_scale)

    # - Ticks
    tick_mode, tick_values, tick_text = _convert_tick_pos_and_label(
        given['y_tick_position'], given['y_label'])
    ticks_length = given['y_tick_length']
    ticks_width = given['y_tick_width']
    if given['show_y_tick']:
        ticks_direction = _convert_tick_direction(given['y_tick_direction'])

    # - Labels
    if given['y_label_rotation'] is not None:
        labels_angle = -given['y_label_rotation']
    else:
        labels_angle = 'auto'

    y_axis_options = dict(
        # Axis
        title=axis_title,
        titlefont=title_dict,
        autorange=axis_range_auto,
        range=axis_range_values,
        # Spine
        showline=show_spine,
        linecolor=spine_color,
        zeroline=False,
        # Labels
        showticklabels=show_label,
        tickfont=labels_dict,
        # Ticks
        ticks=ticks_direction,
        tickcolor=tick_color,
        ticklen=ticks_length,
        tickwidth=ticks_width,
    )
    if axis_scale is not None:
        y_axis_options['type'] = axis_scale
    if labels_angle != 'auto':
        y_axis_options['tickangle'] = labels_angle
    if tick_mode != 'auto':
        y_axis_options['tickmode'] = tick_mode
        y_axis_options['tickvals'] = tick_values
        y_axis_options['ticktext'] = tick_text

    if 'yaxis' not in layout:
        layout['yaxis'] = dict()
    layout['yaxis'].update(y_axis_options)


def set_x_axis_3d(kwargs, layout):
    """Set axis properties: title, labels, spine, ticks.

    References
    ----------
    - https://plotly.com/python/reference/#layout-scene

    """
    if 'x_tick_direction' in kwargs and kwargs['x_tick_direction'] == 'in':
        _logging.warn_user('Tick direction "in" is currently not available for '
                           '3D plots in Plotly.')

    if 'scene' not in layout:
        layout['scene'] = dict()
    set_x_axis(kwargs, layout['scene'])


def set_y_axis_3d(kwargs, layout):
    """Set axis properties: title, labels, spine, ticks.

    References
    ----------
    - https://plotly.com/python/reference/#layout-scene

    """
    if 'y_tick_direction' in kwargs and kwargs['y_tick_direction'] == 'in':
        _logging.warn_user('Tick direction "in" is currently not available for '
                           '3D plots in Plotly.')

    if 'scene' not in layout:
        layout['scene'] = dict()
    set_y_axis(kwargs, layout['scene'])


def set_z_axis_3d(kwargs, layout):
    """Set axis properties: title, labels, spine, ticks.

    References
    ----------
    - https://plotly.com/python/reference/#layout-scene
    - https://github.com/plotly/plotly.js/issues/296

    """
    if 'z_tick_direction' in kwargs and kwargs['z_tick_direction'] == 'in':
        _logging.warn_user('Tick direction "in" is currently not available for '
                           '3D plots in Plotly.')

    given = _parse_spec_kwargs(_args.z_axis, kwargs)

    if given['z_axis_offset'] != 0 and given['z_axis_offset'] is not None:
        _logging.warn_user('Axis offset is currently not available in Plotly.')
    if given['z_title_offset'] != 0 and given['z_title_offset'] is not None:
        _logging.warn_user('Title offset is currently not available in Plotly.')
    if given['z_label_offset'] != 0 and given['z_label_offset'] is not None:
        _logging.warn_user('Label offset is currently not available in Plotly.')

    # 1) On/Off
    # - Axis
    if not given['show_z_axis']:
        given['show_z_spine'] = False
        given['show_z_title'] = False
        given['show_z_tick'] = False
        given['show_z_label'] = False

    # - Spine
    show_spine = given['show_z_spine']

    # - Title
    if given['show_z_title']:
        axis_title = given['z_title']
    else:
        axis_title = ''

    # - Ticks
    if given['show_z_tick']:
        ticks_direction = 'outside'
    else:
        ticks_direction = ''

    # - Labels
    show_label = given['show_z_label']

    # 2) Color
    # - Axis
    if given['z_axis_color'] is not None:
        given['z_spine_color'] = given['z_axis_color']
        given['z_title_color'] = given['z_axis_color']
        given['z_tick_color'] = given['z_axis_color']
        given['z_label_color'] = given['z_axis_color']

    # - Spine
    spine_color = given['z_spine_color']

    # - Title
    title_dict = dict(
        color=given['z_title_color'],
    )

    # - Ticks
    tick_color = given['z_tick_color']

    # - Labels
    labels_dict = dict(color=given['z_label_color'])

    # 3) Font
    # - Title
    title_dict['family'] = given['z_title_font']
    title_dict['size'] = _convert_font_size(given['z_title_size'])

    # - Labels
    labels_dict['family'] = given['z_label_font']
    labels_dict['size'] = _convert_font_size(given['z_label_size'])

    # 4) Other properties
    # - Axis
    axis_scale = _convert_axis_scale(given['z_axis_scale'])
    axis_range_auto, axis_range_values = _convert_axis_range(given['z_axis_range'], axis_scale)

    # - Ticks
    tick_mode, tick_values, tick_text = _convert_tick_pos_and_label(
        given['z_tick_position'], given['z_label'])
    ticks_length = given['z_tick_length']
    ticks_width = given['z_tick_width']
    if given['show_z_tick']:
        ticks_direction = _convert_tick_direction(given['z_tick_direction'])

    # - Labels
    if given['z_label_rotation'] is not None:
        labels_angle = -given['z_label_rotation']
    else:
        labels_angle = 'auto'

    z_axis_options = dict(
        # Axis
        type=axis_scale,
        title=axis_title,
        titlefont=title_dict,
        autorange=axis_range_auto,
        range=axis_range_values,
        # Spine
        showline=show_spine,
        linecolor=spine_color,
        zeroline=False,
        # Labels
        showticklabels=show_label,
        tickfont=labels_dict,
        # Ticks
        ticks=ticks_direction,
        tickcolor=tick_color,
        ticklen=ticks_length,
        tickwidth=ticks_width,
        tickmode=tick_mode,
        tickvals=tick_values,
        ticktext=tick_text,
    )
    if labels_angle != 'auto':
        z_axis_options['tickangle'] = labels_angle
    if 'scene' not in layout:
        layout['scene'] = dict()
    if 'zaxis' not in layout['scene']:
        layout['scene']['zaxis'] = dict()
    layout['scene']['zaxis'].update(z_axis_options)


# V) Grid

def set_grid(kwargs, layout):
    """Set grid properties: on/off, color, style, width.

    References
    ----------
    - https://plotly.com/python/axes
    - https://plotly.com/python/reference/#layout-xaxis-showgrid
    - https://plotly.com/python/reference/#layout-xaxis-gridcolor
    - https://plotly.com/python/reference/#layout-xaxis-gridwidth
    - https://community.plotly.com/t/how-to-customize-grid-lisne-to-dotted-lines/2981/2

    """
    given_x = _parse_spec_kwargs(_args.x_grid, kwargs)
    given_y = _parse_spec_kwargs(_args.y_grid, kwargs)

    if given_x['x_grid_style'] not in ('-', 'solid') or \
            given_y['y_grid_style'] not in ('-', 'solid'):
        _logging.warn_user('Grid line style is currently not available in Plotly.')

    x_axis_options = dict(
        showgrid=given_x['show_x_grid'],
        gridcolor=given_x['x_grid_color'],
        gridwidth=given_x['x_grid_width'],
    )
    if 'xaxis' not in layout:
        layout['xaxis'] = dict()
    layout['xaxis'].update(x_axis_options)

    y_axis_options = dict(
        showgrid=given_y['show_y_grid'],
        gridcolor=given_y['y_grid_color'],
        gridwidth=given_y['y_grid_width'],
    )
    if 'yaxis' not in layout:
        layout['yaxis'] = dict()
    layout['yaxis'].update(y_axis_options)


def set_grid_3d(kwargs, layout):
    """Set grid properties: on/off, color, width.

    References
    ----------
    - https://plotly.com/python/axes

    """
    given_x = _parse_spec_kwargs(_args.x_grid, kwargs)
    given_y = _parse_spec_kwargs(_args.y_grid, kwargs)
    given_z = _parse_spec_kwargs(_args.z_grid, kwargs)

    if given_x['x_grid_style'] not in ('-', 'solid') or \
            given_y['y_grid_style'] not in ('-', 'solid') or \
            given_z['z_grid_style'] not in ('-', 'solid'):
        _logging.warn_user('Grid line style is currently not available in Plotly.')

    x_axis_options = dict(
        showgrid=given_x['show_x_grid'],
        gridcolor=given_x['x_grid_color'],
        gridwidth=given_x['x_grid_width'],
    )
    if 'scene' not in layout:
        layout['scene'] = dict()
    if 'xaxis' not in layout['scene']:
        layout['scene']['xaxis'] = dict()
    layout['scene']['xaxis'].update(x_axis_options)

    y_axis_options = dict(
        showgrid=given_y['show_y_grid'],
        gridcolor=given_y['y_grid_color'],
        gridwidth=given_y['y_grid_width'],
    )
    if 'yaxis' not in layout['scene']:
        layout['scene']['yaxis'] = dict()
    layout['scene']['yaxis'].update(y_axis_options)

    z_axis_options = dict(
        showgrid=given_z['show_z_grid'],
        gridcolor=given_z['z_grid_color'],
        gridwidth=given_z['z_grid_width'],
    )
    if 'zaxis' not in layout['scene']:
        layout['scene']['zaxis'] = dict()
    layout['scene']['zaxis'].update(z_axis_options)


# VI) Legend

def extract_legend(kwargs):
    """Provide legend properties: on/off.

    References
    ----------
    - https://plotly.com/python/reference/#scatter-showlegend

    """
    given = _parse_spec_kwargs(_args.legend, kwargs)
    return given


def set_legend(kwargs, layout):
    """Set legend properties.

    References
    ----------
    - https://plotly.com/python/legend
    - https://plotly.com/python/reference/#layout-legend
    - https://plotly.com/python/reference/#scatter-showlegend

    """
    legend_spec = extract_legend(kwargs)
    show_legend = legend_spec['show_legend'] is True
    layout['showlegend'] = show_legend
    if show_legend:
        if 'legend' not in layout:
            layout['legend'] = dict()
        # Title
        if legend_spec['legend_title']:
            layout['legend']['title'] = dict(
                text=legend_spec['legend_title'],
                font=dict(
                    color=convert_color(legend_spec['legend_color']),
                    size=_convert_font_size(legend_spec['legend_size']),
                    family=legend_spec['legend_font'],
                ),
                # side='top',  # alternatives: 'top', 'top left', 'left'
            )
        # Text: Color, size, font
        layout['legend']['font'] = dict(
            color=convert_color(legend_spec['legend_color']),
            size=_convert_font_size(legend_spec['legend_size']),
            family=legend_spec['legend_font'],
        )
        # Marker size  # TODO: Use legend_spec['legend_marker_size'] once Plotly supports values
        layout['legend']['itemsizing'] = 'constant'  # alternatives: 'constant', 'trace'
        # Background color
        layout['legend']['bgcolor'] = convert_color(legend_spec['legend_background_color'])
        # Position: horizontal, vertical
        if legend_spec['legend_position_horizontal'] == 'left':
            layout['legend']['x'] = 0.005
            layout['legend']['xanchor'] = 'left'
        elif legend_spec['legend_position_horizontal'] == 'center':
            layout['legend']['x'] = 0.5
            layout['legend']['xanchor'] = 'center'
        elif legend_spec['legend_position_horizontal'] == 'right':
            layout['legend']['x'] = 0.995
            layout['legend']['xanchor'] = 'right'
        else:
            message = ('Unknown value for legend_position_horizontal. '
                       'Possible values: "left", "center", "right".')
            raise ValueError(message)
        if legend_spec['legend_position_vertical'] == 'top':
            layout['legend']['y'] = 0.995
            layout['legend']['yanchor'] = 'top'
        elif legend_spec['legend_position_vertical'] == 'center':
            layout['legend']['y'] = 0.5
            layout['legend']['yanchor'] = 'middle'
        elif legend_spec['legend_position_vertical'] == 'bottom':
            layout['legend']['y'] = 0.005
            layout['legend']['yanchor'] = 'bottom'
        else:
            message = ('Unknown value for legend_position_vertical. '
                       'Possible values: "top", "center", "bottom".')
            raise ValueError(message)
        # Border: size, color
        layout['legend']['borderwidth'] = _pt_to_px(legend_spec['legend_border_size'])
        layout['legend']['bordercolor'] = convert_color(legend_spec['legend_border_color'])


# VII) Colormap

def extract_colormap_spec(kwargs):
    """Extract colormap properties from kwargs: colormap, reversed, colorbar on/off.

    References
    ----------
    - https://plotly.com/python/reference/#scatter-marker-colorbar

    Examples
    --------
    - https://plotly.com/python/v3/colorscales
    - https://plotly.com/python/v3/ipython-notebooks/color-scales

    """
    given = _parse_spec_kwargs(_args.colormap, kwargs)
    return given


def _convert_colormap(given_colormap):
    """Convert the given colormap into one that can be used by Plotly.

    Check if a given colormap is known by Plotly. If not, try to construct it by converting it
    from a matplotlib colormap.
    """
    # TODO: check non-string colormaps for validity too in given_cm_to_cm

    def str_to_cm(colormap_name):
        cm_str_lower = colormap_name.lower()
        if cm_str_lower in _colormaps.PLOTLY_BUILTIN_COLORMAPS:
            colormap = _colormaps.PLOTLY_BUILTIN_COLORMAPS[cm_str_lower]
        elif cm_str_lower in _colormaps.PLOTLY_EXTERNAL_COLORMAPS:
            colormap = _colormaps.PLOTLY_EXTERNAL_COLORMAPS[cm_str_lower]
        else:
            message = 'Colormap with name "{}" is not known.'.format(colormap_name)
            raise ValueError(message)
        return colormap

    def given_cm_to_cm(given):
        if isinstance(given, str):
            colormap = str_to_cm(given)
        else:
            colormap = given
        return colormap

    try:
        colormap = given_cm_to_cm(given_colormap)
    except Exception:
        message = 'The provided colormap was not recognized. Using the default colormap instead.'
        _logging.warn_user(message)
        try:
            default_colormap = _config.settings.colormap
            colormap = given_cm_to_cm(default_colormap)
        except Exception:
            message = 'Neither the given colormap nor the default colormap are known.'
            raise ValueError(message)
    return colormap


def convert_colormap_spec(given_colormap_spec):
    """Convert a general colormap spec into one that can be used by Plotly."""
    colormap = _convert_colormap(given_colormap_spec['colormap'])
    colormap_reversed = given_colormap_spec['colormap_reversed']
    show_colormap = given_colormap_spec['show_colormap']
    colormap_label_font = given_colormap_spec['colormap_label_font']
    colormap_label_size = given_colormap_spec['colormap_label_size']
    colormap_label_color = convert_color(given_colormap_spec['colormap_label_color'])
    colormap_border_size = _pt_to_px(given_colormap_spec['colormap_border_size'])
    plotly_colormap_spec = dict(
        showscale=show_colormap,
        colorscale=colormap,
        reversescale=colormap_reversed,
        colorbar=dict(
            outlinewidth=colormap_border_size,
            ypad=0.0,
            xpad=5.0,
            x=1.0,
            tickfont=dict(
                family=colormap_label_font,
                size=_convert_font_size(colormap_label_size),
                color=colormap_label_color,
            ),
        ),
    )
    return plotly_colormap_spec


# VIII) Markers

def extract_marker_spec(kwargs):
    """Extract marker properties from kwargs."""
    given = _parse_spec_kwargs(_args.markers, kwargs)
    return given


def _convert_marker_style(given_style, argument_name='marker_style'):
    """Convert a general marker style into one that can be used by Plotly.

    References
    ----------
    - https://plotly.com/python/reference/#scatter-marker-symbol

    """
    # Argument processing
    given_style = str(given_style).lower()

    # Validity check
    possible_values = [
        'o', 'circle',
        '.', 'point', 'dot',
        't', '3', 'triangle',
        's', '4', 'square',
        'p', '5', 'pentagon',
        'h', '6', 'hexagon',
        '8', 'octagon',
        '*', 'star',
        '+', 'plus',
        'x', 'cross',
        'd', 'diamond',
        '-', '_', 'horizontal_line',
        '|', 'vertical_line',
        '^', 'triangle_up',
        'v', 'triangle_down',
        '<', 'triangle_left',
        '>', 'triangle_right',
    ]
    _shared_preprocessing.check_categorical_argument(given_style, argument_name, possible_values)

    # Transformation
    conversion_map = {
        'o': 'circle',
        'circle': 'circle',
        '.': 'circle-open-dot',
        'point': 'circle-open-dot',
        'dot': 'circle-open-dot',
        't': 'triangle-up',
        '3': 'triangle-up',
        'triangle': 'triangle-up',
        's': 'square',
        '4': 'square',
        'square': 'square',
        'p': 'pentagon',
        '5': 'pentagon',
        'pentagon': 'pentagon',
        'h': 'hexagon',
        '6': 'hexagon',
        'hexagon': 'hexagon',
        '8': 'octagon',
        'octagon': 'octagon',
        '*': 'star',
        'star': 'star',
        '+': 'cross',
        'plus': 'cross',
        'x': 'x',
        'cross': 'x',
        'd': 'diamond',
        'diamond': 'diamond',
        '-': 141,
        '_': 141,
        'horizontal_line': 141,  # 'line-ew' leads to no marker on plot, seems to be a Plotly bug
        '|': 142,
        'vertical_line': 142,    # 'line-ns' leads to no marker on plot, seems to be a Plotly bug
        '^': 'triangle-up',
        'triangle_up': 'triangle-up',
        'v': 'triangle-down',
        'triangle_down': 'triangle-down',
        '<': 'triangle-left',
        'triangle_left': 'triangle-left',
        '>': 'triangle-right',
        'triangle_right': 'triangle-right',
    }
    returned_style = conversion_map[given_style]
    return returned_style


def _convert_marker_size(given):
    """Convert marker size so that a number of 30 means width and height of the marker in points.

    Notes
    -----
    Measurements: Set marker size as number, export plot as SVG, open in Inkscape, measure height
    - number 30  -> height 30 px

    Conclusion: Plotly takes given number and uses it as width and height in px in my setting.

    """
    result = None
    if isinstance(given, _Number):
        result = _pt_to_px(given)
    else:
        try:
            result = [_pt_to_px(val) for val in given]
        except Exception:
            pass
    if result is None:
        message = 'Failed to convert marker size from points (pt) to pixels (px): {}'.format(
            given)
        raise ValueError(message)
    return result


def convert_marker_spec(marker_spec, is_3d=False):
    """Convert a general marker spec into one that can be used by Plotly.

    References
    ----------
    - https://plotly.com/python/reference/#scatter-marker

    """
    plotly_marker_spec = dict(
        color=convert_color(marker_spec['marker_color']),
        colorscale=_convert_colormap(marker_spec['marker_colormap']),
        size=_convert_marker_size(marker_spec['marker_size']),
        opacity=marker_spec['marker_opacity'],
        symbol=_convert_marker_style(marker_spec['marker_style']),
    )
    if is_3d:
        marker_symbols_3d = [
            'circle', 'circle-open', 'square', 'square-open', 'diamond', 'diamond-open',
            'cross', 'x']
        marker_symbols_3d_unified = [
            'o', 'circle', 's', '4', 'square', '+', 'plus', 'x', 'cross', 'd', 'diamond']
        if plotly_marker_spec['symbol'] not in marker_symbols_3d:
            message = (
                '3D plots with Plotly accept only a reduced number of '
                'marker styles: {}'.format(marker_symbols_3d_unified))
            raise ValueError(message)
    show_marker = marker_spec['show_marker']
    return plotly_marker_spec, show_marker


# IX) Lines

def extract_line_spec(kwargs):
    """Extract line properties from kwargs."""
    given = _parse_spec_kwargs(_args.lines, kwargs)
    return given


def _convert_line_style(given_style):
    """Convert a general line style to one that can be used by Plotly.

    References
    ----------
    - https://plotly.com/python/reference/#scatter-line-dash
    - https://plotly.com/python/line-charts

    """
    # Argument processing
    given_style = str(given_style).lower()

    # Validity check
    possible_values = ['solid', '-', 'dash', '--', 'dashdot', '-.', '.-', 'dot', '.', ':', '..']
    _shared_preprocessing.check_categorical_argument(given_style, 'line_style', possible_values)

    # Transformation
    if given_style in ('solid', '-'):
        returned_style = 'solid'
    elif given_style in ('dash', '--'):
        returned_style = 'dash'
    elif given_style in ('dashdot', '-.', '.-'):
        returned_style = 'dashdot'
    else:
        returned_style = 'dot'
    return returned_style


def _convert_line_width(given):
    """Convert line width so that a number of 30 means width of the line in points.

    Notes
    -----
    Measurements: Set marker size as number, export plot as SVG, open in Inkscape, measure width
    - number 30  -> width 30 px

    Conclusion: Plotly takes given number and uses it as width in px in my setting.

    """
    result = None
    if isinstance(given, _Number):
        result = _pt_to_px(given)
    else:
        try:
            result = [_pt_to_px(val) for val in given]
        except Exception:
            pass
    if result is None:
        message = 'Failed to convert line width from points (pt) to pixels (px): {}'.format(given)
        raise ValueError(message)
    return result


def convert_line_spec(line_spec):
    """Convert a general line spec into one that can be used by Plotly.

    References
    ----------
    - https://plotly.com/python/reference/#scatter-line

    """
    # TODO: decide what to do with line colorscale and opacity, seem not to be available

    line_color = convert_color(line_spec['line_color'])
    if not isinstance(line_color, (str, tuple)):
        line_color = 'black'  # because numerical line color is not supported by Plotly

    plotly_line_spec = dict(
        color=line_color,
        width=_convert_line_width(line_spec['line_width']),
        dash=_convert_line_style(line_spec['line_style']),
        # colorscale=convert_colormap(line_spec['line_colormap']),
        # opacity=line_spec['line_opacity'],
    )
    show_line = line_spec['show_line']
    return plotly_line_spec, show_line


# X) Rugs

def extract_rug_spec(kwargs):
    """Provide rug properties."""
    given = _parse_spec_kwargs(_args.rugs, kwargs)
    return given


def convert_rug_spec(rug_spec):
    """Convert rug spec to Plotly parameters."""
    # Note: Analogous to convert_marker_spec and relying on its style & size conversion functions
    plotly_rug_spec = dict(
        color=convert_color(rug_spec['rug_color']),
        colorscale=_convert_colormap(rug_spec['rug_colormap']),
        size=_convert_marker_size(rug_spec['rug_size']),
        opacity=rug_spec['rug_opacity'],
        symbol=_convert_marker_style(rug_spec['rug_style'], argument_name='rug_style'),
    )
    show_rug = rug_spec['show_rug']
    return plotly_rug_spec, show_rug


# XI) Errors

def extract_x_error_spec(kwargs):
    """Provide x error properties."""
    given = _parse_spec_kwargs(_args.x_error, kwargs)
    return given


def extract_y_error_spec(kwargs):
    """Provide y error properties."""
    given = _parse_spec_kwargs(_args.y_error, kwargs)
    return given


def convert_x_error_spec(x_error_spec):
    """Convert a general x error spec into one that can be used by Plotly."""
    plotly_x_error_spec = dict(
        type='data',
        symmetric=False,
        color=convert_color(x_error_spec['x_error_bar_color']),
        thickness=_convert_line_width(x_error_spec['x_error_bar_line_width']),
        width=_convert_line_width(x_error_spec['x_error_bar_size']),
    )
    show_x_error_bar = x_error_spec['show_x_error_bar']
    return plotly_x_error_spec, show_x_error_bar


def convert_y_error_spec(y_error_spec):
    """Convert a general y error spec into one that can be used by Plotly."""
    # 1) Error bar
    show_y_error_bar = y_error_spec['show_y_error_bar']
    plotly_y_error_spec = dict(
        type='data',
        symmetric=False,
        color=convert_color(y_error_spec['y_error_bar_color']),
        thickness=_convert_line_width(y_error_spec['y_error_bar_line_width']),
        width=_convert_line_width(y_error_spec['y_error_bar_size']),
    )
    # 2) Error band
    show_y_error_band = y_error_spec['show_y_error_band']
    band_color = convert_color(y_error_spec['y_error_band_color'])
    band_opacity = y_error_spec['y_error_band_opacity']
    if isinstance(band_color, str) and isinstance(band_opacity, _Number):
        if band_opacity < 0.0:
            band_opacity = 0.0
        elif band_opacity > 1.0:
            band_opacity = 1.0
        band_color = band_color.replace('1.0)', '{})'.format(band_opacity))  # dirty hack
    plotly_y_error_band_spec = dict(
        mode='lines',
        fill='tozerox',
        fillcolor=band_color,
        line=dict(width=0.0),
        showlegend=False,
    )
    return plotly_y_error_spec, show_y_error_bar, plotly_y_error_band_spec, show_y_error_band


# -) Color

def convert_color(given_color):
    """Convert the given RGBA tupel to an RGBA string that can be used by Plotly.

    References
    ----------
    - https://github.com/plotly/plotly.js/blob/master/src/components/color/attributes.js

    """
    try:
        rgba_tuple = _shared_processing.normalize_color(given_color)
        rgba_str = 'rgba{}'.format(rgba_tuple)
        return rgba_str
    except ValueError:
        if not isinstance(given_color, tuple) and \
                isinstance(given_color, _Iterable) and isinstance(given_color[0], _Number):
            return given_color
        raise


# -) Scatter mode (markers, lines or both)

def get_scatter_mode(show_marker, show_line):
    """Convert marker and line visibility to a Plotly mode."""
    if show_marker and show_line:
        mode = 'markers+lines'
    elif show_marker:
        mode = 'markers'
    elif show_line:
        mode = 'lines'
    else:
        mode = ''
    return mode


# -) Bins

def extract_bin_spec(kwargs):
    """Provide bin properties for x-Axis."""
    given = _parse_spec_kwargs(_args.bins, kwargs)
    return given


def convert_bin_spec(bin_spec, x, half_bin_onto_borders=False):
    """Convert bin specification to Plotly parameters."""
    x_min, x_max, x_step = _shared_processing.calc_bins(
        x, bin_spec['bin_x_start'], bin_spec['bin_x_stop'], bin_spec['bin_x_number'],
        half_bin_onto_borders)

    plotly_bin_spec = dict(
        xbins=dict(start=x_min, end=x_max, size=x_step),
        autobinx=False
    )
    return plotly_bin_spec


def extract_bin_2d_spec(kwargs):
    """Provide bin properties for x- and y-Axis."""
    given = _parse_spec_kwargs(_args.bins_2d, kwargs)
    return given


def convert_bin_2d_spec(bin_spec, x, y, half_bin_onto_borders=False):
    """Convert bin 2d specification to Plotly parameters."""
    x_min, x_max, x_step = _shared_processing.calc_bins(
        x, bin_spec['bin_x_start'], bin_spec['bin_x_stop'], bin_spec['bin_x_number'],
        half_bin_onto_borders)
    y_min, y_max, y_step = _shared_processing.calc_bins(
        y, bin_spec['bin_y_start'], bin_spec['bin_y_stop'], bin_spec['bin_y_number'],
        half_bin_onto_borders)

    plotly_bin_2d_spec = dict(
        xbins=dict(start=x_min, end=x_max, size=x_step),
        autobinx=False,
        ybins=dict(start=y_min, end=y_max, size=y_step),
        autobiny=False
    )
    return plotly_bin_2d_spec


# -) Camera position
def convert_camera_position(camera_position):
    """Convert the given camera position to a format that can be used by Plotly."""
    if camera_position is None:
        camera_spec = None
    else:
        try:
            upward, center, view = camera_position
            assert len(upward) == len(center) == len(view) == 3
            camera_spec = dict(
                up=dict(x=upward[0], y=upward[1], z=upward[2]),
                center=dict(x=center[0], y=center[1], z=center[2]),
                eye=dict(x=view[0], y=view[1], z=view[2])
            )
        except Exception:
            message = (
                'The provided camera_position could not be interpreted as '
                'three vectors with three entries each.')
            raise ValueError(message) from None
    return camera_spec

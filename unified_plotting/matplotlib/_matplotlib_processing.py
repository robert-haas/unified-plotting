"""Matplotlib-specific processing of function arguments."""

import math as _math
from collections.abc import Iterable as _Iterable
from numbers import Number as _Number

import matplotlib.pyplot as _plt
from matplotlib.colors import LinearSegmentedColormap as _LinearSegmentedColormap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes as _inset_axes
from mpl_toolkits.mplot3d import Axes3D  # required, although not used directly

from .. import _logging
from .._config import config as _config
from .._unified_arguments import arguments as _args
from .._unified_arguments import colormaps as _colormaps
from .._unified_arguments import shared_preprocessing as _shared_preprocessing
from .._unified_arguments import shared_processing as _shared_processing
from .._unified_arguments.injection import _parse_spec_kwargs
from ._data_structures import Figure as _Figure


# 0) External fig and ax objects

def extract_fig_and_ax(kwargs):
    """Extract fig and ax from kwargs."""
    given = _parse_spec_kwargs(_args.external_fig_and_ax, kwargs)
    fig, ax = given['fig'], given['ax']

    if fig is None or ax is None:
        new_fig, new_ax = _plt.subplots()
        if isinstance(fig, _Figure):
            fig = fig.fig
        elif fig is None:
            fig = new_fig
        if ax is None:
            try:
                ax = fig.axes[0]
            except Exception:
                ax = new_ax
    return fig, ax


def extract_fig_and_ax_3d(kwargs):
    """Extract fig and ax (3d) from kwargs.

    References
    ----------
    - https://stackoverflow.com/questions/8510678/trying-to-add-a-3d-subplot-to-a-matplotlib-figure
    """
    given = _parse_spec_kwargs(_args.external_fig_and_ax_3d, kwargs)
    fig, ax = given['fig'], given['ax']

    if fig is None or ax is None:
        if fig is None:
            fig = _plt.figure()
        if ax is None:
            ax = fig.add_subplot(111, projection='3d')  # better behavior than _Axes3D(fig)
    return fig, ax


# I) Plot size

def set_plot_size(kwargs, fig):
    """Set plot size, resolution and margins in fig object.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure.set_size_inches
    - https://matplotlib.org/users/dflt_style_changes.html#figure-size-font-size-and-screen-dpi
    - https://stackoverflow.com/questions/16032389/pad-inches-0-and-bbox-inches-tight-makes-the-plot-smaller-than-declared-figsiz
    - https://matplotlib.org/tutorials/intermediate/tight_layout_guide.html

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

def set_plot_color(kwargs, fig, ax, preserving=False):
    """Set paper and plot color in ax and/or fig objects.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure.set_facecolor

    """
    given = _parse_spec_kwargs(_args.plot_color, kwargs, preserving)

    if given['plot_background_color'] is not None:
        ax.set_facecolor(convert_color(given['plot_background_color']))
    if given['paper_background_color'] is not None:
        fig.set_facecolor(convert_color(given['paper_background_color']))


# III) Plot title

def set_title(kwargs, ax):
    """Set title properties (on/off, font, size, color, location) in ax object.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_title.html

    """
    given = _parse_spec_kwargs(_args.plot_title, kwargs)

    if given['show_title']:
        font_spec = dict(fontname=given['title_font'], fontsize=given['title_size'])
        ax.set_title(
            label=given['title'],
            color=convert_color(given['title_color']),
            loc=given['title_position'],
            fontdict=font_spec
        )


def set_super_title(kwargs, fig):
    """Set super title properties, i.e. a title for a figure with several plots.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.suptitle.html

    """
    given = _parse_spec_kwargs(_args.plot_title, kwargs)

    if given['show_title']:
        if given['title_position'] == 'left':
            x_pos = 0.0
        elif given['title_position'] == 'right':
            x_pos = 1.0
        else:
            x_pos = 0.5

        font_spec = dict(fontname=given['title_font'])

        fig.suptitle(
            given['title'],
            x=x_pos,
            y=1.005 + given['title_size']*0.00115,
            color=given['title_color'],
            fontdict=font_spec,
            fontsize=given['title_size'],
        )


# IV) Axes

def _convert_axis_scale(axis_scale):
    """Convert the given axis scale (e.g. "log") to one that can be used by Matplotlib.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_xscale.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_yscale.html
    - https://matplotlib.org/gallery/lines_bars_and_markers/categorical_variables.html

    """
    possible_axis_scale = ['lin', 'linear', 'log', 'logarithmic', 'cat', 'categorical']
    if axis_scale is None:
        returned_axis_scale = 'linear'
    elif axis_scale in ('linear', 'lin'):
        returned_axis_scale = 'linear'
    elif axis_scale in ('logarithmic', 'log'):
        returned_axis_scale = 'log'
    elif axis_scale in ('categorical', 'cat'):
        returned_axis_scale = 'linear'  # needs to be accomplished via tick values and labels
    else:
        message = 'Invalid value for axis scale: "{}". Possible values: {}'.format(
            axis_scale, possible_axis_scale)
        raise ValueError(message)
    return returned_axis_scale


def _convert_axis_range(axis_range, axis_scale):
    """Convert the given axis range (=start & stop value) to one that can be used by Matplotlib.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_xlim.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_ylim.html

    """
    if axis_range is None:
        axis_range_auto = True
        axis_range_values = None
    else:
        if not isinstance(axis_range, list) or len(axis_range) != 2 or \
                not isinstance(axis_range[0], _Number) or not isinstance(axis_range[1], _Number):
            message = (
                'Invalid value for axis_range: "{}". '
                'Expected a list of two numbers.'.format(axis_range))
            raise ValueError(message)
        start, stop = axis_range
        if start > stop:
            message = (
                'Invalid axis range: Start value ({}) is bigger than the '
                'stop value ({}).'.format(start, stop))
            raise ValueError(message)

        # Matplotlib would require no special treatment for logarithmic axes, only for consistency
        if axis_scale == 'log':
            try:
                _math.log10(start)
            except ValueError:
                message = (
                    'Start value {} is not possible for a logarithmic axis. '
                    'It needs to be greater than zero.'.format(start))
                raise ValueError(message)
            try:
                _math.log10(stop)
            except ValueError:
                message = (
                    'Stop value {} is not possible for a logarithmic axis. '
                    'It needs to be greater than zero.'.format(stop))
                raise ValueError(message)
        axis_range_auto = False
        axis_range_values = [start, stop]
    return axis_range_auto, axis_range_values


def _convert_tick_pos_and_label(tick_position, label):
    """Convert the given tick positions to ones that can be used by Matplotlib.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_xticks.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_yticks.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_xticklabels.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_yticklabels.html

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
            values = ['' if item is None else str(item) for item in values]
        except Exception:
            message = (
                '{} needs to be an Iterable, '
                'e.g. a list, tuple, NumPy array or Pandas Series.'.format(label))
            raise ValueError(message) from None
        return values

    # Tick position
    if tick_position is None:
        try:
            tick_position = list(range(1, len(label) + 1))
        except TypeError:
            tick_position = None
    else:
        tick_position = to_list_of_numbers(tick_position, 'Tick position')
    # Label
    if label is None:
        tick_text = None
    else:
        tick_text = to_list_of_strings(label, 'Label')
    return tick_position, tick_text


def _convert_tick_direction(tick_direction):
    """Convert the given tick direction to one that can be used by Matplotlib.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.tick_params.html

    """
    if tick_direction is None:
        returned_tick_direction = None
    else:
        possible_values = ['in', 'out']
        if tick_direction not in possible_values:
            raise ValueError('Invalid tick direction: "{}"'
                             'Possible values: {}'.format(tick_direction, possible_values))
        if tick_direction == 'in':
            returned_tick_direction = 'in'
        elif tick_direction == 'out':
            returned_tick_direction = 'out'
    return returned_tick_direction


def set_x_axis(kwargs, ax, preserving=False):
    """Set all properties of the x-Axis.

    References
    ----------
    - https://matplotlib.org/api/axes_api.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_xscale.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.tick_params.html
    - http://jonathansoma.com/lede/data-studio/matplotlib/changing-fonts-in-matplotlib
    - http://matplotlib.1069221.n5.nabble.com/MPL-uses-character-not-defined-by-cmr10-td22780.html

    """
    given = _parse_spec_kwargs(_args.x_axis, kwargs, preserving)

    # Axis
    # - visibility
    if not given['show_x_axis']:
        given['show_x_spine'] = False
        given['show_x_title'] = False
        given['show_x_tick'] = False
        given['show_x_label'] = False
    else:
        ax.spines['bottom'].set_position(('outward', given['x_axis_offset']))
    # - color
    if given['x_axis_color'] is not None:
        given['x_spine_color'] = given['x_axis_color']
        given['x_title_color'] = given['x_axis_color']
        given['x_tick_color'] = given['x_axis_color']
        given['x_label_color'] = given['x_axis_color']
    # - scale
    axis_scale = _convert_axis_scale(given['x_axis_scale'])
    ax.set_xscale(axis_scale)
    # - range
    axis_range_auto, axis_range_values = _convert_axis_range(given['x_axis_range'], axis_scale)
    if not axis_range_auto:
        start, stop = axis_range_values
        ax.set_xlim(start, stop)
    # Title
    if given['show_x_title']:
        ax.set_xlabel(
            xlabel=given['x_title'],
            color=convert_color(given['x_title_color']),
            labelpad=given['x_title_offset'],
            fontdict=dict(
                fontname=given['x_title_font'],
                fontsize=given['x_title_size']
            )
        )
    # Spine
    ax.spines['top'].set_visible(False)
    if not given['show_x_spine']:
        ax.spines['bottom'].set_visible(False)
    else:
        ax.spines['bottom'].set_color(convert_color(given['x_spine_color']))
    # Ticks
    ax.tick_params(top=False)
    if not given['show_x_tick']:
        tick_position, tick_label = None, None
        ax.tick_params(bottom=False)
    else:
        tick_position, tick_label = _convert_tick_pos_and_label(
            given['x_tick_position'], given['x_label'])
        if tick_position is not None:
            ax.set_xticks(tick_position)
        if tick_label is not None:
            ax.set_xticklabels(tick_label)
        ax.tick_params(
            axis='x',
            which='major',
            color=convert_color(given['x_tick_color']),
            direction=_convert_tick_direction(given['x_tick_direction']),
            length=given['x_tick_length'],
            width=given['x_tick_width']
        )
        ax.tick_params(
            axis='x',
            which='minor',
            bottom=False, top=False, left=False, right=False,
            labelbottom=False, labeltop=False, labelleft=False, labelright=False
        )
    # Labels
    ax.tick_params(labeltop=False)
    if not given['show_x_label']:
        ax.tick_params(labelbottom=False)
    else:
        ax.tick_params(
            axis='x',
            which='major',
            labelsize=given['x_label_size'],
            labelcolor=convert_color(given['x_label_color'])
        )
        ax.tick_params(
            axis='x',
            which='minor',
            bottom=False, top=False, left=False, right=False,
            labelbottom=False, labeltop=False, labelleft=False, labelright=False
        )
        for tick in ax.get_xticklabels():
            tick.set_fontname(given['x_label_font'])
        if given['x_label_offset'] is not None:
            ax.tick_params(axis='x', pad=given['x_label_offset'])
        if given['x_label_rotation'] is not None:
            ax.tick_params(axis='x', labelrotation=given['x_label_rotation'])
    return tick_position, tick_label


def set_y_axis(kwargs, ax, preserving=False):
    """Set all properties of the y-Axis.

    References
    ----------
    - https://matplotlib.org/api/axes_api.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_xscale.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.tick_params.html
    - http://jonathansoma.com/lede/data-studio/matplotlib/changing-fonts-in-matplotlib
    - http://matplotlib.1069221.n5.nabble.com/MPL-uses-character-not-defined-by-cmr10-td22780.html

    """
    given = _parse_spec_kwargs(_args.y_axis, kwargs, preserving)

    # Axis
    # - visibility
    if not given['show_y_axis']:
        given['show_y_spine'] = False
        given['show_y_title'] = False
        given['show_y_tick'] = False
        given['show_y_label'] = False
    else:
        ax.spines['left'].set_position(('outward', given['y_axis_offset']))
    # - color
    if given['y_axis_color'] is not None:
        given['y_spine_color'] = given['y_axis_color']
        given['y_title_color'] = given['y_axis_color']
        given['y_tick_color'] = given['y_axis_color']
        given['y_label_color'] = given['y_axis_color']
    # - scale
    axis_scale = _convert_axis_scale(given['y_axis_scale'])
    ax.set_yscale(axis_scale)
    # - range
    axis_range_auto, axis_range_values = _convert_axis_range(given['y_axis_range'], axis_scale)
    if not axis_range_auto:
        start, stop = axis_range_values
        ax.set_ylim(start, stop)
    # Title
    if given['show_y_title']:
        ax.set_ylabel(
            ylabel=given['y_title'],
            color=convert_color(given['y_title_color']),
            labelpad=given['y_title_offset'],
            fontdict=dict(
                fontname=given['y_title_font'],
                fontsize=given['y_title_size']
            )
        )
    # Spine
    ax.spines['right'].set_visible(False)
    if not given['show_y_spine']:
        ax.spines['left'].set_visible(False)
    else:
        ax.spines['left'].set_color(convert_color(given['y_spine_color']))
    # Ticks
    ax.tick_params(right=False)
    if not given['show_y_tick']:
        tick_position, tick_label = None, None
        ax.tick_params(left=False)
    else:
        tick_position, tick_label = _convert_tick_pos_and_label(
            given['y_tick_position'], given['y_label'])
        if tick_position is not None:
            ax.set_yticks(tick_position)
        if tick_label is not None:
            ax.set_yticklabels(tick_label)
        ax.tick_params(
            axis='y',
            which='major',
            color=convert_color(given['y_tick_color']),
            direction=_convert_tick_direction(given['y_tick_direction']),
            length=given['y_tick_length'],
            width=given['y_tick_width']
        )
        ax.tick_params(
            axis='y',
            which='minor',
            bottom=False, top=False, left=False, right=False,
            labelbottom=False, labeltop=False, labelleft=False, labelright=False
        )
    # Labels
    ax.tick_params(labelright=False)
    if not given['show_y_label']:
        ax.tick_params(labelleft=False)
    else:
        ax.tick_params(
            axis='y',
            which='major',
            labelsize=given['y_label_size'],
            labelcolor=convert_color(given['y_label_color'])
        )
        ax.tick_params(
            axis='y',
            which='minor',
            bottom=False, top=False, left=False, right=False,
            labelbottom=False, labeltop=False, labelleft=False, labelright=False
        )
        for tick in ax.get_yticklabels():
            tick.set_fontname(given['y_label_font'])
        if given['y_label_offset'] is not None:
            ax.tick_params(axis='y', pad=given['y_label_offset'])
        if given['y_label_rotation'] is not None:
            ax.tick_params(axis='y', labelrotation=given['y_label_rotation'])
    return tick_position, tick_label


def set_x_axis_post_plot(ax, tick_position, tick_label):
    """Set some properties of the x-Axis after a plot was created."""
    if tick_position is not None:
        ax.set_xticks(tick_position)
    if tick_label is not None:
        ax.set_xticklabels(tick_label)


def set_y_axis_post_plot(ax, tick_position, tick_label):
    """Set some properties of the y-Axis after a plot was created."""
    if tick_position is not None:
        ax.set_yticks(tick_position)
    if tick_label is not None:
        ax.set_yticklabels(tick_label)


def set_x_axis_3d(kwargs, ax, preserving=False):
    """Set all properties of the x-Axis in the 3D case.

    References
    ----------
    - https://matplotlib.org/mpl_toolkits/mplot3d/api.html#module-mpl_toolkits.mplot3d.axes3d
    - https://matplotlib.org/api/_as_gen/mpl_toolkits.mplot3d.axes3d.Axes3D.html
    - https://stackoverflow.com/questions/29041326/3d-plot-with-matplotlib-hide-axes-but-keep-axis-labels

    """
    given = _parse_spec_kwargs(_args.x_axis, kwargs, preserving)

    # Axis
    # - visibility
    if not given['show_x_axis']:
        given['show_x_spine'] = False
        given['show_x_title'] = False
        given['show_x_tick'] = False
        given['show_x_label'] = False
    if given['x_axis_offset']:
        _logging.warn_user('Axis offset is currently not available for 3D plots in Matplotlib.')
    # - color
    if given['x_axis_color'] is not None:
        given['x_spine_color'] = given['x_axis_color']
        given['x_title_color'] = given['x_axis_color']
        given['x_tick_color'] = given['x_axis_color']
        given['x_label_color'] = given['x_axis_color']
    # - scale
    axis_scale = _convert_axis_scale(given['x_axis_scale'])
    if axis_scale != 'linear':
        _logging.warn_user('Logarithmic axis scale is currently not available for 3D plots '
                           'in Matplotlib.')
    # - range
    axis_range_auto, axis_range_values = _convert_axis_range(given['x_axis_range'], axis_scale)
    if not axis_range_auto:
        start, stop = axis_range_values
        ax.set_xlim3d(start, stop)
    # Title
    if given['show_x_title']:
        ax.set_xlabel(
            xlabel=given['x_title'],
            color=convert_color(given['x_title_color']),
            labelpad=given['x_title_offset'],
            fontdict=dict(
                fontname=given['x_title_font'],
                fontsize=given['x_title_size']
            )
        )
    # Spine
    if not given['show_x_spine']:
        ax.xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    else:
        ax.xaxis.line.set_color(convert_color(given['x_spine_color']))
    # Ticks
    if not given['show_x_tick']:
        ax.set_xticks([])
    else:
        tick_color = convert_color(given['x_tick_color'])
        tick_position, tick_label = _convert_tick_pos_and_label(
            given['x_tick_position'], given['x_label'])
        tick_direction = _convert_tick_direction(given['x_tick_direction'])
        tick_length = given['x_tick_length']
        tick_width = given['x_tick_width']
        if tick_length is None:
            tick_length = 4

        if tick_color is not None:
            ax.xaxis._axinfo['tick']['color'] = tick_color
        if tick_position is not None:
            ax.set_xticks(tick_position)
        if tick_label is not None:
            ax.set_xticklabels(tick_label)
        if tick_direction == 'in':
            ax.xaxis._axinfo['tick']['inward_factor'] = 0.0
            ax.xaxis._axinfo['tick']['outward_factor'] = tick_length / 20.0
        else:
            ax.xaxis._axinfo['tick']['inward_factor'] = tick_length / 20.0
            ax.xaxis._axinfo['tick']['outward_factor'] = 0.0
        if tick_width is not None:
            ax.xaxis._axinfo['tick']['linewidth'] = tick_width
    # Labels
    ax.tick_params(labeltop=False)
    if not given['show_x_label']:
        ax.tick_params(labelbottom=False)
    else:
        ax.tick_params(
            axis='x',
            which='major',
            labelsize=given['x_label_size'],
            labelcolor=convert_color(given['x_label_color'])
        )
        ax.tick_params(
            axis='x',
            which='minor',
            bottom=False, top=False, left=False, right=False,
            labelbottom=False, labeltop=False, labelleft=False, labelright=False
        )
        for tick in ax.get_xticklabels():
            tick.set_fontname(given['x_label_font'])
        if given['x_label_offset'] is not None:
            ax.tick_params(axis='x', pad=given['x_label_offset'])
        if given['x_label_rotation'] is not None:
            ax.tick_params(axis='x', labelrotation=given['x_label_rotation'])
    # Pane
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))


def set_y_axis_3d(kwargs, ax, preserving=False):
    """Set all properties of the y-Axis in the 3D case.

    References
    ----------
    - https://matplotlib.org/mpl_toolkits/mplot3d/api.html#module-mpl_toolkits.mplot3d.axes3d
    - https://matplotlib.org/api/_as_gen/mpl_toolkits.mplot3d.axes3d.Axes3D.html
    - https://stackoverflow.com/questions/29041326/3d-plot-with-matplotlib-hide-axes-but-keep-axis-labels

    """
    given = _parse_spec_kwargs(_args.y_axis, kwargs, preserving)

    # Axis
    # - visibility
    if not given['show_y_axis']:
        given['show_y_spine'] = False
        given['show_y_title'] = False
        given['show_y_tick'] = False
        given['show_y_label'] = False
    else:
        # ax.spines['left'].set_position(('outward', given['y_axis_offset']))  # TODO: replacement
        pass
    # - color
    if given['y_axis_color'] is not None:
        given['y_spine_color'] = given['y_axis_color']
        given['y_title_color'] = given['y_axis_color']
        given['y_tick_color'] = given['y_axis_color']
        given['y_label_color'] = given['y_axis_color']
    # - scale
    axis_scale = _convert_axis_scale(given['y_axis_scale'])
    if axis_scale != 'linear':
        _logging.warn_user('Logarithmic axis scale is currently not available for 3D plots '
                           'in Matplotlib.')
    # - range
    axis_range_auto, axis_range_values = _convert_axis_range(given['y_axis_range'], axis_scale)
    if not axis_range_auto:
        start, stop = axis_range_values
        ax.set_ylim3d(start, stop)
    # Title
    if given['show_y_title']:
        ax.set_ylabel(
            ylabel=given['y_title'],
            color=convert_color(given['y_title_color']),
            labelpad=given['y_title_offset'],
            fontdict=dict(
                fontname=given['y_title_font'],
                fontsize=given['y_title_size']
            )
        )
    # Spine
    if not given['show_y_spine']:
        ax.yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    else:
        ax.yaxis.line.set_color(convert_color(given['y_spine_color']))
    # Ticks
    if not given['show_y_tick']:
        ax.set_yticks([])
    else:
        tick_color = convert_color(given['y_tick_color'])
        tick_position, tick_label = _convert_tick_pos_and_label(
            given['y_tick_position'], given['y_label'])
        tick_direction = _convert_tick_direction(given['y_tick_direction'])
        tick_length = given['y_tick_length']
        tick_width = given['y_tick_width']
        if tick_length is None:
            tick_length = 4

        if tick_color is not None:
            ax.yaxis._axinfo['tick']['color'] = tick_color
        if tick_position is not None:
            ax.set_yticks(tick_position)
        if tick_label is not None:
            ax.set_yticklabels(tick_label)
        if tick_direction == 'in':
            ax.yaxis._axinfo['tick']['inward_factor'] = 0.0
            ax.yaxis._axinfo['tick']['outward_factor'] = tick_length / 20.0
        else:
            ax.yaxis._axinfo['tick']['inward_factor'] = tick_length / 20.0
            ax.yaxis._axinfo['tick']['outward_factor'] = 0.0
        if tick_width is not None:
            ax.yaxis._axinfo['tick']['linewidth'] = tick_width
    # Labels
    if given['show_y_label']:
        ax.tick_params(
            axis='y',
            which='major',
            labelsize=given['y_label_size'],
            labelcolor=convert_color(given['y_label_color'])
        )
        ax.tick_params(
            axis='y',
            which='minor',
            bottom=False, top=False, left=False, right=False,
            labelbottom=False, labeltop=False, labelleft=False, labelright=False
        )
        for tick in ax.get_yticklabels():
            tick.set_fontname(given['y_label_font'])
        if given['y_label_offset'] is not None:
            ax.tick_params(axis='y', pad=given['y_label_offset'])
        if given['y_label_rotation'] is not None:
            ax.tick_params(axis='y', labelrotation=given['y_label_rotation'])
    # Pane
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))


def set_z_axis_3d(kwargs, ax, preserving=False):
    """Set all properties of the z-Axis in the 3D case.

    References
    ----------
    - https://matplotlib.org/mpl_toolkits/mplot3d/api.html#module-mpl_toolkits.mplot3d.axes3d
    - https://matplotlib.org/api/_as_gen/mpl_toolkits.mplot3d.axes3d.Axes3D.html
    - https://stackoverflow.com/questions/29041326/3d-plot-with-matplotlib-hide-axes-but-keep-axis-labels
    - http://matplotlib.1069221.n5.nabble.com/setting-ticks-on-Axes3D-td20359.html

    """
    given = _parse_spec_kwargs(_args.z_axis, kwargs, preserving)

    # Axis
    # - visibility
    if not given['show_z_axis']:
        given['show_z_spine'] = False
        given['show_z_title'] = False
        given['show_z_tick'] = False
        given['show_z_label'] = False
    else:
        # ax.spines['left'].set_position(('outward', given['z_axis_offset']))  # TODO: replacement
        pass
    # - color
    if given['z_axis_color'] is not None:
        given['z_spine_color'] = given['z_axis_color']
        given['z_title_color'] = given['z_axis_color']
        given['z_tick_color'] = given['z_axis_color']
        given['z_label_color'] = given['z_axis_color']
    # - scale
    axis_scale = _convert_axis_scale(given['z_axis_scale'])
    if axis_scale != 'linear':
        _logging.warn_user('Logarithmic axis scale is currently not available for 3D plots '
                           'in Matplotlib.')
    # - range
    axis_range_auto, axis_range_values = _convert_axis_range(given['z_axis_range'], axis_scale)
    if not axis_range_auto:
        start, stop = axis_range_values
        ax.set_zlim3d(start, stop)
    # Title
    if given['show_z_title']:
        ax.set_zlabel(
            zlabel=given['z_title'],
            color=convert_color(given['z_title_color']),
            labelpad=given['z_title_offset'],
            fontdict=dict(
                fontname=given['z_title_font'],
                fontsize=given['z_title_size']
            )
        )
    # Spine
    if not given['show_z_spine']:
        ax.zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    else:
        ax.zaxis.line.set_color(convert_color(given['z_spine_color']))
    # Ticks
    if not given['show_z_tick']:
        ax.set_zticks([])
    else:
        tick_color = convert_color(given['z_tick_color'])
        tick_position, tick_label = _convert_tick_pos_and_label(
            given['z_tick_position'], given['z_label'])
        tick_direction = _convert_tick_direction(given['z_tick_direction'])
        tick_length = given['z_tick_length']
        tick_width = given['z_tick_width']
        if tick_length is None:
            tick_length = 4

        if tick_color is not None:
            ax.zaxis._axinfo['tick']['color'] = tick_color
        if tick_position is not None:
            ax.set_zticks(tick_position)
        if tick_label is not None:
            ax.set_zticklabels(tick_label)
        if tick_direction == 'in':
            ax.zaxis._axinfo['tick']['inward_factor'] = 0.0
            ax.zaxis._axinfo['tick']['outward_factor'] = tick_length / 20.0
        else:
            ax.zaxis._axinfo['tick']['inward_factor'] = tick_length / 20.0
            ax.zaxis._axinfo['tick']['outward_factor'] = 0.0
        if tick_width is not None:
            ax.zaxis._axinfo['tick']['linewidth'] = tick_width
    # Labels
    if given['show_z_label']:
        ax.tick_params(
            axis='z',
            which='major',
            labelsize=given['z_label_size'],
            labelcolor=convert_color(given['z_label_color'])
        )
        ax.tick_params(
            axis='z',
            which='minor',
            bottom=False, top=False, left=False, right=False,
            labelbottom=False, labeltop=False, labelleft=False, labelright=False
        )
        for tick in ax.get_zticklabels():
            tick.set_fontname(given['z_label_font'])
        if given['z_label_offset'] is not None:
            ax.tick_params(axis='z', pad=given['z_label_offset'])
        if given['z_label_rotation'] is not None:
            ax.tick_params(axis='z', labelrotation=given['z_label_rotation'])
    # Pane
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))


# V) Grid

def set_grid(kwargs, ax, preserving=False):
    """Set grid properties: on/off, color, style, width.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.grid.html

    """
    given_x = _parse_spec_kwargs(_args.x_grid, kwargs, preserving)
    given_y = _parse_spec_kwargs(_args.y_grid, kwargs, preserving)

    if given_x['show_x_grid']:
        ax.grid(
            axis='x',
            color=convert_color(given_x['x_grid_color']),
            linestyle=_convert_line_style(given_x['x_grid_style']),
            linewidth=given_x['x_grid_width']
        )

    if given_y['show_y_grid']:
        ax.grid(
            axis='y',
            color=convert_color(given_y['y_grid_color']),
            linestyle=_convert_line_style(given_y['y_grid_style']),
            linewidth=given_y['y_grid_width']
        )


def set_grid_3d(kwargs, ax, preserving=False):
    """Set grid properties: on/off, color, style, width.

    References
    ----------
    - https://stackoverflow.com/questions/15611726/matplotlib-mplot3d-label-and-ticks-overlapping-when-using-latex-labels

    """
    # TODO: private _axinfo attribute may be discontinued, find another way if there's one.

    given_x = _parse_spec_kwargs(_args.x_grid, kwargs, preserving)
    given_y = _parse_spec_kwargs(_args.y_grid, kwargs, preserving)
    given_z = _parse_spec_kwargs(_args.z_grid, kwargs, preserving)

    ax.xaxis.gridlines.set_visible(given_x['show_x_grid'])
    if given_x['show_x_grid']:
        if given_x['x_grid_color'] is not None:
            ax.xaxis._axinfo['grid']['color'] = given_x['x_grid_color']
        if given_x['x_grid_width'] is not None:
            ax.xaxis._axinfo['grid']['linewidth'] = given_x['x_grid_width']
        if given_x['x_grid_style'] is not None:
            ax.xaxis._axinfo['grid']['linestyle'] = _convert_line_style(given_x['x_grid_style'])

    ax.yaxis.gridlines.set_visible(given_y['show_y_grid'])
    if given_y['show_y_grid']:
        if given_y['y_grid_color'] is not None:
            ax.yaxis._axinfo['grid']['color'] = given_y['y_grid_color']
        if given_y['y_grid_width'] is not None:
            ax.yaxis._axinfo['grid']['linewidth'] = given_y['y_grid_width']
        if given_y['y_grid_style'] is not None:
            ax.yaxis._axinfo['grid']['linestyle'] = _convert_line_style(given_y['y_grid_style'])

    ax.zaxis.gridlines.set_visible(given_z['show_z_grid'])
    if given_z['show_z_grid']:
        if given_z['z_grid_color'] is not None:
            ax.zaxis._axinfo['grid']['color'] = given_z['z_grid_color']
        if given_z['z_grid_width'] is not None:
            ax.zaxis._axinfo['grid']['linewidth'] = given_z['z_grid_width']
        if given_z['z_grid_style'] is not None:
            ax.zaxis._axinfo['grid']['linestyle'] = _convert_line_style(given_z['z_grid_style'])


# VI) Legend

def extract_legend(kwargs, preserving=False):
    """Get legend properties: on/off.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.legend.html

    """
    return _parse_spec_kwargs(_args.legend, kwargs, preserving)


def set_legend(kwargs, ax):
    """Set legend properties.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html
    - https://github.com/matplotlib/matplotlib/issues/8699
    - https://stackoverflow.com/questions/15637961/matplotlib-alignment-of-legend-title

    """
    legend_spec = extract_legend(kwargs)
    if legend_spec['show_legend']:
        # Title
        title = legend_spec['legend_title']
        # Text: Color, size, fontconvert_colorlegend_spec
        font_spec = dict(
            family=legend_spec['legend_font'],
            size=legend_spec['legend_size'],
        )
        font_color = convert_color(legend_spec['legend_color'])
        # Symbol size
        # markerscale = ...  TODO: Decide whether it is desirable to modify it
        # Background color
        background_color = convert_color(legend_spec['legend_background_color'])
        # Position: horizontal, vertical
        if legend_spec['legend_position_horizontal'] == 'left':
            pos_h = 'left'
        elif legend_spec['legend_position_horizontal'] == 'center':
            pos_h = 'center'
        elif legend_spec['legend_position_horizontal'] == 'right':
            pos_h = 'right'
        else:
            message = ('Unknown value for legend_position_horizontal. '
                       'Possible values: "left", "center", "right".')
            raise ValueError(message)
        if legend_spec['legend_position_vertical'] == 'top':
            pos_v = 'upper'
        elif legend_spec['legend_position_vertical'] == 'center':
            pos_v = 'center'
        elif legend_spec['legend_position_vertical'] == 'bottom':
            pos_v = 'lower'
        else:
            message = ('Unknown value for legend_position_vertical. '
                       'Possible values: "top", "center", "bottom".')
            raise ValueError(message)
        position = '{} {}'.format(pos_v, pos_h)
        if position == 'center center':
            position = 'center'
        # Border: size, color
        border_size = legend_spec['legend_border_size']
        border_color = convert_color(legend_spec['legend_border_color'])

        # Set most properties via ax.legend()
        legend = ax.legend(
            title=title,
            loc=position,
            prop=font_spec,
            framealpha=1.0,
            edgecolor=border_color,
            facecolor=background_color,
            frameon=True,
            shadow=False,
            fancybox=False,
            borderpad=0.6 + border_size / 20.0,  # from trial and error with visual appearance
            markerscale=1.5,
            markerfirst=True,
        )
        legend._legend_box.align = 'left'  # Legend title alignment
        # Set other properties for which no argument is available in ax.legend
        # - Marker size: fixed
        # https://stackoverflow.com/questions/24706125/setting-a-fixed-size-for-points-in-legend
        try:
            legend_marker_size = _convert_marker_size(legend_spec['legend_marker_size'])
            if isinstance(legend_marker_size, _Number):
                for handle in legend.legendHandles:
                    handle.set_sizes([legend_marker_size])
            else:
                for i, handle in enumerate(legend.legendHandles):
                    try:
                        lms_i = legend_marker_size[i]
                    except Exception:
                        lms_i = 16.0
                    handle.set_sizes([lms_i])
        except Exception:
            pass
        # - Font color
        try:
            for legend_text in legend.get_texts():
                legend_text.set_color(font_color)
        except Exception:
            pass
        # - Title size, color and font
        try:
            legend_title = legend.get_title()
            legend_title.set_fontsize(legend_spec['legend_size'])
            legend_title.set_color(font_color)
            legend_title.set_family(legend_spec['legend_font'])
        except Exception:
            pass
        # - Border size
        try:
            legend_frame = legend.get_frame()
            legend_frame.set_linewidth(border_size)
        except Exception:
            pass
        # - zorder, to be drawn in front of everything else, especially due to scatter plot zorder
        legend.set_zorder(20)


# VII) Colormap

def extract_colormap_spec(kwargs, preserving=False):
    """Extract colormap properties from kwargs: colormap, reversed, colorbar on/off."""
    given = _parse_spec_kwargs(_args.colormap, kwargs, preserving)
    return given


def _convert_colormap(given_colormap):
    """Convert the given colormap into one that can be used by Matplotlib.

    References
    ----------
    - https://matplotlib.org/api/pyplot_summary.html#colors-in-matplotlib
    - https://matplotlib.org/api/cm_api.html
    - https://matplotlib.org/tutorials/index.html#tutorials-colors
    - https://matplotlib.org/tutorials/colors/colormaps.html#sphx-glr-tutorials-colors-colormaps-py

    """
    # TODO: check non-string colormaps for validity too

    if isinstance(given_colormap, str):
        cm_str_lower = given_colormap.lower()
        if cm_str_lower in _colormaps.MATPLOTLIB_BUILTIN_COLORMAPS:
            colormap = _colormaps.MATPLOTLIB_BUILTIN_COLORMAPS[cm_str_lower]
        elif cm_str_lower in _colormaps.MATPLOTLIB_EXTERNAL_COLORMAPS:
            colormap_values = _colormaps.MATPLOTLIB_EXTERNAL_COLORMAPS[cm_str_lower]
            colormap = _LinearSegmentedColormap.from_list(
                name=given_colormap, colors=colormap_values)
        else:
            colormap = _config.settings.colormap
            message = (
                'Colormap "{}" was not recognized. '
                'Using default colormap "{}" instead.'.format(given_colormap, colormap))
            _logging.warn_user(message)
    else:
        colormap = given_colormap
    return colormap


def convert_colormap_spec(given_colormap_spec):
    """Convert a general colormap spec into one that can be used by Matplotlib."""
    colormap = _plt.cm.get_cmap(_convert_colormap(given_colormap_spec['colormap']))
    if given_colormap_spec['colormap_reversed']:
        colormap = colormap.reversed()
    mpl_colormap_spec = dict(
        cmap=colormap,
        show_colormap=given_colormap_spec['show_colormap'],
        colormap_label_font=given_colormap_spec['colormap_label_font'],
        colormap_label_size=given_colormap_spec['colormap_label_size'],
        colormap_label_color=given_colormap_spec['colormap_label_color'],
        colormap_border_size=given_colormap_spec['colormap_border_size'],
    )
    return mpl_colormap_spec


def set_colormap_properties(ax, collection, mpl_colormap_spec):
    """Set the appearance of a colormap (colorbar).

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.inset_axes.html
    - https://matplotlib.org/api/_as_gen/mpl_toolkits.axes_grid1.inset_locator.inset_axes.html
    - https://stackoverflow.com/questions/15003353/why-does-my-colorbar-have-lines-in-it

    """
    width_mm = 8.0
    width_inch = width_mm / 25.4
    cax = _inset_axes(
        ax,
        width=width_inch,
        height='100%',
        loc='upper left',
        bbox_to_anchor=(1.012, 0.0, 1.0, 1.0),
        bbox_transform=ax.transAxes,
        borderpad=0,
    )
    color_bar = _plt.colorbar(collection, cax=cax)
    color_bar.solids.set_edgecolor('face')  # fixes a problem with discrete lines in colorbar
    color_bar.set_alpha(1.0)
    color_bar.draw_all()
    color_bar.outline.set_linewidth(mpl_colormap_spec['colormap_border_size'])
    for label in color_bar.ax.yaxis.get_ticklabels():
        label.set_family(mpl_colormap_spec['colormap_label_font'])
        label.set_size(mpl_colormap_spec['colormap_label_size'])
        label.set_color(mpl_colormap_spec['colormap_label_color'])


# VIII) Markers

def extract_marker_spec(kwargs):
    """Extract marker properties from kwargs.

    References
    ----------
    - https://matplotlib.org/api/markers_api.html#module-matplotlib.markers

    """
    given = _parse_spec_kwargs(_args.markers, kwargs)
    return given


def _convert_marker_style(given_style):
    """Convert a general marker style into one that can be used by Matplotlib.

    References
    ----------
    - https://matplotlib.org/api/markers_api.html#module-matplotlib.markers

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
    _shared_preprocessing.check_categorical_argument(given_style, 'marker_style', possible_values)

    # Transformation
    conversion_map = {
        'o': 'o',
        'circle': 'o',
        '.': '.',
        'point': '.',
        'dot': '.',
        't': '^',
        '3': '^',
        'triangle': '^',
        's': 's',
        '4': 's',
        'square': 's',
        'p': 'p',
        '5': 'p',
        'pentagon': 'p',
        'h': 'h',
        '6': 'h',
        'hexagon': 'h',
        '8': '8',
        'octagon': '8',
        '*': '*',
        'star': '*',
        '+': '+',
        'plus': '+',
        'x': 'x',
        'cross': 'x',
        'd': 'D',
        'diamond': 'D',
        '-': '_',
        '_': '_',
        'horizontal_line': '|',
        '|': '|',
        'vertical_line': '_',
        '^': '^',
        'triangle_up': '^',
        'v': 'v',
        'triangle_down': 'v',
        '<': '<',
        'triangle_left': '<',
        '>': '>',
        'triangle_right': '>',
    }
    returned_style = conversion_map[given_style]
    return returned_style


def _convert_marker_size(given):
    """Convert marker size so that a number of 30 means width and height of the marker in points.

    References
    ----------
    - https://stackoverflow.com/questions/14827650/pyplot-scatter-plot-marker-size

    Notes
    -----
    Measurements: Set marker size as number, export plot as SVG, open in Inkscape, measure height
    - number 10  -> height 3,162 pt = 4,216 px = 1,115 mm   -- where sqrt(10) = 3.1622
    - number 20  -> height 4,472 pt = 5,963 px = 1,578 mm   -- where sqrt(20) = 4.4721
    - number 30  -> height 5,477 pt = 7,303 px = 1,932 mm   -- where sqrt(30) = 5.4772
    - number 40  -> height 6,325 pt = 8,433 px = 2,231 mm   -- where sqrt(40) = 6.3245
    - number 100 -> height 10,001 pt = 13,333 px = 3,528 mm -- where sqrt(100) = 10

    Conclusion: Matplotlib takes sqrt of the given number and uses it as width and height in pt.

    """
    result = None
    if isinstance(given, _Number):
        result = given**2
    else:
        try:
            result = [val**2 for val in given]
        except Exception:
            pass
    if result is None:
        message = 'Failed to convert marker size into width_pt and height_pt: {}'.format(given)
        raise ValueError(message)
    return result


def convert_marker_spec(marker_spec):
    """Convert a general marker spec into one that can be used by Matplotlib.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.scatter.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.scatter.html

    """
    # To prevent a warning that a tuple could stand for RGB/RGBA or individual numbers
    color = convert_color(marker_spec['marker_color'])
    if isinstance(color, tuple) and len(color) in [3, 4]:
        color = [color]
        colormap = None
    else:
        colormap = _convert_colormap(marker_spec['marker_colormap'])

    # Conversion
    mpl_marker_spec = dict(
        c=color,
        cmap=colormap,
        s=_convert_marker_size(marker_spec['marker_size']),
        alpha=marker_spec['marker_opacity'],
        marker=_convert_marker_style(marker_spec['marker_style']),
        linewidths=0.0,
    )
    show_marker = marker_spec['show_marker']
    return mpl_marker_spec, show_marker


# IX) Lines

def extract_line_spec(kwargs):
    """Extract line properties from kwargs."""
    given = _parse_spec_kwargs(_args.lines, kwargs)
    return given


def _convert_line_style(given_style):
    """Convert the given line style to one that can be used by Matplotlib.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D.set_linestyle
    - https://matplotlib.org/gallery/lines_bars_and_markers/line_styles_reference.html

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
        returned_style = 'dashed'
    elif given_style in ('dashdot', '-.', '.-'):
        returned_style = 'dashdot'
    else:
        returned_style = 'dotted'
    return returned_style


def convert_line_spec(line_spec):
    """Convert a general line spec into one that can be used by Matplotlib.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.plot.html#matplotlib.axes.Axes.plot

    """
    # TODO: find solution for opacity of lines, or remove it

    line_color = convert_color(line_spec['line_color'])
    if not isinstance(line_color, (str, tuple)):
        line_color = 'black'  # because numerical line color is a problem in Matplotlib

    # Parameters for plot()
    mpl_line_spec = dict(
        marker=None,
        color=line_color,
        linewidth=line_spec['line_width'],
        linestyle=_convert_line_style(line_spec['line_style']),
        # cmap=convert_colormap(line_spec['line_colormap']),
        alpha=line_spec['line_opacity'],
    )
    show_line = line_spec['show_line']
    return mpl_line_spec, show_line


# X) Rugs

def get_rugs(kwargs, ax, preserving=False):
    """Extract rugs from kwargs."""
    # TODO: maybe replace by markers
    #       - is there a plot where both markers and rugs are present?
    #       - is there a plot where rugs can only take a subset of marker forms?

    given = _parse_spec_kwargs(_args.rugs, kwargs, preserving)
    return given


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
    """Convert a general x error spec into one that can be used by Matplotlib."""
    mpl_x_error_spec = dict(
        ecolor=convert_color(x_error_spec['x_error_bar_color']),
        elinewidth=x_error_spec['x_error_bar_line_width'],
        capthick=x_error_spec['x_error_bar_line_width'],
        capsize=x_error_spec['x_error_bar_size'],
    )
    show_x_error_bar = x_error_spec['show_x_error_bar']
    return mpl_x_error_spec, show_x_error_bar


def convert_y_error_spec(y_error_spec):
    """Convert a general y error spec into one that can be used by Matplotlib."""
    # 1) Error bar
    show_y_error_bar = y_error_spec['show_y_error_bar']
    mpl_y_error_bar_spec = dict(
        ecolor=convert_color(y_error_spec['y_error_bar_color']),
        elinewidth=y_error_spec['y_error_bar_line_width'],
        capthick=y_error_spec['y_error_bar_line_width'],
        capsize=y_error_spec['y_error_bar_size'],
    )
    # 2) Error band
    show_y_error_band = y_error_spec['show_y_error_band']
    band_opacity = y_error_spec['y_error_band_opacity']
    if isinstance(band_opacity, _Number):
        if band_opacity < 0.0:
            band_opacity = 0.0
        if band_opacity > 1.0:
            band_opacity = 1.0
    mpl_y_error_band_spec = dict(
        color=convert_color(y_error_spec['y_error_band_color']),
        alpha=band_opacity,
        linewidth=0.0,
    )
    return mpl_y_error_bar_spec, show_y_error_bar, mpl_y_error_band_spec, show_y_error_band


# -) Color

def convert_color(given_color):
    """Convert the given color to one that can be used by Matplotlib.

    Accepts a color in one of several commonly used formats:
    name, hex, rgb str, rgb tuple, rgba str, rgba tuple

    References
    ----------
    - https://matplotlib.org/users/colors.html
    - https://matplotlib.org/gallery/color/named_colors.html

    """
    try:
        rgba_tuple = _shared_processing.normalize_color(given_color)
        scaled_rgba_tuple = (
            float(rgba_tuple[0] / 255.0),
            float(rgba_tuple[1] / 255.0),
            float(rgba_tuple[2] / 255.0),
            float(rgba_tuple[3])
        )
        return scaled_rgba_tuple
    except ValueError:
        if not isinstance(given_color, tuple) and \
                isinstance(given_color, _Iterable) and isinstance(given_color[0], _Number):
            return given_color
        raise


# -) Bins

def extract_bin_spec(kwargs):
    """Provide bin properties for x-Axis."""
    given = _parse_spec_kwargs(_args.bins, kwargs)
    return given


def convert_bin_spec(bin_spec, x, half_bin_onto_borders=False):
    """Convert bin specification to Matplotlib parameters."""
    x_min, x_max, x_step = _shared_processing.calc_bins(
        x, bin_spec['bin_x_start'], bin_spec['bin_x_stop'], bin_spec['bin_x_number'],
        half_bin_onto_borders)
    x_num = bin_spec['bin_x_number']

    mpl_bin_spec = dict(
        range=(x_min, x_max),
        bins=x_num
    )
    return mpl_bin_spec


def extract_bin_2d_spec(kwargs):
    """Provide bin properties for x- and y-Axis."""
    given = _parse_spec_kwargs(_args.bins_2d, kwargs)
    return given


def convert_bin_2d_spec(bin_spec, x, y, target, half_bin_onto_borders=False):
    """Convert bin 2d specification to Matplotlib parameters."""
    # TODO: Why is the used heuristic correction necessary? Can it be done better?

    x_min, x_max, x_step = _shared_processing.calc_bins(
        x, bin_spec['bin_x_start'], bin_spec['bin_x_stop'], bin_spec['bin_x_number'],
        half_bin_onto_borders)
    y_min, y_max, y_step = _shared_processing.calc_bins(
        y, bin_spec['bin_y_start'], bin_spec['bin_y_stop'], bin_spec['bin_y_number'],
        half_bin_onto_borders)
    x_num = bin_spec['bin_x_number']
    y_num = bin_spec['bin_y_number']

    if target == 'hexbin':
        if y_num < 4:
            correction = 1
        elif y_num < 6:
            correction = 2
        elif y_num < 8:
            correction = 3
        else:
            correction = int(y_num/2-1)

        mpl_bin_spec = dict(
            extent=(x_min, x_max, y_min, y_max),
            gridsize=(x_num, y_num-correction)
        )
    elif target == 'hist2d':
        mpl_bin_spec = dict(
            range=[[x_min, x_max], [y_min, y_max]],
            bins=[x_num, y_num]
        )
    return mpl_bin_spec

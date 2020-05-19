"""Plotly plots for n-dimensional vector data."""

from numbers import Number as _Number

import numpy as _np
import plotly.figure_factory as _figure_factory
import plotly.graph_objs as _go

from .. import _logging
from .._config import config as _config
from .._unified_arguments import arguments as _args
from .._unified_arguments import shared_preprocessing as _shared_preprocessing
from .._unified_arguments import shared_processing as _shared_processing
from .._unified_arguments.injection import inject_functions as _inject_functions
from . import _plotly_processing, _plots_2d
from ._data_structures import Figure as _Figure


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid,
                   _args.rugs)
def band(data, name=None, color=None, opacity=None, show_mean=False, **kwargs):
    """Create a plot showing statistics (min, max, mean, median, ...) as lines between axes.

    Parameters
    ----------
    data : list of lists, pandas DataFrame, or filepath of a CSV file
        A list of lists. Each list may have a different number of items.
        If a list contains a non-numerical item (str, None, ...),
        the entire list will be removed automatically and a warning will be shown.
        If a list contains a numerical but non-finite item (NaN, +Inf, -Inf),
        the individual entry will be removed automatically and a warning will be shown.
    name : list
        Name(s) of the visualized data series. Used as axis description.
    color : str, tuple or list
        Color(s) for the plot elements, in this case the lines and fillings in between them.
        Possible values: See :ref:`colors`.
    opacity : float
        Opacity of the plot elements, in this case the lines and fillings in between them.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    show_mean : bool
        Show or hide a dashed mean line.

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://plot.ly/python/reference/#scatter
    - https://docs.scipy.org/doc/numpy/reference/routines.statistics.html
    - https://docs.scipy.org/doc/scipy/reference/stats.html

    Examples
    --------
    - https://plot.ly/python/continuous-error-bars

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    data, name = _shared_preprocessing.prepare_vector_data_nd_stats(data, name, kwargs)

    # Argument processing
    data = _np.array(data)
    x = _shared_processing.get_all_names(name, len(data))

    # Layout
    layout = _go.Layout()
    size_spec = _plotly_processing.set_plot_size(kwargs, layout)
    _plotly_processing.set_plot_color(kwargs, layout)
    _plotly_processing.set_title(kwargs, layout)
    _plotly_processing.set_x_axis(kwargs, layout)
    _plotly_processing.set_y_axis(kwargs, layout)
    _plotly_processing.set_grid(kwargs, layout)

    # Data
    name_i = _shared_processing.get_next_name(name, i=0)
    color_i = _shared_processing.get_next_color(color, i=0)
    color_i = _plotly_processing.convert_color(color_i)
    opacity_i = _shared_processing.get_next_opacity(opacity, i=0)
    rug_spec = _plotly_processing.extract_rug_spec(kwargs)
    rug_spec_i = _shared_processing.get_next_rug_spec(rug_spec, color_i, opacity_i, None, i=0)
    plotly_rug_spec, show_rug = _plotly_processing.convert_rug_spec(rug_spec_i)

    y_stats = dict(min=[], lower_quartile=[], median=[], mean=[], upper_quartile=[], max=[],
                   std=[], var=[])
    for i, series in enumerate(data):
        # Measures of location
        y_stats['min'].append(_np.nanmin(series))
        y_stats['lower_quartile'].append(_np.nanpercentile(series, q=25, interpolation='nearest'))
        y_stats['median'].append(_np.nanpercentile(series, q=50, interpolation='nearest'))
        y_stats['mean'].append(_np.nanmean(series))
        y_stats['upper_quartile'].append(_np.nanpercentile(series, q=75, interpolation='nearest'))
        y_stats['max'].append(_np.nanmax(series))

        # Measures of dispersion
        y_stats['std'].append(_np.nanstd(series))
        y_stats['var'].append(_np.nanvar(series))

    linewidth = 0.8
    linecolor = color_i
    trace_max = _go.Scatter(
        x=x,
        y=y_stats['max'],
        name='Maximum',
        mode='lines',
        line=dict(width=linewidth*2, color=linecolor),
        opacity=opacity_i,
        showlegend=False,
    )
    trace_min = _go.Scatter(
        x=x,
        y=y_stats['min'],
        fill='tonexty',
        name='Minimum',
        mode='lines',
        line=dict(width=linewidth*2, color=linecolor),
        opacity=opacity_i,
        showlegend=False,
    )
    trace_upper_quartile = _go.Scatter(
        x=x,
        y=y_stats['upper_quartile'],
        name='Upper quartile',
        mode='lines',
        line=dict(width=linewidth, color=linecolor),
        opacity=opacity_i,
        showlegend=False,
    )
    trace_lower_quartile = _go.Scatter(
        x=x,
        y=y_stats['lower_quartile'],
        fill='tonexty',
        name='Lower quartile',
        mode='lines',
        line=dict(width=linewidth, color=linecolor),
        opacity=opacity_i,
        showlegend=False,
    )
    trace_median = _go.Scatter(
        x=x,
        y=y_stats['median'],
        name='Median',
        mode='lines',
        line=dict(width=linewidth*2, color=linecolor),
        opacity=opacity_i,
        showlegend=False,
    )
    plotly_data = [trace_max, trace_min, trace_upper_quartile, trace_lower_quartile, trace_median]

    if show_mean:
        trace_mean = _go.Scatter(
            x=x,
            y=y_stats['mean'],
            name='Mean',
            mode='lines',
            line=dict(width=linewidth, color=linecolor, dash='dash'),
            opacity=opacity_i,
            showlegend=False,
        )
        plotly_data.append(trace_mean)

    del plotly_rug_spec['colorscale']
    if show_rug:
        x_points, y_points = [], []
        for i, series in enumerate(data):
            name_i = _shared_processing.get_next_name(name, i)
            for val in series:
                x_points.append(name_i)
                y_points.append(val)
        trace_markers = _go.Scatter(
            x=x_points,
            y=y_points,
            mode='markers',
            marker=plotly_rug_spec,
            opacity=opacity_i,
            showlegend=False,
        )
        plotly_data.append(trace_markers)

    # Figure
    fig = _go.Figure(data=plotly_data, layout=layout)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid,
                   _args.rugs)
def box(data, name=None, color=None, opacity=None, box_width=None, orientation='vertical',
        show_mean=False, show_notch=False, point_jitter=0.0, point_position=-1.6,
        **kwargs):
    """Create a box plot.

    Parameters
    ----------
    data : list of lists, pandas DataFrame, or filepath of a CSV file
        A list of lists. Each list may have a different number of items.
        If a list contains a non-numerical item (str, None, ...),
        the entire list will be removed automatically and a warning will be shown.
        If a list contains a numerical but non-finite item (NaN, +Inf, -Inf),
        the individual entry will be removed automatically and a warning will be shown.
    name : list
        Name(s) of the visualized data series. Used as axis description.
    color : str, tuple or list
        Color(s) of the plot elements, in this case the boxes.
        Possible values: See :ref:`colors`.
    opacity : float
        Opacity of the plot elements, in this case the boxes.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    box_width : float
        Width of the boxes.
    orientation : str
        Orientation of the boxes. Possible values: "vertical", "horizontal"
    show_mean : bool
        Show or hide a dashed line in the box to represent the mean value.
    show_notch : bool
        Show or hide notches in the box to highlight the median value.
    point_jitter : float
        Amount of random jitter applied to the points.
        Possible values: Positive float numbers, e.g. 0.0 (=no jitter) and 1.0 (=jitter amount
        of box width)
    point_position : float
        Position of sample points relative to boxes.

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://plot.ly/python/reference/#box

    Examples
    --------
    - https://plot.ly/python/box-plots
    - https://help.plot.ly/what-is-a-box-plot

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    data, name = _shared_preprocessing.prepare_vector_data_nd_stats(data, name, kwargs)

    # Argument processing
    _shared_preprocessing.check_categorical_argument(
        orientation, 'orientation', ['vertical', 'horizontal'])
    orientation = 'v' if orientation == 'vertical' else 'h'
    original_rug_style = kwargs['rug_style']

    # Layout
    layout = _go.Layout(showlegend=False)
    size_spec = _plotly_processing.set_plot_size(kwargs, layout)
    _plotly_processing.set_plot_color(kwargs, layout)
    _plotly_processing.set_title(kwargs, layout)
    _plotly_processing.set_x_axis(kwargs, layout)
    _plotly_processing.set_y_axis(kwargs, layout)
    _plotly_processing.set_grid(kwargs, layout)

    # Data
    rug_spec = _plotly_processing.extract_rug_spec(kwargs)
    plotly_data = []
    for i, series in enumerate(data):
        used_series = dict(x=series) if orientation == 'h' else dict(y=series)
        name_i = _shared_processing.get_next_name(name, i)
        color_i = _shared_processing.get_next_color(color, i)
        color_i = _plotly_processing.convert_color(color_i)
        opacity_i = _shared_processing.get_next_opacity(opacity, i)
        plotly_colormap = None
        rug_spec_i = _shared_processing.get_next_rug_spec(
            rug_spec, color_i, opacity_i, plotly_colormap, i)
        if orientation == 'h' and original_rug_style is None and rug_spec_i['rug_style'] == "-":
            rug_spec_i['rug_style'] = "|"
        plotly_rug_spec, show_rug = _plotly_processing.convert_rug_spec(rug_spec_i)

        marker_spec = dict(symbol=141, size=5, opacity=opacity_i/3)
        if show_rug:
            boxpoints = 'all'
            marker_spec['color'] = plotly_rug_spec['color']
            marker_spec['size'] = plotly_rug_spec['size']
            marker_spec['opacity'] = plotly_rug_spec['opacity']
            marker_spec['symbol'] = plotly_rug_spec['symbol']
        else:
            boxpoints = False
        trace = _go.Box(
            **used_series,
            name=name_i,
            fillcolor=color_i,
            opacity=opacity_i,
            marker=marker_spec,
            width=box_width,
            orientation=orientation,
            boxpoints=boxpoints,
            boxmean=show_mean,
            notched=show_notch,
            jitter=point_jitter,
            pointpos=point_position,
            line=dict(
                color='black',
                width=1
            ),
        )
        plotly_data.append(trace)

    # Figure
    fig = _go.Figure(data=plotly_data, layout=layout)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.x_axis, _args.y_axis,
                   _args.legend, _args.bins)
def density(data, name=None, color=None, opacity=None,
            show_density=True, show_histogram=True, show_rug=True,
            **kwargs):
    """Create a density plot.

    Parameters
    ----------
    data : list of lists, pandas DataFrame, or filepath of a CSV file
        A list of lists. Each list may have a different number of items.
        If a list contains a non-numerical item (str, None, ...),
        the entire list will be removed automatically and a warning will be shown.
        If a list contains a numerical but non-finite item (NaN, +Inf, -Inf),
        the individual entry will be removed automatically and a warning will be shown.
    name : list
        Name(s) of the visualized data series. Used as axis description.
    color : str, tuple or list
        Color(s) of the plot elements, in this case the density lines, rugs and bars.
        Possible values: See :ref:`colors`.
    opacity : float
        Opacity of the plot elements, in this case the density lines, rugs and bars.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    show_density : bool
        Show or hide the line(s) representing the calculated density.
    show_histogram : bool
        Show or hide the histogram(s).
    show_rug : bool
        Show or hide rug.

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://en.wikipedia.org/wiki/Density_estimation
    - https://en.wikipedia.org/wiki/Kernel_density_estimation

    Examples
    --------
    - https://plot.ly/python/distplot

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    data, name = _shared_preprocessing.prepare_vector_data_nd_stats(data, name, kwargs)

    # Layout
    layout = _go.Layout(bargap=0.05)
    size_spec = _plotly_processing.set_plot_size(kwargs, layout)
    _plotly_processing.set_plot_color(kwargs, layout)
    _plotly_processing.set_title(kwargs, layout)
    layout_for_certain_axes = dict()
    _plotly_processing.set_x_axis(kwargs, layout_for_certain_axes)
    _plotly_processing.set_y_axis(kwargs, layout_for_certain_axes)
    layout['xaxis'] = layout_for_certain_axes['xaxis']
    layout['xaxis']['anchor'] = 'y1'
    layout['yaxis'] = layout_for_certain_axes['yaxis']
    layout['yaxis']['showgrid'] = False
    if show_rug:
        layout['yaxis']['domain'] = [0.04*(len(data)+3), 1.0]
        layout['yaxis2'] = {'domain': [0, 0.04*len(data)]}

    # Data
    names = _shared_processing.get_all_names(name, len(data))
    colors = _shared_processing.get_all_colors(color, len(data))
    colors = [_plotly_processing.convert_color(col) for col in colors]
    opacity_i = _shared_processing.get_next_opacity(opacity, i=0)
    bin_spec = _plotly_processing.extract_bin_spec(kwargs)
    if kwargs['show_legend'] is None:
        kwargs['show_legend'] = len(data) > 1
    _plotly_processing.set_legend(kwargs, layout)

    # Figure
    fig = _figure_factory.create_distplot(
        data, names,
        colors=colors,
        show_curve=show_density,
        show_hist=show_histogram,
        show_rug=show_rug,
    )
    for sub_data in fig['data']:
        sub_data['opacity'] = opacity_i
        if sub_data['type'] == 'histogram':
            plotly_bin_spec = _plotly_processing.convert_bin_spec(
                bin_spec, sub_data['x'], half_bin_onto_borders=True)
            sub_data.update(plotly_bin_spec)
            if show_density:
                sub_data['opacity'] /= 2.0
    fig['layout'].update(layout)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid,
                   _args.legend, _args.bins)
def histogram(data, name=None, color=None, opacity=None,
              bar_mode='group', orientation='vertical', normalization='probability density',
              **kwargs):
    """Create a histogram plot.

    Note
    ----
    If the data contains multiple lists, Plotly considers only the first one to determine
    the bin range for all lists, while Matplotlib considers each list individually.
    This may lead to undesired results, which can be corrected by providing explicit
    values for ``bin_x_start``, ``bin_x_stop`` and ``bin_x_number``.

    Parameters
    ----------
    data : list of lists, pandas DataFrame, or filepath of a CSV file
        A list of lists. Each list may have a different number of items.
        If a list contains a non-numerical item (str, None, ...),
        the entire list will be removed automatically and a warning will be shown.
        If a list contains a numerical but non-finite item (NaN, +Inf, -Inf),
        the individual entry will be removed automatically and a warning will be shown.
    name : list
        Name(s) of the visualized data series. Used as axis description.
    color : str, tuple or list
        Color(s) of the plot elements, in this case the bars.
        Possible values: See :ref:`colors`.
    opacity : float
        Opacity of the plot elements, in this case the bars.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    bar_mode : str
        How bars at the same location are displayed.
        Possible values:
        "group" (=next to each other, centered around the shared location),
        "stack" (=stacked on top of each other),
        "overlay" (=behind each other),
        "relative" (=stacked on top of each other, negative values below axis, positive above)
        Caution: Some options require equal bin widths, which is currently not possible for
        most multi-dimensional data.
    orientation : str
        Orientation of the bars. Possible values: "vertical", "horizontal"
    normalization : str
        Type of normalization, see
        https://plot.ly/python/reference/#histogram2d-histnorm
        Possible values: "percent", "probability", "density", "probability density".

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://plot.ly/python/reference/#histogram

    Examples
    --------
    - https://plot.ly/python/histograms
    - https://plot.ly/pandas/histograms
    - https://plot.ly/pandas/2D-Histogram

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    data, name = _shared_preprocessing.prepare_vector_data_nd_stats(data, name, kwargs)

    # Argument processing
    _shared_preprocessing.check_categorical_argument(
        orientation, 'orientation', ['vertical', 'horizontal'])
    orientation = 'v' if orientation == 'vertical' else 'h'

    # Layout
    layout = _go.Layout(barmode=bar_mode, bargap=0.05)  # bargroupgap
    size_spec = _plotly_processing.set_plot_size(kwargs, layout)
    _plotly_processing.set_plot_color(kwargs, layout)
    _plotly_processing.set_title(kwargs, layout)
    _plotly_processing.set_x_axis(kwargs, layout)
    _plotly_processing.set_y_axis(kwargs, layout)
    _plotly_processing.set_grid(kwargs, layout)
    if kwargs['show_legend'] is None:
        kwargs['show_legend'] = len(data) > 1
    _plotly_processing.set_legend(kwargs, layout)

    # Data
    bin_spec = _plotly_processing.extract_bin_spec(kwargs)

    plotly_data = []
    for i, series in enumerate(data):
        used_series = dict(y=series) if orientation == 'h' else dict(x=series)
        name_i = _shared_processing.get_next_name(name, i)
        color_i = _shared_processing.get_next_color(color, i)
        color_i = _plotly_processing.convert_color(color_i)
        opacity_i = _shared_processing.get_next_opacity(opacity, i)

        plotly_bin_spec = _plotly_processing.convert_bin_spec(
            bin_spec, data[i], half_bin_onto_borders=True)

        if len(data) > 1:
            line_spec = dict()
        else:
            line_spec = dict(color='white', width=1)
        marker_spec = dict(color=color_i, opacity=1, line=line_spec)
        trace = _go.Histogram(
            **used_series,
            name=name_i,
            histnorm=normalization,
            marker=marker_spec,
            opacity=opacity_i,
            **plotly_bin_spec,
        )
        plotly_data.append(trace)

    # Figure
    fig = _go.Figure(data=plotly_data, layout=layout)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.colormap)
def parallel_coordinates(data, data_range=None, num_significant_digits=1,
                         name=None, color=None,
                         show_label=None, label_font=None, label_size=None, label_color=None,
                         **kwargs):
    """Create a parallel coordinates plot.

    Parameters
    ----------
    data : list of lists, pandas DataFrame, or filepath of a CSV file
        A list of lists. Each list needs to have the same number of items.
        If a list contains a non-numerical item (str, None, ...),
        the entire list will be removed automatically and a warning will be shown.
        If a list contains a numerical but non-finite item (NaN, +Inf, -Inf),
        the position of the entry will be removed from each list automatically
        and a warning will be shown.
    data_range : optional, tuple or list of tuples
        Display range for each dimension.
        Possible values: (min, max) or [(min1, max1), (min2, max2), ...].
    num_significant_digits : optional, int
        If data ranges are determined automatically,
        how many significant digits can min and max values have. A higher number means
        that the axis ranges can be closer to the min and max value in the data. A lower
        number produces less clutter and may be more intuitive.
    name : list
        Name(s) of the visualized data series. Used as axis description.
    color : str, tuple or list
        Color(s) of the plot elements, in this case the lines.
        Default: Values of the first dimension, used together with the colormap.
        Possible values: See :ref:`colors`.
    show_label : bool
        Show or hide axis labels.
    label_font : str
        Font of axis labels.
    label_size : float
        Size of axis labels.
    label_color : str or tuple
        Color of axis labels.

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://plot.ly/python/reference/#parcoords

    Examples
    --------
    - https://plot.ly/python/parallel-coordinates-plot
    - https://plot.ly/pandas/parallel-coordinates-plot

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    data, name = _shared_preprocessing.prepare_vector_data_nd(data, name)

    # Argument processing
    if isinstance(data_range, tuple) and len(data_range) == 2:
        data_range = [data_range] * len(data)

    if color is None:
        color_i = data[0]
    else:
        color_i = _shared_processing.get_next_color(color, i=0)
        color_i = _plotly_processing.convert_color(color_i)
        if isinstance(color_i, str):
            # Special processing because RGBA strings are not recognized as in all other plots
            def rgba_to_rgb(given_str):
                return given_str[:3]+given_str[4:-6]+')'

            color_i = rgba_to_rgb(color_i)

    if show_label is None:
        show_label = _config.settings.show_x_label
    if label_font is None:
        label_font = _config.settings.x_label_font
    if label_size is None:
        label_size = _config.settings.x_label_size
    if label_color is None:
        label_color = _config.settings.x_label_color

    # Layout
    layout = _go.Layout()
    size_spec = _plotly_processing.set_plot_size(kwargs, layout)
    _plotly_processing.set_plot_color(kwargs, layout)
    _plotly_processing.set_title(kwargs, layout)

    if 'margin' in layout:
        if 't' in layout['margin']:
            layout['margin'].pop('t')
    if show_label:
        layout['font'] = dict(family=label_font, color=label_color, size=label_size)
    else:
        layout['font'] = dict(color='rgba(255,255,255,0)')

    # Data
    colormap_spec = _plotly_processing.extract_colormap_spec(kwargs)
    plotly_colormap_spec = _plotly_processing.convert_colormap_spec(colormap_spec)
    plotly_colormap_spec['showscale'] = False  # always hidden because redundant information

    dimensions = []
    for i, series in enumerate(data):
        name_i = _shared_processing.get_next_name(name, i)
        try:
            min_val, max_val = data_range[i]
            assert isinstance(min_val, _Number)
            assert isinstance(max_val, _Number)
        except Exception:
            min_val_ori = min(data[i])
            min_val_lower = min_val_ori - abs(min_val_ori * 0.3)
            min_val = _shared_preprocessing.round_to_significant_digits(
                min_val_lower, num_significant_digits)
            max_val_ori = max(data[i])
            max_val_higher = max_val_ori + abs(max_val_ori * 0.3)
            max_val = _shared_preprocessing.round_to_significant_digits(
                max_val_higher, num_significant_digits)
        dimensions.append(dict(label=name_i, values=series, range=[min_val, max_val]))
    trace = _go.Parcoords(
        line=dict(
            color=color_i,
            **plotly_colormap_spec,
        ),
        dimensions=dimensions,
    )
    plotly_data = [trace]

    # Figure
    fig = _go.Figure(data=plotly_data, layout=layout)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid,
                   _args.colormap, _args.markers, _args.lines, _args.bins_2d)
def scatter_matrix(data, name=None, color=None, opacity=None,
                   show_diagonal=True, show_diagonal_histogram=True, show_diagonal_scatter=False,
                   show_lower=True, show_lower_density=False, show_lower_histogram=False,
                   show_lower_scatter=True,
                   show_upper=True, show_upper_density=False, show_upper_histogram=False,
                   show_upper_scatter=True,
                   **kwargs):
    """Create a scatter plot matrix.

    Parameters
    ----------
    data : list of lists, pandas DataFrame, or filepath of a CSV file
        A list of lists. Each list needs to have the same number of items.
        If a list contains a non-numerical item (str, None, ...),
        the entire list will be removed automatically and a warning will be shown.
        If a list contains a numerical but non-finite item (NaN, +Inf, -Inf),
        the position of the entry will be removed from each list automatically
        and a warning will be shown.
    name : list
        Name(s) of the visualized data series. Used as subplot axis description.
    color : str, tuple or list
        Color(s) of the plot elements, in this case the markers and
        lines. Can be overruled by **marker_color** and **line_color**.
        Possible values: See :ref:`colors`.
    opacity : float
        Opacity of the plot elements, in this case the markers and
        lines. Can be overruled by **marker_opacity** and **line_opacity**.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    show_diagonal : bool
        Show or hide the plots on the diagonal of the matrix.
    show_diagonal_histogram : bool
        Show or hide a histogram plot on the diagonal.
    show_diagonal_scatter : bool
        Show or hide a scatter plot on the diagonal.
    show_lower : bool
        Show or hide the plots on the lower half of the matrix.
    show_lower_density : bool
        Show or hide density plots on the lower half.
    show_lower_histogram : bool
        Show or hide histogram plots on the lower half.
    show_lower_scatter : bool
        Show or hide scatter plots on the lower half.
    show_upper : bool
        Show or hide the plots on the upper half of the matrix.
    show_upper_density : bool
        Show or hide density plots on the upper half.
    show_upper_histogram : bool
        Show or hide histogram plots on the lower half.
    show_upper_scatter : bool
        Show or hide scatter plots on the lower half.

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting the plot.

    Examples
    --------
    - https://plot.ly/python/scatterplot-matrix
    - https://plot.ly/python/subplots

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    data, name = _shared_preprocessing.prepare_vector_data_nd(data, name)

    # Argument processing
    for arg in ['show_colormap', 'show_legend']:
        if kwargs.get(arg, None) is True:
            _logging.report_inactive_argument(arg)

    # Layout
    full_layout = _go.Layout()
    size_spec = _plotly_processing.set_plot_size(kwargs, full_layout)
    _plotly_processing.set_plot_color(kwargs, full_layout)
    _plotly_processing.set_title(kwargs, full_layout)
    full_layout['showlegend'] = False

    sub_layout_prototype = _go.Layout()
    show_x_title = kwargs['show_x_title'] is not False
    show_y_title = kwargs['show_y_title'] is not False
    _plotly_processing.set_x_axis(kwargs, sub_layout_prototype)
    _plotly_processing.set_y_axis(kwargs, sub_layout_prototype)
    _plotly_processing.set_grid(kwargs, sub_layout_prototype)

    # Data
    color_i = _shared_processing.get_next_color(color, i=0)
    color_i = _plotly_processing.convert_color(color_i)

    opacity_i = _shared_processing.get_next_opacity(opacity, i=0)

    colormap_spec = _plotly_processing.extract_colormap_spec(kwargs)
    colormap_spec['show_colormap'] = False  # Disabled currently to prevent duplicate colorbars
    marker_spec = _plotly_processing.extract_marker_spec(kwargs)
    line_spec = _plotly_processing.extract_line_spec(kwargs)

    bin_2d_spec = _plotly_processing.extract_bin_2d_spec(kwargs)
    bin_spec = {key: val for key, val in bin_2d_spec.items() if 'x_' in key}

    # Figure
    num_series = len(data)
    num_spacer = num_series - 1
    if num_spacer > 0:
        spacer_size_total = 0.1
        spacer_size = spacer_size_total / num_spacer
        subplot_space = 1.0 - spacer_size_total
        subplot_size = subplot_space / num_series
    else:
        spacer_size = 0.0
        subplot_size = 1.0
    axis_hider = dict(showticklabels=False, title=None, ticks='')
    full_data = []
    for i in range(num_series):
        for j in range(num_series):
            # Identify relative plot position
            is_diagonal = (i == j)
            is_lower_triangle = i > j
            is_upper_triangle = i < j
            is_left_column = j == 0
            is_bottom_row = i == num_series-1

            # Preparation
            x, y = data[j], data[i]
            plot_identifier = str(i*num_series+j+1)
            x_indexer = 'xaxis' if plot_identifier == '1' else 'xaxis' + plot_identifier
            y_indexer = 'yaxis' if plot_identifier == '1' else 'yaxis' + plot_identifier
            x_anchor = 'x' + plot_identifier
            y_anchor = 'y' + plot_identifier

            # Figure generation
            def construct_fig(x, y,
                              draw_scatter=False, draw_histogram=False,
                              draw_histogram_2d=False, draw_density_2d=False):
                figures = []
                if draw_scatter:
                    fig = _plots_2d.scatter(
                        x, y, color=color_i, opacity=opacity_i, show_legend=False,
                        **marker_spec, **line_spec, **colormap_spec)
                    figures.append(fig)
                if draw_histogram:
                    fig = histogram([x], color='black', show_legend=False, **bin_spec)
                    figures.append(fig)
                if draw_histogram_2d:
                    fig = _plots_2d.histogram_2d(x, y, **bin_2d_spec, **colormap_spec)
                    figures.append(fig)
                if draw_density_2d:
                    fig = _plots_2d.density_2d(x, y, **bin_2d_spec, **colormap_spec)
                    figures.append(fig)
                if len(figures) > 0:
                    fig = figures[0]
                    for other_fig in figures[1:]:
                        fig = fig + other_fig
                else:
                    fig = None
                return fig

            def construct_empty_fig():
                fig = dict(data=[], layout=dict(xaxis=dict(), yaxis=dict()))
                return _Figure(fig, **size_spec)

            if is_diagonal:
                fig = construct_fig(
                    x, y, draw_scatter=show_diagonal_scatter,
                    draw_histogram=show_diagonal_histogram)
                if not show_diagonal or fig is None:
                    fig = construct_empty_fig()
            elif is_upper_triangle:
                fig = construct_fig(
                    x, y, draw_scatter=show_upper_scatter,
                    draw_histogram_2d=show_upper_histogram,
                    draw_density_2d=show_upper_density)
                if not show_upper or fig is None:
                    fig = construct_empty_fig()
            elif is_lower_triangle:
                fig = construct_fig(
                    x, y, draw_scatter=show_lower_scatter,
                    draw_histogram_2d=show_lower_histogram,
                    draw_density_2d=show_lower_density)
                if not show_lower or fig is None:
                    fig = construct_empty_fig()
            for trace in fig.fig['data']:
                trace['xaxis'] = x_anchor
                trace['yaxis'] = y_anchor
                full_data.append(trace)
            full_layout[x_indexer] = fig.fig['layout']['xaxis']
            full_layout[y_indexer] = fig.fig['layout']['yaxis']

            # Figure adaption
            def float_correction(given):
                if given > 1.0:
                    given = 1.0
                elif given < 0.0:
                    given = 0.0
                return given
            x_start = float_correction((subplot_size + spacer_size) * j)
            x_end = float_correction(x_start + subplot_size)
            y_end = float_correction(1.0 - ((subplot_size + spacer_size) * i))
            y_start = float_correction(y_end - subplot_size)
            x_positioner = dict(domain=[x_start, x_end], anchor=y_anchor)  # y_anchor is correct
            y_positioner = dict(domain=[y_start, y_end], anchor=x_anchor)  # x_anchor is correct
            full_layout[x_indexer].update(sub_layout_prototype['xaxis'])
            full_layout[x_indexer].update(x_positioner)
            full_layout[y_indexer].update(sub_layout_prototype['yaxis'])
            full_layout[y_indexer].update(y_positioner)
            # Linked x axes
            if i > 0:
                x_scale_anchor = 'x{}'.format(j+1)
                full_layout[x_indexer]['matches'] = x_scale_anchor
            # Linked y axes
            if j > 0:
                y_scale_anchor = 'y{}'.format(num_series*i+1)
                if y_scale_anchor == 'y1' and not show_diagonal_scatter:
                    y_scale_anchor = 'y2'
                if not is_diagonal or show_diagonal_scatter:
                    if not (y_indexer == 'yaxis2' and y_scale_anchor == 'y2'):
                        full_layout[y_indexer]['matches'] = y_scale_anchor
            # Hide axes and provide titles
            if is_bottom_row:
                x_title = _shared_processing.get_next_name(name, j)
                full_layout[x_indexer]['title']['text'] = x_title if show_x_title else ''
            else:
                full_layout[x_indexer].update(axis_hider)
            if is_left_column:
                y_title = _shared_processing.get_next_name(name, i)
                full_layout[y_indexer]['title']['text'] = y_title if show_y_title else ''
            else:
                full_layout[y_indexer].update(axis_hider)

            # Hide grid in diagonal plots, except they only contain a scatter plot
            if is_diagonal and show_diagonal_histogram:
                full_layout[x_indexer]['showgrid'] = False
                full_layout[y_indexer]['showgrid'] = False

    fig = _go.Figure(data=full_data, layout=full_layout)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid,
                   _args.rugs)
def violin(data, name=None, color=None, opacity=None, violin_width=0.6, orientation='vertical',
           show_mean=False, show_box=False, scale_mode='width', span_mode='soft', side='both',
           point_mode='all', point_jitter=0.0, point_position=-1.5, **kwargs):
    """Create a violin plot.

    Parameters
    ----------
    data : list of lists, pandas DataFrame, or filepath of a CSV file
        A list of lists. Each list may have a different number of items.
        If a list contains a non-numerical item (str, None, ...),
        the entire list will be removed automatically and a warning will be shown.
        If a list contains a numerical but non-finite item (NaN, +Inf, -Inf),
        the individual entry will be removed automatically and a warning will be shown.
    name : list
        Name(s) of the visualized data series. Used as axis description.
    color : str, tuple or list
        Color(s) of the plot elements, in this case the violins.
        Possible values: See :ref:`colors`.
    opacity : float
        Opacity of the plot elements, in this case the violins.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    violin_width : float
        Width of the violins.
    orientation : str
        Orientation of the violins. Possible values: "vertical", "horizontal"
    show_mean : bool
        Show a black line at the position of the mean value of each series.
    show_box : bool
        Show or hide small boxes within violins.
    scale_mode : str
        Metric by which the width of the violin is determined.
        Possible values: "width" (=each violin has same max width),
        "count" (=max width is determined by the number of sample points).
    span_mode : str
        Over which span in data space the density function is computed.
        Possible values: "soft" (=min/max and two bandwidths), "hard" (min/max).
    side : str
        Side on which the density function is drawn.
        Possible values: "positive", "negative", "both".
    point_mode : str
        Which sample points are visualized.
        Possible values: "all" (=all points), "outliers" (=only points outside the whiskers),
        "suspectedoutliers" (=only outlier points).
    point_jitter : float
        Amount of random jitter applied to the points.
        Possible values: Positive float numbers, e.g. 0.0 (=no jitter) and 1.0 (=jitter amount
        of violin width)
    point_position : float
        Position of sample points relative to violines.

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://plot.ly/python/reference/#violin

    Examples
    --------
    - https://plot.ly/python/violin

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    data, name = _shared_preprocessing.prepare_vector_data_nd_stats(data, name, kwargs)

    # Argument processing
    original_rug_style = kwargs['rug_style']
    _shared_preprocessing.check_categorical_argument(
        orientation, 'orientation', ['vertical', 'horizontal'])
    orientation = 'v' if orientation == 'vertical' else 'h'

    # Layout
    layout = _go.Layout(showlegend=False)
    size_spec = _plotly_processing.set_plot_size(kwargs, layout)
    _plotly_processing.set_plot_color(kwargs, layout)
    _plotly_processing.set_title(kwargs, layout)
    _plotly_processing.set_x_axis(kwargs, layout)
    _plotly_processing.set_y_axis(kwargs, layout)
    _plotly_processing.set_grid(kwargs, layout)

    # Data
    rug_spec = _plotly_processing.extract_rug_spec(kwargs)

    plotly_data = []
    for i, series in enumerate(data):
        used_series = dict(x=series) if orientation == 'h' else dict(y=series)
        name_i = _shared_processing.get_next_name(name, i)
        color_i = _shared_processing.get_next_color(color, i)
        color_i = _plotly_processing.convert_color(color_i)
        opacity_i = _shared_processing.get_next_opacity(opacity, i)

        if show_box:
            box_spec = dict(visible=True, fillcolor=color_i, line=dict(color='black', width=1))
        else:
            box_spec = dict(visible=False)
        # Rugs
        rug_spec_i = _shared_processing.get_next_rug_spec(rug_spec, color_i, opacity_i, None, i)
        if orientation == 'h' and original_rug_style is None and rug_spec_i['rug_style'] == "-":
            rug_spec_i['rug_style'] = "|"
        plotly_rug_spec, show_rug = _plotly_processing.convert_rug_spec(rug_spec_i)
        point_spec = dict()
        if show_rug:
            point_spec['points'] = 'all'
            point_spec['marker'] = dict(
                symbol=plotly_rug_spec['symbol'],
                size=plotly_rug_spec['size'],
                color=plotly_rug_spec['color'],
                opacity=plotly_rug_spec['opacity'],
            )
            point_spec['points'] = point_mode
            point_spec['jitter'] = point_jitter
            point_spec['pointpos'] = point_position
        else:
            point_spec['points'] = False
        trace = _go.Violin(
            **used_series,
            name=name_i,
            fillcolor=color_i,
            opacity=opacity_i,
            side=side,
            scalemode=scale_mode,
            spanmode=span_mode,
            width=violin_width,
            orientation=orientation,
            line=dict(color='black', width=1),
            meanline=dict(visible=show_mean, color='black'),
            box=box_spec,
            **point_spec,
        )
        plotly_data.append(trace)

    # Figure
    fig = _go.Figure(data=plotly_data, layout=layout)
    return _Figure(fig, **size_spec)

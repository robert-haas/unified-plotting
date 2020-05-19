"""Plotly plots for 2-dimensional vector data."""

from collections.abc import Iterable as _Iterable
from numbers import Number as _Number

import plotly.figure_factory as _figure_factory
import plotly.graph_objs as _go

from .._unified_arguments import arguments as _args
from .._unified_arguments import shared_preprocessing as _shared_preprocessing
from .._unified_arguments import shared_processing as _shared_processing
from .._unified_arguments.injection import inject_functions as _inject_functions
from . import _plotly_processing
from ._data_structures import Figure as _Figure


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid,
                   _args.legend)
def bar(x, y, name=None, color=None, opacity=None, orientation='vertical',
        bar_mode='group', bar_width=None,
        show_bartext=False, bartext_font=None, bartext_color=None, bartext_size=None,
        bartext_position='outside',
        **kwargs):
    """Create a bar plot.

    Parameters
    ----------
    x : list or list of lists
        A list of numbers or if ``x_axis_scale="categorical"`` a list of strings or a
        list of multiple such lists. It needs to have the same number of items as ``y``.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
    y : list or list of lists
        A list of numbers or if ``y_axis_scale="categorical"`` a list of strings or a
        list of multiple such lists. It needs to have the same number of items as ``x``.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
    name : list
        Names of the y series. Used in the legend if more than one series is present.
    color : str, tuple or list
        Color or colors of the plot elements, in this case the bars.
        Possible values: See :ref:`colors`.
    opacity : float
        Opacity of the plot elements, in this case the bars.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    orientation : str
        Orientation of the bars. Possible values: "vertical", "horizontal"
    bar_mode : str
        How bars at the same location are displayed.
        Possible values: "stack" (=stacked on top of one another),
        "group" (=next to one another centered around the shared location),
        "overlay" (=over one another), "relative" (=stacked on top of one another,
        negative values below the axis, positive values above)
    bar_width : float
        Width of bars.
    show_bartext : bool
        Show or hide text in bars that shows the respective y value.
    bartext_font : str
        Font of the bar text.
        Default: Font of the x-Axis labels.
    bartext_color : str, tuple or list
        Color of the bar text.
        Possible values: See :ref:`colors`.
    bartext_size : float
        Size of the bar text.
        Default: Size of the x-Axis labels.
        The positioning algorithm may resize and scale the text.
    bartext_position : str
        Positioning of the bar text.
        Possible values: "inside", "outside", "auto".

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://plot.ly/python/reference/#bar

    Examples
    --------
    - https://plot.ly/python/bar-charts
    - https://plot.ly/python/horizontal-bar-charts

    **Further parameters that are unified across plots and libraries**

    """
    # Orientation
    _shared_preprocessing.check_categorical_argument(
        orientation, 'orientation', ['vertical', 'horizontal'])
    if orientation == 'horizontal':
        x, y = y, x
    orientation = 'v' if orientation == 'vertical' else 'h'

    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    xs, ys, _, _, _, _, _ = _shared_preprocessing.prepare_vector_data_2d_multiple(x, y, kwargs)

    # Argument processing
    _shared_preprocessing.check_categorical_argument(
        bar_mode, 'bar_mode', ['stack', 'group', 'overlay', 'relative'])
    _shared_preprocessing.check_categorical_argument(
        bartext_position, 'bartext_position', ['auto', 'inside', 'outside'])
    if bartext_color is None:
        bartext_color = color

    # Layout
    layout = _go.Layout()
    size_spec = _plotly_processing.set_plot_size(kwargs, layout)
    _plotly_processing.set_plot_color(kwargs, layout)
    _plotly_processing.set_title(kwargs, layout)
    _plotly_processing.set_x_axis(kwargs, layout)
    _plotly_processing.set_y_axis(kwargs, layout)
    _plotly_processing.set_grid(kwargs, layout)
    legend_spec = _plotly_processing.extract_legend(kwargs)
    layout['barmode'] = bar_mode

    # Data
    data = []
    for i, (x_i, y_i) in enumerate(zip(xs, ys)):
        name_i = _shared_processing.get_next_name(name, i)
        color_i = _shared_processing.get_next_color(color, i)
        color_i = _plotly_processing.convert_color(color_i)
        opacity_i = _shared_processing.get_next_opacity(opacity, i)
        trace = _go.Bar(
            x=x_i,
            y=y_i,
            name=name_i,
            marker=dict(color=color_i),
            width=bar_width,
            opacity=opacity_i,
            orientation=orientation,
        )
        if show_bartext:
            text = []
            series = y_i if orientation == 'vertical' else x_i
            for val in series:
                if isinstance(val, float):
                    text.append('{:.2g}'.format(val))
                else:
                    text.append(str(val))
            if bartext_font is None:
                bartext_font = layout['xaxis']['tickfont']['family']
            if bartext_size is None:
                bartext_size = layout['xaxis']['tickfont']['size']
            trace['text'] = text
            trace['textposition'] = bartext_position
            bartext_color_i = _shared_processing.get_next_color(bartext_color, i)
            bartext_color_i = _plotly_processing.convert_color(bartext_color_i)
            trace['textfont'] = dict(
                family=bartext_font,
                color=bartext_color_i,
                size=bartext_size,
            )
        data.append(trace)

    # Legend
    if legend_spec['show_legend'] is None:
        legend_spec['show_legend'] = len(ys) > 1
    _plotly_processing.set_legend(legend_spec, layout)

    # Figure
    fig = _go.Figure(data=data, layout=layout)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid,
                   _args.lines, _args.colormap, _args.bins_2d)
def density_2d(x, y, color=None, opacity=None, smoothing=0.7,
               show_contour_label=False, contour_label_font=None, contour_label_size=None,
               contour_label_color=None, **kwargs):
    """Create a 2D density plot.

    Parameters
    ----------
    x : list
        A list of numbers or if ``x_axis_scale="categorical"`` a list of strings.
        It needs to have the same number of items as ``y``.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
    y : list
        A list of numbers or if ``y_axis_scale="categorical"`` a list of strings.
        It needs to have the same number of items as ``x``.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
    color : str, tuple or list
        Color(s) of the plot elements, in this case the contour lines
        which are shown only if ``show_line`` is True.
        Can be overruled by ``line_color``.
        Possible values: See :ref:`colors`.
    opacity : float
        Opacity of the plot elements, in this case the density areas.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    smoothing : float
        Factor for how much smoothing is applied in density calculation.
        Possible values: Between 0.0 (=no smoothing) and 1.3 (=maximum smoothing).
    show_contour_label : bool
        Show labels for contour lines.
    contour_label_font : str
        Font of contour line labels. Default: Font of x axis labels.
    contour_label_size : float
        Size of contour line labels. Default: Size of x axis labels.
    contour_label_color : str
        Color of contour line labels. Default: Color of x axis labels.

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://plot.ly/python/reference/#histogram2dcontour

    Examples
    --------
    - https://plot.ly/python/2d-histogram-contour

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    x, y = _shared_preprocessing.prepare_vector_data_2d(x, y, kwargs)

    # Layout
    layout = _go.Layout()
    size_spec = _plotly_processing.set_plot_size(kwargs, layout)
    _plotly_processing.set_plot_color(kwargs, layout)
    _plotly_processing.set_title(kwargs, layout)
    _plotly_processing.set_x_axis(kwargs, layout)
    _plotly_processing.set_y_axis(kwargs, layout)
    _plotly_processing.set_grid(kwargs, layout)

    # Contour label style by default from x label style
    if contour_label_font is None:
        contour_label_font = layout['xaxis']['tickfont']['family']
    if contour_label_size is None:
        contour_label_size = layout['xaxis']['tickfont']['size']
    elif isinstance(contour_label_size, _Number):
        contour_label_size *= 1.33333333
    if contour_label_color is None:
        contour_label_color = layout['xaxis']['tickfont']['color']
    else:
        contour_label_color = _plotly_processing.convert_color(contour_label_color)

    # Data
    color_i = _shared_processing.get_next_color(color, i=0)
    color_i = _plotly_processing.convert_color(color_i)
    opacity_i = _shared_processing.get_next_opacity(opacity, i=0)

    line_spec = _plotly_processing.extract_line_spec(kwargs)
    line_spec_i = _shared_processing.get_next_line_spec(
        line_spec, color_i, opacity_i, given_colormap=None, i=0)
    plotly_line_spec, show_line = _plotly_processing.convert_line_spec(line_spec_i)
    colormap_spec = _plotly_processing.extract_colormap_spec(kwargs)
    plotly_colormap_spec = _plotly_processing.convert_colormap_spec(colormap_spec)
    bin_spec = _plotly_processing.extract_bin_2d_spec(kwargs)
    plotly_bin_spec = _plotly_processing.convert_bin_2d_spec(
        bin_spec, x, y, half_bin_onto_borders=True)

    contours_spec = dict(
        showlines=show_line,
        showlabels=show_contour_label,
        labelfont=dict(
            family=contour_label_font,
            size=contour_label_size,
            color=contour_label_color,
        ),
    )
    contour_line_spec = dict(
        smoothing=smoothing,
        **plotly_line_spec
    )
    trace = _go.Histogram2dContour(
        x=x,
        y=y,
        opacity=opacity_i,
        contours=contours_spec,
        line=contour_line_spec,
        **plotly_colormap_spec,
        **plotly_bin_spec,
    )
    data = [trace]

    # Figure
    fig = _go.Figure(data=data, layout=layout)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid,
                   _args.markers, _args.colormap, _args.bins_2d)
def density_scatter_histogram_2d(x, y, color=None, opacity=None,
                                 show_histogram=True, show_density=True, **kwargs):
    """Create a 2D density plot with data points inside and histograms on the margins.

    Parameters
    ----------
    x : list
        A list of numbers or if ``x_axis_scale="categorical"`` a list of strings.
        It needs to have the same number of items as ``y``.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
    y : list
        A list of numbers or if ``y_axis_scale="categorical"`` a list of strings.
        It needs to have the same number of items as ``x``.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
    color : str, tuple or list
        Color(s) of the plot elements, in this case the markers.
        Can be overruled by ``marker_color``.
        Possible values: See :ref:`colors`.
    opacity : float
        Opacity of the plot elements, in this case the markers.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    show_histogram : bool
        Show or hide the histograms on the margins of the plot.
    show_density : bool
        Show or hide the density.
    show_marker : bool
        Show or hide the scatter markers. See also below at marker section.

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting the plot.

    Examples
    --------
    - https://plot.ly/python/2d-density-plots
    - https://plot.ly/python/density-plots

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    x, y = _shared_preprocessing.prepare_vector_data_2d(x, y, kwargs)

    # Layout
    layout = _go.Layout()
    size_spec = _plotly_processing.set_plot_size(kwargs, layout)
    _plotly_processing.set_plot_color(kwargs, layout)
    _plotly_processing.set_title(kwargs, layout)
    _plotly_processing.set_x_axis(kwargs, layout)
    _plotly_processing.set_y_axis(kwargs, layout)
    _plotly_processing.set_grid(kwargs, layout)

    # Data
    color_i = _shared_processing.get_next_color(color, i=0)
    color_i = _plotly_processing.convert_color(color_i)

    opacity_i = _shared_processing.get_next_opacity(opacity, i=0)

    marker_spec = _plotly_processing.extract_marker_spec(kwargs)
    marker_spec_i = _shared_processing.get_next_marker_spec(
        marker_spec, color_i, opacity_i, given_colormap=None, i=0)
    plotly_marker_spec, show_marker = _plotly_processing.convert_marker_spec(marker_spec_i)

    colormap_spec = _plotly_processing.extract_colormap_spec(kwargs)
    plotly_colormap_spec = _plotly_processing.convert_colormap_spec(colormap_spec)

    bin_spec = _plotly_processing.extract_bin_2d_spec(kwargs)

    # Figure
    fig = _figure_factory.create_2d_density(x, y)
    fig['layout'].pop('title', None)
    fig['layout'].update(layout)
    fig_data = list(fig['data'])

    # Modification of figure parts after generation
    scatter_plot_index, contour_plot_index, histogram_x_index, histogram_y_index = 0, 1, 2, 3

    # Scatter plot
    if show_marker:
        fig_data[scatter_plot_index]['marker'] = plotly_marker_spec
    else:
        del fig_data[scatter_plot_index]
        contour_plot_index -= 1
        histogram_x_index -= 1
        histogram_y_index -= 1

    # Density plot
    if show_density:
        for key in plotly_colormap_spec:
            fig_data[contour_plot_index][key] = plotly_colormap_spec[key]
        fig_data[contour_plot_index]['opacity'] = opacity_i
        plotly_bin_spec = _plotly_processing.convert_bin_2d_spec(
            bin_spec, x, y, half_bin_onto_borders=True)
        fig_data[contour_plot_index].update(plotly_bin_spec)
    else:
        del fig_data[contour_plot_index]
        histogram_x_index -= 1
        histogram_y_index -= 1

    # Histogram plot
    if show_histogram:
        fig_data[histogram_x_index]['marker']['color'] = 'black'
        fig_data[histogram_y_index]['marker']['color'] = 'black'
        plotly_bin_spec = _plotly_processing.convert_bin_2d_spec(
            bin_spec, x, y, half_bin_onto_borders=False)
        fig_data[histogram_x_index].update(plotly_bin_spec)
        fig_data[histogram_y_index].update(plotly_bin_spec)
        fig['layout']['xaxis2']['zeroline'] = True
        fig['layout']['yaxis2']['zeroline'] = True
        fig['layout']['xaxis2']['showticklabels'] = False
        fig['layout']['yaxis2']['showticklabels'] = False
    else:
        del fig_data[histogram_y_index]
        del fig_data[histogram_x_index]
    fig['data'] = tuple(fig_data)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid,
                   _args.colormap, _args.bins_2d)
def histogram_2d(x, y, opacity=None, **kwargs):
    """Create a 2D histogram plot.

    Parameters
    ----------
    x : list
        A list of numbers or if ``x_axis_scale="categorical"`` a list of strings.
        It needs to have the same number of items as ``y``.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
    y : list
        A list of numbers or if ``y_axis_scale="categorical"`` a list of strings.
        It needs to have the same number of items as ``x``.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
    opacity : float
        Opacity of the plot elements, in this case the square counting bins.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://plot.ly/python/reference/#histogram2d

    Examples
    --------
    - https://plot.ly/python/2D-Histogram

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    x, y = _shared_preprocessing.prepare_vector_data_2d(x, y, kwargs)

    # Layout
    layout = _go.Layout()
    size_spec = _plotly_processing.set_plot_size(kwargs, layout)
    _plotly_processing.set_plot_color(kwargs, layout)
    _plotly_processing.set_title(kwargs, layout)
    _plotly_processing.set_x_axis(kwargs, layout)
    _plotly_processing.set_y_axis(kwargs, layout)
    _plotly_processing.set_grid(kwargs, layout)

    # Data
    colormap_spec = _plotly_processing.extract_colormap_spec(kwargs)
    plotly_colormap_spec = _plotly_processing.convert_colormap_spec(colormap_spec)

    bin_spec = _plotly_processing.extract_bin_2d_spec(kwargs)
    plotly_bin_spec = _plotly_processing.convert_bin_2d_spec(
        bin_spec, x, y, half_bin_onto_borders=True)

    trace = _go.Histogram2d(
        x=x,
        y=y,
        opacity=opacity,
        **plotly_colormap_spec,
        **plotly_bin_spec,
    )
    data = [trace]

    # Figure
    fig = _go.Figure(data=data, layout=layout)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.x_axis, _args.y_axis, _args.x_error, _args.y_error,
                   _args.x_grid, _args.y_grid,
                   _args.legend, _args.markers, _args.lines, _args.colormap)
def scatter(x, y, name=None, color=None, opacity=None, **kwargs):
    """Create a scatter plot.

    Parameters
    ----------
    x : list or list of lists
        A list of numbers or if ``x_axis_scale="categorical"`` a list of strings or a
        list of multiple such lists. It needs to have the same number of items as ``y``.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
    y : list or list of lists
        A list of numbers or if ``y_axis_scale="categorical"`` a list of strings or a
        list of multiple such lists. It needs to have the same number of items as ``x``.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
    name : list
        Name(s) of the visualized data series. Used in the legend.
    color : str, tuple or list
        Color(s) of the plot elements, in this case the markers and
        lines. Can be overruled by **marker_color** and **line_color**.
        Possible values: See :ref:`colors`.
    opacity : float
        Opacity of the plot elements, in this case the markers and
        lines. Can be overruled by **marker_opacity** and **line_opacity**.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://en.wikipedia.org/wiki/Scatter_plot
    - https://plot.ly/python/reference/#scatter
    - https://plot.ly/python/reference/#scattergl

    Examples
    --------
    - https://plot.ly/python/line-and-scatter
    - https://plot.ly/python/bubble-charts
    - https://plot.ly/python/dot-plots
    - https://plot.ly/python/line-charts
    - https://plot.ly/python/filled-area-plots
    - https://plot.ly/python/graphing-multiple-chart-types
    - https://plot.ly/python/error-bars
    - https://plot.ly/python/continuous-error-bars

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    xs, ys, x_el, x_er, y_et, y_eb, multiple_series = \
        _shared_preprocessing.prepare_vector_data_2d_multiple(x, y, kwargs)

    # Layout
    layout = _go.Layout()
    size_spec = _plotly_processing.set_plot_size(kwargs, layout)
    _plotly_processing.set_plot_color(kwargs, layout)
    _plotly_processing.set_title(kwargs, layout)
    _plotly_processing.set_x_axis(kwargs, layout)
    _plotly_processing.set_y_axis(kwargs, layout)
    _plotly_processing.set_grid(kwargs, layout)
    legend_spec = _plotly_processing.extract_legend(kwargs)

    # Data
    marker_spec = _plotly_processing.extract_marker_spec(kwargs)
    line_spec = _plotly_processing.extract_line_spec(kwargs)
    colormap_spec = _plotly_processing.extract_colormap_spec(kwargs)
    x_error_spec = _plotly_processing.extract_x_error_spec(kwargs)
    y_error_spec = _plotly_processing.extract_y_error_spec(kwargs)

    data = []
    count_colormaps = 0
    for i, (x_i, y_i) in enumerate(zip(xs, ys)):
        name_i = _shared_processing.get_next_name(name, i)
        color_i = _shared_processing.get_next_color(color, i)
        color_i = _plotly_processing.convert_color(color_i)
        opacity_i = _shared_processing.get_next_opacity(opacity, i)

        colormap_spec_i = _shared_processing.get_next_colormap_spec(colormap_spec, i)
        plotly_colormap_spec = _plotly_processing.convert_colormap_spec(colormap_spec_i)
        plotly_colormap = plotly_colormap_spec['colorscale']

        marker_spec_i = _shared_processing.get_next_marker_spec(
            marker_spec, color_i, opacity_i, plotly_colormap, i)
        plotly_marker_spec, show_marker = _plotly_processing.convert_marker_spec(
            marker_spec_i)
        plotly_marker_spec['reversescale'] = plotly_colormap_spec['reversescale']
        if plotly_colormap_spec['showscale'] and count_colormaps == 0:
            colors = plotly_marker_spec['color']
            colors_represent_values = (
                isinstance(colors, _Iterable) and not isinstance(colors, str)
                and len(colors) == len(x_i))
            if colors_represent_values:
                for key in plotly_colormap_spec:
                    plotly_marker_spec[key] = plotly_colormap_spec[key]
                count_colormaps += 1

        line_spec_i = _shared_processing.get_next_line_spec(
            line_spec, color_i, opacity_i, plotly_colormap, i)
        plotly_line_spec, show_line = _plotly_processing.convert_line_spec(line_spec_i)

        x_error_spec_i = _shared_processing.get_next_x_error_spec(
            x_error_spec, line_spec_i, color_i, i)
        plotly_x_error_spec, show_x_error_bar = \
            _plotly_processing.convert_x_error_spec(x_error_spec_i)
        y_error_spec_i = _shared_processing.get_next_y_error_spec(
            y_error_spec, line_spec_i, color_i, opacity_i, i)
        plotly_y_error_bar_spec, show_y_error_bar, plotly_y_error_band_spec, show_y_error_band = \
            _plotly_processing.convert_y_error_spec(y_error_spec_i)

        mode = _plotly_processing.get_scatter_mode(show_marker, show_line)

        # Error bars
        error_bar_kwargs = dict()
        if show_x_error_bar and (x_el or x_er):
            error_bar_kwargs['error_x'] = dict(
                array=x_er[i],
                arrayminus=x_el[i],
                **plotly_x_error_spec,
            )
        if show_y_error_bar and (y_et or y_eb):
            error_bar_kwargs['error_y'] = dict(
                array=y_et[i],
                arrayminus=y_eb[i],
                **plotly_y_error_bar_spec,
            )

        # Plot
        if mode:
            trace = _go.Scatter(
                x=x_i,
                y=y_i,
                name=name_i,
                marker=plotly_marker_spec,
                line=plotly_line_spec,
                mode=mode,
                **error_bar_kwargs,
            )
        else:
            trace = _go.Scatter()
        data.append(trace)

        # y error band
        if show_y_error_band and (y_et or y_eb):
            y_error_bottom = [ym-yb for ym, yb in zip(y_i, y_eb[i])]
            y_error_top = [ym+yt for ym, yt in zip(y_i, y_et[i])]
            x_error_points = x_i + list(reversed(x_i)) + x_i[:1]
            y_error_points = y_error_top + list(reversed(y_error_bottom)) + y_error_top[:1]
            error_band_trace = _go.Scatter(
                x=x_error_points,
                y=y_error_points,
                **plotly_y_error_band_spec,
            )
            data.append(error_band_trace)

    # Legend
    show_legend = legend_spec['show_legend']
    legend_spec['show_legend'] = show_legend or (show_legend is None and multiple_series)
    _plotly_processing.set_legend(legend_spec, layout)

    # Figure
    fig = _go.Figure(data=data, layout=layout)
    return _Figure(fig, **size_spec)

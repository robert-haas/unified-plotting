"""Matplotlib plots for 2-dimensional vector data."""

from collections.abc import Iterable as _Iterable

import matplotlib.pyplot as _plt

from .._unified_arguments import arguments as _args
from .._unified_arguments import shared_preprocessing as _shared_preprocessing
from .._unified_arguments import shared_processing as _shared_processing
from .._unified_arguments.injection import inject_functions as _inject_functions
from . import _matplotlib_processing
from ._data_structures import Figure as _Figure


@_inject_functions(_args.external_fig_and_ax, _args.plot_size_and_resolution, _args.plot_color,
                   _args.plot_title, _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid,
                   _args.colormap, _args.bins_2d)
def hexbin(x, y, opacity=None, **kwargs):
    """Create a hexbin plot.

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
        Opacity of the plot elements, in this case the hexagonal counting bins.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).

    Returns
    -------
    A :ref:`Figure <mpl-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.hexbin.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.hexbin.html

    Examples
    --------
    - https://matplotlib.org/examples/pylab_examples/hexbin_demo.html

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    x, y = _shared_preprocessing.prepare_vector_data_2d(x, y, kwargs)

    # Layout
    _plt.ioff()  # Required to prevent multiple outputs, not sure why it needs to be exactly here
    fig, ax = _matplotlib_processing.extract_fig_and_ax(kwargs)
    size_spec = _matplotlib_processing.set_plot_size(kwargs, fig)
    _matplotlib_processing.set_plot_color(kwargs, fig, ax)
    _matplotlib_processing.set_title(kwargs, ax)
    _matplotlib_processing.set_x_axis(kwargs, ax)
    _matplotlib_processing.set_y_axis(kwargs, ax)
    _matplotlib_processing.set_grid(kwargs, ax)

    # Data
    colormap_spec = _matplotlib_processing.extract_colormap_spec(kwargs)
    mpl_colormap_spec = _matplotlib_processing.convert_colormap_spec(colormap_spec)

    opacity_i = _shared_processing.get_next_opacity(opacity, i=0)

    bin_spec = _matplotlib_processing.extract_bin_2d_spec(kwargs)
    mpl_bin_spec = _matplotlib_processing.convert_bin_2d_spec(
        bin_spec, x, y, half_bin_onto_borders=False, target='hexbin')

    # Plot
    collection = ax.hexbin(
        x,
        y,
        cmap=mpl_colormap_spec['cmap'],
        alpha=opacity_i,
        linewidths=0.07,
        edgecolors='white',
        **mpl_bin_spec,
    )
    if mpl_colormap_spec['show_colormap']:
        _matplotlib_processing.set_colormap_properties(ax, collection, mpl_colormap_spec)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.external_fig_and_ax, _args.plot_size_and_resolution, _args.plot_color,
                   _args.plot_title, _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid,
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
        Opacity of the plot elements, in this case the hexagonal counting bins.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).

    Returns
    -------
    A :ref:`Figure <mpl-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.hist2d.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.hist2d.html

    Examples
    --------
    - https://matplotlib.org/examples/pylab_examples/hist2d_demo.html

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    x, y = _shared_preprocessing.prepare_vector_data_2d(x, y, kwargs)

    # Layout
    _plt.ioff()  # Required to prevent multiple outputs, not sure why it needs to be exactly here
    fig, ax = _matplotlib_processing.extract_fig_and_ax(kwargs)
    size_spec = _matplotlib_processing.set_plot_size(kwargs, fig)
    _matplotlib_processing.set_plot_color(kwargs, fig, ax)
    _matplotlib_processing.set_title(kwargs, ax)

    # Data
    colormap_spec = _matplotlib_processing.extract_colormap_spec(kwargs)
    mpl_colormap_spec = _matplotlib_processing.convert_colormap_spec(colormap_spec)

    opacity_i = _shared_processing.get_next_opacity(opacity, i=0)

    bin_spec = _matplotlib_processing.extract_bin_2d_spec(kwargs)
    mpl_bin_spec = _matplotlib_processing.convert_bin_2d_spec(
        bin_spec, x, y, half_bin_onto_borders=True, target='hist2d')

    # Plot
    result = ax.hist2d(
        x,
        y,
        cmap=mpl_colormap_spec['cmap'],
        alpha=opacity_i,
        **mpl_bin_spec,
    )

    # Layout 2: needs to be applied after plotting here
    _matplotlib_processing.set_x_axis(kwargs, ax)
    _matplotlib_processing.set_y_axis(kwargs, ax)
    _matplotlib_processing.set_grid(kwargs, ax)

    if mpl_colormap_spec['show_colormap']:
        collection = result[3]
        _matplotlib_processing.set_colormap_properties(ax, collection, mpl_colormap_spec)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.external_fig_and_ax, _args.plot_size_and_resolution, _args.plot_color,
                   _args.plot_title, _args.x_axis, _args.y_axis, _args.x_error, _args.y_error,
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
        Color(s) of the plot elements, in this case the markers and lines.
        Can be overruled by **marker_color** and **line_color**.
        Possible values: See :ref:`colors`.
    opacity : float
        Opacity of the plot elements, in this case the markers and lines.
        Can be overruled by **marker_opacity** and **line_opacity**.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).

    Returns
    -------
    A :ref:`Figure <mpl-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.plot.html
    - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.scatter.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.scatter.html
    - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.errorbar.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.errorbar.html

    Examples
    --------
    - https://matplotlib.org/examples/axes_grid/scatter_hist.html
    - https://matplotlib.org/examples/api/scatter_piecharts.html
    - https://matplotlib.org/examples/lines_bars_and_markers/scatter_with_legend.html
    - https://matplotlib.org/examples/pie_and_polar_charts/polar_scatter_demo.html
    - https://matplotlib.org/examples/pylab_examples/scatter_custom_symbol.html
    - https://matplotlib.org/examples/pylab_examples/scatter_demo2.html
    - https://matplotlib.org/examples/pylab_examples/scatter_hist.html
    - https://matplotlib.org/examples/pylab_examples/scatter_masked.html
    - https://matplotlib.org/examples/pylab_examples/scatter_profile.html
    - https://matplotlib.org/examples/pylab_examples/scatter_star_poly.html
    - https://matplotlib.org/examples/pylab_examples/scatter_symbol.html
    - https://matplotlib.org/examples/shapes_and_collections/scatter_demo.html

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    xs, ys, x_el, x_er, y_et, y_eb, multiple_series = \
        _shared_preprocessing.prepare_vector_data_2d_multiple(x, y, kwargs)

    # Layout
    _plt.ioff()  # Required to prevent multiple outputs, not sure why it needs to be exactly here
    fig, ax = _matplotlib_processing.extract_fig_and_ax(kwargs)
    size_spec = _matplotlib_processing.set_plot_size(kwargs, fig)
    _matplotlib_processing.set_plot_color(kwargs, fig, ax)
    _matplotlib_processing.set_title(kwargs, ax)
    _matplotlib_processing.set_x_axis(kwargs, ax)
    _matplotlib_processing.set_y_axis(kwargs, ax)
    _matplotlib_processing.set_grid(kwargs, ax)
    legend_spec = _matplotlib_processing.extract_legend(kwargs)

    # Data
    marker_spec = _matplotlib_processing.extract_marker_spec(kwargs)
    line_spec = _matplotlib_processing.extract_line_spec(kwargs)
    colormap_spec = _matplotlib_processing.extract_colormap_spec(kwargs)
    x_error_spec = _matplotlib_processing.extract_x_error_spec(kwargs)
    y_error_spec = _matplotlib_processing.extract_y_error_spec(kwargs)
    count_colormaps = 0
    for i, (x_i, y_i) in enumerate(zip(xs, ys)):
        name_i = _shared_processing.get_next_name(name, i)
        color_i = _shared_processing.get_next_color(color, i)
        color_i = _matplotlib_processing.convert_color(color_i)
        opacity_i = _shared_processing.get_next_opacity(opacity, i)

        colormap_spec_i = _shared_processing.get_next_colormap_spec(colormap_spec, i)
        mpl_colormap_spec = _matplotlib_processing.convert_colormap_spec(colormap_spec_i)

        marker_spec_i = _shared_processing.get_next_marker_spec(
            marker_spec, color_i, opacity_i, mpl_colormap_spec['cmap'], i)
        mpl_marker_spec, show_marker = _matplotlib_processing.convert_marker_spec(
            marker_spec_i)

        line_spec_i = _shared_processing.get_next_line_spec(
            line_spec, color_i, opacity_i, mpl_colormap_spec['cmap'], i)
        mpl_line_spec, show_line = _matplotlib_processing.convert_line_spec(line_spec_i)

        x_error_spec_i = _shared_processing.get_next_x_error_spec(
            x_error_spec, line_spec_i, color_i, i)
        mpl_x_error_spec, show_x_error_bar = \
            _matplotlib_processing.convert_x_error_spec(x_error_spec_i)
        y_error_spec_i = _shared_processing.get_next_y_error_spec(
            y_error_spec, line_spec_i, color_i, opacity_i, i)
        mpl_y_error_bar_spec, show_y_error_bar, mpl_y_error_band_spec, show_y_error_band = \
            _matplotlib_processing.convert_y_error_spec(y_error_spec_i)

        # Plot
        if show_marker and show_line:
            result = ax.scatter(x_i, y_i, label=name_i, **mpl_marker_spec, zorder=12)
            ax.plot(x_i, y_i, **mpl_line_spec, zorder=11)
        elif show_marker:
            result = ax.scatter(x_i, y_i, label=name_i, **mpl_marker_spec, zorder=12)
        elif show_line:
            result = ax.plot(x_i, y_i, label=name_i, **mpl_line_spec, zorder=11)
        else:
            pass

        # Error bars and y error band
        if x_el or x_er or y_et or y_eb:
            if show_x_error_bar or show_y_error_bar:
                if show_x_error_bar and (x_el or x_er):
                    ax.errorbar(
                        x_i,
                        y_i,
                        xerr=[x_el[i], x_er[i]],
                        zorder=8,
                        fmt='none',
                        **mpl_x_error_spec,
                    )
                if show_y_error_bar and (y_et or y_eb):
                    ax.errorbar(
                        x_i,
                        y_i,
                        yerr=[y_eb[i], y_et[i]],
                        zorder=8,
                        fmt='none',
                        **mpl_y_error_bar_spec,
                    )

            if show_y_error_band and (y_et or y_eb):
                ax.fill_between(
                    x_i,
                    y1=[ym-yb for ym, yb in zip(y_i, y_eb[i])],
                    y2=[ym+yt for ym, yt in zip(y_i, y_et[i])],
                    zorder=7,
                    **mpl_y_error_band_spec,
                )

        if mpl_colormap_spec['show_colormap'] and count_colormaps == 0:
            colors = mpl_marker_spec['c']
            colors_represent_values = (
                isinstance(colors, _Iterable) and not isinstance(colors, str)
                and len(colors) == len(x_i) > 1)
            if colors_represent_values:
                collection = result
                _matplotlib_processing.set_colormap_properties(
                    ax, collection, mpl_colormap_spec)
                # Current design decision: Allow a maximum of one colormap to keep it tidy
                count_colormaps += 1

    # Legend
    show_legend = legend_spec['show_legend']
    legend_spec['show_legend'] = show_legend or (show_legend is None and multiple_series)
    _matplotlib_processing.set_legend(legend_spec, ax)

    # Figure
    return _Figure(fig, **size_spec)

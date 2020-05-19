"""Matplotlib plots for n-dimensional vector data."""

from collections.abc import Iterable as _Iterable

import matplotlib.pyplot as _plt

from .. import _logging
from .._unified_arguments import arguments as _args
from .._unified_arguments import shared_preprocessing as _shared_preprocessing
from .._unified_arguments import shared_processing as _shared_processing
from .._unified_arguments.injection import inject_functions as _inject_functions
from . import _matplotlib_processing, _plots_2d
from ._data_structures import Figure as _Figure


@_inject_functions(_args.external_fig_and_ax, _args.plot_size_and_resolution, _args.plot_color,
                   _args.plot_title, _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid)
def box(data, name=None, color=None, opacity=None, orientation='vertical',
        show_mean=False, show_notch=False, **kwargs):
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
        Name(s) of the visualized data series. Used in the axis description.
    color : str, tuple or list
        Color(s) of the plot elements, in this case the boxes.
        Possible values: See :ref:`colors`.
    opacity : float
        Opacity of the plot elements, in this case the boxes.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    orientation : str
        Orientation of the boxes. Possible values: "vertical", "horizontal"
    show_mean : bool
        Show or hide a dashed line in the box to represent the mean value.
    show_notch : bool
        Show or hide notches in the box to highlight the median value.

    Returns
    -------
    A :ref:`Figure <mpl-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.boxplot.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.boxplot.html

    Examples
    --------
    - https://matplotlib.org/examples/pylab_examples/boxplot_demo.html
    - https://matplotlib.org/examples/pylab_examples/boxplot_demo2.html
    - https://matplotlib.org/examples/pylab_examples/boxplot_demo3.html
    - https://matplotlib.org/examples/statistics/bxp_demo.html
    - https://matplotlib.org/examples/statistics/boxplot_color_demo.html
    - https://matplotlib.org/examples/statistics/boxplot_demo.html
    - https://matplotlib.org/examples/statistics/boxplot_vs_violin_demo.html
    - https://matplotlib.org/gallery/statistics/boxplot_color.html

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    data, name = _shared_preprocessing.prepare_vector_data_nd_stats(data, name, kwargs)
    _shared_preprocessing.warn_if_categorical_axis(kwargs)

    # Argument processing
    _shared_preprocessing.check_categorical_argument(
        orientation, 'orientation', ['vertical', 'horizontal'])

    # Layout
    _plt.ioff()  # Required to prevent multiple outputs, not sure why it needs to be exactly here
    fig, ax = _matplotlib_processing.extract_fig_and_ax(kwargs)
    size_spec = _matplotlib_processing.set_plot_size(kwargs, fig)
    _matplotlib_processing.set_plot_color(kwargs, fig, ax)
    _matplotlib_processing.set_title(kwargs, ax)
    x_tick_pos, x_label = _matplotlib_processing.set_x_axis(kwargs, ax)
    y_tick_pos, y_label = _matplotlib_processing.set_y_axis(kwargs, ax)
    _matplotlib_processing.set_grid(kwargs, ax)

    # Data
    names = _shared_processing.get_all_names(name, len(data))
    opacity_i = _shared_processing.get_next_opacity(opacity, i=0)

    # Figure
    result = ax.boxplot(
        data,
        vert=(orientation == 'vertical'),
        labels=names,
        sym='.k',
        widths=0.6,
        notch=show_notch,
        showmeans=show_mean,
        meanline=show_mean,
        boxprops=dict(linestyle='-', linewidth=1, color='black'),
        medianprops=dict(linestyle='-', linewidth=1, color='black'),
        meanprops=dict(linestyle='--', linewidth=1, color='black'),
        patch_artist=True,
    )

    # Axis modifications
    _matplotlib_processing.set_x_axis_post_plot(ax, x_tick_pos, x_label)
    _matplotlib_processing.set_y_axis_post_plot(ax, y_tick_pos, y_label)

    # Box modifications
    for i, patch in enumerate(result['boxes']):
        color_i = _shared_processing.get_next_color(color, i)
        color_i = _matplotlib_processing.convert_color(color_i)
        patch.set_facecolor(color_i)
        patch.set_alpha(opacity_i)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.external_fig_and_ax, _args.plot_size_and_resolution, _args.plot_color,
                   _args.plot_title, _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid,
                   _args.legend, _args.bins)
def histogram(data, name=None, color=None, opacity=None, bar_mode='group', orientation='vertical',
              **kwargs):
    """Create a histogram plot.

    Parameters
    ----------
    data : list of lists, pandas DataFrame, or filepath of a CSV file
        A list of lists. Each list may have a different number of items.
        If a list contains a non-numerical item (str, None, ...),
        the entire list will be removed automatically and a warning will be shown.
        If a list contains a numerical but non-finite item (NaN, +Inf, -Inf),
        the individual entry will be removed automatically and a warning will be shown.
    name : list
        Name(s) of the visualized data series. Used in the axis description.
    color : str, tuple or list
        Color(s) of the plot elements, in this case the bars.
        Possible values: See :ref:`colors`.
    opacity : float
        Opacity of the plot elements, in this case the bars.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    bar_mode : str
        How bars at the same location are displayed.
        Possible values: "group" (=next to each other, centered around the shared location),
        "stack" (=stacked on top of each another)
    orientation : str
        Orientation of the bars. Possible values: "vertical", "horizontal"

    Returns
    -------
    A :ref:`Figure <mpl-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.hist.html
    - https://matplotlib.org/devdocs/api/_as_gen/matplotlib.axes.Axes.hist.html

    Examples
    --------
    - https://matplotlib.org/examples/statistics/histogram_demo_features.html
    - https://matplotlib.org/examples/statistics/histogram_demo_histtypes.html
    - https://matplotlib.org/examples/statistics/histogram_demo_multihist.html
    - https://matplotlib.org/examples/statistics/multiple_histograms_side_by_side.html
    - https://matplotlib.org/examples/statistics/histogram_demo_cumulative.html

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    data, name = _shared_preprocessing.prepare_vector_data_nd_stats(data, name, kwargs)
    _shared_preprocessing.warn_if_categorical_axis(kwargs)

    # Argument processing
    _shared_preprocessing.check_categorical_argument(
        orientation, 'orientation', ['vertical', 'horizontal'])
    _shared_preprocessing.check_categorical_argument(
        bar_mode, 'bar_mode', ['stack', 'group'])
    histtype = 'barstacked' if bar_mode == 'stack' else 'bar'

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
    names = _shared_processing.get_all_names(name, len(data))
    colors = _shared_processing.get_all_colors(color, len(data))
    colors = [_matplotlib_processing.convert_color(color) for color in colors]
    opacity_i = _shared_processing.get_next_opacity(opacity, i=0)

    bin_spec = _matplotlib_processing.extract_bin_spec(kwargs)

    global_min = None
    global_max = None
    for x in data:
        x_min = min(x)
        x_max = max(x)
        if global_min is None or x_min < global_min:
            global_min = x_min
        if global_max is None or x_max > global_max:
            global_max = x_max
    global_data = [global_min, global_max]
    mpl_bin_spec = _matplotlib_processing.convert_bin_spec(
        bin_spec, global_data, half_bin_onto_borders=True)

    # Figure
    ax.hist(
        data,
        label=names,
        color=colors,
        alpha=opacity_i,
        rwidth=0.8,
        histtype=histtype,
        orientation=orientation,
        **mpl_bin_spec,
    )

    # Legend
    if legend_spec['show_legend'] is None:
        legend_spec['show_legend'] = len(data) > 1
    _matplotlib_processing.set_legend(legend_spec, ax)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.external_fig_and_ax, _args.plot_size_and_resolution, _args.plot_color,
                   _args.plot_title, _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid,
                   _args.colormap, _args.markers, _args.lines, _args.bins_2d)
def scatter_matrix(data, name=None, color=None, opacity=None,
                   show_diagonal=True, show_lower=True, show_upper=True,
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
        Name(s) of the visualized data series. Used in the plot descriptions.
    color : str, tuple or list
        Color(s) of the plot elements, in this case the markers and
        lines. Can be overruled by **marker_color** and **line_color**.
        Possible values: See :ref:`colors`.
    opacity : float
        Opacity of the plot elements, in this case the markers and lines.
        Can be overruled by **marker_opacity** and **line_opacity**.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    show_diagonal : bool
        Show or hide the plots on the diagonal of the matrix.
    show_lower : bool
        Show or hide the plots on the lower half of the matrix.
    show_upper : bool
        Show or hide the plots on the upper half of the matrix.

    Returns
    -------
    A :ref:`Figure <mpl-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.hist.html
    - https://matplotlib.org/devdocs/api/_as_gen/matplotlib.axes.Axes.hist.html

    Examples
    --------
    - https://matplotlib.org/examples/statistics/histogram_demo_features.html
    - https://matplotlib.org/examples/statistics/histogram_demo_histtypes.html
    - https://matplotlib.org/examples/statistics/histogram_demo_multihist.html
    - https://matplotlib.org/examples/statistics/multiple_histograms_side_by_side.html
    - https://matplotlib.org/examples/statistics/histogram_demo_cumulative.html

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    data, name = _shared_preprocessing.prepare_vector_data_nd(data, name)
    _shared_preprocessing.warn_if_categorical_axis(kwargs)

    # Argument processing
    for arg in ['show_colormap', 'show_legend']:
        if kwargs.get(arg, None) is True:
            _logging.report_inactive_argument(arg)

    # Layout
    num_series = len(data)
    _plt.ioff()  # Required to prevent multiple outputs, not sure why it needs to be exactly here
    fig, axes = _plt.subplots(num_series, num_series, sharex='col')
    size_spec = _matplotlib_processing.set_plot_size(kwargs, fig)
    _matplotlib_processing.set_super_title(kwargs, fig)

    # Data
    color_i = _shared_processing.get_next_color(color, i=0)
    color_i = _matplotlib_processing.convert_color(color_i)

    opacity_i = _shared_processing.get_next_opacity(opacity, i=0)

    colormap_spec = _matplotlib_processing.extract_colormap_spec(kwargs)
    colormap_spec['show_colormap'] = False
    marker_spec = _matplotlib_processing.extract_marker_spec(kwargs)
    line_spec = _matplotlib_processing.extract_line_spec(kwargs)

    bin_2d_spec = _matplotlib_processing.extract_bin_2d_spec(kwargs)
    bin_spec = {key: val for key, val in bin_2d_spec.items() if 'x_' in key}

    num_series = len(data)

    # Figure
    axes_left, axes_bottom = [], []
    for i in range(num_series):
        for j in range(num_series):
            try:
                ax = axes[i, j]
            except TypeError:
                ax = axes
            ax.tick_params(left=False, right=False, top=False, bottom=False,
                           labelleft=False, labelright=False, labeltop=False, labelbottom=False)
            is_diagonal = i == j
            is_lower_triangle = i > j
            is_upper_triangle = i < j
            is_left_column = j == 0
            is_bottom_row = i == num_series-1

            if is_diagonal:
                if show_diagonal:
                    try:
                        x = data[i]
                        histogram(
                            ax=ax, data=[x], color='black', **bin_spec,
                            show_x_title=False, show_y_title=False)
                        _matplotlib_processing.set_plot_color(kwargs, fig, ax, preserving=True)
                    except Exception as excp:
                        message = 'Exception during diagonal plotting: {}'.format(excp)
                        _logging.warn_user(message)
                else:
                    ax.set_axis_off()

            if is_lower_triangle:
                if show_lower:
                    try:
                        x = data[j]
                        y = data[i]
                        _plots_2d.scatter(
                            ax=ax, x=x, y=y, color=color_i, opacity=opacity_i,
                            **marker_spec, **line_spec, **colormap_spec,
                            show_x_title=False, show_y_title=False)
                        _matplotlib_processing.set_plot_color(kwargs, fig, ax, preserving=True)
                        _matplotlib_processing.set_grid(kwargs, ax, preserving=True)
                    except Exception as excp:
                        message = 'Exception during lower triangle plotting: {}'.format(excp)
                        _logging.warn_user(message)
                else:
                    ax.set_axis_off()

            if is_upper_triangle:
                if show_upper:
                    try:
                        x = data[j]
                        y = data[i]
                        _plots_2d.scatter(
                            ax=ax, x=x, y=y, color=color_i, opacity=opacity_i,
                            **marker_spec, **line_spec, **colormap_spec,
                            show_x_title=False, show_y_title=False)
                        _matplotlib_processing.set_plot_color(kwargs, fig, ax, preserving=True)
                        _matplotlib_processing.set_grid(kwargs, ax, preserving=True)
                    except Exception as excp:
                        message = 'Exception during upper triangle plotting: {}'.format(excp)
                        _logging.warn_user(message)
                else:
                    ax.set_axis_off()

            if is_left_column:
                axes_left.append(ax)
                kwargs['y_title'] = _shared_processing.get_next_name(name, i)
                ax.tick_params(left=True, labelleft=True)
                _matplotlib_processing.set_y_axis(kwargs, ax, preserving=True)

            if is_bottom_row:
                axes_bottom.append(ax)
                kwargs['x_title'] = _shared_processing.get_next_name(name, j)
                ax.tick_params(bottom=True, labelbottom=True)
                for tick in ax.get_xticklabels():
                    tick.set_rotation(90)
                _matplotlib_processing.set_x_axis(kwargs, ax, preserving=True)

    # Align axis titles
    try:
        fig.align_xlabels(axes_bottom)
        fig.align_ylabels(axes_left)
    except Exception:
        pass

    return _Figure(fig, **size_spec)


@_inject_functions(_args.external_fig_and_ax, _args.plot_size_and_resolution, _args.plot_color,
                   _args.plot_title, _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid)
def violin(data, name=None, color=None, opacity=None, violin_width=0.6, orientation='vertical',
           show_mean=False, show_median=True, show_extrema=True, **kwargs):
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
        Name(s) of the visualized data series. Used in the axis description.
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
        Show a dashed line at the position of the mean value of each series.
    show_median : bool
        Show a line at the position of the median value of each series.
    show_extrema : bool
        Show a line at the position of the min and max value of each series.
        Caution: The line along violin direction is also dependent on this option.


    Returns
    -------
    A :ref:`Figure <mpl-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.violinplot.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.violinplot.html

    Examples
    --------
    - https://matplotlib.org/examples/statistics/boxplot_vs_violin_demo.html
    - https://matplotlib.org/examples/statistics/violinplot_demo.html
    - https://matplotlib.org/examples/statistics/customized_violin_demo.html

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    data, name = _shared_preprocessing.prepare_vector_data_nd_stats(data, name, kwargs)
    _shared_preprocessing.warn_if_categorical_axis(kwargs)

    # Argument processing
    _shared_preprocessing.check_categorical_argument(
        orientation, 'orientation', ['vertical', 'horizontal'])

    # Layout
    _plt.ioff()  # Required to prevent multiple outputs, not sure why it needs to be exactly here
    fig, ax = _matplotlib_processing.extract_fig_and_ax(kwargs)
    size_spec = _matplotlib_processing.set_plot_size(kwargs, fig)
    _matplotlib_processing.set_plot_color(kwargs, fig, ax)
    _matplotlib_processing.set_title(kwargs, ax)
    x_tick_pos, x_label = _matplotlib_processing.set_x_axis(kwargs, ax)
    y_tick_pos, y_label = _matplotlib_processing.set_y_axis(kwargs, ax)
    _matplotlib_processing.set_grid(kwargs, ax)

    # Data
    name = _shared_processing.get_all_names(name, len(data))
    opacity_i = _shared_processing.get_next_opacity(opacity, i=0)

    # Figure
    components = ax.violinplot(
        data,
        widths=violin_width,
        showmeans=show_mean,
        showmedians=show_median,
        showextrema=show_extrema,
        vert=(orientation == 'vertical'),
    )

    # Plot component modifications
    for partname in ('cbars', 'cmins', 'cmaxes', 'cmedians', 'cmeans'):
        if partname in components:
            part = components[partname]
            part.set_linewidth(1)
            part.set_edgecolor('black')
            if partname == 'cmeans':
                part.set_linestyle('--')
    for i, component in enumerate(components['bodies']):
        color_i = _shared_processing.get_next_color(color, i)
        color_i = _matplotlib_processing.convert_color(color_i)
        component.set_facecolor(color_i)
        component.set_edgecolor('black')
        component.set_alpha(opacity_i)

    # Axis modifications
    if isinstance(name, _Iterable):
        if orientation == 'vertical':
            x_label = x_label if x_label else name
            x_tick_pos = x_tick_pos if x_tick_pos else list(range(1, len(name) + 1))
        else:
            y_label = y_label if x_label else name
            y_tick_pos = y_tick_pos if y_tick_pos else list(range(1, len(name) + 1))
    _matplotlib_processing.set_x_axis_post_plot(ax, x_tick_pos, x_label)
    _matplotlib_processing.set_y_axis_post_plot(ax, y_tick_pos, y_label)
    return _Figure(fig, **size_spec)

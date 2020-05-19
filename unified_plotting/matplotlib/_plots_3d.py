"""Matplotlib plots for 3-dimensional vector data."""

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
                   _args.colormap)
def contour(x, y, z, opacity=None,
            interpolation_method=None, interpolation_selection=None,
            interpolation_num_x_gridpoints=None, interpolation_num_y_gridpoints=None, **kwargs):
    """Create a contour plot.

    Parameters
    ----------
    x : list
        A list of numbers or if ``x_axis_scale="categorical"`` a list of strings.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
        The meaning of the ``n`` items in this list depends on the shape of ``z``.
    y : list
        A list of numbers or if ``y_axis_scale="categorical"`` a list of strings.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
        The meaning of the ``m`` items in this list depends on the shape of ``z``.
    z : list or list of lists
        A list of numbers or if ``z_axis_scale="categorical"`` a list of strings or a list of
        multiple such lists.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.

        There are two possible shapes for ``z``:

        1. A list of ``n`` items. In this case, ``x`` and ``y`` need to have the same number
           of items as ``z``. Each entry represents a point at an arbitrary position in 3D space.
           In order to get a valid description of a surface, a regular grid of points is created
           automatcially based on the ranges of ``x`` and ``y`` and then interpolation is
           performed to get a height for each point that fits to the closest ``z`` values.

        2. A list of ``m`` lists, each containing ``n`` items. In this case, ``x`` needs to
           have ``n`` items and ``y`` needs to have ``m`` items. ``x`` and ``y``
           form the basis of a rectilinear ``n x m`` grid of points and ``z`` provides the
           height of each. No interpolation is performed because the input is already a valid
           description of a surface.
    opacity : float
        Opacity of the plot elements, in this case the contour areas.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    interpolation_method : str
        Method for calculating the unknown values at regular grid points that sit between
        the given points with known values.
        Caution: Currently this becomes only active if the given data points are not already on
        a regular grid.
        Possible values: "allrounder_linear", "allrounder_nearest", "allrounder_cubic",
        "rbf_cubic", "rbf_gaussian", "rbf_inverse", "rbf_linear", "rbf_multiquadric",
        "rbf_quintic", "rbf_thin_plate", "spline_linear", "spline_cubic", "spline_quintic".
    interpolation_selection : str
        If at the same x, y point there are multiple known z-values, which one shall be used,
        i.e. through which one shall the surface go.
        Possible values: "min", "max".
    interpolation_num_x_gridpoints : int
        Number of grid points along the x-Axis.
    interpolation_num_y_gridpoints : int
        Number of grid points along the y-Axis.

    Returns
    -------
    A :ref:`Figure <mpl-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.contour.html
    - https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.contour.html

    Examples
    --------
    - https://matplotlib.org/examples/pylab_examples/tricontour_vs_griddata.html
    - https://jakevdp.github.io/PythonDataScienceHandbook/04.04-density-and-contour-plots.html

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    x, y, z = _shared_preprocessing.prepare_vector_data_3d_grid(
        x, y, z, kwargs, interpolation_method, interpolation_selection,
        interpolation_num_x_gridpoints, interpolation_num_y_gridpoints)

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

    # Figure
    result = ax.contourf(x, y, z, cmap=mpl_colormap_spec['cmap'], alpha=opacity_i)

    if mpl_colormap_spec['show_colormap']:
        collection = result
        _matplotlib_processing.set_colormap_properties(ax, collection, mpl_colormap_spec)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.external_fig_and_ax_3d, _args.plot_size_and_resolution, _args.plot_color,
                   _args.plot_title,
                   _args.x_axis, _args.y_axis, _args.z_axis,
                   _args.x_grid, _args.y_grid, _args.z_grid,
                   _args.legend, _args.markers, _args.lines, _args.colormap)
def scatter_3d(x, y, z, name=None, color=None, opacity=None,
               camera_angle_vertical=30.0, camera_angle_horizontal=-60.0, **kwargs):
    """Create a 3D scatter plot.

    Note: Currently there seems to be no straightforward way to specify an axis ratio in 3D plots.

    Parameters
    ----------
    x : list or list of lists
        A list of numbers or if ``x_axis_scale="categorical"`` a list of strings or a
        list of multiple such lists. It needs to have the same number of items as ``y`` and ``z``.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
    y : list or list of lists
        A list of numbers or if ``y_axis_scale="categorical"`` a list of strings or a
        list of multiple such lists. It needs to have the same number of items as ``x`` and ``z``.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
    z : list or list of lists
        A list of numbers or if ``z_axis_scale="categorical"`` a list of strings or a
        list of multiple such lists. It needs to have the same number of items as ``x`` and ``y``.
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
    camera_angle_vertical : float
        Vertical camera angle in degree.
    camera_angle_horizontal : float
        Horizontal camera angle in degree.

    Returns
    -------
    A :ref:`Figure <mpl-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://matplotlib.org/mpl_toolkits/index.html#mplot3d
    - https://matplotlib.org/api/toolkits/mplot3d.html#toolkit-mplot3d-api
    - https://matplotlib.org/mpl_toolkits/mplot3d/api.html#mpl_toolkits.mplot3d.axes3d.Axes3D.view_init
    - https://matplotlib.org/api/_as_gen/mpl_toolkits.mplot3d.axes3d.Axes3D.html#mpl_toolkits.mplot3d.axes3d.Axes3D.scatter
    - https://matplotlib.org/gallery/mplot3d/scatter3d.html

    Examples
    --------
    - https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html
    - https://matplotlib.org/examples/mplot3d/surface3d_demo.html
    - https://matplotlib.org/examples/mplot3d/custom_shaded_3d_surface.html
    - https://matplotlib.org/examples/mplot3d/contour3d_demo.html
    - https://matplotlib.org/examples/mplot3d/contour3d_demo2.html
    - https://matplotlib.org/examples/mplot3d/contour3d_demo3.html
    - https://matplotlib.org/examples/mplot3d/contourf3d_demo.html
    - https://matplotlib.org/examples/mplot3d/contourf3d_demo2.html
    - http://scipy-cookbook.readthedocs.io/items/Matplotlib_mplot3D.html

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    xs, ys, zs, multiple_series = _shared_preprocessing.prepare_vector_data_3d_multiple(
        x, y, z, kwargs)

    # Layout
    _plt.ioff()  # Required to prevent multiple outputs, not sure why it needs to be exactly here.
    fig, ax = _matplotlib_processing.extract_fig_and_ax_3d(kwargs)
    size_spec = _matplotlib_processing.set_plot_size(kwargs, fig)
    _matplotlib_processing.set_plot_color(kwargs, fig, ax)
    _matplotlib_processing.set_title(kwargs, ax)
    _matplotlib_processing.set_x_axis_3d(kwargs, ax)
    _matplotlib_processing.set_y_axis_3d(kwargs, ax)
    _matplotlib_processing.set_z_axis_3d(kwargs, ax)
    _matplotlib_processing.set_grid_3d(kwargs, ax)

    # Data
    marker_spec = _matplotlib_processing.extract_marker_spec(kwargs)
    line_spec = _matplotlib_processing.extract_line_spec(kwargs)
    colormap_spec = _matplotlib_processing.extract_colormap_spec(kwargs)
    legend_spec = _matplotlib_processing.extract_legend(kwargs)

    count_colormaps = 0
    for i, (x_i, y_i, z_i) in enumerate(zip(xs, ys, zs)):
        # Preparation
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

        # Points and lines
        if show_line and show_marker:
            ax.plot(x_i, y_i, z_i, zorder=11, **mpl_line_spec)
            result = ax.scatter(x_i, y_i, z_i, zorder=12, label=name_i, **mpl_marker_spec)
        elif show_marker:
            result = ax.scatter(x_i, y_i, z_i, zorder=12, label=name_i, **mpl_marker_spec)
        elif show_line:
            ax.plot(x_i, y_i, z_i, zorder=11, label=name_i, **mpl_line_spec)
        else:
            pass

        # Colorbar
        if mpl_colormap_spec['show_colormap'] and count_colormaps == 0:
            colors = mpl_marker_spec['c']
            colors_represent_values = (
                isinstance(colors, _Iterable) and not isinstance(colors, str)
                and len(colors) == len(x_i))
            if colors_represent_values and show_marker:
                collection = result
                _matplotlib_processing.set_colormap_properties(ax, collection, mpl_colormap_spec)
                # Current design decision: Allow a maximum of one colormap to keep it tidy
                count_colormaps += 1

    # Legend
    show_legend = legend_spec['show_legend']
    legend_spec['show_legend'] = show_legend or (show_legend is None and multiple_series)
    _matplotlib_processing.set_legend(legend_spec, ax)

    # View angles
    ax = fig.axes[0]
    ax.view_init(elev=camera_angle_vertical, azim=camera_angle_horizontal)

    # Figure
    return _Figure(fig, **size_spec)

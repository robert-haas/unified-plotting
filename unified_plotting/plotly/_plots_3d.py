"""Plotly plots for 3-dimensional vector data."""

from collections.abc import Iterable as _Iterable

import numpy as _np
import plotly.figure_factory as _figure_factory
import plotly.graph_objs as _go
from scipy.spatial import Delaunay as _Delaunay

from .. import _logging
from .._unified_arguments import arguments as _args
from .._unified_arguments import shared_preprocessing as _shared_preprocessing
from .._unified_arguments import shared_processing as _shared_processing
from .._unified_arguments.injection import inject_functions as _inject_functions
from ..utilities import interpolation as _interpolation
from . import _plotly_processing
from ._data_structures import Figure as _Figure


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid,
                   _args.colormap)
def contour(x, y, z, opacity=None, axis_aspect_ratio=None,
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
    axis_aspect_ratio : tuple
        Ratio of the three axis lengths.
        Requires a tuple of float numbers of form (x_ratio, y_ratio, z_ratio),
        for example (1.0, 1.0, 0.7).
        Default value: (1.0, 1.0, 1.0), leads to all axes having equal display size.
    interpolation_method : str
        Method for calculating the unknown values at regular grid
        points that sit between the given points with known values.
        Caution: Currently this becomes only active if the given data points are not already on
        a regular grid.
        Possible values: "allrounder_linear", "allrounder_nearest", "allrounder_cubic",
        "rbf_cubic", "rbf_gaussian", "rbf_inverse", "rbf_linear", "rbf_multiquadric",
        "rbf_quintic", "rbf_thin_plate", "spline_linear", "spline_cubic", "spline_quintic".
    interpolation_selection : str
        If at the same x, y point there are multiple known z-values,
        which one shall be used, i.e. through which one shall the surface go.
        Possible values: "min", "max".
    interpolation_num_x_gridpoints : int
        Number of grid points along the x-Axis.
    interpolation_num_y_gridpoints : int
        Number of grid points along the y-Axis.

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://plot.ly/python/reference/#contour

    Examples
    --------
    - https://plot.ly/python/contour-plots

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    x, y, z = _shared_preprocessing.prepare_vector_data_3d_grid(
        x, y, z, kwargs, interpolation_method, interpolation_selection,
        interpolation_num_x_gridpoints, interpolation_num_y_gridpoints)

    # Argument processing
    if axis_aspect_ratio is None:
        axis_aspect_ratio = dict(x=1.0, y=1.0, z=1.0)
    else:
        x_ratio, y_ratio, z_ratio = axis_aspect_ratio
        axis_aspect_ratio = dict(x=x_ratio, y=y_ratio, z=z_ratio)

    # Layout
    layout = _go.Layout(scene=dict(aspectmode='manual', aspectratio=axis_aspect_ratio))
    size_spec = _plotly_processing.set_plot_size(kwargs, layout)
    _plotly_processing.set_plot_color(kwargs, layout)
    _plotly_processing.set_title(kwargs, layout)
    _plotly_processing.set_x_axis(kwargs, layout)
    _plotly_processing.set_y_axis(kwargs, layout)
    _plotly_processing.set_grid(kwargs, layout)

    # Data
    opacity_i = _shared_processing.get_next_opacity(opacity, i=0)

    colormap_spec = _plotly_processing.extract_colormap_spec(kwargs)
    plotly_colormap_spec = _plotly_processing.convert_colormap_spec(colormap_spec)

    trace = _go.Contour(
        x=x,
        y=y,
        z=z,
        opacity=opacity_i,
        **plotly_colormap_spec,
    )
    data = [trace]

    # Figure
    fig = _go.Figure(data=data, layout=layout)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid,
                   _args.colormap)
def heatmap(x, y, z, opacity=None, **kwargs):
    """Create a heatmap plot.

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

        2. A list of ``m`` lists, each containing ``n`` items. In this case, ``x`` needs to
           have ``n`` items and ``y`` needs to have ``m`` items. ``x`` and ``y``
           form the basis of a rectilinear ``n x m`` grid of points and ``z`` provides the
           height of each.
    opacity : float
        Opacity of the plot elements, in this case the contour lines.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://plot.ly/python/reference/#heatmap

    Examples
    --------
    - https://plot.ly/python/heatmaps

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    x, y, z = _shared_preprocessing.prepare_vector_data_3d_grid(
        x, y, z, kwargs, interpolate=False)

    # Layout
    layout = _go.Layout()
    size_spec = _plotly_processing.set_plot_size(kwargs, layout)
    _plotly_processing.set_plot_color(kwargs, layout)
    _plotly_processing.set_title(kwargs, layout)
    _plotly_processing.set_x_axis(kwargs, layout)
    _plotly_processing.set_y_axis(kwargs, layout)
    _plotly_processing.set_grid(kwargs, layout)

    # Data
    opacity_i = _shared_processing.get_next_opacity(opacity, i=0)

    colormap_spec = _plotly_processing.extract_colormap_spec(kwargs)
    plotly_colormap_spec = _plotly_processing.convert_colormap_spec(colormap_spec)

    trace = _go.Heatmap(
        x=x,
        y=y,
        z=z,
        opacity=opacity_i,
        **plotly_colormap_spec,
    )
    data = [trace]

    # Figure
    fig = _go.Figure(data=data, layout=layout)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.x_axis, _args.y_axis, _args.z_axis,
                   _args.x_grid, _args.y_grid, _args.z_grid,
                   _args.legend, _args.markers, _args.lines, _args.colormap)
def scatter_3d(x, y, z, name=None, color=None, opacity=None, axis_aspect_ratio=None,
               camera_position=None,
               # Stems
               show_stem_x=False, show_stem_y=False, show_stem_z=False, show_stem_line=True,
               stem_x_position=None, stem_y_position=None, stem_z_position=None,
               stem_shift_factor=0.05,
               # Interpolation allrounder
               interpolation_with_highest_points=True, interpolation_num_gridpoints=200,
               show_interpolation_allrounder=False, interpolation_allrounder_method='nearest',
               # Interpolation delaunay
               show_interpolation_delaunay=False,
               # Interpolation rbf
               show_interpolation_rbf=False, interpolation_rbf_method='linear',
               # Interpolation spline
               show_interpolation_spline=False, interpolation_spline_method='linear',
               **kwargs):
    """Create a 3D scatter plot.

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
        Color(s) of the plot elements, in this case the markers and
        lines. Can be overruled by **marker_color** and **line_color**.
        Possible values: See :ref:`colors`.
    opacity : float
        Opacity of the plot elements, in this case the markers and
        lines. Can be overruled by **marker_opacity** and **line_opacity**.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    axis_aspect_ratio : tuple
        Ratio of the three axis sizes.
        Requires a tuple of float numbers of form (x_ratio, y_ratio, z_ratio),
        for example (1.0, 1.0, 0.5) leads to a z axis which is half the size of x and y.
        Default value: (1.0, 1.0, 1.0), leads to all axes having equal display size.
    camera_position : list of tuples
        The camera position is defined by three vectors with three entries each:

        1. Up vector: Determines the up direction on the page. Default: (0, 0, 1)
        2. Center vector: Determines the center point. Default: (0, 0, 0)
        3. Eye vector: Determines the position of the camera. Default: (1.25, 1.25, 1.25)

        For more information, see https://plot.ly/python/3d-camera-controls

        Example: [(0, 0, 1), (0, 0, 0), (1.25, 1.25, 1.25)]
    show_stem_x : bool
        Show or hide marker projection in x-direction.
    show_stem_y : bool
        Show or hide marker projection in y-direction.
    show_stem_z : bool
        Show or hide marker projection in z-direction.
    show_stem_line : bool
        Show or hide stem line.
    stem_x_position : float
        Position on x-Axis where projection plane is drawn.
    stem_y_position : float
        Position on y-Axis where projection plane is drawn.
    stem_z_position : float
        Position on z-Axis where projection plane is drawn.
    stem_shift_factor : float
        Factor that determines the distance of the projection planes from the data points.
        Default: 0.05 means a distance of 5% of the span of the data.
    interpolation_with_highest_points : bool
        If several z-values are present at the same xy-point, use the highest value for the
        surface to go through (True), or the lowest (False).
    interpolation_num_gridpoints : int
        Number of grid points along both x- and y-Axis.
    show_interpolation_allrounder : bool
        Show or hide an interpolated surface calculated with an allrounder method from SciPy.
    interpolation_allrounder_method : str
        Choose which allrounder method is used.
        Default: "nearest".
        Possible values: "linear", "nearest", "cubic".
    show_interpolation_delaunay : bool
        Show or hide an interpolated surface calculated with
        Delaunay method by Plotly.
    show_interpolation_rbf : bool
        Show or hide an interpolated surface calculated
        with a radial basis function (RBF) method from SciPy.
    interpolation_rbf_method : str
        Choose which radial basis function (RBF) is used.
        Default: "linear".
        Possible values: "cubic", "gaussian", "inverse", "linear", "multiquadric", "quintic",
        "thin_plate".
    show_interpolation_spline : bool
        Show or hide an interpolated surface calculated with a spline method from SciPy.
    interpolation_spline_method : str
        Choose which spline is used.
        Default: "linear".
        Possible values: "linear", "cubic", "quintic".

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://plot.ly/python/reference/#scatter3d

    Examples
    --------
    - https://plot.ly/python/3d-scatter-plots

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    xs, ys, zs, multiple_series = _shared_preprocessing.prepare_vector_data_3d_multiple(
        x, y, z, kwargs)

    # Argument processing
    axis_aspect_ratio_spec = _plotly_processing.convert_axis_aspect_ratio(axis_aspect_ratio)
    camera_spec = _plotly_processing.convert_camera_position(camera_position)

    # Layout
    layout = _go.Layout(scene=dict(aspectmode='manual', aspectratio=axis_aspect_ratio_spec))
    size_spec = _plotly_processing.set_plot_size(kwargs, layout)
    _plotly_processing.set_plot_color_3d(kwargs, layout)
    _plotly_processing.set_title(kwargs, layout)
    _plotly_processing.set_x_axis_3d(kwargs, layout)
    _plotly_processing.set_y_axis_3d(kwargs, layout)
    _plotly_processing.set_z_axis_3d(kwargs, layout)
    _plotly_processing.set_grid_3d(kwargs, layout)
    legend_spec = _plotly_processing.extract_legend(kwargs)
    if camera_spec is not None:
        layout['scene']['camera'] = camera_spec

    # Data
    marker_spec = _plotly_processing.extract_marker_spec(kwargs)
    line_spec = _plotly_processing.extract_line_spec(kwargs)
    colormap_spec = _plotly_processing.extract_colormap_spec(kwargs)

    if show_stem_x or show_stem_y or show_stem_z:
        x_bound, y_bound, z_bound = _shared_processing.calc_stem_plane_position(
            xs, ys, zs, stem_shift_factor, stem_x_position, stem_y_position, stem_z_position)

    data = []
    count_colormaps = 0
    for i, (x_i, y_i, z_i) in enumerate(zip(xs, ys, zs)):
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
            marker_spec_i, is_3d=True)
        plotly_marker_spec['size'] /= 3.5  # Correction factor for same appearance as in 2d
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

        mode = _plotly_processing.get_scatter_mode(show_marker, show_line)

        # Stem plots
        if show_stem_x or show_stem_y or show_stem_z:
            x_new, y_new, z_new = [], [], []
            if show_stem_x:
                for x_val, y_val, z_val in zip(x_i, y_i, z_i):
                    x_new.extend([x_bound, x_val, None])
                    y_new.extend([y_val, y_val, None])
                    z_new.extend([z_val, z_val, None])
            if show_stem_y:
                for x_val, y_val, z_val in zip(x_i, y_i, z_i):
                    x_new.extend([x_val, x_val, None])
                    y_new.extend([y_bound, y_val, None])
                    z_new.extend([z_val, z_val, None])
            if show_stem_z:
                for x_val, y_val, z_val in zip(x_i, y_i, z_i):
                    x_new.extend([x_val, x_val, None])
                    y_new.extend([y_val, y_val, None])
                    z_new.extend([z_bound, z_val, None])
            if isinstance(plotly_marker_spec['color'], str):
                marker_color = plotly_marker_spec['color']
            else:
                marker_color = []
                for num in plotly_marker_spec['color']:
                    marker_color.extend([num]*3)
                marker_color = marker_color*3
            if show_stem_line:
                stem_mode = 'markers+lines'
            else:
                stem_mode = 'markers'
            trace_stems = _go.Scatter3d(
                x=x_new,
                y=y_new,
                z=z_new,
                name=name_i,
                hoverinfo='skip',
                mode=stem_mode,
                connectgaps=False,
                marker=dict(
                    size=plotly_marker_spec['size']*0.8,
                    color=marker_color,
                    colorscale=plotly_marker_spec['colorscale'],
                    opacity=plotly_marker_spec['opacity'] / 2.5,
                ),
                line=dict(
                    width=0.7,
                    color='rgba(0,0,0,0.08)'
                ),
                legendgroup='stems',
                showlegend=False,
            )
            data.append(trace_stems)

        # Interpolated surface plots with different interpolaiton methods
        def create_error_message(interpolation_method, exception):
            message = (
                '{} interpolation failed. The corresponding surface could not be plotted. '
                '\nError: {}'.format(interpolation_method, exception))
            return message

        show_any_interpolation = (
            show_interpolation_delaunay or show_interpolation_delaunay or
            show_interpolation_allrounder or show_interpolation_rbf or
            show_interpolation_spline)
        if show_any_interpolation:
            if interpolation_with_highest_points:
                interpolation_mode = 'max'
            else:
                interpolation_mode = 'min'
            x_unique, y_unique, z_unique = _interpolation.remove_duplicate_xy_points(
                x_i, y_i, z_i, interpolation_mode)
        plotly_colormap_spec['showscale'] = False
        if show_interpolation_delaunay:
            # https://community.plotly.com/t/what-colorscales-are-available-in-plotly-and-which-are-the-default/2079
            accepted_colormaps = [
                'Blackbody', 'Bluered', 'Blues', 'Earth', 'Cividis', 'Electric', 'Greens',
                'Greys', 'Hot', 'Jet', 'Picnic', 'Portland', 'Rainbow', 'RdBu', 'Reds',
                'Viridis', 'YlGnBu', 'YlOrRd']
            try:
                try:
                    cm_name = plotly_colormap.lower()
                    for item in accepted_colormaps:
                        if cm_name == item.lower():
                            plotly_colormap = item
                            break
                    else:
                        raise ValueError
                except Exception:
                    message = (
                        'Surfaces from Delaunay interpolation accept only a restricted set '
                        'of colormaps: {}'.format(accepted_colormaps))
                    raise ValueError(message) from None
                points_2d = list(zip(x_unique, y_unique))
                tri = _Delaunay(points_2d)
                simplices = tri.simplices
                fig_interpolation = _figure_factory.create_trisurf(
                    x=x_unique,
                    y=y_unique,
                    z=z_unique,
                    simplices=simplices,
                    colormap=plotly_colormap,
                    showbackground=False,
                    plot_edges=True
                )
                trace_interpolation = fig_interpolation.data[0]
                trace_interpolation['opacity'] = opacity_i
                data.append(trace_interpolation)
            except Exception as excp:
                message = create_error_message('Delaunay', excp)
                _logging.warn_user(message)
        if show_interpolation_allrounder:
            try:
                x_grid, y_grid, z_interp_on_grid = _interpolation.allrounder(
                    x_unique, y_unique, z_unique, method=interpolation_allrounder_method,
                    num_x_gridpoints=interpolation_num_gridpoints,
                    num_y_gridpoints=interpolation_num_gridpoints)
                trace_interpolation = _go.Surface(
                    x=x_grid,
                    y=y_grid,
                    z=z_interp_on_grid,
                    hoverinfo='skip',
                    opacity=opacity_i,
                    **plotly_colormap_spec,
                )
                data.append(trace_interpolation)
            except Exception as excp:
                message = create_error_message('Allrounder', excp)
                _logging.warn_user(message)
        if show_interpolation_rbf:
            try:
                x_grid, y_grid, z_interp_on_grid = _interpolation.radial_basis_function(
                    x_unique, y_unique, z_unique, method=interpolation_rbf_method,
                    num_x_gridpoints=interpolation_num_gridpoints,
                    num_y_gridpoints=interpolation_num_gridpoints)
                trace_interpolation = _go.Surface(
                    x=x_grid,
                    y=y_grid,
                    z=z_interp_on_grid,
                    hoverinfo='skip',
                    opacity=opacity_i,
                    **plotly_colormap_spec,
                )
                data.append(trace_interpolation)
            except Exception as excp:
                message = create_error_message('RBF', excp)
                _logging.warn_user(message)
        if show_interpolation_spline:
            try:
                x_grid, y_grid, z_interp_on_grid = _interpolation.spline(
                    x_unique, y_unique, z_unique, method=interpolation_spline_method,
                    num_x_gridpoints=interpolation_num_gridpoints,
                    num_y_gridpoints=interpolation_num_gridpoints)
                trace_interpolation = _go.Surface(
                    x=x_grid,
                    y=y_grid,
                    z=z_interp_on_grid,
                    hoverinfo='skip',
                    opacity=opacity_i,
                    **plotly_colormap_spec,
                )
                data.append(trace_interpolation)
            except Exception as excp:
                message = create_error_message('Spline', excp)
                _logging.warn_user(message)

        # Points and lines
        if show_marker or show_line:
            trace_points = _go.Scatter3d(
                x=x_i,
                y=y_i,
                z=z_i,
                name=name_i,
                hoverinfo='all',
                marker=plotly_marker_spec,
                line=plotly_line_spec,
                mode=mode,
            )
            data.append(trace_points)

    # Legend
    show_legend = legend_spec['show_legend']
    legend_spec['show_legend'] = show_legend or (show_legend is None and multiple_series)
    _plotly_processing.set_legend(legend_spec, layout)

    # Figure
    fig = _go.Figure(data=data, layout=layout)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.x_axis, _args.y_axis, _args.z_axis,
                   _args.x_grid, _args.y_grid, _args.z_grid,
                   _args.colormap)
def surface(x, y, z, opacity=None, axis_aspect_ratio=None, camera_position=None,
            show_surface=True, surface_opacity=1.0,
            show_projection_x=False, show_projection_y=False, show_projection_z=False,
            projection_x_opacity=1.0, projection_y_opacity=1.0, projection_z_opacity=1.0,
            projection_shift_factor=0.05,
            interpolation_method=None, interpolation_selection=None,
            interpolation_num_x_gridpoints=None, interpolation_num_y_gridpoints=None,
            **kwargs):
    """Create a surface plot.

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
        Opacity of the plot elements, in this case the contour lines.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    axis_aspect_ratio : tuple
        Ratio of the three axis sizes.
        Requires a tuple of float numbers of form (x_ratio, y_ratio, z_ratio),
        for example (1.0, 1.0, 0.5) leads to a z axis which is half the size of x and y.
        Default value: (1.0, 1.0, 1.0), leads to all axes having equal display size.
    camera_position : list of tuples
        The camera position is defined by three vectors with three entries each:

        1. Up vector: Determines the up direction on the page. Default: (0, 0, 1)
        2. Center vector: Determines the center point. Default: (0, 0, 0)
        3. Eye vector: Determines the position of the camera. Default: (1.25, 1.25, 1.25)

        For more information, see https://plot.ly/python/3d-camera-controls

        Example: [(0, 0, 1), (0, 0, 0), (1.25, 1.25, 1.25)]
    show_surface : bool
        Show or hide the 3D surface.
    surface_opacity : float
        Opacity of the 3D surface.
        Overrules ``opacity``.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    show_projection_x : bool
        Show or hide the projection in x-direction onto the yz-plane.
    show_projection_y : bool
        Show or hide the projection in y-direction onto the xz-plane.
    show_projection_z : bool
        Show or hide the projection in z-direction onto the xy-plane.
    projection_x_opacity : float
        Opacity of the projection in x-direction.
        Overrules ``opacity``.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    projection_y_opacity : float
        Opacity of the projection in y-direction.
        Overrules ``opacity``.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    projection_z_opacity : float
        Opacity of the projection in z-direction.
        Overrules ``opacity``.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).
    projection_shift_factor : float
        Factor that determines the distance of the projection planes from the data points.
        Default: 0.05 means a distance of 5% of the span of the data.
    interpolation_method : str
        Method for calculating the unknown values at regular grid points that sit between the
        given points with known values.
        Caution: Currently this becomes only active if the given data points are not already on
        a regular grid.
        Possible values: "allrounder_linear", "allrounder_nearest", "allrounder_cubic",
        "rbf_cubic", "rbf_gaussian", "rbf_inverse", "rbf_linear", "rbf_multiquadric",
        "rbf_quintic", "rbf_thin_plate", "spline_linear", "spline_cubic", "spline_quintic".
    interpolation_selection : str
        If at the same x, y point there are multiple known z-values,
        which one shall be used, i.e. through which one shall the surface go.
        Possible values: "min", "max".
    interpolation_num_x_gridpoints : int
        Number of grid points along the x-Axis.
    interpolation_num_y_gridpoints : int
        Number of grid points along the y-Axis.

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://plot.ly/python/reference/#surface

    Examples
    --------
    - https://plot.ly/python/3d-surface-plots
    - https://plot.ly/python/2d-projection-of-3d-surface

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    x, y, z = _shared_preprocessing.prepare_vector_data_3d_grid(
        x, y, z, kwargs, interpolation_method, interpolation_selection,
        interpolation_num_x_gridpoints, interpolation_num_y_gridpoints)

    # Argument processing
    axis_aspect_ratio_spec = _plotly_processing.convert_axis_aspect_ratio(axis_aspect_ratio)
    camera_spec = _plotly_processing.convert_camera_position(camera_position)

    # Layout
    layout = _go.Layout(scene=dict(aspectmode='manual', aspectratio=axis_aspect_ratio_spec))
    size_spec = _plotly_processing.set_plot_size(kwargs, layout)
    _plotly_processing.set_plot_color_3d(kwargs, layout)
    _plotly_processing.set_title(kwargs, layout)
    _plotly_processing.set_x_axis_3d(kwargs, layout)
    _plotly_processing.set_y_axis_3d(kwargs, layout)
    _plotly_processing.set_z_axis_3d(kwargs, layout)
    _plotly_processing.set_grid_3d(kwargs, layout)
    if camera_spec is not None:
        layout['scene']['camera'] = camera_spec

    # Data
    opacity_i = _shared_processing.get_next_opacity(opacity, i=0)
    if surface_opacity is None:
        surface_opacity = opacity_i

    colormap_spec = _plotly_processing.extract_colormap_spec(kwargs)
    plotly_colormap_spec = _plotly_processing.convert_colormap_spec(colormap_spec)

    data = []
    if show_surface:
        trace_surface = _go.Surface(
            x=x,
            y=y,
            z=z,
            opacity=surface_opacity,
            **plotly_colormap_spec,
        )
        data.append(trace_surface)
    if show_projection_x or show_projection_y or show_projection_z:
        x, y, z = _np.array(x), _np.array(y), _np.array(z)
        x_bound, y_bound, z_bound = _shared_preprocessing.shift_away_from_extrema(
            x, y, z, direction='lower', shift_factor=projection_shift_factor)

    plotly_colormap_spec['showscale'] = False
    if show_projection_x:
        x_offset = x_bound * _np.ones(x.shape)
        trace_projection_x = _go.Surface(
            x=x_offset,
            y=y,
            z=z,
            opacity=projection_x_opacity,
            surfacecolor=z,
            hoverinfo='skip',
            **plotly_colormap_spec,
        )
        data.append(trace_projection_x)
    if show_projection_y:
        y_offset = y_bound * _np.ones(y.shape)
        trace_projection_y = _go.Surface(
            x=x,
            y=y_offset,
            z=z,
            opacity=projection_y_opacity,
            surfacecolor=z,
            hoverinfo='skip',
            **plotly_colormap_spec,
        )
        data.append(trace_projection_y)
    if show_projection_z:
        z_offset = z_bound * _np.ones(z.shape)
        trace_projection_z = _go.Surface(
            x=x,
            y=y,
            z=z_offset,
            opacity=projection_z_opacity,
            surfacecolor=z,
            hoverinfo='skip',
            **plotly_colormap_spec,
        )
        data.append(trace_projection_z)

    # Figure
    fig = _go.Figure(data=data, layout=layout)
    return _Figure(fig, **size_spec)

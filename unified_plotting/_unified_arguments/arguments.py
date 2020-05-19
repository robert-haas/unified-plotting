"""Definition of unified arguments that can be injected to plotting functions.

Design decisions for unified arguments:

- Plotly tries to decouple plot layout from data. This is mimicked to some degree here.
- Parameter names contain no plural nouns, only singular ones.
   - It prevents sources of inconsistency like markers_color/marker_colors/markers_colors
   - It facilitates easier remembering of parameter names for frequent users
   - It has the downside of some unintuitive name-value pairs in case of iterables,
     e.g. tick_position needs a list of values for tick positions
- Wrong parameter values are reported as ValueError together with possible correct values
- Arbitrary conventions for consistency
   - Parameter order: font - size - color - position/length/width/...
   - Parameter documentation:
     - Listing of possible values, for example: Possible values: "left", "center", "right".
     - Hints if feature is not available, e.g. "Currently not available for Plotly".
     - Consistent names for bool arguments, e.g. "show_..."
     - Parameter that is overruled by other parameter, for example: Overrules ...
"""

import inspect as _inspect
import re as _re
import sys as _sys
from collections import OrderedDict as _OrderedDict


def plot_size_and_resolution(width_mm=None, width_in=None, width_pt=None,
                             height_mm=None, height_in=None, height_pt=None,
                             dpi=None,
                             margin_auto=None,
                             margin_left_mm=None, margin_left_in=None, margin_left_pt=None,
                             margin_left_rel=None,
                             margin_right_mm=None, margin_right_in=None, margin_right_pt=None,
                             margin_right_rel=None,
                             margin_top_mm=None, margin_top_in=None, margin_top_pt=None,
                             margin_top_rel=None,
                             margin_bottom_mm=None, margin_bottom_in=None, margin_bottom_pt=None,
                             margin_bottom_rel=None):
    """
    *Plot size, resolution and margins*

    Parameters
    ----------
    width_mm : float
        Plot width in millimeters.
        Overrules ``width_in`` and ``width_pt``.
    width_in : float
        Plot width in inches.
        Overrules ``width_pt``.
    width_pt : float
        Plot width in points (1 in = 72 pt).

    height_mm : float
        Plot height in millimeters.
        Overrules ``height_in`` and ``height_pt``.
    height_in : float
        Plot height in inches.
        Overrules ``height_pt``.
    height_pt : float
        Plot height in points (1 in = 72 pt).

    dpi : int
        Dots per inch, used synonymously with pixels per inch (ppi).
        Example: Using width_in=2 and dpi=300 results in an image that is 600 pixels wide .
        Note that font size is specified in pt (=1/72 in). Therefore, using width_in=1
        and dpi=600 also results in an image that is 600 pixels wide but texts are twice as large.

    margin_auto : bool
        If True, all margins are set automatically by layout calculations of
        the plotting library.
        Caution: Other margin arguments are ignored in this case!

    margin_left_mm : float
        Left margin in millimeters.
        Overrules ``margin_left_in``, ``margin_left_pt`` and ``margin_left_rel``.
        Note: If margins are too low for any axis texts,
        then Plotly will modify the margins so the text can fit,
        while Matplotlib will not modify the margins so the text can be outside the image.
    margin_left_in : float
        Left margin in inches.
        Overrules ``margin_left_pt`` and ``margin_left_rel``.
    margin_left_pt : float
        Left margin in points (1 in = 72 pt).
        Overrules ``margin_left_rel``.
    margin_left_rel : float
        Left margin in percent, i.e. a relative measure.

    margin_right_mm : float
        right margin in millimeters.
        Overrules ``margin_right_in``, ``margin_right_pt`` and ``margin_right_rel``.
    margin_right_in : float
        right margin in inches.
        Overrules ``margin_right_pt`` and ``margin_right_rel``.
    margin_right_pt : float
        right margin in points (1 in = 72 pt).
        Overrules ``margin_right_rel``.
    margin_right_rel : float
        right margin in percent, i.e. a relative measure.

    margin_top_mm : float
        top margin in millimeters.
        Overrules ``margin_top_in``, ``margin_top_pt`` and ``margin_top_rel``.
    margin_top_in : float
        top margin in inches.
        Overrules ``margin_top_pt`` and ``margin_top_rel``.
    margin_top_pt : float
        top margin in points (1 in = 72 pt).
        Overrules ``margin_top_rel``.
    margin_top_rel : float
        top margin in percent, i.e. a relative measure.

    margin_bottom_mm : float
        bottom margin in millimeters.
        Overrules ``margin_bottom_in``, ``margin_bottom_pt`` and ``margin_bottom_rel``.
    margin_bottom_in : float
        bottom margin in inches.
        Overrules ``margin_bottom_pt`` and ``margin_bottom_rel``.
    margin_bottom_pt : float
        bottom margin in points (1 in = 72 pt).
        Overrules ``margin_bottom_rel``.
    margin_bottom_rel : float
        bottom margin in percent, i.e. a relative measure.


    """


def plot_color(plot_background_color=None, paper_background_color=None):
    """
    *Plot and paper color*

    Parameters
    ----------
    plot_background_color : str or tuple
        Background color of the main plot area.
        Possible values: See :ref:`colors`.
    paper_background_color : str or tuple
        Background color of the entire drawing area.
        Possible values: See :ref:`colors`.


    """


def plot_title(show_title=None, title=None, title_font=None, title_size=None, title_color=None,
               title_position=None):
    """
    *Plot title*

    Parameters
    ----------
    show_title : bool
        Show or hide the plot title.
    title : str
        Text of the plot title.
    title_font : str
        Font of the plot title.
    title_size : int
        Size of the plot title.
    title_color : str or tuple
        Color of the plot title.
        Possible values: See :ref:`colors`.
    title_position : str
        Position of the plot title.
        Possible values: "left", "center", "right".


    """


def x_axis(show_x_axis=None, x_axis_color=None, x_axis_scale=None, x_axis_range=None,
           x_axis_offset=None,
           # Spine
           show_x_spine=None, x_spine_color=None,
           # Title
           show_x_title=None, x_title=None, x_title_font=None, x_title_size=None,
           x_title_color=None, x_title_offset=None,
           # Ticks
           show_x_tick=None, x_tick_color=None, x_tick_position=None, x_tick_direction=None,
           x_tick_length=None, x_tick_width=None,
           # Labels
           show_x_label=True, x_label=None, x_label_font=None, x_label_size=None,
           x_label_color=None, x_label_offset=None, x_label_rotation=None):
    """
    *x axis*

    Parameters
    ----------
    show_x_axis : bool
        Show or hide the x-Axis (=title, spine, ticks and labels).
        Overrules ``show_x_title``, ``show_x_spine``, ``show_x_tick``, ``show_x_label``.
    x_axis_color : str or tuple
        Color of the x-Axis (=title, spine, ticks and labels).
        Overrules ``x_title_color``, ``x_spine_color``, ``x_tick_color``, ``x_label_color``.
        Possible values: See :ref:`colors`.
    x_axis_scale : str
        Scale of the x-Axis.
        Possible values: "lin", "linear", "log", "logarithmic", "cat", "categorical".
        Logarithmic scale is currently not available for 3D plots in Matplotlib.
    x_axis_range : list
        Start and stop value of the x-Axis.
        Requires a list of two numbers where the first is smaller than the second.
    x_axis_offset : float
        Offset for the drawing position of the x-Axis (directed away from the plot).
        Currently not available for Plotly.

    show_x_spine : bool
        Show or hide x-Axis spine.
    x_spine_color : str or tuple
        Color of x-Axis spine.
        Possible values: See :ref:`colors`.

    show_x_title : bool
        Show or hide the x-Axis title.
    x_title : str
        Text of the x-Axis title.
    x_title_font : str
        Font of the x-Axis title.
    x_title_size : float
        Size of the x-Axis title.
    x_title_color : str or tuple
        Color of the x-Axis title.
        Possible values: See :ref:`colors`.
    x_title_offset : float
        Offset for the drawing position of the x-Axis title (directed away from the plot).
        Currently not available for Plotly.

    show_x_tick : bool
        Show or hide x-Axis ticks.
    x_tick_color : str
        Color of the x-Axis ticks.
        Possible values: See :ref:`colors`.
    x_tick_position : list of float
        Positions where x-Axis ticks are places on the spine.
        Currently also determines positions of grid lines.
        Currently not available for Plotly when using a logarithmic axis scale.
    x_tick_direction : str
        Drawing direction of the x-Axis ticks.
        Possible values: "in", "out".
        Currently "in" is not available for 3D plots in Plotly.
    x_tick_length : float
        Length of the x-Axis ticks.
    x_tick_width : float
        Width of the x-Axis ticks.

    show_x_label : bool
        Show or hide x-Axis labels.
    x_label : list
        List of x-Axis labels.
    x_label_font : str
        Font of the x-Axis labels.
    x_label_size : float
        Size of the x-Axis labels.
    x_label_color : str
        Color of the x-Axis labels.
        Possible values: See :ref:`colors`.
    x_label_offset : float
        Offset for the drawing position of the x-Axis labels (directed away from the plot).
        Currently not available for Plotly.
    x_label_rotation : float
        Counter-clockwise rotation of the x-Axis labels in degree (e.g. 30).


    """
    # TODO: tick start/end/step or explicit values
    # TODO: translate axis range (logarithmic to log) for matplotlib
    # TODO: x_tick_direction correct unified values (in and out?)


def y_axis(show_y_axis=None, y_axis_color=None, y_axis_scale=None, y_axis_range=None,
           y_axis_offset=None,
           # Spine
           show_y_spine=None, y_spine_color=None,
           # Title
           show_y_title=None, y_title=None, y_title_font=None, y_title_size=None,
           y_title_color=None, y_title_offset=None,
           # Ticks
           show_y_tick=None, y_tick_color=None, y_tick_position=None, y_tick_direction=None,
           y_tick_length=None, y_tick_width=None,
           # Labels
           show_y_label=True, y_label=None, y_label_font=None, y_label_size=None,
           y_label_color=None, y_label_offset=None, y_label_rotation=None):
    """
    *y axis*

    Parameters
    ----------
    show_y_axis : bool
        Show or hide the y-Axis (=title, spine, ticks and labels).
        Overrules show_y_title, show_y_spine, show_y_tick, show_y_label.
    y_axis_color : str or tuple
        Color of the y-Axis (=title, spine, ticks and labels).
        Overrules y_title_color, y_spine_color, y_tick_color, y_label_color.
        Possible values: See :ref:`colors`.
    y_axis_scale : str
        Scale of the y-Axis.
        Possible values: "lin", "linear", "log", "logarithmic", "cat", "categorical".
        Logarithmic scale is currently not available for 3D plots in Matplotlib.
    y_axis_range : list
        Start and stop value of the y-Axis.
        Requires a list of two numbers where the first is smaller than the second.
    y_axis_offset : float
        Offset for the drawing position of the y-Axis (directed away from the plot).
        Currently not available for Plotly.

    show_y_spine : bool
        Show or hide y-Axis spine.
    y_spine_color : str or tuple
        Color of y-Axis spine.
        Possible values: See :ref:`colors`.

    show_y_title : bool
        Show or hide the y-Axis title.
    y_title : str
        Text of the y-Axis title.
    y_title_font : str
        Font of the y-Axis title.
    y_title_size : float
        Size of the y-Axis title.
    y_title_color : str or tuple
        Color of the y-Axis title.
        Possible values: See :ref:`colors`.
    y_title_offset : float
        Offset for the drawing position of the y-Axis title (directed away from the plot).
        Currently not available for Plotly.

    show_y_tick : bool
        Show or hide y-Axis ticks.
    y_tick_color : str
        Color of the y-Axis ticks.
        Possible values: See :ref:`colors`.
    y_tick_position : list of float
        Positions where y-Axis ticks are places on the spine.
        Currently also determines positions of grid lines.
        Currently not available for Plotly when using a logarithmic axis scale.
    y_tick_direction : str
        Drawing direction of the y-Axis ticks.
        Possible values: "in", "out".
        Currently "in" is not available for 3D plots in Plotly.
    y_tick_length : float
        Length of the y-Axis ticks.
    y_tick_width : float
        Width of the y-Axis ticks.

    show_y_label : bool
        Show or hide y-Axis labels.
    y_label : list
        List of y-Axis labels.
    y_label_font : str
        Font of the y-Axis labels.
    y_label_size : float
        Size of the y-Axis labels.
    y_label_color : str
        Color of the y-Axis labels.
        Possible values: See :ref:`colors`.
    y_label_offset : float
        Offset for the drawing position of the y-Axis labels (directed away from the plot).
        Currently not available for Plotly.
    y_label_rotation : float
        Counter-clockwise rotation of the y-Axis labels in degree (e.g. 30).


    """


def z_axis(show_z_axis=None, z_axis_color=None, z_axis_scale=None, z_axis_range=None,
           z_axis_offset=None,
           # Spine
           show_z_spine=None, z_spine_color=None,
           # Title
           show_z_title=None, z_title=None, z_title_font=None, z_title_size=None,
           z_title_color=None, z_title_offset=None,
           # Ticks
           show_z_tick=None, z_tick_color=None, z_tick_position=None, z_tick_direction=None,
           z_tick_length=None, z_tick_width=None,
           # Labels
           show_z_label=True, z_label=None, z_label_font=None, z_label_size=None,
           z_label_color=None, z_label_offset=None, z_label_rotation=None):
    """
    *z axis*

    Parameters
    ----------
    show_z_axis : bool
        Show or hide the z-Axis (=title, spine, ticks and labels).
        Overrules show_z_title, show_z_spine, show_z_tick, show_z_label.
    z_axis_color : str or tuple
        Color of the z-Axis (=title, spine, ticks and labels).
        Overrules z_title_color, z_spine_color, z_tick_color, z_label_color.
        Possible values: See :ref:`colors`.
    z_axis_scale : str
        Scale of the z-Axis.
        Possible values: "lin", "linear", "log", "logarithmic", "cat", "categorical".
        Logarithmic scale is currently not available for 3D plots in Matplotlib.
    z_axis_range : list
        Start and stop value of the z-Axis.
        Requires a list of two numbers where the first is smaller than the second.
    z_axis_offset : float
        Offset for the drawing position of the z-Axis (directed away from the plot).
        Currently not available for Plotly.

    show_z_spine : bool
        Show or hide z-Axis spine (=main line, ticks are perpendicular).
    z_spine_color : str or tuple
        Color of z-Axis spine.

    show_z_title : bool
        Show or hide the z-Axis title.
    z_title : str
        Text of the z-Axis title.
    z_title_font : str
        Font of the z-Axis title.
    z_title_size : float
        Size of the z-Axis title.
    z_title_color : str or tuple
        Color of the z-Axis title.
        Possible values: See :ref:`colors`.
    z_title_offset : float
        Offset for the drawing position of the z-Axis title (directed away from the plot).
        Currently not available for Plotly.

    show_z_tick : bool
        Show or hide z-Axis ticks.
    z_tick_color : str
        Color of the z-Axis ticks.
        Possible values: See :ref:`colors`.
    z_tick_position : list of float
        Positions where z-Axis ticks are places on the spine.
        Currently also determines positions of grid lines.
        Currently not available for Plotly when using a logarithmic axis scale.
    z_tick_direction : str
        Drawing direction of the z-Axis ticks.
        Possible values: "in", "out".
        Currently "in" is not available for 3D plots in Plotly.
    z_tick_length : float
        Length of the z-Axis ticks.
    z_tick_width : float
        Width of the z-Axis ticks.

    show_z_label : bool
        Show or hide z-Axis labels.
    z_label : list
        List of z-Axis labels.
    z_label_font : str
        Font of the z-Axis labels.
    z_label_size : float
        Size of the z-Axis labels.
    z_label_color : str
        Color of the z-Axis labels.
        Possible values: See :ref:`colors`.
    z_label_offset : float
        Offset for the drawing position of the z-Axis labels (directed away from the plot).
        Currently not available for Plotly.
    z_label_rotation : float
        Counter-clockwise rotation of the z-Axis labels in degree (e.g. 30).


    """


def x_error(x_error_left=None, x_error_right=None,
            show_x_error_bar=None,
            x_error_bar_color=None, x_error_bar_line_width=None, x_error_bar_size=None):
    """
    *x errors*

    Parameters
    ----------
    x_error_left : list or list of lists
        A list of numbers or a list of multiple such lists.
        It needs to have the same number of items as ``x``.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
    x_error_right : list or list of lists
        A list of numbers or a list of multiple such lists.
        It needs to have the same number of items as ``x``.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
    show_x_error_bar : bool
        Show or hide x error bars.
    x_error_bar_color : str or tuple
        Color of x error bars.
        Possible values: See :ref:`colors`.
    x_error_bar_line_width : float
        Width of x error bar lines.
    x_error_bar_size : float
        Size of x error bars.


    """


def y_error(y_error_top=None, y_error_bottom=None,
            show_y_error_bar=None,
            y_error_bar_color=None, y_error_bar_line_width=None, y_error_bar_size=None,
            show_y_error_band=None, y_error_band_color=None, y_error_band_opacity=None):
    """
    *y errors*

    Parameters
    ----------
    y_error_top : list or list of lists
        A list of numbers or a list of multiple such lists.
        It needs to have the same number of items as ``y``.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
    y_error_bottom : list or list of lists
        A list of numbers or a list of multiple such lists.
        It needs to have the same number of items as ``y``.
        If the values are numerical, all non-finite entries (NaN, +Inf, -Inf) will
        be removed automatically and a warning will be shown.
    show_y_error_bar : bool
        Show or hide y error bars.
    y_error_bar_color : str or tuple
        Color of y error bars.
        Possible values: See :ref:`colors`.
    y_error_bar_line_width : float
        Width of y error bar lines.
    y_error_bar_size : float
        Size of y error bars.
    show_y_error_band : bool
        Show or hide y error bands.
    y_error_band_color : str or tuple
        Color of y error bands.
        Possible values: See :ref:`colors`.
    y_error_band_opacity : float
        Opacity of y error bands.


    """


def x_grid(show_x_grid=None, x_grid_color=None, x_grid_width=None, x_grid_style=None):
    """
    *x grid*

    Parameters
    ----------
    show_x_grid : bool
        Show or hide the x-Grid.
    x_grid_color : str or tuple
        Color of the x-Grid.
        Possible values: See :ref:`colors`.
    x_grid_width : float
        Width of the x-Grid lines.
    x_grid_style : str
        Style of the x-Grid lines.
        Possible values: See :ref:`line-styles`.
        Currently not available for Plotly.


    """
    # TODO: grid positions - make them independent from tick positions?


def y_grid(show_y_grid=None, y_grid_color=None, y_grid_width=None, y_grid_style=None):
    """
    *y grid*

    Parameters
    ----------
    show_y_grid : bool
        Show or hide the y-Grid.
    y_grid_color : str or tuple
        Color of the y-Grid.
        Possible values: See :ref:`colors`.
    y_grid_width : float
        Width of the y-Grid lines.
    y_grid_style : str
        Style of the y-Grid lines.
        Possible values: See :ref:`line-styles`.
        Currently not available for Plotly.


    """


def z_grid(show_z_grid=None, z_grid_color=None, z_grid_width=None, z_grid_style=None):
    """
    *z grid*

    Parameters
    ----------
    show_z_grid : bool
        Show or hide the z-Grid.
    z_grid_color : str or tuple
        Color of the z-Grid.
        Possible values: See :ref:`colors`.
    z_grid_width : float
        Width of the z-Grid lines.
    z_grid_style : str
        Style of the z-Grid lines.
        Possible values: See :ref:`line-styles`.
        Currently not available for Plotly.


    """


def legend(show_legend=None, legend_title=None, legend_color=None, legend_size=None,
           legend_font=None, legend_background_color=None,
           legend_position_horizontal=None, legend_position_vertical=None,
           legend_marker_size=None, legend_border_size=None, legend_border_color=None):
    """
    *Legend*

    Parameters
    ----------
    show_legend : bool
        Show or hide the legend.
    legend_title : str
        Optional title for the legend.
    legend_color : str
        Font color of the legend text.
    legend_size : float
        Font size (in pt) of the legend text.
    legend_font : float
        Font family of the legend text.
    legend_background_color : str
        Color of the legend box background behind the legend text.
    legend_position_horizontal = str
        Horizontal positioning of the legend. Possible values: "left", "center", "right"
    legend_position_vertical = str
        Horizontal positioning of the legend. Possible values: "top", "center", "bottom"
    legend_marker_size : float
        Size (in pt) of the marker that represents a data series.
        This is currently not available in Plotly.
    legend_border_size : float
        Size (in pt) of the border around the legend box.
    legend_border_color : str
        Color of the border around the legend box.


    """


def colormap(show_colormap=None, colormap=None, colormap_reversed=None,
             colormap_label_font=None, colormap_label_size=None, colormap_label_color=None,
             colormap_border_size=None):
    """
    *Colormap*

    Parameters
    ----------
    show_colormap : bool
        Show or hide the colormap in form of a colorbar.
        Currently not supported for some plot types.
    colormap : str
        Colormap.
        Possible values: See :ref:`colormaps`.
    colormap_reversed : bool
        If True, the colormap is reversed.
        Currently not available for Matplotlib.
    colormap_label_font : str
        Font of the colormap labels.
    colormap_label_size : float
        Size of the colormap labels.
    colormap_label_color : str
        Color of the colormap labels.
    colormap_border_size : float
        Size (in pt) of the border around the legend box.


    """
    # TODO: long list or short reference to possible values
    # TODO: start and end value for covered range (plotly: cmin, cmax)


def markers(show_marker=None, marker_color=None, marker_colormap=None, marker_size=None,
            marker_style=None, marker_opacity=None):
    """
    *Markers*

    Parameters
    ----------
    show_marker : bool
        Show or hide marker symbols for data points.
    marker_color : str, tuple or list
        Color of markers.
        Overrules ``color``.
        Possible values: A single color (str or tuple), a list of colors,
        a list of numbers (uses colormap), a list of lists.
        See :ref:`colors`.
    marker_colormap : str
        Colormap for markers.
        Overrules ``colormap``.
        Used only if ``marker_color`` is a list of numbers.
        Possible values: See :ref:`colormaps`.
    marker_size : float
        Size (in pt) of markers.
    marker_style : str
        Style of markers.
        Possible values: See :ref:`marker-styles`.
    marker_opacity : float
        Opacity of markers.
        Overrules ``opacity``.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).


    """
    # TODO: provide marker style possible values
    # TODO: marker_colormap reverse option that overrules the general one


def lines(show_line=None, line_color=None,
          line_width=None, line_style=None, line_opacity=None):
    """
    *Lines*

    Parameters
    ----------
    show_line : bool
        Show or hide lines for data points.
    line_color : str, tuple or list
        Color of lines.
        Overrules ``color``.
        Possible values: A color or a list of colors.
        (Numerical values together with a colormap are currently not possible.)
        See :ref:`colors`.
    line_width : float
        Width (in pt) of lines.
    line_style : str
        Style of lines.
        Possible values: See :ref:`line-styles`.
    line_opacity : float
        Opacity of lines.
        Overrules ``opacity``.
        Currently not available for some plots in Plotly (e.g. with contour lines).


    """
    # TODO: can following removed arguments be used somehow?
    # line_colormap=None,
    # line_colormap (str): Colormap for lines.
    #         Used only if line_color is a list of numbers.
    #         Overrules colormap (only for lines, not for markers, surface, etc.).


def rugs(show_rug=None, rug_color=None, rug_colormap=None, rug_size=None, rug_style=None,
         rug_opacity=None):
    """
    *Rugs*

    Parameters
    ----------
    show_rug : bool
        Show or hide rugs.
    rug_color : str
        Color of rugs.
        Possible values: See :ref:`colors`.
    rug_colormap : str
        Colormap for rugs.
        Used only if rug_color is a list of numbers.
        Overrules colormap (only for rugs, not for lines, surface, etc.).
    rug_size : float
        Size of rugs.
    rug_style : str
        Style of rugs.
        Possible values: See :ref:`marker-styles`.
    rug_opacity : float
        Opacity of rugs.


    """
    # TODO: Use them consistently at all places where rugs can appear (box, violin, density, ...)


def bins(bin_x_start=None, bin_x_stop=None, bin_x_number=None):
    """
    *Bins*

    Parameters
    ----------
    bin_x_number : int
        Number of bins along the x-Axis.
    bin_x_start : float
        Value on x-Axis that is used as start for first bin.
    bin_x_stop : float
        Value on x-Axis that is used as end for last bin.


    """


def bins_2d(bin_x_start=None, bin_x_stop=None, bin_x_number=None,
            bin_y_start=None, bin_y_stop=None, bin_y_number=None):
    """
    *Bins*

    Parameters
    ----------
    bin_x_number : int
        Number of bins along the x-Axis.
    bin_x_start : float
        Value on x-Axis that is used as start for first bin.
    bin_x_stop : float
        Value on x-Axis that is used as stop for last bin.
    bin_y_number : int
        Number of bins along the x-Axis.
    bin_y_start : float
        Value on x-Axis that is used as start for first bin.
    bin_y_stop : float
        Value on x-Axis that is used as stop for last bin.


    """


def contour_lines(show_line=None, line_color=None, line_width=None, line_style=None):
    """
    *Contour lines*

    Parameters
    ----------
    show_line : bool
        Show or hide contour lines.
    line_color : str or tuple
        Color of contour lines.
        Possible values: See :ref:`colors`.
    line_width : float
        Width of contour lines.
    line_style : str
        Style of contour lines.


    """


def external_fig_and_ax(fig=None, ax=None):
    """
    *Existing Matplotlib figure and axes*

    Parameters
    ----------
    fig
        A Matplotlib Figure object. Contains one or several Axes objects.
        If in doubt, look here: https://matplotlib.org/faq/usage_faq.html
    ax
        A Matplotlib Axes object to draw to. Done via the plotting methods it provides.
        The most common way to create both figure and axes is the subplots() function, see
        https://matplotlib.org/api/_as_gen/matplotlib.pyplot.subplots.html


    """


def external_fig_and_ax_3d(fig=None, ax=None):
    """
    *Existing Matplotlib figure and 3D axes*

    Parameters
    ----------
    fig
        A Matplotlib Figure object. Contains one or several Axes objects.
        If in doubt, look here: https://matplotlib.org/faq/usage_faq.html
    ax
        A Matplotlib 3D Axes object to draw to. Done via the plotting methods it provides.


    """


# Hack to get all functions in the order of their definition and list all their arguments
UNIFIED_ARGS = []
_THIS_MODULE = _sys.modules[__name__]
_SOURCE_CODE = _inspect.getsource(_THIS_MODULE)
for func_name in _re.compile(r'def\s(.+?)\(').findall(_SOURCE_CODE):
    func = getattr(_THIS_MODULE, func_name)
    argspec = _inspect.getfullargspec(func)
    args = argspec[0]
    UNIFIED_ARGS.extend(args)
UNIFIED_ARGS = list(_OrderedDict.fromkeys(UNIFIED_ARGS))

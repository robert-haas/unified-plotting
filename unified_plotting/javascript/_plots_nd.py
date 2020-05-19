"""JavaScript plots for n-dimensional vector data."""

from collections.abc import Iterable as _Iterable

from .._unified_arguments import colormaps as _colormaps
from .._unified_arguments import shared_preprocessing as _shared_preprocessing
from . import _data_structures, _template_system


def parallel_coordinates_table(data=None, name=None,
                               column_html=None, column_hidden=None, column_shown=None,
                               parallel_coordinates_height=250,
                               parallel_coordinates_width_factor=1.0,
                               table_height=200,
                               show_menu=True, show_menu_toggle_button=True,
                               line_width=1.4, opacity=0.3, smoothness=0.0, color=None,
                               colormap="Viridis", colormap_reversed=False,
                               background_color="white", axis_color="black", tick_color="black",
                               title_font="sans", title_size=10, title_color="black",
                               label_font="sans", label_size=10, label_color="black",
                               table_cell_width=50, table_cell_height=20):
    """Create a parallel coordinate plot with d3.parcoords.js and linked table with slick.grid.js.

    Parameters
    ----------
    data : list of lists, pandas DataFrame, or filepath of a CSV file
        A list of lists. Each list needs to have the same number of items. Each item can be a
        number or a string.
        If a list contains only numerical values and a non-finite item (NaN, +Inf, -Inf)
        is detected, the position of the entry will be removed from each list automatically
        and a warning will be shown.
    name : list
        Name(s) of the visualized data series. Used in the axis description of the parallel
        coordinates plot and headers of the table.
    column_html : list of str
        Name(s) of columns that shall be treated as HTML text in the table. This can e.g.
        be used to display images from some image URL in table cells.
    column_hidden : list of str
        Name(s) of columns that shall be hidden in the parallel coordinates plot, while all
        columns are shown in the table. This enables a negative selection useful when
        only a few of a lot of columns shall be hidden.
    column_shown : list of str
        Name(s) of columns that shall be shown in the parallel coordinates plot, while all
        columns are shown in the table. This enables a positive selection useful when
        only a few of a lot of columns shall be shown.
    parallel_coordinates_height : float
        Height of the parallel coordinates container in pixels (px).
    parallel_coordinates_width_factor : float
        Relative width of the parallel coordinates plot. For example, 2.0 means that the plot
        takes up 200% of the container width and a horizonta scroll bar appears.
    table_height : float
        Height of the table container in pixels (px).
    show_menu : bool
        If True, the menu container is shown on load, otherwise hidden.
    show_menu_toggle_button : bool
        If True, a button is shown that allows to toggle the visibility of the menu container.
    line_width : float
        Width of each line in the parallel coordinates plot in pixels (px).
    opacity : float
        Opacity of each line in the parallel coordinates plot.
    smoothness : float
        Smoothness value of each line in the parallel coordinates plot.
    color : str
        Name of the column that is used as data source for coloring lines in the parallel
        coordinate plot. It needs to be a shown column.
    colormap : str
        Name of the colormap that shall be used to convert numerical values into colors
        in the parallel coordinates plot.
        Possible values: A d3.js colormap: 'Blues', 'Greens', 'Greys', 'Oranges', 'Purples',
        'Reds', 'Turbo', 'Viridis', 'Inferno', 'Magma', 'Plasma', 'Cividis', 'Warm', 'Cool',
        'Cubehelix', 'BuGn', 'BuPu', 'GnBu', 'OrRd', 'PuBuGn', 'PuBu', 'PuRd', 'RdPu', 'YlGnBu',
        'YlGn', 'YlOrBr', 'YlOrRd', 'BrBG', 'PRGn', 'PiYG', 'PuOr', 'RdBu', 'RdGy', 'RdYlBu',
        'RdYlGn', 'Spectral', 'Rainbow', 'Sinebow'
    colormap_reversed : bool
        If True, the colormap is reversed.
    background_color : str
        Color of the background.
    axis_color : str
        Color of the axes.
    tick_color : str
        Color of the ticks.
    title_font : str
        Font of the axis titles.
    title_size : float
        Size of the axis titles.
    title_color : str
        Color of the axis titles.
    label_font : str
        Font of the axis labels.
    label_size : float
        Size of the axis labels.
    label_color : str
        Color of the axis labels.
    table_cell_width : float
        Width of a cell in the table in pixels (px).
    table_cell_height : float
        Height of a cell in the table in pixels (px).

    Returns
    -------
    A :ref:`Figure <js-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://github.com/BigFatDog/parcoords-es
    - https://slickgrid.net

    """
    # Shared argument processing
    data, name = _shared_preprocessing.prepare_vector_data_nd(
        data, name, remove_non_numerical_vectors=False)

    # Further argument processing
    name = _parse_names_for_table(name, num_names=len(data))
    data = _convert_data_for_table(data, name)
    column_full = ['id'] + name
    column_html = _check_column(column_html, default=[], allowed=column_full)
    column_hidden = _check_column(column_hidden, default=[], allowed=column_full)
    column_shown = _check_column(column_shown, default=name, allowed=column_full)
    column_finally_shown = [col for col in column_shown if col not in column_hidden]
    column_finally_hidden = [col for col in column_full if col not in column_finally_shown]
    if not column_finally_hidden:
        message = ('The number of columns selected to be shown in the parallel '
                   'coordinates plot is zero, which can not be done.')
        raise ValueError(message)
    if color is None:
        color = column_finally_shown[0]
    elif color not in column_shown:
        message = 'Value "{}" for color is invalid. Possible values: {}'.format(
            color, column_shown)
        raise ValueError(message)
    if not isinstance(colormap, str) or colormap.lower() not in _colormaps.D3_BUILTIN_COLORMAPS:
        message = (
            'Value "{}" for colormap is invalid. Possible values (d3 colormaps): '
            '{}'.format(colormap, sorted(_colormaps.D3_BUILTIN_COLORMAPS.values())))
        raise ValueError(message)
    colormap = _colormaps.D3_BUILTIN_COLORMAPS[colormap.lower()]

    # Transformation
    site_template = _template_system.load('templates/pc_table_parcoords_slickgrid.html')
    insert_data = {
        'DEFINE_D3_COLOR': _template_system.load(
            'third_party/d3-color/d3-color.v1.min.def.js'),
        'DEFINE_D3_INTERPOLATE': _template_system.load(
            'third_party/d3-interpolate/d3-interpolate.v1.min.def.js'),
        'DEFINE_D3_SCALE_CHROMATIC': _template_system.load(
            'third_party/d3-scale-chromatic/d3-scale-chromatic.v1.min.def.js'),
        'DEFINE_PARCOORDS': _template_system.load(
            'third_party/parcoords/parcoords.standalone.min.def.js'),
        'DEFINE_JQUERY': _template_system.load(
            'third_party/jquery/jquery.min.def.js'),
        'DEFINE_SLICKGRID': _template_system.load(
            'third_party/slickgrid/slickgrid.combined.def.js'),

        'DATA': _template_system.to_json(data),
        'COLUMN_NAME': _template_system.to_json(name),
        'COLUMN_HTML': _template_system.to_json(column_html),
        'COLUMN_HIDDEN': _template_system.to_json(column_finally_hidden),
        'COLUMN_SHOWN': _template_system.to_json(column_finally_shown),

        'PC_HEIGHT': _template_system.to_json(parallel_coordinates_height),
        'PC_WIDTH_FACTOR': _template_system.to_json(parallel_coordinates_width_factor),
        'TABLE_HEIGHT': _template_system.to_json(table_height),
        'SHOW_MENU': _template_system.to_json(show_menu),
        'SHOW_MENU_TOGGLE_BUTTON': _template_system.to_json(show_menu_toggle_button),

        'LINE_WIDTH': _template_system.to_json(line_width),
        'OPACITY': _template_system.to_json(opacity),
        'SMOOTHNESS': _template_system.to_json(smoothness),
        'COLOR_COLUMN': _template_system.to_json(color),
        'COLORMAP': _template_system.to_json(colormap),
        'COLORMAP_REVERSED': _template_system.to_json(colormap_reversed),
        'BACKGROUND_COLOR': _template_system.to_json(background_color),
        'AXIS_COLOR': _template_system.to_json(axis_color),
        'TICK_COLOR': _template_system.to_json(tick_color),
        'TITLE_FONT': _template_system.to_json(title_font),
        'TITLE_SIZE': _template_system.to_json(title_size),
        'TITLE_COLOR': _template_system.to_json(title_color),
        'LABEL_FONT': _template_system.to_json(label_font),
        'LABEL_SIZE': _template_system.to_json(label_size),
        'LABEL_COLOR': _template_system.to_json(label_color),

        'TABLE_CELL_WIDTH': _template_system.to_json(table_cell_width),
        'TABLE_CELL_HEIGHT': _template_system.to_json(table_cell_height),
    }
    site_template = _template_system.insert(site_template, insert_data)
    fig = _data_structures.Figure(site_template)
    return fig


def table(data=None, name=None, column_html=None,
          table_height=350, table_cell_width=50, table_cell_height=22,
          show_menu=True, show_menu_toggle_button=True):
    """Create an interactive table with slick.grid.js.

    Parameters
    ----------
    data : list of lists, pandas DataFrame, or filepath of a CSV file
        A list of lists. Each list needs to have the same number of items. Each item can be a
        number or a string.
        If a list contains only numerical values and a non-finite item (NaN, +Inf, -Inf)
        is detected, the position of the entry will be removed from each list automatically
        and a warning will be shown.
    name : list
        Name(s) of the visualized data series. Used in the axis description of the parallel
        coordinates plot and headers of the table.
    column_html : list of str
        Name(s) of columns that shall be treated as HTML text in the table. This can e.g.
        be used to display images from some image URL in table cells.
    table_height : float
        Height of the table container in pixels (px).
    table_cell_width : float
        Width of a cell in the table in pixels (px).
    table_cell_height : float
        Height of a cell in the table in pixels (px).
    show_menu : bool
        If True, the menu container is shown on load, otherwise hidden.
    show_menu_toggle_button : bool
        If True, a button is shown that allows to toggle the visibility of the menu container.

    Returns
    -------
    A :ref:`Figure <js-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://slickgrid.net

    """
    # Shared argument processing
    data, name = _shared_preprocessing.prepare_vector_data_nd(
        data, name, remove_non_numerical_vectors=False)

    # Further argument processing
    name = _parse_names_for_table(name, num_names=len(data))
    data = _convert_data_for_table(data, name)
    column_full = ['id'] + name
    column_html = _check_column(column_html, default=[], allowed=column_full)

    # Transformation
    site_template = _template_system.load('templates/table_slickgrid.html')
    insert_data = {
        'DEFINE_JQUERY': _template_system.load(
            'third_party/jquery/jquery.min.def.js'),
        'DEFINE_SLICKGRID': _template_system.load(
            'third_party/slickgrid/slickgrid.combined.def.js'),
        'DATA': _template_system.to_json(data),
        'COLUMN_NAME': _template_system.to_json(name),
        'COLUMN_HTML': _template_system.to_json(column_html),
        'TABLE_HEIGHT': _template_system.to_json(table_height),
        'TABLE_CELL_WIDTH': _template_system.to_json(table_cell_width),
        'TABLE_CELL_HEIGHT': _template_system.to_json(table_cell_height),
        'SHOW_MENU': _template_system.to_json(show_menu),
        'SHOW_MENU_TOGGLE_BUTTON': _template_system.to_json(show_menu_toggle_button),
    }

    site_template = _template_system.insert(site_template, insert_data)
    fig = _data_structures.Figure(site_template)
    return fig


def _parse_names_for_table(names, num_names):
    used_names = []
    forbidden_names = ['id', 'checkbox']
    for i in range(num_names):
        try:
            name = str(names[i])
        except Exception:
            name = 'Column {}'.format(i+1)
        while name in forbidden_names or name in used_names:
            name = '_' + name
        used_names.append(name)
    return used_names


def _convert_data_for_table(data, names):
    num_rows = len(data[0])
    new_data = []
    for row_id in range(num_rows):
        row_dict = {
            'id': row_id,
            'checkbox': 0,
        }
        for col_id, col in enumerate(names):
            row_dict[col] = data[col_id][row_id]
        new_data.append(row_dict)
    return new_data


def _check_column(column_list, default, allowed):
    if column_list is None:
        column_list = default
    elif not isinstance(column_list, _Iterable) or isinstance(column_list, str):
        column_list = [column_list]
    for col in column_list:
        if col not in allowed:
            message = 'Given column "{}" is not part of known columns: {}'.format(col, allowed)
            raise ValueError(message)
    return column_list

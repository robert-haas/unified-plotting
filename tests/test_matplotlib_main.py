import os

import pytest

import unified_plotting as up
from shared_data_loading import (ALL_COLORMAPS, INTERPOLATION_METHODS, LINE_STYLES, MARKER_STYLES,
                                 TEST_COLORS, TESTDATA, TESTDATA_GRID, TESTDATA_SMALL)
from shared_testing import try_all_legend_parameters, try_unknown_argument


# Common preliminaries

def create_output_filepath(my_outdir, name):
    return os.path.join(my_outdir, 'matplotlib_' + name)


def export_all_available_formats(fig, filepath):
    fig.export_html(filepath)
    fig.export_png(filepath)
    fig.export_eps(filepath)
    fig.export_pdf(filepath)
    fig.export_pgf(filepath)
    fig.export_ps(filepath)
    fig.export_svg(filepath)


# Tests with pytest

# 2d plots

@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_hexbin_export(my_outdir, name, x, y, z):
    fig = up.matplotlib.hexbin(x, y)
    filepath = create_output_filepath(my_outdir, 'hexbin_' + name)
    export_all_available_formats(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_hexbin_parameters(name, x, y, z):
    # default
    up.matplotlib.hexbin(x, y)

    # opacity
    up.matplotlib.hexbin(x, y, opacity=0.2)

    # bins
    up.matplotlib.hexbin(x, y, bin_x_number=5, bin_x_stop=+2, bin_y_number=5, bin_y_start=1)


def test_hexbin_unknown_arg(caplog):
    try_unknown_argument(caplog, up.matplotlib.hexbin, dict(x=[1, 2, 3], y=[1, 2, 3]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_histogram_2d_export(my_outdir, name, x, y, z):
    fig = up.matplotlib.histogram_2d(x, y)
    filepath = create_output_filepath(my_outdir, 'histogram_2d_' + name)
    export_all_available_formats(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_histogram_2d_parameters(name, x, y, z):
    # default
    up.matplotlib.histogram_2d(x, y)

    # opacity
    up.matplotlib.histogram_2d(x, y, opacity=0.2)

    # bins
    up.matplotlib.histogram_2d(
        x, y, bin_x_number=5, bin_x_stop=+2, bin_y_number=5, bin_y_start=1)


def test_histogram_2d_unknown_arg(caplog):
    try_unknown_argument(caplog, up.matplotlib.histogram_2d, dict(x=[1, 2, 3], y=[1, 2, 3]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_scatter_export(my_outdir, name, x, y, z):
    fig = up.matplotlib.scatter(x, y)
    filepath = create_output_filepath(my_outdir, 'scatter_' + name)
    export_all_available_formats(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_scatter_parameters(name, x, y, z):
    # default
    up.matplotlib.scatter(x, y)
    up.matplotlib.scatter([x, x], [y, z])
    up.matplotlib.scatter(x=x, y=y)
    up.matplotlib.scatter(x=[x, x], y=[y, z])

    with pytest.raises(ValueError):
        up.matplotlib.scatter(x, y+[42])
    with pytest.raises(ValueError):
        up.matplotlib.scatter(x+[42], y)
    with pytest.raises(ValueError):
        up.matplotlib.scatter(x=[x, x], y=[y, z+[42]])
    with pytest.raises(ValueError):
        up.matplotlib.scatter(x=[x, x+[42]], y=[y, z])

    # name
    up.matplotlib.scatter(x, y, name=[], show_legend=True)
    up.matplotlib.scatter(x, y, name=['y'])
    up.matplotlib.scatter(x, y, name=['y', 'too much'])
    up.matplotlib.scatter([x, x, x], [y, y, y], name=[])
    up.matplotlib.scatter([x, x, x], [y, y, y], name=['a', 'too little'])
    up.matplotlib.scatter([x, x, x], [y, y, y], name=[1, 2, 3])
    up.matplotlib.scatter([x, x, x], [y, y, y], name=['a', 'b', 'c', 'too much'])

    # color
    for color in TEST_COLORS:
        up.matplotlib.scatter(x, y, color=color)
        up.matplotlib.scatter([x, x], [y, y], color=[color, color])
    up.matplotlib.scatter(x, y, color=x)
    up.matplotlib.scatter([x, x, x], [y, y, y], color=[x, y, x])
    up.matplotlib.scatter([x, x, x], [y, y, y], color=[x, 'blue'])
    up.matplotlib.scatter([x, x, x], [y, y, y], color=[x, 'blue', (0, 10, 0)])
    up.matplotlib.scatter([x, x, x], [y, y, y], color=[x, 'blue', (0, 10, 0), y])

    # opacity
    up.matplotlib.scatter(x, y, opacity=0.5)
    up.matplotlib.scatter([x, x, x], [y, y, y], opacity=0.5)
    up.matplotlib.scatter([x, x, x], [y, y, y], opacity=[0.1, 1.0])
    up.matplotlib.scatter([x, x, x], [y, y, y], opacity=[0.1, 1.0, 0.5])
    up.matplotlib.scatter([x, x, x], [y, y, y], opacity=[0.1, 1.0, 0.5, 0.8])

    # marker and line
    up.matplotlib.scatter(x, y, show_marker=False, show_line=False)

    up.matplotlib.scatter(x, y, marker_color=x, marker_colormap='viridis')
    up.matplotlib.scatter(x, y, color=x, marker_colormap='viridis')
    up.matplotlib.scatter(x, y, marker_color=x, colormap='viridis')

    up.matplotlib.scatter(x, y, marker_size=10, marker_style='s', marker_opacity=0.2)
    up.matplotlib.scatter([x, x, x], [y, y, y], marker_size=[1, 2], marker_style=['s', '*'],
                          marker_opacity=[0.1, 0.2])

    for marker_style in MARKER_STYLES:
        up.matplotlib.scatter(x, y, marker_style=marker_style)

    up.matplotlib.scatter(x, y, show_line=True, line_color='red', line_width=5, line_style='--')
    up.matplotlib.scatter(x, y, show_line=True, line_color=x, line_width=0.1, line_style='.')
    up.matplotlib.scatter([x, x, x], [y, y, y], show_line=True, line_color=[x, y],
                          line_width=[0.1, 0.5], line_style=['.', '-'])

    for line_style in LINE_STYLES:
        up.matplotlib.scatter(x, y, show_line=True, line_style=line_style)


@pytest.mark.parametrize('kwargs', [
    dict(),
    dict(x_axis_scale='cat'),
    dict(x_axis_scale='log'),
    dict(y_axis_scale='cat'),
    dict(y_axis_scale='log'),
    dict(x_axis_scale='cat'), dict(y_axis_scale='cat'),
    dict(x_axis_scale='log'), dict(y_axis_scale='log'),
])
def test_scatter_error_bars(kwargs):
    # Single series, single x error, single y error
    up.matplotlib.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_left=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_top=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        **kwargs,
    )
    up.matplotlib.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_left=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_bottom=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        **kwargs,
    )
    up.matplotlib.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_right=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_top=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        **kwargs,
    )
    up.matplotlib.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_right=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_bottom=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        **kwargs,
    )
    # Single series, single x error, dual y error
    up.matplotlib.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_left=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_bottom=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        y_error_top=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        **kwargs,
    )
    up.matplotlib.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_right=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_bottom=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        y_error_top=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        **kwargs,
    )
    # Single series, dual x error, single y error
    up.matplotlib.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_left=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        x_error_right=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_bottom=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        **kwargs,
    )
    up.matplotlib.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_left=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        x_error_right=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_top=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        **kwargs,
    )
    # Single series, dual x error, dual y error
    up.matplotlib.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_left=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        x_error_right=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_top=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        y_error_bottom=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        **kwargs,
    )
    # Multiple series, single x error, single y error
    up.matplotlib.scatter(
        x=[[1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7]],
        y=[[2, 3, 4, 5, 6, 7, 8], [4, 5, 6, 7, 8, 9, 10]],
        x_error_left=[[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]],
        y_error_bottom=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]],
        **kwargs,
    )
    # Multiple series, dual x error, dual y error
    up.matplotlib.scatter(
        x=[[1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7]],
        y=[[2, 3, 4, 5, 6, 7, 8], [4, 5, 6, 7, 8, 9, 10]],
        x_error_left=[[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]],
        x_error_right=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]],
        y_error_top=[[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]],
        y_error_bottom=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]],
        **kwargs,
    )
    # Single series, single spec
    up.matplotlib.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_left=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_bottom=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        show_x_error_bar=True,
        show_y_error_bar=True,
        show_y_error_band=True,
        x_error_bar_color=(0, 1, 0),
        x_error_bar_line_width=2,
        x_error_bar_size=10,
        y_error_bar_color='rgba(0, 0, 1, 0.3)',
        y_error_bar_line_width=2,
        y_error_bar_size=10,
        y_error_band_color='xkcd.vomit_green',
        y_error_band_opacity=0.1,
        **kwargs,
    )
    # Single series, multiple spec
    up.matplotlib.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_left=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_bottom=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        show_x_error_bar=[True, False],
        show_y_error_bar=[False, True],
        show_y_error_band=[True, False],
        x_error_bar_color=[(0, 1, 0), 'gray'],
        x_error_bar_line_width=[2, 4],
        x_error_bar_size=[10, 20],
        y_error_bar_color=['rgba(0, 0, 1, 0.3)', 'rgb(0, 0, 213)'],
        y_error_bar_line_width=[2, 4],
        y_error_bar_size=[20, 10],
        y_error_band_color=['xkcd.vomit_green', (255, 0, 0)],
        y_error_band_opacity=[0.1, 1.3],
        **kwargs,
    )
    # Multiple series, single spec
    up.matplotlib.scatter(
        x=[[1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7]],
        y=[[2, 3, 4, 5, 6, 7, 8], [4, 5, 6, 7, 8, 9, 10]],
        x_error_left=[[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]],
        x_error_right=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]],
        y_error_top=[[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]],
        y_error_bottom=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]],
        show_x_error_bar=True,
        show_y_error_bar=True,
        show_y_error_band=True,
        x_error_bar_color=(0, 1, 0),
        x_error_bar_line_width=2,
        x_error_bar_size=10,
        y_error_bar_color='rgba(0, 0, 1, 0.3)',
        y_error_bar_line_width=2,
        y_error_bar_size=10,
        y_error_band_color='xkcd.vomit_green',
        y_error_band_opacity=0.1,
        **kwargs,
    )
    # Multiple series, multiple spec
    up.matplotlib.scatter(
        x=[[1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7]],
        y=[[2, 3, 4, 5, 6, 7, 8], [4, 5, 6, 7, 8, 9, 10]],
        x_error_left=[[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]],
        x_error_right=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]],
        y_error_top=[[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]],
        y_error_bottom=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]],
        show_x_error_bar=[True, False],
        show_y_error_bar=[False, True],
        show_y_error_band=[True, False],
        x_error_bar_color=[(0, 1, 0), 'gray'],
        x_error_bar_line_width=[2, 4],
        x_error_bar_size=[10, 20],
        y_error_bar_color=['rgba(0, 0, 1, 0.3)', 'rgb(0, 0, 213)'],
        y_error_bar_line_width=[2, 4],
        y_error_bar_size=[20, 10],
        y_error_band_color=['xkcd.vomit_green', (255, 0, 0)],
        y_error_band_opacity=[0.1, 1.3],
        **kwargs,
    )
    up.matplotlib.scatter(
        x=[[1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7]],
        y=[[2, 3, 4, 5, 6, 7, 8], [4, 5, 6, 7, 8, 9, 10]],
        x_error_left=[[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]],
        x_error_right=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]],
        y_error_top=[[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]],
        y_error_bottom=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]],
        show_x_error_bar=[True, True],
        show_y_error_bar=[True, True],
        show_y_error_band=[True, True],
        x_error_bar_color=[(0, 1, 0), 'gray'],
        x_error_bar_line_width=[2, 4],
        x_error_bar_size=[10, 20],
        y_error_bar_color=['rgba(0, 0, 1, 0.3)', 'rgb(0, 0, 213)'],
        y_error_bar_line_width=[2, 4],
        y_error_bar_size=[20, 10],
        y_error_band_color=['xkcd.vomit_green', (255, 0, 0)],
        y_error_band_opacity=[0.1, 1.3],
        **kwargs,
    )


def test_scatter_legend_parameters():
    data = dict(x=list(range(20)), y=list(range(20)))
    try_all_legend_parameters(up.matplotlib.scatter, data)


def test_scatter_unknown_arg(caplog):
    try_unknown_argument(caplog, up.matplotlib.scatter, dict(x=[1, 2, 3], y=[1, 2, 3]))


# 3d plots

@pytest.mark.parametrize('name, x, y, z', TESTDATA_GRID)
def test_contour_export(my_outdir, name, x, y, z):
    fig = up.matplotlib.contour(x, y, z, x_axis_scale='cat', y_axis_scale='categorical')
    filepath = create_output_filepath(my_outdir, 'contour_' + name)
    export_all_available_formats(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_GRID)
def test_contour_parameters(name, x, y, z):
    # default
    up.matplotlib.contour(x, y, z, x_axis_scale='categorical', y_axis_scale='cat')

    # opacity
    up.matplotlib.contour(x, y, z, opacity=0.5, x_axis_scale='categorical', y_axis_scale='cat')

    # interpolation_method and interpolation_selection
    for method in INTERPOLATION_METHODS:
        for selection in [None, 'min', 'max']:
            if method not in ['spline_cubic', 'spline_quintic']:  # fail under many conditions
                up.matplotlib.contour(
                    x, y, z, x_axis_scale='cat', y_axis_scale='cat',
                    interpolation_method=method, interpolation_selection=selection)

    # interpolation_num_x_gridpoints
    up.matplotlib.contour(
        x, y, z, x_axis_scale='cat', y_axis_scale='cat', interpolation_num_x_gridpoints=50)

    # interpolation_num_y_gridpoints
    up.matplotlib.contour(
        x, y, z, x_axis_scale='cat', y_axis_scale='cat', interpolation_num_y_gridpoints=50)

    # colormaps
    for cmap in ALL_COLORMAPS[0:len(ALL_COLORMAPS):len(ALL_COLORMAPS)//15]:
        up.matplotlib.contour(
            x, y, z, x_axis_scale='cat', y_axis_scale='cat',
            colormap=cmap, colormap_reversed=True,
            colormap_label_size=20, colormap_label_color='red', colormap_label_font='serif')


def test_contour_unknown_arg(caplog):
    try_unknown_argument(
        caplog, up.matplotlib.contour, dict(x=[1, 2, 3], y=[1, 2, 3], z=[1, 2, 3]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_scatter_3d_export(my_outdir, name, x, y, z):
    fig = up.matplotlib.scatter_3d(x, y, z)
    filepath = create_output_filepath(my_outdir, 'scatter_3d_' + name)
    export_all_available_formats(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_scatter_3d_parameters(name, x, y, z):
    # default
    up.matplotlib.scatter_3d(x, y, z)
    up.matplotlib.scatter_3d([x, x], [y, y], [z, z])
    with pytest.raises(ValueError):
        up.matplotlib.scatter_3d(x, y+[42], z)
    with pytest.raises(ValueError):
        up.matplotlib.scatter_3d(x+[42], y, z)
    with pytest.raises(ValueError):
        up.matplotlib.scatter_3d(x=[x, x], y=[y, y+[42]], z=[z, z])
    with pytest.raises(ValueError):
        up.matplotlib.scatter_3d(x=[x, x+[42]], y=[y, y], z=[z, z])

    # name
    up.matplotlib.scatter_3d(x, y, z, name=['1'])
    up.matplotlib.scatter_3d(x, y, z, name=['1', '2', '3'])
    up.matplotlib.scatter_3d([x, x], [y, y], [z, z], name=['1'])
    up.matplotlib.scatter_3d([x, x], [y, y], [z, z], name=['1', '2', '3'])

    # color
    for color in TEST_COLORS + [x]:
        up.matplotlib.scatter_3d(x, y, z, color=color)
        up.matplotlib.scatter_3d(x, y, z, color=[color, 'red', color])
        up.matplotlib.scatter_3d([x, x], [y, y], [z, z], color=color)
        up.matplotlib.scatter_3d([x, x], [y, y], [z, z], color=[color, 'red', color])

    # opacity
    up.matplotlib.scatter_3d(x, y, z, opacity=0.5)
    up.matplotlib.scatter_3d(x, y, z, opacity=[0.1, 0.8])
    up.matplotlib.scatter_3d([x, x], [y, y], [z, z], opacity=0.5)
    up.matplotlib.scatter_3d([x, x], [y, y], [z, z], opacity=[0.1, 0.8])

    # lines
    up.matplotlib.scatter_3d(x, y, z, show_line=True, line_color='red', line_width=2)

    # grid
    up.matplotlib.scatter_3d(x, y, z, show_x_grid=True)
    up.matplotlib.scatter_3d(x, y, z, show_y_grid=True)
    up.matplotlib.scatter_3d(x, y, z, show_z_grid=True)
    up.matplotlib.scatter_3d(x, y, z, show_x_grid=True, show_y_grid=True)
    up.matplotlib.scatter_3d(x, y, z, show_x_grid=True, show_z_grid=True)
    up.matplotlib.scatter_3d(x, y, z, show_y_grid=True, show_z_grid=True)
    up.matplotlib.scatter_3d(x, y, z, show_x_grid=True, show_y_grid=True, show_z_grid=True)

    # camera angle
    up.matplotlib.scatter_3d(x, y, z, camera_angle_vertical=20)
    up.matplotlib.scatter_3d(x, y, z, camera_angle_horizontal=-45)
    up.matplotlib.scatter_3d(x, y, z, camera_angle_vertical=20, camera_angle_horizontal=-45)


def test_scatter_3d_legend_parameters():
    series = list(range(20))
    data = dict(x=series, y=series, z=series)
    try_all_legend_parameters(up.matplotlib.scatter_3d, data)


def test_scatter_3d_unknown_arg(caplog):
    try_unknown_argument(
        caplog, up.matplotlib.scatter_3d, dict(x=[1, 2, 3], y=[1, 2, 3], z=[1, 2, 3]))


# Nd plots

@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_box_export(my_outdir, name, x, y, z):
    fig = up.matplotlib.box([x, y, z])
    filepath = create_output_filepath(my_outdir, 'box_' + name)
    export_all_available_formats(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_box_parameters(name, x, y, z):
    # default
    up.matplotlib.box([x, y, z])

    # name
    up.matplotlib.box([x, y, z], name=['a', 'b'])

    # color
    for color in TEST_COLORS:
        up.matplotlib.box([x, y, z], color=color)
        up.matplotlib.box([x, y, z], color=[color, 'red', color, 'blue'])

    # opacity
    up.matplotlib.box([x, y, z], opacity=0.5)

    # orientation
    up.matplotlib.box([x, y, z], orientation='horizontal')
    up.matplotlib.box([x, y, z], orientation='vertical')
    with pytest.raises(ValueError):
        up.matplotlib.box([x, y, z], orientation='nonsense')

    # show_mean
    up.matplotlib.box([x, y, z], show_mean=False)
    up.matplotlib.box([x, y, z], show_mean=True)

    # show_notch
    up.matplotlib.box([x, y, z], show_notch=False)
    up.matplotlib.box([x, y, z], show_notch=True)


def test_box_unknown_arg(caplog):
    try_unknown_argument(caplog, up.matplotlib.box, dict(data=[[1, 2, 3], [1, 2, 3]]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_histogram_export(my_outdir, name, x, y, z):
    fig = up.matplotlib.histogram([x, y, z])
    filepath = create_output_filepath(my_outdir, 'histogram_' + name)
    export_all_available_formats(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_histogram_parameters(name, x, y, z):
    # default
    up.matplotlib.histogram([x, y, z])

    # name
    up.matplotlib.histogram([x, y, z], name=['a', 'b'])

    # color
    for color in TEST_COLORS:
        up.matplotlib.histogram([x, y, z], color=color)
        up.matplotlib.histogram([x, y, z], color=[color, 'red', color, 'blue'])

    # opacity
    up.matplotlib.histogram([x, y, z], opacity=0.5)

    # bar_mode and normalization
    for bar_mode in ['stack', 'group']:
        up.matplotlib.histogram([x, y, z], bar_mode=bar_mode)

    # orientation
    up.matplotlib.histogram([x, y, z], orientation='horizontal')
    up.matplotlib.histogram([x, y, z], orientation='vertical')
    with pytest.raises(ValueError):
        up.matplotlib.histogram([x, y, z], orientation='nonsense')

    # bins
    up.matplotlib.histogram([x, y, z], bin_x_number=20, bin_x_start=0.0, bin_x_stop=12.0)


def test_histogram_legend_parameters():
    series = list(range(20))
    data = dict(data=[series, series, series])
    try_all_legend_parameters(up.matplotlib.histogram, data)


def test_histogram_unknown_arg(caplog):
    try_unknown_argument(caplog, up.matplotlib.histogram, dict(data=[[1, 2, 3], [1, 2, 3]]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_scatter_matrix_export(my_outdir, name, x, y, z):
    fig = up.matplotlib.scatter_matrix([x, y, z])
    filepath = create_output_filepath(my_outdir, 'scatter_matrix_' + name)
    export_all_available_formats(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_scatter_matrix_parameters(name, x, y, z):
    # default
    up.matplotlib.scatter_matrix([x, y, z])

    # name
    up.matplotlib.scatter_matrix([x, y, z], name=['a', 'b'])

    # color
    for color in TEST_COLORS[0:len(TEST_COLORS):len(TEST_COLORS)//5]:
        up.matplotlib.scatter_matrix([x, y, z], color=color)
        up.matplotlib.scatter_matrix([x, y, z], color=[color, 'red', color, 'blue'])

    # opacity
    up.matplotlib.scatter_matrix([x, y, z], opacity=0.5)

    # show or hide plots
    up.matplotlib.scatter_matrix([x, y, z], show_diagonal=False)
    up.matplotlib.scatter_matrix([x, y, z], show_diagonal=True)

    up.matplotlib.scatter_matrix([x, y, z], show_lower=True)
    up.matplotlib.scatter_matrix([x, y, z], show_lower=False)

    up.matplotlib.scatter_matrix([x, y, z], show_upper=True)
    up.matplotlib.scatter_matrix([x, y, z], show_upper=False)

    # show_colormap
    up.matplotlib.scatter_matrix(
        [x, y, z], color=x, colormap='viridis', show_colormap=True, colormap_reversed=True,
        colormap_label_size=20, colormap_label_color='red', colormap_label_font='serif')

    # tick hiding
    up.matplotlib.scatter_matrix([x, y, z]*3, show_upper=False)


def test_scatter_matrix_unknown_arg(caplog):
    try_unknown_argument(caplog, up.matplotlib.scatter_matrix, dict(data=[[1, 2, 3], [1, 2, 3]]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_violin_export(my_outdir, name, x, y, z):
    fig = up.matplotlib.violin([x, y, z])
    filepath = create_output_filepath(my_outdir, 'violin_' + name)
    export_all_available_formats(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_violin_parameters(name, x, y, z):
    # default
    up.matplotlib.violin([x, y, z])

    # name
    up.matplotlib.violin([x, y, z], name=['a', 'b'])

    # color
    for color in TEST_COLORS:
        up.matplotlib.violin([x, y, z], color=color)
        up.matplotlib.violin([x, y, z], color=[color, 'red', color, 'blue'])

    # opacity
    up.matplotlib.violin([x, y, z], opacity=0.5)

    # orientation
    up.matplotlib.violin([x, y, z], orientation='horizontal')
    up.matplotlib.violin([x, y, z], orientation='vertical')
    with pytest.raises(ValueError):
        up.matplotlib.violin([x, y, z], orientation='nonsense')

    # violin width
    up.matplotlib.violin([x, y, z], violin_width=0.2)

    # median, mean, min/max
    for val in [True, False]:
        up.matplotlib.violin([x, y, z], show_mean=val, show_median=val, show_extrema=val)


def test_violin_unknown_arg(caplog):
    try_unknown_argument(caplog, up.matplotlib.violin, dict(data=[[1, 2, 3], [1, 2, 3]]))

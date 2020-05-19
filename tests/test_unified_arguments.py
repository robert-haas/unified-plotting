import pytest

import unified_plotting as up
from unified_plotting._unified_arguments import colormaps as cm
from unified_plotting._unified_arguments import colors
from unified_plotting._unified_arguments.colors.conversion import any_color_to_rgba


# Shared

mpl_builtin_cm = list(cm.MATPLOTLIB_BUILTIN_COLORMAPS)
mpl_external_cm = list(cm.MATPLOTLIB_EXTERNAL_COLORMAPS)
mpl_all_cm = mpl_builtin_cm + mpl_external_cm
plotly_builtin_cm = list(cm.PLOTLY_BUILTIN_COLORMAPS)
plotly_external_cm = list(cm.PLOTLY_EXTERNAL_COLORMAPS)
plotly_all_cm = plotly_builtin_cm + plotly_external_cm


# Tests

# - marker_style
def test_marker_style():
    marker_styles = [
        "o", "circle",
        ".", "point", "dot",
        "t", "3", "triangle",
        "s", "4", "square",
        "p", "5", "pentagon",
        "h", "6", "hexagon",
        "8", "octagon",
        "*", "star",
        "+", "plus",
        "x", "cross",
        "d", "diamond",
        "-", "_", "horizontal_line",
        "|", "vertical_line",
        "^", "triangle_up",
        "v", "triangle_down",
        "<", "triangle_left",
        ">", "triangle_right",
    ]
    for ms in marker_styles:
        up.matplotlib.scatter(x=[1, 2], y=[1, 2], marker_style=ms)
        up.plotly.scatter(x=[1, 2], y=[1, 2], marker_style=ms)


# - line_style
def test_line_style():
    line_styles = [
        "solid", "-",
        "dash", "--",
        "dashdot", "-.", ".-",
        "dot", ".", ":", "..",
    ]
    for ls in line_styles:
        up.matplotlib.scatter(x=[1, 2], y=[1, 2], line_style=ls, show_line=True)
        up.plotly.scatter(x=[1, 2], y=[1, 2], line_style=ls, show_line=True)


# - colormap
def test_colormaps_unified():
    some_colormaps = [
        'aggrnyl', 'pastel2', 'cividis', 'accent', 'cmr.arctic',
        'cet.cyclic_tritanopic_wrwc_70_100_c20', 'cet.glasbey_bw', 'cet.linear_kbgyw_5_98_c62',
        'cmo.algae', 'cmo.matter',
        'cmr.amber', 'cmr.waterlily',
        'svc.blue1', 'svc.discrete-4-blue-green', 'svc.outlier-gray-25',
    ]
    for cmap in some_colormaps:
        assert cmap in mpl_all_cm
        assert cmap in plotly_all_cm
    assert set(mpl_all_cm) == set(plotly_all_cm)


def test_colormaps_nonredundant():
    assert len(set(mpl_all_cm)) == len(mpl_all_cm)
    assert len(set(plotly_all_cm)) == len(plotly_all_cm)


def test_colormaps_matplotlib():
    for cmap in mpl_all_cm:
        up.matplotlib.histogram_2d([1, 2], [1, 2], colormap=cmap)


def test_colormaps_plotly():
    some_colormaps = plotly_all_cm[0:len(plotly_all_cm):len(plotly_all_cm)//50]
    for cmap in some_colormaps:
        up.plotly.histogram_2d([1, 2], [1, 2], colormap=cmap)


# - color
def test_colors_unified():
    some_colors = [
        "g", "darkseagreen", "tab.green", "xkcd.algae_green",
        'y', 'blanchedalmond', 'limegreen', 'xkcd.azul', 'xkcd.hot_magenta', 'xkcd.peacock_blue',
        'tab.orange', 'tab.red',
    ]
    for col in some_colors:
        assert col in colors.named_colors.COLORS


def test_colors_matplotlib():
    some_colors = [
        "#CC7030", "#00ff00",
        "g", "darkseagreen", "tab.green", "xkcd.algae_green",
        "#0f0",
        "rgb(51, 51, 255)",
        (0.2, 0.2, 1.0),
        "rgba(0, 255, 0, 0.3)",
        (0, 255, 0, 0.3),
    ]
    for col in some_colors:
        up.matplotlib.scatter(x=[1, 2], y=[1, 2], color=col)


def test_colors_plotly():
    some_colors = [
        "#CC7030", "#00ff00",
        "g", "darkseagreen", "tab.green", "xkcd.algae_green",
        "#0f0",
        "rgb(51, 51, 255)",
        (0.2, 0.2, 1.0),
        "rgba(0, 255, 0, 0.3)",
        (0, 255, 0, 0.3),
    ]
    for col in some_colors:
        up.plotly.scatter(x=[1, 2], y=[1, 2], color=col)


def test_color_conversion1():
    col_hex = colors.conversion.any_color_to_rgba('#ddeeff')
    col_hex_short = colors.conversion.any_color_to_rgba('#def')
    col_rgb_str = colors.conversion.any_color_to_rgba('rgb(221,238,255)')
    col_rgb_tup = colors.conversion.any_color_to_rgba((221, 238, 255))
    col_rgb_tup2 = colors.conversion.any_color_to_rgba((221/255.0, 238/255.0, 255/255.0))
    col_rgba_str = colors.conversion.any_color_to_rgba('rgba(221,238,255,1)')
    col_rgba_tup = colors.conversion.any_color_to_rgba((221, 238, 255, 1.0))
    col_rgba_tup2 = colors.conversion.any_color_to_rgba((221/255.0, 238/255.0, 255/255.0, 1.0))
    assert col_hex == col_hex_short == col_rgb_str == col_rgb_tup == col_rgb_tup2 == \
        col_rgba_str == col_rgba_tup == col_rgba_tup2 == (221, 238, 255, 1.0)


def test_color_conversion2():
    in_out_map = [
        # named
        ['transparent', (0, 0, 0, 0.0)],
        ['black', (0, 0, 0, 1.0)],
        ['white', (255, 255, 255, 1.0)],
        ['red', (255, 0, 0, 1.0)],
        ['blue', (0, 0, 255, 1.0)],
        ['green', (0, 128, 0, 1.0)],
        ['teal', (0, 128, 128, 1.0)],

        # hex triplet
        ['#000000', (0, 0, 0, 1.0)],
        ['#FFFFFF', (255, 255, 255, 1.0)],
        ['#ffffff', (255, 255, 255, 1.0)],
        ['#FfFfFF', (255, 255, 255, 1.0)],
        ['#BFBF3F', (191, 191, 63, 1.0)],
        ['#bfBF3f', (191, 191, 63, 1.0)],
        ['#F78B26', (247, 139, 38, 1.0)],
        ['#f78b26', (247, 139, 38, 1.0)],

        # RGB str
        ['rgb(0,0,0)', (0, 0, 0, 1.0)],
        ['rgb (0, 0, 0)', (0, 0, 0, 1.0)],
        ['r g b (0 , 0 , 0)', (0, 0, 0, 1.0)],
        ['rgb(255,255,255)', (255, 255, 255, 1.0)],
        ['rgb(255, 255, 255)', (255, 255, 255, 1.0)],
        ['r g b  (255,  255,  255)', (255, 255, 255, 1.0)],
        ['rgb(17.1,4.4,3.8)', (17, 4, 3, 1.0)],

        ['rgb(0, 0, 1.0)', (0, 0, 255, 1.0)],
        ['rgb(0, 1.0, 1.0)', (0, 255, 255, 1.0)],
        ['rgb(1.0, 1.0, 1.0)', (255, 255, 255, 1.0)],
        ['rgb(1, 1, 1)', (1, 1, 1, 1.0)],  # special case

        # RGBA str
        ['rgba(0, 0, 255, 1.0)', (0, 0, 255, 1.0)],
        ['rgba( 0.0, 0, 255.0, 1)', (0, 0, 255, 1.0)],

        ['rgba(1.0, 1.0, 1.0, 0.5)', (255, 255, 255, 0.5)],
        ['rgba(1.0, 1.0, 1.0, 1.0)', (255, 255, 255, 1.0)],
        ['rgba(1.0, 1.0, 1.0, 1)', (255, 255, 255, 1.0)],
        ['rgba(1, 1, 1, 0.5)', (1, 1, 1, 0.5)],  # special case
        ['rgba(1, 1, 1, 1.0)', (1, 1, 1, 1.0)],  # special case
        ['rgba(1, 1, 1, 1)', (1, 1, 1, 1.0)],  # special case

        # RGB tuple
        [(0, 0, 255), (0, 0, 255, 1.0)],

        [(1.0, 1.0, 1.0), (255, 255, 255, 1.0)],
        [(1.0, 1, 1), (255, 255, 255, 1.0)],
        [(1, 1, 1), (1, 1, 1, 1.0)],  # special case

        # RGBA tuple
        [(0, 0, 0, 1.0), (0, 0, 0, 1.0)],
        [(255, 255, 255, 1.0), (255, 255, 255, 1.0)],
        [(128, 0, 0, 0.5), (128, 0, 0, 0.5)],

        [(1.0, 1.0, 1.0, 0.5), (255, 255, 255, 0.5)],
        [(1.0, 1.0, 1.0, 1.0), (255, 255, 255, 1.0)],
        [(1.0, 1.0, 1.0, 1), (255, 255, 255, 1.0)],
        [(1, 1, 1.0, 0.5), (255, 255, 255, 0.5)],
        [(1, 1, 1, 0.5), (1, 1, 1, 0.5)],  # special case
        [(1, 1, 1, 1.0), (1, 1, 1, 1.0)],  # special case
        [(1, 1, 1, 1), (1, 1, 1, 1.0)],  # special case
    ]

    for color_in, color_out_rgba in in_out_map:
        assert any_color_to_rgba(color_in) == color_out_rgba


def test_color_conversion_fail():
    invalid_inputs = [
        # named
        'thisisnonsense',
        'utternonsense',

        # hex triplet
        '00FF00',
        '-1FF00',
        '00GG00',

        # RGB str
        'rgb(-1, 0, 0)',
        'rgb(0, -1, 0)',
        'rgb(0, 0, -1)',
        'rgb(256, 0, 0)',
        'rgb(0, 256, 0)',
        'rgb(0, 0, 256)',
        'rgb(0, 0, 0, 0)',
        'rgb(0, 255, 0, 255)',
        'rgb[0, 255, 0]',
        # 'rgb(0, 255, 0',  # TODO
        'rgb 0, 255, 0)',
        'rgb 0, 255, 0',
        'rgb(0; 255; 0)',

        # RGBA str
        'rgba(-1, 0, 0, 1.0)',
        'rgba(0, -1, 0, 1.0)',
        'rgba(0, 0, -1, 1.0)',
        'rgba(0, 0, 0, -0.1)',
        'rgba(256, 0, 0, 1.0)',
        'rgba(0, 256, 0, 1.0)',
        'rgba(0, 0, 256, 1.0)',
        'rgba(0, 0, 0, 1.1)',

        # RGB tuple
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, -1),
        (256, 0, 0),
        (0, 256, 0),
        (0, 0, 256),

        # RGBA tuple
        (-1, 0, 0, 1.0),
        (0, -1, 0, 1.0),
        (0, 0, -1, 1.0),
        (0, 0, 0, -0.1),
        (256, 0, 0, 1.0),
        (0, 256, 0, 1.0),
        (0, 0, 256, 1.0),
        (0, 0, 0, 1.1),

        # wrong length tuple
        (0, 0),
        (0, 0, 0, 0, 0),
    ]
    for color_in in invalid_inputs:
        with pytest.raises(ValueError):
            any_color_to_rgba(color_in)

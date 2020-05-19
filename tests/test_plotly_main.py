import os

import pytest

import unified_plotting as up
from shared_data_loading import (ALL_COLORMAPS, INTERPOLATION_METHODS, LINE_STYLES, MARKER_STYLES,
                                 NAMED_COLORS, TEST_COLORS, TESTDATA, TESTDATA_GRID,
                                 TESTDATA_SMALL)
from shared_testing import try_all_legend_parameters, try_unknown_argument


# Common preliminaries

def create_output_filepath(my_outdir, name):
    return os.path.join(my_outdir, 'plotly_' + name)


def export_one_format(fig, filepath):
    fig.export_html(filepath)


def export_all_available_formats(fig, filepath):
    fig.export_html(filepath)
    fig.export_eps(filepath)
    fig.export_jpg(filepath)
    fig.export_png(filepath)
    fig.export_pdf(filepath)
    fig.export_svg(filepath)
    fig.export_webp(filepath)


# Tests with pytest

# 2d plots

@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_bar_export(my_outdir, name, x, y, z):
    fig = up.plotly.bar(x=[x, x, x], y=[x, y, z])
    filepath = create_output_filepath(my_outdir, 'bar_' + name)
    export_all_available_formats(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_bar_parameters(name, x, y, z):
    # default, y is a list
    up.plotly.bar(x, y)
    up.plotly.bar(x=x, y=y)
    with pytest.raises(ValueError):
        up.plotly.bar(x, y+[42])
    with pytest.raises(ValueError):
        up.plotly.bar(x=x, y=y+[42])

    # default, y is a list of lists
    up.plotly.bar([x, x, x], [x, y, z])
    up.plotly.bar(x=[x, x, x], y=[x, y, z])
    with pytest.raises(ValueError):
        up.plotly.bar(x, [x, y, z])  # first api, now deprecated
    with pytest.raises(ValueError):
        up.plotly.bar([x, x, x], [x, y+[42], z])
    with pytest.raises(ValueError):
        up.plotly.bar(x=x, y=[x, y+[42], z])

    # different data types
    up.plotly.bar([1, 2, 3], [1, 2, 3])
    up.plotly.bar([1, 2, 3], [1.0, 2.0, 3])
    up.plotly.bar([1.0, 2.0, 3.0], [1, 2, 3])

    # numerical x axis (instead of categorical default)
    x_num = [i*2 for i in range(len(x))]
    up.plotly.bar([x_num, x_num, x_num], [x, y, z], x_axis_scale='linear')

    # name
    up.plotly.bar([x, x, x], [x, y, z], name=[])
    up.plotly.bar([x, x, x], [x, y, z], name=['too little'])
    up.plotly.bar([x, x, x], [x, y, z], name=['a', 'too little'])
    up.plotly.bar([x, x, x], [x, y, z], name=['a', 'b', 'c'])
    up.plotly.bar([x, x, x], [x, y, z], name=['a', 'b', 'c', 'too much'])

    # color
    for col in ['#00ff00', 'rgb(1, 2, 3)']:
        up.plotly.bar(x, y, color=col)
        up.plotly.bar([x, x, x], [x, y, z], color=col)
        up.plotly.bar(x, y, color=[col, 'red', col])
        up.plotly.bar([x, x, x], [x, y, z], color=[col, 'red', col])
    # named_colors are only tested here and partly due to their large number
    for col in NAMED_COLORS[0:300:30]:
        up.plotly.bar(x, y, color=col)
        up.plotly.bar(x, y, color=[col, 'red', col])

    # opacity
    up.plotly.bar(x, y, opacity=0.1)
    up.plotly.bar([x, x, x], [x, y, z], opacity=0.1)

    # bar_mode
    up.plotly.bar([x, x, x], [x, y, z], bar_mode='stack')
    up.plotly.bar([x, x, x], [x, y, z], bar_mode='group')
    up.plotly.bar([x, x, x], [x, y, z], bar_mode='overlay')
    up.plotly.bar([x, x, x], [x, y, z], bar_mode='relative')
    with pytest.raises(ValueError):
        up.plotly.bar(x, [x, y, z], bar_mode='nonsense')

    # bar_width
    for val in [0.1, 0.8, 1.1]:
        up.plotly.bar(x, y, bar_width=val)
        up.plotly.bar([x, x, x], [x, y, z], bar_width=val)

    # bartext
    up.plotly.bar([1, 2, 3], [1, 2, 3], show_bartext=True)
    up.plotly.bar([x, x, x], [x, y, z], show_bartext=True)
    up.plotly.bar([x, x, x], [x, y, z], show_bartext=True, bartext_font='Arial')
    for col in TEST_COLORS:
        up.plotly.bar([x, x, x], [x, y, z], show_bartext=True, bartext_color=col)
        up.plotly.bar([x, x, x], [x, y, z], show_bartext=True, bartext_color=[col, 'red', col])
    up.plotly.bar([x, x, x], [x, y, z], show_bartext=True, bartext_size=8)
    for pos in ['inside', 'outside', 'auto']:
        up.plotly.bar([x, x, x], [x, y, z], show_bartext=True, bartext_position=pos)
    with pytest.raises(ValueError):
        up.plotly.bar([x, x, x], [x, y, z], show_bartext=True, bartext_position='nonsense')

    # plot size - tested once here
    up.plotly.bar([1, 2, 3], [1, 2, 3], width_mm=100, height_mm=100)
    up.plotly.bar([1, 2, 3], [1, 2, 3], width_in=2, height_in=2)
    up.plotly.bar([1, 2, 3], [1, 2, 3], width_pt=300, height_pt=300)

    # plot color - tested once here
    up.plotly.bar([1, 2, 3], [1, 2, 3], plot_background_color='red')
    up.plotly.bar([1, 2, 3], [1, 2, 3], paper_background_color='red')

    # title - tested once here
    up.plotly.bar([1, 2, 3], [1, 2, 3], title='my title', title_color='red', title_size=14,
                  title_font='Arial', title_position='left')
    up.plotly.bar([1, 2, 3], [1, 2, 3], title='my title', title_color='rgb(0,0,0)',
                  title_font='cmr10', title_position='right')

    # axis scale - tested once here
    up.plotly.bar([1, 2, 3], [1, 2, 3], x_axis_scale='log')
    up.plotly.bar([1, 2, 3], [1, 2, 3], x_axis_scale='lin')
    up.plotly.bar([1, 2, 3], [1, 2, 3], y_axis_scale='log')
    up.plotly.bar([1, 2, 3], [1, 2, 3], y_axis_scale='lin')
    with pytest.raises(ValueError):
        up.plotly.bar([x, x, x], [x, y, z], x_axis_scale='nonsense')
    with pytest.raises(ValueError):
        up.plotly.bar([x, x, x], [x, y, z], y_axis_scale='nonsense')


def test_bar_legend_parameters():
    data = dict(x=range(20), y=range(20))
    try_all_legend_parameters(up.plotly.bar, data)


def test_bar_unknown_arg(caplog):
    try_unknown_argument(caplog, up.plotly.bar, dict(x=[1, 2, 3], y=[1, 2, 3]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_density_2d_export(my_outdir, name, x, y, z):
    fig = up.plotly.density_2d(x, y)
    filepath = create_output_filepath(my_outdir, 'density_2d_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_density_2d_parameters(name, x, y, z):
    # default
    up.plotly.density_2d(x, y)
    up.plotly.density_2d(x=x, y=y)
    with pytest.raises(ValueError):
        up.plotly.density_2d(x, y+[42])

    # color & contour line
    up.plotly.density_2d(x, y, color='magenta')
    up.plotly.density_2d(x, y, show_line=True, color='magenta')
    up.plotly.density_2d(x, y, show_line=True, color='magenta', line_color='cyan')

    # contour label
    up.plotly.density_2d(x, y, show_contour_label=True, contour_label_font='serif',
                         contour_label_size=20, contour_label_color='red')

    # opacity
    up.plotly.density_2d(x, y, opacity=0.5)

    # smoothing
    up.plotly.density_2d(x, y, smoothing=0.5)

    # bin_x_number
    up.plotly.density_2d(x, y, bin_x_number=10)

    # bin_y_number
    up.plotly.density_2d(x, y, bin_x_number=10)

    # colormaps
    for cmap in ALL_COLORMAPS[0:len(ALL_COLORMAPS):len(ALL_COLORMAPS)//15]:
        up.plotly.density_2d(
            x, y, colormap=cmap, colormap_reversed=True,
            colormap_label_size=20, colormap_label_color='red', colormap_label_font='serif')

    # kwargs
    up.plotly.density_2d(x, y, contours=dict(showlines=False))


def test_density_2d_unknown_arg(caplog):
    try_unknown_argument(caplog, up.plotly.density_2d, dict(x=[1, 2, 3], y=[1, 2, 3]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_density_scatter_histogram_2d_export(my_outdir, name, x, y, z):
    fig = up.plotly.density_scatter_histogram_2d(x, y)
    filepath = create_output_filepath(my_outdir, 'density_scatter_histogram_2d_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_density_scatter_histogram_2d_parameters(name, x, y, z):
    # default
    up.plotly.density_scatter_histogram_2d(x, y)
    up.plotly.density_scatter_histogram_2d(x=x, y=y)
    with pytest.raises(ValueError):
        up.plotly.density_scatter_histogram_2d(x, y+[42])

    # color
    for color in TEST_COLORS:
        up.plotly.density_scatter_histogram_2d(x, y, color=color)
        up.plotly.density_scatter_histogram_2d(x, y, color='magenta', marker_color=color)

    # opacity
    up.plotly.density_scatter_histogram_2d(x, y, opacity=0.1)
    up.plotly.density_scatter_histogram_2d(x, y, opacity=0.1, marker_opacity=0.3)

    # show_histogram
    up.plotly.density_scatter_histogram_2d(x, y, show_histogram=True)
    up.plotly.density_scatter_histogram_2d(x, y, show_histogram=False)

    # show_density
    up.plotly.density_scatter_histogram_2d(x, y, show_density=True)
    up.plotly.density_scatter_histogram_2d(x, y, show_density=False)

    # show_marker
    up.plotly.density_scatter_histogram_2d(x, y, show_marker=True)
    up.plotly.density_scatter_histogram_2d(x, y, show_marker=False)

    # colormaps
    for cmap in ALL_COLORMAPS[0:50:5]:
        up.plotly.density_scatter_histogram_2d(
            x, y, colormap=cmap, colormap_reversed=True,
            colormap_label_size=20, colormap_label_color='red', colormap_label_font='serif')


def test_density_scatter_histogram_2d_unknown_arg(caplog):
    try_unknown_argument(
        caplog, up.plotly.density_scatter_histogram_2d, dict(x=[1, 2, 3], y=[1, 2, 3]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_histogram_2d_export(my_outdir, name, x, y, z):
    fig = up.plotly.histogram_2d(x, y)
    filepath = create_output_filepath(my_outdir, 'histogram_2d_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_histogram_2d_parameters(name, x, y, z):
    # default
    up.plotly.histogram_2d(x, y)
    up.plotly.histogram_2d(x=x, y=y)
    with pytest.raises(ValueError):
        up.plotly.histogram_2d(x, y+[42])

    # opacity
    up.plotly.histogram_2d(x, y, opacity=0.5)

    # bin_x_number
    up.plotly.histogram_2d(x, y, bin_x_number=10)

    # colormaps
    for cmap in ALL_COLORMAPS[0:50:5]:
        up.plotly.histogram_2d(
            x, y, colormap=cmap, colormap_reversed=True,
            colormap_label_size=20, colormap_label_color='red', colormap_label_font='serif')


def test_histogram_2d_unknown_arg(caplog):
    try_unknown_argument(caplog, up.plotly.histogram_2d, dict(x=[1, 2, 3], y=[1, 2, 3]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_scatter_export(my_outdir, name, x, y, z):
    fig = up.plotly.scatter(x, y)
    filepath = create_output_filepath(my_outdir, 'scatter_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_scatter_parameters(name, x, y, z):
    # default
    up.plotly.scatter(x, y)
    up.plotly.scatter([x, x], [y, z])
    up.plotly.scatter(x=x, y=y)
    up.plotly.scatter(x=[x, x], y=[y, z])

    with pytest.raises(ValueError):
        up.plotly.scatter(x, y+[42])
    with pytest.raises(ValueError):
        up.plotly.scatter(x+[42], y)
    with pytest.raises(ValueError):
        up.plotly.scatter(x=[x, x], y=[y, z+[42]])
    with pytest.raises(ValueError):
        up.plotly.scatter(x=[x, x+[42]], y=[y, z])

    # name
    up.plotly.scatter(x, y, name=[], show_legend=True)
    up.plotly.scatter(x, y, name=['y'])                                        # default used
    up.plotly.scatter(x, y, name=['y', 'too much'])                            # simply not used
    up.plotly.scatter([x, x, x], [y, y, y], name=[])                           # default used
    up.plotly.scatter([x, x, x], [y, y, y], name=['a', 'too little'])          # default used
    up.plotly.scatter([x, x, x], [y, y, y], name=[1, 2, 3])                    # str conversion
    up.plotly.scatter([x, x, x], [y, y, y], name=['a', 'b', 'c', 'too much'])  # simply not used

    # color
    for color in TEST_COLORS:
        up.plotly.scatter(x, y, color=color)
        up.plotly.scatter([x, x], [y, y], color=[color, color])
    up.plotly.scatter(x, y, color=x)
    up.plotly.scatter([x, x, x], [y, y, y], color=[x, y, x])
    up.plotly.scatter([x, x, x], [y, y, y], color=[x, 'blue'])
    up.plotly.scatter([x, x, x], [y, y, y], color=[x, 'blue', (0, 10, 0)])
    up.plotly.scatter([x, x, x], [y, y, y], color=[x, 'blue', (0, 10, 0), y])

    # opacity
    up.plotly.scatter(x, y, opacity=0.5)
    up.plotly.scatter([x, x, x], [y, y, y], opacity=0.5)
    up.plotly.scatter([x, x, x], [y, y, y], opacity=[0.1, 1.0])
    up.plotly.scatter([x, x, x], [y, y, y], opacity=[0.1, 1.0, 0.5])
    up.plotly.scatter([x, x, x], [y, y, y], opacity=[0.1, 1.0, 0.5, 0.8])

    # marker and line
    up.plotly.scatter(x, y, show_marker=False, show_line=False)

    up.plotly.scatter(x, y, marker_color=x, marker_colormap='viridis')
    up.plotly.scatter(x, y, color=x, marker_colormap='viridis')
    up.plotly.scatter(
        x, y, marker_color=x, colormap='viridis', colormap_reversed=True,
        colormap_label_size=20, colormap_label_color='red', colormap_label_font='serif')

    up.plotly.scatter(x, y, marker_size=10, marker_style='s', marker_opacity=0.2)
    up.plotly.scatter([x, x, x], [y, y, y], marker_size=[1, 2], marker_style=['s', '*'],
                      marker_opacity=[0.1, 0.2])

    for marker_style in MARKER_STYLES:
        up.plotly.scatter(x, y, marker_style=marker_style)

    up.plotly.scatter(x, y, show_line=True, line_color='red', line_width=5, line_style='--')
    up.plotly.scatter(x, y, show_line=True, line_color=x, line_width=0.1, line_style='.')
    up.plotly.scatter([x, x, x], [y, y, y], show_line=True, line_color=[x, y],
                      line_width=[0.1, 0.5], line_style=['.', '-'])

    for line_style in LINE_STYLES:
        up.plotly.scatter(x, y, show_line=True, line_style=line_style)

    # legend
    arguments = [
        ('legend_title', 'Legend'),
        ('legend_color', 'red'),
        ('legend_color', (0, 1, 0)),
        ('legend_color', 'rgba(0, 1, 0, 0.8)'),
        ('legend_color', '#00ff00'),
        ('legend_size', 20),
        ('legend_font', 'serif'),
        ('legend_background_color', 'red'),
        ('legend_background_color', (0, 1, 0)),
        ('legend_background_color', 'rgba(0, 1, 0, 0.8)'),
        ('legend_background_color', '#0f00f0'),
        ('legend_position_horizontal', 'center'),
        ('legend_position_vertical', 'center'),
        ('legend_border_color', 'red'),
        ('legend_border_color', (0, 1, 0)),
        ('legend_border_color', 'rgba(0, 1, 0, 0.8)'),
        ('legend_border_color', '#0f00f0'),
        ('legend_border_size', 3.2),
    ]
    svg_texts = []
    for key, val in arguments:
        kwargs = {key: val}
        for show_legend in [True, False]:
            fig = up.plotly.scatter(x, y, show_legend=show_legend, **kwargs)
            svg_texts.append(fig.svg_text)
    assert len(svg_texts) == len(set(svg_texts))


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
    up.plotly.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_left=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_top=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        **kwargs,
    )
    up.plotly.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_left=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_bottom=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        **kwargs,
    )
    up.plotly.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_right=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_top=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        **kwargs,
    )
    up.plotly.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_right=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_bottom=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        **kwargs,
    )
    # Single series, single x error, dual y error
    up.plotly.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_left=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_bottom=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        y_error_top=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        **kwargs,
    )
    up.plotly.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_right=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_bottom=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        y_error_top=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        **kwargs,
    )
    # Single series, dual x error, single y error
    up.plotly.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_left=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        x_error_right=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_bottom=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        **kwargs,
    )
    up.plotly.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_left=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        x_error_right=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_top=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        **kwargs,
    )
    # Single series, dual x error, dual y error
    up.plotly.scatter(
        x=[1, 2, 3, 4, 5, 6, 7],
        y=[2, 3, 4, 5, 6, 7, 8],
        x_error_left=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        x_error_right=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        y_error_top=[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        y_error_bottom=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        **kwargs,
    )
    # Multiple series, single x error, single y error
    up.plotly.scatter(
        x=[[1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7]],
        y=[[2, 3, 4, 5, 6, 7, 8], [4, 5, 6, 7, 8, 9, 10]],
        x_error_left=[[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]],
        y_error_bottom=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]],
        **kwargs,
    )
    # Multiple series, dual x error, dual y error
    up.plotly.scatter(
        x=[[1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7]],
        y=[[2, 3, 4, 5, 6, 7, 8], [4, 5, 6, 7, 8, 9, 10]],
        x_error_left=[[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]],
        x_error_right=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]],
        y_error_top=[[0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]],
        y_error_bottom=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]],
        **kwargs,
    )
    # Single series, single spec
    up.plotly.scatter(
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
    up.plotly.scatter(
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
    up.plotly.scatter(
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
    up.plotly.scatter(
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
    up.plotly.scatter(
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
    try_all_legend_parameters(up.plotly.scatter, data)


def test_scatter_unknown_arg(caplog):
    try_unknown_argument(caplog, up.plotly.scatter, dict(x=[1, 2, 3], y=[1, 2, 3]))


# 3d plots

@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_contour_irregular(my_outdir, name, x, y, z):
    fig = up.plotly.contour(x, y, z)
    filepath = create_output_filepath(my_outdir, 'contour_irregular_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_GRID)
def test_contour_grid(my_outdir, name, x, y, z):
    fig = up.plotly.contour(x, y, z, x_axis_scale='cat', y_axis_scale='cat')
    filepath = create_output_filepath(my_outdir, 'contour_grid_' + name)
    export_one_format(fig, filepath)


def test_contour_categorical(my_outdir):
    # 1) Irregular
    # x
    with pytest.raises(ValueError):
        up.plotly.contour(['a', 'b', 'c'], [1, 2, 3], [3, 4, 3])
    up.plotly.contour(['a', 'b', 'c'], [1, 2, 3], [3, 4, 3], x_axis_scale='cat')
    up.plotly.contour(['a', 'b', 'c'], [1, 2, 3], [3, 4, 3], x_axis_scale='categorical')
    # y
    with pytest.raises(ValueError):
        up.plotly.contour([1, 2, 3], ['a', 'b', 'c'], [3, 4, 3])
    up.plotly.contour([1, 2, 3], ['a', 'b', 'c'], [3, 4, 3], y_axis_scale='cat')
    up.plotly.contour([1, 2, 3], ['a', 'b', 'c'], [3, 4, 3], y_axis_scale='categorical')
    # z
    with pytest.raises(ValueError):
        up.plotly.contour([1, 2, 3], [3, 4, 3], ['a', 'b', 'c'])
    up.plotly.contour([1, 2, 3], [3, 4, 3], ['a', 'b', 'c'], z_axis_scale='cat')
    up.plotly.contour([1, 2, 3], [3, 4, 3], ['a', 'b', 'c'], z_axis_scale='categorical')
    # 2) Grid
    up.plotly.contour([1, 2, 3], [1, 2], [[2, 1, 2], [3, 4, 3]])
    # - x
    up.plotly.contour([2, 1, 3], [1, 2], [[2, 1, 2], [3, 4, 3]], x_axis_scale='cat')
    up.plotly.contour([2, 1, 3], [1, 2], [[2, 1, 2], [3, 4, 3]], x_axis_scale='categorical')
    # str
    with pytest.raises(ValueError):
        up.plotly.contour(['a', 'b', 'c'], [1, 2], [[2, 1, 2], [3, 4, 3]])
    up.plotly.contour(['a', 'b', 'c'], [1, 2], [[2, 1, 2], [3, 4, 3]], x_axis_scale='cat')
    up.plotly.contour(['a', 'b', 'c'], [1, 2], [[2, 1, 2], [3, 4, 3]], x_axis_scale='categorical')
    # - y
    up.plotly.contour([1, 2, 3], [2, 1], [[2, 1, 2], [3, 4, 3]], y_axis_scale='cat')
    up.plotly.contour([1, 2, 3], [2, 1], [[2, 1, 2], [3, 4, 3]], y_axis_scale='categorical')
    # str
    with pytest.raises(ValueError):
        up.plotly.contour([1, 2, 3], ['ab', 'cd'], [[2, 1, 2], [3, 4, 3]])
    up.plotly.contour([1, 2, 3], ['ab', 'cd'], [[2, 1, 2], [3, 4, 3]], y_axis_scale='cat')
    up.plotly.contour([1, 2, 3], ['ab', 'cd'], [[2, 1, 2], [3, 4, 3]], y_axis_scale='categorical')
    # - z
    up.plotly.contour([2, 1, 3], [1, 2], [[2, 1, 2], [3, 4, 3]], z_axis_scale='cat')
    up.plotly.contour([2, 1, 3], [1, 2], [[2, 1, 2], [3, 4, 3]], z_axis_scale='categorical')
    # str
    up.plotly.contour(
        [1, 2, 3], [1, 2], [['a', 'b', 'a'], ['c', 'd', 'd']], z_axis_scale='cat')
    up.plotly.contour(
        [1, 2, 3], [1, 2], [['a', 'b', 'a'], ['c', 'd', 'd']], z_axis_scale='categorical')
    with pytest.raises(ValueError):
        up.plotly.contour([1, 2, 3], [1, 2], [['a', 'b', 'a'], ['c', 'd', 'd']])


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_contour_parameters(name, x, y, z):
    # default
    up.plotly.contour(x, y, z)

    # opacity
    up.plotly.contour(x, y, z, opacity=0.5)

    # axis_aspect_ratio
    up.plotly.contour(x, y, z, axis_aspect_ratio=(1, 0.7, 0.5))

    # interpolation_method and interpolation_selection
    for method in INTERPOLATION_METHODS:
        for selection in [None, 'min', 'max']:
            if method not in ['spline_cubic', 'spline_quintic']:  # fail under many conditions
                up.plotly.contour(x, y, z, interpolation_method=method,
                                  interpolation_selection=selection)

    # interpolation_num_x_gridpoints
    up.plotly.contour(x, y, z, interpolation_num_x_gridpoints=50)

    # interpolation_num_y_gridpoints
    up.plotly.contour(x, y, z, interpolation_num_y_gridpoints=50)

    # colormaps
    for cmap in ALL_COLORMAPS[0:50:5]:
        up.plotly.contour(
            x, y, z, colormap=cmap, colormap_reversed=True,
            colormap_label_size=20, colormap_label_color='red', colormap_label_font='serif')


def test_contour_fail1():
    with pytest.raises(ValueError):
        up.plotly.contour(x=[1, 2, 3], y=[1, 2, 3], z=[1, 2, 3, 4])


def test_contour_fail2():
    with pytest.raises(ValueError):
        up.plotly.contour(x=[[1, 2], [1, 2]], y=[[1, 2], [1, 2], [1, 2]], z=[[1, 2], [1, 2]])


def test_contour_fail3():
    with pytest.raises(ValueError):
        up.plotly.contour(x=[1, 2], y=[1, 2, 3], z=[[1, 1, 1], [2, 2, 2]])


def test_contour_fail4():
    with pytest.raises(ValueError):
        up.plotly.contour(x=[1, 2, 3], y=[1, 2, 3], z=[1, 2, 3],
                          interpolation_method='method_which_is_not_known')


def test_contour_fail5():
    with pytest.raises(ValueError):
        up.plotly.contour(x=[1, 2, 3], y=[1, 2, 3], z=[1, 2, 3],
                          interpolation_selection='a_choice_which_is_not_available')


def test_contour_unknown_arg(caplog):
    try_unknown_argument(caplog, up.plotly.contour, dict(x=[1, 2, 3], y=[1, 2, 3], z=[1, 2, 3]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA_GRID)
def test_heatmap_export(my_outdir, name, x, y, z):
    fig = up.plotly.heatmap(x, y, z, x_axis_scale='cat', y_axis_scale='cat')
    filepath = create_output_filepath(my_outdir, 'heatmap_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_GRID)
def test_heatmap_parameters(name, x, y, z):
    # default
    up.plotly.heatmap(x, y, z, x_axis_scale='cat', y_axis_scale='cat')

    # opacity
    up.plotly.heatmap(x, y, z, x_axis_scale='cat', y_axis_scale='cat', opacity=0.5)

    # colormaps
    for cmap in ALL_COLORMAPS[0:50:5]:
        up.plotly.heatmap(
            x, y, z, x_axis_scale='cat', y_axis_scale='cat',
            colormap=cmap, colormap_reversed=True,
            colormap_label_size=20, colormap_label_color='red', colormap_label_font='serif')


def test_heatmap_unknown_arg(caplog):
    try_unknown_argument(caplog, up.plotly.heatmap, dict(x=[1, 2, 3], y=[1, 2, 3], z=[1, 2, 3]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_scatter_3d_export(my_outdir, name, x, y, z):
    fig = up.plotly.scatter_3d(x, y, z)
    filepath = create_output_filepath(my_outdir, 'scatter_3d_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_scatter_3d_parameters(name, x, y, z):
    # default
    up.plotly.scatter_3d(x, y, z)
    up.plotly.scatter_3d([x, x], [y, y], [z, z])
    with pytest.raises(ValueError):
        up.plotly.scatter_3d(x, y+[42], z)
    with pytest.raises(ValueError):
        up.plotly.scatter_3d(x+[42], y, z)
    with pytest.raises(ValueError):
        up.plotly.scatter_3d(x=[x, x], y=[y, y+[42]], z=[z, z])
    with pytest.raises(ValueError):
        up.plotly.scatter_3d(x=[x, x+[42]], y=[y, y], z=[z, z])

    # name
    up.plotly.scatter_3d(x, y, z, name=['1'])
    up.plotly.scatter_3d(x, y, z, name=['1', '2', '3'])
    up.plotly.scatter_3d([x, x], [y, y], [z, z], name=['1'])
    up.plotly.scatter_3d([x, x], [y, y], [z, z], name=['1', '2', '3'])

    # color
    for color in TEST_COLORS + [x]:
        up.plotly.scatter_3d(x, y, z, color=color)
        up.plotly.scatter_3d(x, y, z, color=[color, 'red', color])
        up.plotly.scatter_3d([x, x], [y, y], [z, z], color=color)
        up.plotly.scatter_3d([x, x], [y, y], [z, z], color=[color, 'red', color])

    # opacity
    up.plotly.scatter_3d(x, y, z, opacity=0.5)
    up.plotly.scatter_3d(x, y, z, opacity=[0.1, 0.8])
    up.plotly.scatter_3d([x, x], [y, y], [z, z], opacity=0.5)
    up.plotly.scatter_3d([x, x], [y, y], [z, z], opacity=[0.1, 0.8])

    # axis_aspect_ratio
    up.plotly.scatter_3d(x, y, z, axis_aspect_ratio=(1, 0.7, 0.5))

    # camera position
    up.plotly.scatter_3d(x, y, z, camera_position=[(0, 0, 1), (0, 0, 0), (2, 0.8, 1.0)])

    # show_stem_x, show_stem_y, show_stem_z, show_stem_line, stem_x_position, stem_y_position,
    # stem_z_position
    up.plotly.scatter_3d(
        x, y, z, show_stem_x=False, show_stem_y=True, show_stem_z=False, show_stem_line=True,
        stem_y_position=-10.0, stem_z_position=3.14)
    up.plotly.scatter_3d(
        x, y, z, show_stem_x=True, show_stem_y=False, show_stem_z=True, show_stem_line=False,
        stem_x_position=0.0, stem_y_position=-10.0, stem_z_position=3.14)
    up.plotly.scatter_3d(
        x, y, z, show_stem_x=True, show_stem_y=False, show_stem_z=True, show_stem_line=False,
        stem_shift_factor=0.09)
    up.plotly.scatter_3d(
        [x, x], [y, y], [z, z], show_stem_x=True, show_stem_y=False, show_stem_z=True,
        show_stem_line=False, stem_shift_factor=0.09)

    # interpolation
    up.plotly.scatter_3d(
        x, y, z, show_interpolation_delaunay=True, interpolation_with_highest_points=True)
    for method in ['linear', 'nearest', 'cubic']:
        up.plotly.scatter_3d(
            x, y, z, show_interpolation_allrounder=True, interpolation_allrounder_method=method)
    for method in ['cubic', 'gaussian', 'inverse', 'linear', 'multiquadric', 'quintic',
                   'thin_plate']:
        up.plotly.scatter_3d(
            x, y, z, show_interpolation_rbf=True, interpolation_allrounder_method=method,
            interpolation_with_highest_points=True)
    for method in ['linear', 'cubic', 'quintic']:
        up.plotly.scatter_3d(
            x, y, z, show_interpolation_spline=True, interpolation_allrounder_method=method,
            interpolation_with_highest_points=False)


def test_scatter_3d_legend_parameters():
    series = list(range(20))
    data = dict(x=series, y=series, z=series)
    try_all_legend_parameters(up.plotly.scatter_3d, data)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_scatter_3d_interpolation_allrounder(my_outdir, name, x, y, z):
    fig = up.plotly.scatter_3d(x, y, z, show_interpolation_allrounder=True)
    filepath = create_output_filepath(my_outdir, 'scatter_3d_interpolation_allrounder_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_scatter_3d_interpolation_delaunay(my_outdir, name, x, y, z):
    fig = up.plotly.scatter_3d(x, y, z, show_interpolation_delaunay=True)
    filepath = create_output_filepath(my_outdir, 'scatter_3d_interpolation_delaunay_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_scatter_3d_interpolation_rbf(my_outdir, name, x, y, z):
    fig = up.plotly.scatter_3d(x, y, z, show_interpolation_rbf=True)
    filepath = create_output_filepath(my_outdir, 'scatter_3d_interpolation_rbf_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_scatter_3d_interpolation_spline(my_outdir, name, x, y, z):
    fig = up.plotly.scatter_3d(x, y, z, show_interpolation_spline=True)
    filepath = create_output_filepath(my_outdir, 'scatter_3d_interpolation_spline_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_scatter_3d_fail1(name, x, y, z):
    with pytest.raises(ValueError):
        up.plotly.scatter_3d(x, y, z+[1])
    with pytest.raises(ValueError):
        up.plotly.scatter_3d([x, x], [y, y], [z, z+[1]])


def test_scatter_3d_unknown_arg(caplog):
    try_unknown_argument(
        caplog, up.plotly.scatter_3d, dict(x=[1, 2, 3], y=[1, 2, 3], z=[1, 2, 3]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_surface_irregular_export(my_outdir, name, x, y, z):
    fig = up.plotly.surface(x, y, z)
    filepath = create_output_filepath(my_outdir, 'surface_irregular_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_GRID)
def test_surface_grid_export(my_outdir, name, x, y, z):
    fig = up.plotly.surface(x, y, z, x_axis_scale='cat', y_axis_scale='cat')
    filepath = create_output_filepath(my_outdir, 'surface_grid_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_surface_parameters(name, x, y, z):
    # default
    up.plotly.surface(x, y, z)

    # opacity
    up.plotly.surface(x, y, z, opacity=0.5)

    # axis_aspect_ratio
    up.plotly.surface(x, y, z, axis_aspect_ratio=(1, 0.7, 0.5))

    # camera position
    up.plotly.surface(x, y, z, camera_position=[(0, 0, 1), (0, 0, 0), (2, 0.8, 1.0)])

    # show_surface
    up.plotly.surface(x, y, z, show_surface=False)

    # surface_opacity,
    up.plotly.surface(x, y, z, surface_opacity=0.8)

    # show_projection_x and projection_x_opacity
    up.plotly.surface(x, y, z, show_projection_x=True, projection_x_opacity=0.8)

    # show_projection_y and projection_y_opacity
    up.plotly.surface(x, y, z, show_projection_y=True, projection_y_opacity=0.8)

    # show_projection_z and projection_z_opacity
    up.plotly.surface(x, y, z, show_projection_z=True, projection_z_opacity=0.8)

    # projection_shift_factor
    up.plotly.surface(x, y, z, projection_shift_factor=0.1)

    # interpolation_method and interpolation_selection
    for method in INTERPOLATION_METHODS:
        for selection in [None, 'min', 'max']:
            if method not in ['spline_cubic', 'spline_quintic']:  # fail under many conditions
                up.plotly.surface(x, y, z, interpolation_method=method,
                                  interpolation_selection=selection)

    # interpolation_num_x_gridpoints
    up.plotly.surface(x, y, z, interpolation_num_x_gridpoints=50)

    # interpolation_num_y_gridpoints
    up.plotly.surface(x, y, z, interpolation_num_y_gridpoints=50)

    # colormaps
    for cmap in ALL_COLORMAPS[0:50:5]:
        up.plotly.surface(
            x, y, z, colormap=cmap, colormap_reversed=True,
            colormap_label_size=20, colormap_label_color='red', colormap_label_font='serif')


def test_surface_fail1():
    with pytest.raises(ValueError):
        up.plotly.surface(x=[1, 2, 3], y=[1, 2, 3], z=[1, 2, 3, 4])


def test_surface_fail2():
    with pytest.raises(ValueError):
        up.plotly.surface(x=[[1, 2], [1, 2]], y=[[1, 2], [1, 2], [1, 2]], z=[[1, 2], [1, 2]])


def test_surface_fail3():
    with pytest.raises(ValueError):
        up.plotly.surface(x=[1, 2], y=[1, 2, 3], z=[[1, 1, 1], [2, 2, 2]])


def test_surface_fail4():
    with pytest.raises(ValueError):
        up.plotly.surface(x=[1, 2, 3], y=[1, 2, 3], z=[1, 2, 3],
                          interpolation_method='a_choice_which_is_not_available')


def test_surface_fail5():
    with pytest.raises(ValueError):
        up.plotly.surface(x=[1, 2, 3], y=[1, 2, 3], z=[1, 2, 3],
                          interpolation_selection='a_choice_which_is_not_available')


def test_surface_unknown_arg(caplog):
    try_unknown_argument(caplog, up.plotly.surface, dict(x=[1, 2, 3], y=[1, 2, 3], z=[1, 2, 3]))


# Nd plots

@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_box_export(my_outdir, name, x, y, z):
    fig = up.plotly.box([x, y, z])
    filepath = create_output_filepath(my_outdir, 'box_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_box_parameters(name, x, y, z):
    # default
    up.plotly.box([x, y, z])

    # name
    up.plotly.box([x, y, z], name=['a', 'b'])

    # color
    for color in TEST_COLORS:
        up.plotly.box([x, y, z], color=color)
        up.plotly.box([x, y, z], color=[color, 'red', color, 'blue'])

    # opacity
    up.plotly.box([x, y, z], opacity=0.5)

    # orientation
    up.plotly.box([x, y, z], orientation='horizontal')
    up.plotly.box([x, y, z], orientation='vertical')
    with pytest.raises(ValueError):
        up.plotly.box([x, y, z], orientation='nonsense')

    # show_mean
    up.plotly.box([x, y, z], show_mean=False)
    up.plotly.box([x, y, z], show_mean=True)

    # show_notch
    up.plotly.box([x, y, z], show_notch=False)
    up.plotly.box([x, y, z], show_notch=True)

    # point_jitter
    up.plotly.box([x, y, z], point_jitter=0.42)

    # point_position
    up.plotly.box([x, y, z], point_position=-1.4)

    # rugs
    up.plotly.box([x, y, z], show_rug=False)
    up.plotly.box([x, y, z], show_rug=True)
    up.plotly.box([x, y, z], show_rug=True,
                  rug_color='black', rug_colormap='Viridis',
                  rug_size=4, rug_opacity=0.1, rug_style='s')
    up.plotly.box([x, y, z],
                  rug_color=['red', 'green', 'blue'],
                  rug_size=[1, 2, 3], rug_opacity=[1.0, 0.5, 0.1], rug_style=['-', 'o', 's'])
    with pytest.raises(ValueError):
        up.plotly.box([x, y, z], rug_style='r')


def test_box_unknown_arg(caplog):
    try_unknown_argument(caplog, up.plotly.box, dict(data=[[1, 2, 3], [1, 2, 3]]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_density_export(my_outdir, name, x, y, z):
    fig = up.plotly.density([x, y, z])
    filepath = create_output_filepath(my_outdir, 'density_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_density_parameters(name, x, y, z):
    # default
    up.plotly.density([x, y, z])

    # name
    up.plotly.density([x, y, z], name=['a', 'b'])

    # color
    for color in TEST_COLORS:
        up.plotly.density([x, y, z], color=color)
        up.plotly.density([x, y, z], color=[color, 'red', color, 'blue'])

    # opacity
    up.plotly.density([x, y, z], opacity=0.5)

    # show_density
    up.plotly.density([x, y, z], show_density=False)
    up.plotly.density([x, y, z], show_density=True)

    # show_box_notch
    up.plotly.density([x, y, z], show_histogram=False)
    up.plotly.density([x, y, z], show_histogram=True)

    # bins
    up.plotly.density([x, y, z], bin_x_number=20, bin_x_start=0.0, bin_x_stop=12.0)

    # kwargs
    up.plotly.density([x, y, z], show_curve=False)
    up.plotly.density([x, y, z], show_hist=False)


def test_density_legend_parameters():
    series = list(range(20))
    data = dict(data=[series, series, series])
    try_all_legend_parameters(up.plotly.density, data)


def test_density_unknown_arg(caplog):
    try_unknown_argument(caplog, up.plotly.density, dict(data=[[1, 2, 3], [1, 2, 3]]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_histogram_export(my_outdir, name, x, y, z):
    fig = up.plotly.histogram([x, y, z])
    filepath = create_output_filepath(my_outdir, 'histogram_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_histogram_parameters(name, x, y, z):
    # default
    up.plotly.histogram([x, y, z])

    # name
    up.plotly.histogram([x, y, z], name=['a', 'b'])

    # color
    for color in TEST_COLORS:
        up.plotly.histogram([x, y, z], color=color)
        up.plotly.histogram([x, y, z], color=[color, 'red', color, 'blue'])

    # opacity
    up.plotly.histogram([x, y, z], opacity=0.5)

    # bar_mode and normalization
    for bar_mode in ['stack', 'group', 'overlay', 'relative']:
        for normalization in ['percent', 'probability', 'density', 'probability density']:
            up.plotly.histogram([x, y, z], bar_mode=bar_mode, normalization=normalization)

    # orientation
    up.plotly.histogram([x, y, z], orientation='horizontal')
    up.plotly.histogram([x, y, z], orientation='vertical')
    with pytest.raises(ValueError):
        up.plotly.histogram([x, y, z], orientation='nonsense')

    # TODO: Validity checks
    # with pytest.raises(ValueError):
    #     up.plotly.histogram([x, y, z], bar_mode='nonsense')
    # with pytest.raises(ValueError):
    #     up.plotly.histogram([x, y, z], normalization='nonsense')

    # bins
    up.plotly.histogram([x, y, z], bin_x_number=20, bin_x_start=0.0, bin_x_stop=12.0)


def test_histogram_legend_parameters():
    series = list(range(20))
    data = dict(data=[series, series, series])
    try_all_legend_parameters(up.plotly.histogram, data)


def test_histogram_unknown_arg(caplog):
    try_unknown_argument(caplog, up.plotly.histogram, dict(data=[[1, 2, 3], [1, 2, 3]]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_parallel_coordinates_export(my_outdir, name, x, y, z):
    fig = up.plotly.parallel_coordinates([x, y, z])
    filepath = create_output_filepath(my_outdir, 'parallel_coordinates_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_parallel_coordinates_parameters(name, x, y, z):
    # default
    up.plotly.parallel_coordinates([x, y, z])

    # data_range
    up.plotly.parallel_coordinates([x, y, z], data_range=(0, 10))
    up.plotly.parallel_coordinates([x, y, z], data_range=[(0, 10), (0, 20), (0, 30)])

    # num_significant_digits
    up.plotly.parallel_coordinates([x, y, z], num_significant_digits=2)

    # name
    up.plotly.parallel_coordinates([x, y, z], name=['a', 'b'])

    # color
    up.plotly.parallel_coordinates([x, y, z], color=y)
    for color in TEST_COLORS:
        up.plotly.parallel_coordinates([x, y, z], color=color)
        up.plotly.parallel_coordinates([x, y, z], color=[color, 'red', color, 'blue'])

    # show_label, label_font, label_size, label_color
    up.plotly.parallel_coordinates(
        [x, y, z], show_label=True, label_font='Arial', label_size=12, label_color='green')
    up.plotly.parallel_coordinates([x, y, z], show_label=False)


def test_parallel_coordinates_unknown_arg(caplog):
    try_unknown_argument(
        caplog, up.plotly.parallel_coordinates, dict(data=[[1, 2, 3], [1, 2, 3]]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_scatter_matrix_export(my_outdir, name, x, y, z):
    fig = up.plotly.scatter_matrix([x, y, z])
    filepath = create_output_filepath(my_outdir, 'scatter_matrix_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_scatter_matrix_parameters(name, x, y, z):
    # default
    up.plotly.scatter_matrix([x, y, z])

    # name
    up.plotly.scatter_matrix([x, y, z], name=['a', 'b'])

    # color
    for color in ['#00ff00', 'rgb(1, 2, 3)']:
        up.plotly.scatter_matrix([x, y, z], color=color)
        up.plotly.scatter_matrix(
            [x, y, z], color=['rgba(1.0, 1.0, 1.0, 0.1)', color, (1, 2, 3), 'blue'])

    # opacity
    up.plotly.scatter_matrix([x, y, z], opacity=0.5)

    # show or hide plots
    up.plotly.scatter_matrix([x, y, z], show_diagonal=False)
    up.plotly.scatter_matrix([x, y, z], show_diagonal=True)

    up.plotly.scatter_matrix([x, y, z], show_diagonal_box=True)
    up.plotly.scatter_matrix([x, y, z], show_diagonal_box=False)

    up.plotly.scatter_matrix([x, y, z], show_diagonal_histogram=True)
    up.plotly.scatter_matrix([x, y, z], show_diagonal_histogram=False)

    up.plotly.scatter_matrix([x, y, z], show_diagonal_scatter=True)
    up.plotly.scatter_matrix([x, y, z], show_diagonal_scatter=False)

    up.plotly.scatter_matrix([x, y, z], show_lower=True)
    up.plotly.scatter_matrix([x, y, z], show_lower=False)

    up.plotly.scatter_matrix([x, y, z], show_lower_density=True)
    up.plotly.scatter_matrix([x, y, z], show_lower_density=False)

    up.plotly.scatter_matrix([x, y, z], show_lower_histogram=True)
    up.plotly.scatter_matrix([x, y, z], show_lower_histogram=False)

    up.plotly.scatter_matrix([x, y, z], show_lower_scatter=True)
    up.plotly.scatter_matrix([x, y, z], show_lower_scatter=False)

    up.plotly.scatter_matrix([x, y, z], show_upper=True)
    up.plotly.scatter_matrix([x, y, z], show_upper=False)

    up.plotly.scatter_matrix([x, y, z], show_upper_histogram=True)
    up.plotly.scatter_matrix([x, y, z], show_upper_histogram=False)

    up.plotly.scatter_matrix([x, y, z], show_upper_scatter=True)
    up.plotly.scatter_matrix([x, y, z], show_upper_scatter=False)

    up.plotly.scatter_matrix([x, y, z], show_diagonal=False, show_diagonal_box=True)
    up.plotly.scatter_matrix([x, y, z], show_diagonal=True, show_diagonal_box=False)

    # show_colormap
    up.plotly.scatter_matrix(
        [x, y, z], show_colormap=True, colormap_reversed=True,
        colormap_label_size=20, colormap_label_color='red', colormap_label_font='serif')


def test_scatter_matrix_unknown_arg(caplog):
    try_unknown_argument(caplog, up.plotly.scatter_matrix, dict(data=[[1, 2, 3], [1, 2, 3]]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_band_export(my_outdir, name, x, y, z):
    fig = up.plotly.band([x, y, z])
    filepath = create_output_filepath(my_outdir, 'band_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_band_parameters(name, x, y, z):
    # default
    up.plotly.band([x, y, z])

    # name
    up.plotly.band([x, y, z], name=['a', 'b'])

    # color
    for color in TEST_COLORS:
        up.plotly.band([x, y, z], color=color)
        up.plotly.band([x, y, z], color=[color, 'red', color, 'blue'])

    # opacity
    up.plotly.band([x, y, z], opacity=0.5)

    # show_mean
    up.plotly.band([x, y, z], show_mean=True)

    # rug
    up.plotly.band(
        [x, y, z], show_rug=True, rug_color='black', rug_size=5, rug_style='s', rug_opacity=1.0)


def test_band_unknown_arg(caplog):
    try_unknown_argument(caplog, up.plotly.band, dict(data=[[1, 2, 3], [1, 2, 3]]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_violin_export(my_outdir, name, x, y, z):
    fig = up.plotly.violin([x, y, z])
    filepath = create_output_filepath(my_outdir, 'violin_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_violin_parameters(name, x, y, z):
    # default
    up.plotly.violin([x, y, z])

    # name
    up.plotly.violin([x, y, z], name=['a', 'b'])

    # color
    for color in TEST_COLORS:
        up.plotly.violin([x, y, z], color=color)
        up.plotly.violin([x, y, z], color=[color, 'red', color, 'blue'])

    # opacity
    up.plotly.violin([x, y, z], opacity=0.5)

    # orientation
    up.plotly.violin([x, y, z], orientation='horizontal')
    up.plotly.violin([x, y, z], orientation='vertical')
    with pytest.raises(ValueError):
        up.plotly.violin([x, y, z], orientation='nonsense')

    # side
    for side in ['positive', 'negative', 'both']:
        up.plotly.violin([x, y, z], side=side)

    # scale_mode
    for scale_mode in ['width', 'count']:
        up.plotly.violin([x, y, z], scale_mode=scale_mode)

    # span_mode
    for span_mode in ['soft', 'hard']:
        up.plotly.violin([x, y, z], span_mode=span_mode)

    # point_mode
    for point_mode in ['all', 'outliers', 'suspectedoutliers']:
        up.plotly.violin([x, y, z], point_mode=point_mode)

    # point_jitter
    up.plotly.violin([x, y, z], point_jitter=0.42)

    # point_position
    up.plotly.violin([x, y, z], point_position=-1.4)

    # violin_width
    up.plotly.violin([x, y, z], violin_width=0.2)

    # show_box
    up.plotly.violin([x, y, z], show_box=False)
    up.plotly.violin([x, y, z], show_box=True)

    # show_mean
    up.plotly.violin([x, y, z], show_mean=False)
    up.plotly.violin([x, y, z], show_mean=True)

    # orientation
    up.plotly.violin([x, y, z], orientation='horizontal')
    up.plotly.violin([x, y, z], orientation='vertical')
    with pytest.raises(ValueError):
        up.plotly.violin([x, y, z], orientation='nonsense')


def test_violin_unknown_arg(caplog):
    try_unknown_argument(caplog, up.plotly.violin, dict(data=[[1, 2, 3], [1, 2, 3]]))


# financial plots

@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_candlestick_export(my_outdir, name, x, y, z):
    fig = up.plotly.candlestick(x, y, z, y, z)
    filepath = create_output_filepath(my_outdir, 'candlestick_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_candlestick_parameters(name, x, y, z):
    # default
    up.plotly.candlestick(x, y, z, y, z)

    # opacity
    up.plotly.candlestick(x, y, z, y, z, opacity=0.5)


def test_candlestick_unknown_arg(caplog):
    try_unknown_argument(
        caplog, up.plotly.candlestick,
        dict(x=[1, 2], open=[1, 2], high=[1, 2], low=[1, 2], close=[1, 2]))


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_ohlc_export(my_outdir, name, x, y, z):
    fig = up.plotly.ohlc(x, y, z, y, z)
    filepath = create_output_filepath(my_outdir, 'ohlc_' + name)
    export_one_format(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA_SMALL)
def test_ohlc_parameters(name, x, y, z):
    # default
    up.plotly.ohlc(x, y, z, y, z)

    # opacity
    up.plotly.ohlc(x, y, z, y, z, opacity=0.5)


def test_ohlc_unknown_arg(caplog):
    try_unknown_argument(
        caplog, up.plotly.ohlc,
        dict(x=[1, 2], open=[1, 2], high=[1, 2], low=[1, 2], close=[1, 2]))

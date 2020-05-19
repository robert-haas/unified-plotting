import os
import random

import pytest

import unified_plotting as up


# Common preliminaries

def create_output_filepath(my_outdir, name):
    return os.path.join(my_outdir, 'plotly_picked_' + name)


def export_all_available_formats(fig, filepath):
    fig.export_html(filepath)


def construct_testdata():
    n = 100
    x = [random.random() for i in range(n)]
    y = [random.gauss(10, 2) for i in range(n)]
    z = [2*xi - 0.3*yi + random.random() for xi, yi in zip(x, y)]
    dataset1 = ['random', x, y, z]
    return [dataset1]


TESTDATA = construct_testdata()


# Tests with pytest

# 2d plots

@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_bar_1(my_outdir, name, x, y, z):
    fig = up.plotly.bar(
        x=[['Roll {}'.format(item) for item in x]] * 2,
        y=[y, z],
        name=['a', 'b', 'c'],
        x_axis_scale='cat',
        show_legend=True,
        color=['black', 'green', 'blue'],
        opacity=0.3,
        bar_mode='stack',
        bar_width=0.7,
        show_bartext=True,
        bartext_font='Arial',
        bartext_color='white',  # (255, 255, 255, 1),
        bartext_size=8,
        bartext_position='inside',
        width_mm=250,
        x_label_rotation=45,
        show_x_title=False,
        show_y_axis=False,
    )
    filepath = create_output_filepath(my_outdir, name)
    export_all_available_formats(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_density_2d_1(my_outdir, name, x, y, z):
    fig = up.plotly.density_2d(
        x=x,
        y=y,
        color='magenta',
        opacity=0.75,
        smoothing=0.2,
        show_line=True,
        line_color='rgba(255,255,255,0.5)',
        line_opacity=0.1,
        line_width=1,
        show_x_grid=True, x_grid_color='gray', x_grid_width=1,
        show_y_grid=True, y_grid_color='gray', y_grid_width=1,
        colormap='Greens',
    ) + up.plotly.scatter(x, y, color='cyan')
    filepath = create_output_filepath(my_outdir, name)
    export_all_available_formats(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_density_scatter_histogram_2d_1(my_outdir, name, x, y, z):
    fig = up.plotly.density_scatter_histogram_2d(
        x=x,
        y=y,
        colormap='Greens',
        opacity=0.5,
        show_histogram=True,
        show_density=True,
        marker_color=x,
        marker_colormap='Blues',
        marker_size=5,
        marker_opacity=1.0,
        marker_style='square',
        show_x_grid=True, x_grid_color='rgba(0, 0, 0, 0.1)', x_grid_width=2,
        show_y_grid=True, y_grid_color='rgba(0, 0, 0, 0.1)', y_grid_width=2,
    ) + up.plotly.scatter(x, y, color='cyan')
    filepath = create_output_filepath(my_outdir, name)
    export_all_available_formats(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_histogram_2d_1(my_outdir, name, x, y, z):
    fig = up.plotly.histogram_2d(
        x=x,
        y=y,
        opacity=1.0,
        colormap='Greens',
        show_colormap=True,
        bin_x_number=11,
    ) + up.plotly.scatter(x, y, color='cyan')
    filepath = create_output_filepath(my_outdir, name)
    export_all_available_formats(fig, filepath)


@pytest.mark.parametrize('name, x, y, z', TESTDATA)
def test_scatter_3d(name, x, y, z):
    up.plotly.scatter_3d(
        x=x,
        y=y,
        z=z,
        axis_aspect_ratio=(1, 1, 0.75),
        # show_interpolation_delaunay=True,
        show_interpolation_allrounder=True,
        # show_interpolation_rbf=True,
        # show_interpolation_spline=True,
        opacity=1.0,
        color=[x, 'black'],
        colormap=['Viridis', 'Hot'],
        marker_color=[x, y],
        marker_opacity=0.5,
        show_line=True,
        line_color=['rgba(0,0,0,0.1)', 'rgba(0,255,255,0.05)'],
        show_stem_x=True,
        show_stem_y=True,
        show_stem_z=True,
        stem_shift_factor=0.3,
        show_stem_line=True,
    )

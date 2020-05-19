import os

import pytest
from PIL import Image as pil_image

import unified_plotting as up


# Shared

WIDTH_MM_DEFAULT = up.config.settings.width_mm
HEIGHT_MM_DEFAULT = up.config.settings.height_mm
DPI_DEFAULT = up.config.settings.dpi
X = list(range(5))
Y = [val**2 - val for val in X]
Z = [-val**2 + 2*val for val in X]
MPL_METHODS_AND_DATA = [
    # 2d
    ['hexbin', dict(x=X, y=Y)],
    ['histogram_2d', dict(x=X, y=Y)],
    ['scatter', dict(x=X, y=Y)],
    # 3d
    ['contour', dict(x=X, y=Y, z=Z)],
    ['scatter_3d', dict(x=X, y=Y, z=Z)],
    # nd
    ['box', dict(data=[X, Y, Z])],
    ['histogram', dict(data=[X, Y, Z])],
    ['scatter_matrix', dict(data=[X, Y, Z])],
    ['violin', dict(data=[X, Y, Z])],
]
PLOTLY_METHODS_AND_DATA_and_data = [
    # 2d
    ['bar', dict(x=X, y=Y)],
    ['density_2d', dict(x=X, y=Y)],
    ['density_scatter_histogram_2d', dict(x=X, y=Y)],
    ['histogram_2d', dict(x=X, y=Y)],
    ['scatter', dict(x=X, y=Y)],
    # 3d
    ['contour', dict(x=X, y=Y, z=Z)],
    ['heatmap', dict(x=X, y=Y, z=Z)],
    ['scatter_3d', dict(x=X, y=Y, z=Z)],
    ['surface', dict(x=X, y=Y, z=Z)],
    # nd
    ['band', dict(data=[X, Y, Z])],
    ['box', dict(data=[X, Y, Z])],
    ['density', dict(data=[X, Y, Z])],
    ['histogram', dict(data=[X, Y, Z])],
    ['parallel_coordinates', dict(data=[X, Y, Z])],
    ['scatter_matrix', dict(data=[X, Y, Z])],
    ['violin', dict(data=[X, Y, Z])],
    # financial
    ['candlestick', dict(x=X, open=Y, high=Y, low=Z, close=Z)],
    ['ohlc', dict(x=X, open=Y, high=Y, low=Z, close=Z)],
]


def check_size_and_resolution(filepath, fig, expected_dpi, expected_width_mm, expected_height_mm,
                              image_format):
    # Export image
    export_method_name = 'export_{}'.format(image_format)
    export_method = getattr(fig, export_method_name)
    used_filepath = export_method(filepath)
    assert os.path.isfile(used_filepath)

    # Analyze exported image
    # - pdf and svg cannot be accessed with pillow
    # - TODO: eps and ps result in wrong sizes, probably due to embedding in a "page", not sure
    if image_format not in ['eps', 'pdf', 'ps', 'svg']:
        # Open image with Pillow to check its width, height and dpi
        img = pil_image.open(used_filepath)
        width = img.width
        height = img.height
        # if dpi is not contained in metadata, the expected dpi is used (effectively no check)
        width_dpi, height_dpi = img.info.get('dpi', [expected_dpi]*2)
        # Comparison
        assert width_dpi == expected_dpi
        assert height_dpi == expected_dpi
        assert width == int(expected_width_mm / 25.4 * expected_dpi)
        assert height == int(expected_height_mm / 25.4 * expected_dpi)


def compare_html_export_when_size_is_changed(filepath, fig):
    # Size 1
    fig.set_size(width_mm=321, height_mm=324, dpi=432)
    used_filepath = fig.export_html(filepath)
    size1 = os.path.getsize(used_filepath)
    # Size 2
    fig.set_size(width_mm=41, height_mm=42, dpi=43)
    used_filepath = fig.export_html(filepath)
    size2 = os.path.getsize(used_filepath)
    # Comparison
    assert size1 != size2


def check_data_url(fig, image_format):
    fig.set_size(width_mm=50, height_mm=50, dpi=20)
    prop_name = '{}_data_url'.format(image_format)
    data_url = getattr(fig, prop_name)
    assert isinstance(data_url, str)


def compare_data_urls_when_size_is_changed(fig, image_format):
    prop_name = '{}_data_url'.format(image_format)
    # Size 1
    fig.set_size(width_mm=200, height_mm=200, dpi=200)
    data_url = getattr(fig, prop_name)
    assert isinstance(data_url, str)
    size1 = len(data_url)
    # Size 2
    fig.set_size(width_mm=50, height_mm=50, dpi=20)
    data_url = getattr(fig, prop_name)
    assert isinstance(data_url, str)
    size2 = len(data_url)
    # Comparison
    assert size1 > size2


# Manual tests

# All image generation features of figure objects
# - Test protocol
#   1. Set explicit width, height, margins in inch and font sizes as numbers (pt)
#   2. Generate images in all ways (export_..., display in Jupyter, export_html and download)
#   3. Load all results into Inkscape, scale them to width in inch
#   4. Check with rectangles if margins are correct and with text if all font sizes are correct.
#   5. Check with rectangles if marker size means height measured in points (as font size),
#      e.g. a "j" written in font size 30 should be as high as a point with marker_size 30.
#      Same for line width and other plot elements with numerically specified size.
#   6. Use Jupyter notebook with a markdown cell to see if size units fit to HTML behavior
#      A horizontal bar: <div style="background-color: red; width: 5in; height: 0.5in;"></div>
#   7. Use pillow (PIL) to load image and check if the number of pixels along width and height
#      fit to width_in, height_in and dpi values.
# - Results
#   - With font "Sans", Plotly uses "sans-serif" and Matplotlib "Arial", which look different
#   - Matplotlib writes DPI metadata into files, hence they can be imported in correct size
#     into Inkscape, while Plotly does not and images need to be manually scaled.
#   - Matplotlib uses square root of marker size, so that doubling the number results in
#     double the area instead of double the height. I corrected for it, so that Matplotlib
#     and Plotly give the same results, where the given number for marker size or line width
#     means height or width in points (1in = 72pt) and therefore has the same unit as font size.


# Automatic tests

@pytest.mark.parametrize('image_format', ['eps', 'pdf', 'png', 'ps', 'svg'])
def test_export_img_resolution_matplotlib(my_outdir, image_format):
    for method_name, data in MPL_METHODS_AND_DATA:
        method = getattr(up.matplotlib, method_name)
        # Reset config to defaults
        up.config.load_defaults()
        # Default image size
        fig = method(**data)
        filepath = os.path.join(my_outdir, 'matplotlib_resolution_def_{}'.format(method_name))
        check_size_and_resolution(
            filepath, fig, DPI_DEFAULT, WIDTH_MM_DEFAULT, HEIGHT_MM_DEFAULT, image_format)
        # Chosen image size
        # 1) Via function arguments
        dpi_spec = 50
        width_mm_spec = 140
        height_mm_spec = 120
        fig = method(**data, dpi=dpi_spec, width_mm=width_mm_spec, height_mm=height_mm_spec)
        filepath = os.path.join(
            my_outdir, 'matplotlib_resolution_140mm_120mm_{}'.format(method_name))
        check_size_and_resolution(
            filepath, fig, dpi_spec, width_mm_spec, height_mm_spec, image_format)
        # 2) Via config setting
        dpi_spec, width_in_spec, height_in_spec = 120, 4, 2
        width_mm_spec = width_in_spec * 25.4
        height_mm_spec = height_in_spec * 25.4
        up.config.settings.dpi = dpi_spec
        up.config.settings.width_mm = None
        up.config.settings.height_mm = None
        up.config.settings.width_in = width_in_spec
        up.config.settings.height_in = height_in_spec
        fig = method(**data)
        filepath = os.path.join(my_outdir, 'matplotlib_resolution_4in_2in_{}'.format(method_name))
        check_size_and_resolution(
            filepath, fig, dpi_spec, width_mm_spec, height_mm_spec, image_format)
        if image_format in ['pdf']:
            # Data URL without size comparison
            prop_name = '{}_data_url'.format(image_format)
            data_url = getattr(fig, prop_name)
            assert isinstance(data_url, str)
        else:
            # Data URLs with size comparison
            compare_data_urls_when_size_is_changed(fig, image_format)
        # Reset config to defaults
        up.config.load_defaults()


def test_export_html_matplotlib(my_outdir):
    for method_name, data in MPL_METHODS_AND_DATA:
        method = getattr(up.matplotlib, method_name)
        up.config.load_defaults()
        fig = method(**data)
        filepath = os.path.join(my_outdir, 'matplotlib_resolution_def_{}'.format(method_name))
        compare_html_export_when_size_is_changed(filepath, fig)

    # Reset config to defaults (otherwise it might have influence on other tests)
    up.config.load_defaults()


def test_text_representations_matplotlib():
    fig = up.matplotlib.scatter_3d(X, Y, Z, dpi=50)

    # Language
    for prop_name in ['svg_text', 'html_text']:
        prop = getattr(fig, prop_name)
        assert isinstance(prop, str)
        assert len(prop) > 100

    # Data URLs
    for img_format in ['png', 'svg', 'eps', 'pdf', 'ps']:
        prop_name = '{}_data_url'.format(img_format)
        prop = getattr(fig, prop_name)
        assert isinstance(prop, str)
        assert len(prop) > 100

    # HTML elements with data URLs
    for img_format in ['png', 'svg']:
        prop_name = '{}_img_element'.format(img_format)
        prop = getattr(fig, prop_name)
        assert isinstance(prop, str)
        assert len(prop) > 100

    for img_format in ['eps', 'pdf', 'ps']:
        prop_name = '{}_object_element'.format(img_format)
        prop = getattr(fig, prop_name)
        assert isinstance(prop, str)
        assert len(prop) > 100


def test_display_matplotlib():
    fig = up.matplotlib.scatter_3d(X, Y, Z, dpi=50)
    assert fig._display_format == 'png'

    displayed_texts = []
    for fmt in ['eps', 'pdf', 'png', 'ps', 'svg']:
        fig.set_display_format(fmt)
        assert fig._display_format == fmt
        html_text = fig._repr_html_()
        assert len(html_text) > 0
        displayed_texts.append(html_text)
    assert len(displayed_texts) == len(set(displayed_texts))

    with pytest.raises(ValueError):
        fig.set_display_format('webp')

    with pytest.raises(ValueError):
        fig._display_format = 'nonsense'
        fig._repr_html_()


@pytest.mark.parametrize('image_format', ['eps', 'jpg', 'pdf', 'png', 'svg', 'webp'])
def test_export_img_resolution_plotly(my_outdir, image_format):
    for method_name, data in PLOTLY_METHODS_AND_DATA_and_data:
        method = getattr(up.plotly, method_name)
        # Default image size
        fig = method(**data)
        filepath = os.path.join(my_outdir, 'plotly_resolution_def_{}'.format(method_name))
        check_size_and_resolution(
            filepath, fig, DPI_DEFAULT, WIDTH_MM_DEFAULT, HEIGHT_MM_DEFAULT, image_format)
        # Chosen image size
        dpi_spec = 50
        width_mm_spec = 140
        height_mm_spec = 120
        fig = method(**data, dpi=dpi_spec, width_mm=width_mm_spec, height_mm=height_mm_spec)
        filepath = os.path.join(
            my_outdir, 'plotly_resolution_140mm_120mm_{}'.format(method_name))
        check_size_and_resolution(
            filepath, fig, dpi_spec, width_mm_spec, height_mm_spec, image_format)
        # Compare data URL representations with different sizes
        if image_format in ['jpg', 'png']:
            compare_data_urls_when_size_is_changed(fig, image_format)
        else:
            check_data_url(fig, image_format)
        # Reset config to defaults
        up.config.load_defaults()

    # Reset config to defaults (otherwise it might have influence on other tests)
    up.config.load_defaults()


def test_export_html_plotly(my_outdir):
    for method_name, data in PLOTLY_METHODS_AND_DATA_and_data:
        method = getattr(up.plotly, method_name)
        up.config.load_defaults()
        fig = method(**data)
        filepath = os.path.join(my_outdir, 'plotly_resolution_def_{}'.format(method_name))
        compare_html_export_when_size_is_changed(filepath, fig)

    # Reset config to defaults (otherwise it might have influence on other tests)
    up.config.load_defaults()


def test_text_representations_plotly():
    fig = up.plotly.scatter_3d(X, Y, Z, dpi=100)

    # Language
    prop_names = [
        'svg_text', 'html_text', 'html_text_standalone', 'html_text_cdn', 'html_text_partial',
        'json_text']
    for prop_name in prop_names:
        prop = getattr(fig, prop_name)
        assert isinstance(prop, str)
        assert len(prop) > 100

    # Data URLs
    for img_format in ['eps', 'jpg', 'pdf', 'png', 'svg', 'webp']:
        prop_name = '{}_data_url'.format(img_format)
        prop = getattr(fig, prop_name)
        assert isinstance(prop, str)
        assert len(prop) > 100

    # HTML elements with data URLs
    for img_format in ['jpg', 'png', 'svg', 'webp']:
        prop_name = '{}_img_element'.format(img_format)
        prop = getattr(fig, prop_name)
        assert isinstance(prop, str)
        assert len(prop) > 100

    for img_format in ['eps', 'pdf']:
        prop_name = '{}_object_element'.format(img_format)
        prop = getattr(fig, prop_name)
        assert isinstance(prop, str)
        assert len(prop) > 100


def test_display_plotly():
    fig = up.plotly.scatter_3d(X, Y, Z, dpi=100)
    assert fig._display_format == 'html'

    displayed_texts = []
    for fmt in ['html', 'eps', 'jpg', 'pdf', 'png', 'svg',  'webp']:
        fig.set_display_format(fmt)
        assert fig._display_format == fmt
        html_text = fig._repr_html_()
        assert len(html_text) > 0
        displayed_texts.append(html_text)
    assert len(displayed_texts) == len(set(displayed_texts))

    with pytest.raises(ValueError):
        fig.set_display_format('ps')

    with pytest.raises(ValueError):
        fig._display_format = 'nonsense'
        fig._repr_html_()


def test_margin_size_differences_have_effect(my_outdir):
    filepath = os.path.join(my_outdir, 'margin')

    arguments = dict(
        margin_auto=True,
        margin_left_mm=51,
        margin_left_in=0.934,
        margin_left_pt=63,
        margin_left_rel=0.323,
        margin_right_mm=51,
        margin_right_in=0.934,
        margin_right_pt=63,
        margin_right_rel=0.323,
        margin_top_mm=51,
        margin_top_in=0.93,
        margin_top_pt=60,
        margin_top_rel=0.323,
        margin_bottom_mm=51,
        margin_bottom_in=0.934,
        margin_bottom_pt=63,
        margin_bottom_rel=0.323,
    )

    def set_config_to_lowest_priority():
        up.config.settings.margin_auto = False
        up.config.settings.margin_left_mm = None
        up.config.settings.margin_left_in = None
        up.config.settings.margin_left_pt = None
        up.config.settings.margin_left_rel = 0
        up.config.settings.margin_right_mm = None
        up.config.settings.margin_right_in = None
        up.config.settings.margin_right_pt = None
        up.config.settings.margin_right_rel = 0
        up.config.settings.margin_top_mm = None
        up.config.settings.margin_top_in = None
        up.config.settings.margin_top_pt = None
        up.config.settings.margin_top_rel = 0
        up.config.settings.margin_bottom_mm = None
        up.config.settings.margin_bottom_in = None
        up.config.settings.margin_bottom_pt = None
        up.config.settings.margin_bottom_rel = 0

    for func in [up.plotly.scatter]:  # TODO: up.matplotlib.scatter (no jpg support anymore)
        set_config_to_lowest_priority()
        # Chosen margin
        # 1) Via function arguments
        sizes1 = []
        for key, val in arguments.items():
            fig = func(list(range(20)), list(range(20)), **{key: val})
            used_filepath = fig.export_jpg(filepath)
            sizes1.append(os.path.getsize(used_filepath))
        assert len(sizes1) == len(set(sizes1))
        # 2) Via config setting
        sizes2 = []
        for key, val in arguments.items():
            set_config_to_lowest_priority()
            setattr(up.config.settings, key, val)
            fig = func(X, Y)
            used_filepath = fig.export_jpg(filepath)
            sizes2.append(os.path.getsize(used_filepath))
        assert len(sizes2) == len(set(sizes2))
        # Function arguments and config settings lead to same results
        # assert sizes1 == sizes2  # TODO: flaky for Plotly, not sure why

    # Reset config to defaults (otherwise it might have influence on other tests)
    up.config.load_defaults()


def test_margin_unit_equivalences(my_outdir):
    filepath = os.path.join(my_outdir, 'margin')

    equivalent_kwargs_list = [
        dict(margin_left_mm=25.4, margin_left_in=1, margin_left_pt=72,
             margin_left_rel=0.2),
        dict(margin_right_mm=25.4, margin_right_in=1, margin_right_pt=72,
             margin_right_rel=0.2),
        dict(margin_top_mm=25.4, margin_top_in=1, margin_top_pt=72,
             margin_top_rel=0.2),
        dict(margin_bottom_mm=25.4, margin_bottom_in=1, margin_bottom_pt=72,
             margin_bottom_rel=0.2),
    ]

    up.config.load_defaults()
    for func in [up.matplotlib.scatter, up.plotly.scatter]:
        for kwargs in equivalent_kwargs_list:
            print(kwargs)
            sizes = []
            for key, val in kwargs.items():
                fig = func(X, Y, width_in=5, height_in=5, margin_auto=False, **{key: val})
                used_filepath = fig.export_png(filepath)
                sizes.append(os.path.getsize(used_filepath))
            assert len(set(sizes)) <= 2  # TODO: == 1 is flaky for Plotly, not sure why

    # Reset config to defaults (otherwise it might have influence on other tests)
    up.config.load_defaults()


def test_set_size_memory(my_outdir):
    filepath = os.path.join(my_outdir, 'set_size')
    image_format = 'png'
    for func in [up.matplotlib.scatter, up.plotly.scatter]:
        width_mm_1 = 133
        fig = func(X, Y, width_mm=width_mm_1)
        check_size_and_resolution(
            filepath, fig, DPI_DEFAULT, width_mm_1, HEIGHT_MM_DEFAULT, image_format)
        # set DPI, leave width and height unchanged
        dpi_2 = 57
        fig.set_size(dpi=dpi_2)
        check_size_and_resolution(
            filepath, fig, dpi_2, width_mm_1, HEIGHT_MM_DEFAULT, image_format)
        # set height, leave dpi and width unchanged
        height_mm_3 = 131
        fig.set_size(height_mm=height_mm_3)
        check_size_and_resolution(
            filepath, fig, dpi_2, width_mm_1, height_mm_3, image_format)

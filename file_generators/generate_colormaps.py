import xml.etree.ElementTree as _xmlElementTree

import plotly.graph_objs as _go
import plotly.express as _px
import matplotlib.pyplot as _plt
import requests as _requests
from matplotlib.cm import get_cmap as _get_cmap


MATPLOTLIB_COLORMAP_NAMES = sorted(cm for cm in _plt.colormaps() if not cm.endswith('_r'))

PLOTLY_JS_COLORMAP_NAMES = [
    'Blackbody', 'Bluered', 'Blues', 'Earth', 'Cividis', 'Electric', 'Greens',
    'Greys', 'Hot', 'Jet', 'Picnic', 'Portland', 'Rainbow', 'RdBu', 'Reds',
    'Viridis', 'YlGnBu', 'YlOrRd']

PLOTLY_COLORMAP_NAMES = []
for plotly_py_cm in sorted(_px.colors.named_colorscales()):
    for plotly_js_cm in PLOTLY_JS_COLORMAP_NAMES:
        if plotly_py_cm.lower() == plotly_js_cm.lower():
            PLOTLY_COLORMAP_NAMES.append(plotly_js_cm)
            break
    else:
        PLOTLY_COLORMAP_NAMES.append(plotly_py_cm)

D3_COLORMAP_NAMES = [
    'Blues', 'Greens', 'Greys', 'Oranges', 'Purples', 'Reds', 'Turbo', 'Viridis', 'Inferno',
    'Magma', 'Plasma', 'Cividis', 'Warm', 'Cool', 'Cubehelix', 'BuGn', 'BuPu', 'GnBu', 'OrRd',
    'PuBuGn', 'PuBu', 'PuRd', 'RdPu', 'YlGnBu', 'YlGn', 'YlOrBr', 'YlOrRd', 'BrBG', 'PRGn',
    'PiYG', 'PuOr', 'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral', 'Rainbow', 'Sinebow',
]
MAIN_COLORMAP_SET = set(cm.lower() for cm in MATPLOTLIB_COLORMAP_NAMES + PLOTLY_COLORMAP_NAMES)


# Imports deliberately after previous section to prevent registrations to Matplotlib colormaps
import cmasher as _cmr
import cmocean as _cmo
import colorcet as _cet
CMASHER_COLORMAP_NAMES = sorted(
    name for name in dir(_cmr.cm)
    if not name.startswith('__') and not name.endswith('_r') and not name.startswith('cmap_'))
CMOCEAN_COLORMAP_NAMES = sorted(_cmo.cm.cmapnames)
COLORCET_COLORMAP_NAMES = sorted(_cet.all_original_names())


def list_colormap_names(txl, colormap_names, target_variable):
    txl.append('{} = {{'.format(target_variable))
    for cm_name in colormap_names:
        if not cm_name.endswith('_r'):
            txl.append("    '{}': '{}',".format(cm_name.lower(), cm_name))
    txl.append('}')


def list_matplotlib_definitions_for_plotly(txl):
    num_colors = 256
    txl.append('    # Matplotlib colormaps converted for Plotly')
    excluded_lower = set(cm_name.lower() for cm_name in PLOTLY_COLORMAP_NAMES)
    for colormap_name in MATPLOTLIB_COLORMAP_NAMES:
        if colormap_name.lower() not in excluded_lower:
            cmap = _get_cmap(colormap_name)
            step_size = 1.0 / (num_colors - 1)
            txl.append("    '{}': [".format(colormap_name.lower()))
            for i in range(num_colors):
                normed_float = round(i * step_size, 5)
                rgb_list = [int(val * 255.0) for val in cmap(normed_float)[:3]]
                rgb_str = 'rgb({},{},{})'.format(*rgb_list)
                color = [normed_float, rgb_str]
                txl.append('        {},'.format(color))
            txl.append('    ],')


def list_plotly_definitions_for_matplotlib(txl):
    # https://matplotlib.org/api/_as_gen/matplotlib.colors.LinearSegmentedColormap.html#matplotlib.colors.LinearSegmentedColormap.from_list
    def convert_rgb_str_to_list(val, color):
        try:
            red, green, blue = [int(item) for item in color[4:-1].split(',')]
        except Exception:
            assert color.startswith('#') and len(color) == 7
            hex_str = color[1:]
            red, green, blue = [int(hex_str[i: i+2], 16) for i in (0, 2, 4)]
        mpl_color = (val, [red/255.0, green/255.0, blue/255.0, 1.0])  # (value, color) tuple
        return mpl_color

    txl.append('    # Plotly colormaps converted for Matplotlib')
    excluded_lower = set(cm_name.lower() for cm_name in MATPLOTLIB_COLORMAP_NAMES)
    for colormap_name in PLOTLY_COLORMAP_NAMES:
        if colormap_name.lower() not in excluded_lower:
            fig = _go.Histogram2d(x=[1, 2], y=[1, 2], colorscale=colormap_name)
            txl.append("    '{}': [".format(colormap_name.lower()))
            for val, color in fig['colorscale']:
                txl.append('        {},'.format(convert_rgb_str_to_list(val, color)))
            txl.append('    ],')


def list_cmocean_definitions(txl, target):
    """cmocean colormaps

    References
    ----------
    - https://matplotlib.org/cmocean

    """
    if target == 'Plotly':
        txl.append('    # cmocean colormaps converted for Plotly')

        def convert_cm_element(rgba, color_counter, num_colors):
            def to_0_255(given):
                result = int(round(given * 255.0))
                if result < 0:
                    result = 0
                elif result > 255:
                    result = 255
                return result

            red, green, blue, _ = rgba
            rgb_255_str = 'rgb({},{},{})'.format(to_0_255(red), to_0_255(green), to_0_255(blue))
            position = color_counter / (num_colors - 1)  # requirement: first is 0.0, last is 1.0
            return "[{}, '{}']".format(position, rgb_255_str)
    elif target == 'Matplotlib':
        txl.append('    # cmocean colormaps converted for Matplotlib')

        def convert_cm_element(rgba, color_counter, num_colors):
            return rgba
    else:
        raise ValueError('target needs to be Plotly or Matplotlib.')

    # Conversion
    num_colors = 256  # needs to be 256, otherwise cropped colormap
    for cm_name in CMOCEAN_COLORMAP_NAMES:
        cm = getattr(_cmo.cm, cm_name)
        txl.append("    'cmo.{}': [".format(cm_name.lower()))
        for color_counter in range(256):
            rgba = cm(color_counter)
            color = convert_cm_element(rgba, color_counter, num_colors)
            txl.append("        {},".format(color))
        txl.append('    ],')


def list_cmasher_definitions(txl, target):
    """Print CMasher colormap definitions

    References
    ----------
    - https://cmasher.readthedocs.io
    - https://github.com/1313e/CMasher/blob/master/cmasher/colormaps/amber/amber.py

    """
    # _cmr.create_cmap_overview()

    # Argument processing
    if target == 'Plotly':
        txl.append('    # CMasher colormaps converted for Plotly')

        def to_0_255(given):
                result = int(round(given * 255.0))
                if result < 0:
                    result = 0
                elif result > 255:
                    result = 255
                return result

        def convert_cm_element(line, i, num_colors):
            red, green, blue = line
            rgb_255_str = 'rgb({},{},{})'.format(to_0_255(red), to_0_255(green), to_0_255(blue))
            position = color_counter / (num_colors - 1)  # requirement: first is 0.0, last is 1.0
            return "[{}, '{}']".format(position, rgb_255_str)
    elif target == 'Matplotlib':
        txl.append('    # CMasher colormaps converted for Matplotlib')

        def convert_cm_element(line, i, num_colors):
            red, green, blue = line
            return [red, green, blue, 1.0]
    else:
        raise ValueError('target needs to be Plotly or Matplotlib.')

    # Conversion
    use_only_half = set(['fusion', 'iceburn', 'redshift', 'waterlily'])
    use_only_minimal = set(['neutral'])
    for cm_name in CMASHER_COLORMAP_NAMES:
        cm = getattr(_cmr, cm_name).colors
        txl.append("    'cmr.{}': [".format(cm_name.lower()))
        num_colors = len(cm)
        for color_counter, line in enumerate(cm):
            if cm_name.lower() in use_only_half:
                # Reduce number of colormap entries to prevent Plotly bugs (e.g. in surface plots)
                if color_counter % 2 != 0 and color_counter != (num_colors-1):
                    continue
            elif cm_name.lower() in use_only_minimal:
                # Reduce number of colormap entries to prevent Plotly bugs (e.g. in surface plots)
                if color_counter % 11 != 0 and color_counter != (num_colors-1):
                    continue
            color = convert_cm_element(line, color_counter, num_colors)
            txl.append("        {},".format(color))
        txl.append('    ],')


def list_colorcet_definitions(txl, target):
    """Print colorcet colormap definitions

    References
    ----------
    - https://colorcet.holoviz.org
    - https://github.com/holoviz/colorcet

    """
    # Argument processing
    if target == 'Plotly':
        txl.append('    # colorcet colormaps converted for Plotly')

        def to_0_255(given):
                result = int(round(given * 255.0))
                if result < 0:
                    result = 0
                elif result > 255:
                    result = 255
                return result

        def convert_cm_element(line, i, num_colors):
            red, green, blue = line
            rgb_255_str = 'rgb({},{},{})'.format(to_0_255(red), to_0_255(green), to_0_255(blue))
            position = color_counter / (num_colors - 1)  # requirement: first is 0.0, last is 1.0
            return "[{}, '{}']".format(position, rgb_255_str)
    elif target == 'Matplotlib':
        txl.append('    # colorcet colormaps converted for Matplotlib')

        def convert_cm_element(line, i, num_colors):
            red, green, blue = line
            return [red, green, blue, 1.0]
    else:
        raise ValueError('target needs to be Plotly or Matplotlib.')

    # Conversion
    for cm_name in COLORCET_COLORMAP_NAMES:
        cm = getattr(_cet, cm_name)
        txl.append("    'cet.{}': [".format(cm_name.lower()))
        num_colors = len(cm)
        for color_counter, line in enumerate(cm):
            color = convert_cm_element(line, color_counter, num_colors)
            txl.append("        {},".format(color))
        txl.append('    ],')


def list_sciviscolor_definitions(txl, target):
    """Print SciVisColor colormap definitions

    References
    ----------
    - https://sciviscolor.org/home/colormaps

    """
    # Argument processing
    if target == 'Plotly':
        txl.append('    # sciviscolor colormaps converted for Plotly')

        def to_0_255(given):
                result = int(round(given * 255.0))
                if result < 0:
                    result = 0
                elif result > 255:
                    result = 255
                return result

        def convert_cm_element(line):
            position, (red, green, blue) = line
            rgb_255_str = 'rgb({},{},{})'.format(to_0_255(red), to_0_255(green), to_0_255(blue))
            return "[{}, '{}']".format(position, rgb_255_str)
    elif target == 'Matplotlib':
        txl.append('    # sciviscolor colormaps converted for Matplotlib')

        def convert_cm_element(line):
            # https://matplotlib.org/api/_as_gen/matplotlib.colors.LinearSegmentedColormap.html#matplotlib.colors.LinearSegmentedColormap.from_list
            position, (red, green, blue) = line
            return (position, [red, green, blue, 1.0])  # (value, color) tuple
    else:
        raise ValueError('target needs to be Plotly or Matplotlib.')

    urls_and_names = [
        # https://sciviscolor.org/home/colormaps/v2_colorsacles/
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/blue-1.xml', 'blue1'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/blue-2.xml', 'blue2'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/blue-3.xml', 'blue3'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/not-blue-4.xml', 'blue4'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/blue-5.xml', 'blue5'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/blue-6.xml', 'blue6'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/blue-7.xml', 'blue7'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/blue-8.xml', 'blue8'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/blue-9.xml', 'blue9'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/blue-10.xml', 'blue10'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/blue-11.xml', 'blue11'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/brown-1.xml', 'brown1'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/brown-2.xml', 'brown2'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/brown-3.xml', 'brown3'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/brown-4.xml', 'brown4'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/brown-5.xml', 'brown5'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/brown-6.xml', 'brown6'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/brown-7.xml', 'brown7'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/brown-8.xml', 'brown8'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/brown-9.xml', 'brown9'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/red-1.xml', 'red1'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/red-2.xml', 'red2'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/red-3.xml', 'red3'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/red-4.xml', 'red4'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/maroon-5.xml', 'maroon'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/purple-6.xml', 'purple1'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/purple-7.xml', 'purple2'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/purple-8.xml', 'purple3'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/green-1.xml', 'green1'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/green-2.xml', 'green2'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/green-3.xml', 'green3'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/green-4.xml', 'green4'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/green-5.xml', 'green5'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/not-green-6.xml', 'green6'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/green-7.xml', 'green7'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/green-8.xml', 'green8'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/yellow-1.xml', 'yellow1'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/yellow-2.xml', 'yellow2'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/yellow-3.xml', 'yellow3'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/orange-4.xml', 'orange1'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/orange-5.xml', 'orange2'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/orange-6.xml', 'orange3'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/yellow-7.xml', 'yellow4'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/yellow-8.xml', 'yellow5'),
        # https://sciviscolor.org/home/colormaps/contrasting-divergent-colormaps/
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/blue-orange-div.xml',
         'div-blue-orange'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/gray-gold.xml',
         'div-gray-gold'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/green-brown-div.xml',
         'div-green-brown'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/turqoise-olive.xml',
         'div-turqoise-olive'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/asym-orange-blue.xml',
         'div-orange-blue'),
        # https://sciviscolor.org/home/colormaps/rainbow-alternatives/
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/mellow-rainbow.xml',
         'rainbow-mellow'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/5-step-melow-wave.xml',
         'rainbow-mellow-wave'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/pale-sat-blue-rainbow.xml',
         'rainbow-blue'),
        # https://sciviscolor.org/home/colormaps/765-2/
        # https://sciviscolor.org/wave-colormaps/
        # 3 Wave Colormaps
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/3wave-bgYr.odt',
         '3wave-blue-green-red'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/3wave-bGrBr.odt',
         '3wave-blue-gray-brown'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/12/3w_gby.odt',
         '3wave-gray-brown-yellow'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/3W_muted_a01.xml',
         '3wave-brown-to-green'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/10/3wave-yellow-grey-blue.xml',
         '3wave-red-gray-blue'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/12/3w_gGB.odt',
         '3wave-gray-green-blue'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/12/3w_gBg.odt',
         '3wave-gray-blue-gray'),
        # 4 Wave Colormaps
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/4Wmed8.odt',
         '4wave-blue-to-red'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/4wave-bgyGr.odt',
         '4wave-blue-to-gray'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/12/4w_bgby.odt',
         '4wave-blue-to-yellow'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/12/yellow-green-teal-gray.odt',
         '4wave-yellow-green-gray'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/orange-green-blue-gray.xml',
         '4wave-orange-green-gray'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/12/4w_bgTR.odt',
         '4wave-gray-blue-red'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/12/4w_ROTB.odt',
         '4wave-red-blue'),
        # 5 Wave Colormaps
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/5-wave-yellow-to-blue.xml',
         '5wave-yellow-to-blue'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/10/5wave-yellow-brown-blue.xml',
         '5wave-yellow-brown-blue'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/5-wave-yellow-green.xml',
         '5wave-yellow-and-green'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/12/5w_BRgpb.odt',
         '5wave-blue-red-blue'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/5-wave-orange-to-green.xml',
         '5wave-orange-to-green'),
        # https://sciviscolor.org/highlight-insert-colormaps/
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/gr-insert_0-10.odt',
         'insert-green-0-10'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/gr-insert_10-20.odt',
         'insert-green-10-20'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/gr-insert_20-30.odt',
         'insert-green-20-30'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/gr-insert_30-40.odt',
         'insert-green-30-40'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/gr-insert_40-50.odt',
         'insert-green-40-50'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/gr-insert_50-60.odt',
         'insert-green-50-60'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/gr-insert_60-70.odt',
         'insert-green-60-70'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/gr-insert_70-80.odt',
         'insert-green-70-80'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/gr-insert_80-90.odt',
         'insert-green-80-90'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/gr-insert_90-100.odt',
         'insert-green-90-100'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/0-20-green-inset.xml',
         'insert-green-0-20'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/20-40-green-inset.xml',
         'insert-green-20-40'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/40-60-green-inset.xml',
         'insert-green-40-60'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/60-80-green-inset.xml',
         'insert-green-60-80'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/80-100-green-inset.xml',
         'insert-green-80-100'),
        # https://sciviscolor.org/outlier-focused-colormaps/
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/outl-5.odt',
         'outlier-gray-5'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/outl-10.odt',
         'outlier-gray-10'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/outl-15.odt',
         'outlier-gray-15'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/outl-20.odt',
         'outlier-gray-20'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/outl-25.odt',
         'outlier-gray-25'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/blue-green-sat-on-ends.xml',
         'outlier-green-blue'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/12/4Ew_GgbB.odt',
         'outlier-green-blue-2'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/12/4Ew_BbpR.odt',
         'outlier-blue-red'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2018/07/blue-red-sat-inner.odt',
         'outlier-blue-red-middle'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/12/4Sw_bgbB.odt',
         'outlier-brown-gray-blue'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/12/3Sw_bRp.odt',
         'outlier-brown-orange'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/12/3Sw_gRb.odt',
         'outlier-blue-orange'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/orange-turquoise-div-inset.xml',
         'outlier-orange-turqoise'),
        # https://sciviscolor.org/home/colormaps/813-2/
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/7-section-muted.xml',
         'discrete-7'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/5-discrete-gr-ye-rd-dark.xml',
         'discrete-5-dark'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/5-section-muted-autumn.xml',
         'discrete-5-autumn'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/4-section-light-autumn.xml',
         'discrete-4-light'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/4-section-blue-orange.xml',
         'discrete-4-blue-orange'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/4-discrete-blue-green.xml',
         'discrete-4-blue-green'),
        ('https://sciviscolor.org/wp-content/uploads/sites/14/2017/09/4-section-discrete-vanEyck.xml',
         'discrete-4-van-eyck'),
    ]

    # Conversion
    def url_to_xml_text(url):
        response = _requests.get(url)
        xml_text = response.text
        return xml_text

    def xml_text_to_colormap(xml_text):
        root = _xmlElementTree.fromstring(xml_text)
        colormap = []
        for elem in root.iter():
            if elem.tag == 'Point':
                dictionary = elem.attrib
                pos, red, green, blue, _ = [float(dictionary[letter]) for letter in 'xrgbo']
                colormap.append([pos, [red, green, blue]])
        return colormap

    for url, cm_name in urls_and_names:
        try:
            cmap = xml_text_to_colormap(url_to_xml_text(url))
        except Exception as excp:
            txl.append(url, 'FAILED:', excp)
            continue

        # Corrections
        # - Sort
        cmap = sorted(cmap, key=lambda item: item[0])
        # - Remove duplicates
        duplicates = set(i for i in range(len(cmap)) if cmap[i][0] == cmap[i-1][0])
        cmap = [item for i, item in enumerate(cmap) if i not in duplicates]
        # Insert 0.0 or 1.0 if missing (otherwise Plotly uses default colormap without warning)
        if cmap[0][0] != 0.0:
            start = cmap[0].copy()
            start[0] = 0.0
            cmap.insert(0, start)
        if cmap[-1][0] != 1.0:
            end = cmap[-1].copy()
            end[0] = 1.0
            cmap.append(end)

        txl.append("    'svc.{}': [".format(cm_name.lower()))
        for line in cmap:
            color = convert_cm_element(line)
            txl.append("        {},".format(color))
        txl.append('    ],')


def export_colormaps_as_python_file(filepath):
    # This function takes ~4min and fetches data from the web
    # Create a text list (txl)
    txl = []
    txl.append('# Plotly builtin colormaps (state: v2.5.0)')
    txl.append('# - https://plot.ly/python/builtin-colorscales/')
    txl.append('# - https://github.com/plotly/plotly.js/blob/master/src/components/colorscale/scales.js')
    list_colormap_names(txl, PLOTLY_COLORMAP_NAMES, 'PLOTLY_BUILTIN_COLORMAPS')
    txl.append('')

    txl.append('# Matplotlib builtin colormaps (state: v3)')
    list_colormap_names(txl, MATPLOTLIB_COLORMAP_NAMES, 'MATPLOTLIB_BUILTIN_COLORMAPS')
    txl.append('')

    txl.append('# D3 builtin colormaps')
    list_colormap_names(txl, D3_COLORMAP_NAMES, 'D3_BUILTIN_COLORMAPS')
    txl.append('')

    txl.append('# Plotly custom colormaps')
    txl.append('PLOTLY_EXTERNAL_COLORMAPS = {')
    list_matplotlib_definitions_for_plotly(txl)
    list_cmasher_definitions(txl, 'Plotly')
    list_cmocean_definitions(txl, 'Plotly')
    list_colorcet_definitions(txl, 'Plotly')
    list_sciviscolor_definitions(txl, 'Plotly')
    txl.append('}')
    txl.append('')

    txl.append('# Matplotlib custom colormaps')
    txl.append('MATPLOTLIB_EXTERNAL_COLORMAPS = {')
    list_plotly_definitions_for_matplotlib(txl)
    list_cmasher_definitions(txl, 'Matplotlib')
    list_cmocean_definitions(txl, 'Matplotlib')
    list_colorcet_definitions(txl, 'Matplotlib')
    list_sciviscolor_definitions(txl, 'Matplotlib')
    txl.append('}')

    # Export the text
    text = '\n'.join(txl)
    with open(filepath, 'w') as file_handle:
        file_handle.write(text)


print('Generating colormaps and python file')
export_colormaps_as_python_file('colormaps.py')

import os as _os

import matplotlib.pyplot as _plt
import numpy as _np
from matplotlib.colors import LinearSegmentedColormap as _LinearSegmentedColormap

import unified_plotting as up
from unified_plotting._unified_arguments import colormaps as _colormaps


def generate_colormap_image(given_colormap, width, height):
    gradient = _np.linspace(0, 1, 256)
    gradient = _np.vstack((gradient, gradient))
    fig, ax = _plt.subplots()
    fig.set_size_inches(width/72, height/72)
    if isinstance(given_colormap, str):
        cmap = _plt.get_cmap(given_colormap)
    else:
        cmap = _LinearSegmentedColormap.from_list(name='a', colors=given_colormap)
    ax.imshow(gradient, cmap=cmap, aspect='auto')
    ax.set_axis_off()
    fig = up.matplotlib.Figure(
        fig, width_mm=width, height_mm=height,
        margin_bottom_mm=0, margin_top_mm=0, margin_left_mm=0, margin_right_mm=0)
    return fig.png_img_element


def export_colormap_images(width, height):
    # https://matplotlib.org/2.0.2/examples/color/colormaps_reference.html
    all_colormaps = list(_colormaps.MATPLOTLIB_BUILTIN_COLORMAPS.items()) + \
        list(_colormaps.MATPLOTLIB_EXTERNAL_COLORMAPS.items())
    gradient = _np.linspace(0, 1, 256)
    gradient = _np.vstack((gradient, gradient))
    for key, val in all_colormaps:
        fig, ax = _plt.subplots()
        fig.set_size_inches(width/72, height/72)
        if isinstance(val, str):
            cmap = _plt.get_cmap(val)
        else:
            cmap = _LinearSegmentedColormap.from_list(name='a', colors=val)
        ax.imshow(gradient, cmap=cmap, aspect='auto')
        ax.set_axis_off()
        fig.savefig(
            fname='colormaps/{}.png'.format(key),
            dpi=72,
            format='png',
            bbox_inches='tight', pad_inches=0
        )
        fig.clear()


def export_rst_text(filepath, width, height):
    fig_template = """- {name}

  .. raw:: html

     {img_text}
"""
    txl = []
    txl.append('.. _colormap-list:')
    txl.append('')
    txl.append('Colormaps')
    txl.append('#########')
    txl.append('')
    txl.append('The following list is sorted in a hierarchy with two levels:')
    txl.append('')
    txl.append('1. by source of the colormap: built-in and external ones')
    txl.append('2. by alphabetical order of the colormap names')
    txl.append('')
    txl.append(
        'Note that it is currently not considered whether a colormap is sequential, '
        'diverging or categorical, which may lead to a visual impression of disorder.')
    txl.append('')
    txl.append('')
    header = 'Built-in colormaps of Matplotlib and Plotly'
    txl.append(header)
    txl.append('='*len(header))
    txl.append('')
    all_colormaps = {
        **_colormaps.MATPLOTLIB_BUILTIN_COLORMAPS,
        **_colormaps.MATPLOTLIB_EXTERNAL_COLORMAPS,
    }
    builtin_colormaps = set(_colormaps.MATPLOTLIB_BUILTIN_COLORMAPS).union(
        set(_colormaps.PLOTLY_BUILTIN_COLORMAPS))

    def img_to_text(given):
        return '<p style="margin-top:-5pt;margin-bottom:1ex;">' + given + '</p>'

    for cm_name in sorted(builtin_colormaps):
        cm = all_colormaps[cm_name]
        img_text = img_to_text(generate_colormap_image(cm, width, height))
        txl.append(fig_template.format(name=cm_name, img_text=img_text))

    def ext(txl, name, prefix):
        header = 'External colormaps provided by {}'.format(name)
        txl.append('')
        txl.append(header)
        txl.append('='*len(header))
        for cm_name in sorted(_colormaps.MATPLOTLIB_EXTERNAL_COLORMAPS):
            if cm_name.startswith(prefix):
                cm = all_colormaps[cm_name]
                img_text = img_to_text(generate_colormap_image(cm, width, height))
                txl.append(fig_template.format(name=cm_name, img_text=img_text))

    ext(txl, 'Colorcet', 'cet.')
    ext(txl, 'CMasher', 'cmr.')
    ext(txl, 'cmocean', 'cmo.')
    ext(txl, 'SciVisColor', 'svc.')

    text = '\n'.join(txl)
    with open(filepath, 'w') as file_handle:
        file_handle.write(text)


DIRPATH = 'doc'
_os.makedirs(DIRPATH, exist_ok=True)

# now images are embedded directly in rst instead of using image files
#print('Generating doc images')
#DIRPATH = _os.path.join('doc', 'colormaps')
#export_colormap_images(DIRPATH, width=700, height=25)

print('Generating doc text')
FILEPATH = _os.path.join('doc', 'colormaps.rst')
export_rst_text(FILEPATH, 150, 7)

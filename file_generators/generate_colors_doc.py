import os as _os

import named_colors as _named_colors


def export_color_images(color_dict, dirpath, width, height):
    _os.makedirs(dirpath, exist_ok=True)
    for color_name, color_hex in color_dict.items():
        # SVG
        x_rect = 0
        y_rect = 0
        width_rect = width
        height_rect = height
        svg_text = (
            '<svg xmlns="http://www.w3.org/2000/svg">'
            '<rect x="{}" y="{}" width="{}" height="{}" style="fill:{};" />'
            '</svg>'
        ).format(x_rect, y_rect, width_rect, height_rect, color_hex)
        # Export
        filepath = _os.path.join(dirpath, color_name + '.svg')
        with open(filepath, 'w') as file_handle:
            file_handle.write(svg_text)


def export_rst_text(color_dict, filepath, width, height):
    fig_template = """- {name} ({hex_value})
  
  .. raw:: html

     {svg_text}
"""
    txl = []
    txl.append('.. _named-color-list:')
    txl.append('')
    txl.append('Named colors')
    txl.append('############')
    txl.append('')
    txl.append(
        "The current list of named colors stems from Matplotlib's :code:`colors` module, "
        "specifically the global variables :code:`BASE_COLORS`, :code:`CSS4_COLORS`, "
        ":code:`TABLEAU_COLORS` and :code:`XKCD_COLORS`. These names are made available "
        "both for Matplotlib and Plotly figures.")
    txl.append('')
    txl.append('Base colors')
    txl.append('-----------')
    txl.append('')
    for key, val in color_dict.items():
        # Headings (caution: depend on color list, might become wrong if more colors are added)
        if key == 'aliceblue':
            txl.append('')
            txl.append('CSS4 colors')
            txl.append('-----------')
            txl.append('')
        elif key == 'tab.blue':
            txl.append('')
            txl.append('Tableau colors')
            txl.append('--------------')
            txl.append('')
        elif key == 'xkcd.acid_green':
            txl.append('')
            txl.append('xkcd colors')
            txl.append('-----------')
            txl.append('')
        # SVG with rect filled in color
        svg_text = (
            '<p style="margin-top:-5pt">'
            '<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">'
            '<rect width="100%" height="100%" style="fill:{color};stroke:black;stroke-width:1" />'
            '</svg>'
            '</p>'
        ).format(w=width, h=height, color=val)
        txl.append(fig_template.format(name=key, hex_value=val, svg_text=svg_text))
    text = '\n'.join(txl)
    with open(filepath, 'w') as file_handle:
        file_handle.write(text)


ALL_COLORS = _named_colors.COLORS

DIRPATH = 'doc'
_os.makedirs(DIRPATH, exist_ok=True)

# now images are embedded directly in rst instead of using image files
# print('Generating doc images as svg files')
# export_color_images(all_colors, _os.path.join(dirpath, 'colors'), width=700, height=25)

print('Generating doc text as rst file')
FILEPATH = _os.path.join(DIRPATH, 'colors.rst')
export_rst_text(ALL_COLORS, FILEPATH, width='150mm', height='7mm')

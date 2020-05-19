# References
# - Matplotlib
#   - https://matplotlib.org/gallery/color/named_colors.html#sphx-glr-gallery-color-named-colors-py
#   - https://matplotlib.org/users/colors.html
#
# - Web standards
#   - Different resources
#     - https://en.wikipedia.org/wiki/Web_colors
#     - https://www.w3schools.com/colors/colors_names.asp
#     - https://xkcd.com/color/rgb/
#   - HTML 4.01 specification (1999) defines 16 colors (sRGB)
#     - https://www.w3.org/TR/REC-html40/types.html#h-6.5
#   - CSS 4
#     - https://drafts.csswg.org/css-color/#named-colors
#
# - Vendor standards
#   - https://en.wikipedia.org/wiki/X11_color_names
#
# - Other
#   - https://en.wikipedia.org/wiki/List_of_colors_(compact)

from collections import OrderedDict as _OrderedDict
from itertools import chain as _chain

from matplotlib import colors as _mpl_colors


def replace_symbols(given):
    replacement_table = [
        ('/', '_'),
        (':', '.'),
        (':', '.'),
        ('/', '_'),
        (' ', '_'),
        ("'", ''),
    ]
    for source, target in replacement_table:
        given = given.replace(source, target)
    return given


def generate_color_dict():
    base_colors = _OrderedDict(
        (name, _mpl_colors.rgb2hex(val).upper())
        for name, val in sorted(_mpl_colors.BASE_COLORS.items(), key=lambda x: x[0]))
    css4_colors = _OrderedDict(
        (name, val.upper())
        for name, val in sorted(_mpl_colors.CSS4_COLORS.items(), key=lambda x: x[0]))
    tableau_colors = _OrderedDict(
        (replace_symbols(name), val.upper())
        for name, val in sorted(_mpl_colors.TABLEAU_COLORS.items(), key=lambda x: x[0]))
    xkcd_colors = _OrderedDict(
        (replace_symbols(name), val.upper())
        for name, val in sorted(_mpl_colors.XKCD_COLORS.items(), key=lambda x: x[0]))
    combined_colors = _OrderedDict(_chain(
        base_colors.items(), css4_colors.items(), tableau_colors.items(), xkcd_colors.items()))
    return combined_colors


def export_colors_as_python_file(color_dict, filepath):
    text_list = []
    text_list.append('COLORS = {')
    for key, val in color_dict.items():
        text_list.append('    "{}": "{}",'.format(key, val))
    text_list.append('}')

    text = '\n'.join(text_list)
    with open(filepath, 'w') as file_handle:
        file_handle.write(text)


print('Generating color dict')
ALL_COLORS = generate_color_dict()

print('Generating python file')
export_colors_as_python_file(ALL_COLORS, 'named_colors.py')

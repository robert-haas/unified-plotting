"""Color conversion for different plotting libraries."""

from functools import lru_cache as _lru_cache

from . import named_colors as _named_colors


# Color conversion

def any_color_to_rgba(given_color):
    """Convert a given color in any format into a color in RGBA tuple format.

    References
    ----------
    - https://en.wikipedia.org/wiki/Web_colors
    - https://en.wikipedia.org/wiki/Web_colors#Shorthand_hexadecimal_form
    - https://matplotlib.org/gallery/color/named_colors.html
    - https://en.wikipedia.org/wiki/Web_colors#Shorthand_hexadecimal_form
    - https://www.w3.org/wiki/CSS3/Color/RGBA
    - https://developer.mozilla.org/en-US/docs/Web/CSS/color_value

    """
    if isinstance(given_color, str):
        # 1) Named color
        try:
            return _named_color_to_rgba_tuple(given_color)
        except ValueError:
            pass

        # 2) Hex triplet or quadruple color, e.g. "#00FF3C" or "#00FF3CF0"
        try:
            return _hex_str_to_rgba_tuple(given_color)
        except ValueError:
            pass

        # 3) RGB color str, e.g. "rgb(10, 200, 17)"
        try:
            return _rgb_str_to_rgba_tuple(given_color)
        except ValueError:
            pass

        # 4) RGBA color, e.g. "rgba(10, 200, 17, 0.77)"
        try:
            return _rgba_str_to_rgba_tuple(given_color)
        except ValueError:
            pass
    elif isinstance(given_color, tuple):
        # 5) RGB tuple, e.g. (10, 200, 17)
        if len(given_color) == 3:
            try:
                return _rgb_tuple_to_rgba_tuple(given_color)
            except ValueError:
                pass

        # 6) RGBA tuple, e.g. (10, 200, 17, 0.77)
        if len(given_color) == 4:
            try:
                return _rgba_tuple_to_rgba_tuple(given_color)
            except ValueError:
                pass

    raise ValueError('{} is not a valid color. Conversion to RGBA tuple failed.'.format(
        given_color))


def _check_rgba_format(rgba_tuple):
    assert len(rgba_tuple) == 4
    assert all(isinstance(num, int) and 0 <= num <= 255 for num in rgba_tuple[0:3])
    assert isinstance(rgba_tuple[3], float) and rgba_tuple[3] >= 0.0 and rgba_tuple[3] <= 1.0


def _remove_prefix(text, prefix):
    if text.startswith(prefix):
        text = text[len(prefix):]
    return text


@_lru_cache(maxsize=256)
def _named_color_to_rgba_tuple(given_color):
    """Convert a named color to an RGBA tuple.

    Parameters
    ----------
    given_color : str
        A color name.
        Case insensitive, i.e. "green", "Green" and "GREEN" are treated equally.

    """
    if given_color == 'transparent':
        return (0, 0, 0, 0.0)
    try:
        normalized_color_name = given_color.lower()
        color_hex = _named_colors.COLORS[normalized_color_name]
        return _hex_str_to_rgba_tuple(color_hex)
    except Exception:
        raise ValueError('Color conversion failed. Assumed input to be a named color.')


@_lru_cache(maxsize=256)
def _hex_str_to_rgba_tuple(given_color):
    """Convert a hex triplet color to an RGBA tuple."""
    try:
        # Preprocessing: Remove beginning #
        assert given_color.startswith('#')
        hex_str = _remove_prefix(given_color, '#')

        # Preprocessing: 3 or 4 letter shorthand form to 6 or 8 letter normal form
        num_letters = len(hex_str)
        if num_letters in (3, 4):
            hex_str = ''.join(char+char for char in hex_str)
            num_letters = len(hex_str)

        # Conversion of hex string to rgba tuple of 4 numbers in range 0-255, 0-255, 0-255, 0.0-1.0
        rgb = [int(hex_str[i: i+2], 16) for i in (0, 2, 4)]
        if num_letters == 6:
            rgba = tuple(rgb + [1.0])
        elif num_letters == 8:
            alpha = int(hex_str[6:8], 16) / 255.0
            rgba = tuple(rgb + [alpha])

        _check_rgba_format(rgba)
        return rgba
    except Exception:
        raise ValueError('Color conversion failed. Assumed input to be a shorthand 3 (4) '
                         'or normal 6 (8) digit hex color.')


@_lru_cache(maxsize=256)
def _rgb_str_to_rgba_tuple(given_color):
    """Convert an RGB str of form "rgb(num, num, num)" to an RGBA tuple."""
    try:
        given_color = given_color.replace(' ', '').lower().rstrip(')')
        given_color = _remove_prefix(given_color, 'rgb(')
        number_str_list = given_color.split(',')

        if number_str_list == ['1', '1', '1']:  # special case
            rgb_tuple = (1, 1, 1)
        else:
            rgb_tuple = tuple(float(num_str) for num_str in number_str_list)
        return _rgb_tuple_to_rgba_tuple(rgb_tuple)
    except Exception:
        raise ValueError('Color conversion failed. Assumed input to be an RGB string.')


@_lru_cache(maxsize=256)
def _rgba_str_to_rgba_tuple(given_color):
    """Convert an RGBA str of form "rgba(num, num, num, num)" to an RGBA tuple."""
    try:
        given_color = given_color.replace(' ', '').lower().rstrip(')')
        given_color = _remove_prefix(given_color, 'rgba(')
        number_str_list = given_color.split(',')

        if number_str_list[0:3] == ['1', '1', '1']:  # special case
            rgba_tuple = (1, 1, 1, float(number_str_list[3]))
        else:
            rgba_tuple = tuple(float(num_str) for num_str in number_str_list)
        return _rgba_tuple_to_rgba_tuple(rgba_tuple)
    except Exception:
        raise ValueError('Color conversion failed. Assumed input to be an RGBA string.')


def _rgb_tuple_to_rgba_tuple(given_color):
    """Convert an RGB tuple of form (num, num, num) to an RGBA tuple."""
    try:
        assert len(given_color) == 3
        rgba_list = list(given_color) + [1.0]
        return _rgba_tuple_to_rgba_tuple(rgba_list)
    except Exception:
        raise ValueError('Color conversion failed. Assumed input to be an RGB tuple.')


def _rgba_tuple_to_rgba_tuple(given_color):
    """Convert an RGBA tuple of form (num, num, num, num) to a valid RGBA tuple."""
    try:
        assert len(given_color) == 4
        if any(num > 1.0 for num in given_color[0:3]):
            factor = 1.0
        else:
            factor = 255.0
        if all(num == 1 and isinstance(num, int) for num in given_color[0:3]):
            rgb_0_to_255 = [1, 1, 1]  # special case
        else:
            rgb_0_to_255 = [int(item*factor) for item in given_color[0:3]]
        rgba_0_to_255 = tuple(rgb_0_to_255 + [float(given_color[3])])
        _check_rgba_format(rgba_0_to_255)
        return rgba_0_to_255
    except Exception:
        raise ValueError('Color conversion failed. Assumed input to be an RGB tuple.')


def _rgba_tuple_to_rgba_hex_str(given_color):
    red = int(given_color[0])
    green = int(given_color[1])
    blue = int(given_color[2])
    alpha = int(given_color[3] * 255.0)
    hex_str = '#{0:02x}{1:02x}{2:02x}{3:02x}'.format(red, green, blue, alpha)
    return hex_str

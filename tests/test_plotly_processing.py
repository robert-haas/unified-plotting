import pytest

from unified_plotting.plotly import _plotly_processing


# Tests with pytest

def test_color_conversion():
    in_out_map = [
        [(0, 0, 0, 1.0), 'rgba(0, 0, 0, 1.0)'],
        [(255, 255, 255, 1.0), 'rgba(255, 255, 255, 1.0)'],
        [(128, 0, 0, 0.5), 'rgba(128, 0, 0, 0.5)'],
    ]
    for color_in, color_out in in_out_map:
        assert _plotly_processing.convert_color(color_in) == color_out


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

        # wrong length tuple
        (0, 0),
        (0, 0, 0, 0, 0),
    ]
    for color_in in invalid_inputs:
        with pytest.raises(ValueError):
            print(_plotly_processing.convert_color(color_in))

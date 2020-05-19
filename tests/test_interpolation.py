import pytest

import unified_plotting as up


# Common preliminaries

x = [1, 1, 2, 2, 1, 1, 2, 2]
y = [1, 2, 1, 2, 1, 2, 1, 2]
z = [1, 1, 2, 2, 2, 2, 1, 1]


# Tests with pytest

@pytest.mark.parametrize('testmode, result', [
    ('min', [1, 1, 1, 1]),
    ('max', [2, 2, 2, 2])
])
def test_duplicate_removal(testmode, result):
    a, b, c = up.utilities.interpolation.remove_duplicate_xy_points(x, y, z, mode=testmode)
    assert list(c) == list(result)


def test_interpolation_on_grid():
    x = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
    y = [0, 1, 2, 3]*4
    z = [x_i+y_i for x_i, y_i in zip(x, y)]
    available_methods = ['allrounder_linear', 'allrounder_nearest', 'allrounder_cubic',
                         'rbf_cubic', 'rbf_gaussian', 'rbf_inverse', 'rbf_linear',
                         'rbf_multiquadric', 'rbf_quintic', 'rbf_thin_plate',
                         'spline_linear', 'spline_cubic']
    # 'spline_quintic'  hard to find suitable data
    for method in available_methods:
        up.utilities.interpolation.interpolate_at_gridpoints(x, y, z, interpolation_method=method)

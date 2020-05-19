"""2D interpolation on regular grids with various methods."""

from collections import OrderedDict as _OrderedDict

import numpy as _np
from scipy.interpolate import CloughTocher2DInterpolator as _CloughTocher2DInterpolator
from scipy.interpolate import Rbf as _Rbf
from scipy.interpolate import griddata as _griddata
from scipy.interpolate import interp2d as _interp2d

from .._unified_arguments import shared_preprocessing as _shared_preprocessing


def create_grid_2d(x, y, num_x_gridpoints=None, num_y_gridpoints=None,
                   x_min=None, x_max=None, y_min=None, y_max=None):
    """Create a regulard 2d grid of (x, y) pairs."""
    # Argument processing
    x_arr, y_arr = _np.array(x), _np.array(y)

    if num_x_gridpoints is None:  # Strong default, calls with explicit None are corrected
        num_x_gridpoints = 100
    if num_y_gridpoints is None:
        num_y_gridpoints = 100

    if x_min is None:
        x_min = _np.nanmin(x_arr)
    if x_max is None:
        x_max = _np.nanmax(x_arr)
    if y_min is None:
        y_min = _np.nanmin(y_arr)
    if y_max is None:
        y_max = _np.nanmax(y_arr)

    # Grid creation
    x_1d = _np.linspace(x_min, x_max, num_x_gridpoints)
    y_1d = _np.linspace(y_min, y_max, num_y_gridpoints)
    x_2d, y_2d = _np.meshgrid(x_1d, y_1d)
    return x_2d, y_2d


def interpolate_at_gridpoints(x, y, z, x_grid=None, y_grid=None,
                              num_x_gridpoints=None, num_y_gridpoints=None,
                              interpolation_method=None, interpolation_selection=None):
    """Interpolate given z values at irregular (x, y) positions on a regular 2d grid."""
    # Fast argument processing
    if interpolation_method is None:  # Strong default, calls with explicit None are corrected
        interpolation_method = 'rbf_linear'
    if interpolation_selection is None:
        interpolation_selection = 'max'

    # Validity checks
    available_methods = ['allrounder_linear', 'allrounder_nearest', 'allrounder_cubic',
                         'rbf_cubic', 'rbf_gaussian', 'rbf_inverse', 'rbf_linear',
                         'rbf_multiquadric', 'rbf_quintic', 'rbf_thin_plate',
                         'spline_linear', 'spline_cubic', 'spline_quintic']
    _shared_preprocessing.check_categorical_argument(
        interpolation_method, 'interpolation_method', available_methods)

    # Slow argument processing
    if x_grid is None or y_grid is None:
        x_grid, y_grid = create_grid_2d(x, y, num_x_gridpoints=num_x_gridpoints,
                                        num_y_gridpoints=num_y_gridpoints)
    x_unique, y_unique, z_unique = remove_duplicate_xy_points(x, y, z,
                                                              mode=interpolation_selection)

    # Interpolation
    main, sub = interpolation_method.split('_', 1)  # split only on first underscore
    try:
        if main == 'allrounder':
            x_2d, y_2d, z_2d = allrounder(x_unique, y_unique, z_unique, x_grid, y_grid, method=sub)
        elif main == 'rbf':
            x_2d, y_2d, z_2d = radial_basis_function(x_unique, y_unique, z_unique, x_grid, y_grid,
                                                     method=sub)
        elif main == 'spline':
            x_2d, y_2d, z_2d = spline(x_unique, y_unique, z_unique, x_grid, y_grid, method=sub)
        else:
            raise ValueError('Interpolation method could not be recognized.')
    except Exception:
        raise ValueError('Interpolation method "{}" failed for some reason. '
                         'You can try to use another interpolation method '
                         'of {}'.format(interpolation_method, available_methods))
    x_1d = x_2d[0, :]  # Plotly's go.Surface() works with either (x_1d, y_1d) or (x_2d, y_2d)
    y_1d = y_2d[:, 0]  # but go.Contour() only with (x_2d, y_2d)
    return x_1d, y_1d, z_2d


def allrounder(x, y, z, x_grid=None, y_grid=None, method='linear',
               num_x_gridpoints=None, num_y_gridpoints=None):
    """Interpolate using the general interpolation method in SciPy.

    References
    ----------
    - https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html#scipy.interpolate.griddata
    - https://stackoverflow.com/questions/37872171/how-can-i-perform-two-dimensional-interpolation-using-scipy

    """
    # Validity checks
    available_methods = ['linear', 'nearest', 'cubic']
    if method not in available_methods:
        raise ValueError('Interpolation method "{}" is not known. Please choose one of {}'.format(
            method, available_methods))

    # Argument processing
    x_arr, y_arr, z_arr = _np.array(x), _np.array(y), _np.array(z)
    if x_grid is None or y_grid is None:
        x_grid, y_grid = create_grid_2d(x_arr, y_arr, num_x_gridpoints=num_x_gridpoints,
                                        num_y_gridpoints=num_y_gridpoints)

    # Interpolation
    points2d = _np.array([x_arr.ravel(), y_arr.ravel()]).T
    values = z_arr.ravel()
    x_i = (x_grid, y_grid)
    z_interpolated_on_grid = _griddata(points=points2d, values=values, xi=x_i, method=method)
    return x_grid, y_grid, z_interpolated_on_grid


def clough_tocher(x, y, z, x_grid=None, y_grid=None,
                  num_x_gridpoints=None, num_y_gridpoints=None):
    """Interpolate using the Clough-Toucher interpolation method in SciPy.

    Notes
    -----
    In 2D it is exactly the same as griddata interpolator with method='cubic'

    References
    ----------
    - https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.CloughTocher2DInterpolator.html

    """
    # Argument processing
    x_arr, y_arr, z_arr = _np.array(x), _np.array(y), _np.array(z)
    if x_grid is None or y_grid is None:
        x_grid, y_grid = create_grid_2d(x_arr, y_arr, num_x_gridpoints=num_x_gridpoints,
                                        num_y_gridpoints=num_y_gridpoints)

    # Interpolation
    points2d = _np.array([x_arr.ravel(), y_arr.ravel()]).T
    values = z_arr.ravel()
    x_i = (x_grid, y_grid)
    ct_interpolator = _CloughTocher2DInterpolator(points=points2d, values=values)
    z_interpolated_on_grid = ct_interpolator(x_i)
    return x_grid, y_grid, z_interpolated_on_grid


def radial_basis_function(x, y, z, x_grid=None, y_grid=None, method='linear',
                          num_x_gridpoints=100, num_y_gridpoints=100):
    """Interpolate using the radial basis function approximation in SciPy.

    References
    ----------
    - https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.Rbf.html
    - https://stackoverflow.com/questions/37872171/how-can-i-perform-two-dimensional-interpolation-using-scipy

    """
    # Validity checks
    available_methods = ['cubic', 'gaussian', 'inverse', 'linear', 'multiquadric', 'quintic',
                         'thin_plate']
    if method not in available_methods:
        raise ValueError('Interpolation method "{}" is not known. Please choose one of {}'.format(
            method, available_methods))

    # Argument processing
    x_arr, y_arr, z_arr = _np.array(x), _np.array(y), _np.array(z)
    if x_grid is None or y_grid is None:
        x_grid, y_grid = create_grid_2d(x_arr, y_arr, num_x_gridpoints=num_x_gridpoints,
                                        num_y_gridpoints=num_y_gridpoints)

    # Interpolation
    rbf_interpolator = _Rbf(x_arr, y_arr, z_arr, smooth=0, function=method)
    z_interpolated_on_grid = rbf_interpolator(x_grid, y_grid)
    return x_grid, y_grid, z_interpolated_on_grid


def spline(x, y, z, x_grid=None, y_grid=None, method='linear',
           num_x_gridpoints=100, num_y_gridpoints=100):
    """Interpolate using the spline interpolation method in SciPy.

    Caution: Only first row of x_grid and first column of y_grid are used.

    References
    ----------
    - https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp2d.html#scipy.interpolate.interp2d

    """
    # Validity checks
    available_methods = ['linear', 'cubic', 'quintic']
    if method not in available_methods:
        raise ValueError('Interpolation method "{}" is not known. Please choose one of {}'.format(
            method, available_methods))

    # Argument processing
    x_arr, y_arr, z_arr = _np.array(x), _np.array(y), _np.array(z)
    if x_grid is None or y_grid is None:
        x_grid, y_grid = create_grid_2d(x_arr, y_arr, num_x_gridpoints=num_x_gridpoints,
                                        num_y_gridpoints=num_y_gridpoints)

    # Interpolation
    spline_interpolator = _interp2d(x_arr, y_arr, z_arr, kind=method)
    x_i = x_grid[0]
    y_i = y_grid[:, 0]
    z_interpolated_on_grid = spline_interpolator(x_i, y_i)
    return x_grid, y_grid, z_interpolated_on_grid


def remove_duplicate_xy_points(x, y, z, mode='max'):
    """Remove duplicate points where x and y values are identical and keep a single z value."""
    # Validity checks
    if len(x) != len(y) or len(x) != len(z) or len(y) != len(z):
        raise ValueError('x, y and z need to be of same length')
    available_modes = ['min', 'max']
    if mode not in available_modes:
        raise ValueError('Duplicate selection mode "{}" is not known. Please choose '
                         'one of {}'.format(mode, available_modes))

    # Construction of unique xy points, keeping either min or max of all corresponding z values
    unique_points_dict = _OrderedDict()
    for x_i, y_i, z_i in zip(x, y, z):
        point_i = (x_i, y_i)
        if point_i in unique_points_dict:
            # del d[point]  # Other sort order, such that point appears at position with largest z
            if mode == 'max':
                if z_i > unique_points_dict[point_i]:
                    unique_points_dict[point_i] = z_i
            else:
                if z_i < unique_points_dict[point_i]:
                    unique_points_dict[point_i] = z_i
        else:
            unique_points_dict[point_i] = z_i
    n_points = len(unique_points_dict)
    x_unique, y_unique, z_unique = _np.zeros(n_points), _np.zeros(n_points), _np.zeros(n_points)
    for i, (key, val) in enumerate(unique_points_dict.items()):
        x_unique[i] = key[0]
        y_unique[i] = key[1]
        z_unique[i] = val
    return x_unique, y_unique, z_unique

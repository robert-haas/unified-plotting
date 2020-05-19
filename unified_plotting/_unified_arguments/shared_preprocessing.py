"""Preprocessing used by various subpackages."""

import json as _json
from collections import OrderedDict as _OrderedDict
from collections.abc import Iterable as _Iterable
from math import floor as _floor
from math import log10 as _log10
from numbers import Number as _Number

import numpy as _np

from .. import _logging
from .._unified_arguments import arguments as _arguments
from ..utilities import format_conversion as _format_conversion
from ..utilities import interpolation as _interpolation
from ..utilities import io as _io
from ..utilities import operating_system as _operating_system


# Part 1: Function arguments

def check_and_filter_kwargs(kwargs, exceptions=None):
    """Check if the provided keyword arguments are known.

    If unknown arguments are present, exclude them and issue a warning.

    """
    # Argument processing
    if exceptions is None:
        exceptions = []

    # Transformation
    unknown_kwargs = [key for key in kwargs
                      if key not in _arguments.UNIFIED_ARGS and key not in exceptions]
    if unknown_kwargs:
        _logging.report_unknown_kwargs(unknown_kwargs)
    known_kwargs = {key: val for key, val in kwargs.items()
                    if key not in unknown_kwargs}
    return known_kwargs


def check_categorical_argument(given_value, argument_name, possible_values):
    """Check if the given value for a categorical argument is in a list of possible values."""
    if given_value not in possible_values:
        possible_values_str = ', '.join(repr(el) for el in possible_values)
        message = (
            'Got an invalid value for an argument: {}={}\n\nPossible '
            'values: {}'.format(argument_name, repr(given_value), possible_values_str))
        raise ValueError(message)


# Part 2: Vector data

def prepare_vector_data_2d(x, y, kwargs):
    """Prepare vector data for standard 2d plots."""
    # Convert various Iterables to list
    x = _try_to_list(x)
    y = _try_to_list(y)
    # Convert categorical axes if necessary
    x, kwargs = _convert_axis_if_cat('x', x, kwargs)
    y, kwargs = _convert_axis_if_cat('y', y, kwargs)
    # Require vectors to be non-empty and to have equal lengths
    _check_if_nonempty([x, y])
    _check_if_equal_lengths([x, y])
    # If a vector contains a non-finite numerical element, remove the position from all
    x, y = _remove_nonfinite_rows([x, y])
    return x, y


def prepare_vector_data_2d_multiple(x, y, kwargs):
    """Prepare vector data for 2d plots that accept multiple series per argument."""
    # Default values for error series
    x_error_left = kwargs.get('x_error_left', None)
    x_error_right = kwargs.get('x_error_right', None)
    y_error_top = kwargs.get('y_error_top', None)
    y_error_bottom = kwargs.get('y_error_bottom', None)
    no_x_error = False
    if x_error_left is None and x_error_right is None:
        no_x_error = True
    elif x_error_left is None:
        x_error_left = x_error_right
    elif x_error_right is None:
        x_error_right = x_error_left
    no_y_error = False
    if y_error_top is None and y_error_bottom is None:
        no_y_error = True
    elif y_error_top is None:
        y_error_top = y_error_bottom
    elif y_error_bottom is None:
        y_error_bottom = y_error_top
    # Convert various Iterables to list
    x = _try_to_list(x)
    y = _try_to_list(y)
    x_el = _try_to_list(x_error_left)
    x_er = _try_to_list(x_error_right)
    y_et = _try_to_list(y_error_top)
    y_eb = _try_to_list(y_error_bottom)
    # Convert single to multiple series if necessary
    multiple_series = _data_contains_multiple_series(x) and _data_contains_multiple_series(y)
    if multiple_series:
        xs, ys = x, y
        x_els, x_ers, y_ets, y_ebs = x_el, x_er, y_et, y_eb
    else:
        xs, ys = [x], [y]
        x_els, x_ers, y_ets, y_ebs = [x_el], [x_er], [y_et], [y_eb]
    # Convert categorical axes if necessary
    xs, kwargs = _convert_axis_if_cat_multiple('x', xs, kwargs)
    ys, kwargs = _convert_axis_if_cat_multiple('y', ys, kwargs)
    # Combine data
    if no_x_error and no_y_error:
        data = [xs, ys]
    elif no_x_error:
        data = [xs, ys, y_ets, y_ebs]
    elif no_y_error:
        data = [xs, ys, x_els, x_ers]
    else:
        data = [xs, ys, x_els, x_ers, y_ets, y_ebs]
    # Convert data
    new_data = [[] for _ in range(len(data))]
    for vectors in zip(*data):
        # Convert various Iterables to list
        vectors = [_try_to_list(vec) for vec in vectors]
        # Require vectors to be non-empty and to have equal lengths
        _check_if_nonempty(vectors)
        _check_if_equal_lengths(vectors)
        # If a vector contains a non-finite numerical element, remove the position from all
        vectors = _remove_nonfinite_rows(vectors)
        for i, vec in enumerate(vectors):
            new_data[i].append(vec)
    # Split data
    if no_x_error and no_y_error:
        xs, ys = new_data
        x_els, x_ers = None, None
        y_ets, y_ebs = None, None
    elif no_x_error:
        xs, ys, y_ets, y_ebs = new_data
        x_els, x_ers = None, None
    elif no_y_error:
        xs, ys, x_els, x_ers = new_data
        y_ets, y_ebs = None, None
    else:
        xs, ys, x_els, x_ers, y_ets, y_ebs = new_data
    return xs, ys, x_els, x_ers, y_ets, y_ebs, multiple_series


def prepare_vector_data_3d_grid(x, y, z, kwargs,
                                interpolation_method=None, interpolation_selection=None,
                                interpolation_num_x_gridpoints=None,
                                interpolation_num_y_gridpoints=None,
                                interpolate=True):
    """Prepare vector data for 3d plots that accept equal-length vector data or grid data."""
    # Convert various Iterables to list
    x = _try_to_list(x)
    y = _try_to_list(y)
    z = _try_to_list(z)
    # Convert categorical axes if necessary
    x, kwargs = _convert_axis_if_cat('x', x, kwargs)
    y, kwargs = _convert_axis_if_cat('y', y, kwargs)
    if _data_contains_multiple_series(z):
        z, kwargs = _convert_axis_if_cat_grid('z', z, kwargs)
    else:
        z, kwargs = _convert_axis_if_cat('z', z, kwargs)
    # Require vectors to be non-empty
    _check_if_nonempty([x, y, z])
    # Shared message if data format is wrong
    message = (
        'The provided data is invalid. There are two possible formats: '
        '1) x, y and z each are a list of values with the same length. '
        '2) x is a list of n values in increasing order, y a list of m values in increasing '
        'order and z a list of m lists with n values each, such that together they define a '
        'regular m x n grid. '
        'Given lengths: x={}, y={}, z={}'.format(len(x), len(y), len(z)))

    # Transformation based on data format
    # 1)  Vectors with different lengths: x with length n, y with length m, z with shape m x n
    if isinstance(z[0], _Iterable) and not isinstance(z[0], (str, bytes)):
        # Require vectors to have suitable lengths
        if len(x) != len(z[0]) or len(y) != len(z):
            raise ValueError(message)
        # Remove rows where at least one vector has a non-finite numerical value
        # - x and z
        result = _remove_nonfinite_rows([x] + z)
        x, z = result[0], result[1:]
        # - y and z
        z = list(zip(*z))  # transpose
        result = _remove_nonfinite_rows([y] + z)
        y, z = result[0], result[1:]
        z = list(zip(*z))  # transpose (back)
        # Check if monotonically increasing
        if not _is_increasing_vector(x):
            message = (
                'The values in x are not in increasing order. '
                'This may cause an incorrect appearance.')
            _logging.warn_user(message)
        if not _is_increasing_vector(y):
            message = (
                'The values in y are not in increasing order. '
                'This may cause an incorrect appearance.')
            _logging.warn_user(message)
    # 2)Three vectors with same length
    else:
        # Require vectors to have equal length
        try:
            _check_if_equal_lengths([x, y, z])
        except Exception:
            raise ValueError(message) from None
        # Remove rows where at least one vector has a non-finite numerical value
        x, y, z = _remove_nonfinite_rows([x, y, z])
        # Interpolate on a regular grid
        if interpolate:
            x, y, z = _interpolation.interpolate_at_gridpoints(
                x, y, z,
                num_x_gridpoints=interpolation_num_x_gridpoints,
                num_y_gridpoints=interpolation_num_y_gridpoints,
                interpolation_method=interpolation_method,
                interpolation_selection=interpolation_selection
            )
    return x, y, z


def prepare_vector_data_3d_multiple(x, y, z, kwargs):
    """Prepare vector data for 3d plots that accept multiple series per argument."""
    # Convert various Iterables to list
    x = _try_to_list(x)
    y = _try_to_list(y)
    z = _try_to_list(z)
    # Convert single to multiple series if necessary
    multiple_series = (
        _data_contains_multiple_series(x) and
        _data_contains_multiple_series(y) and
        _data_contains_multiple_series(z)
    )
    if multiple_series:
        xs, ys, zs = x, y, z
    else:
        xs, ys, zs = [x], [y], [z]
    # Convert categorical axes if necessary
    xs, kwargs = _convert_axis_if_cat_multiple('x', xs, kwargs)
    ys, kwargs = _convert_axis_if_cat_multiple('y', ys, kwargs)
    zs, kwargs = _convert_axis_if_cat_multiple('z', zs, kwargs)
    xs_new, ys_new, zs_new = [], [], []
    for x_i, y_i, z_i in zip(xs, ys, zs):
        # Convert various Iterables to list
        x_i = _try_to_list(x_i)
        y_i = _try_to_list(y_i)
        z_i = _try_to_list(z_i)
        # Require corresponding vectors to be non-empty and to have equal length
        _check_if_nonempty([x_i, y_i, z_i])
        _check_if_equal_lengths([x_i, y_i, z_i])
        # Remove rows where at least one vector has a non-finite numerical value
        x_i, y_i, z_i = _remove_nonfinite_rows([x_i, y_i, z_i])
        xs_new.append(x_i)
        ys_new.append(y_i)
        zs_new.append(z_i)
    xs, ys, zs = xs_new, ys_new, zs_new
    return xs, ys, zs, multiple_series


def prepare_vector_data_nd(data, name, remove_non_numerical_vectors=True):
    """Prepare vector data for standard nd plots."""
    # Filepath or dataframe to list of vectors
    data, name = _to_list_of_vectors_and_names(data, name)
    # Convert various Iterables to list
    data = [_try_to_list(vec) for vec in data]
    # Require vectors to be non-empty and to have equal length
    _check_if_nonempty(data)
    _check_if_equal_lengths(data)
    # Remove vectors with at least one non-numerical entry
    if remove_non_numerical_vectors:
        data, name = _remove_nonnumerical_vectors(data, name)
    # Remove rows where at least one vector has a non-finite numerical value
    data = _remove_nonfinite_rows(data, consider_only_numbers=not remove_non_numerical_vectors)
    return data, name


def prepare_vector_data_nd_stats(data, name, remove_non_numerical_vectors=True):
    """Prepare vector data for nd plots that display statistics, hence allow different lengths."""
    # Filepath or dataframe to list of vectors
    data, name = _to_list_of_vectors_and_names(data, name)
    # Convert various Iterables to list
    data = [_try_to_list(vec) for vec in data]
    # Require vectors to be non-empty
    _check_if_nonempty(data)
    # Remove vectors with at least one non-numerical entry
    if remove_non_numerical_vectors:
        data, name = _remove_nonnumerical_vectors(data, name)
    # Remove non-finite numerical values individually (in a single vector, not spread to all)
    data = _remove_nonfinite_elements(data)
    return data, name


def _is_finite_number(value):
    """Check whether a given element is a finite number."""
    try:
        returned = _np.isfinite(value)
        if isinstance(returned, _np.ndarray):
            result = False
        else:
            result = bool(returned)
    except Exception:
        result = False
    return result


def _is_number(value):
    return isinstance(value, _Number)


def _is_finite_number_or_other_type(value):
    """Check whether a given element is a number and finite, or another type."""
    if _is_number(value):
        result = _is_finite_number(value)
    else:
        result = True
    return result


def _is_axis_categorical(name, kwargs):
    """Check if an axis is defined to be categorical in kwargs."""
    key = '{}_axis_scale'.format(name)
    value = kwargs.get(key, None)
    return value in ('cat', 'categorical')


def _is_increasing_vector(vector):
    """Check if a vector is monotonically increasing."""
    try:
        vector = _np.array(vector)
        result = _np.all(vector[1:] >= vector[:-1])
    except Exception:
        result = False
    return result


def _to_list_of_vectors_and_names(data, name):
    """Convert various data sources (DSV filepath, DataFrame) to lists of vectors and names."""
    # Data
    name_from_data = None
    if isinstance(data, str):
        if _operating_system.is_nonempty_file(data):
            data, name_from_data = _io.read_dsv_file(data, name)
        else:
            message = 'The provided data is invalid. It is a string but not a valid filepath.'
            raise ValueError(message)
    elif 'DataFrame' in str(type(data)):
        data, name_from_data = _format_conversion.dataframe_to_vector_data(data)
    else:
        data = list(data)
    # Name
    if name is None:
        if name_from_data:
            name = name_from_data
        else:
            name = ['Series {}'.format(i+1) for i in range(len(data))]
    if len(name) < len(data):
        name += ['Series {}'.format(i+1) for i in range(len(name), len(data))]
    elif len(name) > len(data):
        name = name[:len(data)]
    return data, name


def _try_to_list(vector):
    try:
        assert not isinstance(vector, (str, bytes))
        result = list(vector)
    except Exception:
        result = vector
    return result


def _check_if_nonempty(data):
    """Check if a list of vectors is non-empty."""
    vector_lengths = set(len(vector) for vector in data)
    if not vector_lengths:
        message = 'The data contains zero vectors. Nothing can be plotted.'
        raise ValueError(message)
    if 0 in vector_lengths:
        if len(vector_lengths) == 1:
            message = 'The data contains only vectors with no elements. Nothing can be plotted.'
            raise ValueError(message)
        message = (
            'The data contains a vector with no elements. This seems to be a mistake, '
            'therefore no plot was created.')
        raise ValueError(message)


def _check_if_equal_lengths(data):
    """Check whether all vectors share the same length."""
    vector_lengths = set(len(vector) for vector in data)
    if len(vector_lengths) > 1:
        vector_lengths_str = ', '.join(str(length) for length in sorted(vector_lengths))
        message = (
            'This plot type requires that all vectors have the same length. '
            'Found following different lengths: {}'.format(vector_lengths_str))
        raise ValueError(message)


def _categories_to_values(vector_of_categories, category_to_value_map=None):
    """Convert a categorical vector to unique categories, numbers and a map between them."""
    # Argument processing
    vector_of_categories = [str(item) for item in vector_of_categories]

    # Transformation
    if category_to_value_map is None:
        category_to_value_map = _OrderedDict((cat, None) for cat in vector_of_categories)
    else:
        for cat in vector_of_categories:
            category_to_value_map[cat] = None
    for i, key in enumerate(category_to_value_map):
        category_to_value_map[key] = i
    numeric_values = [category_to_value_map[item] for item in vector_of_categories]
    categorical_values = list(category_to_value_map)
    return categorical_values, numeric_values, category_to_value_map


def _set_axis_to_categorical(name, categorical_values, kwargs):
    """Set scale, tick positions and labels of an axis in order to show categorical data."""
    def set_kwarg_if_it_is_none(kwargs, key, value):
        current_value = kwargs.get(key, None)
        kwargs[key] = value if current_value is None else current_value

    kwargs['{}_axis_scale'.format(name)] = 'linear'
    tick_position = list(range(len(categorical_values)))
    set_kwarg_if_it_is_none(kwargs, '{}_tick_position'.format(name), tick_position)
    set_kwarg_if_it_is_none(kwargs, '{}_label'.format(name), categorical_values)


def _convert_axis_if_cat(name, vector, kwargs):
    """Check if an axis was set to be categorical and if so adapt it to a single data series."""
    if _is_axis_categorical(name, kwargs):
        categorical_values, numeric_values, _ = _categories_to_values(vector)
        _set_axis_to_categorical(name, categorical_values, kwargs)
        vector = numeric_values
    return vector, kwargs


def _convert_axis_if_cat_grid(name, list_of_vectors, kwargs):
    """Check if an axis was set to be categorical and if so adapt it to 2d grid data."""
    if _is_axis_categorical(name, kwargs):
        m, n = len(list_of_vectors), len(list_of_vectors[0])
        flat_vector = [element for vector in list_of_vectors for element in vector]
        categorical_values, numeric_values, _ = _categories_to_values(flat_vector)
        list_of_vectors = [numeric_values[i*n:(i+1)*n] for i in range(m)]
        _set_axis_to_categorical(name, categorical_values, kwargs)
    return list_of_vectors, kwargs


def _convert_axis_if_cat_multiple(name, list_of_vectors, kwargs):
    """Check if an axis was set to be categorical and if so adapt it to multiple data series."""
    if _is_axis_categorical(name, kwargs):
        # Note that there is interplay between all series by sharing the category-number map
        # (and categorical_values grows by that mechanism too)
        cn_map = None
        new_list_of_vectors = []
        for vector in list_of_vectors:
            categorical_values, numeric_values, cn_map = _categories_to_values(vector, cn_map)
            new_list_of_vectors.append(numeric_values)
        list_of_vectors = new_list_of_vectors
        _set_axis_to_categorical(name, categorical_values, kwargs)
    return list_of_vectors, kwargs


def _data_contains_multiple_series(data):
    """Check if the provided data contains multiple series of values."""
    multiple_series = True
    try:
        series = data[0]
        assert isinstance(series, _Iterable) and not isinstance(series, (str, bytes))
    except Exception:
        multiple_series = False
    return multiple_series


def _remove_nonnumerical_vectors(data, name, ignored_vectors=None):
    """Remove non-numerical vectors from a list of vectors."""
    # Argument processing
    if ignored_vectors is None:
        ignored_vectors = [False] * len(data)

    # Validity checks
    try:
        assert len(data) == len(name) == len(ignored_vectors)
    except Exception:
        message = (
            'The filtering function for removing non-numerical vectors got '
            'invalid data as input.')
        raise ValueError(message) from None

    # Transformation
    new_data = []
    new_name = []
    count_removed = 0
    for vector, label, ignored in zip(data, name, ignored_vectors):
        if ignored:
            skip_vector = False
        else:
            skip_vector = any(not isinstance(element, _Number) for element in vector)
        if skip_vector:
            count_removed += 1
        else:
            new_data.append(vector)
            new_name.append(label)

    # Report if anything got removed
    if count_removed > 0:
        plural = 's' if count_removed > 1 else ''
        message = (
            'Some non-numeric values were detected in the provided data. '
            'In total, {} vector{} with at least one non-numerical element got removed '
            'automatically before plotting.'.format(count_removed, plural))
        if len(new_data) == 0:
            message += ' After this filtering process, no vectors remained to be plotted.'
            raise ValueError(message)
        _logging.warn_user(message)
    return new_data, new_name


def _remove_nonfinite_elements(data, ignored_vectors=None):
    """Remove non-finite elements from a list of vectors and do not conserve equal lengths."""
    # Argument processing
    if ignored_vectors is None:
        ignored_vectors = [False] * len(data)

    # Transformation
    new_data = []
    count_removed = 0
    for ignore, vector in zip(ignored_vectors, data):
        if ignore:
            new_vector = new_data.append(vector)
        else:
            new_vector = []
            for element in vector:
                if _is_finite_number(element):
                    new_vector.append(element)
                else:
                    count_removed += 1
            new_data.append(new_vector)

    # Report if anything got removed
    if count_removed > 0:
        plural = 's' if count_removed > 1 else ''
        message = (
            'Some non-finite values (NaN, +Inf, -Inf, non-numerical) were detected in the '
            'provided data. In total, {} such item{} got removed individually before '
            'plotting.'.format(count_removed, plural))
        if all(len(vector) == 0 for vector in new_data):
            message += ' After this filtering process, no elements remained to be plotted.'
            raise ValueError(message)
        _logging.warn_user(message)
    return new_data


def _remove_nonfinite_rows(data, ignored_vectors=None, consider_only_numbers=False):
    """Remove non-finite rows from a list of vectors and conserve equal lengths."""
    # Argument processing
    if ignored_vectors is None:
        ignored_vectors = [False] * len(data)

    # Transformation
    if consider_only_numbers:
        is_accepted = _is_finite_number_or_other_type
    else:
        is_accepted = _is_finite_number

    new_data = []
    count_removed = 0
    for row in zip(*data):
        skip_row = False
        for ignore, element in zip(ignored_vectors, row):
            if not ignore:
                if not is_accepted(element):
                    skip_row = True
                    break
        if skip_row:
            count_removed += 1
        else:
            new_data.append(row)
    new_data = list(list(col) for col in zip(*new_data))  # from rows back to column vectors

    # Report if anything got removed
    if count_removed > 0:
        plural = 's' if count_removed > 1 else ''
        message = (
            'Some non-numerical (str, None, ...) or non-finite values (NaN, +Inf, -Inf) '
            'were detected in the provided data. In total, {} row{} got removed '
            'collectively before plotting, because at least one vector contained such '
            'an item at this position.'.format(count_removed, plural))
        if all(len(vector) == 0 for vector in new_data):
            message += ' After this filtering process, no rows remained to be plotted.'
            raise ValueError(message)
        _logging.warn_user(message)
    return new_data


# Part 3: Graph data

def prepare_graph_data(data):
    """Get graph data in various forms and convert it to a single, unified form (JGF).

    Parameters
    ----------
    data : dict conforming to JSON graph format, or graph object of a supported library,
           or filepath to a JSON file

    """
    def raise_error(additional_message=None):
        message = 'Provided data is not in a valid graph format.'
        if additional_message:
            message += ' {}'.format(additional_message)
        raise ValueError(message)

    def filepath_to_json_object(filepath):
        with open(filepath) as file_handle:
            return _json.load(file_handle)

    def json_str_to_json_object(text):
        return _json.loads(text)

    def str_to_json_object(text):
        if _operating_system.is_nonempty_file(text):
            data = filepath_to_json_object(text)
        else:
            try:
                data = json_str_to_json_object(text)
            except Exception:
                message = (
                    'Given data is a string that is neither a filepath nor a valid JSON string.')
                raise ValueError(message)
        return data
    # Case 0: A string that can be a filepath to a text file or a JSON string
    if isinstance(data, str):
        data = str_to_json_object(data)
    # Case 1: Single graph object
    if _is_known_graph_object(data):
        data = _convert_graph_object_to_jgf(data)
        data = [data]
    # Case 2: Single JGF dict (with single graph)
    elif isinstance(data, dict) and 'graph' in data:
        data = data['graph']
        data = [data]
    # Case 3: Single JGF dict (with multiple graphs)
    elif isinstance(data, dict) and 'graphs' in data:
        data = data['graphs']
    # Case 4: Iterable of multiple graph objects and/or JGF dicts (with single graph each)
    elif isinstance(data, _Iterable) and not isinstance(data, dict):
        try:
            num_items = len(data)
        except Exception:
            raise_error('Iterable with no length.')
        if num_items < 1:
            raise_error('Iterable with zero items.')
        new_data = []
        for idx in range(num_items):
            item = data[idx]
            if _is_known_graph_object(item):
                item = _convert_graph_object_to_jgf(item)
            elif isinstance(item, str):
                item = str_to_json_object(item)
            elif isinstance(item, dict) and 'graph' in item:
                item = item['graph']
            else:
                raise_error('Iterable with invalid item at position {}.'.format(idx))
            new_data.append(item)
        data = new_data
    # Case 5: Other unknown data
    else:
        raise_error()
    return data


def _is_known_graph_object(data):
    """Check if the given data is a graph object from one of the supported libraries."""
    result = False
    try:
        dtype = str(type(data)).lower()
        if isinstance(data, list):
            dtype_inner = str(type(data[0])).lower()
            if 'networkit' in dtype_inner:
                dtype = dtype_inner
        result = ('graph_tool.graph' in dtype) or \
            ('igraph.graph' in dtype) or \
            ('networkit' in dtype) or \
            ('networkx.classes' in dtype) or \
            ('snap' in dtype)
    except Exception:
        pass
    return result


def _convert_graph_object_to_jgf(data):
    """Convert a graph object from a supported library into JGF without top-level graph key."""
    dtype = str(type(data)).lower()
    if isinstance(data, list):
        dtype_inner = str(type(data[0])).lower()
        if 'networkit' in dtype_inner:
            dtype = dtype_inner
    if 'graph_tool.graph' in dtype:
        data = _format_conversion.graphtool_to_jgf(data)
    elif 'igraph.graph' in dtype:
        data = _format_conversion.igraph_to_jgf(data)
    elif 'networkit' in dtype:
        data = _format_conversion.networkit_to_jgf(data)
    elif 'networkx.classes' in dtype:
        data = _format_conversion.networkx_to_jgf(data)
    elif 'snap' in dtype:
        data = _format_conversion.snap_to_jgf(data)
    else:
        message = 'Provided data is not a known graph object.'
        raise ValueError(message)
    return data['graph']


# Part 4: Different helper functions

def warn_if_categorical_axis(kwargs):
    """Warn if an axis is specified to be categorical in a plot not supporting it."""
    for axis_name in ('x', 'y'):
        if _is_axis_categorical(axis_name, kwargs):
            message = (
                'This plot type currently does not support the {} axis scale to be '
                'categorical. It is treated as numerical and linear instead.'.format(axis_name))
            _logging.warn_user(message)


def categorical_to_numerical(vector_categorical, name_to_number_map=None):
    """Transform a categorical variable (str items) into a numerical variable (int items)."""
    # Argument processing
    if not name_to_number_map:
        name_to_number_map = dict()
        counter = 1  # next used number is 1
    else:
        counter = max(name_to_number_map.values()) + 1  # next used number is one higher than max

    # Transformation
    vector_numerical = list()
    for name in vector_categorical:
        number = counter
        if name not in name_to_number_map:
            name_to_number_map[name] = number
            counter += 1
        else:
            number = name_to_number_map[name]
        vector_numerical.append(number)
    return vector_numerical, name_to_number_map


def shift_away_from_extrema(x, y, z, direction, shift_factor=0.05):
    """Determine x, y, and z values that lie a certain distance outwards of the data range."""
    # Validity check
    possible_values = ['lower', 'upper']
    check_categorical_argument(direction, 'direction', possible_values)

    # Transformation
    def safe_get_min(array):
        try:
            min_val = _np.nanmin(array)
        except Exception:
            min_val = 0.0
        return min_val

    def safe_get_max(array):
        try:
            max_val = _np.nanmax(array)
        except Exception:
            max_val = len(array)
        return max_val

    x_min, y_min, z_min = safe_get_min(x), safe_get_min(y), safe_get_min(z)
    x_max, y_max, z_max = safe_get_max(x), safe_get_max(y), safe_get_max(z)
    x_span, y_span, z_span = x_max-x_min, y_max-y_min, z_max-z_min
    if direction == 'lower':
        x_bound = x_min - x_span*shift_factor
        y_bound = y_min - y_span*shift_factor
        z_bound = z_min - z_span*shift_factor
    elif direction == 'upper':
        x_bound = x_max + x_span*shift_factor
        y_bound = y_max + y_span*shift_factor
        z_bound = z_max + z_span*shift_factor
    return x_bound, y_bound, z_bound


def round_to_significant_digits(number, num_significant_digits):
    """Round a float number to a given number of significant digits.

    References
    ----------
    - https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python

    """
    # Validity check
    if not isinstance(number, _Number):
        raise TypeError('Given data is not a number: {} of type {}'.format(number, type(number)))

    # Transformation
    try:
        return round(number, num_significant_digits-int(_floor(_log10(abs(number))))-1)
    except Exception:
        return number

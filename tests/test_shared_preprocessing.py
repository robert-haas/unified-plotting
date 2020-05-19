import os

import numpy as np
import pytest

import unified_plotting as up
from shared_data_loading import IN_DIR
from unified_plotting._unified_arguments import shared_preprocessing


# Helper functions

def emits_warning(func, caplog, expected_message):
    if isinstance(expected_message, str):
        expected_message = [expected_message]
    caplog.clear()
    func()
    if len(caplog.records) == 0:
        raise ValueError('The expected warning was not emitted: {}'.format(expected_message))
    for message, record in zip(expected_message, caplog.records):
        assert message in record.message


def emits_no_warning(func, caplog):
    caplog.clear()
    func()
    assert len(caplog.records) == 0


def emits_error(func, error_type, expected_message=None):
    # https://docs.pytest.org/en/latest/assert.html#assertions-about-expected-exceptions
    with pytest.raises(error_type) as excp:
        func()
    if expected_message:
        assert expected_message in str(excp.value)


def create_filter_data():
    vn5 = [1, 2, 3, 4, 5]
    vn6 = [1, 2, 3, 4, 5, 6]
    vf1 = [1, 2, 3, float('nan'), 5]
    vf2 = [1, float('inf'), 3, float('nan'), 5]
    vf3 = [float('-inf'), float('nan'), 3, float('inf'), 5]
    vc1 = [1, 2, 3, 'abc', 5]
    vc2 = [1, 'a', 3, 'bc', 5]
    vc3 = ['xy', 'ab', 3, 'cd', 5]
    return vn5, vn6, vf1, vf2, vf3, vc1, vc2, vc3


def create_filter_messages():
    mrs = '{} row got removed'
    mrp = '{} rows got removed'
    mis = '{} such item got removed'
    mip = '{} such items got removed'
    mnz = 'no vectors remained'
    mns = '{} vector with at least one non-numerical element got removed'
    mnp = '{} vectors with at least one non-numerical element got removed'
    return mrs, mrp, mis, mip, mnz, mns, mnp


# Tests with pytest

@pytest.mark.parametrize('value, expected_result', [
    (0, True),
    (1, True),
    (-1, True),
    (3.14, True),
    (-3.14, True),
    (float('nan'), True),
    (float('inf'), True),
    (float('-inf'), True),
    ('0', False),
    ([1, 2], False),
    ([], False),
    ((), False),
    (None, False),
    ('', False),
])
def test_is_number(value, expected_result):
    result = shared_preprocessing._is_number(value)
    assert result in [True, False]
    assert result == expected_result


@pytest.mark.parametrize('value, expected_result', [
    (0, True),
    (1, True),
    (-1, True),
    (3.14, True),
    (-3.14, True),
    (float('nan'), False),
    (float('inf'), False),
    (float('-inf'), False),
    ('0', False),
    ([1, 2], False),
    ([], False),
    ((), False),
    (None, False),
    ('', False),
])
def test_is_finite_number(value, expected_result):
    result = shared_preprocessing._is_finite_number(value)
    assert result in [True, False]
    assert result == expected_result


@pytest.mark.parametrize('value, expected_result', [
    (0, True),
    (1, True),
    (-1, True),
    (3.14, True),
    (-3.14, True),
    (float('nan'), False),
    (float('inf'), False),
    (float('-inf'), False),
    ('0', True),
    ([1, 2], True),
    ([], True),
    ((), True),
    (None, True),
    ('', True),
])
def test_is_finite_number_or_other_type(value, expected_result):
    result = shared_preprocessing._is_finite_number_or_other_type(value)
    assert result in [True, False]
    assert result == expected_result


@pytest.mark.parametrize('data, ignored_vectors, expected_result', [
    # Single vector
    ([[]], [False], [[]]),
    ([[1, 2, 3]], [False], [[1, 2, 3]]),
    ([[1, 2, float('inf')]], [False], [[1, 2, float('inf')]]),
    # Two vectors
    ([[], []], [False, False], [[], []]),
    ([[], []], [False, True], [[], []]),
    ([[], []], [True, False], [[], []]),
    ([[], []], [True, True], [[], []]),
    ([[1, 2, 3], [4, 5, 6]], [False, False], [[1, 2, 3], [4, 5, 6]]),
    ([[1, 2, 3], [4, 5, 6]], [False, True], [[1, 2, 3], [4, 5, 6]]),
    ([[1, 2, 3], [4, 5, 6]], [True, False], [[1, 2, 3], [4, 5, 6]]),
    ([[1, 2, 3], [4, 5, 6]], [True, True], [[1, 2, 3], [4, 5, 6]]),
    ([[1, 2, 3], [4, 5]], [False, False], [[1, 2, 3], [4, 5]]),
    ([[1, 2, 3], [4, 5]], [False, True], [[1, 2, 3], [4, 5]]),
    ([[1, 2, 3], [4, 5]], [True, False], [[1, 2, 3], [4, 5]]),
    ([[1, 2, 3], [4, 5]], [True, True], [[1, 2, 3], [4, 5]]),
    ([[1, 2, 'a'], [4, 5, 6]], [False, False], [[4, 5, 6]]),
    ([[1, 2, 'a'], [4, 5, 6]], [False, True], [[4, 5, 6]]),
    ([[1, 2, 'a'], [4, 5, 6]], [True, False], [[1, 2, 'a'], [4, 5, 6]]),
    ([[1, 2, 'a'], [4, 5, 6]], [True, True], [[1, 2, 'a'], [4, 5, 6]]),
    ([[1, 2, None], [4, 5, 6]], [False, False], [[4, 5, 6]]),
    ([[1, 2, None], [4, 5, 6]], [False, True], [[4, 5, 6]]),
    ([[1, 2, None], [4, 5, 6]], [True, False], [[1, 2, None], [4, 5, 6]]),
    ([[1, 2, None], [4, 5, 6]], [True, True], [[1, 2, None], [4, 5, 6]]),
    ([[1, 2, []], [4, 5, 6]], [False, False], [[4, 5, 6]]),
    ([[1, 2, []], [4, 5, 6]], [False, True], [[4, 5, 6]]),
    ([[1, 2, []], [4, 5, 6]], [True, False], [[1, 2, []], [4, 5, 6]]),
    ([[1, 2, []], [4, 5, 6]], [True, True], [[1, 2, []], [4, 5, 6]]),
    ([[1, 2, 3], [4, 5, 'a']], [False, False], [[1, 2, 3]]),
    ([[1, 2, 3], [4, 'a', 6]], [False, True], [[1, 2, 3], [4, 'a', 6]]),
    ([[1, 2, 3], ['a', 5, 6]], [True, False], [[1, 2, 3]]),
    ([[1, 2, 3], [4, 'a', 6]], [True, True], [[1, 2, 3], [4, 'a', 6]]),
    # Three vectors
    ([[1, 2], [3, 4, 5], [6]], [False, False, False], [[1, 2], [3, 4, 5], [6]]),
    ([[1, 2], [3, 4, 5], [6]], [False, False, True], [[1, 2], [3, 4, 5], [6]]),
    ([[1, 2], [3, 4, 5], [6]], [False, True, False], [[1, 2], [3, 4, 5], [6]]),
    ([[1, 2], [3, 4, 5], [6]], [False, True, True], [[1, 2], [3, 4, 5], [6]]),
    ([[1, 2], [3, 4, 5], [6]], [True, False, False], [[1, 2], [3, 4, 5], [6]]),
    ([[1, 2], [3, 4, 5], [6]], [True, False, True], [[1, 2], [3, 4, 5], [6]]),
    ([[1, 2], [3, 4, 5], [6]], [True, True, False], [[1, 2], [3, 4, 5], [6]]),
    ([[1, 2], [3, 4, 5], [6]], [True, True, True], [[1, 2], [3, 4, 5], [6]]),
    ([[1, 2], [3, 'a', 5], [6]], [False, False, False], [[1, 2], [6]]),
    ([[1, 2], [3, 'a', 5], [6]], [False, False, True], [[1, 2], [6]]),
    ([[1, 2], [3, 'a', 5], [6]], [False, True, False], [[1, 2], [3, 'a', 5], [6]]),
    ([[1, 2], [3, 'a', 5], [6]], [False, True, True], [[1, 2], [3, 'a', 5], [6]]),
    ([[1, 2], [3, 'a', 5], [6]], [True, False, False], [[1, 2], [6]]),
    ([[1, 2], [3, 'a', 5], [6]], [True, False, True], [[1, 2], [6]]),
    ([[1, 2], [3, 'a', 5], [6]], [True, True, False], [[1, 2], [3, 'a', 5], [6]]),
    ([[1, 2], [3, 'a', 5], [6]], [True, True, True], [[1, 2], [3, 'a', 5], [6]]),
])
def test_remove_nonnumerical_vectors(data, ignored_vectors, expected_result):
    name = ['Series {}'.format(i) for i in range(len(data))]
    result, _ = shared_preprocessing._remove_nonnumerical_vectors(data, name, ignored_vectors)
    print(data)
    print(result)
    assert np.array_equal(result, expected_result)


@pytest.mark.parametrize('data, name, ignored_vectors', [
    ([[1, 2]], None, None),
    ([[1, 2]], None, [False]),
    ([[1, 2], [1, 2]], ['a', 'b'], [False]),
    ([[1, 2], [1, 2]], ['a'], [False, True]),
    ([[1, 2]], ['a', 'b'], [False, True]),
])
def test_remove_nonnumerical_vectors_fail(data, name, ignored_vectors):
    with pytest.raises(ValueError):
        shared_preprocessing._remove_nonnumerical_vectors(data, name, ignored_vectors)


@pytest.mark.parametrize('data, expected_result', [
    # Single vector
    ([[1, 2, 3]], [[1, 2, 3]]),
    ([[1, 'a', 3]], [[1, 3]]),
    ([['a', 2, 3]], [[2, 3]]),
    ([[1, 2, 'a']], [[1, 2]]),
    # Two vectors
    ([[1, 2, 3], [10, 20, 30]], [[1, 2, 3], [10, 20, 30]]),
    ([['a', 2, 3], [10, 20, 30]], [[2, 3], [20, 30]]),
    ([[None, 2, 3], [10, 20, 30]], [[2, 3], [20, 30]]),
    ([[[42], 2, 3], [10, 20, 30]], [[2, 3], [20, 30]]),
    ([[1, 2, 3], ['a', 20, 30]], [[2, 3], [20, 30]]),
    ([[1, 2, 'a'], [10, 20, 30]], [[1, 2], [10, 20]]),
    ([[1, 2, None], [10, 20, 30]], [[1, 2], [10, 20]]),
    ([[1, 2, [42]], [10, 20, 30]], [[1, 2], [10, 20]]),
    ([[1, 2, 3], [10, 20, 'a']], [[1, 2], [10, 20]]),
    ([['a', 2, 3], [10, 'a', 30]], [[3], [30]]),
    ([[1, 'a', 3], [10, 20, 'a']], [[1], [10]]),
    ([[1, 'a', 'a'], [10, 'a', 30]], [[1], [10]]),
    # Three vectors
    ([[1, 2, 3], [10, 20, 30], [100, 200, 300]], [[1, 2, 3], [10, 20, 30], [100, 200, 300]]),
    ([['a', 2, 3], [10, 20, 30], [None, 200, 300]], [[2, 3], [20, 30], [200, 300]]),
    ([[1, 2, 3], [10, 20, None], [100, 200, 300]], [[1, 2], [10, 20], [100, 200]]),
])
def test_remove_nonfinite_rows(data, expected_result):
    result = shared_preprocessing._remove_nonfinite_rows(data, [False]*len(data))
    assert np.array_equal(result, expected_result)


@pytest.mark.parametrize('data, expected_result', [
    # Single vector
    ([[1, 2, 3]], [[1, 2, 3]]),
    ([[1, float('nan'), 3]], [[1, 3]]),
    ([[float('nan'), 2, 3]], [[2, 3]]),
    ([[1, 2, float('nan')]], [[1, 2]]),
    # Two vectors
    ([[1, 2, 3], [10, 20, 30]], [[1, 2, 3], [10, 20, 30]]),
    ([['a', 2, 3], [10, 20, 30]], [[2, 3], [20, 30]]),
    ([[None, 2, 3], [10, 20, 30]], [[2, 3], [20, 30]]),
    ([[[42], 2, 3], [10, 20, 30]], [[2, 3], [20, 30]]),
    ([[1, 2, 3], [10, 'b', 'c']], [[1], [10]]),
    ([[1, 2, 'a'], [10, 20, 30]], [[1, 2], [10, 20]]),
    ([[1, 2, None], [10, 20, 30]], [[1, 2], [10, 20]]),
    ([[1, 2, [42]], [10, 20, 30]], [[1, 2], [10, 20]]),
    ([[1, 2, 3], [10, 20, 'a']], [[1, 2], [10, 20]]),
    ([['a', 2, 3], [10, None, 30]], [[3], [30]]),
    ([[1, 'a', 3], [10, 20, 'a']], [[1], [10]]),
    ([[1, 'a', 'a'], [10, 'a', 30]], [[1], [10]]),
    # Three vectors
    ([[1, 2, 3], [10, 20, 30], [100, 200, 300]], [[1, 2, 3], [10, 20, 30], [100, 200, 300]]),
    ([['a', 2, 3], [10, 20, 30], [None, 200, 300]], [[2, 3], [20, 30], [200, 300]]),
    ([[1, 2, 3], [10, 'x', 'y'], [100, 200, 300]], [[1], [10], [100]]),
])
def test_get_finite_numeric_rows(data, expected_result):
    result = shared_preprocessing._remove_nonfinite_rows(data)
    for vec1, vec2 in zip(result, expected_result):
        for item1, item2 in zip(vec1, vec2):
            assert item1 == item2


def test_prepare_vector_data_nd():
    data = [[1, 2, 3], [4, 5, 6]]
    returned_data, name = shared_preprocessing.prepare_vector_data_nd(data, name=None)
    assert returned_data
    assert isinstance(returned_data, list)
    assert returned_data == data
    assert name
    assert isinstance(name, list)
    assert name == ['Series 1', 'Series 2']

    filepath = os.path.join(IN_DIR, 't1_minimal.csv')
    returned_data, name = shared_preprocessing.prepare_vector_data_nd(filepath, name=['first'])
    assert returned_data
    assert isinstance(returned_data, list)
    assert returned_data == [[1, 2, 1], [1, 2, 2], [1, 2, 1]]
    assert name
    assert isinstance(name, list)
    assert name == ['first', 'Series 2', 'Series 3']

    filepath = os.path.join(IN_DIR, 't1_minimal_with_partial_header.csv')
    returned_data, name = shared_preprocessing.prepare_vector_data_nd(filepath, name=None)
    assert returned_data
    assert isinstance(returned_data, list)
    assert returned_data == [[1, 2, 1], [1, 2, 2], [1, 2, 1]]
    assert name
    assert isinstance(name, list)
    assert name == ['a', 'b', '']


def test_prepare_vector_data_2d_filtering(caplog):
    vn5, vn6, vf1, vf2, vf3, vc1, vc2, vc3 = create_filter_data()
    mrs, mrp, mis, mip, mnz, mns, mnp = create_filter_messages()

    # 2d plots that expect vectors with same length and filter entire rows
    methods = [
        up.matplotlib.hexbin,
        up.matplotlib.histogram_2d,
        up.plotly.density_2d,
        up.plotly.density_scatter_histogram_2d,
        up.plotly.histogram_2d,
    ]
    for method in methods:
        # numerical
        emits_error(lambda: method(x=[], y=[]), ValueError, 'only vectors with no elements')
        emits_error(lambda: method(x=[], y=[1, 2]), ValueError, 'a vector with no elements')
        emits_error(lambda: method(x=vn5, y=vn6), ValueError, 'vectors have the same length')
        emits_error(lambda: method(x=vn6, y=vn5), ValueError, 'vectors have the same length')
        emits_no_warning(lambda: method(x=vn5, y=vn5), caplog)
        emits_no_warning(lambda: method(x=reversed(vn5), y=vn5), caplog)
        emits_no_warning(lambda: method(x=vn5, y=reversed(vn5)), caplog)
        emits_warning(lambda: method(x=vf1, y=vn5), caplog, mrs.format(1))
        emits_warning(lambda: method(x=vn5, y=vf1), caplog, mrs.format(1))
        emits_warning(lambda: method(x=vf1, y=vf1), caplog, mrs.format(1))
        emits_warning(lambda: method(x=vn5, y=vf2), caplog, mrp.format(2))
        emits_warning(lambda: method(x=vf2, y=vf1), caplog, mrp.format(2))
        emits_warning(lambda: method(x=vf2, y=vf3), caplog, mrp.format(3))
        # categorical
        emits_warning(lambda: method(x=vc1, y=vn5), caplog, mrs.format(1))
        emits_warning(lambda: method(x=vn5, y=vc1), caplog, mrs.format(1))
        emits_warning(lambda: method(x=vc1, y=vc1), caplog, mrs.format(1))
        emits_warning(lambda: method(x=vc2, y=vc1), caplog, mrp.format(2))
        emits_warning(lambda: method(x=vc3, y=vf3), caplog, mrp.format(3))
        emits_no_warning(lambda: method(x=vc1, y=vn5, x_axis_scale='cat'), caplog)
        emits_no_warning(lambda: method(x=vn5, y=vc1, y_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=vc1, y=vc1, x_axis_scale='cat', y_axis_scale='cat'), caplog)
        emits_no_warning(lambda: method(x=reversed(vc1), y=vn5, x_axis_scale='cat'), caplog)
        emits_no_warning(lambda: method(x=vn5, y=reversed(vc1), y_axis_scale='cat'), caplog)

    # 2d plots that expect single or multiple series of vectors with same length
    methods = [
        up.matplotlib.scatter,
        up.plotly.bar,
        up.plotly.scatter,
    ]
    for method in methods:
        # 1) single
        # numerical
        emits_error(lambda: method(x=[], y=[]), ValueError, 'only vectors with no elements')
        emits_error(lambda: method(x=[], y=[1, 2]), ValueError, 'a vector with no elements')
        emits_error(lambda: method(x=vn5, y=vn6), ValueError, 'vectors have the same length')
        emits_error(lambda: method(x=vn6, y=vn5), ValueError, 'vectors have the same length')
        emits_no_warning(lambda: method(x=vn5, y=vn5), caplog)
        emits_no_warning(lambda: method(x=reversed(vn5), y=vn5), caplog)
        emits_no_warning(lambda: method(x=vn5, y=reversed(vn5)), caplog)
        emits_warning(lambda: method(x=vf1, y=vn5), caplog, mrs.format(1))
        emits_warning(lambda: method(x=vn5, y=vf1), caplog, mrs.format(1))
        emits_warning(lambda: method(x=vf1, y=vf1), caplog, mrs.format(1))
        emits_warning(lambda: method(x=vn5, y=vf2), caplog, mrp.format(2))
        emits_warning(lambda: method(x=vf2, y=vf1), caplog, mrp.format(2))
        emits_warning(lambda: method(x=vf2, y=vf3), caplog, mrp.format(3))
        # categorical
        emits_warning(lambda: method(x=vc1, y=vn5), caplog, mrs.format(1))
        emits_warning(lambda: method(x=vn5, y=vc1), caplog, mrs.format(1))
        emits_warning(lambda: method(x=vc1, y=vc1), caplog, mrs.format(1))
        emits_warning(lambda: method(x=vc2, y=vc1), caplog, mrp.format(2))
        emits_warning(lambda: method(x=vc3, y=vf3), caplog, mrp.format(3))
        emits_no_warning(lambda: method(x=vc1, y=vn5, x_axis_scale='cat'), caplog)
        emits_no_warning(lambda: method(x=reversed(vc1), y=vn5, x_axis_scale='cat'), caplog)
        emits_no_warning(lambda: method(x=vc1, y=reversed(vn5), x_axis_scale='cat'), caplog)
        emits_warning(
            lambda: method(x=vc1, y=vn5, y_axis_scale='cat'),
            caplog, mrs.format(1))
        emits_no_warning(
            lambda: method(x=vn5, y=vc1, y_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=vc1, y=vc1, x_axis_scale='categorical', y_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=vc2, y=vc1, x_axis_scale='cat', y_axis_scale='categorical'), caplog)
        emits_warning(
            lambda: method(x=vc3, y=vf2, x_axis_scale='cat'),
            caplog, mrp.format(2))
        # 2) multiple
        # numerical
        emits_error(
            lambda: method(x=[[], []], y=[[], []]), ValueError, 'only vectors with no elements')
        emits_error(
            lambda: method(x=[[1, 2], []], y=[[1, 2], [1, 2]]),
            ValueError, 'a vector with no elements')
        emits_error(
            lambda: method(x=[vn5, vn5], y=[vn5, vn6]),
            ValueError, 'vectors have the same length')
        emits_error(
            lambda: method(x=[vn5, vn6], y=[vn5, vn5]),
            ValueError, 'vectors have the same length')
        emits_no_warning(lambda: method(x=[vn5, vn5], y=[vn5, vn5]), caplog)
        emits_no_warning(lambda: method(x=reversed([vn5, vn5]), y=[vn5, vn5]), caplog)
        emits_no_warning(lambda: method(x=[reversed(vn5), vn5], y=[vn5, vn5]), caplog)
        emits_no_warning(lambda: method(x=[vn5, vn5], y=[vn5, reversed(vn5)]), caplog)
        emits_warning(
            lambda: method(x=[vn5, vf1], y=[vn5, vn5]),
            caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=[vn5, vn5, vn5], y=[vf1, vn5, vn5]),
            caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=[vf1], y=[vf1]),
            caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=[vf1, vn5], y=[vf2, vn5]),
            caplog, mrp.format(2))
        emits_warning(
            lambda: method(x=[vf2], y=[vf1]),
            caplog, mrp.format(2))
        emits_warning(
            lambda: method(x=[vn5, vf2], y=[vn5, vf3]),
            caplog, mrp.format(3))
        # categorical
        emits_warning(
            lambda: method(x=[vc1], y=[vn5]),
            caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=[vn5, vn5], y=[vc1, vn5]),
            caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=[vn5, vc1], y=[vn5, vc1]),
            caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=[vc2, vc1], y=[vn5, vc1]),
            caplog, [mrp.format(2), mrs.format(1)])
        emits_warning(
            lambda: method(x=[vc2, vn5], y=[vn5, vf3]),
            caplog, [mrp.format(2), mrp.format(3)])
        emits_no_warning(
            lambda: method(x=[vc1], y=[vn5], x_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=[reversed(vc1)], y=[vn5], x_axis_scale='cat'), caplog)
        emits_warning(
            lambda: method(x=[vc1], y=[vn5], y_axis_scale='cat'),
            caplog, mrs.format(1))
        emits_no_warning(
            lambda: method(x=[vn5], y=[vc1], y_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=reversed([vn5, vn5]), y=[reversed(vc1), vc1], y_axis_scale='cat'),
            caplog)
        emits_no_warning(
            lambda: method(x=[vc1], y=[vc1], x_axis_scale='categorical', y_axis_scale='cat'),
            caplog)
        emits_no_warning(
            lambda: method(x=[vc2], y=[vc1], x_axis_scale='cat', y_axis_scale='categorical'),
            caplog)
        emits_warning(
            lambda: method(x=[vc3], y=[vf2], x_axis_scale='cat'),
            caplog, mrp.format(2))


def test_prepare_vector_data_3d_filtering(caplog):
    vn5, vn6, vf1, vf2, vf3, vc1, vc2, vc3 = create_filter_data()
    mrs, mrp, mis, mip, mnz, mns, mnp = create_filter_messages()

    # 3d plots that expect single or multiple series of vectors with same length
    methods = [
        up.matplotlib.scatter_3d,
        up.plotly.scatter_3d,
    ]
    for method in methods:
        # 1) single
        # numerical
        emits_error(
            lambda: method(x=[], y=[], z=[]), ValueError, 'only vectors with no elements')
        emits_error(
            lambda: method(x=[], y=[1, 2], z=[3, 4]), ValueError, 'a vector with no elements')
        emits_error(
            lambda: method(x=vn6, y=vn6, z=vn5), ValueError, 'vectors have the same length')
        emits_error(
            lambda: method(x=vn5, y=vn6, z=vn5), ValueError, 'vectors have the same length')
        emits_error(
            lambda: method(x=vn5, y=vn5, z=vn6), ValueError, 'vectors have the same length')
        emits_no_warning(
            lambda: method(x=vn5, y=vn5, z=vn5), caplog)
        emits_no_warning(
            lambda: method(x=reversed(vn5), y=vn5, z=vn5), caplog)
        emits_no_warning(
            lambda: method(x=vn5, y=reversed(vn5), z=vn5), caplog)
        emits_no_warning(
            lambda: method(x=vn5, y=vn5, z=reversed(vn5)), caplog)
        emits_warning(
            lambda: method(x=vf1, y=vn5, z=vn5), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vn5, y=vf1, z=vn5), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vf1, y=vf1, z=vf1), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vn5, y=vf2, z=vf1), caplog, mrp.format(2))
        emits_warning(
            lambda: method(x=vf2, y=vf1, z=vn5), caplog, mrp.format(2))
        emits_warning(
            lambda: method(x=vf2, y=vf3, z=vf1), caplog, mrp.format(3))
        # categorical
        emits_warning(
            lambda: method(x=vc1, y=vn5, z=vn5), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vn5, y=vc1, z=vf1), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vc1, y=vc1, z=vn5), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vc2, y=vc1, z=vc1), caplog, mrp.format(2))
        emits_warning(
            lambda: method(x=vc3, y=vf3, z=vf2), caplog, mrp.format(3))
        emits_no_warning(
            lambda: method(x=vc1, y=vn5, z=vn5, x_axis_scale='cat'), caplog)
        emits_warning(
            lambda: method(x=vc1, y=vn5, z=vn5, y_axis_scale='cat'),
            caplog, mrs.format(1))
        emits_no_warning(
            lambda: method(x=vn5, y=vc1, z=vn5, y_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=vn5, y=vn5, z=vc1, z_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=vc1, y=vc1, z=vn5, x_axis_scale='categorical', y_axis_scale='cat'),
            caplog)
        emits_no_warning(
            lambda: method(
                x=vc2, y=vc1, z=vc3, x_axis_scale='cat', y_axis_scale='cat', z_axis_scale='cat'),
            caplog)
        emits_no_warning(
            lambda: method(x=reversed(vn5), y=vc1, z=vn5, y_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=vn5, y=reversed(vc1), z=vn5, y_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=vn5, y=reversed(vn5), z=vc1, z_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=vn5, y=vn5, z=reversed(vc1), z_axis_scale='cat'), caplog)
        emits_warning(
            lambda: method(x=vc3, y=vf2, z=vf1, x_axis_scale='cat'),
            caplog, mrp.format(2))
        # 2) multiple
        # numerical
        emits_error(
            lambda: method(x=[[], []], y=[[], []], z=[[], []]),
            ValueError, 'only vectors with no elements')
        emits_error(
            lambda: method(x=[[1, 2], []], y=[[1, 2], [1, 2]], z=[[1, 2], [1, 2]]),
            ValueError, 'a vector with no elements')
        emits_error(
            lambda: method(x=[vn5, vn6], y=[vn5, vn5], z=[vn5, vn5]),
            ValueError, 'vectors have the same length')
        emits_error(
            lambda: method(x=[vn5, vn5], y=[vn6, vn5], z=[vn5, vn5]),
            ValueError, 'vectors have the same length')
        emits_error(
            lambda: method(x=[vn5, vn5], y=[vn5, vn5], z=[vn5, vn6]),
            ValueError, 'vectors have the same length')
        emits_no_warning(
            lambda: method(x=[vn5, vn5], y=[vn5, vn5], z=[vn5, vn5]), caplog)
        emits_no_warning(
            lambda: method(x=[reversed(vn5), vn5], y=[vn5, vn5], z=[vn5, vn5]), caplog)
        emits_no_warning(
            lambda: method(x=reversed([vn5, vn5]), y=[vn5, vn5], z=[vn5, vn5]), caplog)
        emits_no_warning(
            lambda: method(x=[vn5, vn5], y=[reversed(vn5), vn5], z=[vn5, vn5]), caplog)
        emits_no_warning(
            lambda: method(x=[vn5, vn5], y=reversed([vn5, vn5]), z=[vn5, vn5]), caplog)
        emits_no_warning(
            lambda: method(x=[vn5, vn5], y=[vn5, vn5], z=[reversed(vn5), vn5]), caplog)
        emits_no_warning(
            lambda: method(x=[vn5, vn5], y=[vn5, vn5], z=reversed([vn5, vn5])), caplog)
        emits_warning(
            lambda: method(x=[vn5, vf1], y=[vn5, vn5], z=[vn5, vc1]),
            caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=[vn5, vn5, vn5], y=[vf1, vn5, vn5], z=[vn5, vn5, vn5]),
            caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=[vf1], y=[vf1], z=[vc1]),
            caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=[vf1, vn5], y=[vf2, vn5], z=[vf1, vn5]),
            caplog, mrp.format(2))
        emits_warning(
            lambda: method(x=[vf2], y=[vf1], z=[vn5]),
            caplog, mrp.format(2))
        emits_warning(
            lambda: method(x=[vn5, vf2], y=[vn5, vf3], z=[vn5, vc1]),
            caplog, mrp.format(3))
        # categorical
        emits_warning(
            lambda: method(x=[vc1], y=[vn5], z=[vn5]),
            caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=[vn5, vn5], y=[vc1, vn5], z=[vc1, vn5]),
            caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=[vn5, vn5], y=[vn5, vc1], z=[vn5, vc1]),
            caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=[vc2, vc1], y=[vn5, vc1], z=[vf2, vc1]),
            caplog, [mrp.format(2), mrs.format(1)])
        emits_warning(
            lambda: method(x=[vc2, vn5], y=[vn5, vf3], z=[vn5, vf3]),
            caplog, [mrp.format(2), mrp.format(3)])
        emits_no_warning(
            lambda: method(x=[vc1], y=[vn5], z=[vn5], x_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=[vn5], y=[vc1], z=[vn5], y_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=[vn5], y=[vn5], z=[vc1], z_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=reversed([vc1]), y=[vn5], z=[vn5], x_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=[vn5], y=[reversed(vc1)], z=[vn5], y_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=[vn5], y=[vn5], z=[reversed(vc1)], z_axis_scale='cat'), caplog)
        emits_warning(
            lambda: method(x=[vc1], y=[vn5], z=[vn5], y_axis_scale='cat'),
            caplog, mrs.format(1))
        emits_no_warning(
            lambda: method(x=[vn5], y=[vc1], z=[vn5], y_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=[vc1], y=[vc1], z=[vn5], x_axis_scale='categorical',
                           y_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=[vc2], y=[vc1], z=[vn5], x_axis_scale='cat',
                           y_axis_scale='categorical'), caplog)
        emits_warning(
            lambda: method(x=[vc3], y=[vf2], z=[vn5], x_axis_scale='cat'),
            caplog, mrp.format(2))

    # 3d plots that expect three same-length vectors OR grid data
    methods = [
        up.matplotlib.contour,
        up.plotly.contour,
        up.plotly.heatmap,
        up.plotly.surface,
    ]
    for method in methods:
        # 1) same length
        # numerical
        emits_error(
            lambda: method(x=[], y=[], z=[]), ValueError, 'only vectors with no elements')
        emits_error(
            lambda: method(x=[], y=[1, 2], z=[3, 4]), ValueError, 'a vector with no elements')
        emits_error(
            lambda: method(x=vn6, y=vn6, z=vn5), ValueError, 'provided data is invalid')
        emits_error(
            lambda: method(x=vn5, y=vn6, z=vn5), ValueError, 'provided data is invalid')
        emits_error(
            lambda: method(x=vn5, y=vn5, z=vn6), ValueError, 'provided data is invalid')
        emits_no_warning(
            lambda: method(x=vn5, y=vn5, z=vn5), caplog)
        emits_no_warning(
            lambda: method(x=reversed(vn5), y=vn5, z=vn5), caplog)
        emits_no_warning(
            lambda: method(x=vn5, y=reversed(vn5), z=vn5), caplog)
        emits_no_warning(
            lambda: method(x=vn5, y=vn5, z=reversed(vn5)), caplog)
        emits_warning(
            lambda: method(x=vf1, y=vn5, z=vn5), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vn5, y=vf1, z=vn5), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vf1, y=vf1, z=vf1), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vn5, y=vf2, z=vf1), caplog, mrp.format(2))
        emits_warning(
            lambda: method(x=vf2, y=vf1, z=vn5), caplog, mrp.format(2))
        emits_warning(
            lambda: method(x=vf2, y=vf3, z=vf1), caplog, mrp.format(3))
        # categorical
        emits_warning(
            lambda: method(x=vc1, y=vn5, z=vn5), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vn5, y=vc1, z=vf1), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vc1, y=vc1, z=vn5), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vc2, y=vc1, z=vc1), caplog, mrp.format(2))
        emits_warning(
            lambda: method(x=vc3, y=vf3, z=vf2), caplog, mrp.format(3))
        emits_no_warning(
            lambda: method(x=vc1, y=vn5, z=vn5, x_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=vc1, y=reversed(vn5), z=vn5, x_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=reversed(vc1), y=vn5, z=vn5, x_axis_scale='cat'), caplog)
        emits_warning(
            lambda: method(x=vc1, y=vn5, z=vn5, y_axis_scale='cat'),
            caplog, mrs.format(1))
        emits_no_warning(
            lambda: method(x=vn5, y=vc1, z=vn5, y_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=vn5, y=vn5, z=vc1, z_axis_scale='cat'), caplog)
        emits_no_warning(
            lambda: method(x=vc1, y=vc1, z=vn5, x_axis_scale='categorical', y_axis_scale='cat'),
            caplog)
        emits_no_warning(
            lambda: method(
                x=vc2, y=vc1, z=vc3, x_axis_scale='cat', y_axis_scale='cat', z_axis_scale='cat'),
            caplog)
        emits_warning(
            lambda: method(x=vc3, y=vf2, z=vf1, x_axis_scale='cat'),
            caplog, mrp.format(2))
        # 2) grid
        # numerical
        emits_error(
            lambda: method(x=[], y=[], z=[]), ValueError, 'only vectors with no elements')
        emits_error(
            lambda: method(x=[], y=[1, 2], z=[[3, 4], [3, 4]]),
            ValueError, 'a vector with no elements')
        emits_no_warning(
            lambda: method(x=vn5, y=vn5, z=[vn5]*5), caplog)
        emits_warning(
            lambda: method(x=vf1, y=vn5, z=[vn5]*5), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vn5, y=vf1, z=[vn5]*5), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vn5, y=vn5, z=[vf1]*5), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vf2, y=vn5, z=[vf2]*5), caplog, mrp.format(2))
        emits_warning(
            lambda: method(x=vf1, y=vf1, z=[vn5]*5), caplog,
            [mrs.format(1), mrs.format(1)])
        emits_warning(
            lambda: method(x=reversed(vn5), y=vn5, z=[vn5]*5),
            caplog, 'values in x are not in increasing order')
        emits_warning(
            lambda: method(x=vn5, y=reversed(vn5), z=[vn5]*5),
            caplog, 'values in y are not in increasing order')
        emits_warning(
            lambda: method(x=reversed(vn5), y=reversed(vn5), z=[vn5]*5),
            caplog, ['x are not in increasing order', 'y are not in increasing order'])
        # categorical
        emits_warning(
            lambda: method(x=vc1, y=vn5, z=[vn5]*5), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vn5, y=vc1, z=[vn5]*5), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vn5, y=vn5, z=[vc1]*5), caplog, mrs.format(1))
        emits_warning(
            lambda: method(x=vc2, y=vn5, z=[vc2]*5), caplog, mrp.format(2))
        emits_warning(
            lambda: method(x=vn5, y=vc1, z=[vc1]*5), caplog,
            [mrs.format(1), mrs.format(1)])
        emits_warning(
            lambda: method(x=vn5, y=vf1, z=[vc1]*5), caplog,
            [mrs.format(1), mrs.format(1)])


def test_prepare_vector_data_nd_filtering(caplog):
    vn5, vn6, vf1, vf2, vf3, vc1, vc2, vc3 = create_filter_data()
    mrs, mrp, mis, mip, mnz, mns, mnp = create_filter_messages()

    # nd plots that accept numerical vectors of different length and filter individual elements
    methods = [
        up.matplotlib.box,
        up.matplotlib.histogram,
        up.matplotlib.violin,
        up.plotly.band,
        up.plotly.box,
        up.plotly.density,
        up.plotly.histogram,
        up.plotly.violin,
    ]
    for method in methods:
        # numerical
        emits_error(lambda: method([]), ValueError, 'The data contains zero vectors')
        emits_error(lambda: method([[]]), ValueError, 'only vectors with no elements')
        emits_no_warning(lambda: method([vn5]), caplog)
        emits_no_warning(lambda: method([vn5, vn6]), caplog)
        emits_no_warning(lambda: method([vn5, vn5]), caplog)
        emits_no_warning(lambda: method([vn5, vn6, vn5]), caplog)
        emits_warning(lambda: method([vf1]), caplog, mis.format(1))
        emits_warning(lambda: method([vn5, vf2]), caplog, mip.format(2))
        emits_warning(
            lambda: method([vf1, vf3, vn5]), caplog, mip.format(4))
        emits_warning(
            lambda: method([vf1, vf3, vf3, vn5]), caplog, mip.format(7))
        # categorical
        emits_error(lambda: method([vc1]), ValueError, mnz)
        emits_error(lambda: method([vc1, vc2]), ValueError, mnz)
        emits_warning(
            lambda: method([vc1, vf1, vf1]), caplog,
            [mns.format(1), mip.format(2)])
        emits_warning(
            lambda: method([vc1, vf2, vc2, vc1, vn5, vf1]), caplog,
            [mnp.format(3), mip.format(3)])

    # nd plots that accept numerical vectors with same length and filter entire rows
    methods = [
        up.matplotlib.scatter_matrix,
        up.plotly.parallel_coordinates,
        up.plotly.scatter_matrix,
    ]
    for method in methods:
        # numerical
        emits_error(lambda: method([]), ValueError, 'The data contains zero vectors')
        emits_error(lambda: method([[]]), ValueError, 'only vectors with no elements')
        emits_no_warning(lambda: method([vn5]), caplog)
        emits_error(lambda: method([vn5, vn6]), ValueError, 'vectors have the same length')
        emits_no_warning(lambda: method([vn5, vn5]), caplog)
        emits_warning(lambda: method([vf1]), caplog, mrs.format(1))
        emits_warning(lambda: method([vn5, vf2]), caplog, mrp.format(2))
        emits_warning(lambda: method([vf1, vf3, vn5]), caplog, mrp.format(3))
        # categorical
        emits_error(lambda: method([vc1]), ValueError, mnz)
        emits_error(lambda: method([vc1, vc2]), ValueError, mnz)
        emits_warning(
            lambda: method([vc1, vf1, vf1]), caplog,
            [mns.format(1), mrs.format(1)])
        emits_warning(
            lambda: method([vc1, vf2, vc2, vc1, vn5, vf1]), caplog,
            [mnp.format(3), mrp.format(2)])

    # nd plots that expect numerical or categorical vectors with same length
    methods = [
        up.javascript.parallel_coordinates_table,
        up.javascript.table,
    ]
    for method in methods:
        # numerical
        emits_error(lambda: method([]), ValueError, 'The data contains zero vectors')
        emits_error(lambda: method([[]]), ValueError, 'only vectors with no elements')
        emits_no_warning(lambda: method([vn5]), caplog)
        emits_error(lambda: method([vn5, vn6]), ValueError, 'vectors have the same length')
        emits_no_warning(lambda: method([vn5, vn5]), caplog)
        emits_warning(lambda: method([vf1]), caplog, mrs.format(1))
        emits_warning(lambda: method([vn5, vf2]), caplog, mrp.format(2))
        emits_warning(lambda: method([vf1, vf3, vn5]), caplog, mrp.format(3))
        # categorical
        emits_no_warning(lambda: method([vc1]), caplog)
        emits_no_warning(lambda: method([vc1, vc2]), caplog)
        emits_warning(
            lambda: method([vc1, vf1, vf1]), caplog, mrs.format(1))
        emits_warning(
            lambda: method([vc1, vf2, vc2, vc1, vn5, vf1]), caplog,
            mrp.format(2))


def test_prepare_graph_data():
    jgf_data = {
        "graph": {
          "directed": True,
          "metadata": {"arrowSize": 50, "arrowColor": "red"},
          "nodes": [
            {
              "id": "0",
            },
            {
              "id": "1",
            },
          ],
          "edges": [
            {
              "source": "0",
              "target": "1",
            },
          ]
        }
    }
    returned_data = shared_preprocessing.prepare_graph_data(jgf_data)
    assert returned_data
    assert isinstance(returned_data, list)
    assert returned_data == [jgf_data['graph']]

    filepath = os.path.join(IN_DIR, 'jgf_graph_single.json')
    returned_data = shared_preprocessing.prepare_graph_data(filepath)
    assert returned_data
    assert isinstance(returned_data, list)


@pytest.mark.parametrize('x, y, z, x_low, y_low, z_low, x_up, y_up, z_up', [
    # Minimal series of two values
    ([0, 100], [1000, 2000], [30000, 40000], -5, 950, 29500, 105, 2050, 40500),
    ([-50, 50], [-20, 80], [-120, -20], -55, -25, -125, 55, 85, -15),
    # Longer series
    ([50, 5, -50, 22], [3, 80, -20, 0, -3], [-70, -120, -20, -50], -55, -25, -125, 55, 85, -15),
])
def test_boundaries(x, y, z, x_low, y_low, z_low, x_up, y_up, z_up):
    x_res, y_res, z_res = shared_preprocessing.shift_away_from_extrema(x, y, z, direction='lower')
    assert x_res == x_low
    assert y_res == y_low
    assert z_res == z_low
    x_res, y_res, z_res = shared_preprocessing.shift_away_from_extrema(x, y, z, direction='upper')
    assert x_res == x_up
    assert y_res == y_up
    assert z_res == z_up


def test_categorical_to_numerical_basics():
    data_categorical = ['a', 'b', 'a', 'c', 'b', 'a', 'c']
    data_numerical, name_to_num_map = shared_preprocessing.categorical_to_numerical(
        data_categorical)
    assert data_numerical == [1, 2, 1, 3, 2, 1, 3]
    assert name_to_num_map == dict(a=1, b=2, c=3)

    given_name_to_num_map = dict(c=4, b=8)
    data_numerical, name_to_num_map = shared_preprocessing.categorical_to_numerical(
        data_categorical, given_name_to_num_map)
    assert data_numerical == [9, 8, 9, 4, 8, 9, 4]
    assert name_to_num_map == dict(a=9, b=8, c=4)

    given_name_to_num_map = dict(a=0, b=1, c=2, d=3)
    data_numerical, name_to_num_map = shared_preprocessing.categorical_to_numerical(
        data_categorical, given_name_to_num_map)
    assert data_numerical == [0, 1, 0, 2, 1, 0, 2]
    assert name_to_num_map == dict(a=0, b=1, c=2, d=3)


def test_categorical_to_numerical_order():
    data_categorical = ['a', 'c', 'a', 'c', 'b', 'a', 'c']
    data_numerical, name_to_num_map = shared_preprocessing.categorical_to_numerical(
        data_categorical)
    assert data_numerical == [1, 2, 1, 2, 3, 1, 2]
    assert name_to_num_map == dict(a=1, c=2, b=3)

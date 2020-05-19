import os

from shared_data_loading import IN_DIR
from unified_plotting.utilities import io, ode_solver


# Tests with pytest

def test_csv_loading_without_header_row():
    filepath = os.path.join(IN_DIR, 'uci_wine.csv')

    # default: check if a valid header row is present -> no -> no column names
    data, name = io.read_dsv_file(filepath)
    assert data[0][0] == 1.0
    assert len(data) == 14
    assert len(data[0]) == 178
    assert name == ['Series {}'.format(i) for i in range(1, 14+1)]

    # given_name: provided names as column names (header row part of data)
    given_name = [
        'Class', 'Alcohol', 'Malic acid', 'Ash', 'Alcalinity', 'Magnesium', 'Phenols',
        'Flavanoids', 'Nonflav.', 'Proanthoc.', 'Color int.', 'Hue', 'OD280/OD315', 'Proline']
    data, name = io.read_dsv_file(filepath, given_name)
    assert data[0][0] == 1.0
    assert len(data) == 14
    assert len(data[0]) == 178
    assert name == given_name

    # get_name_from_header=True: header row as column names
    data, name = io.read_dsv_file(filepath, get_name_from_header=True)
    assert data[0][0] == 1.0
    assert len(data) == 14
    assert len(data[0]) == 178 - 1
    assert name[0] == '1.0'

    # given_name AND get_name_from_header=True: header row as column names
    given_name = [
        'Class', 'Alcohol', 'Malic acid', 'Ash', 'Alcalinity', 'Magnesium', 'Phenols',
        'Flavanoids', 'Nonflav.', 'Proanthoc.', 'Color int.', 'Hue', 'OD280/OD315', 'Proline']
    data, name = io.read_dsv_file(filepath, given_name, get_name_from_header=True)
    assert data[0][0] == 1.0
    assert len(data) == 14
    assert len(data[0]) == 178 - 1
    assert name[0] == '1.0'


def test_csv_loading_with_header_row():
    filepath = os.path.join(IN_DIR, 'iris_with_header.csv')

    # default: check if a valid header row is present -> yes -> header row as column names
    data, name = io.read_dsv_file(filepath)
    assert data[0][0] == 5.1
    assert data[-1][0] == 'setosa'
    assert len(data) == 5
    assert len(data[0]) == 150
    assert name[0] == 'sepal_length'
    assert name[-1] == 'species'

    # given_name: provided names as column names (header row part of data)
    given_name = ['a', 'b', 'c', 'd', 'e']
    data, name = io.read_dsv_file(filepath, given_name)
    # assert data[0][0] == 'sepal_length'  # column gets converted to float, hence NaN is right
    assert data[0][1] == 5.1
    assert data[-1][0] == 'species'
    assert data[-1][1] == 'setosa'
    assert len(data) == 5
    assert len(data[0]) == 150 + 1
    assert name[0] == 'a'
    assert name[1] == 'b'
    assert name[2] == 'c'
    assert name[3] == 'd'
    assert name[-1] == 'e'

    # get_name_from_header=True: header row as column names
    data, name = io.read_dsv_file(filepath, get_name_from_header=True)
    assert data[0][0] == 5.1
    assert data[-1][0] == 'setosa'
    assert len(data) == 5
    assert len(data[0]) == 150
    assert name[0] == 'sepal_length'
    assert name[-1] == 'species'

    # given_name AND get_name_from_header=True: header row as column names
    given_name = ['a', 'b', 'c', 'd']
    data, name = io.read_dsv_file(filepath, given_name, get_name_from_header=True)
    assert data[0][0] == 5.1
    assert data[-1][0] == 'setosa'
    assert len(data) == 5
    assert len(data[0]) == 150
    assert name[0] == 'sepal_length'
    assert name[-1] == 'species'


def test_json_file_loading():
    filepath = os.path.join(IN_DIR, 'defaults.json')

    # default
    data = io.read_json_file(filepath)
    assert isinstance(data, dict)
    assert data


def test_ode_solver():
    import math

    def thomas_system(t, state_vector):
        x, y, z = state_vector
        b = 0.181
        dx = math.sin(y) - b*x
        dy = math.sin(z) - b*y
        dz = math.sin(x) - b*z
        state_vector_change = [dx, dy, dz]
        return state_vector_change

    state_start = [1, 4, 3.93]
    time_start = 0
    time_end = 500
    time_evaluation_points = list(range(500))
    for method in ['RK45', 'RK23', 'DOP853', 'Radau', 'BDF', 'LSODA']:
        for t_step_max in [None, 0.3]:
            for t_grid in [None, time_evaluation_points]:
                t, y = ode_solver.scipy(
                    thomas_system,
                    state_start,
                    time_start,
                    time_end,
                    t_step_max=t_step_max,
                    t_grid=t_grid)
                assert len(y[0]) == len(y[1]) == len(y[2]) == len(t) > 100
                if t_grid is not None:
                    assert len(t) == len(t_grid)

    def check_y_t(y, t, n):
        assert len(t) == n
        for y_i in y:
            assert len(y_i) == n

    # t_step
    for t_step in [0.95, 0.99, 1.0]:
        t, y = ode_solver.scipy(thomas_system, t_start=0, t_end=10, t_step=1, y_start=[1, 1, 1])
        check_y_t(y, t, 11)

    # t_step_max
    for t_step_max in [0.1]:
        t, y = ode_solver.scipy(
            thomas_system, t_start=0, t_end=10, t_step_max=t_step_max, y_start=[1, 1, 1])
        assert len(t) > 100
        y, t = ode_solver.scipy(thomas_system, t_start=0, t_end=10, y_start=[1, 1, 1])
        assert len(t) < 100

    # t_grid
    for t_grid in [[0, 1, 2, 3, 4, 5], [0, 2, 4, 6, 8, 10]]:
        t, y = ode_solver.scipy(thomas_system, t_start=0, t_end=10, t_grid=t_grid, y_start=[1, 1, 1])
        check_y_t(y, t, 6)

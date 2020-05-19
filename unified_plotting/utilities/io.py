"""Input/output operations for vector and graph data."""

import csv as _csv
import json as _json
from math import isnan as _isnan


def read_dsv_file(filepath, name=None, get_name_from_header=None, delimiter=','):
    """Read a delimiter-separated value file and provide it as vector data."""
    # Argument processing
    if not isinstance(filepath, str):
        raise ValueError('Filepath is not a string.')
    if not filepath:
        raise ValueError('Filepath is an empty string.')

    # Helper functions
    def convert_to_float_or_str(item):
        item = str(item).strip()
        try:
            return float(item)
        except Exception:
            pass
        return item

    def convert_to_float(item):
        try:
            return float(item)
        except Exception:
            return float('NaN')

    def convert_to_str(item):
        if isinstance(item, float) and _isnan(item):
            return ''
        return str(item)

    def parse_line(line, data, is_categorical):
        for i, item in enumerate(line):
            parsed_value = convert_to_float_or_str(item)
            if isinstance(parsed_value, str) and len(parsed_value) > 0:
                is_categorical[i] = True
            data[i].append(parsed_value)

    def dsv_file_to_vectors_and_names(filepath, name, get_name_from_header):
        # Read data and convert each field to float or otherwise str
        data = []
        with open(filepath) as file_handle:
            reader = _csv.reader(file_handle, delimiter=delimiter)
            # Read first line, possibly a header
            first_line = next(reader)
            is_categorical_fl = [False] * len(first_line)
            data = [[] for _ in range(len(first_line))]
            parse_line(first_line, data, is_categorical_fl)
            first_line_parsed = [data[i][0] for i in range(len(first_line))]
            # Read all other lines
            # is_categorical: only True if a non-empty string is found which can't be a float
            is_categorical = [False] * len(first_line)
            for line in reader:
                parse_line(line, data, is_categorical)

        # Check if a header row is present: Finds only cases where header is str and rest float
        header_detected = False
        for col_num in range(len(first_line)):
            header = first_line_parsed[col_num]
            column_values = data[col_num]
            if isinstance(header, str) and len(header) > 0:               # valid str in header
                if any(isinstance(val, float) for val in column_values):  # a valid float in rest
                    header_detected = True
                    break
        if get_name_from_header or \
                (header_detected and name is None and get_name_from_header is not False):
            name_from_header = [str(column_values[0]) for column_values in data]
            data = [column_values[1:] for column_values in data]
        else:
            name_from_header = ['Series {}'.format(i+1) for i in range(len(data))]
        if name is None or get_name_from_header:
            used_name = name_from_header
        else:
            used_name = []
            for i in range(len(first_line)):
                try:
                    assert not isinstance(name, str)
                    used_name.append(name[i])
                except Exception:
                    used_name.append('Series {}'.format(i+1))
        # Convert all values of a column to float or str
        for i, value in enumerate(is_categorical):
            if value:
                # Convert a categorical column to pure str values
                # => Some values that were recognized as valid float might become str again
                data[i] = [convert_to_str(item) for item in data[i]]
            else:
                # Convert a numerical column to pure float values
                # => Some values that were parsed as str (e.g. empty str) become float (e.g. NaN)
                data[i] = [convert_to_float(item) for item in data[i]]
        return data, used_name

    # Transformation
    try:
        data, name = dsv_file_to_vectors_and_names(filepath, name, get_name_from_header)
    except Exception:
        message = 'Failure during trying to read DSV file.'
        raise ValueError(message)
    return data, name


def read_json_file(filepath):
    """Read a JSON file and provide it as Python object."""
    # Argument processing
    if not filepath:
        raise ValueError('Filepath is empty.')
    if not isinstance(filepath, str):
        raise ValueError('Filepath is not a string.')

    # Transformation
    with open(filepath) as file_handle:
        data = _json.load(file_handle)
    return data

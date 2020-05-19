"""Template system for using HTML template files and inserting data into them."""

import json as _json

import numpy as _np
import pkg_resources as _pkg_resources


def load(resource_path):
    """Load a file in the same directory as the template system module."""
    resource_package = __name__
    binary_data = _pkg_resources.resource_string(resource_package, resource_path)
    string = binary_data.decode('utf-8')
    return string


def insert(template, data):
    """Insert data into a template."""
    for key, val in data.items():
        tag = '§' + key + '§'
        template = template.replace(tag, val)
    return template


def to_json(data):
    """Convert data to JSON."""
    return _json.dumps(data, cls=_NpEncoder)


class _NpEncoder(_json.JSONEncoder):
    # https://stackoverflow.com/questions/50916422/python-typeerror-object-of-type-int64-is-not-json-serializable/50916741
    def default(self, obj):
        if isinstance(obj, _np.integer):
            return int(obj)
        if isinstance(obj, _np.floating):
            return float(obj)
        if isinstance(obj, _np.ndarray):
            return obj.tolist()
        return super(_NpEncoder, self).default(obj)

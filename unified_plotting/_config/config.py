"""This is the module :py:mod:`unified_plotting.config <unified_plotting._config.config>`.

It provides a central configuration system for the
package :py:mod:`unified_plotting`.

Its main purpose is to provide **global package settings** that
determine the **basic style used in every plot**.
Each individual setting comes with a sensible default value that is
loaded during import of the package but can be altered by the user
during runtime. Once some settings were modified, they can also be
exported as JSON file and loaded again whenever desired.
In this way, user-defined styles can be created and reused.


Change the settings
-------------------

The current settings are stored in the object
:py:obj:`unified_plotting.config.settings`.

- Its members can be accessed and modified via dot notation,
  for example:

  .. code-block:: python

     import unified_plotting as up
     up.config.settings.x_labels_color = "#008800"
     up.config.settings.x_labels_fontname = "Arial"
     up.config.settings.y_labels_color = "#008800"
     up.config.settings.y_labels_fontname = "Arial"


Report the current settings
---------------------------

- The function :py:func:`unified_plotting.config.report`
  can be used to get a list of available options as well as their
  currently assigned values.

  .. code-block:: python

     import unified_plotting as up
     up.config.report()


Save and restore settings
-------------------------

The module :py:mod:`unified_plotting.config` contains following
functions that interact with the global package settings.
"""

import json as _json
import sys as _sys
from pprint import pprint as _pprint

from pkg_resources import resource_string as _resource_string

from ..utilities import operating_system as _operating_system


class _GenericSettings:
    """Helper class for automatical conversion between nested JSON data and nested Python objects.

    This allows to load settings from a JSON file and provide it as a
    nested object whose members can be accessed and set via simple
    dot notation.

    References
    ----------
    - https://stackoverflow.com/questions/43776223/converting-nested-json-into-python-object

    """

    @classmethod
    def _from_dict(cls, given_dict):
        obj = cls()
        obj.__dict__.update(given_dict)
        return obj

    @staticmethod
    def _to_dict(settings_obj):
        settings_json = _json.dumps(settings_obj, sort_keys=True, default=lambda obj: obj.__dict__)
        settings_dict = _json.loads(settings_json)
        return settings_dict

    def __str__(self):
        return str(self.__class__._to_dict(self))


def load_defaults():
    """Load default settings of this package.

    This function is called automatically when the package is loaded.

    """
    data_json_str = _resource_string(__name__, 'settings.json').decode()
    data = _json.loads(data_json_str, object_hook=_GenericSettings._from_dict)
    _THIS_MODULE.settings = data


def save_defaults_to_json(filepath):
    """Save the default settings of this package to a JSON file.

    It may be used as starting point to create a file with user-defined settings.
    Only the contained keys will be recognized and the values have to be valid JSON
    (e.g. true instead of Python's True, null instead of Python's None).

    Parameters
    ----------
    filepath : str
       Filepath of the created JSON file.
       If the file exists it will be overwritten without warning.
       If the path does not end with '.json' it will be changed to do so.
       If the parent directory does not exist it will be created.

    Returns
    -------
    filepath : str
        Filepath of the generated JSON file, guaranteed to end with ".json".

    """
    # Precondition
    filepath = _operating_system.ensure_file_extension(filepath, 'json')
    _operating_system.ensure_parent_directory(filepath)

    # Transformation
    data_json_str = _resource_string(__name__, 'settings.json').decode()
    with open(filepath, 'w') as file_handle:
        file_handle.write(data_json_str)
    return filepath


def load_from_json(filepath):
    """Load settings from a JSON file.

    Parameters
    ----------
    filepath : str
        Filepath of the JSON file that contains the settings.

    """
    with open(filepath, 'r') as file_handle:
        data = _json.load(file_handle, object_hook=_GenericSettings._from_dict)
    _THIS_MODULE.settings = data


def save_to_json(filepath):
    """Save the current settings to a JSON file.

    It can be used to load the same settings in another session.

    Parameters
    ----------
    filepath : str
        Filepath of the created JSON file.
        If the file exists it will be overwritten without warning.
        If the path does not end with '.json' it will be changed to do so.
        If the parent directory does not exist it will be created.

    Returns
    -------
    filepath : str
        Filepath of the generated JSON file, guaranteed to end with ".json".

    """
    # Precondition
    filepath = _operating_system.ensure_file_extension(filepath, 'json')
    _operating_system.ensure_parent_directory(filepath)

    # Transformation
    data = _THIS_MODULE.settings
    with open(filepath, 'w') as file_handle:
        _json.dump(data, file_handle, indent=4, sort_keys=True, default=lambda obj: obj.__dict__)
    return filepath


def report():
    """Print a report of the current settings."""
    settings_obj = _THIS_MODULE.settings
    settings_dict = _GenericSettings._to_dict(settings_obj)
    _pprint(settings_dict)


# https://stackoverflow.com/questions/1977362/how-to-create-module-wide-variables-in-python
_THIS_MODULE = _sys.modules[__name__]
_THIS_MODULE.settings = None
load_defaults()

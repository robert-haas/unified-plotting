"""This is a central logging system for this package.

It provides the single point where calls are made to
Python's built-in logging system to ensure consistency.

References
----------
- https://docs.python.org/3/howto/logging.html
- https://docs.python.org/3/howto/logging-cookbook.html

"""

import logging as _logging


FORMATTER = _logging.Formatter('%(name)s: %(levelname)s: %(message)s')

STREAMHANDLER = _logging.StreamHandler()
STREAMHANDLER.setFormatter(FORMATTER)

LOGGER = _logging.getLogger('unified_plotting')
LOGGER.setLevel(_logging.INFO)
LOGGER.addHandler(STREAMHANDLER)


def warn_user(message):
    """General warning displayed to the user."""
    LOGGER.warning(message)


def report_missing_library(library_name, exception):
    """Warning to the user about missing library."""
    message = ('ImportError during loading of {}. Plots with this library are not '
               'available.\nError message: {}'.format(library_name, exception))
    LOGGER.warning(message)


def report_inactive_argument(argument_name):
    """Warning to the user about provided argument that is ignored by the function."""
    message = 'The argument "{}" is currently inactive in this plot type.'.format(argument_name)
    LOGGER.warning(message)


def report_unknown_kwargs(kwargs):
    """Warning to the user about provided arguments that are unknown and ignored."""
    kwargs_str = ', '.join('"{}"'.format(item) for item in kwargs)
    message = 'Following arguments are unknown and ignored: {}'.format(kwargs_str)
    LOGGER.warning(message)


def report_failed_plot(plot_name):
    """Warning to the user about a plot that failed perhaps due to incorrect data format."""
    message = (
        'Plotting with function "{}" failed for some reason. '
        'Is the provided data in the correct format?').format(plot_name)
    raise ValueError(message)

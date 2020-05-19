"""Waitress server for serving the Flask app."""

import logging as _logging

import waitress as _waitress

from ._flask_app import MY_FLASK_APP as _MY_FLASK_APP


def start(address, port, num_workers):
    """Serve the Flask app with waitress at a provided address and port."""
    logger = _logging.getLogger('waitress')
    logger.setLevel(_logging.ERROR)
    print()
    print()
    message = 'Output from Waitress while serving a Flask app'
    print(message)
    print('-' * len(message))
    _waitress.serve(_MY_FLASK_APP, host=address, port=port, threads=num_workers)

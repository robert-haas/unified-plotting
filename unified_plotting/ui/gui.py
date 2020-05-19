"""Entry point for serving a web app to provide a browser-based GUI."""

import argparse as _argparse
import multiprocessing as _multiprocessing
import random as _random
import socket as _socket

from . import _waitress_server


def _get_number_of_workers():
    """Check how many CPUs are available on the system and get a suitable number of workers."""
    return _multiprocessing.cpu_count() * 2


def _check_port_is_free(address, port):
    """Check if a port is free and can be used.

    References
    ----------
    - https://www.reddit.com/r/learnpython/comments/2i4qrj/how_to_write_a_python_script_that_checks_to_see/

    """
    with _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM) as skt:
        try:
            skt.bind((address, port))
            return True
        except OSError:
            return False


def _get_random_port(min_val, max_val):
    """Get a random port between a minimum and maximum value (included)."""
    return _random.randint(min_val, max_val)


def _get_random_free_port(address, min_val, max_val, num_tries=50):
    """Find a free random port in a given range and with a limited number of tries."""
    for _ in range(num_tries):
        port = _get_random_port(min_val, max_val)
        if _check_port_is_free(address, port):
            break
    else:
        message = 'Failed to find a free port for serving the app.'
        raise ValueError(message)
    return port


def _parse_arguments():
    parser = _argparse.ArgumentParser(prog='unified_plotting')
    parser.add_argument(
        '--address',
        '-a',
        type=str,
        default='127.0.0.1',
        required=False,
        help='IP address (default: 127.0.0.1)',
    )
    parser.add_argument(
        '--port',
        '-p',
        type=int,
        default=-1,
        required=False,
        help='Port (default: -1, selects a random free port between 49000 and 50000)',
    )
    args = parser.parse_args()
    return args.address, args.port


def main():
    """Provide the entry point for starting the GUI via command line."""
    # Argument processing
    try:
        address, port = _parse_arguments()
    except Exception:
        address, port = '127.0.0.1', -1
    if port == -1:
        port = _get_random_free_port(address, min_val=49000, max_val=50000)
    num_workers = _get_number_of_workers()

    # Start web-app
    print('Starting the web interface of unified plotting.')
    print('You can access it now with a browser at http://{}:{}'.format(address, port))
    _waitress_server.start(address, port, num_workers)

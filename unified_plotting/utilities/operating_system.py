"""Simple, central access to operating system functionality."""

import atexit as _atexit
import logging as _logging
import os as _os
import random as _random
import re as _re
import shutil as _shutil
import subprocess as _subprocess
import sys as _sys
import tempfile as _tempfile
import threading as _threading
import webbrowser as _webbrowser
from datetime import datetime as _datetime
from distutils import dir_util as _dir_util

import flask as _flask


# Construction of texts

def command_builder(program_name, arguments=None, keyword_arguments=None, assignment_symbol='='):
    """Create a shell command from name, args and kwargs."""
    # Argument processing
    if arguments is None:
        arguments = []
    if keyword_arguments is None:
        keyword_arguments = []

    # Transformation
    cmd = program_name
    for arg in arguments:
        cmd += ' ' + str(arg)
    for key, value in keyword_arguments.items():
        if value is not None:
            cmd += ' ' + str(key) + assignment_symbol + str(value)
    return cmd


def ensure_file_extension(filepath, extension):
    """Ensure that a filepath ends with a given extension.

    References
    ----------
    - https://docs.python.org/3.8/library/os.path.html#os.path.splitext

    """
    # Precondition
    if not filepath:
        raise ValueError('Invalid filepath: "{}"'.format(filepath))
    if not extension:
        raise ValueError('Invalid extension: "{}"'.format(filepath))
    if not extension.startswith('.'):
        extension = '.' + extension

    # Transformation
    if not filepath.endswith(extension):
        filepath += extension

    # Postcondition
    if not filepath or not isinstance(filepath, str):
        raise ValueError('Could not create a valid filepath: "{}"'.format(filepath))
    return filepath


def ensure_new_directory_name(path):
    """Check whether a given path exists and if yes try to find an increment variant not yet used.

    Caution: Not threadsafe.
    """
    while _os.path.exists(path):
        parse_result = _re.search(r'(.*?)(\d+)$', path)
        if parse_result:
            starting_text = parse_result.group(1)
            ending_number = int(parse_result.group(2)) + 1
        else:
            starting_text = path
            ending_number = 2
        path = starting_text + str(ending_number)
    return path


def inject_system_info(text):
    """Given a string that contains 0 to n variables inside {}, try to inject current information.

    Examples
    --------
    - '{date}_{time}_out' gives '2018-01-31_13:14:15_out'

    """
    # Precondition
    if not isinstance(text, str):
        raise ValueError('Given data is not a string: {}'.format(text))

    # Transformation
    if '{date}' in text:
        current_date = _datetime.now().strftime("%Y-%m-%d")
        text = text.replace('{date}', current_date)
    if '{time}' in text:
        current_time = _datetime.now().strftime("%I-%M-%S")
        text = text.replace('{time}', current_time)
    return text


def string_to_vaild_path(string):
    """Turn a string into a valid path.

    Conversion steps:
    - Replaces non-alphanumeric characters with an underscore
    - Replaces repetitive underscores by a single underscore
    - Removes leading and trailing underscores

    References
    ----------
    - https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    - https://stackoverflow.com/questions/10072744/remove-repeating-characters-from-words

    """
    path = ''.join(letter if letter.isalnum() else '_' for letter in string)
    path = _re.sub(r'(_)\1+', r'\1', path)
    path = path.strip('_')
    if not path:
        raise ValueError('Could not create a valid path from string "{}"'.format(string))
    return path


# Requests about operating system objects

def get_current_working_directory():
    """Get the current working directory.

    References
    ----------
    - https://docs.python.org/3/library/os.html#os.getcwd

    """
    return _os.getcwd()


def get_directory_name(dirpath):
    """Extract the top-most directory from a full dirpath.

    References
    ----------
    - https://stackoverflow.com/questions/3925096/how-to-get-only-the-last-part-of-a-path-in-python

    """
    return _os.path.basename(_os.path.normpath(dirpath))


def get_file_extension(filepath):
    """Get the file extension from a filepath."""
    _, ext = _os.path.splitext(filepath)
    return ext


def get_file_name(filepath):
    """Extract the filename from a full filepath.

    References
    ----------
    - https://stackoverflow.com/questions/3925096/how-to-get-only-the-last-part-of-a-path-in-python

    """
    return _os.path.basename(_os.path.normpath(filepath))


def get_parent_directory(filepath):
    """Get the parent directory of a file from its filepath.

    References
    ----------
    - https://docs.python.org/2/library/os.path.html#os.path.dirname

    """
    return _os.path.dirname(filepath)


def is_nonempty_file(filepath, raise_exception=False, message=None):
    """Check if a file exists and is non-empty.

    References
    ----------
    - https://docs.python.org/3/library/os.html#os.DirEntry.is_file
    - https://docs.python.org/3/library/os.path.html#os.path.getsize

    """
    # Positive
    try:
        if _os.path.isfile(filepath):
            if _os.path.getsize(filepath) > 0:
                return True
    except Exception:
        pass
    # Negative
    if raise_exception:
        error_msg = 'Invalid file (not existing or empty): "{}"'.format(filepath)
        if message is not None:
            error_msg += '\n' + message
        raise ValueError(error_msg)
    return False


def is_nonempty_directory(dirpath, raise_exception=False, message=None):
    """Check if a directory exists and is non-empty.

    References
    ----------
    - https://docs.python.org/3/library/os.html#os.DirEntry.is_dir
    - https://docs.python.org/3/library/os.html#os.listdir

    """
    # Positive
    try:
        if _os.path.isdir(dirpath):
            if _os.listdir(dirpath):
                return True
    except Exception:
        pass
    # Negative
    if raise_exception:
        error_msg = 'Invalid directory (not existing or empty): "{}"'.format(dirpath)
        if message is not None:
            error_msg += '\n' + message
        raise ValueError(error_msg)
    return False


def is_shell_variable_set(variable, raise_exception=False):
    """Check if a shell environment variable is set.

    References
    ----------
    - https://docs.python.org/3/library/os.html#os.environ
    - https://stackoverflow.com/questions/40697845/what-is-a-good-practice-to-check-if-an-environmental-variable-exists-or-not

    """
    is_set = variable in _os.environ
    if raise_exception:
        if not is_set:
            raise ValueError('Environment variable "{}" is not set on your system.'.format(
                variable))
    return is_set


def is_shell_command_known(command, raise_exception=False):
    """Check if a string is a known shell command.

    References
    ----------
    - https://docs.python.org/3.8/library/shutil.html#shutil.which
    - https://stackoverflow.com/questions/592620/check-if-a-program-exists-from-a-bash-script

    """
    if _shutil.which(command) is None:
        if raise_exception:
            raise ValueError('Shell command "{}" is not available on your system.'.format(command))
        return False
    return True


def relative_to_absolute_path(relative_filepath):
    """Convert a relative filepath to an absolute one.

    References
    ----------
    - https://docs.python.org/3.8/library/os.path.html#os.path.abspath

    """
    return _os.path.abspath(relative_filepath)


# Manipulate operating system objects

def change_to_directory(dirpath):
    """Change the current working directory to a given dirpath.

    References
    ----------
    - https://docs.python.org/3/library/os.html#os.chdir

    """
    _os.chdir(dirpath)


def copy_directory(source_dirpath, target_dirpath):
    """Copy a directory from a source to a target destination.

    Caution: In case of existence, an overwrite happens without warning.

    References
    ----------
    - https://docs.python.org/3/library/shutil.html#shutil.copytree
    - https://docs.python.org/3/distutils/apiref.html#distutils.dir_util.copy_tree
    - https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth

    """
    # Precondition: Source directory exists
    if not _os.path.isdir(source_dirpath):
        raise ValueError('Source directory "{}" is not a directory.'.format(source_dirpath))

    # Transformation
    # _shutil.copytree(source_dirpath, target_dirpath)   # overwriting not possible
    _dir_util.copy_tree(source_dirpath, target_dirpath)  # overwriting supported

    # Postcondition: Target directory exists
    if not _os.path.isdir(target_dirpath):
        raise ValueError('Target directory "{}" was not created.'.format(target_dirpath))


def copy_file(source_filepath, target_filepath):
    """Copy a file from a source filepath to a target filepath, possibly renaming it.

    Caution: In case of existence, an overwrite happens without warning.

    References
    ----------
    - https://docs.python.org/3/library/shutil.html#shutil.copyfile

    """
    # Precondition: Source file and target directory exist
    if not _os.path.isfile(source_filepath):
        raise ValueError('Source "{}" is not a file.'.format(source_filepath))
    ensure_parent_directory(target_filepath)

    # Transformation
    try:
        _shutil.copyfile(source_filepath, target_filepath)
    except _shutil.SameFileError:
        pass

    # Postcondition: Target file exists
    if not _os.path.isfile(target_filepath):
        raise ValueError('Target file "{}" was not created.'.format(target_filepath))


def create_directory(dirpath):
    """Given a directory path, create it and all necessary parent directories.

    Do nothing if the directory already exists.

    References
    ----------
    - https://docs.python.org/2/library/os.html#os.makedirs

    """
    _os.makedirs(dirpath, exist_ok=True)
    return dirpath


def create_new_directory(dirpath):
    """Given a directory path, create a new directory path with incremented end number."""
    # TODO: refactor, possibly delete
    # TODO: this can lead to confusion! especially the need to consider the return value

    dirpath = ensure_new_directory_name(dirpath)
    _os.makedirs(dirpath)
    return dirpath


def create_unique_directory(dirpath, prefix=None):
    """Create a new unique directory."""
    # TODO: refactor, possibly delete

    # Precondition
    parent_directory = dirpath
    create_directory(parent_directory)

    # Transformation
    dirpath = _tempfile.mkdtemp(prefix=prefix, dir=parent_directory)
    return dirpath


def create_temporary_directory(prefix=None):
    """Create a temporary directory that is deleted at the end of normal program execution.

    Notes
    -----
    Every created directory lies within a common parent folder.

    References
    ----------
    - https://stackoverflow.com/questions/13379742/right-way-to-clean-up-a-temporary-folder-in-python-class
    - https://stackoverflow.com/questions/6884991/how-to-delete-dir-created-by-python-tempfile-mkdtemp

    """
    # Precondition
    parent_directory = '_temporary_files'
    create_directory(parent_directory)

    # Transformation
    dirpath = _tempfile.mkdtemp(prefix=prefix, dir=parent_directory)
    dirpath_absolute = _os.path.abspath(dirpath)

    # Postcondition
    def rm_temp_dir(dirpath):
        delete_directory(dirpath)

    execute_at_program_exit(rm_temp_dir, parent_directory)
    return dirpath_absolute


def delete_directory(dirpath):
    """Delete a directory which may have contents in it, or write a warning if it does not exist.

    References
    ----------
    - https://docs.python.org/3/library/shutil.html#shutil.rmtree

    """
    try:
        _shutil.rmtree(dirpath)
    except FileNotFoundError:
        pass


def delete_file(filepath):
    """Delete a file.

    References
    ----------
    - https://docs.python.org/3/library/os.html#os.remove

    """
    _os.remove(filepath)


def ensure_parent_directory(filepath):
    """Given a filepath, make sure that its parent directory exists.

    The aim is to allow the creation of a file without facing any directory problems.
    """
    # Precondition
    parent_dirpath = _os.path.dirname(_os.path.realpath(filepath))

    # Transformation
    create_directory(parent_dirpath)


def execute_at_program_exit(function, *args, **kwargs):
    """Execute a function at program exit, e.g. to remove temporary files.

    Notes
    -----
    It is not executed in every possible case of program exit because
    it seems hardly possible to do so in Python.

    References
    ----------
    - https://docs.python.org/3/library/atexit.html#atexit.register
    - http://grodola.blogspot.com/2016/02/how-to-always-execute-exit-functions-in-py.html
    - https://github.com/lucasvickers/python-sigterm

    """
    _atexit.register(function, *args, **kwargs)


def move_file(source_filepath, target_filepath):
    """Transform a file from a source filepath to a target filepath, possibly renaming it.

    References
    ----------
    - https://docs.python.org/3/library/shutil.html#shutil.move

    """
    # Precondition: Source file and target directory exist
    if not _os.path.isfile(source_filepath):
        raise ValueError('Source "{}" is not a file.'.format(source_filepath))
    ensure_parent_directory(target_filepath)

    # Transformation
    _shutil.move(source_filepath, target_filepath)

    # Postcondition: Target file exists
    if not _os.path.isfile(target_filepath):
        raise ValueError('Target file "{}" was not created.'.format(target_filepath))


# Run programs

def open_url_or_file_in_webbrowser(data):
    """Open an URL or file in the default webbrowser.

    References
    ----------
    - https://docs.python.org/3/library/webbrowser.html#webbrowser.open

    """
    # Precondition: URL is valid
    if isinstance(data, str) and data.startswith('www.'):
        data = 'http://' + data
    try:
        if _os.path.isfile(data):
            data = 'file://' + _os.path.abspath(data)
    except Exception:
        pass

    # Transformation
    _webbrowser.open(data)


def open_html_text_in_webbrowser(data):
    """Open HTML text in the default webbrowser.

    A short-lived HTTP server is created that serves only one request to show the HTML text
    in the webbrowser. The alternative would be to write the HTML text to a temporary file
    and open this file in the webbrowser.

    References
    ----------
    - https://stackoverflow.com/questions/54141751/how-to-disable-flask-app-run-s-default-message
    - https://stackoverflow.com/questions/14888799/disable-console-messages-in-flask-server

    """
    def mute_werkzeug():
        try:
            log = _logging.getLogger('werkzeug')
            log.disabled = True
        except Exception:
            pass

    def mute_flask():
        try:
            cli = _sys.modules['flask.cli']
            cli.show_server_banner = lambda *x: None
        except Exception:
            pass

    def shutdown_werkzeug():
        func = _flask.request.environ.get('werkzeug.server.shutdown')
        if func is None:
            message = 'Can not stop Flask app, because it is not running on a Werkzeug server.'
            raise RuntimeError(message)
        func()

    my_flask_app = _flask.Flask(__name__)

    @my_flask_app.route('/', methods=['GET', 'POST'])
    def index():
        shutdown_werkzeug()
        return data

    def run_app(port):
        my_flask_app.run(port=port, debug=False)

    mute_werkzeug()
    mute_flask()
    for _ in range(5):
        try:
            random_port = 5000 + _random.randint(0, 999)
            url = 'http://127.0.0.1:{}'.format(random_port)
            _threading.Timer(0.5, lambda: _webbrowser.open(url)).start()
            run_app(random_port)
            break
        except Exception:
            pass


def run_command(cmd):
    """Execute a shell command.

    Notes
    -----
    This function starts a new process. This can be a problem,
    e.g. on cluster with cluster manager.

    References
    ----------
    - https://docs.python.org/3/library/subprocess.html#subprocess.run
    - https://docs.python.org/3/library/os.html#os.system

    """
    output = _subprocess.run(
        cmd, shell=True, check=True, stdout=_subprocess.PIPE, universal_newlines=True)
    stdout = output.stdout
    if isinstance(stdout, str):
        stdout = stdout.rstrip()
    stderr = output.stderr
    if isinstance(stderr, str):
        stdout = stderr.rstrip()
    return stdout, stderr


class SuppressStdoutStderr():
    """A context manager for doing a "deep suppression" of stdout and stderr in Python.

    Notes
    -----
    - It will suppress all print statements, even if the print originates in a compiled
      C/Fortran function.
    - It will not suppress raised exceptions, since exceptions are printed to stderr just before
      a script exits, and after the context manager has exited.

    References
    ----------
    - https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functions

    """

    def __init__(self):
        """Create an instance of a context manager for output suppression."""
        # Open a pair of null files
        self.null_file_descriptors = [_os.open(_os.devnull, _os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_file_descriptors = [_os.dup(1), _os.dup(2)]

    def __enter__(self):
        """Start using the context manager."""
        # Assign the null pointers to stdout and stderr.
        _os.dup2(self.null_file_descriptors[0], 1)
        _os.dup2(self.null_file_descriptors[1], 2)

    def __exit__(self, *_):
        """Stop using the context manager."""
        # Re-assign the real stdout/stderr back to (1) and (2)
        _os.dup2(self.save_file_descriptors[0], 1)
        _os.dup2(self.save_file_descriptors[1], 2)
        # Close all file descriptors
        for file_descriptor in self.null_file_descriptors + self.save_file_descriptors:
            _os.close(file_descriptor)

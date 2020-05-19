"""Machinery for injecting shared arguments into plotting functions."""

from inspect import signature as _signature

from .._config import config as _config


def _get_arg_lists(func):
    """Get all arguments (+default values) of a function by inspecting its signature.

    Caution: It fails if an argument has assigned an iterable like a list as default value.
             This should be avoided in Python anyways.

    """
    args_complete = str(_signature(func)).lstrip('(').rstrip(')').split(', ')
    args_without_varargs_and_varkw = [arg for arg in args_complete if not arg.startswith('*')]
    args = [arg.split('=')[0] for arg in args_without_varargs_and_varkw]
    args_with_values = args_without_varargs_and_varkw
    args_with_variables = [arg+'='+arg for arg in args]
    return args, args_with_values, args_with_variables


def inject_functions(*functions):
    """Inject arguments and documentation from one function into another.

    Notes
    -----
    - Related concept: https://en.wikipedia.org/wiki/Dependency_injection#Interface_injection

    References
    ----------
    - https://docs.python.org/3/library/functions.html#compile
    - https://docs.python.org/3/library/functions.html#eval
    - https://github.com/python/cpython/blob/master/Lib/functools.py (see update_wrapper)

    """
    def injection_decorator(f_ori):
        # Collect arguments for newly created function
        _, args_ori_with_vals, args_ori_with_vars = _get_arg_lists(f_ori)
        args_inj, args_inj_with_vals, args_inj_with_vars = [], [], []
        docs_inj = []
        for f_inj in functions:
            args, args_with_vals, args_with_vars = _get_arg_lists(f_inj)
            args_inj.extend(args)
            args_inj_with_vals.extend(args_with_vals)
            args_inj_with_vars.extend(args_with_vars)
            docs_inj.append(f_inj.__doc__.strip('\n'))
        args_comb_with_vals = ', '.join(args_ori_with_vals + args_inj_with_vals + ['**kwargs'])
        args_comb_with_vars = ', '.join(args_ori_with_vars + args_inj_with_vars + ['**kwargs'])

        # Create new function
        f_comb_name = f_ori.__name__
        f_comb_str = 'def {}({}):\n    return f_ori({})'.format(
            f_comb_name, args_comb_with_vals, args_comb_with_vars)
        f_comb_code = compile(f_comb_str, filename='<combined_function_compiler>', mode='exec')
        eval_locals = dict()
        eval_globals = {'f_ori': f_ori}
        eval(f_comb_code, eval_globals, eval_locals)  # pylint: disable=eval-used
        f_comb = eval_locals[f_comb_name]

        # Update properties of new function from original function (similar to functools.wraps)
        for attr in ('__module__', '__qualname__', '__annotations__'):
            try:
                value = getattr(f_ori, attr)
            except AttributeError:
                pass
            else:
                setattr(f_comb, attr, value)
        for f_inj in functions:
            f_comb.__dict__.update(f_inj.__dict__)

        # Update docs of new function by all docs of injected functions
        if f_ori.__doc__:
            f_comb.__doc__ = '\n'.join([f_ori.__doc__] + docs_inj)
        else:
            message = 'Injection failed: Original function needs to have a doc string.'
            raise ValueError(message)
        return f_comb
    return injection_decorator


def _parse_spec_kwargs(spec_function, kwargs, preserving=False):
    """Get certain arguments (specified by a function) from a kwargs list and return them."""
    args, _, _ = _get_arg_lists(spec_function)
    given = dict()
    for arg in args:
        # Case 1: The value is contained in kwargs => Use it (and optionally remove it)
        if preserving:
            given[arg] = kwargs[arg]
        else:
            given[arg] = kwargs.pop(arg)
        # Case 2: The value is not contained in kwargs or None => Use a default from settings
        if given[arg] is None:
            try:
                given[arg] = getattr(_config.settings, arg)
            except AttributeError:
                pass
    return given


def _remove_spec_kwargs(spec_function, kwargs):
    """Remove certain arguments (specified by a function) from a kwargs list."""
    args, _, _ = _get_arg_lists(spec_function)
    for arg in args:
        kwargs.pop(arg)
    return kwargs

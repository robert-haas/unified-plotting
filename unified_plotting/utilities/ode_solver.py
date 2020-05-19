"""Integration methods for solving initial-value problems of ODEs."""

from numpy import arange as _arange
from scipy.integrate import solve_ivp as _solve_ivp


def scipy(rhs_function, y_start, t_start, t_end, t_step=None, t_step_max=None, t_grid=None,
          method='RK45'):
    """Solve an ODE initial value problem with some integration method implemented in SciPy.

    Parameters
    ----------
    rhs_function : function
    y_start : float
        Initial state y, a vector (y1, y2, y3, ...) of all system variables.
    t_start : float
        Start time.
    t_end : float
        End time.
    t_step : float
        Step size between two points in time.
        It is translated into a uniform grid passed to t_grid
        and overrules any value passed to t_grid.
    t_step_max : float
        Maximum step size between two points in time.
        If not provided, it is automatically chosen by the integrator.
    t_grid : list of float
        Time points at which the computed result shall be stored.
        Each point must lie in the interval between t_start and t_end.
        If not provided, the solver chooses the points.
    method: str
        Integration method used to solve the initial value problem. Possible values:

        - 'RK45': Explicit Runge-Kutta method of order 5.
        - 'RK23': Explicit Runge-Kutta method of order 3.
        - 'DOP853': Explicit Runge-Kutta method of order 8.
        - 'Radau': Implicit Runge-Kutta method of the Radau IIA family of order 5.
        - 'BDF': Implicit multi-step variable-order (1 to 5) method based on a
          backward differentiation formula for the derivative approximation.
        - 'LSODA': Adams/BDF method with automatic stiffness detection and switching.

    Returns
    -------
    States and times : tuple (state_sequence, time_sequence)
        The result of the integration. A sequence of states y (=list of sequences for each
        system variable y0 to yn) and a sequence of time points at which these states
        were calculated.

    References
    ----------
    - https://docs.scipy.org/doc/scipy/reference/integrate.html#solving-initial-value-problems-for-ode-systems
    - https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html#scipy.integrate.solve_ivp

    """
    # Argument processing
    if t_step:
        t_grid = _arange(t_start, t_end+10e-10, t_step)
    kwargs = dict()
    if t_step_max is not None:
        kwargs['max_step'] = t_step_max
    if t_grid is not None:
        kwargs['t_eval'] = t_grid

    # Transformation
    result = _solve_ivp(
        fun=rhs_function,
        t_span=(t_start, t_end),
        y0=y_start,
        method=method,
        **kwargs
    )

    # Postcondition
    if result.status != 0:
        status_name = 'Unknown'
        if result.status == -1:
            status_name = 'Integration step failed'
        elif result.status == 1:
            status_name = 'A termination event occurred'
        message = 'Integration failed with status "{}"'.format(status_name)
        raise ValueError(message)
    return result.t, result.y

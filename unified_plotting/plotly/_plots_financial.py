"""Plotly plots for financial (OHLCV) data."""

import plotly.graph_objs as _go

from .._unified_arguments import arguments as _args
from .._unified_arguments import shared_preprocessing as _shared_preprocessing
from .._unified_arguments import shared_processing as _shared_processing
from .._unified_arguments.injection import inject_functions as _inject_functions
from . import _plotly_processing
from ._data_structures import Figure as _Figure


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid)
def candlestick(x, open, high, low, close, opacity=None, **kwargs):
    """Create a candlestick plot for financial data.

    Parameters
    ----------
    x : list
        Numerical data represented by the x-Axis.
    open : list
        Numerical data represented by the y-Axis as top of a green or bottom of a red candle.
    high : list
        Numerical data represented by the y-Axis as top of the stick.
    low : list
        Numerical data represented by the y-Axis as bottom of the stick.
    close : list
        Numerical data represented by the y-Axis as bottom of a green or top of a red candle.
    opacity : float
        Opacity of the plot elements, in this case the contour areas.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting
    the plot.

    References
    ----------
    - https://en.wikipedia.org/wiki/Candlestick_chart
    - https://plot.ly/python/reference/#candlestick

    Examples
    --------
    - https://plot.ly/python/candlestick-charts

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    data = [x, open, high, low, close]
    data, _ = _shared_preprocessing.prepare_vector_data_nd(
        data, None, remove_non_numerical_vectors=False)
    x, open, high, low, close = data

    # Layout
    layout = _go.Layout()
    size_spec = _plotly_processing.set_plot_size(kwargs, layout)
    _plotly_processing.set_plot_color(kwargs, layout)
    _plotly_processing.set_title(kwargs, layout)
    _plotly_processing.set_x_axis(kwargs, layout)
    _plotly_processing.set_y_axis(kwargs, layout)
    _plotly_processing.set_grid(kwargs, layout)

    # Data
    opacity_i = _shared_processing.get_next_opacity(opacity, i=0)

    trace = _go.Candlestick(
        x=x,
        open=open,
        high=high,
        low=low,
        close=close,
        opacity=opacity_i,
    )
    data = [trace]

    # Figure
    fig = _go.Figure(data=data, layout=layout)
    return _Figure(fig, **size_spec)


@_inject_functions(_args.plot_size_and_resolution, _args.plot_color, _args.plot_title,
                   _args.x_axis, _args.y_axis, _args.x_grid, _args.y_grid,
                   _args.legend)
def ohlc(x, open, high, low, close, opacity=None, **kwargs):
    """Create an OHLC plot for financial data.

    Parameters
    ----------
    x : list
        A list of numbers or if ``x_axis_scale="categorical"`` a list of strings.
    open : list
        A list of numbers represented by the y-Axis as left tick of the line.
    high : list
        A list of numbers represented by the y-Axis as top of the line.
    low : list
        A list of numbers represented by the y-Axis as bottom of the line.
    close : list
        A list of numbers represented by the y-Axis as right tick of the line.
    opacity : float
        Opacity of the plot elements, in this case the contour areas.
        Possible values: Between 0.0 (=completely transparent) and 1.0 (=completely opaque).

    Returns
    -------
    A :ref:`Figure <plotly-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://en.wikipedia.org/wiki/Open-high-low-close_chart
    - https://plot.ly/python/reference/#ohlc

    Examples
    --------
    - https://plot.ly/python/ohlc-charts

    **Further parameters that are unified across plots and libraries**

    """
    # Shared argument processing
    kwargs = _shared_preprocessing.check_and_filter_kwargs(kwargs)
    data = [x, open, high, low, close]
    data, _ = _shared_preprocessing.prepare_vector_data_nd(
        data, None, remove_non_numerical_vectors=False)
    x, open, high, low, close = data

    # Layout
    layout = _go.Layout()
    size_spec = _plotly_processing.set_plot_size(kwargs, layout)
    _plotly_processing.set_plot_color(kwargs, layout)
    _plotly_processing.set_title(kwargs, layout)
    _plotly_processing.set_x_axis(kwargs, layout)
    _plotly_processing.set_y_axis(kwargs, layout)
    _plotly_processing.set_grid(kwargs, layout)

    # Data
    opacity_i = _shared_processing.get_next_opacity(opacity, i=0)

    _plotly_processing.set_legend(kwargs, layout)
    trace = _go.Ohlc(
        x=x,
        open=open,
        high=high,
        low=low,
        close=close,
        opacity=opacity_i,
    )
    data = [trace]

    # Figure
    fig = _go.Figure(data=data, layout=layout)
    return _Figure(fig, **size_spec)

"""This is the subpackage :py:mod:`unified_plotting.plotly`.

It provides interactive plots based on `Plotly <https://plot.ly/>`__.
Its main purpose is to enable easier access to the rich plotting
capabilities of this Python library by providing a simple, unified,
high-level API for many plot types.

It contains the following modules and plotting functions.
"""

from .. import _logging


try:
    __all__ = [
        'band',
        'bar',
        'box',
        'candlestick',
        'contour',
        'density',
        'density_2d',
        'heatmap',
        'histogram',
        'histogram_2d',
        'density_scatter_histogram_2d',
        'ohlc',
        'parallel_coordinates',
        'scatter',
        'scatter_3d',
        'scatter_matrix',
        'surface',
        'violin',
        'Figure',
    ]

    # Plot imports
    from ._plots_2d import bar
    from ._plots_2d import density_2d
    from ._plots_2d import density_scatter_histogram_2d
    from ._plots_2d import histogram_2d
    from ._plots_2d import scatter
    from ._plots_3d import contour
    from ._plots_3d import heatmap
    from ._plots_3d import scatter_3d
    from ._plots_3d import surface
    from ._plots_nd import band
    from ._plots_nd import box
    from ._plots_nd import density
    from ._plots_nd import histogram
    from ._plots_nd import parallel_coordinates
    from ._plots_nd import scatter_matrix
    from ._plots_nd import violin
    from ._plots_financial import candlestick
    from ._plots_financial import ohlc
    from ._data_structures import Figure
except ImportError as excp:
    __all__ = []
    _logging.report_missing_library('Plotly', excp)

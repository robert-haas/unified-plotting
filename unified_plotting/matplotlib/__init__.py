"""This is the subpackage :py:mod:`unified_plotting.matplotlib`.

It provides static plots based on `Matplotlib <https://matplotlib.org/>`__.
Its main purpose is to enable easier access to the rich plotting
capabilities of this Python library by providing a simple, unified,
high-level API for many plot types.

It contains the following modules and plotting functions.
"""

from .. import _logging


try:
    __all__ = [
        'box',
        'contour',
        'histogram',
        'histogram_2d',
        'hexbin',
        'scatter',
        'scatter_3d',
        'scatter_matrix',
        'violin',
        'Figure',
    ]

    from matplotlib import rcParams as _rcParams
    from matplotlib import pyplot as _plt
    import warnings as _warnings

    # 1) Customizations
    # https://matplotlib.org/tutorials/introductory/customizing.html
    # - Use fonts in SVG instead of paths
    _rcParams['svg.fonttype'] = 'none'

    # - Render minus symbol correctly with cmr10 font: hyphen instead of defect Unicode minus
    _rcParams['axes.unicode_minus'] = False
    _rcParams['axes.axisbelow'] = True

    # - Set global style, basis on which later both package- and user-defined settings are applied
    _plt.style.use('seaborn-white')

    # 2) Suppress undesired warnings
    # - via warning module
    # https://github.com/ipython/ipython/issues/11167
    _warnings.filterwarnings(
        action='ignore',
        category=UserWarning,
        message=('This figure includes Axes that are not compatible with tight_layout, '
                 'so results might be incorrect.')
    )
    # - via logging module
    import logging as _py_logging
    _py_logging.getLogger('matplotlib').setLevel(_py_logging.ERROR)
    # - via package settings in rcParams
    _rcParams['figure.max_open_warning'] = False

    # Plot imports
    from ._plots_2d import hexbin
    from ._plots_2d import histogram_2d
    from ._plots_2d import scatter
    from ._plots_3d import contour
    from ._plots_3d import scatter_3d
    from ._plots_nd import box
    from ._plots_nd import histogram
    from ._plots_nd import scatter_matrix
    from ._plots_nd import violin
    from ._data_structures import Figure
except ImportError as excp:
    _logging.report_missing_library('Matplotlib', excp)
    __all__ = []

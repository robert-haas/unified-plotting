"""This is the subpackage :py:mod:`unified_plotting.javascript`.

It provides interactive plots based on
**web technology (HTML/CSS/JavaScript)** and modern,
highly optimized **web browsers**.
Its main purpose is to enable visualizations that are currently not
available in this form in Python libraries, e.g. interactive and highly
customizable network plots.

Export of a plot is currently only possible as stand-alone HTML file,
but when opened in a web browser like Firefox or Chrome, the UI
provides additional export functions to create static image files in
formats such as SVG, PNG or JPG by utilizing modern browser APIs.
Currently there is no simple and lightweight alternative for direct
static image export from within Python that does not depend on manual
user interaction in a browser.

It contains the following modules and plotting functions.
"""

from .. import _logging


try:
    __all__ = [
        'image_viewer',
        'network_d3',
        'network_vis',
        'network_webgl',
        'parallel_coordinates_table',
        'table',
    ]

    from ._plots_external import image_viewer
    from ._plots_nd import parallel_coordinates_table, table
    from ._plots_network import network_d3, network_vis, network_webgl
except ImportError as excp:
    __all__ = []
    _logging.report_missing_library('JavaScript subpackage', excp)

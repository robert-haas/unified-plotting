"""This is the package :py:mod:`unified_plotting`.

It provides a simple, unified, high-level API to easily
access the capabilities of multiple plotting libraries.
Various plot types can be generated by simple function
calls. They come with a range of optional arguments to
modify the appearance of the resulting visualization,
which comes in form of a unified figure object with methods
for representing, displaying or exporting the plot.
There is also a central config system that allows to
change default argument values globally for all plot types,
thereby enabling the generation of user-defined styles that
can be shared.

It contains the following subpackages.
"""

__all__ = [
    'config',
    'javascript',
    'matplotlib',
    'plotly',
    'ui',
    'utilities',
]

__version__ = '0.5.0rc1'

from . import javascript, matplotlib, plotly, ui, utilities
from ._config import config

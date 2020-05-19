"""Data structures for representing JavaScript plots."""

import random as _random
import string as _string

from ..utilities import operating_system as _operating_system
from . import _template_system


try:
    from IPython.display import display as _display
    from IPython.display import HTML as _HTML
except ImportError:
    pass


class Figure:
    """Data structure for wrapping, displaying and exporting a JavaScript figure."""

    def __init__(self, html_template):
        """Initialize a figure with a partly filled HTML template containing a visualization."""
        self._html_template = html_template

    # IPython integration
    def _repr_html_(self):
        """Provide HTML text for integration with IPython rich display representation.

        References
        ----------
        - https://ipython.readthedocs.io/en/stable/config/integrating.html#rich-display
        - https://ipython.readthedocs.io/en/stable/api/generated/IPython.core.formatters.html#IPython.core.formatters.HTMLFormatter

        """
        return self.html_text_partial

    # Display in browser or notebook
    def display(self, inline=False):
        """Display the plot in a webbrowser or as IPython rich display representation.

        Parameters
        ----------
        in_jupyter : bool
            If True, the plot will be shown inline in a Jupyter notebook.

        """
        if inline:
            _display(_HTML(self.html_text_partial))
        else:
            _operating_system.open_html_text_in_webbrowser(self.html_text_standalone)

    # Representation as text
    @property
    def html_text(self):
        """Create a HTML text representation."""
        return self.html_text_standalone

    @property
    def html_text_standalone(self):
        """Create a standalone HTML text representation that has all javascript code embedded."""
        data = {
            'RANDOM_ID': self._generate_random_id(),
            'PREFIX': """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
</head>
<body style="margin:0;">""",
            'LOAD_REQUIRE': _template_system.load('third_party/require/require.min.js'),
            'SUFFIX': """</body>
</html>""",
        }
        html_text = _template_system.insert(self._html_template, data)
        return html_text

    @property
    def html_text_partial(self):
        """Create a dependent HTML text representation that loads javascript with require.js."""
        # Caution: Needs require.js to know where to find javascript code  - WRONG; change description, all code is included each time I guess
        data = {
            'RANDOM_ID': self._generate_random_id(),
            'PREFIX': '',
            'LOAD_REQUIRE': _template_system.load('third_party/require/require.min.js'),
            'SUFFIX': '',
        }
        html_text = _template_system.insert(self._html_template, data)
        return html_text

    # Export as HTML file (interactive)
    def export_html(self, filepath):
        """Export the plot as HTML file.

        Parameters
        ----------
        filepath : str
            Filepath of the created HTML file.
            If the file exists it will be overwritten without warning.
            If the path does not end with ".html" it will be changed to do so.
            If the parent directory does not exist it will be created.

        Returns
        -------
        filepath : str
            Filepath of the generated HTML file, guaranteed to end with ".html".

        """
        # Precondition
        used_filepath = _operating_system.ensure_file_extension(filepath, 'html')

        # Transformation
        with open(used_filepath, 'w') as file_handle:
            file_handle.write(self.html_text)
        return used_filepath

    @staticmethod
    def _generate_random_id(length=32):
        symbols = _string.ascii_letters + _string.digits
        return 'r' + ''.join(_random.choice(symbols) for _ in range(length))

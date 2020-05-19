"""Data structures for representing Matplotlib plots."""

import io as _io

import matplotlib.pyplot as _plt

from .._unified_arguments import shared_processing as _shared_processing
from ..utilities import base64 as _base64
from ..utilities import operating_system as _operating_system


class Figure:
    """Data structure for wrapping, representing, displaying and exporting a Matplotlib figure.

    References
    ----------
    - https://matplotlib.org/users/index.html
    - https://matplotlib.org/tutorials/introductory/pyplot.html
    - https://matplotlib.org/api/index.html
    - https://matplotlib.org/api/pyplot_summary.html
    - https://matplotlib.org/gallery/index.html
    - https://matplotlib.org/gallery/index.html#api-examples

    """

    def __init__(self, fig,
                 width_mm=None, width_in=None, width_pt=None,
                 height_mm=None, height_in=None, height_pt=None,
                 dpi=None,
                 margin_auto=None, margin_left_mm=None, margin_left_in=None,
                 margin_left_pt=None, margin_left_rel=None,
                 margin_right_mm=None, margin_right_in=None,
                 margin_right_pt=None, margin_right_rel=None,
                 margin_top_mm=None, margin_top_in=None,
                 margin_top_pt=None, margin_top_rel=None,
                 margin_bottom_mm=None, margin_bottom_in=None,
                 margin_bottom_pt=None, margin_bottom_rel=None):
        """Initialize a figure with a Matplotlib figure object."""
        self.fig = fig
        self.set_size(
            width_mm, width_in, width_pt, height_mm, height_in, height_pt, dpi,
            margin_auto, margin_left_mm, margin_left_in, margin_left_pt, margin_left_rel,
            margin_right_mm, margin_right_in, margin_right_pt, margin_right_rel,
            margin_top_mm, margin_top_in, margin_top_pt, margin_top_rel,
            margin_bottom_mm, margin_bottom_in, margin_bottom_pt, margin_bottom_rel)
        self._display_format = 'png'

    def __del__(self):
        """Delete a figure by closing the embedded Matplotlib figure object."""
        try:
            _plt.close(self.fig)
        except Exception:
            pass

    # IPython integration
    def _repr_html_(self):
        """Provide HTML text for integration with IPython rich display representation.

        References
        ----------
        - https://ipython.readthedocs.io/en/stable/config/integrating.html#rich-display
        - https://ipython.readthedocs.io/en/stable/api/generated/IPython.core.formatters.html#IPython.core.formatters.HTMLFormatter

        """
        if self._display_format == 'eps':
            html_text = self.eps_object_element
        elif self._display_format == 'pdf':
            html_text = self.pdf_object_element
        elif self._display_format == 'png':
            html_text = self.png_img_element
        elif self._display_format == 'ps':
            html_text = self.ps_object_element
        elif self._display_format == 'svg':
            html_text = self.svg_img_element
        else:
            message = 'Unknown display format: {}'.format(self._display_format)
            raise ValueError(message)
        return html_text

    # Setters
    def set_size(self, width_mm=None, width_in=None, width_pt=None,
                 height_mm=None, height_in=None, height_pt=None, dpi=None,
                 margin_auto=None,
                 margin_left_mm=None, margin_left_in=None,
                 margin_left_pt=None, margin_left_rel=None,
                 margin_right_mm=None, margin_right_in=None,
                 margin_right_pt=None, margin_right_rel=None,
                 margin_top_mm=None, margin_top_in=None,
                 margin_top_pt=None, margin_top_rel=None,
                 margin_bottom_mm=None, margin_bottom_in=None,
                 margin_bottom_pt=None, margin_bottom_rel=None):
        """Set size, resolution and margins of the plot.

        Parameters
        ----------
        width_mm : float
            Plot width in millimeters.
            Overrules ``width_in`` and ``width_pt``.
        width_in : float
            Plot width in inches.
            Overrules ``width_pt``.
        width_pt : float
            Plot width in points (1 in = 72 pt).

        height_mm : float
            Plot height in millimeters.
            Overrules ``height_in`` and ``height_pt``.
        height_in : float
            Plot height in inches.
            Overrules ``height_pt``.
        height_pt : float
            Plot height in points (1 in = 72 pt).

        dpi : int
            Dots per inch, used synonymously with pixels per inch (ppi).
            Example: Using width_in=2 and dpi=300 results in an image that is 600 pixels wide .
            Note that font size is specified in pt (=1/72 in). Therefore, using width_in=1
            and dpi=600 also results in an image that is 600 pixels wide but texts are twice as large.

        margin_auto : bool
            If True, all margins are set automatically by layout calculations of
            the plotting library.
            Caution: Other margin arguments are ignored in this case!

        margin_left_mm : float
            Left margin in millimeters.
            Overrules ``margin_left_in``, ``margin_left_pt`` and ``margin_left_rel``.
        margin_left_in : float
            Left margin in inches.
            Overrules ``margin_left_pt`` and ``margin_left_rel``.
        margin_left_pt : float
            Left margin in points (1 in = 72 pt).
            Overrules ``margin_left_rel``.
        margin_left_rel : float
            Left margin in percent, i.e. a relative measure.

        margin_right_mm : float
            right margin in millimeters.
            Overrules ``margin_right_in``, ``margin_right_pt`` and ``margin_right_rel``.
        margin_right_in : float
            right margin in inches.
            Overrules ``margin_right_pt`` and ``margin_right_rel``.
        margin_right_pt : float
            right margin in points (1 in = 72 pt).
            Overrules ``margin_right_rel``.
        margin_right_rel : float
            right margin in percent, i.e. a relative measure.

        margin_top_mm : float
            top margin in millimeters.
            Overrules ``margin_top_in``, ``margin_top_pt`` and ``margin_top_rel``.
        margin_top_in : float
            top margin in inches.
            Overrules ``margin_top_pt`` and ``margin_top_rel``.
        margin_top_pt : float
            top margin in points (1 in = 72 pt).
            Overrules ``margin_top_rel``.
        margin_top_rel : float
            top margin in percent, i.e. a relative measure.

        margin_bottom_mm : float
            bottom margin in millimeters.
            Overrules ``margin_bottom_in``, ``margin_bottom_pt`` and ``margin_bottom_rel``.
        margin_bottom_in : float
            bottom margin in inches.
            Overrules ``margin_bottom_pt`` and ``margin_bottom_rel``.
        margin_bottom_pt : float
            bottom margin in points (1 in = 72 pt).
            Overrules ``margin_bottom_rel``.
        margin_bottom_rel : float
            bottom margin in percent, i.e. a relative measure.

        References
        ----------
        - https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure.set_size_inches
        - https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure.subplots_adjust
        - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.tight_layout.html
        - https://matplotlib.org/tutorials/intermediate/tight_layout_guide.html
        - https://matplotlib.org/tutorials/intermediate/constrainedlayout_guide.html

        """
        # Calculate quantities in all units
        current_size = self.size if hasattr(self, 'size') else None
        self.size = _shared_processing.SizeManager(
            width_mm, width_in, width_pt, height_mm, height_in, height_pt, dpi,
            margin_auto, margin_left_mm, margin_left_in, margin_left_pt, margin_left_rel,
            margin_right_mm, margin_right_in, margin_right_pt, margin_right_rel,
            margin_top_mm, margin_top_in, margin_top_pt, margin_top_rel,
            margin_bottom_mm, margin_bottom_in, margin_bottom_pt, margin_bottom_rel,
            current_size)
        # Set plot size
        self.fig.set_size_inches(self.size.width_in, self.size.height_in)
        # Set margins
        if self.size.margin_auto:
            self.fig.tight_layout()
        else:
            self.fig.subplots_adjust(
                left=self.size.margin_left_rel,
                right=1.0-self.size.margin_right_rel,
                top=1.0-self.size.margin_top_rel,
                bottom=self.size.margin_bottom_rel,
            )

    def set_display_format(self, data_format):
        """Set data format of the image shown by display() or automatically in notebooks.

        Parameters
        ----------
        data_format : str
            Possible values: "eps", "pdf", "png", "ps", "svg",
        """
        if isinstance(data_format, str):
            data_format = data_format.lower()
        known_formats = ['eps', 'pdf', 'png', 'ps', 'svg']
        if data_format in known_formats:
            self._display_format = data_format
        else:
            message = 'Unknown data format. Possible values: {}'.format(known_formats)
            raise ValueError(message)

    # Display in browser or notebook
    def display(self, inline=False):
        """Display the plot in a webbrowser or as IPython rich display representation.

        Parameters
        ----------
        inline : bool
            If True, the plot will be shown inline in a Jupyter notebook or QT console.

        Notes
        -----
        Matplotlib usually uses Tkinter to display plots. Here the plot is instead shown in a
        webbrowser, by transforming it into a HTML image element (e.g. png, svg).
        This should be a bit more robust. For example, it can also be called within a
        Jupyter notebook for which the standard method would result in a backend error.

        References
        ----------
        - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.show.html

        """
        if inline:
            from IPython.display import display, HTML
            display(HTML(self._repr_html_()))
        else:
            _operating_system.open_html_text_in_webbrowser(self._repr_html_())

    # Representation as text
    @property
    def html_text(self):
        """Create a standalone HTML text representation of the plot without any dependencies.

        The plot is converted to an SVG image element with a base64 data URL, which is then
        embedded in a HTML context.
        """
        template = (
            '<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body>{}</body></html>')
        html_text = template.format(self.svg_img_element)
        return html_text

    @property
    def svg_text(self):
        """Create an SVG text representation of the plot, usable in HTML context or SVG file."""
        # Write SVG output into memory
        try:
            with _io.StringIO() as file_handle:
                self.fig.savefig(
                    fname=file_handle,
                    dpi=self.size.dpi,
                    facecolor=self.fig.get_facecolor(),
                    edgecolor=self.fig.get_edgecolor(),
                    format='svg',
                )
                svg_text = file_handle.getvalue()
        except Exception:
            message = 'Matplotlib failed to generate an image in "svg" format.'
            raise ValueError(message)
        # Remove '\n' and unnecessary whitespaces
        svg_text = ''.join(line.strip() for line in svg_text.splitlines())
        # Remove <xml> prefix
        start = svg_text.find('<svg')
        svg_text = svg_text[start:]
        return svg_text

    # Representation as data URL
    def _to_binary_data(self, data_format):
        """Create a binary representation of the plot in a chosen image format."""
        try:
            with _io.BytesIO() as file_handle:
                # Note: Passing facecolor is necessary, otherwise it would default to 'w'
                self.fig.savefig(
                    fname=file_handle,
                    dpi=self.size.dpi,
                    facecolor=self.fig.get_facecolor(),
                    edgecolor=self.fig.get_edgecolor(),
                    format=data_format,
                )
                file_handle.seek(0)
                binary_data = file_handle.getvalue()
        except Exception:
            message = 'Matplotlib failed to generate an image in "{}" format.'.format(data_format)
            raise ValueError(message)
        return binary_data

    def _to_data_url(self, data_format):
        """Create a data URL representation with base64 encoded date in a chosen image format."""
        binary_data = self._to_binary_data(data_format)
        base64_text = _base64.binary_data_to_base64_text(binary_data)
        data_url = _base64.base64_text_to_data_url(base64_text, data_format)
        return data_url

    @property
    def eps_data_url(self):
        """Create a data URL representation with EPS image format."""
        return self._to_data_url('eps')

    @property
    def pdf_data_url(self):
        """Create a data URL representation with PDF image format."""
        return self._to_data_url('pdf')

    @property
    def png_data_url(self):
        """Create a data URL representation with PNG image format."""
        return self._to_data_url('png')

    @property
    def ps_data_url(self):
        """Create a data URL representation with PS image format."""
        return self._to_data_url('ps')

    @property
    def svg_data_url(self):
        """Create a data URL representation with SVG image format."""
        return self._to_data_url('svg')

    # Representation as HTML element (with data URL embedded in img or object tag)
    def _to_img_element(self, data_format):
        """Convert the plot to a HTML image element with suitable size (1 in = 96 CSS px)."""
        data_url = self._to_data_url(data_format)
        alternative_text = 'A Matplotlib plot rendered as image in {} format.'.format(data_format)
        img_element = _base64.url_to_img_element(
            data_url, self.size.width_px, self.size.height_px, alternative_text)
        return img_element

    def _to_object_element(self, data_format):
        """Convert the plot to a HTML object element with suitable size (1 in = 96 CSS px)."""
        data_url = self._to_data_url(data_format)
        alternative_text = 'A Matplotlib plot rendered as image in {} format.'.format(data_format)
        object_element = _base64.url_to_object_element(
            data_url, self.size.width_px, self.size.height_px, alternative_text)
        return object_element

    @property
    def eps_object_element(self):
        """Create a HTML object element with EPS image format."""
        return self._to_object_element('eps')

    @property
    def pdf_object_element(self):
        """Create a HTML image element with PDF image format."""
        return self._to_object_element('pdf')

    @property
    def png_img_element(self):
        """Create a HTML image element with PNG image format."""
        return self._to_img_element('png')

    @property
    def ps_object_element(self):
        """Create a HTML object element with PS image format."""
        return self._to_object_element('ps')

    @property
    def svg_img_element(self):
        """Create a HTML image element with SVG image format."""
        return self._to_img_element('svg')

    # Export as HTML file
    def export_html(self, filepath):
        """Export the plot as HTML file that contains a vector graphic in SVG format.

        Parameters
        ----------
        filepath : str
            Filepath of the created HTML file.
            If the file exists it will be overwritten without warning.
            If the path does not end with ".html" it will be changed to do so.
            If the parent directory does not exist it will be created.

        Returns
        -------
        filepath_used : str
            Filepath of the generated HTML file, guaranteed to end with ".html".

        """
        # Precondition
        filepath_used = _operating_system.ensure_file_extension(filepath, 'html')
        _operating_system.ensure_parent_directory(filepath_used)

        # Transformation
        with open(filepath_used, 'w') as file_handle:
            file_handle.write(self.html_text)

        # Postcondition
        _operating_system.is_nonempty_file(
            filepath_used, raise_exception=True, message='Export of plot as HTML file failed.')
        return filepath_used

    # Export as image file: 1) raster graphics
    def _export_img(self, filepath, data_format, quality=None):
        """Export the plot as raster or vector graphic in different formats.

        Currently available according help text returned by
        ``plt.gcf().canvas.get_supported_filetypes_grouped()``:
        - Postscript: 'ps'
        - Encapsulated Postscript: 'eps'
        - Portable Document Format: 'pdf'
        - PGF code for LaTeX: 'pgf'
        - Portable Network Graphics: 'png'
        - Raw RGBA bitmap: 'raw', 'rgba'
        - Scalable Vector Graphics: 'svg', 'svgz'
        - Joint Photographic Experts Group: 'jpeg', 'jpg'
        - Tagged Image File Format: 'tif', 'tiff'

        References
        ----------
        - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.savefig.html

        """
        # Precondition
        filepath_used = _operating_system.ensure_file_extension(filepath, data_format)
        _operating_system.ensure_parent_directory(filepath_used)

        # Transformation
        try:
            self.fig.savefig(
                fname=filepath_used,
                dpi=self.size.dpi,
                quality=quality,
                facecolor=self.fig.get_facecolor(),
                edgecolor=self.fig.get_edgecolor(),
                format=data_format,
            )
        except Exception:
            message = 'Matplotlib failed to generate an image in "{}" format.'.format(data_format)
            raise ValueError(message)

        # Postcondition
        _operating_system.is_nonempty_file(
            filepath_used, raise_exception=True,
            message='Export of plot as image file in {} format failed.'.format(
                data_format.upper()))
        return filepath_used

    def export_png(self, filepath):
        """Export the plot as raster graphic in PNG format.

        Parameters
        ----------
        filepath : str
            Filepath of the created PNG file.
            If the file exists it will be overwritten without warning.
            If the path does not end with ".png" it will be changed to do so.
            If the parent directory does not exist it will be created.

        Returns
        -------
        filepath_used : str
            Filepath of the generated PNG file, guaranteed to end with ".png".

        """
        return self._export_img(filepath, data_format='png')

    # Export as image file: 2) vector graphics
    def export_eps(self, filepath):
        """Export the plot as vector graphic in EPS format.

        .. note::
           Matplotlib does not support transparency for vector graphics in EPS format.

        Parameters
        ----------
        filepath : str
            Filepath of the created EPS file.
            If the file exists it will be overwritten without warning.
            If the path does not end with ".eps" it will be changed to do so.
            If the parent directory does not exist it will be created.

        Returns
        -------
        filepath_used : str
            Filepath of the generated EPS file, guaranteed to end with ".eps".

        """
        return self._export_img(filepath, data_format='eps')

    def export_pdf(self, filepath):
        """Export the plot as vector graphic in PDF format.

        Parameters
        ----------
        filepath : str
            Filepath of the created PDF file.
            If the file exists it will be overwritten without warning.
            If the path does not end with ".pdf" it will be changed to do so.
            If the parent directory does not exist it will be created.

        Returns
        -------
        filepath_used : str
            Filepath of the generated PDF file, guaranteed to end with ".pdf".

        """
        return self._export_img(filepath, data_format='pdf')

    def export_pgf(self, filepath):
        """Export the plot as vector graphic in PGF format for LaTeX.

        Parameters
        ----------
        filepath : str
            Filepath of the created PGF file.
            If the file exists it will be overwritten without warning.
            If the path does not end with ".pgf" it will be changed to do so.
            If the parent directory does not exist it will be created.

        Returns
        -------
        filepath_used : str
            Filepath of the generated PGF file, guaranteed to end with ".pgf".

        """
        return self._export_img(filepath, data_format='pgf')

    def export_ps(self, filepath):
        """Export the plot as vector graphic in PS format.

        .. note::
           Matplotlib does not support transparency for vector graphics in PS format.

        Parameters
        ----------
        filepath : str
            Filepath of the created PS file.
            If the file exists it will be overwritten without warning.
            If the path does not end with ".ps" it will be changed to do so.
            If the parent directory does not exist it will be created.

        Returns
        -------
        filepath_used : str
            Filepath of the generated PS file, guaranteed to end with ".ps".

        """
        return self._export_img(filepath, data_format='ps')

    def export_svg(self, filepath):
        """Export the plot as vector graphic in SVG format.

        Parameters
        ----------
        filepath : str
            Filepath of the created SVG file.
            If the file exists it will be overwritten without warning.
            If the path does not end with ".svg" it will be changed to do so.
            If the parent directory does not exist it will be created.

        Returns
        -------
        filepath_used : str
            Filepath of the generated SVG file, guaranteed to end with ".svg".

        """
        return self._export_img(filepath, data_format='svg')

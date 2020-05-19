"""Data structures for representing Plotly plots."""

from plotly import io as _pio
from plotly.offline import init_notebook_mode as _init_notebook_mode

from .._unified_arguments import shared_processing as _shared_processing
from ..utilities import base64 as _base64
from ..utilities import operating_system as _operating_system


class Figure:
    """Data structure for wrapping, representing, displaying and exporting a Plotly figure.

    References
    ----------
    - https://plot.ly/python/creating-and-updating-figures
    - https://plot.ly/python/renderers
    - https://plot.ly/python-api-reference

    """

    # class variable to load plotly.js code into Jupyter notebook exactly once, not for each plot
    _notebook_initialized = False

    def __init__(self, fig,
                 width_mm=None, width_in=None, width_pt=None,
                 height_mm=None, height_in=None, height_pt=None,
                 dpi=None,
                 margin_auto=None,
                 margin_left_mm=None, margin_left_in=None,
                 margin_left_pt=None, margin_left_rel=None,
                 margin_right_mm=None, margin_right_in=None,
                 margin_right_pt=None, margin_right_rel=None,
                 margin_top_mm=None, margin_top_in=None,
                 margin_top_pt=None, margin_top_rel=None,
                 margin_bottom_mm=None, margin_bottom_in=None,
                 margin_bottom_pt=None, margin_bottom_rel=None):
        """Initialize a figure with a Plotly figure object."""
        self.fig = fig
        self.set_size(
            width_mm, width_in, width_pt, height_mm, height_in, height_pt, dpi,
            margin_auto,
            margin_left_mm, margin_left_in, margin_left_pt, margin_left_rel,
            margin_right_mm, margin_right_in, margin_right_pt, margin_right_rel,
            margin_top_mm, margin_top_in, margin_top_pt, margin_top_rel,
            margin_bottom_mm, margin_bottom_in, margin_bottom_pt, margin_bottom_rel)
        self._set_config()
        self.set_display_format('html')

    def __add__(self, other):
        """Add a figure to this one in a simplistic way by adding the trace but not its layout."""
        self.fig.add_traces(other.fig['data'])
        return self

    # IPython integration
    def _repr_html_(self):
        """Provide HTML text for integration with IPython rich display representation.

        References
        ----------
        - https://ipython.readthedocs.io/en/stable/config/integrating.html#rich-display
        - https://ipython.readthedocs.io/en/stable/api/generated/IPython.core.formatters.html#IPython.core.formatters.HTMLFormatter

        """
        if self._display_format == 'html':
            # Load plotly.js into notebook once, so that require.js can find it (also offline)
            if not self.__class__._notebook_initialized:
                try:
                    _init_notebook_mode()
                    self.__class__._notebook_initialized = True
                except Exception:
                    pass
            html_text = self.html_text_partial
        elif self._display_format == 'eps':
            html_text = self.eps_object_element
        elif self._display_format == 'jpg':
            html_text = self.jpg_img_element
        elif self._display_format == 'pdf':
            html_text = self.pdf_object_element
        elif self._display_format == 'png':
            html_text = self.png_img_element
        elif self._display_format == 'svg':
            html_text = self.svg_img_element
        elif self._display_format == 'webp':
            html_text = self.webp_img_element
        else:
            message = 'Unknown display format: {}'.format(self._display_format)
            raise ValueError(message)
        return html_text

    # Setters
    def _set_config(self):
        """Set plotly.js config for interactive plots that provide an export button for user."""
        self._config = {
            'displaylogo': False,
            'scrollZoom': True,
            'staticPlot': False,  # not provided as option, because True fails in simple examples
            'toImageButtonOptions': {
                'format': 'svg',  # alternatives: png, svg, jpeg, webp
                'filename': 'plotly_image',
            },
            'modeBarButtonsToRemove': [
                'sendDataToCloud', 'lasso2d', 'select2d', 'autoScale2d', 'zoomIn2d', 'zoomOut2d',
                'hoverClosestCartesian', 'hoverCompareCartesian', 'hoverClosest3d', ],
        }

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
        - https://plot.ly/python/setting-graph-size
        - https://plot.ly/python/reference/#layout-width
        - https://plot.ly/python/reference/#layout-height
        - https://plot.ly/python/reference/#layout-margin
        - https://github.com/plotly/orca/issues/205#issuecomment-485387841

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
        if 'layout' not in self.fig:
            self.fig['layout'] = dict()
        self.fig['layout']['width'] = self.size.width_px
        self.fig['layout']['height'] = self.size.height_px
        # Set margins
        if self.size.margin_auto:
            self.fig['layout']['margin'] = dict()
        else:
            self.fig['layout']['margin'] = dict(
                l=self.size.margin_left_px,
                r=self.size.margin_right_px,
                t=self.size.margin_top_px,
                b=self.size.margin_bottom_px,
            )

    def set_display_format(self, data_format):
        """Set data format of the image shown by display() or automatically in notebooks.

        Parameters
        ----------
        data_format : str
            Possible values: "html", "eps", "jpg", "pdf", "png", "svg",  "webp"

        """
        if isinstance(data_format, str):
            data_format = data_format.lower()
        known_formats = ['html', 'eps', 'jpg', 'pdf', 'png', 'svg', 'webp']
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

        References
        ----------
        - https://plot.ly/python/renderers

        """
        if inline:
            from IPython.display import display, HTML
            display(HTML(self._repr_html_()))
        else:
            _operating_system.open_html_text_in_webbrowser(self.html_text)

    # Representation as text
    @property
    def html_text(self):
        """Create a HTML text representation."""
        return self.html_text_standalone

    @property
    def html_text_standalone(self):
        """Create a standalone HTML text representation that has all plotly.js code embedded.

        References
        ----------
        - https://plot.ly/python-api-reference/generated/plotly.io.to_html.html

        """
        html_text = _pio.to_html(
            fig=self.fig,
            config=self._config,
            full_html=True,         # starting with an <html> tag
            include_plotlyjs=True,  # script tag containing plotly.js source code (~3MB)
        )
        return html_text

    @property
    def html_text_cdn(self):
        """Create a dependent HTML text representation that loads plotly.js from a CDN on the web.

        References
        ----------
        - https://plot.ly/python-api-reference/generated/plotly.io.to_html.html

        """
        html_text = _pio.to_html(
            fig=self.fig,
            config=self._config,
            full_html=True,
            include_plotlyjs='cdn',  # plotly.js is loaded using a CDN (requires web connection!)
        )
        return html_text

    @property
    def html_text_partial(self):
        """Create a dependent HTML text representation that loads plotly.js with require.js.

        References
        ----------
        - https://plot.ly/python-api-reference/generated/plotly.io.to_html.html

        """
        # Caution: Needs require.js to know where to find plotly.js
        #          For Jupyter notebooks it is ensured with_init_notebook_mode() in _repr_html_()
        #          For use in a webserver, it has to be ensured by surrounding JS code.
        html_text = _pio.to_html(
            fig=self.fig,
            config=self._config,
            full_html=False,             # starting with an <div> tag
            include_plotlyjs='require',  # plotly.js is loaded using require.js.
        )
        return html_text

    @property
    def json_text(self):
        """JSON representation of the Plotly figure.

        It can also be used by Plotly's JavaScript graphing library
        `plotly.js <https://plot.ly/javascript>`_.

        References
        ----------
        - https://plot.ly/python-api-reference/generated/plotly.io.to_json.html
        - https://plot.ly/python-api-reference/generated/plotly.io.write_json.html
        - https://plot.ly/python-api-reference/generated/plotly.io.from_json.html
        - https://plot.ly/python-api-reference/generated/plotly.io.read_json.html
        - https://help.plot.ly/json-chart-schema

        """
        return _pio.to_json(fig=self.fig)

    @property
    def svg_text(self):
        """Create an SVG text representation of the plot, usable in HTML context or SVG file."""
        svg_text = self._to_binary_data('svg').decode('utf-8')
        return svg_text

    # Representation as data URL
    def _to_binary_data(self, data_format):
        """Create an image of the plot encoded in binary data.

        References
        ----------
        - https://plot.ly/python-api-reference/generated/plotly.io.to_image.html

        """
        binary_data = _pio.to_image(
            fig=self.fig,
            format=data_format,
            width=self.size.width_px,    # width of the exported image in layout pixels
            height=self.size.height_px,  # height of the exported image in layout pixels
            scale=self.size.dpi / 96.0,  # larger than 1.0 will increase the image resolution
        )
        return binary_data

    def _to_data_url(self, data_format):
        binary_data = self._to_binary_data(data_format)
        base64_text = _base64.binary_data_to_base64_text(binary_data)
        data_url = _base64.base64_text_to_data_url(base64_text, data_format)
        return data_url

    @property
    def eps_data_url(self):
        """Create a data URL representation with EPS image format."""
        return self._to_data_url('eps')

    @property
    def jpg_data_url(self):
        """Create a data URL representation with JPG image format."""
        return self._to_data_url('jpeg')

    @property
    def pdf_data_url(self):
        """Create a data URL representation with PDF image format."""
        return self._to_data_url('pdf')

    @property
    def png_data_url(self):
        """Create a data URL representation with PNG image format."""
        return self._to_data_url('png')

    @property
    def svg_data_url(self):
        """Create a data URL representation with SVG image format."""
        return self._to_data_url('svg')

    @property
    def webp_data_url(self):
        """Create a data URL representation with WebP image format."""
        return self._to_data_url('webp')

    # Representation as HTML element (with data URL embedded in img or object tag)
    def _to_img_element(self, data_format):
        """Convert the plot to a HTML image element with suitable size (1 in = 96 CSS px)."""
        data_url = self._to_data_url(data_format)
        alternative_text = 'A Plotly plot rendered as image in {} format.'.format(data_format)
        img_element = _base64.url_to_img_element(
            data_url, self.size.width_px, self.size.height_px, alternative_text)
        return img_element

    def _to_object_element(self, data_format):
        """Convert the plot to a HTML object element with suitable size (1 in = 96 CSS px)."""
        data_url = self._to_data_url(data_format)
        alternative_text = 'A Plotly plot rendered as image in {} format.'.format(data_format)
        object_element = _base64.url_to_object_element(
            data_url, self.size.width_px, self.size.height_px, alternative_text)
        return object_element

    @property
    def eps_object_element(self):
        """Create a HTML object element with EPS image format."""
        return self._to_object_element('eps')

    @property
    def jpg_img_element(self):
        """Create a HTML image element with JPG image format."""
        return self._to_img_element('jpg')

    @property
    def pdf_object_element(self):
        """Create a HTML image element with PDF image format."""
        return self._to_object_element('pdf')

    @property
    def png_img_element(self):
        """Create a HTML image element with PNG image format."""
        return self._to_img_element('png')

    @property
    def svg_img_element(self):
        """Create a HTML image element with SVG image format."""
        return self._to_img_element('svg')

    @property
    def webp_img_element(self):
        """Create a HTML image element with WebP image format."""
        return self._to_img_element('webp')

    # Export as HTML file (interactive)
    def export_html(self, filepath):
        """Export the plot as HTML file that contains an interactive vector graphic.

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

        References
        ----------
        - https://plot.ly/python-api-reference/generated/plotly.io.write_html.html
        - https://plot.ly/python/getting-started
        - https://plot.ly/python/v4-migration
        - https://plot.ly/javascript/configuration-options

        """
        # Precondition
        filepath_used = _operating_system.ensure_file_extension(filepath, 'html')
        _operating_system.ensure_parent_directory(filepath_used)

        # Transformation
        _pio.write_html(
            fig=self.fig,
            file=filepath_used,
            config=self._config,
            auto_open=False,
            full_html=True,         # starting with an <html> tag
            include_plotlyjs=True,  # script tag containing plotly.js source code (~3MB)
        )

        # Postcondition
        _operating_system.is_nonempty_file(
            filepath_used, raise_exception=True, message='Export of plot as HTML file failed.')
        return filepath_used

    # Export as image file (static): 1) raster graphics
    def _export_img(self, filepath, data_format):
        """Export the plot as raster or vector graphics in different formats.

        Currently available according to help text returned by ``help(plotly.io.write_image)``:
        - 'png'
        - 'jpg' or 'jpeg'
        - 'webp'
        - 'svg'
        - 'pdf'
        - 'eps' (Requires the poppler library to be installed)

        References
        ----------
        - https://plot.ly/python-api-reference/generated/plotly.io.write_image.html
        - https://plot.ly/python/static-image-export
        - https://plot.ly/python/orca-management
        - https://plot.ly/javascript/static-image-export

        """
        # Precondition
        filepath_used = _operating_system.ensure_file_extension(filepath, data_format)
        _operating_system.ensure_parent_directory(filepath_used)

        # Transformation
        try:
            _pio.write_image(
                fig=self.fig,
                file=filepath_used,
                format=data_format,
                width=self.size.width_px,
                height=self.size.height_px,
                scale=self.size.dpi / 96.0,
            )
        except ValueError as excp:
            if 'orca' in str(excp):
                message = (
                    'Plotly requires Orca to be installed in order to export image files. '
                    'The online documentation of "unified plotting" contains an installation '
                    'guide including a section on how to install Orca.')
                raise ValueError(message)
            raise excp

        # Postcondition
        _operating_system.is_nonempty_file(
            filepath_used, raise_exception=True,
            message='Export of plot as image file in {} format failed.'.format(
                data_format.upper()))
        return filepath_used

    def export_eps(self, filepath):
        """Export the plot as vector graphic in EPS format.

        .. note::
           Requires the poppler library to be installed

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

        References
        ----------
        - https://plot.ly/python/static-image-export

        """
        return self._export_img(filepath, data_format='eps')

    def export_jpg(self, filepath):
        """Export the plot as raster graphic in JPG format.

        Parameters
        ----------
        filepath : str
            Filepath of the created JPG file.
            If the file exists it will be overwritten without warning.
            If the path does not end with ".jpg" it will be changed to do so.
            If the parent directory does not exist it will be created.

        Returns
        -------
        filepath_used : str
            Filepath of the generated JPG file, guaranteed to end with ".jpg".

        References
        ----------
        - https://plot.ly/python/static-image-export

        """
        return self._export_img(filepath, data_format='jpg')

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

        References
        ----------
        - https://plot.ly/python/static-image-export

        """
        return self._export_img(filepath, data_format='png')

    def export_webp(self, filepath):
        """Export the plot as raster graphic in WebP format.

        Parameters
        ----------
        filepath : str
            Filepath of the created WebP file.
            If the file exists it will be overwritten without warning.
            If the path does not end with ".webp" it will be changed to do so.
            If the parent directory does not exist it will be created.

        Returns
        -------
        filepath_used : str
            Filepath of the generated WebP file, guaranteed to end with ".webp".

        References
        ----------
        - https://plot.ly/python/static-image-export

        """
        return self._export_img(filepath, data_format='webp')

    # Export as image file (static): 2) vector graphics
    def export_pdf(self, filepath):
        """Export the plot as vector graphic in PDF format.

        .. note::
           Figures which contain WebGL traces (e.g. 3D surface or scatter plots) will
           include encapsulated rasters instead of vectors for parts of the image.

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

        References
        ----------
        - https://plot.ly/python/static-image-export

        """
        return self._export_img(filepath, data_format='pdf')

    def export_svg(self, filepath):
        """Export the plot as vector graphic in SVG format.

        .. note::
           Figures which contain WebGL traces (e.g. 3D surface or scatter plots) will
           include encapsulated rasters instead of vectors for parts of the image.

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

        References
        ----------
        - https://plot.ly/python/static-image-export

        """
        return self._export_img(filepath, data_format='svg')

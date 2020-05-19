"""Processing used by various subpackages."""

from collections.abc import Iterable as _Iterable
from numbers import Number as _Number

from .._config import config as _config
from . import shared_preprocessing as _shared_preprocessing
from .colors import conversion as _conversion


# I) Plot size

def select_plot_size_kwargs(pre_kwargs, post_kwargs):
    """Collect kwargs that specify plot and margin size."""
    def decide_what_is_used(pre_kwargs, post_kwargs, names):
        used = {key: pre_kwargs[key] for key in names}
        if all(val is None for val in used.values()):
            used = {key: post_kwargs[key] for key in names}
        return used

    # Width
    width_names = ['width_mm', 'width_in', 'width_pt']
    width_kwargs = decide_what_is_used(pre_kwargs, post_kwargs, width_names)
    width_mm, width_in, width_pt = [width_kwargs[key] for key in width_names]

    # Height
    height_names = ['height_mm', 'height_in', 'height_pt']
    height_kwargs = decide_what_is_used(pre_kwargs, post_kwargs, height_names)
    height_mm, height_in, height_pt = [height_kwargs[key] for key in height_names]

    # DPI
    dpi = pre_kwargs['dpi']
    if dpi is None:
        dpi = post_kwargs['dpi']

    # Margin automatic
    margin_auto = pre_kwargs['margin_auto']
    if margin_auto is None:
        margin_auto = post_kwargs['margin_auto']

    # Margin left
    margin_left_names = [
        'margin_left_mm', 'margin_left_in', 'margin_left_pt', 'margin_left_rel']
    margin_left_kwargs = decide_what_is_used(pre_kwargs, post_kwargs, margin_left_names)
    margin_left_mm, margin_left_in, margin_left_pt, margin_left_rel = \
        [margin_left_kwargs[key] for key in margin_left_names]

    # Margin right
    margin_right_names = [
        'margin_right_mm', 'margin_right_in', 'margin_right_pt', 'margin_right_rel']
    margin_right_kwargs = decide_what_is_used(pre_kwargs, post_kwargs, margin_right_names)
    margin_right_mm, margin_right_in, margin_right_pt, margin_right_rel = \
        [margin_right_kwargs[key] for key in margin_right_names]

    # Margin top
    margin_top_names = [
        'margin_top_mm', 'margin_top_in', 'margin_top_pt', 'margin_top_rel']
    margin_top_kwargs = decide_what_is_used(pre_kwargs, post_kwargs, margin_top_names)
    margin_top_mm, margin_top_in, margin_top_pt, margin_top_rel = \
        [margin_top_kwargs[key] for key in margin_top_names]

    # Margin bottom
    margin_bottom_names = [
        'margin_bottom_mm', 'margin_bottom_in', 'margin_bottom_pt', 'margin_bottom_rel']
    margin_bottom_kwargs = decide_what_is_used(pre_kwargs, post_kwargs, margin_bottom_names)
    margin_bottom_mm, margin_bottom_in, margin_bottom_pt, margin_bottom_rel = \
        [margin_bottom_kwargs[key] for key in margin_bottom_names]

    # Combine all kwargs again
    selected_kwargs = dict(
        width_mm=width_mm, width_in=width_in, width_pt=width_pt,
        height_mm=height_mm, height_in=height_in, height_pt=height_pt,
        dpi=dpi,
        margin_auto=margin_auto,
        margin_left_mm=margin_left_mm, margin_left_in=margin_left_in,
        margin_left_pt=margin_left_pt, margin_left_rel=margin_left_rel,
        margin_right_mm=margin_right_mm, margin_right_in=margin_right_in,
        margin_right_pt=margin_right_pt, margin_right_rel=margin_right_rel,
        margin_top_mm=margin_top_mm, margin_top_in=margin_top_in,
        margin_top_pt=margin_top_pt, margin_top_rel=margin_top_rel,
        margin_bottom_mm=margin_bottom_mm, margin_bottom_in=margin_bottom_in,
        margin_bottom_pt=margin_bottom_pt, margin_bottom_rel=margin_bottom_rel,
    )
    return selected_kwargs


class SizeManager:
    """Container for all plot size parameters."""

    def __init__(self, width_mm=None, width_in=None, width_pt=None,
                 height_mm=None, height_in=None, height_pt=None,
                 dpi=None,
                 margin_auto=None, margin_left_mm=None, margin_left_in=None,
                 margin_left_pt=None, margin_left_rel=None,
                 margin_right_mm=None, margin_right_in=None,
                 margin_right_pt=None, margin_right_rel=None,
                 margin_top_mm=None, margin_top_in=None,
                 margin_top_pt=None, margin_top_rel=None,
                 margin_bottom_mm=None, margin_bottom_in=None,
                 margin_bottom_pt=None, margin_bottom_rel=None,
                 previous_size=None):
        """Create an instance of a size manager with or without given values."""
        # Argument processing
        used_defaults = _config.settings if previous_size is None else previous_size
        if width_mm is None and width_in is None and width_pt is None:
            width_mm = used_defaults.width_mm
            width_in = used_defaults.width_in
            width_pt = used_defaults.width_pt
        if height_mm is None and height_in is None and height_pt is None:
            height_mm = used_defaults.height_mm
            height_in = used_defaults.height_in
            height_pt = used_defaults.height_pt
        if dpi is None:
            dpi = used_defaults.dpi
        if margin_auto is None:
            margin_auto = used_defaults.margin_auto
        if margin_left_mm is None and margin_left_in is None and margin_left_pt is None \
                and margin_left_rel is None:
            margin_left_mm = used_defaults.margin_left_mm
            margin_left_in = used_defaults.margin_left_in
            margin_left_pt = used_defaults.margin_left_pt
            margin_left_rel = used_defaults.margin_left_rel
        if margin_right_mm is None and margin_right_in is None and margin_right_pt is None \
                and margin_right_rel is None:
            margin_right_mm = used_defaults.margin_right_mm
            margin_right_in = used_defaults.margin_right_in
            margin_right_pt = used_defaults.margin_right_pt
            margin_right_rel = used_defaults.margin_right_rel
        if margin_top_mm is None and margin_top_in is None and margin_top_pt is None \
                and margin_top_rel is None:
            margin_top_mm = used_defaults.margin_top_mm
            margin_top_in = used_defaults.margin_top_in
            margin_top_pt = used_defaults.margin_top_pt
            margin_top_rel = used_defaults.margin_top_rel
        if margin_bottom_mm is None and margin_bottom_in is None and margin_bottom_pt is None \
                and margin_bottom_rel is None:
            margin_bottom_mm = used_defaults.margin_bottom_mm
            margin_bottom_in = used_defaults.margin_bottom_in
            margin_bottom_pt = used_defaults.margin_bottom_pt
            margin_bottom_rel = used_defaults.margin_bottom_rel

        # Width
        if width_mm is not None:
            self.width_mm = width_mm
            self.width_in = self._mm_to_in(width_mm)
            self.width_pt = self._mm_to_pt(width_mm)
        elif width_in is not None:
            self.width_mm = self._in_to_mm(width_in)
            self.width_in = width_in
            self.width_pt = self._in_to_pt(width_in)
        elif width_pt is not None:
            self.width_mm = self._pt_to_mm(width_pt)
            self.width_in = self._pt_to_in(width_pt)
            self.width_pt = width_pt
        else:
            message = 'No width given. Please provide width_mm, width_in or width_pt.'
            raise ValueError(message)
        # Height
        if height_mm is not None:
            self.height_mm = height_mm
            self.height_in = self._mm_to_in(height_mm)
            self.height_pt = self._mm_to_pt(height_mm)
        elif height_in is not None:
            self.height_mm = self._in_to_mm(height_in)
            self.height_in = height_in
            self.height_pt = self._in_to_pt(height_in)
        elif height_pt is not None:
            self.height_mm = self._pt_to_mm(height_pt)
            self.height_in = self._pt_to_in(height_pt)
            self.height_pt = height_pt
        else:
            message = 'No height given. Please provide height_mm, height_in or height_pt.'
            raise ValueError(message)
        # DPI
        self.dpi = dpi
        # Margin left
        if margin_left_mm is not None:
            self.margin_left_mm = margin_left_mm
            self.margin_left_in = self._mm_to_in(margin_left_mm)
            self.margin_left_pt = self._mm_to_pt(margin_left_mm)
            self.margin_left_rel = self._abs_to_rel(self.width_mm, margin_left_mm)
        elif margin_left_in is not None:
            self.margin_left_mm = self._in_to_mm(margin_left_in)
            self.margin_left_in = margin_left_in
            self.margin_left_pt = self._in_to_pt(margin_left_in)
            self.margin_left_rel = self._abs_to_rel(self.width_in, margin_left_in)
        elif margin_left_pt is not None:
            self.margin_left_mm = self._pt_to_mm(margin_left_pt)
            self.margin_left_in = self._pt_to_in(margin_left_pt)
            self.margin_left_pt = margin_left_pt
            self.margin_left_rel = self._abs_to_rel(self.width_pt, margin_left_pt)
        elif margin_left_rel is not None:
            self.margin_left_mm = self._rel_to_abs(self.width_mm, margin_left_rel)
            self.margin_left_in = self._rel_to_abs(self.width_in, margin_left_rel)
            self.margin_left_pt = self._rel_to_abs(self.width_pt, margin_left_rel)
            self.margin_left_rel = margin_left_rel
        else:
            message = (
                'No margin_left given. Please provide margin_left_mm, margin_left_in, '
                'margin_left_pt or margin_left_rel.')
            raise ValueError(message)
        # Margin auto
        self.margin_auto = margin_auto
        # Margin right
        if margin_right_mm is not None:
            self.margin_right_mm = margin_right_mm
            self.margin_right_in = self._mm_to_in(margin_right_mm)
            self.margin_right_pt = self._mm_to_pt(margin_right_mm)
            self.margin_right_rel = self._abs_to_rel(self.width_mm, margin_right_mm)
        elif margin_right_in is not None:
            self.margin_right_mm = self._in_to_mm(margin_right_in)
            self.margin_right_in = margin_right_in
            self.margin_right_pt = self._in_to_pt(margin_right_in)
            self.margin_right_rel = self._abs_to_rel(self.width_in, margin_right_in)
        elif margin_right_pt is not None:
            self.margin_right_mm = self._pt_to_mm(margin_right_pt)
            self.margin_right_in = self._pt_to_in(margin_right_pt)
            self.margin_right_pt = margin_right_pt
            self.margin_right_rel = self._abs_to_rel(self.width_pt, margin_right_pt)
        elif margin_right_rel is not None:
            self.margin_right_mm = self._rel_to_abs(self.width_mm, margin_right_rel)
            self.margin_right_in = self._rel_to_abs(self.width_in, margin_right_rel)
            self.margin_right_pt = self._rel_to_abs(self.width_pt, margin_right_rel)
            self.margin_right_rel = margin_right_rel
        else:
            message = (
                'No margin_right given. Please provide margin_right_mm, margin_right_in, '
                'margin_right_pt or margin_right_rel.')
            raise ValueError(message)
        # Margin top
        if margin_top_mm is not None:
            self.margin_top_mm = margin_top_mm
            self.margin_top_in = self._mm_to_in(margin_top_mm)
            self.margin_top_pt = self._mm_to_pt(margin_top_mm)
            self.margin_top_rel = self._abs_to_rel(self.height_mm, margin_top_mm)
        elif margin_top_in is not None:
            self.margin_top_mm = self._in_to_mm(margin_top_in)
            self.margin_top_in = margin_top_in
            self.margin_top_pt = self._in_to_pt(margin_top_in)
            self.margin_top_rel = self._abs_to_rel(self.height_in, margin_top_in)
        elif margin_top_pt is not None:
            self.margin_top_mm = self._pt_to_mm(margin_top_pt)
            self.margin_top_in = self._pt_to_in(margin_top_pt)
            self.margin_top_pt = margin_top_pt
            self.margin_top_rel = self._abs_to_rel(self.height_pt, margin_top_pt)
        elif margin_top_rel is not None:
            self.margin_top_mm = self._rel_to_abs(self.height_mm, margin_top_rel)
            self.margin_top_in = self._rel_to_abs(self.height_in, margin_top_rel)
            self.margin_top_pt = self._rel_to_abs(self.height_pt, margin_top_rel)
            self.margin_top_rel = margin_top_rel
        else:
            message = (
                'No margin_top given. Please provide margin_top_mm, margin_top_in, '
                'margin_top_pt or margin_top_rel.')
            raise ValueError(message)
        # Margin bottom
        if margin_bottom_mm is not None:
            self.margin_bottom_mm = margin_bottom_mm
            self.margin_bottom_in = self._mm_to_in(margin_bottom_mm)
            self.margin_bottom_pt = self._mm_to_pt(margin_bottom_mm)
            self.margin_bottom_rel = self._abs_to_rel(self.height_mm, margin_bottom_mm)
        elif margin_bottom_in is not None:
            self.margin_bottom_mm = self._in_to_mm(margin_bottom_in)
            self.margin_bottom_in = margin_bottom_in
            self.margin_bottom_pt = self._in_to_pt(margin_bottom_in)
            self.margin_bottom_rel = self._abs_to_rel(self.height_in, margin_bottom_in)
        elif margin_bottom_pt is not None:
            self.margin_bottom_mm = self._pt_to_mm(margin_bottom_pt)
            self.margin_bottom_in = self._pt_to_in(margin_bottom_pt)
            self.margin_bottom_pt = margin_bottom_pt
            self.margin_bottom_rel = self._abs_to_rel(self.height_pt, margin_bottom_pt)
        elif margin_bottom_rel is not None:
            self.margin_bottom_mm = self._rel_to_abs(self.height_mm, margin_bottom_rel)
            self.margin_bottom_in = self._rel_to_abs(self.height_in, margin_bottom_rel)
            self.margin_bottom_pt = self._rel_to_abs(self.height_pt, margin_bottom_rel)
            self.margin_bottom_rel = margin_bottom_rel
        else:
            message = (
                'No margin_bottom given. Please provide margin_bottom_mm, margin_bottom_in, '
                'margin_bottom_pt or margin_bottom_rel.')
            raise ValueError(message)

    def __str__(self):
        """Represent the size manager as detailed string."""
        template = (
            'width = {:.2f} mm = {:.2f} in = {:.2f} pt, '
            'height = {:.2f} mm = {:.2f} in = {:.2f} pt, '
            'dpi = {}, '
            'margin_left = {} mm = {} in = {} pt = {} rel, '
            'margin_right = {} mm = {} in = {} pt = {} rel, '
            'margin_top = {} mm = {} in = {} pt = {} rel, '
            'margin_bottom = {} mm = {} in = {} pt = {} rel'
        )
        text = template.format(
            self.width_mm, self.width_in, self.width_pt,
            self.height_mm, self.height_in, self.height_pt, self.dpi,
            self.margin_left_mm, self.margin_left_in,
            self.margin_left_pt, self.margin_left_rel,
            self.margin_right_mm, self.margin_right_in,
            self.margin_right_pt, self.margin_right_rel,
            self.margin_top_mm, self.margin_top_in,
            self.margin_top_pt, self.margin_top_rel,
            self.margin_bottom_mm, self.margin_bottom_in,
            self.margin_bottom_pt, self.margin_bottom_rel,
        )
        return text

    def __repr__(self):
        """Represent the size manager as concise string."""
        return '<{}>'.format(self)

    @property
    def width_px(self):
        """Calculate width for usage with HTML elements (1 in = 96 CSS px)."""
        return self._in_to_px(self.width_in)

    @property
    def height_px(self):
        """Calculate height for usage with HTML elements (1 in = 96 CSS px)."""
        return self._in_to_px(self.height_in)

    @property
    def margin_left_px(self):
        """Calculate left margin size in pixel (px)."""
        return self._in_to_px(self.margin_left_in)

    @property
    def margin_right_px(self):
        """Calculate right margin size in pixel (px)."""
        return self._in_to_px(self.margin_right_in)

    @property
    def margin_top_px(self):
        """Calculate top margin size in pixel (px)."""
        return self._in_to_px(self.margin_top_in)

    @property
    def margin_bottom_px(self):
        """Calculate bottom margin size in pixel (px)."""
        return self._in_to_px(self.margin_bottom_in)

    @staticmethod
    def _in_to_px(given):
        """Pseudo-convert inch (physical unit) to CSS pixel (digital unit).

        References
        ----------
        - https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Values_and_units
        - https://oreillymedia.github.io/Using_SVG/guide/units.html
        - https://stackoverflow.com/questions/40480617/is-a-css-pixel-really-an-absolute-unit-that-is-is-1-inch-96px-true

        """
        return given * 96.0

    # Conversion between phycial units
    @staticmethod
    def _mm_to_in(given):
        return given / 25.4

    @staticmethod
    def _mm_to_pt(given):
        return given / 25.4 * 72.0

    @staticmethod
    def _in_to_mm(given):
        return given * 25.4

    @staticmethod
    def _in_to_pt(given):
        return given * 72.0

    @staticmethod
    def _pt_to_in(given):
        return given / 72.0

    @staticmethod
    def _pt_to_mm(given):
        return given / 72.0 * 25.4

    @staticmethod
    def _abs_to_rel(larger_quantity, smaller_quantity):
        return smaller_quantity / larger_quantity

    @staticmethod
    def _rel_to_abs(quantity, proportion):
        return quantity * proportion


# VII) Colormap

def get_next_colormap_spec(given_colormap_spec, i):
    """Get the i-th colormap spec."""
    colormap_spec_i = dict()

    # - standard treatment (=no alternative value from a more general argument)
    argument_names = [
        'show_colormap', 'colormap', 'colormap_reversed',
        'colormap_label_font', 'colormap_label_size', 'colormap_label_color',
        'colormap_border_size',
    ]
    for arg in argument_names:
        given_val = given_colormap_spec[arg]
        if given_val is None:
            colormap_spec_i[arg] = getattr(_config.settings, arg)
        else:
            try:
                # no iteration if already a named colormap
                assert not isinstance(given_val, str)
                # no iteration if a user-specified colormap
                assert not (isinstance(given_val, _Iterable) and
                            isinstance(given_val[0], _Iterable) and
                            isinstance(given_val[0][0], float) and
                            len(given_val[0]) == 2)
                colormap_spec_i[arg] = given_val[i % len(given_val)]
            except Exception:
                colormap_spec_i[arg] = given_val
    return colormap_spec_i


# VIII) Markers

def get_next_marker_spec(given_marker_spec, given_color, given_opacity, given_colormap, i):
    """Get the i-th marker spec, either from a given or default values."""
    # TODO: allow self-defined colormaps via isinstance(...)
    # TODO: If settings.json has a value for marker_color, then a user-provided color argument
    #       will be overruled be the default marker_color. Maybe change it.

    marker_spec_i = dict()

    # - standard treatment (=no alternative value from a more general argument)
    for arg in ['show_marker', 'marker_size', 'marker_style']:
        given_val = given_marker_spec[arg]
        if given_val is None:
            marker_spec_i[arg] = getattr(_config.settings, arg)
        else:
            try:
                assert not isinstance(given_val, str)
                marker_spec_i[arg] = given_val[i % len(given_val)]
            except Exception:
                marker_spec_i[arg] = given_val

    # - special treatment: marker_color
    # priorities: given marker color / given color / default marker color / default color
    given_marker_color = given_marker_spec['marker_color']
    # given_color = given_color
    default_marker_color = _config.settings.marker_color
    default_color = _config.settings.color

    if given_marker_color is not None:
        used_marker_color = given_marker_color
    elif given_color is not None:
        used_marker_color = given_color
    elif default_marker_color is not None:
        used_marker_color = default_marker_color
    else:
        used_marker_color = default_color

    try:
        assert not isinstance(used_marker_color, str)
        assert not isinstance(used_marker_color, tuple)
        assert not (isinstance(used_marker_color, _Iterable) and
                    isinstance(used_marker_color[0], _Number))
        marker_spec_i['marker_color'] = used_marker_color[i % len(used_marker_color)]
    except Exception:
        marker_spec_i['marker_color'] = used_marker_color

    # - special treatment: marker_opacity
    # priorities: given marker opacity / given opacity / default marker opacity / default opacity
    given_marker_opacity = given_marker_spec['marker_opacity']
    # given_opacity = given_opacity
    default_marker_opacity = _config.settings.marker_opacity
    default_opacity = _config.settings.opacity

    if given_marker_opacity is not None:
        used_marker_opacity = given_marker_opacity
    elif given_opacity is not None:
        used_marker_opacity = given_opacity
    elif default_marker_opacity is not None:
        used_marker_opacity = default_marker_opacity
    else:
        used_marker_opacity = default_opacity

    try:
        assert not isinstance(used_marker_opacity, _Number)
        marker_spec_i['marker_opacity'] = used_marker_opacity[i % len(used_marker_opacity)]
    except Exception:
        marker_spec_i['marker_opacity'] = used_marker_opacity

    # - special treatment: marker_colormap
    # priorities: given marker colormap / given colormap / default marker colormap / def colormap
    given_marker_colormap = given_marker_spec['marker_colormap']
    # given_colormap = given_colormap
    default_marker_colormap = _config.settings.marker_colormap
    default_colormap = _config.settings.colormap

    if given_marker_colormap is not None:
        used_marker_colormap = given_marker_colormap
    elif given_colormap is not None:
        used_marker_colormap = given_colormap
    elif default_marker_color is not None:
        used_marker_colormap = default_marker_colormap
    else:
        used_marker_colormap = default_colormap

    try:
        assert not isinstance(used_marker_colormap, str)  # named colormap
        assert not (isinstance(used_marker_colormap, _Iterable) and  # list of lists colormap
                    isinstance(used_marker_colormap[0], _Iterable) and
                    isinstance(used_marker_colormap[0][0], _Number))
        marker_spec_i['marker_colormap'] = used_marker_colormap[i % len(used_marker_colormap)]
    except Exception:
        marker_spec_i['marker_colormap'] = used_marker_colormap

    return marker_spec_i


# IX) Lines

def get_next_line_spec(given_line_spec, given_color, given_opacity, given_colormap, i):
    """Get the i-th line spec, either from a given or default values."""
    # TODO: create an argument called line_colormap and use given_colormap (does not work
    #       automatically in Plotly but could be interpolated explicitely? maybe not)

    line_spec_i = dict()

    # - standard treatment (=no alternative value from a more general argument)
    for arg in ['show_line', 'line_width', 'line_style']:
        given_val = given_line_spec[arg]
        if given_val is None:
            line_spec_i[arg] = getattr(_config.settings, arg)
        else:
            try:
                assert not isinstance(given_val, str)
                line_spec_i[arg] = given_val[i % len(given_val)]
            except Exception:
                line_spec_i[arg] = given_val

    # - special treatment: line_color
    # priorities: given line color / given color / default line color / default color
    given_line_color = given_line_spec['line_color']
    # given_color = given_color
    default_line_color = _config.settings.line_color
    default_color = _config.settings.color

    if given_line_color is not None:
        used_line_color = given_line_color
    elif given_color is not None:
        used_line_color = given_color
    elif default_line_color is not None:
        used_line_color = default_line_color
    else:
        used_line_color = default_color

    try:
        assert not isinstance(used_line_color, str)
        assert not isinstance(used_line_color, tuple)
        assert not (isinstance(used_line_color, _Iterable) and
                    isinstance(used_line_color[0], _Number))
        line_spec_i['line_color'] = used_line_color[i % len(used_line_color)]
    except Exception:
        line_spec_i['line_color'] = used_line_color

    # - special treatment: line_opacity
    # priorities: given line opacity / given opacity / default line opacity / default opacity
    given_line_opacity = given_line_spec['line_opacity']
    # given_opacity = given_opacity
    default_line_opacity = _config.settings.line_opacity
    default_opacity = _config.settings.opacity

    if given_line_opacity is not None:
        used_line_opacity = given_line_opacity
    elif given_opacity is not None:
        used_line_opacity = given_opacity
    elif default_line_color is not None:
        used_line_opacity = default_line_opacity
    else:
        used_line_opacity = default_opacity

    try:
        assert not isinstance(used_line_color, str)
        line_spec_i['line_opacity'] = used_line_opacity[i % len(used_line_opacity)]
    except Exception:
        line_spec_i['line_opacity'] = used_line_opacity

    return line_spec_i


# X) Rugs
def get_next_rug_spec(given_rug_spec, given_color, given_opacity, given_colormap, i):
    """Get the i-th rug spec, either from a given or default values."""
    # Note: Analogous to get_next_marker_spec, refactor
    rug_spec_i = dict()

    # - standard treatment (=no alternative value from a more general argument)
    for arg in ['show_rug', 'rug_size', 'rug_style']:
        given_val = given_rug_spec[arg]
        if given_val is None:
            rug_spec_i[arg] = getattr(_config.settings, arg)
        else:
            try:
                assert not isinstance(given_val, str)
                rug_spec_i[arg] = given_val[i % len(given_val)]
            except Exception:
                rug_spec_i[arg] = given_val

    # - special treatment: rug_color
    # priorities: given rug color / given color / default rug color / default color
    given_rug_color = given_rug_spec['rug_color']
    default_rug_color = _config.settings.rug_color
    default_color = _config.settings.color

    if given_rug_color is not None:
        used_rug_color = given_rug_color
    elif given_color is not None:
        used_rug_color = given_color
    elif default_rug_color is not None:
        used_rug_color = default_rug_color
    else:
        used_rug_color = default_color

    try:
        assert not isinstance(used_rug_color, str)
        assert not isinstance(used_rug_color, tuple)
        assert not (isinstance(used_rug_color, _Iterable) and
                    isinstance(used_rug_color[0], _Number))
        rug_spec_i['rug_color'] = used_rug_color[i % len(used_rug_color)]
    except Exception:
        rug_spec_i['rug_color'] = used_rug_color

    # - special treatment: rug_opacity
    # priorities: given rug opacity / given opacity / default rug opacity / default opacity
    given_rug_opacity = given_rug_spec['rug_opacity']
    default_rug_opacity = _config.settings.rug_opacity
    default_opacity = _config.settings.opacity

    if given_rug_opacity is not None:
        used_rug_opacity = given_rug_opacity
    elif given_opacity is not None:
        used_rug_opacity = given_opacity
    elif default_rug_opacity is not None:
        used_rug_opacity = default_rug_opacity
    else:
        used_rug_opacity = default_opacity

    try:
        assert not isinstance(used_rug_opacity, _Number)
        rug_spec_i['rug_opacity'] = used_rug_opacity[i % len(used_rug_opacity)]
    except Exception:
        rug_spec_i['rug_opacity'] = used_rug_opacity

    # - special treatment: rug_colormap
    # priorities: given rug colormap / given colormap / default rug colormap / def colormap
    given_rug_colormap = given_rug_spec['rug_colormap']
    default_rug_colormap = _config.settings.rug_colormap
    default_colormap = _config.settings.colormap

    if given_rug_colormap is not None:
        used_rug_colormap = given_rug_colormap
    elif given_colormap is not None:
        used_rug_colormap = given_colormap
    elif default_rug_color is not None:
        used_rug_colormap = default_rug_colormap
    else:
        used_rug_colormap = default_colormap

    try:
        assert not isinstance(used_rug_colormap, str)  # named colormap
        assert not (isinstance(used_rug_colormap, _Iterable) and  # list of lists colormap
                    isinstance(used_rug_colormap[0], _Iterable) and
                    isinstance(used_rug_colormap[0][0], _Number))
        rug_spec_i['rug_colormap'] = used_rug_colormap[i % len(used_rug_colormap)]
    except Exception:
        rug_spec_i['rug_colormap'] = used_rug_colormap

    return rug_spec_i


# XI) Errors

def get_next_x_error_spec(given_x_error_spec, line_spec, color, i):
    """Get the i-th x error spec, either from a given or default values."""
    error_spec_i = dict()

    # - standard treatment (=no alternative value from a more general argument)
    for arg in ['show_x_error_bar', 'x_error_bar_size']:
        given_val = given_x_error_spec[arg]
        if given_val is None:
            error_spec_i[arg] = getattr(_config.settings, arg)
        else:
            try:
                assert not isinstance(given_val, str)
                error_spec_i[arg] = given_val[i % len(given_val)]
            except Exception:
                error_spec_i[arg] = given_val

    # - special treatment: x error bar color
    # priorities: given x error color / given line color / given color /
    #             default x error color / default line color / default color
    given_x_error_bar_color = given_x_error_spec['x_error_bar_color']
    given_line_color = line_spec['line_color']
    given_color = color
    default_x_error_bar_color = _config.settings.x_error_bar_color
    default_line_color = _config.settings.line_color
    default_color = _config.settings.color
    if given_x_error_bar_color is not None:
        used_x_error_bar_color = given_x_error_bar_color
    elif given_line_color is not None:
        used_x_error_bar_color = given_line_color
    elif given_color is not None:
        used_x_error_bar_color = given_color
    elif default_x_error_bar_color is not None:
        used_x_error_bar_color = default_x_error_bar_color
    elif default_line_color is not None:
        used_x_error_bar_color = default_line_color
    else:
        used_x_error_bar_color = default_color
    try:
        assert not isinstance(used_x_error_bar_color, str)
        assert not isinstance(used_x_error_bar_color, tuple)
        assert not (isinstance(used_x_error_bar_color, _Iterable) and
                    isinstance(used_x_error_bar_color[0], _Number))
        n = len(used_x_error_bar_color)
        error_spec_i['x_error_bar_color'] = used_x_error_bar_color[i % n]
    except Exception:
        error_spec_i['x_error_bar_color'] = used_x_error_bar_color

    # - special treatment: x error bar line width
    # priorities: given x error bar line width / given line width /
    #             default x error bar line width / default line width
    given_x_error_bar_line_width = given_x_error_spec['x_error_bar_line_width']
    given_line_width = line_spec['line_width']
    default_x_error_bar_line_width = _config.settings.x_error_bar_line_width
    default_line_width = _config.settings.line_width
    if given_x_error_bar_line_width is not None:
        used_x_error_bar_line_width = given_x_error_bar_line_width
    elif given_line_width is not None:
        used_x_error_bar_line_width = given_line_width
    elif default_x_error_bar_line_width is not None:
        used_x_error_bar_line_width = default_x_error_bar_line_width
    else:
        used_x_error_bar_line_width = default_line_width
    try:
        assert not isinstance(used_x_error_bar_line_width, str)
        n = len(used_x_error_bar_line_width)
        error_spec_i['x_error_bar_line_width'] = used_x_error_bar_line_width[i % n]
    except Exception:
        error_spec_i['x_error_bar_line_width'] = used_x_error_bar_line_width
    return error_spec_i


def get_next_y_error_spec(given_y_error_spec, line_spec, color, opacity, i):
    """Get the i-th y error spec, either from a given or default values."""
    error_spec_i = dict()

    # - standard treatment (=no alternative value from a more general argument)
    for arg in ['show_y_error_bar', 'y_error_bar_size', 'show_y_error_band']:
        given_val = given_y_error_spec[arg]
        if given_val is None:
            error_spec_i[arg] = getattr(_config.settings, arg)
        else:
            try:
                assert not isinstance(given_val, str)
                error_spec_i[arg] = given_val[i % len(given_val)]
            except Exception:
                error_spec_i[arg] = given_val

    # - special treatment: y error bar color
    # priorities: given y error color / given line color / given color /
    #             default y error color / default line color / default color
    given_y_error_bar_color = given_y_error_spec['y_error_bar_color']
    given_line_color = line_spec['line_color']
    given_color = color
    default_y_error_bar_color = _config.settings.y_error_bar_color
    default_line_color = _config.settings.line_color
    default_color = _config.settings.color
    if given_y_error_bar_color is not None:
        used_y_error_bar_color = given_y_error_bar_color
    elif given_line_color is not None:
        used_y_error_bar_color = given_line_color
    elif given_color is not None:
        used_y_error_bar_color = given_color
    elif default_y_error_bar_color is not None:
        used_y_error_bar_color = default_y_error_bar_color
    elif default_line_color is not None:
        used_y_error_bar_color = default_line_color
    else:
        used_y_error_bar_color = default_color
    try:
        assert not isinstance(used_y_error_bar_color, str)
        assert not isinstance(used_y_error_bar_color, tuple)
        assert not (isinstance(used_y_error_bar_color, _Iterable) and
                    isinstance(used_y_error_bar_color[0], _Number))
        n = len(used_y_error_bar_color)
        error_spec_i['y_error_bar_color'] = used_y_error_bar_color[i % n]
    except Exception:
        error_spec_i['y_error_bar_color'] = used_y_error_bar_color

    # - special treatment: y error bar line width
    # priorities: given y error bar line width / given line width /
    #             default y error bar line width / default line width
    given_y_error_bar_line_width = given_y_error_spec['y_error_bar_line_width']
    given_line_width = line_spec['line_width']
    default_y_error_bar_line_width = _config.settings.y_error_bar_line_width
    default_line_width = _config.settings.line_width

    if given_y_error_bar_line_width is not None:
        used_y_error_bar_line_width = given_y_error_bar_line_width
    elif given_line_width is not None:
        used_y_error_bar_line_width = given_line_width
    elif default_y_error_bar_line_width is not None:
        used_y_error_bar_line_width = default_y_error_bar_line_width
    else:
        used_y_error_bar_line_width = default_line_width

    try:
        assert not isinstance(used_y_error_bar_line_width, str)
        n = len(used_y_error_bar_line_width)
        error_spec_i['y_error_bar_line_width'] = used_y_error_bar_line_width[i % n]
    except Exception:
        error_spec_i['y_error_bar_line_width'] = used_y_error_bar_line_width

    # - special treatment: y error band color
    # priorities: given y error band color / given line color / given color /
    #             default y error band / default line color / default color
    given_y_error_band_color = given_y_error_spec['y_error_band_color']
    given_line_color = line_spec['line_color']
    given_color = color
    default_y_error_band_color = _config.settings.y_error_band_color
    default_line_color = _config.settings.line_color
    default_color = _config.settings.color
    if given_y_error_band_color is not None:
        used_y_error_band_color = given_y_error_band_color
    elif given_line_color is not None:
        used_y_error_band_color = given_line_color
    elif given_color is not None:
        used_y_error_band_color = given_color
    elif default_y_error_band_color is not None:
        used_y_error_band_color = default_y_error_band_color
    elif default_line_color is not None:
        used_y_error_band_color = default_line_color
    else:
        used_y_error_band_color = default_color
    try:
        assert not isinstance(used_y_error_band_color, str)
        assert not isinstance(used_y_error_band_color, tuple)
        assert not (isinstance(used_y_error_band_color, _Iterable) and
                    isinstance(used_y_error_band_color[0], _Number))
        n = len(used_y_error_band_color)
        error_spec_i['y_error_band_color'] = used_y_error_band_color[i % n]
    except Exception:
        error_spec_i['y_error_band_color'] = used_y_error_band_color

    # - special treatment: y error band opacity
    # priorities: given y error band opacity / given opacity /
    #             default y error band opacity / default opacity
    given_y_error_band_opacity = given_y_error_spec['y_error_band_opacity']
    given_opacity = opacity
    default_y_error_band_opacity = _config.settings.y_error_band_opacity
    default_opacity = _config.settings.opacity
    if given_y_error_band_opacity is not None:
        used_y_error_band_opacity = given_y_error_band_opacity
    elif given_opacity is not None:
        used_y_error_band_opacity = given_opacity
    elif default_y_error_band_opacity is not None:
        used_y_error_band_opacity = default_y_error_band_opacity
    else:
        used_y_error_band_opacity = default_opacity
    try:
        assert not isinstance(used_y_error_band_opacity, str)
        n = len(used_y_error_band_opacity)
        error_spec_i['y_error_band_opacity'] = used_y_error_band_opacity[i % n]
    except Exception:
        error_spec_i['y_error_band_opacity'] = used_y_error_band_opacity
    return error_spec_i


# -) Color

def normalize_color(given_color):
    """Take a color in one of several formats and transform it into an RGBA tuple."""
    return _conversion.any_color_to_rgba(given_color)


def get_next_color(given_color, i):
    """Get the i-th color, either from a given str/list or from a default list.

    It cycles through the color list, i.e. once the end is reached starts again from the beginning.

    References
    ----------
    - https://personal.sron.nl/~pault
    - https://stats.stackexchange.com/questions/118033/best-series-of-colors-to-use-for-differentiating-series-in-publication-quality
    - http://colorbrewer2.org
    - https://seaborn.pydata.org/tutorial/color_palettes.html

    """
    if isinstance(given_color, (str, tuple)):
        # If the user provided a single color, the *one user-defined color* is returned
        color_i = given_color
    elif isinstance(given_color, _Iterable) and \
            len(given_color) > 0 and isinstance(given_color[0], _Number):
        # If the user provided a list of numbers, this *user-defined color numbers* are returned
        color_i = given_color
    else:
        try:
            # If the user provided a list of colors, the *i-th user-defined color* is returned
            color_i = given_color[i % len(given_color)]
        except Exception:
            # If that does not work (e.g. is None), the *i-th default color* is returned
            default_colors = _config.settings.color
            color_i = default_colors[i % len(default_colors)]
    return color_i


def get_all_colors(given_colors, num_colors):
    """Get the first num_colors colors, either from a given str/list or from a default list."""
    return [get_next_color(given_colors, i) for i in range(num_colors)]


# -) Names

def get_next_name(given_name, i):
    """Get the i-th name."""
    if isinstance(given_name, str):
        name_i = given_name
    else:
        try:
            name_i = given_name[i]  # no cycling to prevent reuse of names
        except Exception:
            name_i = 'Series {}'.format(i+1)
    return name_i


def get_all_names(given_names, num_names):
    """Get all names."""
    return [get_next_name(given_names, i) for i in range(num_names)]


# -) Opacities

def get_next_opacity(given_opacity, i):
    """Get the i-th opacity."""
    if isinstance(given_opacity, _Number):
        opacity_i = given_opacity
    else:
        try:
            opacity_i = given_opacity[i % len(given_opacity)]
        except Exception:
            opacity_i = _config.settings.opacity
    return opacity_i


# -) Stem plane position for 3d plots

def calc_stem_plane_position(xs, ys, zs, stem_shift_factor, given_x, given_y, given_z):
    """Calculate the position of the plane used in a projection with stem lines."""
    x_bound, y_bound, z_bound = None, None, None
    for x, y, z in zip(xs, ys, zs):
        x_bound_i, y_bound_i, z_bound_i = _shared_preprocessing.shift_away_from_extrema(
            x, y, z, direction='lower', shift_factor=stem_shift_factor)
        if x_bound is None or x_bound > x_bound_i:
            x_bound = x_bound_i
        if y_bound is None or y_bound > y_bound_i:
            y_bound = y_bound_i
        if z_bound is None or z_bound > z_bound_i:
            z_bound = z_bound_i

    if given_x is not None:
        x_bound = given_x
    if given_y is not None:
        y_bound = given_y
    if given_z is not None:
        z_bound = given_z
    return x_bound, y_bound, z_bound


# -) Bin sizes for histograms and similar bin counting plots
def calc_bins(data, bin_start=None, bin_end=None, bin_number=None, half_bin_onto_borders=False):
    """Calculate bin sizes for statistical plots that use binning."""
    if bin_start is None:
        data_min = min(data)
        bin_start = data_min - data_min / 10e6
    if bin_end is None:
        data_max = max(data)
        bin_end = data_max + data_max / 10e6
    if bin_number is None:
        bin_number = _config.settings.bin_number

    if half_bin_onto_borders:
        if bin_number > 1:
            span = bin_end - bin_start
            bin_step = span / (bin_number - 1)
            bin_start = bin_start - bin_step / 2.0
            bin_end = bin_end + bin_step / 2.0
        else:
            bin_step = bin_end - bin_start
            bin_start = bin_start - bin_step / 2.0
            bin_end = bin_end + bin_step / 2.0
            bin_step = bin_end - bin_start
    else:
        span = bin_end - bin_start
        bin_step = span / bin_number

    return bin_start, bin_end, bin_step

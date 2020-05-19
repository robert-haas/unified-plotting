"""JavaScript plots for external data (files, resources)."""

import mimetypes as _mimetypes
from numbers import Number as _Number

import requests as _requests

from ..utilities import base64 as _base64
from ..utilities import operating_system as _operating_system
from . import _data_structures, _template_system


def _detect_mimetype(data):
    try:
        mime_type = _mimetypes.guess_type(data)[0]
        assert mime_type and isinstance(mime_type, str)
    except Exception:
        message = (
            'Failed to auto-detect MIME type of the given data. Please provide it manually, '
            'e.g. "application/pdf", "image/png", "image/jpeg" or "image/svg+xml".')
        raise ValueError(message) from None
    return mime_type


def _fetch_url(url):
    try:
        response = _requests.get(url)
        assert response.ok
        result = response.content
        assert result
    except Exception:
        message = 'Failed to fetch data from given URL "{}"'.format(url)
        raise ValueError(message) from None
    return result


def _data_to_data_url(data, mime_type):
    # Case 1: Data is a file
    if _operating_system.is_nonempty_file(data):
        base64_text = _base64.file_to_base64_text(data)
        data_url = 'data:{mt};base64,{b64}'.format(b64=base64_text, mt=mime_type)
    # Case 2: Data is already a data URL
    elif data.startswith('data:'):
        data_url = data
    # Case 3: Assume data is a URL and try to fetch it, otherwise treat the text itself as data
    else:
        try:
            data = _fetch_url(data)
        except Exception:
            pass
        if isinstance(data, bytes):
            base64_text = _base64.binary_data_to_base64_text(data)
        else:
            base64_text = _base64.text_to_base64_text(data)
        data_url = 'data:{mt};base64,{b64}'.format(b64=base64_text, mt=mime_type)
    return data_url


def image_viewer(data, mime_type=None, width=None, height=None,
                 min_width=None, min_height=None, max_width=None, max_height=None,
                 resizable=True, border=True):
    """Create an embedded image from an URL, data URL, filepath or SVG text.

    Parameters
    ----------
    data : str
        Image data in form of an URL, data URL, filepath or SVG text.
    mime_type : str
        MIME type (media type) of the data. If it is not provided, the system tries to guess
        the correct MIME type.
        Examples: "application/pdf", "image/png", "image/jpeg", "image/svg+xml"
    width : int or str
        Exact width of the embedded image.
    height : int or str
        Exact height of the embedded image.
    min_width : int or str
        Minimum width of the embedded image.
    min_height : int or str
        Minimum height of the embedded image.
    max_width : int or str
        Maximum width of the embedded image.
    max_height : int or str
        Maximum height of the embedded image.
    resizable : bool
        If True, the image container can be resized by the user in a webbrowser.
    border : bool
        If True, the image container is shown with a border around it.

    Notes
    -----
    Following precedence rules for the different width and height values are defined by CSS:

    - max-width overrides width, but min-width overrides max-width.

    - max-height overrides height, but min-height overrides max-height.

    All width and height values can be provided as a number or a str with following meaning:

    - If the value is a number, it is interpreted as pixels by converting it to a string
      and adding the suffix "px".

    - If the value is a string, it can be any CSS length number and unit, e.g. "50%", "30mm",
      "200pt", "3in", "5em".
      Caution: Relative heights may not work as indended, but using vh (=1% of viewport height)
      instead of % can help to achieve the desired result.

    Returns
    -------
    A :ref:`Figure <js-figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://developer.mozilla.org/en-US/docs/Web/CSS/max-width
    - https://developer.mozilla.org/en-US/docs/Web/CSS/max-height
    - https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Values_and_units
    - https://en.wikipedia.org/wiki/Media_type
    - https://docs.python.org/3/library/mimetypes.html
    - https://developer.mozilla.org/en-US/docs/Web/HTML/Element/object
    - https://developer.mozilla.org/de/docs/Web/HTML/Element/img

    """
    # Argument processing
    def add_px(val):
        if isinstance(val, _Number):
            val = '{}px'.format(val)
        return val

    width = add_px(width)
    height = add_px(height)
    min_width = add_px(min_width)
    min_height = add_px(min_height)
    max_width = add_px(max_width)
    max_height = add_px(max_height)
    if mime_type is None:
        mime_type = _detect_mimetype(data)
    mime_type = mime_type.lower()

    # Transformation
    # - Arguments to CSS style
    style = ''
    if width:
        style += 'width:{};'.format(width)
    if height:
        style += 'height:{};'.format(height)
    if min_width:
        style += 'min-width:{};'.format(min_width)
    if min_height:
        style += 'min-height:{};'.format(min_height)
    if max_width:
        style += 'max-width:{};'.format(max_width)
    if max_height:
        style += 'max-height:{};'.format(max_height)
    if resizable:
        style += 'resize:both;overflow:hidden;'
    if border:
        style += 'border:1px solid lightgray;border-radius:5px;margin:3px;padding:7px;'
    if style:
        container_style = ' style="{}"'.format(style)  # blank serves as separator from div
    else:
        container_style = ''
    # - Data to data URL
    try:
        data_url = _data_to_data_url(data, mime_type)
    except Exception:
        message = 'Could not convert the provided data to a data URL and hence can not embed it.'
        raise ValueError(message)
    # - Data URL to HTML element
    if 'image' in mime_type:
        html_element = (
            '<img '
            'src="{data_url}" '
            'style="max-width:100%;max-height:100%;" '
            'alt="Image can not be displayed.">'
            '</img>'.format(data_url=data_url)
        )
    else:
        html_element = (
            '<object type="{mime_type}" '
            'data="{data_url}" '
            'width="100%" '
            'height="100%" '
            'alt="Image can not be displayed.">'
            '</object>'.format(mime_type=mime_type, data_url=data_url)
        )
    site_template = _template_system.load('templates/image_viewer.html')
    insert_data = {
        'CONTAINER_STYLE': container_style,
        'DATA': html_element,
    }
    site_template = _template_system.insert(site_template, insert_data)
    fig = _data_structures.Figure(site_template)
    return fig

"""Conversion of data to base64 encoding and HTML elements."""

import base64 as _base64


def binary_data_to_base64_text(binary_data):
    """Convert binary data to text data in Base64 format."""
    return _base64.b64encode(binary_data).decode('utf-8').replace('\n', '')


def text_to_base64_text(text, encoding='utf-8'):
    """Convert text data to text data in Base64 format."""
    binary_data = bytes(text, encoding)
    return binary_data_to_base64_text(binary_data)


def file_to_base64_text(filepath):
    """Convert a file to text data in Base64 format."""
    with open(filepath, 'rb') as file_handle:
        binary_data = file_handle.read()
    return binary_data_to_base64_text(binary_data)


def base64_text_to_data_url(base64_text, data_format):
    """Convert data in form of base64 text to a data URL with suitable prefix."""
    # Argument processing
    if data_format == 'jpg':
        data_format = 'jpeg'
    elif data_format == 'tif':
        data_format = 'tiff'

    # Transformation
    # - MIME type
    if data_format in ['jpeg', 'png', 'tiff', 'webp']:
        mime_type = 'image/' + data_format
    elif data_format == 'svg':
        mime_type = 'image/svg+xml'
    elif data_format == 'pdf':
        mime_type = 'application/pdf'
    elif data_format in ['eps', 'ps']:
        mime_type = 'application/postscript'
    else:
        message = 'Unknown data format. Can not assign a suitable MIME type.'
        raise ValueError(message)
    # - Data URL
    data_url = 'data:{};base64,{}'.format(mime_type, base64_text)
    return data_url


def url_to_img_element(url, width_px, height_px, alternative_text):
    """Convert an URL to a HTML img element."""
    template = '<img src="{}" width="{}" height="{}" alt="{}">'
    return template.format(url, width_px, height_px, alternative_text)


def url_to_object_element(url, width_px, height_px, alternative_text):
    """Convert an URL to a HTML object element."""
    template = '<object data="{}" width="{}" height="{}">{}</object>'
    return template.format(url, width_px, height_px, alternative_text)

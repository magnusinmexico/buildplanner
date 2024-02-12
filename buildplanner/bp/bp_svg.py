# SPDX-FileCopyrightText: 2023-2024 Magnus Pettersson
#
# SPDX-License-Identifier: GPL-3.0-or-later

#------------------------------------------------------------------------------
#
# File: bp_svg.py
# Author: Magnus Pettersson
#
# This module provides utility functions for generating SVG images, including
# functions for creating SVG logos and icons with customizable parameters such
# as size, color, and background.
#
#------------------------------------------------------------------------------

import html

def svg_logo(width: int = None, height: int = None, head: bool = False, color: list[float] = [38, 87, 135], color_text: list[float] = [51, 51, 51]) -> str:
    """
    Generate an SVG logo with customizable parameters.

    Args:
        width (int): The width of the SVG image.
        height (int): The height of the SVG image.
        head (bool): Whether to include XML header.
        color (list[float]): The color of the logo.
        color_text (list[float]): The color of the text.

    Returns:
        str: The SVG logo as a string.
    """
    color = f"rgba({color[0]}, {color[1]}, {color[2]}, 1)"
    color_text = f"rgba({color_text[0]}, {color_text[1]}, {color_text[2]}, 1)"
    str_head = "<?xml version='1.0' encoding='UTF-8'?>" if head else ""
    aspect = 1200.0 / 512.0

    if not (width and height):
        width = 1200
        height = int(round(width / aspect, None))
    elif width and not height:
        height = int(round(width / aspect, None))
    elif height and not width:
        width = int(round(height * aspect, None))

    str_svg = f"""{str_head}
<svg id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 1200 512">
  <defs>
    <style>
      .cls-1 {{
        fill: {color};
      }}
      .cls-2 {{
        fill: {color_text};
      }}
      .cls-1, .cls-2 {{
        stroke-width: 0px;
      }}
    </style>
  </defs>
  <path class="cls-1" d="m383.76,210.75l22.63,22.63c12.48,12.48,12.48,32.78,0,45.25l-135.76,135.76c-12.48,12.48-32.78,12.48-45.25,0l-135.76-135.76c-12.48-12.48-12.48-32.78,0-45.25L225.37,97.61c12.48-12.48,32.78-12.48,45.25,0l45.25,45.25-135.76,135.76,45.25,45.25,113.14-113.14,22.63-22.63,45.25-45.25-90.51-90.51c-37.49-37.49-98.27-37.49-135.76,0L44.35,188.12c-37.49,37.49-37.49,98.27,0,135.76l135.76,135.76c37.49,37.49,98.27,37.49,135.76,0l135.76-135.76c37.49-37.49,37.49-98.27,0-135.76l-22.63-22.63-45.25,45.25Z"/>
  <g>
    <path class="cls-2" d="m560.96,141.47h.36c3.92-6.06,11.41-14.79,27.45-14.79,20.86,0,39.39,16.04,39.39,48.84,0,26.02-11.76,50.98-39.93,50.98-10.34,0-21.39-3.74-27.45-14.44h-.36v11.94h-24.42v-127.99h24.96v45.45Zm20.32,6.77c-17.11,0-21.39,15.33-21.39,30.48,0,14.08,6.24,27.27,22.1,27.27s20.5-17.47,20.5-28.7c0-14.97-5.35-29.06-21.21-29.06Z"/>
    <path class="cls-2" d="m727.62,224h-23.89v-13.37h-.36c-5.7,10.16-15.69,15.86-28.88,15.86-18.72,0-32.26-10.7-32.26-34.94v-62.39h24.96v58.82c0,14.62,8.56,17.47,16.22,17.47,8.2,0,19.25-4.63,19.25-21.57v-54.72h24.96v94.83Z"/>
    <path class="cls-2" d="m776.64,117.94h-24.96v-23.17h24.96v23.17Zm0,11.23v94.83h-24.96v-94.83h24.96Z"/>
    <path class="cls-2" d="m826.19,224h-24.96v-127.99h24.96v127.99Z"/>
    <path class="cls-2" d="m936.71,224h-24.42v-11.94h-.36c-6.06,10.7-17.11,14.44-27.45,14.44-28.16,0-39.93-24.96-39.93-50.98,0-32.8,18.54-48.84,39.39-48.84,16.04,0,23.53,8.73,27.45,14.79h.36v-45.45h24.96v127.99Zm-45.99-18c15.86,0,22.1-13.19,22.1-27.27,0-15.15-4.28-30.48-21.39-30.48-15.86,0-21.21,14.08-21.21,29.06,0,11.23,4.46,28.7,20.5,28.7Z"/>
  </g>
  <g>
    <path class="cls-2" d="m671.1,382.85h-24.96v-127.99h24.96v127.99Z"/>
    <path class="cls-2" d="m771.81,364.31c0,11.23,2.5,13.73,5.53,14.79v3.74h-26.92c-1.43-4.46-1.78-5.88-2.32-11.23-5.7,5.88-13.73,13.73-30.66,13.73-14.26,0-28.88-8.02-28.88-27.63,0-18.54,11.76-27.99,27.63-30.3l22.46-3.39c3.92-.54,8.73-2.14,8.73-7.49,0-10.52-9.98-11.05-16.4-11.05-12.48,0-14.62,7.67-15.33,13.19h-24.06c2.85-29.06,23-33.16,42.42-33.16,13.37,0,37.79,4.1,37.79,27.45v51.34Zm-24.42-27.63c-2.5,1.96-6.6,3.56-16.93,5.17-9.27,1.6-16.93,3.92-16.93,14.26,0,8.73,6.77,11.41,11.59,11.41,11.05,0,22.28-7.13,22.28-18.72v-12.12Z"/>
    <path class="cls-2" d="m879.83,382.85h-24.96v-57.58c0-6.95-.36-18.72-16.22-18.72-11.05,0-19.61,7.49-19.61,21.92v54.37h-24.96v-94.83h23.89v13.9h.36c3.39-5.7,10.52-16.4,28.52-16.4s32.98,10.87,32.98,31.73v65.6Z"/>
    <path class="cls-2" d="m988.74,382.85h-24.96v-57.58c0-6.95-.36-18.72-16.22-18.72-11.05,0-19.61,7.49-19.61,21.92v54.37h-24.96v-94.83h23.89v13.9h.36c3.39-5.7,10.52-16.4,28.52-16.4s32.98,10.87,32.98,31.73v65.6Z"/>
    <path class="cls-2" d="m1093.37,355.04c-6.59,22.82-25.49,30.3-41.71,30.3-26.74,0-47.24-12.83-47.24-51.87,0-11.41,3.92-47.95,45.46-47.95,18.72,0,44.56,8.91,44.56,52.23v4.46h-65.06c.71,7.13,2.14,23.17,22.28,23.17,6.95,0,14.08-3.56,16.04-10.34h25.67Zm-24.6-29.05c-1.43-15.33-11.23-19.96-19.25-19.96-11.76,0-18,7.49-19.43,19.96h38.68Z"/>
    <path class="cls-2" d="m1110.83,288.02h23.89v16.4h.36c5.17-9.62,10.87-18.89,26.03-18.89,1.6,0,3.21.18,4.81.36v25.31c-2.14-.36-4.81-.36-7.13-.36-19.43,0-23,12.12-23,22.64v49.38h-24.96v-94.83Z"/>
  </g>
  <path class="cls-2" d="m588.57,285.52c-16.76,0-23.71,8.73-28.34,16.22h-.36v-13.73h-23.89v127.96h24.96v-45.25h.36c3.03,5.17,9.27,14.62,26.74,14.62,28.16,0,39.93-24.96,39.93-50.98,0-32.8-18.54-48.84-39.39-48.84Zm-6.77,79.32c-15.86,0-21.92-13.19-21.92-27.27,0-15.15,4.1-30.48,21.21-30.48,15.87,0,21.21,14.08,21.21,29.06,0,11.23-4.46,28.7-20.5,28.7Z"/>
</svg>"""

    return str_svg

def svg_icon(size: int = 24, encode=True, head: bool = False, background=False, color: list[float] = [38, 87, 135]) -> str:
    """
    Generate an SVG icon with customizable parameters.

    Args:
        size (int): The size of the icon.
        encode (bool): Whether to HTML-encode the SVG content.
        head (bool): Whether to include XML header.
        background (bool): Whether to include background.
        color (list[float]): The color of the icon.

    Returns:
        str: The SVG icon as a string.
    """
    color = f"rgba({color[0]}, {color[1]}, {color[2]}, 1)"
    str_head = "<?xml version='1.0' encoding='UTF-8'?>" if head else ""

    str_svg = f"""{str_head}
<svg id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 512 512">
  <defs>
    <style>
      .cls-1 {{
        fill: {color};
        stroke-width: 0px;
      }}
    </style>
  </defs>
  <path class="cls-1" d="m391.76,210.75l22.63,22.63c12.48,12.48,12.48,32.78,0,45.25l-135.76,135.76c-12.48,12.48-32.78,12.48-45.25,0l-135.76-135.76c-12.48-12.48-12.48-32.78,0-45.25L233.37,97.61c12.48-12.48,32.78-12.48,45.25,0l45.25,45.25-135.76,135.76,45.25,45.25,113.14-113.14,22.63-22.63,45.25-45.25-90.51-90.51c-37.49-37.49-98.27-37.49-135.76,0L52.35,188.12c-37.49,37.49-37.49,98.27,0,135.76l135.76,135.76c37.49,37.49,98.27,37.49,135.76,0l135.76-135.76c37.49-37.49,37.49-98.27,0-135.76l-22.63-22.63-45.25,45.25Z"/>
</svg>"""

    if encode:
        str_svg = html.escape(str_svg)

    return str_svg

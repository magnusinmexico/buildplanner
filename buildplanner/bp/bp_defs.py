# SPDX-FileCopyrightText: 2023-2024 Magnus Pettersson
#
# SPDX-License-Identifier: GPL-3.0-or-later

#------------------------------------------------------------------------------
#
# File: bp_defs.py
# Author: Magnus Pettersson
#
# This module defines dictionaries for length unit conversion factors and 
# suffixes.
#
#------------------------------------------------------------------------------

length_unit_scale_factor = {
    'NONE': 1.0,           # No unit 
    'MILLIMETERS': 1000.0,
    'CENTIMETERS': 100.0,
    'METERS': 1.0,
    'KILOMETERS': 0.001,
    'INCHES': 39.3701,
    'FEET': 3.28084,
    'MILES': 0.000621371,
    'YARDS': 1.09361,
    'NANOMETERS': 1e9,
    'MICROMETERS': 1e6,
}

length_unit_suffix = {
    'NONE': "",            # No unit
    'MILLIMETERS': "mm",
    'CENTIMETERS': "cm",
    'METERS': "m",
    'KILOMETERS': "km",
    'INCHES': "Inches",
    'FEET': "Feet",
    'MILES': "Miles",
    'YARDS': "Yards",
    'NANOMETERS': "nm",
    'MICROMETERS': "um",
}

#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
builder/model_choices.py
   Populate dropdown list/choices in the builder app.

TODO:
  - Default copyright notice

"""

##############################################################################
#   Internal Model Choices
##############################################################################

# TODO: Sort by membership size
INSTITUTIONS = (
    ('UNM', 'University of New Mexico'),
    ('TECH', 'NM Tech'),
    ('ENM', 'Eastern New Mexico University'),
    ('NMSU', 'New Mexico State University'),
    ('SFI', 'Santa Fe Institute'),
    ('SFCC', 'Santa Fe Community College'),
    ('UNLISTED', 'My Institution Not in List'),
)

COMPONENTS = (
    ('UNKNOWN', 'I do not know my component'),
    ('BIOALGAL', 'BioAlgal Energy'),
    ('GEOTHERMAL', 'Geothermal'),
    ('OSMOTIC', 'Osmotic Power'),
    ('SOLAR', 'Solar Energy'),
    ('SOCIAL', 'Social/Science Nexus'),
    ('URANIUM', 'Uranium'),
    ('WAVE', 'WC-Wave'),
)

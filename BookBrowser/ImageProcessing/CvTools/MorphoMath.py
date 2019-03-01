####################################################################################################
#
# BookBrowser - A Digitised Book Solution
# Copyright (C) 2018 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

"""Module to implement usual `Mathematical Morphology
<https://en.wikipedia.org/wiki/Mathematical_morphology>`_ operations using the OpenCV library.

It basically fix the poor API of OpenCV.

A more serious library is `Mamba <http://www.mamba-image.org>`_ from the `Centre de Morphologie
Mathématique de Paris <http://cmm.ensmp.fr>`_ whose source code is available at
https://github.com/nicolasBeucher/mamba-image, but apparently it is no longer maintained (last
update on September 2017).  See also `Serge Beucher home page <http://cmm.ensmp.fr/~beucher>`_ (last
update on June 2017), he is no longer a referenced member of the CMM on late 2018 (
http://cmm.ensmp.fr/staff.php ). See also <Simple Morphological Image Library
<http://smil.cmm.mines-paristech.fr/wiki/doku.php>`_.

"""

####################################################################################################

__all__ = [
    'alternate_sequential_filter',
    'anti_diagonal_structuring_element',
    'ball_structuring_element',
    'circular_structuring_element',
    'diagonal_structuring_element',
    'horizontal_structuring_element',
    'morphology_close',
    'morphology_dilate',
    'morphology_erode',
    'morphology_gradient',
    'morphology_open',
    'vertical_structuring_element',
]

####################################################################################################

import numpy as np

import cv2 as cv

####################################################################################################

def ball_structuring_element(horizontal_radius, vertical_radius=None):

    """Construct a ball (rectangular) structuring element"""

    if vertical_radius is None:
        vertical_radius = horizontal_radius

    number_of_rows = 2*vertical_radius +1
    number_of_columns = 2*horizontal_radius +1
    kernel = np.ones((number_of_rows, number_of_columns))
    anchor = (horizontal_radius, vertical_radius)

    return kernel, anchor

####################################################################################################

# Fixme: purpose ???
# def _unit_ball():
#     radius = 1
#     return ball_structuring_element(radius, radius)
#
# unit_ball = _unit_ball() # unit ball structuring element

####################################################################################################

def horizontal_structuring_element(radius):
    """Construct an horizontal structuring element"""
    return ball_structuring_element(horizontal_radius=radius, vertical_radius=0)

def vertical_structuring_element(radius):
    """Construct a vertical structuring element"""
    return ball_structuring_element(horizontal_radius=0, vertical_radius=radius)

####################################################################################################

def circular_structuring_element(radius):

    """Construct a circular structuring element"""

    size = 2*radius +1
    kernel = np.ones((size, size), dtype=np.uint8)
    for i in range(1, radius +1):
        for j in range(1, radius +1):
            if i**2 + j**2 > radius**2:
                kernel[radius+i, radius+j] = 0
                kernel[radius-i, radius+j] = 0
                kernel[radius+i, radius-j] = 0
                kernel[radius-i, radius-j] = 0
    anchor = (radius, radius)

    return kernel, anchor

####################################################################################################

def diagonal_structuring_element(radius):

    """Construct a diagonal structuring element"""

    size = 2*radius +1
    kernel = np.ones((size, size), dtype=np.uint8)
    anchor = (radius, radius)

    return kernel, anchor

####################################################################################################

def anti_diagonal_structuring_element(radius):

    """Construct a anti-diagonal structuring element"""

    size = 2*radius +1
    kernel = np.transpose(np.ones((size, size), dtype=np.uint8))
    anchor = (radius, radius)
    return kernel, anchor

####################################################################################################

def morphology_erode(image_src, image_dst, structuring_element):
    """Apply a erosion to the input image"""
    kernel, anchor = structuring_element
    cv.erode(image_src, kernel, image_dst, anchor)

####################################################################################################

def morphology_dilate(image_src, image_dst, structuring_element):
    """Apply a dilation to the input image"""
    kernel, anchor = structuring_element
    cv.dilate(image_src, kernel, image_dst, anchor)

####################################################################################################

def morphology_close(image_src, image_dst, structuring_element):
    """Apply a closing (dilation followed by a erosion) to the input image"""
    kernel, anchor = structuring_element
    cv.morphologyEx(image_src, cv.MORPH_CLOSE, kernel, image_dst, anchor)

####################################################################################################

def morphology_open(image_src, image_dst, structuring_element):
    """Apply an opening (erosion followed by a dilation) to the input image"""
    kernel, anchor = structuring_element
    cv.morphologyEx(image_src, cv.MORPH_OPEN, kernel, image_dst, anchor)

####################################################################################################

def morphology_gradient(image_src, image_dst, structuring_element):
    """Apply a gradient to the input image"""
    kernel, anchor = structuring_element
    cv.morphologyEx(image_src, cv.MORPH_GRADIENT, kernel, image_dst, anchor)

####################################################################################################

def alternate_sequential_filter(image_src, image_dst, radius_max, structuring_element, open_first=True):

    """Apply sequentially to the image an open and close operation with an increasing *structuring
    element* radius from 1 to *radius_max*.  The order of the operations, open and close, is
    determined by the *open_first* parameter.

    """

    operations = (cv.MORPH_OPEN, cv.MORPH_CLOSE)
    if not open_first:
        operations = list(reversed(operations))

    for radius in range(1, radius_max +1):
        kernel, anchor = structuring_element(radius)
        for operation in operations:
            cv.morphologyEx(image_src, operation, kernel, image_dst, anchor)
            image_src = image_dst # Fixme: ok ???

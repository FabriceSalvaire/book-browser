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

"""Module to implement image thresholding using the OpenCV library.

It basically fix the poor API of OpenCV.

"""

####################################################################################################

import numpy as np

import cv2 as cv

####################################################################################################

def threshold(image_src, image_dst, threshold, threshold_type, max_value=255):
    # Source array (single-channel, 8-bit or 32-bit floating point)
    # max_value is used for THRESH_BINARY
    image_float = np.array(image_src, dtype=np.float32) # Fixme:
    cv.threshold(image_float, threshold, max_value, threshold_type, image_float)
    image_dst[...] = image_float[...]

####################################################################################################

def threshold_to_zero(image_src, image_dst, threshold):
    threshold(image_src, image_dst, threshold, cv.THRESH_TOZERO)

####################################################################################################

def threshold_to_binary(image_src, image_dst, threshold, max_value=255):
    threshold(image_src, image_dst, threshold, cv.THRESH_BINARY, max_value)

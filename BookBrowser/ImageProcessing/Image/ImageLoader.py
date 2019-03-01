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

__all__ = ['load_image']

####################################################################################################

# If OpenCV is not available then fallback to Pillow
try:
    import cv2 as cv
except ImportError:
    cv = None
    import numpy as np
    import PIL.Image as PIL_Image

####################################################################################################

from .ImageFormat import ImageFormat
from .Image import Image

####################################################################################################

def load_image(path):

    path = str(path)

    if cv is not None:
        cv_array = cv.imread(path)
        # CV uses BGR format
        image = Image(cv_array, share=True, channels=ImageFormat.BGR)
        image = image.swap_channels(ImageFormat.RGB)
    else:
        array = np.array(PIL_Image.open(path))
        image = Image(array, channels=ImageFormat.RGB)

    return image

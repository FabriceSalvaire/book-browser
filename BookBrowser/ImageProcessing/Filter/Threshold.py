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

####################################################################################################

__all__ = [
    'OtsuThresholdingFilter',
]

####################################################################################################

import logging

import cv2 as cv

from ..ImageFilter import ImageFilter

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class OtsuThresholdingFilter(ImageFilter):

    """Filter to apply an Otsu thresholding"""

    __filter_name__ = 'Gaussian Blur Filter'
    __input_names__ = ('input',)
    __output_names__ = ('blur_image',)

    ##############################################

    # def __init__(self):

    #     super().__init__()

    ##############################################

    def generate_data(self):

        self._logger.info(self.name)

        input_ = self.input().image
        output = self.output().image
        self.threshold, _ = cv.threshold(input_, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU, output)
        self._logger.info("Otsu threshold: {}".format(self.threshold))

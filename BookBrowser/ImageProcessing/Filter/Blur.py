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

__all__ = ['GaussianBlurFilter']

####################################################################################################

import logging

import cv2 as cv

from ..ImageFilter import ImageFilter

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class GaussianBlurFilter(ImageFilter):

    """Gaussian Blur filter"""

    __filter_name__ = 'Gaussian Blur Filter'
    __input_names__ = ('input',)
    __output_names__ = ('blur_image',)

    ##############################################

    def __init__(self, radius=1, sigma_x=0):

        super().__init__()

        self._radius = radius
        self._sigma_x = sigma_x

    ##############################################

    def generate_data(self):

        self._logger.info(self.name)

        input_ = self.input().image
        output = self.output().image

        cv.GaussianBlur(input_, (self._radius, self._radius), self._sigma_x, output)

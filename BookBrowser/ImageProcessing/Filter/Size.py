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
    'ResizeFilter',
]

####################################################################################################

import logging

import cv2 as cv

from ..ImageFilter import ImageFilter

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class ResizeFilter(ImageFilter):

    """Filter to resize an image"""

    __filter_name__ = 'Resize Filter'
    __input_names__ = ('input',)
    __output_names__ = ('resized_image',)

    ##############################################

    def __init__(self, scale_factor=1):

        super().__init__()

        self._scale_factor = scale_factor

    ##############################################

    def generate_image_format(self, output):

        image_format = self.input().image_format
        return image_format.clone(
            width=int(round(image_format.width * self._scale_factor)),
            height=int(round(image_format.height * self._scale_factor)),
        )

    ##############################################

    def generate_data(self):

        self._logger.info(self.name)

        input_ = self.input().image
        output = self.output().image
        cv.resize(
            input_,
            None,
            dst=output,
            fx=self._scale_factor,
            fy=self._scale_factor,
            interpolation=cv.INTER_CUBIC,
        )

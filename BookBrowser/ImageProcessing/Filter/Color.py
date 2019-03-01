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

__all__ = [
    'HlsFilter',
    'GrayFilter',
]

####################################################################################################

import logging

from ..ImageFilter import ImageFilter
from ..Image import ImageFormat

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class HlsFilter(ImageFilter):

    """Filter to convert to HLS color space"""

    __filter_name__ = 'HLS Filter'
    __input_names__ = ('input',)
    __output_names__ = ('hls_image',)

    _logger = _module_logger.getChild('HlsFilter')

    ##############################################

    def generate_image_format(self, output):

        image_format = self.nput().image_format
        return image_format.clone(
            data_type=np.float32,
            normalised=True,
            channels=ImageFormat.HLS,
        )

    ##############################################

    def generate_data(self):

        self._logger.info(self.name)

        input_ = self.input().image
        output = self.output().image
        input_.convert_colour(ImageFormat.HLS, output) # HLS is redundant here

####################################################################################################

class GrayFilter(ImageFilter):

    """Filter to convert to gray image"""

    __filter_name__ = 'Gray Filter'
    __input_names__ = ('input',)
    __output_names__ = ('gray_image',)

    _logger = _module_logger.getChild('GrayFilter')

    ##############################################

    def generate_image_format(self, output):

        image_format = self.input().image_format
        return image_format.clone(
            number_of_channels=1, # Fixme: should be implicit !
            channels=ImageFormat.Gray,
        )

    ##############################################

    def generate_data(self):

        self._logger.info(self.name)

        input_ = self.input().image
        output = self.output().image
        input_.convert_colour(ImageFormat.Gray, output) # Gray is redundant here

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
    'InverseFilter',
]

####################################################################################################

import logging

from ..ImageFilter import ImageFilter
from ..Image import ImageFormat

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class InverseFilter(ImageFilter):

    """Filter to inverse a binary image"""

    __filter_name__ = 'Inverse Filter'
    __input_names__ = ('input',)
    __output_names__ = ('inverse_image',)

    _logger = _module_logger.getChild('InverseFilter')

    ##############################################

    def generate_data(self):

        self._logger.info(self.name)

        input_ = self.input()
        if input_.image_format.channels != ImageFormat.Gray:
            raise ValueError("Invalid image format, a gray image is required")

        output = self.output().image
        output[...] = 255 - input_.image

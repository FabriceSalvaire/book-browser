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
    'OpenFilter',
    'CloseFilter',
    'AsfFilter',
]

####################################################################################################

import logging

# import cv2 as cv

from ..CvTools import MorphoMath
from ..ImageFilter import ImageFilter

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class OpenFilter(ImageFilter):

    """Open Filter"""

    __filter_name__ = 'Open Filter'
    __input_names__ = ('input',)
    __output_names__ = ('open_image',)

    ##############################################

    def __init__(self, structuring_element):

        super().__init__()

        self._structuring_element = structuring_element

    ##############################################

    def generate_data(self):

        self._logger.info(self.name)

        input_ = self.input().image
        output = self.output().image
        MorphoMath.morphology_open(input_, output, self._structuring_element)

####################################################################################################

class CloseFilter(OpenFilter):

    """Close Filter"""

    __filter_name__ = 'Close Filter'
    __output_names__ = ('close_image',)

    ##############################################

    def generate_data(self):

        self._logger.info(self.name)

        input_ = self.input().image
        output = self.output().image
        MorphoMath.morphology_close(input_, output, self._structuring_element)

####################################################################################################

class AsfFilter(ImageFilter):

    """Alternate Sequential Filter"""

    __filter_name__ = 'Alternate Sequential Filter'
    __input_names__ = ('input',)
    __output_names__ = ('asf_image',)

    ##############################################

    def __init__(self, max_radius, structuring_element, open_first=True):

        super().__init__()

        self._max_radius = max_radius
        self._structuring_element = structuring_element
        self._open_first = open_first

    ##############################################

    def generate_data(self):

        self._logger.info(self.name)

        input_ = self.input().image
        output = self.output().image
        MorphoMath.alternate_sequential_filter(
            input_, output,
            self._max_radius,
            self._structuring_element,
            self._open_first,
        )

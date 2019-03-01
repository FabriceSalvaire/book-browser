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
    'ImageLoaderFilter',
    'InputImageFilter',
]

####################################################################################################

import logging

from ..Image import ImageLoader
from ..ImageFilter import ImageFilter

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class InputImageFilter(ImageFilter):

    """Filter for input image"""

    __filter_name__ = 'Input Image Filter'
    __input_names__ = ()
    __output_names__ = ('image',)

    ##############################################

    def __init__(self, image=None):

        super().__init__()

        if image is not None:
            self.update_image(image)

    ##############################################

    def update_image(self, image):

        output = self.output()
        output.image = image
        # output._image_format = output.image.image_format # Fixme: ???
        self.modified()

    ##############################################

    def generate_data(self):
        self._logger.info(self.name)

####################################################################################################

class ImageLoaderFilter(InputImageFilter):

    """Filter to load an image"""

    __filter_name__ = 'Image Loader Filter'

    ##############################################

    def __init__(self, path=None):

        super().__init__()

        if path is not None:
            self.update_image_path(path)

    ##############################################

    def update_image_path(self, path):

        image = ImageLoader.load_image(path)
        self.update_image(image)

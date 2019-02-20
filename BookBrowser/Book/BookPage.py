####################################################################################################
#
# BookBrowser - A book browser
# Copyright (C) 2019 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

__all__ = [
    'BookPage'
    'EmptyBookPage,'
]

####################################################################################################

import logging
import os
import stat

import PIL
from PIL import Image
import numpy as np

from BookBrowser.Common.FileTools import file_watcher

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

RECTO = 'r'
VERSO = 'v'

####################################################################################################

class EmptyBookPage:

    ##############################################

    def __init__(self, page_number):
        self._page_number = page_number

    ##############################################

    @property
    def is_empty(self):
        return True

    ##############################################

    def __int__(self):
        return self._page_number

    ##############################################

    @property
    def page_number(self):
        return self._page_number

    @property
    def orientation(self):
        return RECTO

####################################################################################################

class BookPage:

    _logger = _module_logger.getChild('BookPage')

    ##############################################

    def __init__(self, book, filename):

        self._book = book
        self._filename = str(filename)

        self._parse_filename()
        self.release_image()

        self._mtime = os.stat(self.path)[stat.ST_MTIME]

    ##############################################

    @property
    def is_empty(self):
        return False

    ##############################################

    def __repr__(self):
        template = 'Book Page\n  {0.path}\n  {0._title} {0._page_number}/{0._file_index} {0._extension}'
        return template.format(self)

    def __str__(self):
        return str(self.path)

    def __int__(self):
        return self._page_number or self._file_index

    def __lt__(self, other):
        """Sort by page number or index"""
        return int(self) < int(other)

    ##############################################

    @property
    def book(self):
        return self._book

    ##############################################

    @property
    def filename(self):
        return self._filename

    @property
    def path(self):
        return self._book.joinpath(self._filename)

    # @path.setter
    # def path(self, value):
    #     self._path = value

    ##############################################

    @property
    def mtime(self):
        return self._mtime

    ##############################################

    @property
    def file_index(self):
        return self._file_index

    # @file_index.setter
    # def file_index(self, value):
    #     self._file_index = int(value)

    ##############################################

    @property
    def title(self):
        return self._title

    @property
    def page_number(self):
        return self._page_number

    @property
    def orientation(self):
        return self._orientation

    @property
    def is_recto(self):
        return self._orientation == RECTO

    @property
    def is_verso(self):
        return self._orientation == VERSO

    @property
    def extension(self):
        return self._extension

    ##############################################

    def _parse_filename(self):

        title, page_number, *parts, extension = self._filename.split('.')

        self._title = title
        self._extension = extension

        if page_number.startswith('p'):
            self._page_number = int(page_number[1:])
            self._file_index = None
        else:
            self._page_number = None
            self._file_index = int(page_number)

        if len(parts) == 1:
            self._orientation = parts[0]
        else:
            self._orientation = 'x'

    ##############################################

    def _load_image(self, reload=False):
        if self._image is None or reload:
            pil_image = Image.open(self.path)
            self._image = np.asarray(pil_image)
            # self._logger.info('Image shape {}'.format(self._image.shape))

    ##############################################

    def _load_dual_image(self, reload=False):
        self._load_image(reload)
        if self._dual_image is None or reload:
            self._dual_image = 255 - self._image

    ##############################################

    def release_image(self):
        self._image = None
        self._dual_image = None

    ##############################################

    @property
    def image(self):
        self._load_image()
        return self._image

    @property
    def dual_image(self):
        self._load_dual_image()
        return self._dual_image

    ##############################################

    def flip_image(self):
        # Fixme: is it fast ???
        # self.image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        self._image = np.flip(self.image, 0)

    ##############################################

    def guess_orientation(self, height=100, c_inf=0, c_sup=400):

        dual_image = self.dual_image

        top = int(np.sum(dual_image[:height,c_inf:c_sup]))
        bottom = int(np.sum(dual_image[-height:,c_inf:c_sup]))
        delta_ratio = 100 * (top - bottom)/top
        self._logger.info('top vs bottom {:.2f}'.format(delta_ratio))

        return delta_ratio > 0

    ##############################################

    def get_histogram(self):

        dual_image = self.dual_image
        height, width, _ = dual_image.shape
        self._number_of_pixels = height*width
        channels = [dual_image[:,:,i] for i in range(3)]
        red, green, blue = channels

        histogram = [np.array(np.histogram(channel, bins=256))[0] for channel in channels]
        self._histogram = histogram

    ##############################################

    def compare_histogram(self, other):

        delta = 0
        for i in range(3):
            delta_histogram = self._histogram[i] - other._histogram[i]
            delta_channel = np.sum((delta_histogram[20:-20]/self._number_of_pixels)**2)
            delta += delta_channel**2
        return delta

    ##############################################

    def rename(self, file_index=None, page_number=None, orientation=None, suffix='', dry_run=False):

        if page_number is not None:
            self._page_number = int(page_number)

        if orientation is not None:
            self._orientation = str(orientation)

        number_of_digits = self._book.number_of_digits
        if file_index is None and self._page_number is not None:
            template = '{0._title}.p{0._page_number:0' + str(number_of_digits) + '}.{0._orientation}.{0._extension}'
        else:
            template = '{0._title}.{0._file_index:0' + str(number_of_digits) + '}.{0._orientation}.{0._extension}'

        if file_index is not None:
            self._file_index = file_index
            self._page_number = None

        old_path = str(self.path) + str(suffix)
        filename = template.format(self)
        new_path = self._book.joinpath(filename)
        self._logger.info('rename\n  {}\n->\n{}'.format(old_path, new_path))
        if old_path != new_path:
            if file_watcher.rename_file(old_path, new_path, dry_run=dry_run):
                self._filename = filename
                return True
        return False

    ##############################################

    def flip(self, orientation=None):

        if orientation is None:
            orientation = self._orientation
            if orientation == RECTO:
                orientation = VERSO
            elif orientation == VERSO:
                orientation = RECTO
            else:
                orientation = None

        if orientation is not None:
            self.rename(orientation=orientation)

    ##############################################

    def to_text(self, language, fake=False):

        from BookBrowser.OCR import OcrEngine
        ocr_engine = OcrEngine()

        if self.is_verso:
            self.flip_image()

        text = ocr_engine.image_to_text(self.image, language, fake)

        self.release_image()

        return text

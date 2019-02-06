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
    'BookPage',
    'Book',
]

####################################################################################################

from pathlib import Path
import logging
import math
import os
import stat

from PIL import Image
import numpy as np

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

def rename_file(old_path, new_path, dry_run=False):

    old_path = str(old_path)
    new_path = str(new_path)

    _module_logger.info('Rename\n  {}\n->\n{}'.format(old_path, new_path))
    if Path(new_path).exists():
        _module_logger.warning('Cannot rename file: file exists\n{}'.format(new_path))
        return False
    else:
        if not dry_run:
            os.rename(old_path, new_path)
        return True

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
            self._dual_image = 255 - self._image
            # self._logger.info('Image shape {}'.format(self._image.shape))

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
        self._load_image()
        return self._dual_image

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
            if rename_file(old_path, new_path, dry_run=dry_run):
                self._filename = filename
                return True
        return False

    ##############################################

    def flip(self, orientation=None):

        if orientation is None:
            orientation = self._orientation
            if orientation == 'r':
                orientation = 'v'
            elif orientation == 'v':
                orientation = 'r'
            else:
                orientation = None

        if orientation is not None:
            self.rename(orientation=orientation)

####################################################################################################

class Book:

    _logger = _module_logger.getChild('Book')

    ##############################################

    def __init__(self, path, extension='.png'):

        self._path = Path(str(path)).resolve()
        self._extension = str(extension)

        self._pages = None
        self._get_pages()
        if self.number_of_pages:
            self._number_of_digits = int(math.log10(self.number_of_pages)) + 1
        else:
            self._number_of_digits = 3 # Fixme: ???
        self.check()

    ##############################################

    @property
    def path(self):
        return self._path

    @property
    def extension(self):
        return self._extension

    @property
    def number_of_digits(self):
        return self._number_of_digits

    ##############################################

    def __len__(self):
        return len(self._pages)

    @property
    def number_of_pages(self):
        return len(self._pages)

    def __iter__(self):
        return iter(self._pages)

    def __getitem__(self, page_number):
        return self._pages[page_number -1]

    ##############################################

    @property
    def first_page(self):
        return self._pages[0]

    @property
    def last_page(self):
        return self._pages[-1]

    ##############################################

    @property
    def last_page_number(self):
        """Last page number or index"""
        return int(self.last_page)

    ##############################################

    def iter_by_page_number(self):
        pages = list(self._pages)
        pages.sort(key=lambda page: int(page))
        return iter(pages)

    ##############################################

    def iter_by_mtime(self):
        pages = list(self._pages)
        pages.sort(key=lambda page: page.mtime)
        return iter(pages)

    ##############################################

    def _get_pages(self):

        self._pages = []
        for path, directories, files in os.walk(str(self._path)):
            for filename in files:
                if filename.endswith('_'):
                    path = str(self.joinpath(filename))
                    if not rename_file(path, path[:-1]):
                        filename = filename[:-1]
                    else:
                        raise NameError('')
                if filename.endswith(self._extension):
                    try:
                        self.add_page(filename)
                    except Exception as exception:
                        self._logger.warning('Error on {}\n{}'.format(filename, exception))

        self._pages.sort() # by page number or index

    ##############################################

    def add_page(self, filename):
        page = BookPage(self, filename)
        self._pages.append(page)
        return page

    ##############################################

    def joinpath(self, filename):
        return self._path.joinpath(str(filename))

    ##############################################

    def check(self):

        page_numbers = {}
        for page in self._pages:
            page_number = page.page_number
            if page_number is not None:
                if page_number not in page_numbers:
                    page_numbers[page_number] = 1
                else:
                    self._logger.warning('Page number duplicate {}'.format(page_number))
            if page.orientation not in ('r', 'v'):
                self._logger.warning('Page orientation unset {} '.format(page_number))

    ##############################################

    def fix_empty_pages(self):

        pages = []
        page_number = 0
        for page in self._pages:
            page_number += 1
            if page.page_number is not None and page_number < page.page_number:
                for i in range(page.page_number - page_number):
                    self._logger.warning('Missing page {}'.format(page_number))
                    pages.append(None)
                    page_number += 1
            pages.append(page)
        self._pages = pages

    ##############################################

    def set_orientation(self, positive_delta=True):

        for page in self._pages:
            if page.orientation == 'x':
                self._logger.info(repr(page))
                orientation = page.guess_orientation()
                if not positive_delta:
                    orientation = not orientation
                orientation = 'r' if orientation else 'v'
                if not page.rename(orientation=orientation):
                    raise NameError('')
                page.release_image()

    ##############################################

    def renumerate_pages(self, dry_run=False):

        renames = []
        page_number = 0
        for page in self.iter_by_mtime():
            if page.page_number is None:
                page_number += 1
                renames.append((page, page_number))
                # print('{} -> {}'.format(page.file_index, page_number))
            else:
                if page_number < page.page_number:
                    self._logger.warning('Missing page number {}'.format(page_number))
                elif page_number > page.page_number:
                    self._logger.warning('Inconsitent page number {} > {}'.format(page_number, page.page_number))
                    raise NameError('')
                page_number = page.page_number

        if not dry_run:
            for page, _ in renames:
                path = page.path
                rename_file(path, str(path) + '_') # , dry_run=dry_run

        for page, page_number in renames:
            self._logger.info('Rename {} -> {}'.format(page.file_index, page_number))
            if not dry_run:
                page.rename(page_number=page_number, suffix='_') # , dry_run=dry_run

    ##############################################

    def remove_page_number(self):

        file_index = 0
        for page in self.iter_by_mtime():
            file_index += 1
            page.rename(file_index=file_index)

    ##############################################

    def flip_from_page(self, page_number, orientation):

        for i in range(page_number, self.number_of_pages +1):
            # print(i, orientation)
            self[i].flip(orientation=orientation)
            if orientation == 'r':
                orientation = 'v'
            else:
                orientation = 'r'

    ##############################################

    def _test(self):
        pass

        # pages = self._pages #[:10]

        # for page in pages:
        #     self._logger.info(repr(page))
        #     page.get_histogram()
        #     page.release_image()

        # pages = list(self._pages)
        # pages.sort(key=lambda page: page.footprint)
        # for page in pages:
        #     print(page.filename, page.footprint)

        # page = None
        # duplicat = None
        # duplicat_index = 455
        # for page in pages:
        #     if page.file_index == duplicat_index:
        #         duplicat = page
        # results = []
        # for page in pages:
        #     delta = page.compare_histogram(duplicat)
        #     results.append((page, delta))
        # results.sort(key=lambda result: result[1])
        # for result in results:
        #     print(*result)

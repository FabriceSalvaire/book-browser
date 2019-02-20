####################################################################################################
#
# BookBrowser - A Digitised Book Solution
# Copyright (C) 2019 Fabrice Salvaire
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

__all__ = ['Book']

####################################################################################################

from operator import itemgetter
from pathlib import Path
import logging
import math
import os

from BookBrowser.Common.FileTools import file_watcher
from .BookMetadata import BookMetadata
from .BookPage import BookPage, EmptyBookPage

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Book:

    __book_page_cls__ = BookPage

    EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp', '.tiff')

    _logger = _module_logger.getChild('Book')

    ##############################################

    def __init__(self, path, extension=None):

        # extension='.png'

        self._path = Path(str(path)).resolve()

        # Fixme: will create a book even if it is a wrong path !
        self._load_metadta()

        if extension is not None:
            self._extension = str(extension)
        else:
            self._extension = self._guess_extension()

        self._pages = None
        self._get_pages()
        if self.number_of_pages:
            self._number_of_digits = int(math.log10(self.number_of_pages)) + 1
        else:
            self._number_of_digits = 3 # Fixme: ???
        self.check()

    ##############################################

    @property
    def metadata_path(self):
        return self._path.joinpath(BookMetadata.JSON_FILENAME)

    ##############################################

    def _load_metadta(self):

        json_path = self.metadata_path
        if json_path.exists():
            self._logger.info('Load book metadata {}'.format(json_path))
            self._metadata = BookMetadata.load_json(json_path)
        else:
            self._metadata = BookMetadata(
                path=self._path,
                # number_of_pages=self.number_of_pages,
            )
            self.save_metadata()

    ##############################################

    def save_metadata(self):

        from .BookLibrary import BookLibrary
        if BookLibrary.is_library(self._path):
            self._logger.warning('{} is a library'.format(self._path))
        else:
            json_path = self.metadata_path
            self._logger.info('Save book metadata {}'.format(json_path))
            self._metadata.save_json(json_path)

    ##############################################

    @property
    def metadata(self):
        return self._metadata

    ##############################################

    @property
    def _list_dir(self):
        return iter(os.listdir(self._path))

    ##############################################

    def _guess_extension(self):

        extensions = {}
        for filename in self._list_dir:
            suffix = Path(filename).suffix
            extensions.setdefault(suffix, 0)
            extensions[suffix] += 1

        if extensions:
            extension = sorted(extensions.items(), key=itemgetter(1))[-1][0]
        else:
            extension = '.png'
        # Check for supported image format
        # https://doc.qt.io/qt-5/qtimageformats-index.html
        if extension not in self.EXTENSIONS:
            extension = '.png'
        self._logger.info('Guessed extension {}'.format(extension))

        return extension

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
        try:
            return self._pages[0]
        except IndexError:
            return None

    @property
    def last_page(self):
        try:
            return self._pages[-1]
        except IndexError:
            return None

    ##############################################

    @property
    def last_page_number(self):
        """Last page number or index"""
        if self.number_of_pages:
             return int(self.last_page)
        else:
            return 0

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
        for filename in self._list_dir:
            # Fixme: fix _ suffix
            if filename.endswith('_'):
                path = str(self.joinpath(filename))
                if not file_watcher.rename_file(path, path[:-1]):
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
        page = self.__book_page_cls__(self, filename)
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
            # if page.orientation not in ('r', 'v'):
            #     self._logger.warning('Page orientation unset {} '.format(page_number))

    ##############################################

    def fix_empty_pages(self):

        pages = []
        page_number = 0
        for page in self._pages:
            page_number += 1
            if page.page_number is not None and page_number < page.page_number:
                for i in range(page.page_number - page_number):
                    self._logger.warning('Missing page {}'.format(page_number))
                    pages.append(EmptyBookPage(page_number))
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

    def renumerate_pages(self, dry_run=False, iter_by_mtime=False):

        if iter_by_mtime:
            page_iter = self.iter_by_mtime()
        else:
            page_iter = self

        renames = []
        page_number = 0
        for page in page_iter:
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
                file_watcher.rename_file(path, str(path) + '_') # , dry_run=dry_run

        for page, page_number in renames:
            self._logger.info('Rename {} -> {}'.format(page.file_index, page_number))
            # if not dry_run:
            page.rename(page_number=page_number, suffix='_', dry_run=dry_run)

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

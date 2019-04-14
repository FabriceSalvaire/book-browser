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

__all__ = ['BookLibrary']

####################################################################################################

from operator import attrgetter
from pathlib import Path
import glob
import json
import logging
import os

from .Book import Book
from .BookMetadata import BookMetadata

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class BookCover:

    __json_keys__ = (
        ('path', str),
        ('cover_path', str),
    )

    _logger = _module_logger.getChild('BookCover')

    ##############################################

    def __init__(self, path, cover_path=None):

        self._path = path
        self._metadata = None
        self._cover_path = cover_path

    ##############################################

    @property
    def path(self):
        return self._path

    @property
    def metadata(self):
        if self._metadata is None:
            json_path = BookMetadata.make_json_path(self._path)
            self._metadata = BookMetadata.load_json(json_path)
        return self._metadata

    ##############################################

    @property
    def cover_path(self):
        if self._cover_path is None:
            # files = os.listdir(self._path)
            images = []
            for extension in Book.EXTENSIONS:
                pattern = str(self._path.joinpath('*' + extension))
                images += glob.glob(pattern)
            images.sort()
            if len(images) < 1:
                self._logger.warning('Any cover for {}'.format(self._path))
                return None
            self._cover_path = images[0] # Fixme: full proof ???
            self._logger.info('Cover set to {}'.format(self._cover_path))
        return self._cover_path

    ##############################################

    def to_dict(self):
        return {key:ctor(getattr(self, '_' + key)) for key, ctor in self.__json_keys__}

    ##############################################

    @classmethod
    def load_from_json(cls, json_data):
        return cls(**json_data)

####################################################################################################

class BookLibrary:

    _logger = _module_logger.getChild('BookLibrary')

    JSON_FILENAME = '.book-library-metadata.json'

    ##############################################

    @classmethod
    def make_json_path(cls, library_path):
        # Fixme: func
        # library_path = Path(str(library_path)).resolve()
        return library_path.joinpath(cls.JSON_FILENAME)

    ##############################################

    @classmethod
    def is_library(cls, library_path):
        return cls.make_json_path(library_path).exists()

    ##############################################

    def __init__(self, path):

        self._path = Path(str(path)).resolve()

        self._books = []

    ##############################################

    @property
    def path(self):
        return self._path

    ##############################################

    def scan(self):

        root_path = str(self._path)
        for path, directories, files in os.walk(root_path):
            for directory in directories:
                book_path = Path(path).joinpath(directory)
                json_path = BookMetadata.make_json_path(book_path)
                if json_path.exists():
                    # self._logger.info('Book {}'.format(book_path))
                    book_cover = BookCover(book_path)
                    self._books.append(book_cover)
        self.sort_by_title()

    ##############################################

    def __len__(self):
        return len(self._books)

    def __iter__(self):
        return iter(self._books)

    def __getitemm__(self, slice_):
        return self._books[slice_]

    ##############################################

    def sort_by_title(self):
        self._books.sort(key=lambda book: book.metadata.title)

    ##############################################

    def dump(self):

        self.scan()
        for book in self:
            print('-'*80)
            print(book.path)
            print(book.metadata.title)
            print(book.cover_path)
        self.save_json()

    ##############################################

    @property
    def json_path(self):
        return self.make_json_path(self._path)

    ##############################################

    def load_from_json(self):

        path = self.json_path
        with open(str(path), 'r') as fh:
            json_data = json.loads(fh.read())

        for json_book_cover in json_data:
            book_cover = BookCover.load_from_json(json_book_cover)
            self._books.append(book_cover)

    ##############################################

    def to_json(self):
        data = [book_cover.to_dict() for book_cover in self._books]
        return json.dumps(data, sort_keys=True, indent=4)

    ##############################################

    def save_json(self):

        if BookMetadata.is_book(self._path):
            self._logger.warning('{} is a book'.format(self._path))
        else:
            path = self.json_path
            with open(str(path), 'w') as fh:
                data_json = self.to_json()
                self._logger.info(str(data_json))
                fh.write(data_json)

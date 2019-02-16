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

__all__ = ['BookMetadata']

####################################################################################################

from pathlib import Path
import json
import logging

import isbnlib
import langcodes

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class BookMetadata:

    _logger = _module_logger.getChild('BookMetadata')

    JSON_FILENAME = '.book-metadata.json'

    __json_keys__ = (
        'authors',
        'description',
        'isbn',
        'keywords',
        'language',
        'number_of_pages',
        'page_offset',
        'path',
        'publisher',
        'title',
        'year',
    )

    ##############################################

    def __init__(self, **kwargs):

        self.authors = kwargs.get('authors', ())
        self.isbn = kwargs.get('isbn', '')
        self.language = kwargs.get('language', '')
        self.number_of_pages = kwargs.get('number_of_pages', 0)
        self.publisher = kwargs.get('publisher', '')
        self.title = kwargs.get('title', '')
        self.year = kwargs.get('year', 0)

        self.path = kwargs.get('path', '')
        self.page_offset = kwargs.get('page_offset', 0)

        self.keywords = kwargs.get('keywords', ())
        self.description = kwargs.get('description', '')

    ##############################################

    @classmethod
    def load_json(cls, path):
        with open(str(path), 'r') as fh:
            json_data = json.loads(fh.read())
        return cls(**json_data)

    ##############################################

    def to_dict(self):
        return {key:getattr(self, '_' + key) for key in self.__json_keys__}

    ##############################################

    def to_json(self):
        data = self.to_dict()
        data['path'] = str(data['path'])
        return json.dumps(data, sort_keys=True, indent=4)

    ##############################################

    def save_json(self, path):
        with open(str(path), 'w') as fh:
            fh.write(self.to_json())

    ##############################################

    @staticmethod
    def _check(value, ctor):
        return ctor(value)

    @classmethod
    def _check_int(cls, value):
        return cls._check(value, int)

    @classmethod
    def _check_str(cls, value):
        return cls._check(value, str)

    ##############################################

    @property
    def authors(self):
        return iter(self._authors)

    @property
    def authors_str(self):
        return ', '.join(self._authors)

    @authors.setter
    def authors(self, value):
        if isinstance(value, str):
            self._authors = (value,)
        else:
            self._authors = tuple([str(x) for x in value])

    ##############################################

    @property
    def language(self):
        if self._language:
            return self._language.language_name()
        else:
            return ''

    @language.setter
    def language(self, value):
        try:
            self._language = langcodes.find(value)
        except (LookupError, AttributeError):
            self._language = ''
            if value:
                self._logger.warning('Unknown language {}'.format(value))

    ##############################################

    @property
    def number_of_pages(self):
        return self._number_of_pages

    @number_of_pages.setter
    def number_of_pages(self, value):
        self._number_of_pages = self._check_int(value)

    ##############################################

    @property
    def publisher(self):
        return self._publisher

    @publisher.setter
    def publisher(self, value):
        self._publisher = self._check_str(value)

    ##############################################

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = self._check_str(value)

    ##############################################

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = self._check_int(value)

    ##############################################

    @property
    def isbn(self):
        return self._isbn

    @property
    def isbn_str(self):
        if self._isbn:
            return isbnlib.mask(self._isbn)
        else:
            return ''

    @isbn.setter
    def isbn(self, value):
        if not value:
            self._isbn = ''
        else:
            try:
                if isbnlib.is_isbn13(value):
                    self._isbn = isbnlib.canonical(value)
                elif isbnlib.is_isbn10(value):
                    self._isbn = isbnlib.to_isbn13(value)
            except:
                raise ValueError('Invalid ISBN {}'.format(value))

    ##############################################

    def update_from_isbn(self):

        if self._isbn:
            meta = isbnlib.meta(self._isbn)
            self.authors = meta.get('Authors', ())
            self.language = meta.get('Langage', '')
            self.publisher = meta.get('Publisher', '')
            self.title = meta.get('Title', '')
            self.year = meta.get('Year', 0)

    ##############################################

    @property
    def path(self):
        return self._path

    @property
    def path_str(self):
        return str(self._path)

    @path.setter
    def path(self, value):
        if value:
            self._path = Path(str(value))
        else:
            self._path = ''

    ##############################################

    @property
    def page_offset(self):
        return self._page_offset

    @page_offset.setter
    def page_offset(self, value):
        self._page_offset = int(value)

    ##############################################

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = self._check_str(value)

    ##############################################

    @property
    def keywords(self):
        return iter(self._keywords)

    @property
    def keywords_str(self):
        return ', '.join(self._keywords)

    @keywords.setter
    def keywords(self, value):
        self._keywords = tuple([str(x) for x in value])

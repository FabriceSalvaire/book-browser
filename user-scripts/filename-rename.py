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

####################################################################################################

from pathlib import Path
import logging

from BookBrowser.Book import BookPage, Book

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class MyBookPage(BookPage):

    _logger = _module_logger.getChild('MyBookPage')

    ##############################################

    def _parse_filename(self):

        try:
            title, page_number, *parts, extension = self._filename.split('.')
        except ValueError:
            # Fixme: filename pattern
            extension = (Path(self._filename).suffix)[1:]
            position = self._filename.rfind('-')
            if position != -1:
                title = self._filename[:position]
                page_number = self._filename[position+1:-len(extension)-1]
                parts = ()
            else:
                raise

        self._title =  self._book.path.name # title
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

####################################################################################################

class MyBook(Book):

    __book_page_cls__ = MyBookPage

    _logger = _module_logger.getChild('MyBook')

####################################################################################################

application.book_cls = MyBook

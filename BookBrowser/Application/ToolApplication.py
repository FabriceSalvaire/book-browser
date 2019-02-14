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

"""Module to implement the tool application.

"""

####################################################################################################

__all__ = [
    'ToolApplication',
]

####################################################################################################

import logging

from .BasicApplication import BasicApplication
from BookBrowser.Book import Book
from BookBrowser.Common.ArgparseAction import PathAction

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class ToolApplication(BasicApplication):

    """Class to implement a basic Application."""

    description = 'Book Browser Tool.'

    book_cls = Book # Fixme: name

    _logger = _module_logger.getChild('BasicApplication')

    ##############################################

    def __init__(self):

        super().__init__()

        self._book = None

    ##############################################

    @property
    def book(self):
        return self._book

    ##############################################

    def init_arguments(self):

        super().init_arguments()

        self._parser.add_argument(
            'book_path', metavar='BookPath',
            action=PathAction,
            help='Book path',
        )

        self._parser.add_argument(
            '--dump',
            action='store_true',
            default=False,
            help='dump',
        )

        self._parser.add_argument(
            '--rename',
            action='store_true',
            default=False,
            help='rename pages',
        )

        self._parser.add_argument(
            '--rename-by-mtime',
            action='store_true',
            default=False,
            help='rename-by-mtime pages',
        )

        self._parser.add_argument(
            '--orientation',
            action='store_true',
            default=False,
            help='set page orientation',
        )

        self._parser.add_argument(
            '--negative-delta',
            action='store_true',
            default=False,
            help='set negative delta for  orientation',
        )

        self._parser.add_argument(
            '--remove-page-number',
            action='store_true',
            default=False,
            help='remove page numbers',
        )

    ##############################################

    def run(self):

        super().run()

        self._book = self.book_cls(self._args.book_path)

        if self._args.dump:
            print(self._book.path)
            for i, page in enumerate(self._book):
                template = 'Book Page {0:3} | {1.filename} | {1.title} {1.file_index}/{1.page_number} {1.extension}'
                print(template.format(i+1, page))

        if self._args.rename:
            self._book.renumerate_pages(self._args.dry_run)

        if self._args.orientation:
            self._book.set_orientation(positive_delta=not self._args.negative_delta)

        if self._args.remove_page_number:
            self._book.remove_page_number()
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
    'QmlBook',
]

####################################################################################################

from pathlib import Path
import glob
import logging
import time

from PyQt5 import QtCore
from QtShim.QtCore import (
    Property, Signal, Slot, QObject,
    Qt, QTimer, QUrl
)

from BookBrowser.Book import Book

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class QmlBookPage(QtCore.QObject):

    _logger = _module_logger.getChild('QmlBookPage')

    ##############################################

    def __init__(self, book_page):

        super().__init__()

        self._page = book_page

    ##############################################

    def __repr__(self):
        return '{0} {1}'.format(self.__class__.__name__, self._page)

    ##############################################

    pathChanged = Signal()

    @Property(str, notify=pathChanged)
    def path(self):
        return str(self._page.path)

    ##############################################

    page_numberChanged = Signal()

    @Property(int, notify=page_numberChanged)
    def page_number(self):
        return int(self._page) # self._page.page_number

    ##############################################

    orientationChanged = Signal()

    @Property(int, notify=orientationChanged)
    def orientation(self):
        return 180 if self._page.orientation == 'v' else 0

    ##############################################

    @Slot(str)
    def flip_page(self, orientation):
        # don't emit orientationChanged
        self._page.flip(orientation)

####################################################################################################

class QmlBook(QtCore.QObject):

    new_page = QtCore.pyqtSignal(int)

    _logger = _module_logger.getChild('QmlBook')

    ##############################################

    def __init__(self, path):

        super().__init__()

        self._book = Book(path)
        self._book.fix_empty_pages()

        # We must prevent garbage collection
        self._pages = [QmlBookPage(page) for page in self._book]

    ##############################################

    @Property(str)
    def path(self):
        return str(self._book.path)

    ##############################################

    number_of_pagesChanged = Signal()

    @Property(int, notify=number_of_pagesChanged)
    def number_of_pages(self):
        # return self._book.number_of_pages
        return len(self._pages)

    @Slot(int, result=bool)
    def is_valid_page_number(self, page_number):
        return 0 < page_number <= self.number_of_pages

    ##############################################

    @Property(QmlBookPage)
    def first_page(self):
        return self._pages[0]

    @Property(QmlBookPage)
    def last_page(self):
        return self._pages[-1]

    @Slot(int, result=QmlBookPage)
    def page(self, page_number):
        try:
            return self._pages[page_number-1]
        except IndexError:
            return None

    ##############################################

    @Slot(QmlBookPage, str)
    def flip_from_page(self, page, orientation):
        self._book.flip_from_page(page.page_number, orientation)

    ##############################################

    def start_watcher(self, watcher=None):

        if QtCore is None:
            raise NotImplementedError

        self._files = set(self._glob_files())

        self._watcher = watcher or QtCore.QFileSystemWatcher()
        self._watcher.addPath(str(self._book.path))
        self._watcher.directoryChanged.connect(self._on_directory_change)

    ##############################################

    def _glob_files(self):
        pattern = str(self._book.path.joinpath('*' + self._book.extension))
        for path in glob.glob(pattern):
            yield Path(path).name

    ##############################################

    def _on_directory_change(self, path):

        time.sleep(3)
        # QTimer::singleShot(200, this, SLOT(updateCaption()));

        files = set(self._glob_files())
        new_files = files - self._files
        self._logger.info('New files {}'.format(new_files))
        # Fixme: overwrite

        for filename in new_files:
            self._on_new_file(filename)

        self._files = files

    ##############################################

    def _on_new_file(self, filename):

        self._logger.info('New file {}'.format(filename))

        # try:

        page = self._book.add_page(filename)
        page._page_number = self._book.number_of_pages # Fixme: !!!
        self._logger.info('New page\n{}'.format(page))

        self._pages.append(QmlBookPage(page))
        self.number_of_pagesChanged.emit()
        self.new_page.emit(page.page_number)

        # except Exception as exception:
        #     self._logger.warning('Error on {}\n{}'.format(filename, exception))

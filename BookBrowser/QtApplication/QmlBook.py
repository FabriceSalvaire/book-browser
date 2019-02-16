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

from PyQt5.QtCore import QFileSystemWatcher
from PyQt5.QtQml import QQmlListProperty
from QtShim.QtCore import (
    Property, Signal, Slot, QObject,
    Qt, QTimer, QUrl
)

from BookBrowser.Thumbnail import FreeDesktopThumbnailCache # Fixme: Linux only
from BookBrowser.Book import Book
from .Runnable import Worker

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

thumbnail_cache = FreeDesktopThumbnailCache()

####################################################################################################

class QmlBookMetadata(QObject):

    _logger = _module_logger.getChild('QmlBookMetadata')

    ##############################################

    def __init__(self, book_metadata):

        super().__init__()

        self._metadata = book_metadata

    ##############################################

    @Property(str, constant=True)
    def path(self):
        return self._metadata.path_str

    ##############################################

    number_of_pages_changed = Signal()

    @Property(int, notify=number_of_pages_changed)
    def number_of_pages(self):
        return self._metadata.number_of_pages

    @number_of_pages.setter
    def number_of_pages(self, value):
        if self.number_of_pages != value:
            self._metadata.number_of_pages == value
            self.number_of_pages_changed.emit()

####################################################################################################

class QmlBookPage(QObject):

    _logger = _module_logger.getChild('QmlBookPage')

    thumbnail_ready = Signal()

    ##############################################

    def __init__(self, book_page):

        super().__init__()

        self._page = book_page

    ##############################################

    def __repr__(self):
        return '{0} {1}'.format(self.__class__.__name__, self._page)

    ##############################################

    @property
    def page(self):
        return self._page

    ##############################################

    path_changed = Signal()

    @Property(str, notify=path_changed)
    def path(self):
        return str(self._page.path)

    ##############################################

    @Property(int, constant=True)
    def large_thumbnail_size(self):
        return FreeDesktopThumbnailCache.LARGE_SIZE

    large_thumbnail_path_changed = Signal()

    @Property(str, notify=large_thumbnail_path_changed)
    def large_thumbnail_path(self):
        # Fixme: cache thumbnail instance ?
        return str(thumbnail_cache[self._page.path].large_path)

    ##############################################

    @Slot()
    def request_large_thumbnail(self):

        def job():
            # Fixme: issue when the application is closed
            return str(thumbnail_cache[self._page.path].large)

        worker = Worker(job)
        # worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thumbnail_ready)
        # worker.signals.progress.connect(self.progress_fn)

        from .QmlApplication import Application
        Application.instance.thread_pool.start(worker)

    ##############################################

    page_number_changed = Signal()

    @Property(int, notify=page_number_changed)
    def page_number(self):
        return int(self._page) # self._page.page_number

    ##############################################

    orientation_changed = Signal()

    @Property(int, notify=orientation_changed)
    def orientation(self):
        return 180 if self._page.orientation == 'v' else 0

    ##############################################

    @Slot(str)
    def flip_page(self, orientation):
        # don't emit orientation_changed
        self._page.flip(orientation)

####################################################################################################

class QmlBook(QObject):

    new_page = Signal(int)

    _logger = _module_logger.getChild('QmlBook')

    ##############################################

    def __init__(self, path):

        super().__init__()

        self._book = Book(path)
        self._book.fix_empty_pages()

        self._metadata = QmlBookMetadata(self._book.metadata)

        # We must prevent garbage collection
        self._pages = [QmlBookPage(page) for page in self._book]

    ##############################################

    @Property(str)
    def path(self):
        return str(self._book.path)

    ##############################################

    @Property(QmlBookMetadata)
    def metadata(self):
        return self._metadata

    ##############################################

    number_of_pages_changed = Signal()

    @Property(int, notify=number_of_pages_changed)
    def number_of_pages(self):
        # return self._book.number_of_pages
        return len(self._pages)

    @Slot(int, result=bool)
    def is_valid_page_number(self, page_number):
        return 0 < page_number <= self.number_of_pages

    ##############################################

    last_page_number_changed = Signal()

    @Property(int, notify=last_page_number_changed)
    def last_page_number(self):
        return self._book.last_page_number

    ##############################################

    pages_changed = Signal()

    @Property(QQmlListProperty, notify=pages_changed)
    def pages(self):
        return QQmlListProperty(QmlBookPage, self, self._pages)

    ##############################################

    @Property(QmlBookPage)
    def first_page(self):
        try:
            return self._pages[0]
        except IndexError:
            return None

    @Property(QmlBookPage)
    def last_page(self):
        try:
            return self._pages[-1]
        except IndexError:
            return None

    @Slot(int, result=QmlBookPage)
    def page(self, page_number):
        try:
            return self._pages[page_number-1]
        except IndexError:
            return None

    ##############################################

    @Slot(QmlBookPage, str)
    def flip_from_page(self, qml_page, orientation):
        # Fixme: qml_page.page.page_number is None
        self._logger.info('{} {}'.format(qml_page.page_number, orientation))
        self._book.flip_from_page(qml_page.page_number, orientation)

    ##############################################

    def start_watcher(self, watcher=None):

        self._files = set(self._glob_files())

        self._watcher = watcher or QFileSystemWatcher()
        self._watcher.addPath(str(self._book.path))
        self._watcher.directory_changed.connect(self._on_directory_change)

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
        self.number_of_pages_changed.emit()
        self.new_page.emit(page.page_number)

        # except Exception as exception:
        #     self._logger.warning('Error on {}\n{}'.format(filename, exception))

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

__all__ = [
    'QmlBookLibrary',
]

####################################################################################################

import logging

from PyQt5.QtQml import QQmlListProperty
from QtShim.QtCore import (
    Property, Signal, Slot, QObject,
)

from BookBrowser.Book import BookLibrary
from BookBrowser.Thumbnail import FreeDesktopThumbnailCache # Fixme: Linux only
from .Runnable import Worker

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

thumbnail_cache = FreeDesktopThumbnailCache()

####################################################################################################

class QmlBookCover(QObject):

    _logger = _module_logger.getChild('QmlBookCover')

    ##############################################

    def __init__(self, book_cover):

        super().__init__()

        self._book_cover = book_cover

    ##############################################

    @Property(str, constant=True)
    def path(self):
        return str(self._book_cover.path)

    @Property(str, constant=True)
    def cover_path(self):
        cover_path = self._book_cover.cover_path
        if cover_path:
            return str(cover_path)
        else:
            return ''

    ##############################################

    # Fixme: duplicate code

    @Property(int, constant=True)
    def large_thumbnail_size(self):
        return FreeDesktopThumbnailCache.LARGE_SIZE

    large_thumbnail_path_changed = Signal()

    @Property(str, notify=large_thumbnail_path_changed)
    def large_thumbnail_path(self):
        # Fixme: cache thumbnail instance ?
        cover_path = self.cover_path
        if cover_path:
            return str(thumbnail_cache[cover_path].large_path)
        else:
            return ''

    ##############################################

    thumbnail_ready = Signal()

    @Slot()
    def request_large_thumbnail(self):

        cover_path = self.cover_path
        if not cover_path:
            return

        def job():
            # Fixme: issue when the application is closed
            return str(thumbnail_cache[cover_path].large)

        worker = Worker(job)
        # worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thumbnail_ready)
        # worker.signals.progress.connect(self.progress_fn)

        from .QmlApplication import Application
        Application.instance.thread_pool.start(worker)

####################################################################################################

class QmlBookLibrary(QObject):

    _logger = _module_logger.getChild('QmlBookLibrary')

    ##############################################

    def __init__(self, path):

        super().__init__()

        self._book_library = BookLibrary(path)
        self.scan()

    ##############################################

    def _make_book_covers(self):
        # We must prevent garbage collection
        self._book_covers = [QmlBookCover(book_cover) for book_cover in self._book_library]

    @Property(str, constant=True)
    def path(self):
        return str(self._book_library.path)

    ##############################################

    @Slot()
    def scan(self):
        self._book_library.scan()
        self._make_book_covers()
        self.books_changed.emit()

    ##############################################

    @Slot()
    def save(self):
        self._book_library.save_json()

    ##############################################

    @Property(str, constant=True)
    def path(self):
        return str(self._book_library.path)

    ##############################################

    books_changed = Signal()

    @Property(QQmlListProperty, notify=books_changed)
    def books(self):
        return QQmlListProperty(QmlBookCover, self, self._book_covers)

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
    'QmlBook',
]

####################################################################################################

from pathlib import Path
import glob
import logging
import subprocess
import time

from PyQt5.QtCore import QCoreApplication, QFileSystemWatcher
from PyQt5.QtQml import QQmlListProperty
from QtShim.QtCore import (
    Property, Signal, Slot, QObject,
    Qt, QTimer, QUrl
)

import markdown

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

    def __init__(self, book):

        super().__init__()

        self._book = book
        self._metadata = book.metadata
        self._dirty = False

    ##############################################

    @staticmethod
    def _to_list(value):
        return [x.strip() for x in value.split(',')]

    ##############################################

    @Property(str, constant=True)
    def path(self):
        return self._metadata.path_str

    ##############################################

    dirty_changed = Signal()

    @Property(bool, notify=dirty_changed)
    def dirty(self):
        return self._dirty

    def _set_dirty(self, value=True):
        if self._dirty != value:
            self._dirty = value
            self.dirty_changed.emit()

    ##############################################

    authors_changed = Signal()

    @Property(str, notify=authors_changed)
    def authors(self):
        return self._metadata.authors_str

    @authors.setter
    def authors(self, value):
        value = self._to_list(value)
        if self.authors != value:
            self._metadata.authors = value
            self.authors_changed.emit()
            self._set_dirty()

    ##############################################

    isbn_changed = Signal()

    @Property(str, notify=isbn_changed)
    def isbn(self):
        return self._metadata.isbn_str

    @isbn.setter
    def isbn(self, value):
        if self.isbn != value:
            self._metadata.isbn = value
            self.isbn_changed.emit()
            self._set_dirty()

    ##############################################

    language_changed = Signal()

    @Property(str, notify=language_changed)
    def language(self):
        return self._metadata.language

    @language.setter
    def language(self, value):
        if self.language != value:
            self._metadata.language = value
            self.language_changed.emit()
            self._set_dirty()

    ##############################################

    number_of_pages_changed = Signal()

    @Property(int, notify=number_of_pages_changed)
    def number_of_pages(self):
        return self._metadata.number_of_pages

    @number_of_pages.setter
    def number_of_pages(self, value):
        if self.number_of_pages != value:
            self._metadata.number_of_pages = value
            self.number_of_pages_changed.emit()
            self._set_dirty()

    ##############################################

    publisher_changed = Signal()

    @Property(str, notify=publisher_changed)
    def publisher(self):
        return self._metadata.publisher

    @publisher.setter
    def publisher(self, value):
        if self.publisher != value:
            self._metadata.publisher = value
            self.publisher_changed.emit()
            self._set_dirty()

    ##############################################

    title_changed = Signal()

    @Property(str, notify=title_changed)
    def title(self):
        return self._metadata.title

    @title.setter
    def title(self, value):
        if self.title != value:
            self._metadata.title = value
            self.title_changed.emit()
            self._set_dirty()

    ##############################################

    year_changed = Signal()

    @Property(int, notify=year_changed)
    def year(self):
        return self._metadata.year

    @year.setter
    def year(self, value):
        if self.year != value:
            self._metadata.year = value
            self.year_changed.emit()
            self._set_dirty()

    ##############################################

    page_offset_changed = Signal()

    @Property(int, notify=page_offset_changed)
    def page_offset(self):
        return self._metadata.page_offset

    @page_offset.setter
    def page_offset(self, value):
        if self.page_offset != value:
            self._metadata.page_offset = value
            self.page_offset_changed.emit()
            self._set_dirty()

    ##############################################

    keywords_changed = Signal()

    @Property(str, notify=keywords_changed)
    def keywords(self):
        return self._metadata.keywords_str

    @keywords.setter
    def keywords(self, value):
        value = self._to_list(value)
        if self.keywords != value:
            self._metadata.keywords = value
            self.keywords_changed.emit()
            self._set_dirty()

    ##############################################

    description_changed = Signal()

    @Property(str, notify=description_changed)
    def description(self):
        return self._metadata.description

    @description.setter
    def description(self, value):
        if self.description != value:
            self._metadata.description = value
            self.description_changed.emit()
            self._set_dirty()

    ##############################################

    notes_changed = Signal()
    notes_html_changed = Signal()

    @Property(str, notify=notes_changed)
    def notes(self):
        return self._metadata.notes

    @Property(str, notify=notes_html_changed)
    def notes_html(self):
        return markdown.markdown(self._metadata.notes)

    @notes.setter
    def notes(self, value):
        if self.notes != value:
            self._metadata.notes = value
            self.notes_changed.emit()
            self.notes_html_changed.emit()
            self._set_dirty()

    ##############################################

    @Slot()
    def update_from_isbn(self):

        # Fixme: run in a thread ???
        self._metadata.update_from_isbn()

        self.authors_changed.emit()
        self.language_changed.emit()
        self.publisher_changed.emit()
        self.title_changed.emit()
        self.year_changed.emit()
        self._set_dirty()

    ##############################################

    @Slot()
    def save(self):
        self._book.save_metadata()
        self._set_dirty(False)

####################################################################################################

class QmlBookPage(QObject):

    _logger = _module_logger.getChild('QmlBookPage')

    ##############################################

    def __init__(self, qml_book, book_page):

        super().__init__()

        self._qml_book = qml_book
        self._page = book_page

        self._text = None
        self._ocr_running = False
        self.text_ready.connect(self._ocr_cleanup)

    ##############################################

    def __repr__(self):
        return '{0} {1}'.format(self.__class__.__name__, self._page)

    ##############################################

    @property
    def page(self):
        return self._page

    ##############################################

    @Property(bool, constant=True)
    def is_empty(self):
        return self._page.is_empty

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

    thumbnail_ready = Signal()

    @Slot()
    def request_large_thumbnail(self):

        def job():
            # Fixme: issue when the application is closed
            return str(thumbnail_cache[self._page.path].large)

        worker = Worker(job)
        worker.signals.finished.connect(self.thumbnail_ready)
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

    @Slot()
    def flip_page(self):
        self._page.flip()
        self.orientation_changed.emit()
        self._qml_book.pages_changed.emit()

    ##############################################

    text_ready = Signal()

    @Property(str, constant=True)
    def text(self):

        if not self._ocr_running and self._text is None:
            metadata = self._page.book.metadata
            language = metadata.language or None

            def job():
                # Set fake to debug and receive a large lorem ipsum
                text = self._page.to_text(language, fake=False)
                # use result signal ???
                self._text = text
                # return text

            worker = Worker(job)
            worker.signals.finished.connect(self.text_ready)
            self._ocr_running = True
            from .QmlApplication import Application
            Application.instance.thread_pool.start(worker)

        return self._text

    def _ocr_cleanup(self):
        self._ocr_running = False

    ##############################################

    @Slot(QUrl)
    def save_text(self, url):
        path = url.toString(QUrl.RemoveScheme)
        try:
            with open(path, 'w') as fh:
                fh.write(self.text)
            self._logger.info('Save text page in {}'.format(path))
        except:
            application = QCoreApplication.instance()
            qml_application = application.qml_main
            tr_str = QCoreApplication.translate('QmlBookPage', 'Could not save file {}')
            qml_application.notify_message(tr_str.format(path))

    ##############################################

    @Slot(str)
    def open_in_external_program(self, program):
        command = (program, self.path)
        self._logger.info(' '.join(command))
        process = subprocess.Popen(command)

####################################################################################################

class QmlBook(QObject):

    new_page = Signal(int)

    _logger = _module_logger.getChild('QmlBook')

    ##############################################

    def __init__(self, path):

        super().__init__()

        self._book = Book(path)
        self._book.fix_empty_pages()

        self._metadata = QmlBookMetadata(self._book)

        # We must prevent garbage collection
        self._pages = [QmlBookPage(self, page) for page in self._book]

    ##############################################

    @Property(str, constant=True)
    def path(self):
        return str(self._book.path)

    ##############################################

    @Property(QmlBookMetadata, constant=True)
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
        qml_page.orientation_changed.emit()
        self.pages_changed.emit()

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

        self._pages.append(QmlBookPage(self, page))
        self.number_of_pages_changed.emit()
        self.new_page.emit(page.page_number)

        # except Exception as exception:
        #     self._logger.warning('Error on {}\n{}'.format(filename, exception))

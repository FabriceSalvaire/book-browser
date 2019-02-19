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
    'ScannerImageProvider',
    'QmlScanner',
    'QmlScannerConfig',
]

####################################################################################################

from datetime import datetime
from pathlib import Path
import json
import logging
import os
import uuid

from PyQt5.QtGui import QPixmap
from PyQt5.QtQuick import QQuickImageProvider
from QtShim.QtCore import (
    Property, Signal, Slot, QObject,
    Qt, QTimer, QUrl
)

from PIL import ImageQt, Image

from BookBrowser.Scanner import Scanner, FakeScanner, FileExistsError, PathError
from .Runnable import Worker

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class ScannerImageProvider(QQuickImageProvider):

    _logger = _module_logger.getChild('ScannerImageProvider')

    ##############################################

    def __init__(self):

        super().__init__(QQuickImageProvider.Image) # Pixmap

        self._output = None

    ##############################################

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, image):
        self._output = ImageQt.ImageQt(image)

    ##############################################

    def requestImage(self, image_id, size):
        self._logger.info('{} {}'.format(image_id, size))
        return self._output, self._output.size()

    ##############################################

    def requestPixmap(self, image_id, size):
        self._logger.info('{} {}'.format(image_id, size))
        pixmap = QPixmap(self._output.size())
        pixmap.convertFromImage(self._output)
        return pixmap, pixmap.size()

####################################################################################################

class QmlScannerConfig(QObject):

    # Note: look commit 3fc86cf "Implemented QmlScannerConfig" for the past and simpler
    #       implementation

    maximized = Signal()

    __json_filename__ = '.book_browser.json'

    __json_keys__ = (
        'path',
        'filename_pattern',
        'index',
        'resolution',
        'mode',
        'area',
        'is_maximized',
        'number_of_pages',
    )

    __default_area__ = dict(x_inf=0, x_sup=0, y_inf=0, y_sup=0)

    _logger = _module_logger.getChild('QmlScannerConfig')

    ##############################################

    def __init__(self):

        super().__init__()

        self._path = ''
        self._filename_pattern = ''
        self._index = 0

        self._resolution = 0
        self._mode = ''
        self._area = self.__default_area__
        self._is_maximized = False

        self._number_of_pages = 0

    ##############################################

    path_changed = Signal()

    @Property(str, notify=path_changed)
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        value = str(value)
        if self._path != value:
            self._path = value
            self._logger.info('path = {}'.format(self._path))
            self.path_changed.emit()

    ##############################################

    filename_pattern_changed = Signal()

    @Property(str, notify=filename_pattern_changed)
    def filename_pattern(self):
        return self._filename_pattern

    @filename_pattern.setter
    def filename_pattern(self, value):
        value = str(value)
        if self._filename_pattern != value:
            self._filename_pattern = value
            self._logger.info('filename_pattern = {}'.format(self._filename_pattern))
            self.filename_pattern_changed.emit()

    ##############################################

    index_changed = Signal()

    @Property(int, notify=index_changed)
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        value = int(value)
        if self._index != value:
            self._index = value
            self._logger.info('index = {}'.format(self._index))
            self.index_changed.emit()

    ##############################################

    resolution_changed = Signal()

    @Property(int, notify=resolution_changed)
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, value):
        value = int(value)
        if self._resolution != value:
            self._resolution = value
            self._logger.info('resolution = {}'.format(self._resolution))
            self.resolution_changed.emit()

    ##############################################

    mode_changed = Signal()

    @Property(str, notify=mode_changed)
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        value = str(value)
        if self._mode != value:
            self._mode = value
            self._logger.info('mode = {}'.format(self._mode))
            self.mode_changed.emit()

    ##############################################

    area_changed = Signal()

    # Could use
    # @Slot('QVariantList')
    @Property('QVariantMap', notify=area_changed)
    def area(self):
        return self._area

    @area.setter
    def area(self, value):
        value = dict(value)
        if self._area != value:
            self._area = {key:value[key] for key in ('x_inf', 'x_sup', 'y_inf', 'y_sup')}
            self.is_maximized = False
            self._logger.info('area = {}'.format(self._area))
            self.area_changed.emit()

    ##############################################

    is_maximized_changed = Signal()

    @Property(bool, notify=is_maximized_changed)
    def is_maximized(self):
        return self._is_maximized

    @is_maximized.setter
    def is_maximized(self, value):
        value = bool(value)
        if self._is_maximized != value:
            self._is_maximized = value
            self._logger.info('is_maximized = {}'.format(self._is_maximized))
            self.is_maximized_changed.emit()
            if value:
                self.area = self.__default_area__
                self.maximized.emit()

    ##############################################

    number_of_pages_changed = Signal()

    @Property(int, notify=number_of_pages_changed)
    def number_of_pages(self):
        return self._number_of_pages

    @number_of_pages.setter
    def number_of_pages(self, value):
        value = int(value)
        if self._number_of_pages != value:
            self._number_of_pages = value
            self._logger.info('number_of_pages = {}'.format(self._number_of_pages))
            self.number_of_pages_changed.emit()

    ##############################################

    def _json_path(self):
        return Path(self._path).joinpath(self.__json_filename__)

    @property
    def json_path(self):
        return self._json_path()

    ##############################################

    @Slot()
    def save(self):

        data = {key:getattr(self, '_' + key) for key in self.__json_keys__}
        self._logger.info('Save scanner config {} {}'.format(self.json_path, data))
        json_data = json.dumps(data, sort_keys=True, indent=4)
        with open(self.json_path, 'w') as fh:
            fh.write(json_data)

    ##############################################

    @Slot(result=bool)
    def load(self):

        if self._json_path().exists():
            with open(self.json_path, 'r') as fh:
                data = json.loads(fh.read())

            # In case book was moved !!!
            saved_path = data['path']
            del data['path']

            self._logger.info('Loads scanner config {} {}'.format(self.json_path, data))
            for key, value in data.items():
                setattr(self, key, value)

            return True
        else:
            return False

####################################################################################################

class QmlScanner(QObject):

    # Fixme: these signals are issues with QML code
    # scanner_ready = Signal()
    preview_done = Signal(str)
    file_exists_error = Signal(str)
    path_error = Signal(str)
    scan_done = Signal(str)

    _logger = _module_logger.getChild('QmlScanner')

    ##############################################

    def __init__(self, fake=False):

        super().__init__()

        if fake:
            self._scanner = FakeScanner()
        else:
            self._scanner = Scanner()
        # self.scanner_ready.emit()

        self._config = QmlScannerConfig()

        # Fixme: thread issue ???
        #
        #   Signal is not received when a property is set from QML
        #   https://doc.qt.io/qt-5/threads-qobject.html#signals-and-slots-across-threads
        #
        #   Auto Connection (default)
        #       If the signal is emitted in the thread which the receiving object has affinity then
        #       the behavior is the same as the Direct Connection. Otherwise, the behavior is the
        #       same as the Queued Connection."
        #
        #   Direct Connection
        #       The slot is invoked immediately, when the signal is emitted. The slot is executed in
        #       the emitter's thread, which is not necessarily the receiver's thread.

        self._config.resolution_changed.connect(self._set_resolution, type=Qt.DirectConnection)
        self._config.mode_changed.connect(self._set_mode, type=Qt.DirectConnection)
        self._config.area_changed.connect(self._set_area, type=Qt.DirectConnection)
        self._config.maximized.connect(self._maximize_scan_area, type=Qt.DirectConnection)

        self._config.resolution = 200
        self._config.mode = 'Color'
        # self._config.filename_pattern = 'foo.{:03}.png'
        # self._config.mode = self._scanner.mode
        # self._config.resolution = self._scanner.resolution

        self._start_time = None
        self._page_count = 0
        self.start_timer()

    ##############################################

    def __bool__(self):
        return bool(self._scanner)

    ##############################################

    @Property(bool, constant=True)
    def has_device(self):
        return bool(self._scanner)

    @Property(str, constant=True)
    def device(self):
        return self._scanner.device_name

    ##############################################

    @Property(QmlScannerConfig, constant=True)
    def config(self):
        return self._config

    ##############################################

    @Property('QStringList', constant=True)
    def resolutions(self):
        return [str(x) for x in self._scanner.resolution_constraint]

    @Property('QStringList', constant=True)
    def modes(self):
        return self._scanner.mode_constraint

    @Property(int, constant=True)
    def area_x_sup(self):
        return self._scanner.area_constraint_x_sup

    @Property(int, constant=True)
    def area_y_sup(self):
        return self._scanner.area_constraint_y_sup

    ##############################################

    def _set_resolution(self):
        self._logger.info('Set scanner resolution: {}'.format(self._config.resolution))
        self._scanner.resolution = self._config.resolution

    ##############################################

    def _set_mode(self):
        self._logger.info('Set scanner mode: {}'.format(self._config.mode))
        self._scanner.mode = self._config.mode

    ##############################################

    def _maximize_scan_area(self):
        self._scanner.maximize_scan_area()

    def _set_area(self):
        self._scanner.set_area_as_scale(**self._config.area)

    ##############################################

    @Property(str, constant=True)
    def working_directory(self):
        # return os.getcwd()
        from .QmlApplication import Application
        return str(Application.instance.book.path)

    ##############################################

    @Slot()
    def scan_image(self):

        self._logger.info('')

        from .QmlApplication import Application

        def job():
            # self._scanner.maximize_scan_area() # Fixme: here ok ???
            image = self._scanner.scan_image()
            Application.instance.scanner_image_provider.output = image
            return str(uuid.uuid1())

        worker = Worker(job)
        worker.signals.result.connect(self.preview_done)
        # worker.signals.finished.connect()
        # worker.signals.progress.connect()

        from .QmlApplication import Application
        Application.instance.thread_pool.start(worker)

    ##############################################

    @Slot(bool)
    def scan(self, overwrite):

        filename_path = self._config.path
        filename_pattern = self._config.filename_pattern
        index = self._config.index

        self._logger.info('')

        def job():
            try:
                path_pattern = str(Path(filename_path).joinpath(filename_pattern))
                # Fixme: int required ???
                path = self._scanner.scan(path_pattern, overwrite=bool(overwrite), index=int(index))
                return str(path)
            except FileExistsError as exception:
                path = exception.args[0]
                self.file_exists_error.emit(path)
            except PathError as exception:
                path = exception.args[0]
                self.path_error.emit(path)
            return '' # error

        worker = Worker(job)
        # worker.signals.progress.connect()
        # worker.signals.error.connect()
        worker.signals.result.connect(self.scan_done)
        # worker.signals.finished.connect()

        from .QmlApplication import Application
        Application.instance.thread_pool.start(worker)

        self._page_count += 1 # Fixme: count rescan

    ##############################################

    @Slot()
    def start_timer(self):
        self._start_time = datetime.now()
        self._page_count = 0

    @Slot(int, int, result=str)
    def end_time(self, number_of_pages_done, number_of_pages):

        self._logger.info('{} / {}'.format(number_of_pages_done, number_of_pages))

        if self._page_count < 4:
            return 'estimation in {} pages'.format(4 - self._page_count +1)

        now = datetime.now()
        delta_time = now - self._start_time
        page_count = self._page_count
        speed = delta_time / self._page_count
        self._logger.info('Scan speed {}'.format(speed))
        end_time = now + speed * (number_of_pages - number_of_pages_done)

        achieved = int(100 * number_of_pages_done / number_of_pages)

        number_of_seconds = (end_time - now).total_seconds()
        hours, remainder = divmod(number_of_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        remaining_time = '{:02}:{:02}'.format(int(hours), int(minutes))

        time_format = '%H:%M'
        return '{}   ( {} )   @{} %'.format(
            end_time.strftime(time_format),
            remaining_time,
            achieved
        )

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
]

####################################################################################################

from pathlib import Path
import logging
import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtQuick import QQuickImageProvider
from QtShim.QtCore import (
    Property, Signal, Slot, QObject,
    Qt, QTimer, QUrl
)

from PIL import ImageQt, Image

from BookBrowser.Scanner import Scanner, FileExistsError
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
        self.output = Image.open('/home/fabrice/book-browser/foo.png')

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

class QmlScanner(QObject):

    # scanner_ready = Signal()
    preview_done = Signal(str)
    file_exists_error = Signal(str)
    scan_done = Signal(str)

    _logger = _module_logger.getChild('QmlScanner')

    ##############################################

    def __init__(self):

        super().__init__()

        self._scanner = Scanner()
        #self.scanner_ready.emit()

    ##############################################

    def __bool__(self):
        return bool(self._scanner)

    ##############################################

    @Property(bool, constant=True)
    def has_device(self):
        return bool(self._scanner)

    @Property(str, constant=True)
    def device(self):
        if self:
            return self._scanner.device_name
        else:
            return 'Any device'

    ##############################################

    @Slot()
    def maximize_scan_area(self):
        if self: # for debug
            self._scanner.maximize_scan_area()

    ##############################################

    resolution_changed = Signal()

    @Property(int, notify=resolution_changed)
    def resolution(self):
        if self: # for debug
            return self._scanner.resolution
        else:
            return 0

    @Property('QStringList', constant=True)
    def resolutions(self):
        if self: # for debug
            return [str(x) for x in self._scanner.resolution_constraint]
        else:
            return []

    @resolution.setter
    def resolution(self, value):
        self._logger.info('Set scanner resolution: {}'.format(value))
        if self: # for debug
            self._scanner.resolution = int(value)

    ##############################################

    mode_changed = Signal()

    @Property(str, notify=mode_changed)
    def mode(self):
        if self: # for debug
            return self._scanner.mode
        else:
            return 'None'

    @Property('QStringList', constant=True)
    def modes(self):
        if self: # for debug
            return self._scanner.mode_constraint
        else:
            return []

    @mode.setter
    def mode(self, value):
        self._logger.info('Set scanner resolution: {}'.format(value))
        if self: # for debug
            self._scanner.mode = str(value)

    ##############################################

    area_changed = Signal()

    @Property(str, notify=area_changed)
    def area(self):
        if self: # for debug
            return self._scanner.area
        else:
            return 0

    @Property('QStringList', constant=True)
    def area_constraint(self):
        return self._scanner.area_constraint

    @area.setter
    def area(self, value):
        if self: # for debug
            x_inf, x_sup, y_inf, y_sup = [float(x)/10000 for x in value.split(',')]
            # Fixme:
            print(x_inf, x_sup, y_inf, y_sup)
            print(self._scanner.area_constraint)
            # 0 0 667.8135955536554 921
            # [(0, 14149222, 0), (0, 14149222, 0), (0, 19475988, 0), (0, 19475988, 0)]
            constraint = self._scanner.area_constraint
            scanner_width = constraint[0][1]
            scanner_height = constraint[2][1]
            area = [int(x) for x in (
                x_inf*scanner_width,  x_sup*scanner_width,
                y_inf*scanner_height, y_sup*scanner_height,
            )
            ]
            print(area)
            self._scanner.area = area

    ##############################################

    @Property(str, constant=True)
    def working_directory(self):
        # return os.getcwd()
        from .QmlApplication import Application
        return str(Application.instance.book.path)

    ##############################################

    def _fake_scan(self, *args, **kwargs):

        self._logger.info('Fake scan {} {}'.format(args, kwargs))
        # self.file_exists_error.emit('foo.png')
        # self.preview_done.emit('foo.png')
        self.scan_done.emit('/home/fabrice/book-browser/foo.png')

    ##############################################

    @Slot()
    def scan_image(self):

        self._logger.info('')

        if not self: # for debug
            return self._fake_scan()

        from .QmlApplication import Application

        def job():
            # self._scanner.maximize_scan_area() # Fixme: here ok ???
            image = self._scanner.scan_image()
            Application.instance.scanner_image_provider.output = image
            return 'foo.png' # Fixme:

        worker = Worker(job)
        worker.signals.result.connect(self.preview_done)
        # worker.signals.finished.connect()
        # worker.signals.progress.connect()

        from .QmlApplication import Application
        Application.instance.thread_pool.start(worker)

    ##############################################

    @Slot(str, str, bool, int)
    def scan(self, filename_path, filename_pattern, overwrite, index):

        self._logger.info('')

        if not self:
            return self._fake_scan(filename_path, filename_pattern, overwrite, index)

        def job():
            try:
                path_pattern = str(Path(filename_path).joinpath(filename_pattern))
                # Fixme: int required ???
                path = self._scanner.scan(path_pattern, overwrite=bool(overwrite), index=int(index))
                return str(path)
            except FileExistsError as exception:
                path = exception.args[0]
                self.file_exists_error.emit(path)
                return ''

        worker = Worker(job)
        # worker.signals.progress.connect()
        # worker.signals.error.connect()
        worker.signals.result.connect(self.scan_done)
        # worker.signals.finished.connect()

        from .QmlApplication import Application
        Application.instance.thread_pool.start(worker)

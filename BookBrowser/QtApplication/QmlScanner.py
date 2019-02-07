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

from BookBrowser.Scanner import Scanner, FakeScanner, FileExistsError
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

class QmlScanner(QObject):

    # scanner_ready = Signal()
    preview_done = Signal(str)
    file_exists_error = Signal(str)
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

    @Slot()
    def maximize_scan_area(self):
        self._scanner.maximize_scan_area()

    ##############################################

    resolution_changed = Signal()

    @Property(int, notify=resolution_changed)
    def resolution(self):
        return self._scanner.resolution

    @Property('QStringList', constant=True)
    def resolutions(self):
        return [str(x) for x in self._scanner.resolution_constraint]

    @resolution.setter
    def resolution(self, value):
        self._logger.info('Set scanner resolution: {}'.format(value))
        self._scanner.resolution = int(value)

    ##############################################

    mode_changed = Signal()

    @Property(str, notify=mode_changed)
    def mode(self):
        return self._scanner.mode

    @Property('QStringList', constant=True)
    def modes(self):
        return self._scanner.mode_constraint

    @mode.setter
    def mode(self, value):
        self._logger.info('Set scanner resolution: {}'.format(value))
        self._scanner.mode = str(value)

    ##############################################

    # area_changed = Signal()

    # @Property(str, notify=area_changed)
    # def area(self):
    #     if self: # for debug
    #         return self._scanner.area
    #     else:
    #         return 0

    # @Property('QStringList', constant=True)
    # def area_constraint(self):
    #     return self._scanner.area_constraint

    @Property(int, constant=True)
    def area_x_sup(self):
        return self._scanner.area_constraint_x_sup

    @Property(int, constant=True)
    def area_y_sup(self):
        return self._scanner.area_constraint_y_sup

    # @area.setter
    # def area(self, value):
    #     pass

    @Slot(float, float, float, float)
    def set_area(self, x_inf, x_sup, y_inf, y_sup):
        self._scanner.set_area_as_scale(x_inf, x_sup, y_inf, y_sup)

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

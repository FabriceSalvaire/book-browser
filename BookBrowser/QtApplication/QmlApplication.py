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

"""Module to implement a Qt Application.

"""

####################################################################################################

__all__ = [
    'QmlApplication',
]

####################################################################################################

import argparse
# import datetime
import logging
import sys
import traceback
from pathlib import Path

# Fixme:
from PyQt5 import QtCore

from QtShim.QtCore import (
    Property, Signal, Slot, QObject,
    Qt, QTimer, QUrl
)
from QtShim.QtGui import QGuiApplication, QIcon
from QtShim.QtQml import qmlRegisterType, QQmlApplicationEngine
# Fixme: PYSIDE-574 qmlRegisterSingletonType and qmlRegisterUncreatableType missing in QtQml
from QtShim.QtQml import qmlRegisterUncreatableType
from QtShim.QtQuick import QQuickPaintedItem, QQuickView
# from QtShim.QtQuickControls2 import QQuickStyle

from BookBrowser.Common.ArgparseAction import PathAction
from BookBrowser.Common.Platform import QtPlatform
from .QmlBook import QmlBook, QmlBookPage
from .QmlScanner import ScannerImageProvider, QmlScanner
from .Runnable import Worker

from .rcc import BookBrowserRessource

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class QmlApplication(QObject):

    """Class to implement a Qt QML Application."""

    scanner_ready = Signal()

    preview_done = Signal(str)
    file_exists_error = Signal(str)
    scan_done = Signal(str)

    _logger = _module_logger.getChild('QmlApplication')

    ##############################################

    def __init__(self, application):

        super().__init__()

        self._application = application

    ##############################################

    book_changed = Signal()

    @Property(QmlBook, notify=book_changed)
    def book(self):
        return self._application.book

    ##############################################

    @Slot(str)
    def load_book(self, path):
        self._application.load_book(path)
        self.book_changed.emit()

    ##############################################

    @Slot()
    def init_scanner(self):

        def job():
            self._application.init_scanner()
            return '' # Fixme:

        worker = Worker(job)
        # worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.scanner_ready)
        # worker.signals.progress.connect(self.progress_fn)

        Application.instance.thread_pool.start(worker)

    ##############################################

    @Property(QmlScanner, constant=True)
    def scanner(self):
        return self._application.scanner

    ##############################################

    @Slot()
    def debug(self):

        # self._application.scanner.scan_done.connect(self._on_scan_done)

        self._application.scanner.preview_done.connect(self.preview_done)
        self._application.scanner.file_exists_error.connect(self.file_exists_error)
        self._application.scanner.scan_done.connect(self.scan_done)

    ##############################################

    def _on_scan_done(self, path):
        self._logger.info(path)
        self.scan_done.emit(path)

####################################################################################################

class Application(QObject):

    """Class to implement a Qt Application."""

    instance = None

    _logger = _module_logger.getChild('Application')

    scanner_ready = Signal()

    ##############################################

    # Fixme: Singleton

    @classmethod
    def create(cls, *args, **kwargs):

        if cls.instance is not None:
            raise NameError('Instance exists')

        cls.instance = cls(*args, **kwargs)
        return cls.instance

    ##############################################

    def __init__(self):

        super().__init__()

        QtCore.qInstallMessageHandler(self._message_handler)

        self._parse_arguments()

        self._book = None
        # Fixme: must be defined before QML
        self.load_book(self._args.book_path)

        self._appplication = QGuiApplication(sys.argv)
        self._engine = QQmlApplicationEngine()
        self._qml_application = QmlApplication(self)

        logo_path = ':/icons/logo-256.png'
        self._appplication.setWindowIcon(QIcon(logo_path))

        self._platform = QtPlatform()
        # self._logger.info('\n' + str(self._platform))

        # self._load_translation()
        self._register_qml_types()
        self._set_context_properties()
        self._load_qml_main()

        # self._run_before_event_loop()

        self._thread_pool = QtCore.QThreadPool()
        self._logger.info("Multithreading with maximum {} threads".format(self._thread_pool.maxThreadCount()))

        self._scanner = None
        self._scanner_image_provider = ScannerImageProvider()
        self._engine.addImageProvider('scanner_image',  self._scanner_image_provider)

        QTimer.singleShot(0, self._post_init)

        # self._view = QQuickView()
        # self._view.setResizeMode(QQuickView.SizeRootObjectToView)
        # self._view.setSource(qml_url)

    ##############################################

    @property
    def args(self):
        return self._args

    @property
    def platform(self):
        return self._platform

    @property
    def qml_application(self):
        return self._qml_application

    @property
    def thread_pool(self):
        return self._thread_pool

    @property
    def scanner_image_provider(self):
        return self._scanner_image_provider

    @property
    def scanner(self):
        return self.init_scanner()

    @property
    def book(self):
        return self._book

    @property
    def book_path(self):
        return self._book.path

    ##############################################

    def _print_critical_message(self, message):
        # print('\nCritical Error on {}'.format(datetime.datetime.now()))
        # print('-'*80)
        # print(message)
        self._logger.critical(message)

    ##############################################

    def _message_handler(self, msg_type, context, msg):

        if msg_type == QtCore.QtDebugMsg:
            method = self._logger.debug
        elif msg_type == QtCore.QtInfoMsg:
            method = self._logger.info
        elif msg_type == QtCore.QtWarningMsg:
            method = self._logger.warning
        elif msg_type in (QtCore.QtCriticalMsg, QtCore.QtFatalMsg):
            method = self._logger.critical
            # method = None

        # local_msg = msg.toLocal8Bit()
        # localMsg.constData()
        context_file = context.file
        if context_file is not None:
            file_path = Path(context_file).name
        else:
            file_path = ''
        message = '{1} {3} — {0}'.format(msg, file_path, context.line, context.function)
        if method is not None:
            method(message)
        else:
            self._print_critical_message(message)

    ##############################################

    def _on_critical_exception(self, exception):
        message = str(exception) + '\n' + traceback.format_exc()
        self._print_critical_message(message)
        sys.exit(1)

    ##############################################

    @classmethod
    def setup_gui_application(cls):

        # QGuiApplication.setApplicationName(APPLICATION_NAME)
        # QGuiApplication.setOrganizationName(ORGANISATION_NAME)
        QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

        # QQuickStyle.setStyle('Material')

    ##############################################

    def _parse_arguments(self):

        parser = argparse.ArgumentParser(
            description='BookBrowser',
        )

        # parser.add_argument(
        #     '--version',
        #     action='store_true', default=False,
        #     help="show version and exit",
        # )

        parser.add_argument(
            'book_path', metavar='BookPath',
            action=PathAction,
            help='Book path',
        )

        parser.add_argument(
            '--watcher',
            action='store_true',
            default=False,
            help='start watcher',
        )

        parser.add_argument(
            '--user-script',
            action=PathAction,
            default=None,
            help='user script to execute',
        )

        parser.add_argument(
            '--user-script-args',
            default='',
            help="user script args (don't forget to quote)",
        )

        self._args = parser.parse_args()

    ##############################################

    # def _load_translationt(self):

    #     locale = QLocale()

    #     if m_translator.load(locale, '...', '.', ':/translations', '.qm'):
    #         m_application.installTranslator(m_translator)
    #     else:
    #         raise "No translator for locale" locale.name()

    ##############################################

    def _register_qml_types(self):

        qmlRegisterUncreatableType(QmlApplication, 'BookBrowser', 1, 0, 'QmlApplication', 'Cannot create QmlApplication')
        qmlRegisterUncreatableType(QmlBook, 'BookBrowser', 1, 0, 'QmlBook', 'Cannot create QmlBook')
        qmlRegisterUncreatableType(QmlBookPage, 'BookBrowser', 1, 0, 'QmlBookPage', 'Cannot create QmlBookPage')
        qmlRegisterUncreatableType(QmlScanner, 'BookBrowser', 1, 0, 'QmlScanner', 'Cannot create QmlScanner')

    ##############################################

    def _set_context_properties(self):
        context = self._engine.rootContext()
        context.setContextProperty('application', self._qml_application)

    ##############################################

    def _load_qml_main(self):

        qml_path = Path(__file__).parent.joinpath('qml')
        # qml_path = 'qrc:///qml'
        self._engine.addImportPath(str(qml_path))

        main_qml_path = qml_path.joinpath('main.qml')
        self._qml_url = QUrl.fromLocalFile(str(main_qml_path))
        # QUrl('qrc:/qml/main.qml')
        self._engine.objectCreated.connect(self._check_qml_is_loaded)
        self._engine.load(self._qml_url)

    ##############################################

    def _check_qml_is_loaded(self, obj, url):
        # See https://bugreports.qt.io/browse/QTBUG-39469
        if (obj is None and url == self._qml_url):
            sys.exit(-1)

    ##############################################

    def exec_(self):
        # self._view.show()
        sys.exit(self._appplication.exec_())

    ##############################################

    def _post_init(self):

        # Fixme: ui refresh ???
        self._logger.info('post init')

        if self._args.watcher:
            self._logger.info('Start watcher')
            self._book.start_watcher() # QtCore.QFileSystemWatcher(self)

        if self._args.user_script is not None:
            self.execute_user_script(self._args.user_script)

    ##############################################

    def execute_user_script(self, script_path):

        """Execute an user script provided by file *script_path* in a context where is defined a
        variable *application* that is a reference to the application instance.

        """

        script_path = Path(script_path).absolute()
        self._logger.info('Execute user script:\n  {}'.format(script_path))
        try:
            source = open(script_path).read()
        except FileNotFoundError:
            self._logger.info('File {} not found'.format(script_path))
            sys.exit(1)
        try:
            bytecode = compile(source, script_path, 'exec')
        except SyntaxError as exception:
            self._on_critical_exception(exception)
        try:
            exec(bytecode, {'application':self})
        except Exception as exception:
            self._on_critical_exception(exception)
        self._logger.info('User script done')

    ##############################################

    def init_scanner(self):

        if self._scanner is None:
            # take time
            self._scanner = QmlScanner()
            self.scanner_ready.emit()
        return self._scanner

    ##############################################

    def load_book(self, path):
        self._book = QmlBook(path)

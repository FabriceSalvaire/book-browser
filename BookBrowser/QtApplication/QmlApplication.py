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

"""Module to implement a Qt Application.

"""

####################################################################################################

__all__ = [
    'QmlApplication',
]

####################################################################################################

# import datetime
from pathlib import Path
import argparse
import logging
import sys
import traceback

# Fixme:
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

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

from BookBrowser.Book import BookLibrary
from BookBrowser.Common.ArgparseAction import PathAction
from BookBrowser.Common.Platform import QtPlatform
from .ApplicationMetadata import ApplicationMetadata
from .ApplicationSettings import ApplicationSettings, Shortcut
from .KeySequenceEditor import KeySequenceEditor
from .QmlBook import QmlBook, QmlBookPage, QmlBookMetadata
from .QmlBookLibrary import QmlBookCover, QmlBookLibrary
from .QmlScanner import ScannerImageProvider, QmlScanner, QmlScannerConfig
from .Runnable import Worker

from .rcc import BookBrowserRessource

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class QmlApplication(QObject):

    """Class to implement a Qt QML Application."""

    show_message = Signal(str) # message
    show_error = Signal(str, str) # message backtrace

    scanner_ready = Signal()

    # Fixme: !!!
    preview_done = Signal(str)
    file_exists_error = Signal(str)
    path_error = Signal(str)
    scan_done = Signal(str)

    _logger = _module_logger.getChild('QmlApplication')

    ##############################################

    def __init__(self, application):

        super().__init__()

        self._application = application

    ##############################################

    def notify_message(self ,message):
        self.show_message.emit(str(message))

    def notify_error(self, message):
        backtrace_str = traceback.format_exc()
        self.show_error.emit(str(message), backtrace_str)

    ##############################################

    @Property(str, constant=True)
    def application_name(self):
        return ApplicationMetadata.name

    @Property(str, constant=True)
    def application_url(self):
        return ApplicationMetadata.url

    @Property(str, constant=True)
    def about_message(self):
        return ApplicationMetadata.about_message()

    ##############################################

    library_changed = Signal()

    @Property(QmlBookLibrary, notify=library_changed)
    def library(self):
        # return null if None
        return self._application.library

    ##############################################

    @Slot('QUrl')
    def load_library(self, url):
        path = url.toString(QUrl.RemoveScheme)
        self._application.load_library(path)
        self.library_changed.emit()

    ##############################################

    book_changed = Signal()

    @Property(QmlBook, notify=book_changed)
    def book(self):
        # return null if None
        return self._application.book

    ##############################################

    @Slot('QUrl')
    def load_book(self, url):
        path = url.toString(QUrl.RemoveScheme)
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

        self._application.scanner.preview_done.connect(self.preview_done)
        self._application.scanner.file_exists_error.connect(self.file_exists_error)
        self._application.scanner.path_error.connect(self.path_error)
        self._application.scanner.scan_done.connect(self._on_scan_done)
        # self._application.scanner.scan_done.connect(self.scan_done)

    ##############################################

    def _on_scan_done(self, path):

        # Fixme: not received
        # 13:00,363 - BookBrowser.QtApplication.QmlApplication.Application._message_handler - INFO - ScannerUI.qml on_scanner_ready — Scanner config loaded true
        # 13:01,110 - BookBrowser.QtApplication.QmlScanner.QmlScanner.scan - INFO - 
        # 13:01,111 - BookBrowser.QtApplication.Runnable.Worker.run - INFO - run <function QmlScanner.scan.<locals>.job at 0x7f4962611e18>((), {})
        # 13:01,111 - BookBrowser.Scanner.FakeScanner.scan - INFO - Scan /home/fabrice/home/developpement/python/book-browser/test-directory/afoo.{:03}.png 93
        #             overwrite = False
        # 13:01,112 - BookBrowser.Scanner.FakeScanner.scan_image - INFO - Start scanning ...
        # 13:01,112 - BookBrowser.Scanner.FakeScanner.scan_image - INFO - Start done
        # 13:01,150 - BookBrowser.Scanner.FakeScanner.scan - INFO - Saved /home/fabrice/home/developpement/python/book-browser/test-directory/afoo.093.png
        # 13:01,151 - BookBrowser.QtApplication.Runnable.Worker.run - INFO - emit result /home/fabrice/home/developpement/python/book-browser/test-directory/afoo.093.png
        # 13:01,151 - BookBrowser.QtApplication.Runnable.Worker.run - INFO - emit finished

        self._logger.info(path)
        self.scan_done.emit(path)

####################################################################################################

# Fixme: why not derive from QGuiApplication ???
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

        self._logger.info('Ctor')

        super().__init__()

        QtCore.qInstallMessageHandler(self._message_handler)

        self._parse_arguments()

        self._library = None
        self._book = None
        # Fixme: must be defined before QML
        if BookLibrary.is_library(self._args.path):
            self.load_library(self._args.path)
        else:
            self.load_book(self._args.path)

        # For Qt Labs Platform native widgets
        # self._application = QGuiApplication(sys.argv)
        # use QCoreApplication::instance() to get instance
        self._application = QApplication(sys.argv)
        self._application.main = self
        self._init_application()

        self._engine = QQmlApplicationEngine()
        self._qml_application = QmlApplication(self)
        self._application.qml_main = self._qml_application

        self._platform = QtPlatform()
        # self._logger.info('\n' + str(self._platform))

        self._load_translation()
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
    def settings(self):
        return self._settings

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

    # @property
    # def book_path(self):
    #     return self._book.path

    @property
    def library(self):
        return self._library

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
        self._qml_application.notify_error(exception)
        # sys.exit(1)

    ##############################################

    def _init_application(self):

        self._application.setOrganizationName(ApplicationMetadata.organisation_name)
        self._application.setOrganizationDomain(ApplicationMetadata.organisation_domain)

        self._application.setApplicationName(ApplicationMetadata.name)
        self._application.setApplicationDisplayName(ApplicationMetadata.display_name)
        self._application.setApplicationVersion(ApplicationMetadata.version)

        logo_path = ':/icons/logo/logo-256.png'
        self._application.setWindowIcon(QIcon(logo_path))

        QIcon.setThemeName('material')

        self._settings = ApplicationSettings()

    ##############################################

    @classmethod
    def setup_gui_application(self):

        # https://bugreports.qt.io/browse/QTBUG-55167
        # for path in (
        #         'qt.qpa.xcb.xcberror',
        # ):
        #     QtCore.QLoggingCategory.setFilterRules('{} = false'.format(path))
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

        # Fixme: should be able to start application without !!!
        parser.add_argument(
            'path', metavar='PATH',
            action=PathAction,
            help='book or library path',
        )

        parser.add_argument(
            '--dont-translate',
            action='store_true',
            default=False,
            help="Don't translate application",
        )

        parser.add_argument(
            '--watcher',
            action='store_true',
            default=False,
            help='start watcher',
        )

        parser.add_argument(
            '--fake-scanner',
            action='store_true',
            default=False,
            help='use a fake scanner',
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

    def _load_translation(self):

        if self._args.dont_translate:
            return

        # Fixme: ConfigInstall
        # directory = ':/translations'
        directory = str(Path(__file__).parent.joinpath('rcc', 'translations'))

        locale = QtCore.QLocale()
        self._translator = QtCore.QTranslator()
        if self._translator.load(locale, 'book-browser', '.', directory, '.qm'):
            self._application.installTranslator(self._translator)
        else:
            raise NameError('No translator for locale {}'.format(locale.name()))

    ##############################################

    def _register_qml_types(self):

        qmlRegisterType(KeySequenceEditor, 'BookBrowser', 1, 0, 'KeySequenceEditor')

        qmlRegisterUncreatableType(Shortcut, 'BookBrowser', 1, 0, 'Shortcut', 'Cannot create Shortcut')
        qmlRegisterUncreatableType(ApplicationSettings, 'BookBrowser', 1, 0, 'ApplicationSettings', 'Cannot create ApplicationSettings')
        qmlRegisterUncreatableType(QmlApplication, 'BookBrowser', 1, 0, 'QmlApplication', 'Cannot create QmlApplication')
        qmlRegisterUncreatableType(QmlBookCover, 'BookBrowser', 1, 0, 'QmlBookCover', 'Cannot create QmlBookCover')
        qmlRegisterUncreatableType(QmlBookLibrary, 'BookBrowser', 1, 0, 'QmlBookLibrary', 'Cannot create QmlBookLi')
        qmlRegisterUncreatableType(QmlBook, 'BookBrowser', 1, 0, 'QmlBook', 'Cannot create QmlBook')
        qmlRegisterUncreatableType(QmlBookPage, 'BookBrowser', 1, 0, 'QmlBookPage', 'Cannot create QmlBookPage')
        qmlRegisterUncreatableType(QmlBookMetadata, 'BookBrowser', 1, 0, 'QmlBookMetadata', 'Cannot create QmlBookMetadata')
        qmlRegisterUncreatableType(QmlScannerConfig, 'BookBrowser', 1, 0, 'QmlScannerConfig', 'Cannot create QmlScannerConfig')
        qmlRegisterUncreatableType(QmlScanner, 'BookBrowser', 1, 0, 'QmlScanner', 'Cannot create QmlScanner')

    ##############################################

    def _set_context_properties(self):
        context = self._engine.rootContext()
        context.setContextProperty('application', self._qml_application)
        context.setContextProperty('application_settings', self._settings)

    ##############################################

    def _load_qml_main(self):

        self._logger.info('Load QML...')

        qml_path = Path(__file__).parent.joinpath('qml')
        # qml_path = 'qrc:///qml'
        self._engine.addImportPath(str(qml_path))

        main_qml_path = qml_path.joinpath('main.qml')
        self._qml_url = QUrl.fromLocalFile(str(main_qml_path))
        # QUrl('qrc:/qml/main.qml')
        self._engine.objectCreated.connect(self._check_qml_is_loaded)
        self._engine.load(self._qml_url)

        self._logger.info('QML loaded')

    ##############################################

    def _check_qml_is_loaded(self, obj, url):
        # See https://bugreports.qt.io/browse/QTBUG-39469
        if (obj is None and url == self._qml_url):
            sys.exit(-1)

    ##############################################

    def exec_(self):
        # self._view.show()
        self._logger.info('Start event loop')
        sys.exit(self._application.exec_())

    ##############################################

    def _post_init(self):

        # Fixme: ui refresh ???

        self._logger.info('post Init...')

        if self._args.watcher:
            self._logger.info('Start watcher')
            self._book.start_watcher() # QtCore.QFileSystemWatcher(self)

        if self._args.user_script is not None:
            self.execute_user_script(self._args.user_script)

        self._logger.info('Post Init Done')

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
            self._scanner = QmlScanner(fake=self._args.fake_scanner)
            self.scanner_ready.emit()
        return self._scanner

    ##############################################

    def load_book(self, path):
        self._logger.info('Load book {} ...'.format(path))
        self._book = QmlBook(path)
        self._logger.info('Book loaded')

    ##############################################

    def load_library(self, path):
        self._logger.info('Load library {} ...'.format(path))
        self._library = QmlBookLibrary(path)
        self._logger.info('library loaded')

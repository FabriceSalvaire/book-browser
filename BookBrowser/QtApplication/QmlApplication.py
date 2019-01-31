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
import datetime
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

from BookBrowser.Book import Book
from BookBrowser.Common.Platform import QtPlatform
from BookBrowser.Common.ArgparseAction import PathAction

from .rcc import BookBrowserRessource

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class QmlApplication(QObject):

    """Class to implement a Qt QML Application."""

    _logger = _module_logger.getChild('QmlApplication')

    ##############################################

    def __init__(self, application):

        super().__init__()

        self._application = application

        self._page_number = 1

    ##############################################

    # fooChanged = Signal()

    # @Property(Foo, notify=fooChanged)
    # def foo(self):

    # @foo.setter
    # def foo(self, foo):

    # @Slot(Qxxx, result=str)
    # def foo(self, xxx):

    ##############################################

    @property
    def _book(self):
        return self._application.book

    ##############################################

    @property
    def _page(self):
        return self._book[self._page_number]

    ##############################################

    number_of_pagesChanged = Signal()

    @Property(int, notify=number_of_pagesChanged)
    def number_of_pages(self):
        return len(self._book)

    ##############################################

    page_pathChanged = Signal()

    @Property(str, notify=page_pathChanged)
    def page_path(self):
        if self._page is not None:
            return str(self._page.path)
        else:
            return ''

    ##############################################

    orientationChanged = Signal()

    @Property(int, notify=orientationChanged)
    def orientation(self):
        if self._page is not None:
            return 180 if self._page.orientation == 'v' else 0
        else:
            return 0

    ##############################################

    @Slot(result=int)
    def prev_page(self):
        if self._page_number > 1:
            self._page_number -= 1
            self.page_pathChanged.emit()
        return self._page_number

    ##############################################

    @Slot(result=int)
    def next_page(self):
        if self._page_number < (self.number_of_pages -1):
            self._page_number += 1
            self.page_pathChanged.emit()
        return self._page_number

    ##############################################

    @Slot(int, result=int)
    def to_page(self, page_number):
        if 1 < page_number < (self.number_of_pages -1):
            self._page_number = page_number
            self.page_pathChanged.emit()
        return self._page_number

    ##############################################

    @Slot()
    def flip_page(self):
        # Fixme:_emit ???
        self._page.flip()

####################################################################################################

class Application(QObject):

    """Class to implement a Qt Application."""

    instance = None

    _logger = _module_logger.getChild('Application')

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

        # Fixme: must be defined before QML
        self._book = Book(self._args.book_path)
        self._book.fix_empty_pages()

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

        QTimer.singleShot(0, self._post_init)

        # self._view = QQuickView()
        # self._view.setResizeMode(QQuickView.SizeRootObjectToView)
        # self._view.setSource(qml_url)

    ##############################################

    @property
    def args(self):
        return self._args

    @property
    def qml_application(self):
        return self._qml_application

    @property
    def platform(self):
        return self._platform

    @property
    def book(self):
        return self._book

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
        self._book = None

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
        # qmlRegisterType(QmlApplication, 'BookBrowser', 1, 0, 'QmlApplication')

    ##############################################

    def _set_context_properties(self):
        context = self._engine.rootContext()
        context.setContextProperty('application', self._qml_application)

    ##############################################

    def _load_qml_main(self):

        # self._engine.addImportPath('qrc:///qml')

        qml_path = Path(__file__).parent.joinpath('qml', 'main.qml')
        self._qml_url = QUrl.fromLocalFile(str(qml_path))
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

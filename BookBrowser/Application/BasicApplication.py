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

"""Module to implement a basic application.

"""

####################################################################################################

__all__ = [
    'Application',
]

####################################################################################################

from pathlib import Path
import argparse
import logging
import sys
import traceback

import BookBrowser
from BookBrowser.Common.ArgparseAction import PathAction

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class BasicApplication:

    """Class to implement a basic Application."""

    description = ''

    instance = None

    _logger = _module_logger.getChild('BasicApplication')

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

        self._parse_arguments()

    ##############################################

    @property
    def args(self):
        return self._args

    ##############################################

    def init_arguments(self):

        self._parser.add_argument(
            '--version',
            action='store_true', default=False,
            help="show version and exit",
        )

        self._parser.add_argument(
            '--dry-run',
            action='store_true',
            default=False,
            help='dry run',
        )

        self._parser.add_argument(
            '--user-script',
            action=PathAction,
            default=None,
            help='user script to execute',
        )

        self._parser.add_argument(
            '--user-script-args',
            default='',
            help="user script args (don't forget to quote)",
        )

    ##############################################

    def _parse_arguments(self):

        self._parser = argparse.ArgumentParser(
            description=self.description,
        )
        self.init_arguments()
        self._args = self._parser.parse_args()

    ##############################################

    def _post_init(self):

        self._logger.info('post init')

        if self._args.user_script is not None:
            self.execute_user_script(self._args.user_script)

    ##############################################

    # same as QmlApplication
    def _print_critical_message(self, message):
        # print('\nCritical Error on {}'.format(datetime.datetime.now()))
        # print('-'*80)
        # print(message)
        self._logger.critical(message)

    ##############################################

    # same as QmlApplication
    def _on_critical_exception(self, exception):
        message = str(exception) + '\n' + traceback.format_exc()
        self._print_critical_message(message)
        sys.exit(1)

    ##############################################

    # same as QmlApplication
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

    def run(self):

        if self._args.user_script is not None:
            self.execute_user_script(self._args.user_script)

        if self._args.version:
            print('version', BookBrowser.__version__)
            sys.exit(0)

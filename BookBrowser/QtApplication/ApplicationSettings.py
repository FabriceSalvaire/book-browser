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

"""Module to implement a application settings.

"""

####################################################################################################

__all__ = [
    'ApplicationSettings',
]

####################################################################################################

import logging

# Fixme:
from PyQt5.QtCore import QSettings
from QtShim.QtCore import (
    Property, Signal, Slot,
)

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Shortcuts:

    previous_page = 'Backspace'
    next_page = 'n'
    flip_page = 'r'
    fit_to_screen = 'f'
    full_zoom = 'z'

####################################################################################################

class ApplicationSettings(QSettings):

    """Class to implement application settings."""

    shortcut_changed = Signal(str)

    _logger = _module_logger.getChild('ApplicationSettings')

    ##############################################

    def __init__(self):

        super().__init__()
        self._logger.info('Loading settings from {}'.format(self.fileName()))

    ##############################################

    @Slot(str, result=str)
    def default_shortcut(self, name):
        return getattr(Shortcuts, name)

    ##############################################

    def _shortcut_path(self, name):
        return 'shortcut/{}'.format(name)

    ##############################################

    @Slot(str, result=str)
    def get_shortcut(self, name):
        path = self._shortcut_path(name)
        if self.contains(path):
            return self.value(path)
        else:
            return self.default_shortcut(name)

    ##############################################

    @Slot(str, str)
    def set_shortcut(self, name, value):
        old_value = self.get_shortcut(name)
        if (value != old_value):
            path = self._shortcut_path(name)
            self.setValue(path, value)
            self.shortcut_changed(name)

    ##############################################

    @Property('QStringList', constant=True)
    def shortcuts(self):
        return [name for name in dir(Shortcuts) if not name.startswith('_')]

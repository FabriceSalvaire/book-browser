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

"""Module to implement a scanner interface.

"""

####################################################################################################

__all__ = [
    'Scanner',
]

####################################################################################################

import logging
import pyinsane2

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Scanner:

    """class to implement a scanner interface."""

    __initialised__ = False

    _logger = _module_logger.getChild('Scanner')

    AREA_OPTIONS = ('tl-x', 'br-x', 'tl-y', 'br-y')

    ##############################################

    @classmethod
    def init(cls):
        # take time
        pyinsane2.init()
        cls.__initialised__ = True
        cls._logger.info('Sane is initialised')

    ##############################################

    @classmethod
    def exit(cls):
        if cls.__initialised__:
            pyinsane2.exit()
            cls.__initialised__ = False
            cls._logger.info('Sane exited')

    ##############################################

    @classmethod
    def devices(cls):
        if cls.__initialised__:
            return pyinsane2.get_devices()
        else:
            return []

    ##############################################

    def __init__(self, device_hint='libusb', release=True):

        if not self.__initialised__:
            self.init()

        self._release = bool(release)

        self._device = None
        for device in self.devices():
            if device_hint in str(device):
                self._device = device
                self._logger.info('Sane use {}'.format(device))

    ##############################################

    def __del__(self):
        if self._release:
            self.exit()

    ##############################################

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, name):
        self._device = pyinsane2.Scanner(name=name)

    ##############################################

    def _set_option(self, name, value):
        pyinsane2.set_scanner_opt(self._device, name, [value])

    def _get_option(self, name):
        return self._device.options[name].value

    def _get_option_constraint(self, name):
        return self._device.options[name].constraint

    ##############################################

    def maximize_scan_area(self):
        pyinsane2.maximize_scan_area(self._device)

    ##############################################

    @property
    def resolution(self):
        return self._get_option('resolution')

    @property
    def resolution_constraint(self):
        return self._get_option_constraint('resolution')

    @resolution.setter
    def resolution(self, value):
        self._set_option('resolution', value)

    ##############################################

    @property
    def mode(self):
        return self._get_option('mode')

    @property
    def mode_constraint(self):
        return self._get_option_constraint('mode')

    @mode.setter
    def mode(self, value):
        self._set_option('mode', value)

    ##############################################

    @property
    def area(self):
        return [self._get_option(name) for name in self.AREA_OPTIONS]

    @property
    def area_constraint(self):
        return [self._get_option_constraint(name) for name in self.AREA_OPTIONS]

    @area.setter
    def area(self, x_inf, x_sup, y_inf, y_sup):
        for name, value in zip(self.AREA_OPTIONS, (x_inf, x_sup, y_inf, y_sup)):
            self._set_option(name, value)

    ##############################################

    def scan(self, path):

        scan_session = self._device.scan(multiple=False)

        try:
            while True:
                scan_session.scan.read()
        except EOFError:
            pass

        image = scan_session.images[-1]
        image.save(path)
        self._logger.info('Scanned {}'.format(path))

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

Reference
---------

* `SANE — Scanner Access Now Easy <http://www.sane-project.org>`_
* `The SANE Application Programmer Interface (API) <http://www.sane-project.org/html/doc009.html>`_
* `Windows Image Acquisition 2.0 <https://docs.microsoft.com/en-us/windows/desktop/wia/-wia-startpage>`_

* `PyInsane 2 — Python library to support image scanners (Sane and WIA) <https://gitlab.gnome.org/World/OpenPaperwork/pyinsane>`_

"""

####################################################################################################

__all__ = [
    'Scanner',
    'FileExistsError',
]

####################################################################################################

from pathlib import Path
import logging

import pyinsane2

from PIL import Image, ImageDraw, ImageFont

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class FileExistsError(NameError):
    pass

####################################################################################################

class Scanner:

    """class to implement a scanner interface."""

    __initialised__ = False

    _logger = _module_logger.getChild('Scanner')

    #: Scanning Area (x_inf, x_sup, y_inf, y_sup)
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

    def __bool__(self):
        return self._device is not None

    ##############################################

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, name):
        self._device = pyinsane2.Scanner(name=name)

    @property
    def device_name(self):
        # See pyinsane2/sane/abstract_proc.py
        # device.name
        # device.nice_name
        # device.vendor
        # device.model
        # device.dev_type
        return '{0.vendor} {0.model}'.format(self._device)

    ##############################################

    def _set_option(self, name, value):
        self._logger.info('{} = {}'.format(name, value))
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
        # [(0, 14149222, 0), (0, 14149222, 0),
        #  (0, 19475988, 0), (0, 19475988, 0)]
        return [self._get_option_constraint(name) for name in self.AREA_OPTIONS]

    @property
    def area_constraint_x_inf(self):
        return self.area_constraint[0][0]

    @property
    def area_constraint_x_sup(self):
        return self.area_constraint[0][1]

    @property
    def area_constraint_y_inf(self):
        return self.area_constraint[2][0]

    @property
    def area_constraint_y_sup(self):
        return self.area_constraint[2][1]

    @area.setter
    def area(self, bounds):
        # x_inf, x_sup, y_inf, y_sup = bounds
        self._logger.info('Set scanner area to {}'.format(bounds))
        for name, value in zip(self.AREA_OPTIONS, bounds):
            self._set_option(name, value)

    def set_area_as_scale(self, x_inf, x_sup, y_inf, y_sup):
        bounds = (x_inf, x_sup, y_inf, y_sup)
        self._logger.info('Set scanner area to {} %'.format(bounds))
        scanner_width = self.area_constraint_x_sup
        scanner_height = self.area_constraint_y_sup
        area = [int(round(x)) for x in (
            x_inf*scanner_width,  x_sup*scanner_width,
            y_inf*scanner_height, y_sup*scanner_height,
        )
        ]
        self.area = area

    ##############################################

    def scan_image(self):

        self._logger.info('Start scanning ...')

        scan_session = self._device.scan(multiple=False)

        try:
            while True:
                scan_session.scan.read()
        except EOFError:
            pass

        image = scan_session.images[-1]
        self._logger.info('Start done')

        return image

    ##############################################

    def scan(self, path, overwrite=False, index=None):

        self._logger.info('Scan {} {} overwrite = {}'.format(path, index, overwrite))

        # Fixme: kwargs
        if index is not None:
            path = str(path).format(index)

        path = Path(path).resolve()

        if not overwrite and path.exists():
            # raise NameError('File {} exists'.format(path))
            raise FileExistsError(str(path))

        image = self.scan_image()
        image.save(str(path))
        self._logger.info('Saved {}'.format(path))

        return path

####################################################################################################

class FakeDevice:

    __resolution_constraint__ = [100, 200, 400]
    __mode_constraint__ = ['Color', 'Grayscale']
    __x_max__ = 14149222
    __y_max__ = 19475988
    __area_constraint__ = [(0, __x_max__, 0), (0, __x_max__, 0),
                           (0, __y_max__, 0), (0, __y_max__, 0)]

    _logger = _module_logger.getChild('FakeDevice')

    ##############################################

    def __init__(self):

        self._resolution = self.__resolution_constraint__[0]
        self._mode = self.__mode_constraint__[0]
        self._area = [0, self.__x_max__, 0, self.__y_max__]

    ##############################################

    def __str__(self):
        return 'fake scanner'

    ##############################################

    @property
    def vendor(self):
        return 'Fake'

    @property
    def model(self):
        return 'Scanner'

    ##############################################

    def constraint(self, name):
        return getattr(self, '__{}_constraint__'.format(name))

    ##############################################

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, value):
        self._resolution = int(value)
        self._logger.info('resolution = {0._resolution}'.format(self))

    ##############################################

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = str(value)
        self._logger.info('mode = {0._mode}'.format(self))

    ##############################################

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, value):
        self._area = [int(x) for x in value[:4]]
        self._logger.info('area = {0._area}'.format(self))

####################################################################################################

class FakeScanner(Scanner):

    _logger = _module_logger.getChild('FakeScanner')

    __fake_device__ = FakeDevice()

    __scan_count__ = 0

    ##############################################

    @classmethod
    def init(cls):
        cls.__initialised__ = True
        cls._logger.info('Sane is initialised')

    ##############################################

    @classmethod
    def exit(cls):
        if cls.__initialised__:
            cls.__initialised__ = False
            cls._logger.info('Sane exited')

    ##############################################

    @classmethod
    def devices(cls):
        return [cls.__fake_device__]

    ##############################################

    def __init__(self, device_hint='fake', release=True):
        super().__init__(device_hint, release)

    ##############################################

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, name):
        raise NotImplementedError

    ##############################################

    def _set_option(self, name, value):
        raise NotImplementedError

    def _get_option(self, name):
        raise NotImplementedError

    def _get_option_constraint(self, name):
        return self._device.constraint(name)

    ##############################################

    def maximize_scan_area(self):
        pass

    ##############################################

    @property
    def resolution(self):
        return self._device.resolution

    @resolution.setter
    def resolution(self, value):
        self._device.resolution = value

    ##############################################

    @property
    def mode(self):
        return self._device.mode

    @mode.setter
    def mode(self, value):
        self._device.mode = value

    ##############################################

    @property
    def area(self):
        return self._device.area

    @area.setter
    def area(self, bounds):
        # x_inf, x_sup, y_inf, y_sup = bounds
        self._logger.info('Set scanner area to {}'.format(bounds))
        self._device.area = bounds

    @property
    def area_constraint(self):
        return self._device.constraint('area')

    ##############################################

    def scan_image(self):

        self._logger.info('Start scanning ...')
        self._logger.info('Start done')

        self.__scan_count__ += 1

        size = (1000, 1000) # Fixme:
        image = Image.new('RGB', size, color=(255,255,255))
        font = ImageFont.truetype('DejaVuSans.ttf', 200)
        context= ImageDraw.Draw(image)
        text = '{}'.format(self.__scan_count__)
        context.text((100,100), text, font=font, fill=(0,0,0))

        return image

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

"""Module to implement a scanner interface.

Reference
---------

* `SANE — Scanner Access Now Easy <http://www.sane-project.org>`_
* `The SANE Application Programmer Interface (API) <http://www.sane-project.org/html/doc009.html>`_
* `Windows Image Acquisition 2.0 <https://docs.microsoft.com/en-us/windows/desktop/wia/-wia-startpage>`_

* `PyInsane 2 — Python library to support image scanners (Sane and WIA) <https://gitlab.gnome.org/World/OpenPaperwork/pyinsane>`_

"""

# Fixme: replace PyInsane by a cffi or cython binding, featuring a clean oo api and nogil
#        PyInsane raise exceptions when ???

####################################################################################################

__all__ = [
    'Scanner',
    'FileExistsError'
    'PathError',
]

####################################################################################################

from pathlib import Path
import logging

from PIL import Image, ImageDraw, ImageFont

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

# import pyinsane2
# from pyinsane2.sane.rawapi import SaneException

_module_logger.info("Initializing libinsane ...")
# pip install gobject PyGObject
import gi
from gi.repository import GObject
gi.require_version('Libinsane', '1.0')
from gi.repository import Libinsane

class LibinsaneLogger(GObject.GObject, Libinsane.Logger):
    CALLBACKS = {
        Libinsane.LogLevel.ERROR: _module_logger.error,
        Libinsane.LogLevel.WARNING: _module_logger.warning,
        Libinsane.LogLevel.INFO: _module_logger.info,
        Libinsane.LogLevel.DEBUG: lambda msg: 0,
    }
    def do_log(self, lvl, msg):
        self.CALLBACKS[lvl](msg)

Libinsane.register_logger(LibinsaneLogger())
libinsane = Libinsane.Api.new_safebet()

_module_logger.info('Scan library: Libinsane {}'.format(
    Libinsane.Api.get_version())
)

####################################################################################################

class FileExistsError(NameError):
    pass

class PathError(NameError):
    pass

####################################################################################################

####class LegacyScanner:
####
####    """class to implement a scanner interface."""
####
####    __initialised__ = False
####
####    _logger = _module_logger.getChild('Scanner')
####
####    #: Scanning Area (x_inf, x_sup, y_inf, y_sup)
####    AREA_OPTIONS = ('tl-x', 'br-x', 'tl-y', 'br-y')
####
####    AREA_UNIT_SCALE = 2**16
####
####    ##############################################
####
####    @classmethod
####    def init(cls):
####        # This call takes a lot of time
####        try:
####            pyinsane2.init()
####        except:
####            cls._logger.warning('SANE initialisation failed')
####        cls.__initialised__ = True
####        cls._logger.info('Sane is initialised')
####
####    ##############################################
####
####    @classmethod
####    def exit(cls):
####        if cls.__initialised__:
####            try:
####                pyinsane2.exit()
####            except:
####                self._logger.warning('SANE exit failed')
####            cls.__initialised__ = False
####            cls._logger.info('Sane exited')
####
####    ##############################################
####
####    @classmethod
####    def devices(cls):
####        if cls.__initialised__:
####            return pyinsane2.get_devices() # Fixme: exception ???
####        else:
####            return []
####
####    ##############################################
####
####    def __init__(self, device_hint='libusb', release=True):
####
####        if not self.__initialised__:
####            self.init()
####
####        self._release = bool(release)
####
####        self._device = None
####        for device in self.devices():
####            self._logger.info('Sane device {}'.format(device))
####            if device_hint in str(device):
####                self._device = device
####                self._logger.info('Sane use {}'.format(device))
####
####    ##############################################
####
####    def __del__(self):
####        if self._release:
####            self.exit()
####
####    ##############################################
####
####    def __bool__(self):
####        return self._device is not None
####
####    ##############################################
####
####    @property
####    def device(self):
####        return self._device
####
####    @device.setter
####    def device(self, name):
####        self._device = pyinsane2.Scanner(name=name) # Fixme: exception ???
####
####    @property
####    def device_name(self):
####        # See pyinsane2/sane/abstract_proc.py
####        # device.name
####        # device.nice_name
####        # device.vendor
####        # device.model
####        # device.dev_type
####        return '{0.vendor} {0.model}'.format(self._device)
####
####    ##############################################
####
####    def _set_option(self, name, value):
####        self._logger.info('{} = {}'.format(name, value))
####        try:
####            pyinsane2.set_scanner_opt(self._device, name, [value])
####        except SaneException:
####            self._logger.warning('Invalid option {}={}'.format(name, value))
####
####    def _get_option(self, name):
####        return self._device.options[name].value
####
####    def _get_option_constraint(self, name):
####        return self._device.options[name].constraint
####
####    ##############################################
####
####    def maximize_scan_area(self):
####        pyinsane2.maximize_scan_area(self._device) # Fixme: exception ??? 
####
####    ##############################################
####
####    @property
####    def resolution(self):
####        return self._get_option('resolution')
####
####    @property
####    def resolution_constraint(self):
####        return self._get_option_constraint('resolution')
####
####    @resolution.setter
####    def resolution(self, value):
####        self._set_option('resolution', value)
####
####    ##############################################
####
####    @property
####    def mode(self):
####        return self._get_option('mode')
####
####    @property
####    def mode_constraint(self):
####        return self._get_option_constraint('mode')
####
####    @mode.setter
####    def mode(self, value):
####        self._set_option('mode', value)
####
####    ##############################################
####
####    @classmethod
####    def area_unit_from_mm(cls, x):
####        # scanner unit mm * 2**16 ???
####        return x * cls.AREA_UNIT_SCALE
####
####    @classmethod
####    def area_unit_to_mm(cls, x):
####        return x / cls.AREA_UNIT_SCALE
####
####    @property
####    def area(self):
####        return [self._get_option(name) for name in self.AREA_OPTIONS]
####
####    @property
####    def area_mm(self):
####        return [self.area_unit_to_mm(x) for x in self.area]
####
####    @property
####    def area_constraint(self):
####        # [(0, 14149222, 0), (0, 14149222, 0),
####        #  (0, 19475988, 0), (0, 19475988, 0)]
####        # ~ 21.59 x 29.79 cm
####        return [self._get_option_constraint(name) for name in self.AREA_OPTIONS]
####
####    @property
####    def area_constraint_mm(self):
####        return [self.area_unit_to_mm(x) for x in self.area_constraint]
####
####    @property
####    def area_constraint_x_inf(self):
####        return self.area_constraint[0][0]
####
####    @property
####    def area_constraint_x_sup(self):
####        return self.area_constraint[0][1]
####
####    @property
####    def area_constraint_y_inf(self):
####        return self.area_constraint[2][0]
####
####    @property
####    def area_constraint_y_sup(self):
####        return self.area_constraint[2][1]
####
####    @property
####    def area_constraint_x_inf_mm(self):
####        return self.area_unit_to_mm(self.area_constraint_x_inf)
####
####    @property
####    def area_constraint_y_inf_mm(self):
####        return self.area_unit_to_mm(self.area_constraint_y_inf)
####
####    @property
####    def area_constraint_x_sup_mm(self):
####        return self.area_unit_to_mm(self.area_constraint_x_sup)
####
####    @property
####    def area_constraint_y_sup_mm(self):
####        return self.area_unit_to_mm(self.area_constraint_y_sup)
####
####    @area.setter
####    def area(self, bounds):
####        # x_inf, x_sup, y_inf, y_sup = bounds
####        self._logger.info('Set scanner area to {}'.format(bounds))
####        for name, value in zip(self.AREA_OPTIONS, bounds):
####            self._set_option(name, value)
####
####    def set_area_as_scale(self, x_inf, x_sup, y_inf, y_sup):
####        bounds = (x_inf, x_sup, y_inf, y_sup)
####        self._logger.info('Set scanner area to {} %'.format(bounds))
####        scanner_width = self.area_constraint_x_sup
####        scanner_height = self.area_constraint_y_sup
####        area = [int(round(x)) for x in (
####            x_inf*scanner_width,  x_sup*scanner_width,
####            y_inf*scanner_height, y_sup*scanner_height,
####        )
####        ]
####        self.area = area
####
####    ##############################################
####
####    def scan_image(self):
####
####        self._logger.info('Start scanning ...')
####
####        scan_session = self._device.scan(multiple=False)
####
####        try:
####            while True:
####                scan_session.scan.read()
####        except EOFError:
####            pass
####
####        image = scan_session.images[-1]
####        self._logger.info('Start done')
####
####        return image
####
####    ##############################################
####
####    def scan(self, path, overwrite=False, index=None):
####
####        self._logger.info('Scan {} {} overwrite = {}'.format(path, index, overwrite))
####
####        # Fixme: kwargs
####        if index is not None:
####            path = str(path).format(index)
####
####        path = Path(path).resolve()
####
####        parent = path.parent
####        if not path.parent.exists():
####            raise PathError(str(parent))
####
####        if not overwrite and path.exists():
####            raise FileExistsError(str(path))
####
####        image = self.scan_image()
####        try:
####            image.save(str(path))
####            self._logger.info('Saved {}'.format(path))
####            return path
####        except FileNotFoundError: # should not happen, cf. PathError
####            self._logger.warning('Invalid path {}'.format(path))
####            return None

####################################################################################################

class Scanner:

    """class to implement a scanner interface."""

    _logger = _module_logger.getChild('Scanner')

    #: Scanning Area (x_inf, x_sup, y_inf, y_sup)
    AREA_OPTIONS = ('tl-x', 'br-x', 'tl-y', 'br-y')

    AREA_UNIT_SCALE = 2**16

    ##############################################

    @classmethod
    def init(cls):
        pass

    ##############################################

    @classmethod
    def exit(cls):
        pass

    ##############################################

    @classmethod
    def devices(cls):
        devices = libinsane.list_devices(Libinsane.DeviceLocations.ANY)
        # for device in devices:
        #     print("[{}] : [{}]".format(device.get_dev_id(), device.to_string()))
        return [device.get_dev_id() for device in devices]

    ##############################################

    def __init__(self, device_hint='libusb'):

        self._device = None
        # Fixme: take a while, async
        devices = libinsane.list_devices(Libinsane.DeviceLocations.ANY)
        for device in devices:
            device_id = device.get_dev_id()
            self._logger.info('Sane device {} {}'.format(device_id, device.to_string()))
            if device_hint in device_id:
                self.device = device_id
                self._logger.info('Sane use {}'.format(device_id))

    ##############################################

    def __bool__(self):
        return self._device is not None

    ##############################################

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, device_id):
        self._device = libinsane.get_device(device_id)

    @property
    def device_name(self):
        # Fixme:
        return self._device.get_name()

    ##############################################

    def source_names(self):
        return [source.get_name() for source in self._device.get_children()]

    def source(self, name='flatbed'):
        sources = self._device.get_children()
        for src in sources:
            if src.get_name() == name:
                return  src
        else:
            raise NameError("Source '{}' not found".format(name))

    ##############################################

    @property
    def options(self):
        # Fixme: cache ???
        return {option.get_name():option for option in self._device.get_options()}

    # option.get_name()
    # option.get_title()
    # option.get_desc()
    # option.get_value_type()
    # option.get_value_unit()
    # option.is_readable()
    # option.is_writable()
    # option.get_capabilities()
    # option.get_constraint_type()
    # option.get_constraint()
    # option.get_value()

    ##############################################

    def _set_option(self, name, value):
        self._logger.info('{} = {}'.format(name, value))
        try:
            self.options[name].set_value(value)
        except Exception as exception:
            # traceback.print_exc()
            self._logger.warning('Invalid option {}={}'.format(name, value))

    def _get_option(self, name):
        return self.options[name].get_value()

    def _get_option_constraint(self, name):
        return self.options[name].get_constraint()

    ##############################################

    def maximize_scan_area(self):
        self._set_option('tl-x', self._get_option_constraint('tl-x')[0])
        self._set_option('tl-y', self._get_option_constraint('tl-y')[0])
        self._set_option('br-x', self._get_option_constraint('br-x')[1])
        self._set_option('br-y', self._get_option_constraint('br-y')[1])

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

    @classmethod
    def area_unit_from_mm(cls, x):
        # scanner unit mm * 2**16 ???
        return x * cls.AREA_UNIT_SCALE

    @classmethod
    def area_unit_to_mm(cls, x):
        return x / cls.AREA_UNIT_SCALE

    @property
    def area(self):
        return [self._get_option(name) for name in self.AREA_OPTIONS]

    @property
    def area_mm(self):
        return [self.area_unit_to_mm(x) for x in self.area]

    @property
    def area_constraint(self):
        # [(0, 14149222, 0), (0, 14149222, 0),
        #  (0, 19475988, 0), (0, 19475988, 0)]
        # ~ 21.59 x 29.79 cm
        return [self._get_option_constraint(name) for name in self.AREA_OPTIONS]

    @property
    def area_constraint_mm(self):
        return [self.area_unit_to_mm(x) for x in self.area_constraint]

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

    @property
    def area_constraint_x_inf_mm(self):
        return self.area_unit_to_mm(self.area_constraint_x_inf)

    @property
    def area_constraint_y_inf_mm(self):
        return self.area_unit_to_mm(self.area_constraint_y_inf)

    @property
    def area_constraint_x_sup_mm(self):
        return self.area_unit_to_mm(self.area_constraint_x_sup)

    @property
    def area_constraint_y_sup_mm(self):
        return self.area_unit_to_mm(self.area_constraint_y_sup)

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

    def raw_to_image(self, parameters, image_bytes):
        fmt = parameters.get_format()
        assert(fmt == Libinsane.ImgFormat.RAW_RGB_24)
        (w, h) = (
            parameters.get_width(),
            int(len(image_bytes) / 3 / parameters.get_width())
        )
        return Image.frombuffer('RGB', (w, h), image_bytes, 'raw', 'RGB', 0, 1)

    ##############################################

    def scan_image(self):

        self._logger.info('Start scanning ...')

        source = self.source()
        session = source.scan_start()
        try:
            image = []
            while not session.end_of_page():
                data = session.read_bytes(128 * 1024) # 128 kb
                data = data.get_data()
                image.append(data)
            image = b''.join(image)

            scan_params = session.get_scan_parameters()
            if scan_params.get_format() == Libinsane.ImgFormat.RAW_RGB_24:
                image = self.raw_to_image(scan_params, image)

        except Exception as exception:
            self._logger.error(str(exception))
            raise exception
        finally:
            session.cancel()

        return image

    ##############################################

    def scan(self, path, overwrite=False, index=None):

        self._logger.info('Scan {} {} overwrite = {}'.format(path, index, overwrite))

        # Fixme: kwargs
        if index is not None:
            path = str(path).format(index)

        path = Path(path).resolve()

        parent = path.parent
        if not path.parent.exists():
            raise PathError(str(parent))

        if not overwrite and path.exists():
            raise FileExistsError(str(path))

        image = self.scan_image()
        try:
            image.save(str(path))
            self._logger.info('Saved {}'.format(path))
            return path
        except FileNotFoundError: # should not happen, cf. PathError
            self._logger.warning('Invalid path {}'.format(path))
            return None

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

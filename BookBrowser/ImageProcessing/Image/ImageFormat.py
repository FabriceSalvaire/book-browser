####################################################################################################
#
# BookBrowser - A Digitised Book Solution
# Copyright (C) 2018 Fabrice Salvaire
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

__all__ = ['ImageFormat']

####################################################################################################

import numpy as np

####################################################################################################

class ImageFormat:

    """Class to implement image format"""

    RGB = ('red', 'green', 'blue')
    BGR = ('blue', 'green', 'red')
    HLS = ('hue', 'luminosity', 'saturation')

    Gray = ('intensity',)
    Label = ('label',) # should be unsigned integer
    Binary = ('mask',) # boolean interpretation

    ##############################################

    def __init__(self,
                 height, width, number_of_channels=1,
                 data_type=np.uint8,
                 normalised=False,
                 channels=None):

        error_string = ' must be >= 1'
        if height < 1:
            raise ValueError('height' + error_string)
        if width < 1:
            raise ValueError('width' + error_string)
        if number_of_channels < 1:
            raise ValueError('number of planes' + error_string)

        self._height = height
        self._width = width
        self._number_of_channels = number_of_channels
        self._data_type = data_type
        self._normalised = normalised # only for float data type
        self._channels = channels
        if channels is not None:
            if len(channels) != number_of_channels:
                raise NameError("channels don't match number_of_channels")
            self._channel_map = {channel:i for i, channel in enumerate(channels)}
        else:
            self._channel_map = None

    ##############################################

    def clone(self, **kwargs):
        d = dict(
            height=self._height,
            width=self._width,
            number_of_channels=self._number_of_channels,
            data_type=self._data_type,
            normalised=self._normalised,
            channels=self._channels,
        )
        d.update(kwargs)
        return self.__class__(**d)

    ##############################################

    def transpose(self):
        return self.clone(height=self._width, width=self._height)

    ##############################################

    def __repr__(self):
        return ("ImageFormat shape = ({}, {}, {})\n"
                "  dtype = {} normalised = {}\n"
                "  channels = {}".format(
                    self._height, self._width, self._number_of_channels,
                    self._data_type, self._normalised,
                    self._channels,
        ))

    ##############################################

    def __getitem__(self, i):
        if self._channels is not None:
            # not duck typing
            if isinstance(i, int):
                return self._channels[i]
            else:
                return self._channel_map[i]
        else:
            return None

    ##############################################

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def number_of_channels(self):
        return self._number_of_channels

    @property
    def channels(self):
        return self._channels

    @property
    def data_type(self):
        return self._data_type

    @property
    def is_normalised(self):
        return self._normalised

    ##############################################

    @property
    def number_of_pixels(self):
        return self._height * self._width

    @property
    def dimension(self):
        return (self._width, self._height)

    @property
    def shape(self):
        if self.number_of_channels == 1:
            return (self._height, self._width)
        else:
            return (self._height, self._width, self._number_of_channels)

    ##############################################

    @property
    def number_of_bytes(self):
        return (self._height * self._width * self._number_of_channels
                * self.data_type_number_of_bytes)

    @property
    def data_type_number_of_bytes(self):
        return np.nbytes[self._data_type]

    @property
    def data_type_number_of_bits(self):
        return 8 * self.data_type_number_of_bytes

    ##############################################

    @property
    def is_integer(self):
        return self.is_unsigned_integer or self.is_signed_integer

    @property
    def is_signed_integer(self):
        return self._data_type in (np.int8, np.int16, np.int32, np.int64)

    @property
    def is_unsigned_integer(self):
        return self._data_type in (np.uint8, np.uint16, np.uint32, np.uint64)

    @property
    def is_float(self):
        # == (np.float, np.double)
        return self._data_type in (np.float32, np.float64)

    ##############################################

    @property
    def inf(self):

        if self.is_unsigned_integer:
            return 0
        elif self.is_signed_integer:
            return - 2**(self.data_type_number_of_bits -1)
        elif self.is_float and self._normalised:
            return .0
        else:
            raise NotImplementedError

    ##############################################

    @property
    def sup(self):

        if self.is_unsigned_integer:
            return 2**self.data_type_number_of_bits -1
        elif self.is_signed_integer:
            return 2**(self.data_type_number_of_bits -1) -1
        elif self.is_float and self._normalised:
            return 1.
        else:
            raise NotImplementedError

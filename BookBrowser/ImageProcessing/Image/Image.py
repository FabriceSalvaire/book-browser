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

__all__ = ['Image']

####################################################################################################

import numpy as np

try:
    import cv2 as cv
except ImportError:
    cv = None

####################################################################################################

from .ImageFormat import ImageFormat

####################################################################################################

class Image(np.ndarray):

    """Class to wrap an image as a Numpy array"""

    ##############################################

    def __new__(cls, *args, **kwargs):

        input_array = None
        number_of_args = len(args)
        if number_of_args == 1:
            obj = args[0]
            if isinstance(obj, ImageFormat):
                image_format = obj.clone(**Image._kwargs_for_image_format(kwargs))
            elif isinstance(obj, Image):
                input_array = obj
                image_format = input_array.image_format.clone(**Image._kwargs_for_image_format(kwargs))
            elif isinstance(obj, np.ndarray):
                input_array = obj
                height, width = input_array.shape[:2]
                if input_array.ndim == 3:
                    number_of_channels = input_array.shape[2]
                else:
                    number_of_channels = 1
                kwargs_for_image_format = dict(height=height, width=width, number_of_channels=number_of_channels,
                                               data_type=input_array.dtype)
                kwargs_for_image_format.update(Image._kwargs_for_image_format(kwargs))
                image_format = ImageFormat(**kwargs_for_image_format)
            else:
                raise ValueError("Bad argument " + str(type(obj)))
        else:
            image_format = ImageFormat(*args, **kwargs)

        if input_array is None:
            obj = np.ndarray.__new__(cls, image_format.shape, image_format.data_type,
                                     buffer=None, offset=0, strides=None, order=None)
        else:
            if input_array.shape != image_format.shape:
                raise NameError("Shape mismatch")
            if kwargs.get('share', False):
                obj = input_array.view(cls)
            else:
                obj = np.asarray(input_array, dtype=image_format.data_type).view(cls)

        obj.image_format = image_format

        return obj

    ##############################################

    @staticmethod
    def _kwargs_for_image_format(kwargs):

        kwargs = dict(kwargs)
        for key in ('share',):
            if key in kwargs:
                del kwargs[key]
        return kwargs

    ##############################################

    def __array_finalize__(self, obj):

        if obj is None:
            return

        # _image_format
        self.image_format = getattr(obj, 'image_format', None)

    ##############################################

    # def __repr__(self):
    #     return 'Image\n' + repr(self.image_format)

    ##############################################

    def set(self, value):

        # cv2 ?
        # cv.Set(self, value)
        self[...] = value

    ##############################################

    def clear(self):
        self.set(0)

    ##############################################

    def to_normalised_float(self, float_image=None, double=False):

        if float_image is None:
            if double:
                data_type = np.float64
            else:
                data_type = np.float32
            float_image = self.__class__(self, data_type=data_type, normalised=True)
        else:
            float_image[...] = self
        float_image *= 1./self.image_format.sup

        return float_image

    ##############################################

    def convert_colour(self, channels, output_image=None):

        # Fixme: check output_image

        image_format = self.image_format
        if channels is ImageFormat.HLS:
            if image_format.channels is ImageFormat.RGB:
                if image_format.is_unsigned_integer:
                    float_image = self.to_normalised_float()
                    if output_image is None:
                        output_image = self.__class__(float_image, share=True, channels=ImageFormat.HLS)
                elif image_format.is_float and image_format.normalised:
                    float_image = self
                    if output_image is None:
                        output_image = self.__class__(image_format, channels=ImageFormat.HLS)
                else:
                    raise NotImplementedError
                # Fixme: catch error
                cv.cvtColor(float_image, cv.COLOR_RGB2HLS, output_image)
                output_image[:,:,0] *= 1./360 # normalised float, else have to define sup !
                return output_image
            else:
                raise NotImplementedError

        elif channels is ImageFormat.Gray:
            if image_format.channels is ImageFormat.RGB:
                if output_image is None:
                    output_image = self.__class__(image_format, channels=ImageFormat.Gray)
                cv.cvtColor(self, cv.COLOR_RGB2GRAY, output_image)
                return output_image
            else:
                raise NotImplementedError

        else:
            raise NotImplementedError

    ##############################################

    def swap_channels(self, channels):

        image_format = self.image_format
        if ((channels is ImageFormat.BGR and image_format.channels is ImageFormat.RGB) or
            (channels is ImageFormat.RGB and image_format.channels is ImageFormat.BGR)):
            output = self.__class__(image_format, channels=channels)
            cv.mixChannels([self], [output], (0,2, 1,1, 2,0))
            return output
            # ???
        else:
            raise NotImplementedError

    ##############################################

    def split_channels(self):

        channel_arrays = cv.split(self)
        image_format = self.image_format
        return [self.__class__(channel_array, share=True, number_of_channels=1, channels=(channel,))
                for channel, channel_array in zip(image_format.channels, channel_arrays)]

        # cv.merge(mv)

    ##############################################

    def flip_vertically(self):
        cv.flip(self, 0, self)

    ##############################################

    def flip_horizontally(self):
        cv.flip(self, 1, self)

    ##############################################

    def transpose(self):

        output = self.__class__(self.image_format.transpose())
        cv.transpose(self, output)
        return output

    ##############################################

    def histogram(self, channel=0, inf=None, sup=None, number_of_bins=None):

        image_format = self.image_format
        if inf is None:
            inf = image_format.inf
        if sup is None:
            sup = image_format.sup
        if number_of_bins is None:
            number_of_bins = sup - inf
        if isinstance(channel, str):
            channel = self.image_format[channel]

        histogram = cv.calcHist([self], [channel],
                                None,
                                [number_of_bins], [inf, sup])
        return histogram

    ##############################################

    def save(self, path):
        cv.imwrite(path, self)

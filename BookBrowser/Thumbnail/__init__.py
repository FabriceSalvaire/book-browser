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

"""Module to implement freedesktop.org thumbnail cache
https://specifications.freedesktop.org/thumbnail-spec/thumbnail-spec-latest.html

"""

####################################################################################################

__all__ = ['FreeDesktopThumbnailCache']

####################################################################################################

from functools import lru_cache
from pathlib import Path
import hashlib
import logging
import mimetypes
import os
import shutil

from PIL import Image, PngImagePlugin

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class FreeDesktopThumbnailCache:

    """Class to import FreeDesktop Thumbnail Cache"""

    NORMAL_SIZE = 128
    LARGE_SIZE = 256
    IMAGE_FORMAT = 'png'
    IMAGE_EXTENSION = '.' + IMAGE_FORMAT
    SAMPLING = Image.BICUBIC

    _logger = _module_logger.getChild('FreeDesktopThumbnailCache')

    ##############################################

    def __init__(self):

        self._path = Path.home().joinpath('.cache', 'thumbnails')
        self._normal_path = self._path.joinpath('normal')
        self._large_path = self._path.joinpath('large')

        for path in (self._path, self._normal_path, self._large_path):
            if not path.exists():
                os.mkdir(path)

    ##############################################

    @classmethod
    def uri_path(cls, path):
        return 'file://' + str(path)

    ##############################################

    @lru_cache(maxsize=512)
    def mangle_path(self, path):
        uri = self.uri_path(path)
        return hashlib.md5(uri.encode('utf-8')).hexdigest() + self.IMAGE_EXTENSION

    ##############################################

    def _thumbnail_path(self, cache_path, path):
        return cache_path.joinpath(self.mangle_path(path))

    def thumbnail_path(self, path, is_normal=True):
        if is_normal:
            cache_path = self._normal_path
        else:
            cache_path = self._large_path
        return self._thumbnail_path(cache_path, path)

    def normal_thumbnail_path(self, path):
        return self.thumbnail_path(path, True)

    def large_thumbnail_path(self, path):
        return self.thumbnail_path(path, False)

    ##############################################

    def has_thumbnail(self, path, is_normal=True):
        return self.thumbnail_path(path, is_normal).exists()

    def has_normal_thumbnail(self, path):
        return self.has_thumbnail(path, True)

    def has_large_thumbnail(self, path):
        return self.has_thumbnail(path, False)

    ##############################################

    def clear_cache(self):
        # Warning: This command is dangerous !!!
        #! self._logger.info('Clear thumbnail cache {}'.format(self._path))
        #! shutil.rmtree(str(self._path), ignore_errors=True)
        pass

    ##############################################

    @classmethod
    def _make_png_info(cls, src_path):

        # {
        #     'Thumb::URI': 'file:///home/fabrice/....png'
        #     'Thumb::MTime': '1547660783',
        #
        #     'Thumb::Size': '3312888',
        #     'Thumb::Mimetype': 'image/png',
        #     'Software': 'KDE Thumbnail Generator Images (GIF, PNG, BMP, ...)',
        #
        #     'dpi': (96, 96),
        # }

        file_stat = Path(src_path).stat()

        mtime = int(file_stat.st_mtime)
        file_size = file_stat.st_size # bytes
        mime_type = mimetypes.guess_type(str(src_path))[0]

        png_info = PngImagePlugin.PngInfo()
        # required
        png_info.add_text('Thumb::URI', cls.uri_path(src_path))
        png_info.add_text('Thumb::MTime', mtime)
        # optional
        png_info.add_text('Thumb::Size', file_size)
        png_info.add_text('Thumb::Mimetype', mime_type)
        png_info.add_text('Software', 'Book Browser')

        return png_info

    ##############################################

    @classmethod
    def _make_thumbnail(cls, src_path, dst_path, size):
        image = Image.open(str(src_path))
        image.thumbnail((size, size), resample=cls.SAMPLING)
        png_info = cls._make_png_info(src_path)
        image.save(str(dst_path), 'PNG', pnginfo=png_info)

    ##############################################

    def make_normal_thumbnail(self, path):
        self._make_thumbnail(path, self.normal_thumbnail_path(path), self.NORMAL_SIZE)

    def make_large_thumbnail(self, path):
        self._make_thumbnail(path, self.large_thumbnail_path(path), self.LARGE_SIZE)

    def make_thumbnail(self, path, is_normal=True):
        if is_normal:
            self.make_normal_thumbnail(path)
        else:
            self.make_large_thumbnail(path)

    ##############################################

    def thumbnail(self, path, is_normal=True):
        # Fixme: mangle x3
        if not self.has_thumbnail(path, is_normal):
            self._logger.info('Make thumbnail for {}'.format(path))
            self.make_thumbnail(path, is_normal)
        return self.thumbnail_path(path, is_normal)

    def normal_thumbnail(self, path):
        return self.thumbnail(path, True)

    def large_thumbnail(self, path):
        return self.thumbnail(path, False)

    ##############################################

    def _delete_thumbnail(self, path, is_normal=False):
        if self.has_thumbnail(path, is_normal):
            os.unlink(self.thumbnail_path(path, is_normal))

    def delete_thumbnail(self, path):
        for is_normal in (False, True):
            self._delete_thumbnail(path, is_normal=is_normal)


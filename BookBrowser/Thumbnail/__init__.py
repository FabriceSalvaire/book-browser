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

from pathlib import Path
import hashlib
import logging
import mimetypes
import os
# import shutil

from PIL import Image, PngImagePlugin

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class FreeDesktopThumbnail:

    IMAGE_FORMAT = 'png'
    IMAGE_EXTENSION = '.' + IMAGE_FORMAT
    SAMPLING = Image.BICUBIC

    _logger = _module_logger.getChild('FreeDesktopThumbnail')

    ##############################################

    @classmethod
    def add_uri(cls, path):
        return 'file://' + str(path)

    ##############################################

    @classmethod
    def mangle_path(cls, path):
        uri = cls.add_uri(path)
        return hashlib.md5(uri.encode('utf-8')).hexdigest() + cls.IMAGE_EXTENSION

    ##############################################

    def __init__(self, cache, path):

        self._cache = cache
        self._source_path = Path(path).resolve()
        self._filename = self.mangle_path(path)
        self._stat = self._source_path.stat()

    ##############################################

    @property
    def source_path(self):
        return self._source_path

    @property
    def uri(self):
        return self.add_uri(self._source_path)

    ##############################################

    @property
    def size(self):
        return self._stat.st_size

    @property
    def mtime(self):
        return int(self._stat.st_mtime)

    @property
    def mime_type(self):
        return mimetypes.guess_type(str(self._source_path))[0]

    ##############################################

    @property
    def normal_path(self):
        return self._cache.normal_thumbnail_path(self._filename)

    @property
    def large_path(self):
        return self._cache.large_thumbnail_path(self._filename)

    def thumbnail_path(self, is_normal=True):
        return self._cache.thumbnail_path(self._filename, is_normal)

    ##############################################

    def _delete_thumbnail(self, is_normal=False):
        path = self.thumbnail_path(is_normal)
        if path.exists():
            self._logger.info('Delete thumbnail for {}'.format(self._source_path))
            os.unlink(path)


    def delete_thumbnail(self):
        for is_normal in (False, True):
            self._delete_thumbnail(is_normal)

    ##############################################

    def has_thumbnail(self, is_normal=True):
        path = self.thumbnail_path(is_normal)
        if path.exists():
            stat = path.stat()
            thumbnail_size = int(stat.st_size)
            thumbnail_mtime = int(stat.st_mtime) # Fixme: int ???
            if not thumbnail_size or thumbnail_mtime < self.mtime:
                self.delete_thumbnail()
            else:
                return True
        return False


    def has_normal_thumbnail(self, path):
        return self.has_thumbnail(True)

    def has_large_thumbnail(self, path):
        return self.has_thumbnail(False)

    ##############################################

    def _make_png_info(self):

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

        png_info = PngImagePlugin.PngInfo()
        # required
        png_info.add_text('Thumb::URI', self.uri)
        png_info.add_text('Thumb::MTime', str(self.mtime))
        # optional
        png_info.add_text('Thumb::Size', str(self.size))
        png_info.add_text('Thumb::Mimetype', self.mime_type)
        png_info.add_text('Software', 'Book Browser')

        return png_info

    ##############################################

    def _make_thumbnail(self, dst_path, size):

        image = Image.open(str(self._source_path))
        image.thumbnail((size, size), resample=self.SAMPLING)
        png_info = self._make_png_info()
        image.save(str(dst_path), 'PNG', pnginfo=png_info)

    ##############################################

    def _make_normal_thumbnail(self):
        self._make_thumbnail(self.normal_path, self._cache.NORMAL_SIZE)

    def _make_large_thumbnail(self):
        self._make_thumbnail(self.large_path, self._cache.LARGE_SIZE)

    def _make_xxx_thumbnail(self, is_normal=True):
        if is_normal:
            self._make_normal_thumbnail()
        else:
            self._make_large_thumbnail()

    ##############################################

    def thumbnail(self, is_normal=True):
        # Fixme: mangle x3
        if not self.has_thumbnail(is_normal):
            self._logger.info('Make thumbnail for {}'.format(self._source_path))
            self._make_xxx_thumbnail(is_normal)
        return self.thumbnail_path(is_normal)

    @property
    def normal(self):
        return self.thumbnail(True)

    @property
    def large(self):
        return self.thumbnail(False)

####################################################################################################

class FreeDesktopThumbnailCache:

    """Class to import FreeDesktop Thumbnail Cache"""

    NORMAL_SIZE = 128
    LARGE_SIZE = 256

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

    @property
    def path(self):
        return self._path

    @property
    def normal_path(self):
        return self._normal_path

    @property
    def large_path(self):
        return self._large_path

    ##############################################

    def clear_cache(self):
        # Warning: This command is dangerous !!!
        #! self._logger.info('Clear thumbnail cache {}'.format(self._path))
        #! shutil.rmtree(str(self._path), ignore_errors=True)
        pass

    ##############################################

    def thumbnail_path(self, path, is_normal=True):
        if is_normal:
            cache_path = self._normal_path
        else:
            cache_path = self._large_path
        return cache_path.joinpath(path)

    def normal_thumbnail_path(self, path):
        return self.thumbnail_path(path, True)

    def large_thumbnail_path(self, path):
        return self.thumbnail_path(path, False)

    ##############################################

    def __getitem__(self, path):
        return FreeDesktopThumbnail(self, path)

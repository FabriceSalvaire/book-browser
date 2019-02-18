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

__all__ = [
    'OcrEngine',
]

####################################################################################################

from pathlib import Path
import logging
import os

from PIL import Image

import tesserocr

from BookBrowser.Common.Singleton import SingletonMetaClass

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

try:
    TESSERACT_DATA_PATH = Path(os.environ['TESSDATA_PREFIX'])
except KeyError:
    TESSERACT_DATA_PATH = None

# Fixme: duplicated strings
LANGUAGE_CODE = {
    'en': 'eng',
    'english': 'eng',

    'fr': 'fra',
    'francais': 'fra',
    'français': 'fra',
    'french': 'fra',
}

####################################################################################################

class OcrEngine(metaclass=SingletonMetaClass):

    _logger = _module_logger.getChild('OcrEngine')

    ##############################################

    def __init__(self, data_path=TESSERACT_DATA_PATH):

        self._path = Path(data_path)
        self._logger.info('TESSERACT Data _path {}'.format(self._path))

    ##############################################

    def image_to_text(self, image, language, fake=False):

        self._logger.info('Run OCR engine...')

        if fake:
            import BookBrowser.Common.LoremIpsum as Lorem
            return Lorem.lorem_ipsum_20

        # Fixme: np
        image = Image.fromarray(image).convert('L')

        language_code = LANGUAGE_CODE[language.lower()]
        text = tesserocr.image_to_text(image, path=str(self._path), lang=language_code)

        self._logger.info('OCR done')

        return text

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

__all__ = ['BookLibrary']

####################################################################################################

from pathlib import Path
import logging
import os

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class BookLibrary:

    _logger = _module_logger.getChild('BookLibrary')

    ##############################################

    def __init__(self, path):

        self._path = Path(str(path)).resolve()

    ##############################################

    def scan(self):

        root_path = str(self._path)
        for path, directories, files in os.walk(root_path):
            for directory in directories:
                book_path = Path(path).joinpath(directory)
                self._logger.info('Directory {}'.format(book_path))

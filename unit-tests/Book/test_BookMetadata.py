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

####################################################################################################

from pathlib import Path
import tempfile
import unittest

from BookBrowser.Book.BookMetadata import *

####################################################################################################

class TestBookMetadata(unittest.TestCase):

    ##############################################

    def test(self):

        with tempfile.TemporaryDirectory() as tmp_directory:

            metadata = BookMetadata()
            metadata.title = 'A title'
            metadata.authors = ('John Doe', 'Pierre Paul')

            json_path = Path(tmp_directory).joinpath('book.json')
            metadata.save_json(json_path)
            with open(json_path, 'r') as fh:
                print(fh.read())

            metadata2 = BookMetadata.load_json(json_path)
            self.assertEqual(metadata2.title, metadata.title)

####################################################################################################

if __name__ == '__main__':
    unittest.main()

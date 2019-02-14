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
    'ApplicationMetadata',
]

####################################################################################################

from BookBrowser import __version__

####################################################################################################

_about_message_template = '''
<h1>Book Browser</h1>

<p>Version: {0.version}</p>

<p>Home Page: <a href="{0.url}">{0.url}</a></p>

<p>Copyright (C) {0.year} Fabrice Salvaire</p>

<h2>Therms</h2>

<p>This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</p>

<p>This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.</p>

<p>You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>. </p>
'''

####################################################################################################

class ApplicationMetadata:

    organisation_name = 'Fabrice Salvaire'
    organisation_domain = 'fabrice-salvaire.fr'

    name = 'BookBrowser'
    display_name = 'BookBrowser — A Book Scanner and Reader Application'

    version = str(__version__)

    year = 2019

    url = 'https://github.com/FabriceSalvaire/book-browser'

    ##############################################

    @classmethod
    def about_message(cls):
        return _about_message_template.format(cls)

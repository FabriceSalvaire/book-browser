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

__all__ = ['about_message']

####################################################################################################

from BookBrowser import __version__

####################################################################################################

about_message_template = '''
<h1>Book Browser</h1>

<p>Version: {version}</p>

<p>Home Page: <a href="{url}">{url}</a></p>

<p>Copyright (C) {year} Fabrice Salvaire</p>

<h2>Therms</h2>

<p>This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</p>

<p>This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.</p>

<p>You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>. </p>
'''

####################################################################################################

def about_message():
    return about_message_template.format(
        version=__version__,
        url='https://github.com/FabriceSalvaire/book-browser',
        year=2019,
    )

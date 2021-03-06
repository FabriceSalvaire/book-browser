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

__all__ = [
    'Shortcuts',
    'ExternalProgram',
]

####################################################################################################

from pathlib import Path

from PyQt5.QtCore import QCoreApplication

from BookBrowser.Config import ConfigInstall

####################################################################################################

class Shortcuts:

    previous_page = QCoreApplication.translate('shortcut', 'Previous page'), 'Backspace'
    next_page = QCoreApplication.translate('shortcut', 'Next page'), 'n' # Space
    flip_page = QCoreApplication.translate('shortcut', 'Flip page'), 'r'
    fit_to_screen = QCoreApplication.translate('shortcut', 'Fit to screen'), 'f'
    full_zoom = QCoreApplication.translate('shortcut', 'Full Zoom'), 'z'
    # open_page_in_external_program = QCoreApplication.translate('shortcut', 'Open in External Program'), ''
    # apply_filter_on_page = QCoreApplication.translate('shortcut', 'Apply Filter on Page'), ''

####################################################################################################

class ExternalProgram:

    if ConfigInstall.OS.on_linux:
        gimp = Path('/usr', 'bin', 'gimp')

    else:
        gimp = None

    default = gimp

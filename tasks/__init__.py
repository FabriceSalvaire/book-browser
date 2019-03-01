####################################################################################################
#
# BookBrowser - A Digitised Book Solution
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

# http://www.pyinvoke.org

####################################################################################################

from invoke import task, Collection
 # import sys

####################################################################################################

from . import clean
from . import doc
from . import release

ns = Collection()
ns.add_collection(Collection.from_module(clean))
ns.add_collection(Collection.from_module(release))
ns.add_collection(Collection.from_module(doc))

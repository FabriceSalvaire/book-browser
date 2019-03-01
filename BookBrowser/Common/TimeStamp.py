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

__all__ = [
    'TimeStamp',
    'TimeStampMixin',
]

####################################################################################################

from atomiclong import AtomicLong

####################################################################################################

class TimeStamp:

    """Class to implement timestamp"""

    _time_stamp = AtomicLong(0)

    ##############################################

    def __init__(self):
        self._modified_time = 0

    ##############################################

    def __repr__(self):
        return 'TS {}'.format(self._modified_time)

    ##############################################

    def __lt__(self, other):
        return self._modified_time < other.modified_time

    ##############################################

    def __gt__(self, other):
        return self._modified_time > other.modified_time

    ##############################################

    def __int__(self):
        return self._modified_time

    ##############################################

    def modified(self):

        # Should be atomic
        TimeStamp._time_stamp += 1
        self._modified_time = TimeStamp._time_stamp.value

####################################################################################################

class TimeStampMixin:

    """Mixin to add timestamp to an object"""

     ##############################################

    def __init__(self):
        self._modified_time = TimeStamp()

    ##############################################

    @property
    def modified_time(self):
        return int(self._modified_time)

    ##############################################

    def modified(self):
        self._modified_time.modified()

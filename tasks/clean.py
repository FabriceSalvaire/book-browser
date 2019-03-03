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

####################################################################################################

from invoke import task

####################################################################################################

@task
def clean_flycheck(ctx):
    with ctx.cd(ctx.Package):
        ctx.run('find . -name "flycheck*.py" -exec rm {} \;')

@task
def clean_emacs_backup(ctx):
    ctx.run('find . -name "*~" -type f -exec rm -f {} \;')

@task(clean_flycheck, clean_emacs_backup)
def clean(ctx):
    pass

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

from invoke import task

####################################################################################################

STANDARD_PACKAGES = (
    'argparse',
    'atexit',
    'datetime',
    'hashlib',
    'importlib',
    'json',
    'logging',
    'operator',
    'os',
    'pathlib',
    'shutil',
    'signal',
    'stat',
    'subprocess',
    'sys',
    'time',
    'traceback',
)

@task()
def show_import(ctx):
    package = 'BookBrowser'
    with ctx.cd(package):
        result = ctx.run("grep -r -h -E  '^(import|from) [a-zA-Z]' . | sort | uniq", hide='out')
    imports = set()
    for line in result.stdout.split('\n'):
        if line.startswith('from'):
            position = line.find('import')
            line = line[5:position]
        elif line.startswith('import'):
            line = line[7:]
        # print('|{}|'.format(line))
        position = line.find('.')
        if position != -1:
            line = line[:position]
        line = line.strip()
        if line:
            imports.add(line)
    imports -= set(STANDARD_PACKAGES)
    imports -= set((package,))
    for item in sorted(imports):
        print(item)

@task
def find_package(ctx, name):
    ctx.run('pip freeze | grep -i {}'.format(name))

####################################################################################################

@task()
def update_git_sha(ctx):
    result = ctx.run('git describe --tags --abbrev=0 --always', hide='out')
    sha = result.stdout.strip()
    filename = 'RadioCrawler/__init__.py'
    with open(filename + '.in', 'r') as fh:
        lines = fh.readlines()
    with open(filename, 'w') as fh:
        for line in lines:
            if '@' in line:
                line = line.replace('@GIT_SHA@', sha)
            fh.write(line)

####################################################################################################

def show_python_site(ctx):
    ctx.run('python3 -m site')

@task(update_git_sha)
def build(ctx):
    ctx.run('python3 setup.py build')

@task(build)
def install(ctx):
    ctx.run('python3 setup.py install')

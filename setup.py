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
import glob
import sys
import os

from setuptools import setup, find_packages
setuptools_available = True

####################################################################################################

if sys.version_info < (3,):
    print('BookBrowser requires Python 3', file=sys.stderr)
    sys.exit(1)

exec(compile(open('setup_data.py').read(), 'setup_data.py', 'exec'))

####################################################################################################

def read_requirement():
    return [requirement.strip() for requirement in open('requirements.txt').readlines()]

####################################################################################################

qml_path = Path('BookBrowser', 'QtApplication', 'qml')
data_files = []
for directory_path, sub_directories, filenames in os.walk(qml_path):
    path = Path(directory_path)
    qml_files = []
    for filename in filenames:
        if filename == 'qmldir' or filename.endswith('.qml'):
            file_path = str(path.joinpath(filename))
            qml_files.append(file_path)
    data_files.append((str(path), qml_files))

####################################################################################################

setup_dict.update(dict(
    # include_package_data=True, # Look in MANIFEST.in
    packages=find_packages(exclude=['unit-test']),
    scripts=glob.glob('bin/*'),
    # [
    #     'bin/...',
    # ],
    package_data={
        'BookBrowser.Config': ['logging.yml'],
    },
    data_files=data_files,
    platforms='any',
    zip_safe=False, # due to data files

    # cf. http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Topic :: Office/Business',
        'Intended Audience :: End Users/Desktop',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        ],

    install_requires=read_requirement(),
))

####################################################################################################

setup(**setup_dict)

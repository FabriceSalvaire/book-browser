.. include:: project-links.txt
.. include:: abbreviation.txt

.. _installation-page:

==============
 Installation
==============

On Windows
----------

Firstly, you have to install the `Anaconda Distribution <https://www.anaconda.com/download/>`_ so
as to get a full featured Python 3 environment.

Then open the `Anaconda Navigator <https://docs.continuum.io/anaconda/navigator/>`_ and launch a console for your root environment.

You can now run *pip* to install BookBrowser in your root environment using this command:

.. code-block:: sh

  pip install BookBrowser

On Linux
--------

Firstly, you have to install Python 3 from your distribution.

Then you can install BookBrowser using *pip* or from source. See supra.

On OSX
------

There are several ways to get Python on OSX:

 * use the built in Python
 * install `Miniconda <https://conda.io/miniconda.html>`_
 * install the `Anaconda Distribution <https://www.anaconda.com/download/>`_.
 * install from Brew `brew install python3` **(reported to work)**

You can install BookBrowser using *pip* or from source. See supra.

Installation from PyPi Repository
---------------------------------

BookBrowser is available on the Python Packages |Pypi|_ repository at |BookBrowser@pypi|

Run this command in the console to install the latest release:

.. code-block:: sh

  pip install BookBrowser

Install a more recent version from Github
-----------------------------------------

If you want to install a version which is not yet released on Pypi, you can use one of theses
commands to install the stable or devel branch:

.. code-block:: sh

  pip install git+https://github.com/FabriceSalvaire/BookBrowser

  pip install git+https://github.com/FabriceSalvaire/BookBrowser@devel

Installation from Source
------------------------

The BookBrowser source code is hosted at |BookBrowser@github|

.. add link to pages ...

You have to solution to get the source code, the first one is to clone the repository, but if you
are not familiar with Git then you can simply download an archive either from the BookBrowser Pypi page
(at the bottom) or the GitHub page (see clone or download button).

To clone the Git repository, run this command in a console:

.. code-block:: sh

  git clone https://github.com/FabriceSalvaire/BookBrowser.git

Then to build and install BookBrowser run these commands:

.. code-block:: sh

  python setup.py build
  python setup.py install

Dependencies
------------

See *requirements.txt* file for normal installation and *requirements-dev.txt* to regenerate the package.

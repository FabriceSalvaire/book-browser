.. -*- Mode: rst -*-

.. -*- Mode: rst -*-

..
   |BookBrowserUrl|
   |BookBrowserHomePage|_
   |BookBrowserDoc|_
   |BookBrowser@github|_
   |BookBrowser@readthedocs|_
   |BookBrowser@readthedocs-badge|
   |BookBrowser@pypi|_

.. |ohloh| image:: https://www.openhub.net/accounts/230426/widgets/account_tiny.gif
   :target: https://www.openhub.net/accounts/fabricesalvaire
   :alt: Fabrice Salvaire's Ohloh profile
   :height: 15px
   :width:  80px

.. |BookBrowserUrl| replace:: https://github.com/FabriceSalvaire/book-browser

.. |BookBrowserHomePage| replace:: BookBrowser Home Page
.. _BookBrowserHomePage: https://github.com/FabriceSalvaire/book-browser

.. |BookBrowser@readthedocs-badge| image:: https://readthedocs.org/projects/BookBrowser/badge/?version=latest
   :target: http://BookBrowser.readthedocs.org/en/latest

.. |BookBrowser@github| replace:: https://github.com/FabriceSalvaire/BookBrowser
.. .. _BookBrowser@github: https://github.com/FabriceSalvaire/BookBrowser

.. |BookBrowser@pypi| replace:: https://pypi.python.org/pypi/BookBrowser
.. .. _BookBrowser@pypi: https://pypi.python.org/pypi/BookBrowser

.. |Build Status| image:: https://travis-ci.org/FabriceSalvaire/BookBrowser.svg?branch=master
   :target: https://travis-ci.org/FabriceSalvaire/BookBrowser
   :alt: BookBrowser build status @travis-ci.org

.. |Pypi Version| image:: https://img.shields.io/pypi/v/BookBrowser.svg
   :target: https://pypi.python.org/pypi/BookBrowser
   :alt: BookBrowser last version

.. |Pypi License| image:: https://img.shields.io/pypi/l/BookBrowser.svg
   :target: https://pypi.python.org/pypi/BookBrowser
   :alt: BookBrowser license

.. |Pypi Python Version| image:: https://img.shields.io/pypi/pyversions/BookBrowser.svg
   :target: https://pypi.python.org/pypi/BookBrowser
   :alt: BookBrowser python version

..  coverage test
..  https://img.shields.io/pypi/status/Django.svg
..  https://img.shields.io/github/stars/badges/shields.svg?style=social&label=Star
.. -*- Mode: rst -*-

.. |Python| replace:: Python
.. _Python: http://python.org

.. |PyPI| replace:: PyPI
.. _PyPI: https://pypi.python.org/pypi

.. |Numpy| replace:: Numpy
.. _Numpy: http://www.numpy.org

.. |IPython| replace:: IPython
.. _IPython: http://ipython.org

.. |Sphinx| replace:: Sphinx
.. _Sphinx: http://sphinx-doc.org

.. |PyInsane| replace:: PyInsane 2
.. _PyInsane: https://gitlab.gnome.org/World/OpenPaperwork/pyinsane

.. |SANE| replace:: SANE
.. _SANE: http://www.sane-project.org>

.. |WIA| replace:: WIA
.. _WIA: https://docs.microsoft.com/en-us/windows/desktop/wia/-wia-startpage

.. |FreeDesktopThumbnail| replace:: Free Desktop Thumbnail
.. _FreeDesktopThumbnail: https://specifications.freedesktop.org/thumbnail-spec/thumbnail-spec-latest.html

.. |Tesseract| replace:: Tesseract
.. _Tesseract: https://github.com/tesseract-ocr

.. |Qt| replace:: Qt
.. _Qt: https://www.qt.io

.. |HDF5| replace:: HDF5
.. _HDF5: https://www.hdfgroup.org/solutions/hdf5

.. |PDF| replace:: PDF
.. _PDF: https://en.wikipedia.org/wiki/PDF
.. https://www.iso.org/standard/63534.html

.. |JSON| replace:: JSON
.. _JSON: https://www.json.org

.. |NoSQL| replace:: NoSQL
.. _NoSQL: https://en.wikipedia.org/wiki/NoSQL

.. |SQLite| replace:: SQLite
.. _SQLite: https://www.sqlite.org

=============
 BookBrowser
=============

|Pypi License|
|Pypi Python Version|

|Pypi Version|

* Quick Link to `Production Branch <https://github.com/FabriceSalvaire/BookBrowser/tree/master>`_
* Quick Link to `Devel Branch <https://github.com/FabriceSalvaire/BookBrowser/tree/devel>`_

Overview
========

What is BookBrowser ?
---------------------

**BookBrowser** is a full solution for **book digitalisation**.  The desktop application provides an
**interface to digitise a book** using any scanner device, an **interface to manage a digitised book
library** and **an interface to read digitised books** on screen.

BookBrowser can be used to archive any paper documents to a numerical support or simply transform
some kilo of papers to Go of space disks.

**BookBrowser is multi-platforms and features:**

.. short list !

* A **digitised book library** showing book covers
* A **scanner interface** similar to XSane and featuring a timer to estimate the scan process time (supports |Sane|_ and |WIA|_)
* A book metadata editor to define title etc.
* A pane showing **page thumbnails**
* A **page viewer** which permits to navigate, zoom and fix page orientation
* Pages can be converted to text using the |Tesseract| Open Source OCR Engine
* supports |FreeDesktopThumbnail|_

**Implementation details:**

BookBrowser is written in |Python|_ and the user interface is based on the |Qt|_ framework.
BookBrowser can thus run on desktop platform like Linux, OSX and Windows, as well as on some
embedded devices.

Where is the Documentation ?
----------------------------

The documentation is available on the |BookBrowserHomePage|_.

How to install it ?
-------------------

Look at the `installation <@project_url@/installation.html>`_ section in the documentation.

Credits
=======

Authors: `Fabrice Salvaire <http://fabrice-salvaire.fr>`_

News
====

.. -*- Mode: rst -*-


.. no title here

V0 2019-01-01
---------------

Started project

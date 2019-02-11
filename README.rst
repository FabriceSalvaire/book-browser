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

.. |BookBrowserUrl| replace:: @https://github.com/FabriceSalvaire/book-browser@

.. |BookBrowserHomePage| replace:: BookBrowser Home Page
.. _BookBrowserHomePage: @https://github.com/FabriceSalvaire/book-browser@

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

**BookBrowser** is an application to **scan and read book** (*) where pages are stored as images on
disk.  (*) *A book is just any paper document of several pages.*

It is an alternative to pack the page's images to a huge PDF file.

It also acts as a post-scanning tool to fix orientation, skipped and rescanned pages.

**BookBrowser is multi-platforms and features:**

* A summary pane showing **page thumbnails** (supporting |FreeDesktopThumbnail|_)
* A **page viewer** which permits to navigate, zoom and fix page orientation
* A **scanner interface** similar to XSane and featuring a timer to estimate the scan process time (gsupporting |Sane|_ and |WIA|_)
* It implements a file system watcher in order to show a newer page.

BookBrowser also provides a **command line tool**

* to rename the images to fix page numbers,
* to guess the page orientation.

**Implementation details:**

The page orientation recto/verso can be mangled in the file name by a flag.  This feature permits to
keep raw data and avoid several image flips due to errors.  It is also a fast way to set the page
orientation from a page by alternating the flag and just updating the directory on disk.  Pages are
rendered in the right orientation by a basic GPU shader.

.. in the automatic orientation detection algorithm

BookBrowser is written in **Python 3** and the user interface is based on the **Qt5 QML Controls 2**
framework.  The code base could be plugged to a web application.

Where is the Documentation ?
----------------------------

The documentation is available on the |BookBrowserHomePage|_.

What are the main features ?
----------------------------

* to be completed

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

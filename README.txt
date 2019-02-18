.. -*- Mode: rst -*-

.. include:: project-links.txt
.. include:: abbreviation.txt

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

.. include:: news.txt

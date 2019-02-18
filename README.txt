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

**BookBrowser** is an application **to digitise books** using a scanner device, to manage a
**digitised book library** and **read digitised books** on screen.

BookBrowser can be used to archive any paper documents to a numerical support or simply transform
some kilo of papers to Go of space disks.

**BookBrowser is multi-platforms and features:**

* A **digitised book library** manager showing book covers
* A **scanner interface** similar to XSane and featuring a timer to estimate the scan process time (supports |Sane|_ and |WIA|_)
* A book metadata editor to define title etc.
* A summary pane showing **page thumbnails** (supports |FreeDesktopThumbnail|_)
* A **page viewer** which permits to navigate, zoom and fix page orientation
* Pages can be converted to text using the |Tesseract| Open Source OCR Engine

..  It also implements a file system watcher in order to show a newer page.

BookBrowser also provides a **command line tool** to perform some tasks like:

* rename images to fix page numbers,
* guess page orientation.

**Implementation details:**

BookBrowser is written in |Python|_ and the user interface is based on the |Qt|_ framework.
BookBrowser can thus run on desktop platform like Linux, OSX and Windows, as well as on some
embedded devices.

The graphical interfaced coded on QML is portable and parts of the Python code base could be
rewritten in C++ to make a full Qt application which could run on any platform supported by the Qt
framework, like Android or IOS.

BookBrowser is designed so as to be splitted as a client-server architecture where the client could
be a Python, C++ or web frontend.  This design is made easier by the fact QML supports network
transparency by using URLs.

For example, if you want to restrict that lambda users disseminate digitised books all around then a
Qt frontend is an alternative to a web application, since it would be necessary to hack the frontend
to save data.

BookBrowser stores pages as images on disk.  It is an alternative to pack the page's images to a
huge PDF file.  Since BookBrowser acts as a post-scanning tool to fix orientation, skipped or
rescanned pages and to crop image, theses post-scanning tasks are made easier if we keep raw data.
For example, the page orientation recto/verso can be mangled in the file name by a flag.  This
feature permits to keep raw data and avoid several image flips due to mistakes.  It is also a fast
way to set the page orientation from a page by alternating the flag and just updating the directory
on disk.  Pages are rendered in the right orientation by a basic GPU shader.

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

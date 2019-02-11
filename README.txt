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

.. include:: news.txt

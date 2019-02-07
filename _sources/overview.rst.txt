.. include:: abbreviation.txt
.. include:: project-links.txt

.. _overview-page:

==========
 Overview
==========

What is BookBrowser ?
---------------------

BookBrowser is a small application to read scanned books where the pages are stored as an image on
disk.  It is an alternative to pack the images to a huge PDF file.  It also acts as a post-scanning
tool to fix orientation, skipped and rescanned pages.

BookBrowser provides a command line tool

* to rename the images to fix the page number,
* to guess the page orientation.

The page orientation recto/verso is mangled in the file name. This feature permits to keep raw data
and avoid several image flips due to errors in the automatic orientation detection algorithm.

BookBrowser implements a file system watcher in order to show a newer page.

BookBrowser is written in Python 3 and the user interface is based on the Qt5 QML framework.  The
code base could also be plugged to a web application.

How is BookBrowser licensed ?
-----------------------------

BookBrowser is licensed under the `GPLv3 <https://www.gnu.org/licenses/quick-guide-gplv3.en.html>`_.

Going further with BookBrowser
------------------------------

The best way to know what you can do with BookBrowser, and to learn it, is to look at the examples:

 * :ref:`BookBrowser Reference Manual <reference-manual-page>`

.. * :ref:`Bibliography <bibliography-page>`

Which platforms are supported by BookBrowser ?
----------------------------------------------

BookBrowser runs on Linux, Windows 64-bit and Mac OS X.

How to install BookBrowser ?
----------------------------

The procedure to install BookBrowser is described in the :ref:`Installation Manual <installation-page>`.

Which version of Python is required ?
-------------------------------------

BookBrowser requires Python 3 and the version 3.7 is recommended.

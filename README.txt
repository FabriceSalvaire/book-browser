.. -*- Mode: rst -*-

.. include:: project-links.txt
.. include:: abbreviation.txt

============
 BookBrowser
============

|Pypi License|
|Pypi Python Version|

|Pypi Version|

* Quick Link to `Production Branch <https://github.com/FabriceSalvaire/BookBrowser/tree/master>`_
* Quick Link to `Devel Branch <https://github.com/FabriceSalvaire/BookBrowser/tree/devel>`_

Overview
========

What is BookBrowser ?
---------------------

BookBrowser is a small application to read scanned book where the pages are stored as an image on
disk.  It is an alternative to pack the images to a huge PDF file.

BookBrowser provides a command line tool

* to rename the images to fix the page number,
* to guess the orientation.

The page orientation recto/verso is mangled in the file name. This feature permits to keep raw data
and avoid several image flips due to error in the automatic orientation detection algorithm.

BookBrowser is written in Python 3 and the user interface is based on the Qt5 QML framework.

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

.. include:: abbreviation.txt

.. _design-note-page:

==============
 Design Notes
==============

BookBrowser is written in |Python|_ and the user interface is based on the |Qt|_ framework.
BookBrowser can thus run on desktop platform like Linux, OSX and Windows, as well as on some
embedded devices.

The graphical interfaced coded on QML is portable and parts of the Python code base could be
rewritten in C++ to make a full Qt application which could run on any platform supported by the Qt
framework, like Android or IOS.

BookBrowser is designed so as to be splitted as a client-server architecture where the client could
be a Python, C++ or web frontend.  This design is made easier by the fact QML supports network
transparency.

For example, if you want to prevent lambda users from distributing digitised books then a Qt
frontend is an alternative to a web application, since it would be necessary to hack the frontend to
save data.

.. see FAQ Why a Qt User Interface instead of a web application ?


General Code Design
===================

The code is divided in three parts

* a core part written in Python which implement things like book, page, etc. This part is Qt unaware.
* a Python-QML interface which implements QObject based classes to wrap the core API to QML.
* a QML user interface written in QML and a bit of Javascript snippets.

This design must maintain a clear separation between the roles of each part.  The first one, the
core part, corresponds to the backend.  While the two others make the Qt frontend.


Discussion on data storage
==========================

This section discusses the different way to store data.  The choice of a solution is mainly driven
by the cost of the solution for a particular need.

Page images can be stored in several ways, for example:

* as image on disk,
* as a |PDF|_ file,
* as a |HDF5|_ file,
* in a NoSQL database.

There is mainly three forms of storage: as plain images, as images stored in a container or a
database.

The image and PDF format have the advantage to be portable.

And the image format has the advantage to be easier and fast to update.  In addition images can be
served by a HTTP server like `nginx <http://nginx.org>`_.

Book metadata can be stored in several ways:

* as a |JSON|_ file,
* in a |SQLite|_, SQL or |NoSQL|_ database.


Page Image Format
=================

BookBrowser stores scanned pages as images on disk.  It is an alternative to pack the page images to
a large PDF file.

Since BookBrowser acts as a post-scanning tool to fix orientation, skipped or rescanned pages and to
crop image, theses post-scanning tasks are made easier if we keep raw data.

For example, the page orientation recto/verso can be mangled in the file name by a flag.  This
feature permits to keep raw data and avoid several image flips due to mistakes.  It is also a fast
way to set the page orientation from a page by alternating the flag and just updating the directory
on disk.  Pages are rendered in the right orientation by a basic GPU shader.


Free Desktop Thumbnail Managing Standard
========================================

The `Free Desktop Thumbnail Managing Standard
<https://specifications.freedesktop.org/thumbnail-spec/thumbnail-spec-latest.html>`_ is quite simple but has some issues:

* It doesn't implement a magic middleware.
* It can collect confidential data in a cache directory : dig all my life feature.
* There is no garbage collection until user is running a thumbnail aware application like a file browser.

  * The thumbnail directory can use a significant space disk.
  * It requires some maintenance to recover space disk, like to run a garbage collecting daemon or
    simply manually delete the thumbnail cache.
  * The lack of garbage collection is due to performance reason (file system watching).

.. _design-note-page:

==============
 Design Notes
==============

General Code Design
===================

The code is splitted in three parts

* a core part written in Python which implement things like book, page
* a Python-QML interface which provides QObject classes to wrap the core API to QML
* a QML user interface written in QML / Javascript

This design must maintain a clear separation between the roles of each part.

Free Desktop Thumbnail Managing Standard
========================================

The `Free Desktop Thumbnail Managing Standard
<https://specifications.freedesktop.org/thumbnail-spec/thumbnail-spec-latest.html>`_ is quite simple but has some issues:

* It doesn't implement a middleware.
* It can collect confidential data in a cache directory : dig all my life feature.
* There is no garbage collecting.

  * The thumbnail directory can use a significant disk space.
  * Thumbnail must be renamed if the source is renamed.
  * Thumbnail must be regenerated if the source is changed.

.. Wrong: * We cannot retrieve the path of the source file from the MD5 hash.

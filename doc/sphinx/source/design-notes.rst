.. _design-note-page:

==============
 Design Notes
==============

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

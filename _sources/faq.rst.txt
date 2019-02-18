.. include:: project-links.txt
.. include:: abbreviation.txt

.. _user-faq-page:

==========
 User FAQ
==========

How to get help or report an issue ?
------------------------------------

There is no mailing list or forum actually, so you can either contact me or fill an issue on Github.

.. If you want to **discuss or ask questions on BookBrowser**, you can subscribe and post messages
   on the **BookBrowser User** mailing list.

.. There is actually three lists running on Google Groups (*):

.. `User List <https://groups.google.com/forum/#!forum/BookBrowser-user>`_
..  List for BookBrowser users
.. `Announce List <https://groups.google.com/forum/#!forum/BookBrowser-announce>`_
..  List for announcements regarding BookBrowser releases and development
.. `Devel List <https://groups.google.com/forum/#!forum/BookBrowser-devel>`_
..  List for developers of BookBrowser

**If you encounter an issue, please fill an issue** on the `Issue Tracker <https://github.com/FabriceSalvaire/BookBrowser/issues>`_.

.. (*) Despite Google Groups has many drawbacks, I don't have actually enough resources to run GNU Mailman or
   Discourse on my own IT infrastructure.

Why a Qt User Interface instead of a web application ?
------------------------------------------------------

A web application could be an option for such software.

However it is easier to make a scanner interface on a desktop application, since a web application
would requires either a browser API or a server running on the machine.  Another solution would be
to use a framework such as `Electron <https://electronjs.org>`_ with a scanner API and try to share
code between a web and desktop application.

In addition Qt QML code tends to be cleaner, easier to maintain, and run faster.  While a web
application has a more powerful style engine but at the cost of increased complexity.

Desktop applications also have the advantage of being less open, while web browser implement a
development interface.  It is a nice feature if you want to prevent lambda users from distributing
digitised books, because it is necessary to hack the frontend to save data.

Why Python instead of C++ ?
---------------------------

Simply because it is faster to develop and maintain a Python code, at the cost of a bit slower and
less portable application.  However parts of the Python code could be rewritten in modern C++
without much difficulty.

Why not store digitised book in a PDF ?
---------------------------------------

PDF format is able to store page as image at the cost of a large file.  But it has the advantage of
being a portable container.

.. to be  vs  of being  american ???

However a PDF is only a good approach when the digitisation process is completely achieved and we
don't expect to modify the content afterwards.  While a page image on disk is easier and faster to
update.

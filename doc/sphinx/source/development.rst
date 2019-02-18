.. _development-page:

=========================
 Development & Community
=========================

BookBrowser is an open-source project, and relies on its community of users to keep getting better.

BookBrowser source code and issues are managed on `Github <https://github.com/FabriceSalvaire/BookBrowser>`_.

How you can help ?
------------------

As an open source project, anyone is welcome to contribute in whatever form they are able.

.. , which can include taking part in discussions, filing bug reports, proposing improvements,
   contributing code or documentation, and testing it.

* Promote BookBrowser on the web and all around you
* Fill bug reports
* Test BookBrowser on Linux, Windows and OS X
* Check for errors on the documentation
* Propose improvements
* Implement missing features

Contributors
------------

The list of contributors is available at https://github.com/FabriceSalvaire/BookBrowser/graphs/contributors

How to hack or debug the application ?
--------------------------------------

The application has a :code:`--fake-scanner` option to simulate a fake scanner while working on the
application, this prevent to wait SANE initialise and to use a real scanner device just for tests.

You can use the environment variable **QT_QUICK_CONTROLS_STYLE** to set the Qt style, see
https://doc.qt.io/qt-5.12/qtquickcontrols2-styles.html#environment-variable for more details.

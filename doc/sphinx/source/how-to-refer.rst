.. _how-to-refer-page:

===============================
 How to Refer to BookBrowser ?
===============================

Up to now, the official url for BookBrowser is @project_url@

*A permanent redirection will be implemented if the domain change in the future.*

On Github, you can use the **BookBrowser** `topic <https://github.com/search?q=topic%3ABookBrowser&type=Repositories>`_ for repository related to BookBrowser.

A typical `BibTeX <https://en.wikipedia.org/wiki/BibTeX>`_ citation would be, for example:

.. code:: bibtex

    @software{BookBrowser,
      author = {Fabrice Salvaire}, % actual author and maintainer
      title = {BookBrowser},
      url = {@project_url@},
      version = {x.y},
      date = {yyyy-mm-dd}, % set to the release date
    }

    @Misc{BookBrowser,
      author = {Fabrice Salvaire},
      title = {BookBrowser},
      howpublished = {\url{@project_url@}},
      year = {yyyy}
    }

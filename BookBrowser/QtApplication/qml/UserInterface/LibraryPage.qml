/***************************************************************************************************
 *
 *  Copyright (C) 2019 Fabrice Salvaire
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 ***************************************************************************************************/

import QtQuick 2.11
import QtQuick.Controls 2.4

import BookBrowser 1.0
import Widgets 1.0 as Widgets

Page {
    id: root

    /*******************************************************
     *
     * API
     *
     */

    /******************************************************/

    Widgets.BookCoverViewer {
        id: book_cover_viewer
        anchors.fill: parent

        books_model: application.library.books

       // onShow_page: {
       //     page_viewer.to_page(page_number)
       //     stack_layout.set_viewer_page()
       // }
    }
}

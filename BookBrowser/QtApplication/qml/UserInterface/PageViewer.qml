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

import BookBrowser 1.0
import Widgets 1.0 as Widgets

Widgets.ImageViewer {

    /*******************************************************
     *
     * API
     *
     */

    property var book_page

    signal page_changed() // int page_number

    function first_page() {
        book_page = book.first_page
        page_changed()
    }

    function last_page() {
        book_page = book.last_page
        page_changed()
    }

    function to_page(page_number) {
        if (book.is_valid_page_number(page_number)) {
            book_page = book.page(page_number)
            page_changed()
        }
    }

    function prev_page() {
        to_page(book_page.page_number -1)
    }

    function next_page() {
        to_page(book_page.page_number +1)
    }

    function flip() {
        var orientation
        if (rotation == 0) {
            rotation = 180
            orientation = 'v'
        }
        else {
            rotation = 0
            orientation = 'r'
        }
        book_page.flip_page(orientation)
    }

    function set_recto() {
        book_page.flip_page('r')
    }

    function set_verso() {
        book_page.flip_page('v')
    }

    function flip_from_page() {
        book.flip_from_page(book_page, 'v')
    }

    /******************************************************/

    id: page_viewer

    property var book: application.book

    image_source: book_page ? book_page.path : ''
    image_rotation: book_page ? book_page.orientation : 0

    Component.onCompleted: {
        book.new_page.connect(last_page)
    }
}

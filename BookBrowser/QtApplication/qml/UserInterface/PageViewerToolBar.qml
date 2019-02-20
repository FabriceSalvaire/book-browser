/***************************************************************************************************
 *
 *  BookBrowser - A Digitised Book Solution
 *  Copyright (C) 2019 Fabrice Salvaire
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as
 *  published by the Free Software Foundation, either version 3 of the
 *  License, or (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 ***************************************************************************************************/

import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11

import BookBrowser 1.0
import Widgets 1.0 as Widgets

RowLayout {
    id: root

    /*******************************************************
     *
     * API
     *
     */

    property var actions
    property var page_viewer
    property var page_viewer_page

    /******************************************************/

    property var book: application.book

    /******************************************************/

    Widgets.ToolButtonTip {
        icon.name: 'zoom-out-black'
        onClicked: page_viewer.zoom_out()
    }

    Widgets.ToolButtonTip {
        action: actions.fit_to_screen_action
    }

    Widgets.ToolButtonTip {
        action: actions.zoom_full_action
    }

    Widgets.ToolButtonTip {
        icon.name: 'zoom-in-black'
        onClicked: page_viewer.zoom_in()
    }

    Widgets.ToolButtonTip {
        icon.name: 'first-page-black'
        onClicked: page_viewer.first_page()
    }

    Widgets.ToolButtonTip {
        action: actions.prev_page_action
    }

    Widgets.ToolButtonTip {
        action: actions.next_page_action
    }

    Widgets.ToolButtonTip {
        icon.name: 'last-page-black'
        onClicked: page_viewer.last_page()
    }

    SpinBox {
        id: page_number
        editable: true
        from: 1
        to: book.number_of_pages
        value: page_viewer.book_page ? page_viewer.book_page.page_number: 0

        onValueModified: page_viewer.to_page(value)
    }

    Label {
        text: '/' + book.number_of_pages
    }

    Widgets.ToolButtonTip {
        icon.name: 'grid-on-black'
        tip: qsTr('Show grid')
        checkable: true
        onClicked: page_viewer_page.toggle_grid()
    }

    Widgets.ToolButtonTip {
        action: actions.flip_action
        tip: qsTr('Flip page')
    }

    Widgets.ToolButtonTip {
        icon.name: 'recto-page'
        tip: qsTr('Flip page as recto')
        onClicked: page_viewer.set_recto()
    }

    Widgets.ToolButtonTip {
        icon.name: 'verso-page'
        tip: qsTr('Flip page as verso')
        onClicked: page_viewer.set_verso()
    }

    Widgets.ToolButtonTip {
        icon.name: 'flip-from-page'
        tip: qsTr('Flip page from this page')
        onClicked: page_viewer.flip_from_page()
    }


    Widgets.ToolButtonTip {
        icon.name: 'subject-black'
        tip: qsTr('Convert to text using OCR engine')
        onClicked: page_viewer_page.convert_to_text()
    }


    Widgets.ToolButtonTip {
        icon.name: 'oopen-in-new-black'
        tip: qsTr('Open in ...')
        // onClicked: page_viewer_page.
    }
}

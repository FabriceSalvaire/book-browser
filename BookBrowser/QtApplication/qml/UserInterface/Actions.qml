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

Item {
    id: root

    /*******************************************************
     *
     * API
     *
     */

    property var page_viewer
    // application_window.load_book

    /******************************************************/

    property alias fit_to_screen_action: fit_to_screen_action
    property alias flip_action: flip_action
    property alias next_page_action: next_page_action
    property alias prev_page_action: prev_page_action
    property alias reload_action: reload_action
    property alias zoom_full_action:zoom_full_action

    /******************************************************/

    Action {
        id: reload_action
        icon.name: 'refresh-black'
        // shortcut: ''
        onTriggered: load_book(application.book.path)
    }

    Action {
        id: prev_page_action
        icon.name: 'arrow-back-black'
        shortcut: 'Backspace'
        onTriggered: page_viewer.prev_page()
    }

    Action {
        id: next_page_action
        icon.name: 'arrow-forward-black'
        shortcut: 'n' //'Space'
        onTriggered: page_viewer.next_page()
    }

    Action {
        id: flip_action
        icon.name: 'swap-vert-black'
        shortcut: 'r'
        onTriggered: page_viewer.flip()
    }

    Action {
        id: fit_to_screen_action
        icon.name: 'settings-overscan-black'
        shortcut: 'f'
        onTriggered: page_viewer.fit_to_screen()
    }

    Action {
        id: zoom_full_action
        icon.source: 'qrc:/icons/zoom-fit-width.png'
        shortcut: 'z'
        onTriggered: page_viewer.zoom_full()
    }
}

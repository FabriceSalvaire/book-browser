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

// Fixme: push crash sane, image_viewer ???

import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11

import BookBrowser 1.0
import Widgets 1.0 as Widgets
import UserInterface 1.0 as Ui

ApplicationWindow {
    id: application_window
    title: qsTr('Book Viewer') // Fixme: ???
    visible: true

    width: 1000
    height: 500

    property var book: application.book

    Component.onCompleted: {
        console.info('ApplicationWindow.onCompleted')
        application_window.showMaximized()
        page_viewer.first_page()
    }

    /***********************************************************************************************
     *
     * API
     *
     */

    function clear_message() {
        message_label.text = ''
    }

    function show_message(message) {
        message_label.text = message
    }

    function load_book(path) {
        application.load_book(path)
        show_message(qsTr('Loaded book at %1'.arg(path)))
    }

    /***********************************************************************************************
     *
     * Actions
     *
     */

    Ui.Actions {
        id: actions
        // menu_bar: menu_bar
        page_viewer: page_viewer
    }

    /***********************************************************************************************
     *
     * Slots
     *
     */

    onClosing: {
        console.info('Close', close)
        scanner_ui.save()
    }

    /***********************************************************************************************
     *
     * Dialogs
     *
     */

    Widgets.AboutDialog {
        id: about_dialog
        title: qsTr('About Book Browser')
        about_message: application.about_message // qsTr('...')
    }

    // Widgets.BookFolderDialog {
    Widgets.NativeBookFolderDialog {
        id: book_folder_dialog
        onAccepted: {
            var path = selected_path()
            load_book(path)
        }
    }

    /***********************************************************************************************
     *
     * Menu
     *
     */

    // Fixme: use native menu ???
    menuBar: Ui.MenuBar {
        id: menu_bar
        about_dialog: about_dialog
        book_folder_dialog: book_folder_dialog
    }

    /***********************************************************************************************
     *
     * Header
     *
     */

    header: Ui.HeaderToolBar {
        id: header_tool_bar
        actions: actions
        grid: grid
        page_viewer: page_viewer
        page_viewer_page: page_viewer_page
        scanner_ui: scanner_ui
        stack_layout: stack_layout
    }

    /***********************************************************************************************
     *
     * Items
     *
     */

    StackLayout {
        id: stack_layout
        anchors.fill: parent
        currentIndex: 0

        function set_thumbnail_page() { currentIndex = 0 }
        function set_viewer_page() { currentIndex = 1 }
        function set_scanner_page() { currentIndex = 2 }

        Page {
            id: thumbnail_page

            Widgets.ThumbnailViewer {
                id: thumbnail_viewer
                anchors.fill: parent

                thumbnail_model: book.pages

                onShow_page: {
                    page_viewer.to_page(page_number)
                    stack_layout.set_viewer_page()
                }
            }
        }

        Page {
            id: page_viewer_page

            Widgets.PageViewer {
                id: page_viewer
                anchors.fill: parent

                book: application.book
            }

            Widgets.Grid {
                id: grid
                visible: false
                anchors.fill: parent
            }
        }

        Page {
            id: scanner_page

            Widgets.ScannerUI {
                id: scanner_ui
                anchors.fill: parent

                // scanner: application.scanner
            }
        }
    }

    /***********************************************************************************************
     *
     * Footer
     *
     */

    footer: ToolBar {
        RowLayout {
            Label {
                id: message_label
            }
        }
    }
}

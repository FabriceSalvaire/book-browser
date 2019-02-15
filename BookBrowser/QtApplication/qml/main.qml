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


    Component.onCompleted: {
        console.info('ApplicationWindow.onCompleted')
        application_window.showMaximized()
        page_viewer_page.page_viewer.first_page()
    }

    /***********************************************************************************************
     *
     * API
     *
     */

    function clear_message() {
        footer_tool_bar.message = ''
    }

    function show_message(message) {
        footer_tool_bar.message = message
    }

    function load_book(path) {
        application.load_book(path)
        show_message(qsTr('Loaded book at %1'.arg(path)))
    }

    function close_application(close) {
        console.info('Close application')
        show_message(qsTr('Close ...'))
        scanner_page.scanner_ui.save()
        if (!close)
            Qt.quit()
        // else
        //    close.accepted = false
    }

    /***********************************************************************************************
     *
     * Slots
     *
     */

    onClosing: close_application(close)

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
     * Actions
     *
     */

    Ui.Actions {
        id: actions
        page_viewer: page_viewer_page.page_viewer
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
        page_viewer: page_viewer_page.page_viewer
        page_viewer_page: page_viewer_page
        scanner_ui: scanner_page.scanner_ui
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

        Ui.ThumbnailPage {
            id: thumbnail_page
            page_viewer: page_viewer_page.page_viewer
        }

        Ui.PageViewerPage {
            id: page_viewer_page
        }

        Ui.ScannerPage {
            id: scanner_page
        }
    }

    /***********************************************************************************************
     *
     * Footer
     *
     */

    footer: Ui.FooterToolBar {
        id: footer_tool_bar
    }
}

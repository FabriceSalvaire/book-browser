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

// Fixme: push crash sane, image_viewer ???

import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11

import BookBrowser 1.0
import Widgets 1.0 as Widgets
import UserInterface 1.0 as Ui

ApplicationWindow {
    id: application_window

    /*******************************************************
     *
     * API
     *
     */

    function close_application(close) {
        console.info('Close application')
        show_message(qsTr('Close ...'))
        scanner_page.scanner_ui.save()
        if (!close)
            Qt.quit()
        // else
        //    close.accepted = false
    }

    function clear_message() {
        footer_tool_bar.message = ''
    }

    function show_message(message) {
        footer_tool_bar.message = message
    }

    function load_book(path) {
        application.load_book(path)
        stack_layout.set_thumbnail_page()
        show_message(qsTr('Loaded book at %1'.arg(path)))
    }

    /*******************************************************
     *
     *
     */

    title: qsTr('Book Viewer') // Fixme: ???
    visible: true
    width: 1000
    height: 500

    Component.onCompleted: {
        console.info('ApplicationWindow.onCompleted')
        console.info(application.book)
        console.info(application.library)
        application.show_message.connect(on_message)
        application.show_error.connect(on_error)
        application_window.showMaximized()
        page_viewer_page.page_viewer.first_page()
    }

    function on_message(message) {
        error_message_dialog.open_with_message(message)
    }

    function on_error(message, backtrace) {
        var text = message + '\n' + backtrace
        error_message_dialog.open_with_message(text)
    }

    /*******************************************************
     *
     * Slots
     *
     */

    onClosing: close_application(close)

    /*******************************************************
     *
     * Dialogs
     *
     */

    Widgets.AboutDialog {
        id: about_dialog
        title: qsTr('About Book Browser')
        about_message: application.about_message // qsTr('...')
    }

    Widgets.ErrorMessageDialog {
        id: error_message_dialog
        title: qsTr('An error occurred in Book Browser')
    }

    // Widgets.BookFolderDialog {
    Widgets.NativeBookFolderDialog {
        id: book_folder_dialog
        onAccepted: load_book(selected_path())
    }

    Ui.OptionsDialog {
        id: options_dialog
    }

    /*******************************************************
     *
     * Actions
     *
     */

    Ui.Actions {
        id: actions
        page_viewer: page_viewer_page.page_viewer
    }

    /*******************************************************
     *
     * Menu
     *
     */

    // Fixme: use native menu ???
    menuBar: Ui.MenuBar {
        id: menu_bar
        about_dialog: about_dialog
        book_folder_dialog: book_folder_dialog
        options_dialog: options_dialog
    }

    /*******************************************************
     *
     * Header
     *
     */

    header: Ui.HeaderToolBar {
        id: header_tool_bar
        actions: actions
        page_viewer_page: page_viewer_page
        scanner_ui: scanner_page.scanner_ui
        stack_layout: stack_layout
    }

    /*******************************************************
     *
     * Items
     *
     */

    StackLayout {
        id: stack_layout
        anchors.fill: parent

        // enum ApplicationPage {
        //     MetadataPage,
        //     ThumbnailPage,
        //     ViewerPage,
        //     ScannerPage
        // }

        function set_library_page() { currentIndex = 0 }
        function set_metadata_page() { currentIndex = 1 }
        function set_thumbnail_page() { currentIndex = 2 }
        function set_viewer_page() { currentIndex = 3 }
        function set_scanner_page() { currentIndex = 4 }

        Component.onCompleted: {
            if (application.library)
                set_library_page()
            else
                set_thumbnail_page()
        }

        Ui.LibraryPage {
            id: library_page
        }

        Ui.MetadataPage {
            id: metadata_page
        }

        // Fixme: simplify with Page { Widget{} } ???
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

    /*******************************************************
     *
     * Footer
     *
     */

    footer: Ui.FooterToolBar {
        id: footer_tool_bar
    }
}

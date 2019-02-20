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

import Widgets 1.0 as Widgets

Item {

    /*******************************************************
     *
     * API
     *
     */

    function wait_for_page(book_page) {
        _book_page = book_page
        text_area.text = ''
        _processing = true
        visible = true
        _book_page.text_ready.connect(set_text)
        if (_book_page.text)
            set_text()
    }

    function clear_text() {
        // in case ocr is running when user changes the current page
        if (_book_page)
            _book_page.text_ready.disconnect(set_text)
        visible = false
        _processing = false
        text_area.text = ''
        _book_page = null
    }

    /******************************************************/

    id: root

    property var _book_page
    property bool _processing: false

    function set_text() {
        // console.info('OCR is done')
        text_area.text = _book_page.text
        _book_page.text_ready.disconnect(set_text)
        _processing = false
    }

    /******************************************************/

    Widgets.NativeFileDialog {
        id: save_text_file_dialog
        onAccepted: _book_page.save_text(selected_path())
    }

    ScrollView {
        anchors.fill: parent

        TextArea {
            id: text_area
            selectByMouse: true
            textFormat: TextEdit.PlainText
            wrapMode: TextEdit.Wrap
        }
    }

    BusyIndicator {
        anchors.centerIn: parent
        height: Math.min(parent.width, parent.height) * .5
        width: height
        running: root._processing
    }

     Column {
         anchors.top: root.top
         anchors.right: root.right
         anchors.margins: 20
         z: 1
         visible: !root._processing
         spacing: 20

         Widgets.ToolButtonTip {
             icon.name: 'close-black'
             tip: qsTr('close text viewer')
             onClicked: root.visible = false
         }

         Widgets.ToolButtonTip {
             icon.name: 'save-black'
             tip: qsTr('save text to file')
             onClicked: save_text_file_dialog.open()
         }
     }
}

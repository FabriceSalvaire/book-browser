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
import QtQuick.Layouts 1.11

import BookBrowser 1.0
import Widgets 1.0 as Widgets
import '.' 1.0 as Ui

Page {
    id: root

    /*******************************************************
     *
     * API
     *
     */

    property alias page_viewer: page_viewer

    function toggle_grid() {
        grid.visible = !grid.visible
    }

    function convert_to_text() {
        page_text.text = ''
        page_text_container.processing = true
        page_text_container.visible = true
        page_viewer.book_page.text_ready.connect(set_text)
        var text = page_viewer.book_page.text
        if (text)
            set_text()
    }

    function set_text() {
        var text = page_viewer.book_page.text
        // console.info('OCR is done')
        page_text.text = text
        page_viewer.book_page.text_ready.disconnect(set_text)
        page_text_container.processing = false
    }

    /******************************************************/

    // Component.onCompleted {
    // }

    /******************************************************/

    RowLayout {
        anchors.fill: parent

        Ui.PageViewer {
            id: page_viewer
            Layout.fillHeight: true
            Layout.fillWidth: true

            Widgets.Grid {
                id: grid
                anchors.fill: parent
                visible: false
            }
        }

        Item {
            id: page_text_container
            visible: false
            Layout.fillHeight: true
            Layout.preferredWidth: parent.width/2

            property bool processing: false

            Flickable {
                anchors.fill: parent

                TextArea.flickable: TextArea {
                    id: page_text
                    selectByMouse: true
                    textFormat: TextEdit.PlainText
                    wrapMode: TextEdit.Wrap
                }

                ScrollIndicator.vertical: ScrollIndicator { }
                // ScrollIndicator.horizontal: ScrollIndicator { }
            }

            BusyIndicator {
                anchors.centerIn: parent
                height: Math.min(parent.width, parent.height) * .5
                width: height
                running: page_text_container.processing
            }
        }
    }
}

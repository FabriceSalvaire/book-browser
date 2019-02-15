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
import UserInterface 1.0 as Ui

ToolBar {
    id: root

    /*******************************************************
     *
     * API
     *
     */

    property var actions
    property var page_viewer_page
    property var scanner_ui
    property var stack_layout

    /******************************************************/

    property var book: application.book

    // property alias page_viewer: page_viewer_page.page_viewer

    /******************************************************/

    RowLayout {
        anchors.fill: parent
        spacing: 10

        RowLayout {
            Widgets.ToolButtonTip {
                action: actions.reload_action
                tip: qsTr('Reload book')
            }

            Widgets.ToolButtonTip {
                icon.source: 'qrc:/icons/view-comfy-black.png'
                tip: qsTr('Show page thumbnails')
                onClicked: {
                    stack_layout.set_thumbnail_page()
                }
            }
            Widgets.ToolButtonTip {
                icon.source: 'qrc:/icons/image-black.png'
                tip: qsTr('Show page viewer')
                onClicked: {
                    stack_layout.set_viewer_page()
                }
            }
            Widgets.ToolButtonTip {
                icon.source: 'qrc:/icons/scanner-black.png'
                tip: qsTr('Show scanner interface')
                onClicked: {
                    // Fixme:
                    stack_layout.set_scanner_page()
                    scanner_ui.init()
                }
            }
        }

        Ui.PageViewerToolBar {
            visible: page_viewer_page.visible
            actions: root.actions
            page_viewer: root.page_viewer_page.page_viewer
            page_viewer_page: root.page_viewer_page
        }

        Item {
            Layout.fillWidth: true
        }
    }
}

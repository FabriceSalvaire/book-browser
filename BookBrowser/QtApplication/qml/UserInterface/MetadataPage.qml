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

Page {

    /*******************************************************
     *
     * API
     *
     */

    property var metadata: application.book.metadata

    /******************************************************/

    Component.onCompleted: {
    }

    /******************************************************/

    id: root

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20

        Widgets.ToolButtonTip {
            icon.source: 'qrc:/icons/save-black.png'
            tip: qsTr('Save')
        }

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            ScrollBar.horizontal.policy: ScrollBar.AsNeeded

            GridLayout {
                width: parent.width
                columns: 2
                columnSpacing: 10

                Label {
                    text: qsTr('ISBN')
                }
                RowLayout {
                    TextEdit {
                        Layout.fillWidth: true
                        // id:
                    }

                    Widgets.ToolButtonTip {
                        icon.source: 'qrc:/icons/refresh-black.png'
                        tip: qsTr('Reload book')
                    }
                }

                Label {
                    text: qsTr('Path')
                }
                Label {
                    text: metadata.path
                }

                Label {
                    text: qsTr('Title')
                }
                TextEdit {
                    // id:
                }

                Label {
                    text: qsTr('Authors')
                }
                TextEdit {
                    // id:
                }

                Label {
                    text: qsTr('Publisher')
                }
                TextEdit {
                    // id:
                }

                Label {
                    text: qsTr('Language')
                }
                TextEdit {
                    // id:
                }

                Label {
                    text: qsTr('Number of pages')
                }
                SpinBox {
                    // id:
                    from: 1
                    to: 1000
                    // value: metadata.number_of_pages
                }

                Label {
                    text: qsTr('Page Offset')
                }
                SpinBox {
                    // id:
                    from: 1
                    to: 1000
                }

                Label {
                    text: qsTr('Year')
                }
                SpinBox {
                    // id:
                    from: 0
                    to: 2100
                }

                Label {
                    text: qsTr('Keywords')
                }
                TextEdit {
                    // id:
                }

                Label {
                    text: qsTr('Description')
                }
                TextEdit {
                    // id:
                }
            }
        }
    }
}

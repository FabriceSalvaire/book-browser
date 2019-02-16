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

import QtQml.Models 2.2
import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11

import BookBrowser 1.0
import Widgets 1.0 as Widgets

Widgets.CentredDialog {
    id: dialog
    implicitWidth: 500
    implicitHeight: 400

    standardButtons: Dialog.Ok | Dialog.Cancel

    // onAccepted:
    // onRejected:

    /******************************************************/

    header: TabBar {
        id: tab_bar

        TabButton {
            text: qsTr("General")
        }

        TabButton {
            text: qsTr("Shortcuts")
        }
    }

    StackLayout {
        anchors.fill: parent
        currentIndex: tab_bar.currentIndex

        ColumnLayout {
            id: general_tab

            Item {
                Layout.preferredHeight: 10
            }

            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                ScrollBar.horizontal.policy: ScrollBar.AsNeeded

                GridLayout {
                    width: parent.width
                    columns: 2
                    columnSpacing: 12

                    Label {
                        text: qsTr('Foo')
                    }
                    CheckBox {
                        // id:
                        leftPadding: 0
                        // checked: settings.
                    }
                }
            }
        }

        Item {
            id: shortcut_list_view_container

            ListView {
                id: shortcut_list_view
                anchors.fill: parent
                anchors.rightMargin: ScrollBar.vertical.width
                clip: true

                ScrollBar.vertical: ScrollBar {
                    // id: vertical_scroll_bar
                    // parent: shortcut_list_view.parent
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                }

                // Fixme: ???
                Rectangle {
                    width: parent.width
                    height: 1
                    anchors.top: parent.top
                    color: "#1a000000"
                }

                Rectangle {
                    width: parent.width
                    height: 1
                    anchors.bottom: parent.bottom
                    color: "#1a000000"
                }

                model: ObjectModel {
                    id: shortcut_model

                    Widgets.ShortcutRow {
                        shortcut_name: "Foo"
                        shortcut_display_name: qsTr("Foo")
                    }
                }
            }
        }
    }
}

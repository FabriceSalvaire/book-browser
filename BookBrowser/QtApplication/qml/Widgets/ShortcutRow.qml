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

// Forked from https://github.com/mitchcurtis/slate/blob/master/app/qml/ui/ShortcutRow.qml

import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.1

import BookBrowser 1.0

RowLayout {

    /*******************************************************
     *
     * API
     *
     */

    property string shortcut_name
    property string shortcut_display_name
    property alias original_sequence: editor.original_sequence
    property alias has_changed: editor.has_changed
    property alias new_sequence: editor.new_sequence

    /******************************************************/

    width: parent ? parent.width : 0

    function reset() {
        editor.reset()
    }

    /******************************************************/

    Label {
        Layout.leftMargin: 10
        Layout.fillWidth: true
        text: shortcut_display_name
    }

    KeySequenceEditor {
        id: editor
        Layout.minimumWidth: 200
        enabled: shortcut_name.length > 0
        implicitHeight: edit_button.implicitHeight

        // settings[shortcut_name]
        original_sequence: enabled ? 'Ctrl+A' : ''

        // The fix for QTBUG-57098 probably should have been implemented in C++ as well.
        // I've tried implementing it in C++ with event() and converting the event
        // to a QKeyEvent when the type is ShortcutOverride, but it didn't work.
        Keys.onShortcutOverride: event.accepted = (event.key === Qt.Key_Escape)

        ItemDelegate {
            id: edit_button
            width: parent.width
            implicitWidth: 200
            text: editor.display_sequence
            font.bold: editor.has_changed

            onClicked: editor.forceActiveFocus()

            SequentialAnimation {
                id: flash_animation
                running: editor.activeFocus

                loops: Animation.Infinite
                alwaysRunToEnd: true

                NumberAnimation {
                    target: edit_button.contentItem
                    property: 'opacity'
                    from: 1
                    to: 0.5
                    duration: 300
                }
                NumberAnimation {
                    target: edit_button.contentItem
                    property: 'opacity'
                    from: 0.5
                    to: 1
                    duration: 300
                }
            }
        }
    }
}

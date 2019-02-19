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

Item {

    /*******************************************************
     *
     * API
     *
     */

    property alias text: text_area.text
    property bool processing: false

    /******************************************************/

    id: root

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
        running: root.processing
    }
}

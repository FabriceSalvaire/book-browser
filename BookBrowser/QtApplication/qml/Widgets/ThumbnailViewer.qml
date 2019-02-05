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

Item {
    id: thumbnail_container
    anchors.fill: parent
    anchors.margins: 20

    signal show_page(int page_number)

    Flickable {
	id: flickable
	anchors.fill: parent
	// contentWidth: flow.width
	contentHeight: flow.height

	boundsBehavior: Flickable.StopAtBounds
	clip: true

	Flow {
	    id: flow
	    width: thumbnail_container.width
	    anchors.horizontalCenter: thumbnail_container.horizontalCenter
	    // anchors.margins: 0
	    spacing: 30

	    Repeater {
		model: book.pages

		Rectangle {
		    id: image_container

		    property bool selected: false
		    property int border_width: 5

		    width: thumbnail.sourceSize.width + 2*border_width
		    height: thumbnail.sourceSize.height + 2*border_width
		    border.width: border_width
		    border.color: selected ? '#38b0ff' : '#00000000'
		    color: '#00000000'

		    Image {
			id: thumbnail
			anchors.centerIn: parent

			source: modelData.large_thumbnail_path
			rotation: modelData.orientation

			MouseArea {
			    anchors.fill: parent
			    hoverEnabled: true
			    onClicked: {
				thumbnail_container.show_page(modelData.page_number)
			    }
			    onEntered: selected = true
			    onExited: selected = false
			}
		    }
		}
	    }
	}

	ScrollIndicator.vertical: ScrollIndicator { }
	// ScrollIndicator.horizontal: ScrollIndicator { }
    }
}

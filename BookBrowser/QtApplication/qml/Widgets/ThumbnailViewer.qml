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
    anchors.margins: 20

    signal show_page(int page_number)

    property var thumbnail_model

    Flickable {
	id: flickable
	anchors.fill: parent
	contentWidth: flow.width
	contentHeight: flow.height

	boundsBehavior: Flickable.StopAtBounds
	clip: true

	// ScrollView {
	Flow {
	    id: flow
	    width: flickable.width
	    anchors.horizontalCenter: flickable.horizontalCenter
	    // anchors.margins: 0
	    spacing: 30

	    Repeater {
		model: thumbnail_model

		Rectangle {
		    id: image_container

		    property var book_page: modelData

		    property bool selected: false
		    property int border_width: 5
		    property int image_size: book_page.large_thumbnail_size
		    property bool image_ready: thumbnail.status === Image.Ready

		    width: (image_ready ? thumbnail.sourceSize.width : image_size) + 2*border_width
		    height: (image_ready ? thumbnail.sourceSize.height : image_size) + 2*border_width
		    border.width: border_width
		    border.color: selected ? '#38b0ff' : '#00000000'
		    color: image_ready ? '#00000000' :'#aaaaaa'

		    BusyIndicator {
			anchors.centerIn: parent
			running: !image_ready
		    }

		    Text {
			visible: thumbnail.status !== Image.Ready
			anchors.horizontalCenter: parent.horizontalCenter
			anchors.top: parent.top
			anchors.topMargin: 20
			font.pixelSize: image_size * .10
			text: 'P' + book_page.page_number
		    }

		    Image {
			id: thumbnail
			anchors.centerIn: parent

			asynchronous: true
			source: book_page.large_thumbnail_path
			rotation: book_page.orientation

			MouseArea {
			    anchors.fill: parent
			    hoverEnabled: true
			    onClicked: {
				thumbnail_container.show_page(book_page.page_number)
			    }
			    onEntered: selected = true
			    onExited: selected = false
			}

			function on_thumbnail_ready() {
			    source = book_page.large_thumbnail_path
			}

			onStatusChanged: {
			    if (thumbnail.status == Image.Error) {
				source = ''
			    	book_page.request_large_thumbnail()
				book_page.thumbnail_ready.connect(on_thumbnail_ready)
			    }
			}
		    }
		}
	    }
	}

	// ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
	// ScrollBar.vertical.policy: ScrollBar.AlwaysOn
	ScrollIndicator.vertical: ScrollIndicator { }
	// ScrollIndicator.horizontal: ScrollIndicator { }
    }
}
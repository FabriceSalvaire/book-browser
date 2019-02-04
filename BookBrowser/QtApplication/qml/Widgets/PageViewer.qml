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

// cf. https://raw.githubusercontent.com/oniongarlic/qtquick-flickable-image-zoom/master/qml/main.qml

import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11

Flickable {
    id: flickable

    property var book
    property var book_page

    // The dimensions of the content (the surface controlled by Flickable).
    contentHeight: image_container.height
    contentWidth: image_container.width

    boundsBehavior: Flickable.StopAtBounds
    clip: true

    property bool fit_to_screen_active: true
    property bool full_zoom_active: false
    property real min_zoom: 0.1
    property real max_zoom: 2.0
    property real zoom_step: 0.1

    onWidthChanged: {
        if (fit_to_screen_active)
            fit_to_screen()
    }

    onHeightChanged: {
        if (fit_to_screen_active)
            fit_to_screen()
    }

    onContentXChanged: console.debug('CX' + contentX)
    onContentYChanged: console.debug('CY' + contentY)

    Item {
        id: image_container // purpose ???
	// image_container.size = max(image.size * scale, flickable.size)
        width: Math.max(image.width * image.scale, flickable.width)
        height: Math.max(image.height * image.scale, flickable.height)

        Image {
            id: image
	    // image in centered in image_container
	    // image size can be scaled
            anchors.centerIn: parent
            transformOrigin: Item.Center

            property real prev_scale: 1.0

            asynchronous: true
            cache: false
            fillMode: Image.PreserveAspectFit
            smooth: flickable.moving

	    source: book_page ? book_page.path : ''
	    rotation: book_page ? book_page.orientation : 0

            onScaleChanged: {
                console.debug(scale)
		// if scaled image is larger than flickable
		// then update position of the surface coordinate currently at the top-left corner of the flickable
		// zooming is centered
                if ((width * scale) > flickable.width) {
                    var x_offset = (flickable.width / 2 + flickable.contentX) * scale / prev_scale
                    flickable.contentX = x_offset - flickable.width / 2
                }
                if ((height * scale) > flickable.height) {
                    var y_offset = (flickable.height / 2 + flickable.contentY) * scale / prev_scale
                    flickable.contentY = y_offset - flickable.height / 2
                }
                prev_scale = scale
            }

            onStatusChanged: {
                if (status === Image.Ready) {
		    if (flickable.fit_to_screen_active)
			flickable.fit_to_screen()
		    else if (flickable.full_zoom_active)
			flickable.zoom_full()
                }
            }

            onWidthChanged: console.debug(width)
            onHeightChanged: console.debug(height)
        }
    }

    ScrollIndicator.vertical: ScrollIndicator { }
    ScrollIndicator.horizontal: ScrollIndicator { }


    function fit_to_screen() {
        var new_scale = Math.min(flickable.width / image.width, flickable.height / image.height, 1)
        image.scale = new_scale
        flickable.min_zoom = new_scale // cannot zoom out more than fit scale
        image.prev_scale = 1.0 // flickable.scale ???
        fit_to_screen_active = true
	full_zoom_active = false
	// Ensures the content is within legal bounds
        flickable.returnToBounds()
    }

    function zoom_in() {
        if (image.scale < max_zoom)
            image.scale *= (1.0 + zoom_step)
	// duplicated code
        // flickable.returnToBounds()
        fit_to_screen_active = false
	full_zoom_active = false
        flickable.returnToBounds() // why twice ?
    }

    function zoom_out() {
        if (image.scale > min_zoom)
            image.scale *= (1.0 - zoom_step)
        else
            image.scale = flickable.min_zoom
        // flickable.returnToBounds()
        fit_to_screen_active = false
	full_zoom_active = false
        flickable.returnToBounds()
    }

    function zoom_full() {
        image.scale = 1
        fit_to_screen_active = false
	full_zoom_active = true
        flickable.returnToBounds()
    }

    function first_page() {
	book_page = book.first_page
    }

    function last_page() {
	book_page = book.last_page
    }

    function to_page(page_number) {
	if (book.is_valid_page_number(page_number))
	    book_page = book.page(page_number)
    }

    function prev_page() {
	to_page(book_page.page_number -1)
    }

    function next_page() {
	to_page(book_page.page_number +1)
    }

    function flip() {
	var orientation
	if (rotation == 0) {
	    rotation = 180
	    orientation = 'v'
	}
	else {
	    rotation = 0
	    orientation = 'r'
	}
	book_page.flip_page(orientation)
    }

    function flip_from_page() {
	var orientation
	if (rotation == 0) {
	    // rotation = 180
	    orientation = 'v'
	}
	else {
	    // rotation = 0
	    orientation = 'r'
	}
	book.flip_from_page(page, orientation) // Fixme: orientation ?
    }


    Component.onCompleted: {
	book.new_page.connect(last_page)
    }
}

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

import BookBrowser 1.0

ApplicationWindow {
    id: application_window
    title: qsTr('Book Viewer')
    visible: true

    width: 1000
    height: 500

    property var book: application.book

    Component.onCompleted: {
	console.info('ApplicationWindow.onCompleted')
	application_window.showMaximized()
	image.first_page()
    }

    Page {
        anchors.fill: parent

        Flickable {
            id: flickable
            anchors.fill: parent

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

		    property var book_page
		    source: book_page ? book_page.path : ''
		    rotation: book_page ? book_page.orientation : 0

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

            ScrollIndicator.vertical: ScrollIndicator { }
            ScrollIndicator.horizontal: ScrollIndicator { }
        }

	/*
        PinchArea {
            id: pinch_area
            anchors.fill: f
            enabled: image.status === Image.Ready
            pinch.target: i
            pinch.maximumScale: 2
            pinch.minimumScale: 0.1
            onPinchStarted: {
                console.debug('PinchStart')
                flickable.interactive=false
            }

            onPinchUpdated: {
                flickable.contentX += pinch.previousCenter.x - pinch.center.x
                flickable.contentY += pinch.previousCenter.y - pinch.center.y
            }

            onPinchFinished: {
                console.debug('PinchEnd')
                flickable.interactive=true
                flickable.returnToBounds()
            }
        }
	*/
    }

    header: ToolBar {
        RowLayout {
            ToolButton {
		icon.source: 'qrc:/icons/36x36/zoom-out-black.png'
                onClicked: {
                    flickable.zoom_out()
                }
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/settings-overscan-black.png'
                onClicked: {
                    flickable.fit_to_screen()
                }
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/zoom-fit-width.png'
                onClicked: {
                    flickable.zoom_full()
                }
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/zoom-in-black.png'
                onClicked: {
                    flickable.zoom_in()
                }
            }

            ToolButton {
		icon.source: 'qrc:/icons/36x36/swap-vert-black.png'
                onClicked: {
                    image.flip()
                }
            }

            ToolButton {
		icon.source: 'qrc:/icons/36x36/first-page-black.png'
                onClicked: {
		    image.first_page()
                }
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/arrow-back-black.png'
                onClicked: {
                    image.prev_page()
                }
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/arrow-forward-black.png'
                onClicked: {
                    image.next_page()
                }
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/last-page-black.png'
                onClicked: {
		    image.last_page()
                }
            }
	    SpinBox {
		id: page_number
		editable: true
		from: 1
		to: book.number_of_pages
		value: image.book_page ? image.book_page.page_number: 0

		onValueModified: {
		    image.to_page(value)
		}
            }
	    Label {
		text: '/' + book.number_of_pages
            }

            ToolButton {
		// icon.source: 'qrc:/icons/36x36/.png'
		text: 'Flip from'
                onClicked: {
		    console.info('flip_from_page is disabled')
                    // image.flip_from_page()
                }
            }
        }

	focus: true
	Keys.onPressed: {
	    var key = event.key
            if (key == Qt.Key_Space)
		image.next_page()
            else if (key == Qt.Key_Backspace)
		image.prev_page()
            else if (event.text == 'r')
		image.flip()
            else if (event.text == 'f')
		flickable.fit_to_screen()
            else if (event.text == 'z')
		flickable.zoom_full()
	}
    }

    footer: ToolBar {
        RowLayout {
            Label {
		id: message
		text: ''
            }
	}
    }
}

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

    Component.onCompleted: {
	console.info('ApplicationWindow.onCompleted')
	application_window.showMaximized()
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
                    property int page_index: 1

                    asynchronous: true
                    cache: false
                    fillMode: Image.PreserveAspectFit
                    smooth: flickable.moving

		    function prev_page() {
			page_index = application.prev_page()
		    }

		    function next_page() {
			page_index = application.next_page()
		    }

		    function flip() {
			if (rotation == 0)
			    rotation = 180
			else
			    rotation = 0
			application.flip_page()
		    }

                    // source: application.page_path
		    // rotation: application.orientation
                    source: null
		    rotation: 0

		    function update_page() {
			source = application.page_path
			rotation = application.orientation
		    }

		    Component.onCompleted: {
			application.page_pathChanged.connect(update_page)
			update_page()
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
                            flickable.fit_to_screen()
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
		// Ensures the content is within legal bounds
                flickable.returnToBounds()
            }

            function zoom_in() {
                if (image.scale < max_zoom)
                    image.scale *= (1.0 + zoom_step)
		// duplicated code
                // flickable.returnToBounds()
                fit_to_screen_active = false
                flickable.returnToBounds() // why twice ?
            }

            function zoom_out() {
                if (image.scale > min_zoom)
                    image.scale *= (1.0 - zoom_step)
                else
                    image.scale = flickable.min_zoom
                // flickable.returnToBounds()
                fit_to_screen_active=false
                flickable.returnToBounds()
            }

            function zoom_full() {
                image.scale = 1
                fit_to_screen_active = false
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
	    SpinBox {
		id: page_number
		editable: true
		value: image.page_index

		onValueModified: {
		    application.to_page(value)
		}
            }
	    Label {
		text: '/' + application.number_of_pages
            }
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

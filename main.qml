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

                    asynchronous: true
                    cache: false
                    fillMode: Image.PreserveAspectFit
                    smooth: flickable.moving

                    source: '../Amateur/encyclopedie-patrons-modeles/encyclopedie-patrons-modeles.0411.png'
		    // rotation: 180
		    
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
		console.info('fit_to_screen', flickable.scale, scale, image.scale, new_scale)
                image.scale = new_scale
                flickable.min_zoom = new_scale // cannot zoom out more than fit scale
                image.prev_scale = scale // flickable.scale ???
                fit_to_screen_active = true
		// Ensures the content is within legal bounds
                flickable.returnToBounds()
            }

            function zoom_in() {
                if (flickable.scale < max_zoom) // why flickable scale ???
                    image.scale *= (1.0 + zoom_step)
		// duplicated code
                // flickable.returnToBounds()
                fit_to_screen_active = false
                flickable.returnToBounds() // why twice ?
            }

            function zoom_out() {
                if (flickable.scale > min_zoom)
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

    footer: ToolBar {
        RowLayout {
            ToolButton {
                text: 'Out'
                onClicked: {
                    flickable.zoom_out()
                }
            }
            ToolButton {
                text: 'Reset'
                onClicked: {
                    flickable.zoom_full()
                }
            }
            ToolButton {
                text: 'Fit'
                onClicked: {
                    flickable.fit_to_screen()
                }
            }
            ToolButton {
                text: 'In'
                onClicked: {
                    flickable.zoom_in()
                }
            }
        }
    }

}

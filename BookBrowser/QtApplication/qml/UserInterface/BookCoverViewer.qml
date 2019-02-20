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

// Fixme: duplicated code with ThumbnailViewer.qml

import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11

Item {
    id: thumbnail_container

    /*******************************************************
     *
     * API
     *
     */

    signal load_book(string path)

    property var books_model

    /******************************************************/

    anchors.margins: 20

    /******************************************************/

    Flickable {
        id: flickable
        anchors.fill: parent
        contentWidth: flow.width
        contentHeight: flow.height

        boundsBehavior: Flickable.StopAtBounds
        clip: true

        // ScrollView {
        Flow {
            // Fixme: QML Flow: Cannot anchor to an item that isn't a parent or sibling.
            id: flow
            width: flickable.width
            //! anchors.horizontalCenter: flickable.horizontalCenter
            // anchors.margins: 0
            spacing: 30

            Repeater {
                model: books_model

                Rectangle {
                    id: image_container

                    property var book_cover: modelData

                    property bool selected: false
                    property int border_width: 5
                    property int image_size: book_cover.large_thumbnail_size
                    property bool image_ready: thumbnail.status === Image.Ready

                    width: (image_ready ? thumbnail.sourceSize.width : image_size) + 2*border_width
                    height: (image_ready ? thumbnail.sourceSize.height : image_size) + 2*border_width
                    border.width: border_width
                    border.color: selected ? '#38b0ff' : '#00000000'
                    color: image_ready ? '#00000000' :'#aaaaaa'

                    BusyIndicator {
                        anchors.centerIn: parent
                        running: !(book_cover.is_empty || image_ready)
                    }

                    Image {
                        id: thumbnail
                        anchors.centerIn: parent
                        visible: ! book_cover.is_empty

                        asynchronous: true

                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            onClicked: thumbnail_container.load_book(book_cover.path)
                            onEntered: selected = true
                            onExited: selected = false
                        }

                        Component.onCompleted: {
                            if (!book_cover.is_empty)
                                source = book_cover.large_thumbnail_path
                        }

                        function on_thumbnail_ready() {
                            source = book_cover.large_thumbnail_path
                        }

                        onStatusChanged: {
                            if (thumbnail.status == Image.Error) {
                                source = ''
                                book_cover.request_large_thumbnail()
                                book_cover.thumbnail_ready.connect(on_thumbnail_ready)
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

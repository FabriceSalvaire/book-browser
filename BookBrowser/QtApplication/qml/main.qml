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

import BookBrowser 1.0
import Widgets 1.0 as Widgets

ApplicationWindow {
    id: application_window
    title: qsTr('Book Viewer')
    visible: true

    width: 1000
    height: 500

    // property var book: application.book

    Component.onCompleted: {
	console.info('ApplicationWindow.onCompleted')
	application_window.showMaximized()
	page_viewer.first_page()
    }

    Page {
        anchors.fill: parent

	Widgets.PageViewer {
	    id: page_viewer
	    anchors.fill: parent

	    book: application.book
	}
    }

    header: ToolBar {
        RowLayout {
            ToolButton {
		icon.source: 'qrc:/icons/36x36/zoom-out-black.png'
                onClicked: {
                    page_viewer.zoom_out()
                }
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/settings-overscan-black.png'
                onClicked: {
                    page_viewer.fit_to_screen()
                }
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/zoom-fit-width.png'
                onClicked: {
                    page_viewer.zoom_full()
                }
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/zoom-in-black.png'
                onClicked: {
                    page_viewer.zoom_in()
                }
            }

            ToolButton {
		icon.source: 'qrc:/icons/36x36/swap-vert-black.png'
                onClicked: {
                    page_viewer.flip()
                }
            }

            ToolButton {
		icon.source: 'qrc:/icons/36x36/first-page-black.png'
                onClicked: {
		    page_viewer.first_page()
                }
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/arrow-back-black.png'
                onClicked: {
                    page_viewer.prev_page()
                }
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/arrow-forward-black.png'
                onClicked: {
                    page_viewer.next_page()
                }
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/last-page-black.png'
                onClicked: {
		    page_viewer.last_page()
                }
            }
	    SpinBox {
		id: page_number
		editable: true
		from: 1
		to: book.number_of_pages
		value: page_viewer.book_page ? page_viewer.book_page.page_number: 0

		onValueModified: {
		    page_viewer.to_page(value)
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
                    // page_viewer.flip_from_page()
                }
            }
        }

	focus: true
	Keys.onPressed: {
	    var key = event.key
            if (key == Qt.Key_Space)
		page_viewer.next_page()
            else if (key == Qt.Key_Backspace)
		page_viewer.prev_page()
            else if (event.text == 'r')
		page_viewer.flip()
            else if (event.text == 'f')
		page_viewer.fit_to_screen()
            else if (event.text == 'z')
		page_viewer.zoom_full()
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

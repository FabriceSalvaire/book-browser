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

// Fixme: push crash sane, image_viewer ???

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

    property var book: application.book

    Component.onCompleted: {
	console.info('ApplicationWindow.onCompleted')
	application_window.showMaximized()
	page_viewer.first_page()
    }


    function clear_message() {
	message_label.text = ''
    }

    function show_message(message) {
	message_label.text = message
    }


    StackView {
        id: stack_view
        anchors.fill: parent

        initialItem: Page {
    	    id: thumbnail_page

	    Widgets.ThumbnailViewer {
		id: thumbnail_viewer
		anchors.fill: parent

		thumbnail_model: book.pages

		onShow_page: {
		    page_viewer.to_page(page_number)
		    stack_view.push(page_viewer_page)
		}
	    }
	}

	Page {
	    id: page_viewer_page

	    Widgets.PageViewer {
		id: page_viewer
		anchors.fill: parent

		book: application.book
	    }

	    Widgets.Grid {
		id: grid
		visible: false
		anchors.fill: parent
	    }
	}

	Page {
	    id: scanner_page

	    Widgets.ScannerUI {
		id: scanner_ui
		anchors.fill: parent

		// scanner: application.scanner
	    }
	}
    }

    Action {
	id: prev_page_action
	icon.source: 'qrc:/icons/36x36/arrow-back-black.png'
	shortcut: 'Backspace'
	onTriggered: page_viewer.prev_page()
    }

    Action {
	id: next_page_action
	icon.source: 'qrc:/icons/36x36/arrow-forward-black.png'
	shortcut: 'n' //'Space'
	onTriggered: page_viewer.next_page()
    }

    Action {
	id: flip_action
	icon.source: 'qrc:/icons/36x36/swap-vert-black.png'
	shortcut: 'r'
	onTriggered: page_viewer.flip()
    }

    Action {
	id: fit_to_screen_action
	icon.source: 'qrc:/icons/36x36/settings-overscan-black.png'
	shortcut: 'f'
	onTriggered: page_viewer.fit_to_screen()
    }

    Action {
	id: zoom_full_action
	icon.source: 'qrc:/icons/36x36/zoom-fit-width.png'
	shortcut: 'z'
	onTriggered: page_viewer.zoom_full()
    }

    header: ToolBar {
        RowLayout {
            ToolButton {
		icon.source: 'qrc:/icons/36x36/refresh-black.png'
                onClicked: {
		    var path = book.path
		    application.load_book(path)
		    show_message(qsTr('Loaded book at %1'.arg(path)))
		}
            }

            ToolButton {
		icon.source: 'qrc:/icons/36x36/view-comfy-black.png'
                onClicked: {
		    stack_view.pop()
		}
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/image-black.png'
                onClicked: {
		    stack_view.push(page_viewer_page)
		}
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/scanner-black.png'
                onClicked: {
		    // Fixme:
		    scanner_ui.init()
		    stack_view.push(scanner_page)
		}
            }

            ToolButton {
		icon.source: 'qrc:/icons/36x36/zoom-out-black.png'
                onClicked: page_viewer.zoom_out()
            }
            ToolButton {
		action: fit_to_screen_action
            }
            ToolButton {
		action: zoom_full_action
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/zoom-in-black.png'
                onClicked: page_viewer.zoom_in()
            }

            ToolButton {
		action: flip_action
            }

            ToolButton {
		icon.source: 'qrc:/icons/36x36/first-page-black.png'
                onClicked: page_viewer.first_page()
            }
            ToolButton {
		action: prev_page_action
            }
            ToolButton {
		action: next_page_action
            }
            ToolButton {
		icon.source: 'qrc:/icons/36x36/last-page-black.png'
                onClicked: page_viewer.last_page()
            }
	    SpinBox {
		id: page_number
		editable: true
		from: 1
		to: book.number_of_pages
		value: page_viewer.book_page ? page_viewer.book_page.page_number: 0

		onValueModified: page_viewer.to_page(value)
            }
	    Label {
		text: '/' + book.number_of_pages
            }

            ToolButton {
		icon.source: 'qrc:/icons/36x36/grid-on-black.png'
		checkable: true
                onClicked: grid.visible = !grid.visible
            }

            ToolButton {
		// icon.source: 'qrc:/icons/36x36/.png'
		text: 'Flip from'
                onClicked: {
		    // console.info('flip_from_page is disabled')
                    page_viewer.flip_from_page()
                }
            }
        }
    }

    footer: ToolBar {
        RowLayout {
            Label {
		id: message_label
		text: ''
            }
	}
    }
}

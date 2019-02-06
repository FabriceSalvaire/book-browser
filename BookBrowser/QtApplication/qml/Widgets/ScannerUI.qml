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

// Fixme: selection area, label, backup
// save preview
// show mouse pointer

import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11
import QtQuick.Dialogs 1.0

Item {
    id: scanner_ui

    property var scanner

    property bool dirty_selection_area: false
    property bool is_preview_scan: false
    property bool valid_selection_area: false

    Component.onCompleted: {
	console.info('ScannerUI.onCompleted')
    }


    function init() {
	if (!scanner) {
	    application.init_scanner()
	    application.scanner_ready.connect(on_scanner_ready)
	}
    }


    function on_scanner_ready() {
	console.info('on_scanner_ready', application.scanner.has_device)
	var has_device = application.scanner.has_device
	// has_device = true // debug
	if (has_device) {
	    scanner = application.scanner

	    var default_resolution = '200'
	    resolution_combobox.currentIndex = resolution_combobox.find(default_resolution)
	    scanner.resolution = default_resolution

	    var default_mode = 'Color'
	    mode_combobox.currentIndex = mode_combobox.find(default_mode)
	    scanner.mode = default_mode

	    // Fixme: ???
	    // https://www.kdab.com/slot-not-invoked/
	    // scanner.preview_done.connect(on_preview_done)
	    // scanner.file_exists_error.connect(on_file_exists_error)
	    // scanner.scan_done.connect(on_scan_done)

	    application.debug()
	    application.preview_done.connect(on_preview_done)
	    application.file_exists_error.connect(on_file_exists_error)
	    application.scan_done.connect(on_scan_done)

	    if (application.book)
		filename_count.text = Math.max(application.book.number_of_pages +1, 1)

	    control_panel.enabled = true
	}
    }

    function enable_scan_button(status) {
	scan_button.enabled = status
	preview_scan_button.enabled = status
    }

    function on_preview_done(path) {
	console.info('on_preview_done', path)
	if (path) {
	    is_preview_scan = true
	    image_preview.source = 'image://scanner_image/' + path
	    valid_selection_area = true
	    enable_scan_button(true)
	    application_window.clear_message()
	}
    }

    function on_file_exists_error(path) {
	console.info('on_file_exists_error', path)
	error_dialog_message.text = 'File "' + path + '" exists'
	error_dialog.open() // Fixme: position
	enable_scan_button(true)
    }

    function on_scan_done(path) {
	console.info('on_scan_done', path)
	if (path) {
	    is_preview_scan = false
	    image_preview.source = path
	    filename_count.increment()
	    enable_scan_button(true)
	    application_window.show_message('Saved ' + path)
	}
    }


    function scan_preview() {
	application_window.show_message('Maximize scan area')
	scanner.maximize_scan_area()
	enable_scan_button(false)
	scanner.scan_image()
    }

    function scan_page() {
	if (valid_selection_area) {
	    if (dirty_selection_area) {
		var bounds = image_preview.bounds()
		application_window.show_message('Reset bounds ' + bounds)
		scanner.area = bounds
		dirty_selection_area = false
	    }
	} else {
	    application_window.show_message('Maximize scan area')
	    scanner.maximize_scan_area()
	    dirty_selection_area = false
	    valid_selection_area = true
	}

	if (is_preview_scan)
	    selection_area.visible = false

	enable_scan_button(false)

	scanner.scan(filename_path.text, filename_pattern.text, false, filename_count.text)
    }


    Dialog {
	id: error_dialog
	modal: true
	standardButtons: Dialog.Ok

	Label {
	    id: error_dialog_message
	}
    }

    FileDialog {
	id: file_dialog
	title: 'Please choose a folder'
	folder: shortcuts.home
	selectFolder: true
	onAccepted: {
            console.log('You chose: ' + file_dialog.fileUrls)
	    filename_path.text = file_dialog.fileUrls[0]
	}
	onRejected: {
            console.log('Canceled')
	}
	// Component.onCompleted: visible = true
    }

    RowLayout{
	anchors.fill: parent
	anchors.margins: 10
	spacing: 10

	ColumnLayout {
	    id: control_panel
	    Layout.alignment: Qt.AlignTop
	    Layout.preferredWidth: 250
	    spacing: 20
	    enabled: false

	    RowLayout {
		Label {
		    text: 'Device'
		}
		Label {
		    text: scanner ? scanner.device : ''
		}
		BusyIndicator {
		    running: !scanner
		}
	    }

	    Button {
		id: scan_button
		Layout.preferredHeight: 100
		Layout.preferredWidth: control_panel.width
		text: 'Scan'
		font.pixelSize: 30
		background: Rectangle {
		    // implicitWidth: 100
		    // implicitHeight: 40
		    color: scan_button.down ? "#4b984b" : "#5cb85c"
		    // border.color: "#4b984b"
		    // border.width: 1
		    radius: 10
		}
		onClicked: scan_page()
	    }

	    Button {
		id: preview_scan_button
		Layout.preferredHeight: 50
		Layout.preferredWidth: control_panel.width
		text: 'Preview'
		background: Rectangle {
		    color: preview_scan_button.down ? "#d59945" : "#f0ad4e"
		    radius: 10
		}
		onClicked: scan_preview()
	    }

	    RowLayout {
		ToolButton {
		    icon.source: 'qrc:/icons/36x36/folder-black.png'
                    onClicked: file_dialog.open()
		}
		TextField {
		    id: filename_path
		    Layout.fillWidth: true
		    text: scanner ? scanner.working_directory : ''
		}
	    }

	    RowLayout {
		TextField {
		    id: filename_pattern
		    Layout.fillWidth: true
		    text: 'foo.{:03}.png'
		}
		TextField {
		    id: filename_count
		    // Fixme: take last !!
		    text: '1'

		    function increment(string) {
			text = String(parseInt(text) + 1)
		    }
		}
	    }

	    RowLayout {
		Label {
		    text: 'Resolution'
		}
		ComboBox {
		    id: resolution_combobox
		    model: scanner ? scanner.resolutions : []
		    onAccepted: {
			scanner.resolution = editText
		    }
		}
	    }

	    RowLayout {
		Label {
		    text: 'Mode'
		}
		ComboBox {
		    id: mode_combobox
		    model: scanner ? scanner.modes : []
		    onAccepted: scanner.mode = editText
		}
	    }
	}

	Item {
	    id: image_preview_container
	    Layout.alignment: Qt.AlignTop
	    Layout.preferredWidth: 1000
	    Layout.fillWidth: true
	    Layout.fillHeight: true

	    Image {
	    	id: image_preview
	    	anchors.fill: parent
		horizontalAlignment: Image.AlignLeft
		verticalAlignment: Image.AlignTop
	    	fillMode: Image.PreserveAspectFit

	    	// source: '/home/fabrice/book-browser/foo.png'

		Rectangle {
		    id: selection_area
		    visible: false
		    color: '#aaaaaaff'
		    x: 0
		    y: 0
		    width: 100
		    height: 100
		}

		function maximise_area() {
		    selection_area.x = 0
		    selection_area.y = 0
		    selection_area.width = image_preview.paintedWidth
		    selection_area.height = image_preview.paintedHeight
		    selection_area.visible = true
		}

		function bounds() {
		    var x_inf = selection_area.x
		    var y_inf = selection_area.y
		    var x_sup = x_inf + selection_area.width
		    var y_sup = y_inf + selection_area.height
		    var scale = 10000
		    x_inf *= scale / image_preview.paintedWidth
		    x_sup *= scale / image_preview.paintedWidth
		    y_inf *= scale / image_preview.paintedHeight
		    y_sup *= scale / image_preview.paintedHeight
		    return x_inf + ',' + x_sup + ',' + y_inf + ',' + y_sup
		}

		onStatusChanged: {
                    if (status === Image.Ready) {
			if (is_preview_scan)
			    maximise_area()
		    }
		}

		MouseArea {
		    anchors.fill: parent

		    property int x_handler: 0
		    property int y_handler: 0

		    function selection_area_start(mouse) {
			var x = mouse.x
			var y = mouse.y
			var x_inf = selection_area.x
			var y_inf = selection_area.y
			var x_sup = x_inf + selection_area.width
			var y_sup = y_inf + selection_area.height
			var margin = 100

			if (x < (x_inf + margin))
			    x_handler = 1
			else if ((x_sup - margin) < x)
			    x_handler = 3
			else
			    x_handler = 2

			if (y < (y_inf + margin))
			    y_handler = 1
			else if ((y_sup - margin) < y)
			    y_handler = 3
			else
			    y_handler = 2

			console.info('Handlers', x_handler, y_handler)
		    }

		    function selection_area_update(mouse) {
			var x = Math.min(Math.max(mouse.x, 0), image_preview.paintedWidth)
			var y = Math.min(Math.max(mouse.y, 0), image_preview.paintedHeight)
			var x_inf = selection_area.x
			var y_inf = selection_area.y

			//  X   1  2  3
			//  Y 1 ii xi si
			//    2 ix xx sx
			//    3 is xs ss

			// console.info(x_handler, y_handler, x, y)
			if (x_handler == 1) {
			    selection_area.width = selection_area.width - (x - x_inf)
			    selection_area.x = x
			} else if (x_handler == 3)
			    selection_area.width = x - x_inf

			if (y_handler == 1) {
			    selection_area.height = selection_area.height - (y - y_inf)
			    selection_area.y = y
			} else if (y_handler == 3)
			    selection_area.height = y - y_inf
		    }

		    function selection_area_stop(mouse) {
			x_handler = 0
			y_handler = 0
			dirty_selection_area = true
		    }

		    onPressed: {
			if (selection_area.visible)
			    selection_area_start(mouse)
		    }

		    onPositionChanged: {
			if (selection_area.visible)
			    selection_area_update(mouse)
		    }

		    onReleased: {
			if (selection_area.visible)
			    selection_area_stop(mouse)
		    }
		}
	    }
	}
    }
}

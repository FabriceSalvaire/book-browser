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

import Widgets 1.0 as Widgets

Item {
    id: scanner_ui

    property var scanner // Fixme: interval _scanner

    property bool dirty_selection_area: false
    property bool is_preview_scan: false
    property bool valid_selection_area: false

    // Component.onCompleted: {
    // 	console.info('ScannerUI.onCompleted')
    // }

    /***********************************************************************************************
     *
     * API
     *
     */

    function init() {
	if (!scanner) {
	    busy_indicator.running = true
	    application.init_scanner()
	    application.scanner_ready.connect(on_scanner_ready)
	}
    }

    /***********************************************************************************************
     *
     * Slots
     *
     */

    function on_scanner_ready() {
	console.info('on_scanner_ready', application.scanner.has_device)
	busy_indicator.running = false
	var has_device = application.scanner.has_device
	has_device = true // debug
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

	    image_preview.image_ready.connect(on_image_ready)

	    if (application.book)
		filename_count.value = Math.max(application.book.last_page_number +1, 1)

	    control_panel.enabled = true
	}
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
	file_exists_error_dialog.open_for_path(path)
	enable_scan_button(true)
    }

    function on_scan_done(path) {
	console.info('on_scan_done', path)
	if (path) {
	    is_preview_scan = false
	    image_preview.source = path
	    filename_count.increase()
	    enable_scan_button(true)
	    application_window.show_message('Saved ' + path)
	}
    }

    function on_image_ready() {
	if (is_preview_scan)
	    image_preview.maximise_area()
    }

    /***********************************************************************************************
     *
     * Functions
     *
     */

    function enable_scan_button(status) {
	scan_button.enabled = status
	preview_scan_button.enabled = status
    }

    function maximize_scan_area() {
	scanner.maximize_scan_area()
	scan_area_label.set_maximised()
	application_window.show_message('Maximize scan area')

    }

    function scan_preview() {
	maximize_scan_area()
	enable_scan_button(false)
	scanner.scan_image()
    }

    function call_scan_page(overwrite) {
	// can trigger file_exists_error
	scanner.scan(filename_path.text, filename_pattern.text, overwrite, filename_count.value)
    }

    function to_percent(x) {
	return Math.round(x*100)
    }

    function scan_page() {
	application_window.clear_message()

	if (valid_selection_area) {
	    if (dirty_selection_area) {
		var bounds = image_preview.bounds()
		var x_inf = bounds[0]
		var x_sup = bounds[1]
		var y_inf = bounds[2]
		var y_sup = bounds[3]
		var percent_bounds = bounds.map(to_percent)
		var x_inf_p = percent_bounds[0]
		var x_sup_p = percent_bounds[1]
		var y_inf_p = percent_bounds[2]
		var y_sup_p = percent_bounds[3]
		scan_area_label.set_custon()
		application_window.show_message('Reset bounds to [%1, %2, %3, %4] %'.arg(x_inf_p).arg(x_sup_p).arg(y_inf_p).arg(y_sup_p))
		scanner.set_area(x_inf, x_sup, y_inf, y_sup)
		dirty_selection_area = false
	    }
	} else {
	    maximize_scan_area()
	    dirty_selection_area = false
	    valid_selection_area = true
	}

	if (is_preview_scan)
	    image_preview.hide_selection_area()

	enable_scan_button(false)

	var overwrite = false
	call_scan_page(overwrite)
    }

    /***********************************************************************************************
     *
     * Dialogs
     *
     */

    Widgets.CentredDialog {
	id: error_dialog
	modal: true
	standardButtons: Dialog.Ok

	Label {
	    id: error_dialog_message
	}
    }

    Widgets.CentredDialog {
	id: file_exists_error_dialog
	modal: true
	title: qsTr('File Error')
	standardButtons: Dialog.Ok | Dialog.Cancel

	function open_for_path(path) {
	    var template = qsTr('<p>A file "%1" already exists.</p><p><b>Do you want to overwrite it ?</b></p>')
	    file_exists_error_dialog_message.text = template.arg(path)
	    open() // Fixme: position
	}

	TextArea {
	    id: file_exists_error_dialog_message
	    anchors.margins: 20
	    textFormat: TextEdit.RichText
	}

	onAccepted: {
	    var overwrite = true
	    call_scan_page(overwrite)
	}
    }

    Widgets.BookFolderDialog {
	id: book_folder_dialog
	onAccepted: {
	    filename_path.text = book_folder_dialog.selected_path()
	}
    }

    /***********************************************************************************************
     *
     * Items
     *
     */

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
		    text: qsTr('Device')
		}
		Label {
		    text: scanner ? scanner.device : ''
		}
		BusyIndicator {
		    id: busy_indicator
		    running: false
		}
	    }

	    Button {
		id: scan_button
		Layout.preferredHeight: 100
		Layout.preferredWidth: control_panel.width
		text: qsTr('Scan')
		font.pixelSize: 50
		font.bold: true
		background: Rectangle {
		    // implicitWidth: 100
		    // implicitHeight: 40
		    color: scan_button.down ? "#4c9a4c" : "#5cb85c" // hsv 120 128 184 (-30)
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
		text: qsTr('Preview')
		background: Rectangle {
		    color: preview_scan_button.down ? "#d29744" : "#f0ad4e" // hsv 35 172 240 (-20)
		    radius: 10
		}
		onClicked: scan_preview()
	    }

	    RowLayout {
		ToolButton {
		    icon.source: 'qrc:/icons/36x36/folder-black.png'
                    onClicked: book_folder_dialog.open()
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
		SpinBox {
		    id: filename_count
		    font.pixelSize: 30
		    value: 1
		    to: 1000
		}
	    }

	    RowLayout {
		Label {
		    text: qsTr('Resolution')
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
		    text: qsTr('Mode')
		}
		ComboBox {
		    id: mode_combobox
		    model: scanner ? scanner.modes : []
		    onAccepted: scanner.mode = editText
		}
	    }

	    RowLayout {
		Label {
		    text: qsTr('Scan Area')
		}
		Label {
		    id: scan_area_label
		    function set_maximised() {
			text = qsTr('Maximised')
		    }
		    function set_custon() {
			text = qsTr('Custom')
		    }
		}
	    }
	}

	Item {
	    id: image_preview_container
	    Layout.alignment: Qt.AlignTop
	    Layout.preferredWidth: 1000
	    Layout.fillWidth: true
	    Layout.fillHeight: true

	    Widgets.ImagePreviewer {
	    	id: image_preview
		anchors.fill: parent
		horizontalAlignment: Image.AlignLeft
		verticalAlignment: Image.AlignTop
	    }
	}
    }
}

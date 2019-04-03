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

// Fixme: selection area, label, backup
// save preview
// show mouse pointer

import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11

import Widgets 1.0 as Widgets
import Controls 1.0 as Controls
import Constants 1.0

Item {
    id: scanner_ui

    property var scanner // Fixme: interval _scanner

    property bool dirty_selection_area: false
    property bool is_preview_scan: false
    property bool valid_selection_area: false

    property bool started_scan: false

    // Component.onCompleted: {
    //  console.info('ScannerUI.onCompleted')
    // }

    /*******************************************************
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

    function save() {
        if (scanner) {
            scanner.config.save()
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
        if (has_device) {
            scanner = application.scanner

            console.info('Set scanner config')
            scanner.config.path = scanner.working_directory
            var loaded = scanner.config.load()
            console.info('Scanner config loaded', loaded)

            var default_resolution = scanner.config.resolution
            resolution_combobox.currentIndex = resolution_combobox.find(default_resolution)

            var default_mode = scanner.config.mode
            mode_combobox.currentIndex = mode_combobox.find(default_mode)

            filename_path.text = scanner.config.path
            filename_pattern.text = loaded ? scanner.config.filename_pattern : 'foo.{:03}.png'

            number_of_pages.value = scanner.config.number_of_pages

            scan_area_label.set_custon()

            if (loaded) {
                filename_index.value = scanner.config.index
                valid_selection_area = true
            } else if (application.book) {
                var index = Math.max(application.book.last_page_number +1, 1)
                filename_index.value = index
            }

            // Thread issue ???
            // QML -> QmlScanner start -> Runable -> QmlScanner
            // scanner.preview_done.connect(on_preview_done)
            // scanner.file_exists_error.connect(on_file_exists_error)
            // scanner.scan_done.connect(on_scan_done)

            // Fixme: sometimes signal is not received
            application.debug()
            application.preview_done.connect(on_preview_done)
            application.file_exists_error.connect(on_file_exists_error)
            application.path_error.connect(on_path_error)
            application.scan_done.connect(on_scan_done)

            image_preview.image_ready.connect(on_image_ready)

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

    function on_path_error(path) {
        console.info('on_path_error', path)
        path_error_dialog.open_for_path(path)
        enable_scan_button(true)
    }

    function on_scan_done(path) {
        image_preview.source = '' // to force reload
        console.info('on_scan_done', path)
        if (path) {
            is_preview_scan = false
            image_preview.source = path
            filename_index.increase()
            enable_scan_button(true)
            application_window.show_message('Saved ' + path)
            if (!started_scan) {
                started_scan = true
                scanner.start_timer()
            }
            update_end_time()
        }
    }

    function update_end_time() {
        var end_time = scanner.end_time(filename_index.value -1, number_of_pages.value)
        // if (end_time.length) {
        end_time_label.text = end_time
        // }
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
        rescan_button.enabled = status
        busy_indicator.running = !status
    }

    function maximize_scan_area() {
        scanner.config.is_maximized = true
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
        scanner.scan(overwrite)
    }

    function to_percent(x) {
        return Math.round(x*100)
    }

    function scan_page(overwrite) {
        application_window.clear_message()

        if (valid_selection_area) {
            if (dirty_selection_area) {
                var bounds = image_preview.bounds()
                var x_inf = bounds.x_inf
                var x_sup = bounds.x_sup
                var y_inf = bounds.y_inf
                var y_sup = bounds.y_sup
                var x_inf_p = to_percent(x_inf)
                var x_sup_p = to_percent(y_sup)
                var y_inf_p = to_percent(y_inf)
                var y_sup_p = to_percent(y_sup)
                application_window.show_message('Reset bounds to [%1, %2, %3, %4] %'.arg(x_inf_p).arg(x_sup_p).arg(y_inf_p).arg(y_sup_p))
                scanner.config.area = bounds
                scan_area_label.set_custon()
                dirty_selection_area = false
            }
        } else {
            console.info('no valid selection area')
            maximize_scan_area()
            dirty_selection_area = false
            valid_selection_area = true
        }

        if (is_preview_scan)
            image_preview.hide_selection_area()
        enable_scan_button(false)

        call_scan_page(overwrite)
    }

    function rescan_page() {
        filename_index.decrease()
        enable_scan_button(false)
        scan_page(true) // not call_scan_page
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
            file_error_message.text = template.arg(path)
            open()
        }

        TextArea {
            id: file_error_message
            anchors.margins: 20
            textFormat: TextEdit.RichText
        }

        onAccepted: {
            var overwrite = true
            call_scan_page(overwrite)
        }
    }

    Widgets.CentredDialog {
        id: rescan_page_dialog
        modal: true
        // title: qsTr('')
        standardButtons: Dialog.Ok | Dialog.Cancel
        onAccepted: rescan_page()

        TextArea {
            anchors.margins: 20
            textFormat: TextEdit.RichText
            text: qsTr('<b>Do you want to rescan the page ?</b>')
        }
    }

    Widgets.CentredDialog {
        // Fixme: QML Dialog: Binding loop detected for property "implicitWidth"
        id: path_error_dialog
        modal: true
        title: qsTr('Path Error')
        standardButtons: Dialog.Ok

        function open_for_path(path) {
            var template = qsTr("<p>Path \"%1\" don't exists.</p>")
            path_error_message.text = template.arg(path)
            open()
        }

        TextArea {
            id: path_error_message
            anchors.margins: 20
            textFormat: TextEdit.RichText
        }
    }

    Widgets.BookFolderDialog {
        id: book_folder_dialog
        onAccepted: filename_path.text = book_folder_dialog.selected_path()
    }

    /***********************************************************************************************
     *
     * Items
     *
     */

    RowLayout{
        id: row_layout
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        ColumnLayout {
            id: control_panel
            Layout.alignment: Qt.AlignTop
            Layout.preferredWidth: row_layout.width / 3
            spacing: 20
            enabled: false

            RowLayout {
                Label {
                    text: qsTr('Device')
                }
                Label {
                    text: scanner ? scanner.device : ''
                }
            }

            Controls.CustomButton {
                id: scan_button
                Layout.preferredHeight: 100
                Layout.preferredWidth: control_panel.width
                font.pixelSize: 50
                font.bold: true
                color_label: 'white'
                color_background: Style.color.success

                text: qsTr('Scan')

                onClicked: scan_page(false)
            }

            Controls.CustomButton {
                id: preview_scan_button
                Layout.preferredHeight: 50
                Layout.preferredWidth: control_panel.width
                font.bold: true
                color_label: 'white'
                color_background: Style.color.primary

                text: qsTr('Preview')

                onClicked: scan_preview()
            }

            RowLayout {
                ToolButton {
                    icon.name: 'folder-black'
                    onClicked: book_folder_dialog.open()
                }
                TextField {
                    id: filename_path
                    Layout.fillWidth: true
                    selectByMouse: true
                    text: '' // scanner ? scanner.working_directory : ''
                    onTextChanged: scanner.config.path = text
                }
            }

            RowLayout {
                TextField {
                    id: filename_pattern
                    Layout.fillWidth: true
                    selectByMouse: true
                    text: '' // scanner.config.filename_pattern // cannot bind on different thread
                    onTextChanged: scanner.config.filename_pattern = text
                }
                SpinBox {
                    id: filename_index
                    font.pixelSize: 30
                    value: 0
                    to: 1000
                    onValueChanged: scanner.config.index = value
                }
            }

            RowLayout {
                Label {
                    text: qsTr('Resolution')
                }
                ComboBox {
                    id: resolution_combobox
                    model: scanner ? scanner.resolutions : []
                    onActivated: scanner.config.resolution = parseInt(currentText)
                }
            }

            RowLayout {
                Label {
                    text: qsTr('Mode')
                }
                ComboBox {
                    id: mode_combobox
                    model: scanner ? scanner.modes : []
                    onActivated: scanner.config.mode = currentText
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
                        // Fixme: connect to mouse
                        var area = scanner.config.area_mm
                        text = '[%1, %2] x [%3, %4] mm'
                            .arg(Math.round(area.x_inf))
                            .arg(Math.round(area.x_sup))
                            .arg(Math.round(area.y_inf))
                            .arg(Math.round(area.y_sup))
                    }
                }
            }

            Controls.CustomButton {
                id: rescan_button
                Layout.preferredHeight: 50
                Layout.preferredWidth: control_panel.width
                font.bold: true
                color_label: 'black'
                color_background: Style.color.warning

                text: qsTr('Rescan')

                onClicked: {
                    // rescan_page()
                    rescan_page_dialog.open()
                    rescan_button.focus = false
                    scan_button.focus = true
                }
            }

            GroupBox {
                // title: qsTr('Timer')
                Layout.preferredWidth: parent.width

                ColumnLayout {
                    Layout.preferredWidth: parent.width
                    spacing: 10

                    RowLayout {
                        Label {
                            text: qsTr('Number of pages')
                        }
                        SpinBox {
                            id: number_of_pages
                            from: 1
                            value: 100
                            to: 1000
                            editable: true
                            onValueChanged: {
                                scanner.config.number_of_pages = value
                                update_end_time()
                            }
                        }
                    }

                    RowLayout {
                        Widgets.ToolButtonTip {
                            icon.name: 'alarm-black'
                            size: 36
                            onClicked: {
                                end_time_label.text = '...'
                                scanner.start_timer()
                            }
                        }
                        // Image {
                        //     source: 'qrc:/icons/alarm-black'
                        // }
                        // Label {
                        //     text: qsTr('End Time')
                        // }
                        Label {
                            id: end_time_label
                            // Fixme: cause segfault !!!
                            // text: qsTr('unknown')
                            text: 'unknown'
                        }
                    }

                    // Widgets.ToolButtonTip {
                    //     // text: qsTr('Reset Timer')
                    //     // icon.name: 'hourglass-empty-black'
                    //     icon.name: 'refresh-black'
                    //     onClicked: scanner.start_timer()
                    // }
                }
            }
        }

        Item {
            id: image_preview_container
            Layout.alignment: Qt.AlignTop
            Layout.preferredWidth: scanner_ui.width
            Layout.fillWidth: true
            Layout.fillHeight: true

            Widgets.ImagePreviewer {
                id: image_preview
                anchors.fill: parent
                horizontalAlignment: Image.AlignLeft
                verticalAlignment: Image.AlignTop
            }
        }

        ColumnLayout {
            Layout.alignment: Qt.AlignBottom | Qt.AlignRight
            Layout.preferredWidth: image_magnifier.width
            Layout.fillHeight: true

            Widgets.ImageMagnifier {
                id: image_magnifier
                //! anchors.bottom: parent.bottom
                //! anchors.right: parent.right
                width: 256
                height: 256

                image_viewer: image_preview
            }
        }
    }

    BusyIndicator {
        id: busy_indicator
        anchors.right: parent.right
        anchors.top: parent.top
        width: 128
        height: width
        running: false
    }
}

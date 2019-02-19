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

import QtQml 2.11
import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11

import BookBrowser 1.0
import Widgets 1.0 as Widgets
import Constants 1.0

Page {

    /*******************************************************
     *
     * API
     *
     */

    property var metadata: application.book.metadata

    /******************************************************/

    Component.onCompleted: {
        console.info('Completed Metadata Page')
        init()
    }

    function init() {
        // Fixme: UI — QML binding
        //   if use Binding then
        //      valeus are reset at startup
        //      metadata is updated each time a key is pressed
        path_label.text = metadata.path
        isbn_textfield.text = metadata.isbn
        title_textfield.text = metadata.title
        authors_textfield.text = metadata.authors
        publisher_textfield.text = metadata.publisher
        language_textfield.text = metadata.language
        number_of_pages_spin_box.value = metadata.number_of_pages
        page_offset_spinbox.value = metadata.page_offset
        year_spinbox.value = metadata.year
        keywords_textfield.text = metadata.keywords
        description_textfield.text = metadata.description
        notes_editor.text = metadata.notes
        notes_textarea.text = metadata.notes_html
    }

    function update_from_isbn() {
        metadata.update_from_isbn()

        title_textfield.text = metadata.title
        authors_textfield.text = metadata.authors
        publisher_textfield.text = metadata.publisher
        language_textfield.text = metadata.language
        year_spinbox.value = metadata.year
    }

    /******************************************************/

    id: root

    Item {
        anchors.fill: parent
        anchors.margins: 20

        ColumnLayout {

            Widgets.WarnedToolButton {
                id: save_button
                icon.name: 'save-black'
                size: 64
                tip: qsTr('Save')

                warned: metadata.dirty
                icon.color: warned ? Style.color.danger : Style.color.success

                onClicked: metadata.save()
            }

            ScrollView {
                // Fixme:
                id: container
                Layout.preferredWidth: 800
                Layout.fillHeight: true
                clip: true
                ScrollBar.horizontal.policy: ScrollBar.AsNeeded

                GridLayout {
                    width: container.width
                    columns: 2
                    columnSpacing: 10

                    Label {
                        text: qsTr('Path')
                    }
                    Widgets.TextField {
                        id: path_label
                        Layout.fillWidth: true
                        readOnly: true
                    }

                    Label {
                        text: qsTr('ISBN')
                    }
                    RowLayout {
                        Layout.fillWidth: true

                        Widgets.TextField {
                            id: isbn_textfield
                            Layout.fillWidth: true
                            onEditingFinished: metadata.isbn = text
                        }

                        Widgets.ToolButtonTip {
                            icon.name: 'refresh-black'
                            tip: qsTr('Query ISBN')
                            onClicked: update_from_isbn()
                        }
                    }
                    // Binding { target: metadata; property: 'isbn'; value: isbn_textfield.text }

                    Label {
                        text: qsTr('Title')
                    }
                    Widgets.TextField {
                        id: title_textfield
                        Layout.fillWidth: true
                        onEditingFinished: metadata.title = text
                    }
                    // Binding { target: metadata; property: 'title'; value: title_textfield.text }

                    Label {
                        text: qsTr('Authors')
                    }
                    Widgets.TextField {
                        id: authors_textfield
                        Layout.fillWidth: true
                        onEditingFinished: metadata.authors = text
                    }
                    // Binding { target: metadata; property: 'authors'; value: authors_textfield.text }

                    Label {
                        text: qsTr('Publisher')
                    }
                    Widgets.TextField {
                        id: publisher_textfield
                        Layout.fillWidth: true
                        onEditingFinished: metadata.publisher = text
                    }
                    // Binding { target: metadata; property: 'publisher'; value: publisher_textfield.text }

                    Label {
                        text: qsTr('Language')
                    }
                    Widgets.TextField {
                        id: language_textfield
                        Layout.fillWidth: true
                        onEditingFinished: metadata.language = text
                    }
                    // Binding { target: metadata; property: 'language'; value: language_textfield.text }

                    Label {
                        text: qsTr('Number of pages')
                    }
                    SpinBox {
                        id: number_of_pages_spin_box
                        from: 0
                        to: 1000
                        editable: true
                        onValueModified: metadata.number_of_pages = value
                    }
                    // Binding { target: metadata; property: 'number_of_pages'; value: number_of_pages_spin_box.value }

                    Label {
                        text: qsTr('Page Offset')
                    }
                    SpinBox {
                        id: page_offset_spinbox
                        from: 1
                        to: 1000
                        editable: true
                        onValueModified: metadata.page_offset = value
                    }
                    // Binding { target: metadata; property: 'page_offset'; value: page_offset_spinbox.value }

                    Label {
                        text: qsTr('Year')
                    }
                    SpinBox {
                        id: year_spinbox
                        from: 0
                        to: 2100
                        editable: true
                        // Redefine textFromValue else it shows '2 019'
                        textFromValue: function(value, locale) { return value.toString(); }
                        onValueModified: metadata.year = value
                    }
                    // Binding { target: metadata; property: 'year'; value: year_spinbox.value }

                    Label {
                        text: qsTr('Keywords')
                    }
                    Widgets.TextField {
                        id: keywords_textfield
                        Layout.fillWidth: true
                        onEditingFinished: metadata.keywords = text
                    }
                    // Binding { target: metadata; property: 'keywords'; value: keywords_textfield.text }

                    Label {
                        text: qsTr('Description')
                    }
                    Widgets.TextField {
                        id: description_textfield
                        Layout.fillWidth: true
                        onEditingFinished: metadata.description = text
                    }
                    // Binding { target: metadata; property: 'description'; value: description_textfield.text }


                    Label {
                        text: qsTr('Notes')
                    }
                    RowLayout {
                        Layout.fillWidth: true

                        TextArea {
                            id: notes_textarea
                            Layout.fillWidth: true
                            Layout.preferredHeight: contentHeight // Fixme:
                            Layout.minimumHeight: 200
                            wrapMode: TextEdit.Wrap
                            textFormat: TextEdit.RichText
                            readOnly: true

                            // Fixme:
                            background: Rectangle {
                                border.color: '#21be2b'
                            }
                        }

                        TextArea {
                            id: notes_editor
                            visible: false
                            Layout.fillWidth: true
                            Layout.preferredHeight: contentHeight
                            Layout.minimumHeight: 200
                            wrapMode: TextEdit.Wrap
                            textFormat: TextEdit.PlainText

                            background: Rectangle {
                                border.color: Style.color.danger
                            }

                            Keys.onEscapePressed: {
                                focus = false
                                event.accepted = true
                            }

                            onEditingFinished: {
                                metadata.notes = text
                                notes_textarea.text = metadata.notes_html
                                // swap
                                notes_editor.visible = false
                                notes_textarea.visible = true
                            }
                        }

                        Widgets.WarnedToolButton {
                            id: notes_edit_button
                            Layout.alignment: Qt.AlignTop
                            icon.name: 'edit-black'
                            tip: qsTr('Edit metadata')
                            icon.color: warned ? Style.color.danger : 'black'

                            warned: notes_editor.focus

                            // When a user click on button while the editor has focus, signal order is
                            //   1) editor.onEditingFinished !!!
                            //   2) button.onFocuschanged
                            //   3) editor.onFocuschanged
                            //   4) button.onPressed
                            //   5) button.onClicked

                            onClicked: {
                                // swap and set focus
                                notes_textarea.visible = false
                                notes_editor.visible = true
                                notes_editor.focus = true
                            }
                        }
                    }
                }
            }
        }
    }
}
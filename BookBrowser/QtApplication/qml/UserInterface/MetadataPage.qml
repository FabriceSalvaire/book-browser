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

Page {

    /*******************************************************
     *
     * API
     *
     */

    property var metadata: application.book.metadata

    /******************************************************/

    Component.onCompleted: {
    }

    /******************************************************/

    id: root

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20

        Widgets.ToolButtonTip {
            icon.source: 'qrc:/icons/save-black.png'
            tip: qsTr('Save')
            onClicked: metadata.save()
        }

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            ScrollBar.horizontal.policy: ScrollBar.AsNeeded

            GridLayout {
                width: parent.width
                columns: 2
                columnSpacing: 10

                Label {
                    text: qsTr('ISBN')
                }
                RowLayout {
                    TextField {
                        id: isbn_textfield
                        Layout.fillWidth: true
                        text: metadata.isbn
                    }

                    Widgets.ToolButtonTip {
                        icon.source: 'qrc:/icons/refresh-black.png'
                        tip: qsTr('Query ISBN')
                        onClicked: metadata.query_isbn()
                    }
                }
                Binding { target: metadata; property: 'isbn'; value: isbn_textfield.text }

                Label {
                    text: qsTr('Path')
                }
                Label {
                    text: metadata.path
                }

                Label {
                    text: qsTr('Title')
                }
                TextField {
                    id: title_textfield
                    text: metadata.title
                }
                Binding { target: metadata; property: 'title'; value: title_textfield.text }

                Label {
                    text: qsTr('Authors')
                }
                TextField {
                    id: authors_textfield
                    text: metadata.authors
                }
                Binding { target: metadata; property: 'authors'; value: authors_textfield.text }

                Label {
                    text: qsTr('Publisher')
                }
                TextField {
                    id: publisher_textfield
                    text: metadata.publisher
                }
                Binding { target: metadata; property: 'publisher'; value: publisher_textfield.text }

                Label {
                    text: qsTr('Language')
                }
                TextField {
                    id: language_textfield
                    text: metadata.language
                }
                Binding { target: metadata; property: 'language'; value: language_textfield.text }

                Label {
                    text: qsTr('Number of pages')
                }
                SpinBox {
                    id: number_of_pages_spin_box
                    from: 0
                    to: 1000
                    value: metadata.number_of_pages
                }
                Binding { target: metadata; property: 'number_of_pages'; value: number_of_pages_spin_box.value }

                Label {
                    text: qsTr('Page Offset')
                }
                SpinBox {
                    id: page_offset_spinbox
                    from: 1
                    to: 1000
                    value: metadata.page_offset
                }
                Binding { target: metadata; property: 'page_offset'; value: page_offset_spinbox.value }

                Label {
                    text: qsTr('Year')
                }
                SpinBox {
                    id: year_spinbox
                    from: 0
                    to: 2100
                    value: metadata.year
                }
                Binding { target: metadata; property: 'year'; value: year_spinbox.value }

                Label {
                    text: qsTr('Keywords')
                }
                TextField {
                    id: keywords_textfield
                    text: metadata.keywords
                }
                Binding { target: metadata; property: 'keywords'; value: keywords_textfield.text }

                Label {
                    text: qsTr('Description')
                }
                TextField {
                    id: description_textfield
                    text: metadata.description
                }
                Binding { target: metadata; property: 'description'; value: description_textfield.text }
            }
        }
    }
}

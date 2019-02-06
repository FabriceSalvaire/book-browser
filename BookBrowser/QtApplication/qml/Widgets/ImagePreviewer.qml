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

Image {
    id: image_preview

    // anchors.fill: parent
    // horizontalAlignment: Image.AlignLeft
    // verticalAlignment: Image.AlignTop

    fillMode: Image.PreserveAspectFit

    signal image_ready()

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
        if (status === Image.Ready)
	    image_ready()
    }


    Rectangle {
	id: selection_area
	visible: false
	color: '#aaaaaaff'
	x: 0
	y: 0
	width: 100
	height: 100
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

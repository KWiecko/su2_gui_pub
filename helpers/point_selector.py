# Author: Gael Varoquaux <gael dot varoquaux at normalesup.org>
# Copyright (c) 2009, Enthought, Inc.
# License: BSD style.

import inspect
import numpy as np
from mayavi import mlab
from pynput.keyboard import Controller
from tvtk.api import tvtk

################################################################################
# Disable the rendering, to get bring up the figure quicker:
figure = mlab.gcf()
mlab.clf()
figure.scene.disable_render = True

# Creates two set of points using mlab.points3d: red point and
# white points
x1, y1, z1 = np.random.random((3, 10))
red_glyphs = mlab.points3d(x1, y1, z1, color=(1, 0, 0),
                resolution=40, scale_factor=0.1)

x2, y2, z2 = np.random.random((3, 10))
white_glyphs = mlab.points3d(x2, y2, z2, color=(0.9, 0.9, 0.9),
                resolution=40)

# Add an outline to show the selected point and center it on the first
# data point.
outline = mlab.outline(line_width=3)
outline.outline_mode = 'cornered'
outline.bounds = (x1[0]-0.1, x1[0]+0.1,
                  y1[0]-0.1, y1[0]+0.1,
                  z1[0]-0.1, z1[0]+0.1)

# Every object has been created, we can reenable the rendering.
figure.scene.disable_render = False
################################################################################


# Here, we grab the points describing the individual glyph, to figure
# out how many points are in an individual glyph.
glyph_points = red_glyphs.glyph.glyph_source.glyph_source.output.points.to_array()

print('glyph_points')
print(glyph_points)


def add_red_point(new_p_coords: list, red_glyphs):
    curr_points = np.array(red_glyphs.mlab_source.get('points')['points'])
    new_point = np.array(new_p_coords)
    appnd_p_list = np.vstack((curr_points, np.reshape(new_point, (1, 3))))

    # print('\n\nraw glyph list')
    # # # print(list(curr_points)[-5:])
    # #
    # for el in list(curr_points)[-5:]:
    #     print(el)
    # #
    # print('\n\nappended glyph list')
    # # # print(list(appnd_p_list)[-6:])
    # #
    # for el in list(appnd_p_list)[-6:]:
    #     print(el)

    red_glyphs.mlab_source.set(points=appnd_p_list)


def remove_red_point(to_rmv_point_id: int, red_glyphs):
    curr_points = np.array(red_glyphs.mlab_source.get('points')['points'])

    pass


def picker_callback(picker):
    """ Picker callback: this get called when on pick events.
    """
    # check for point picking
    point_id = picker.point_id / glyph_points.shape[0]
    print('point_id, picker.point_id')
    print(point_id, picker.point_id)
    print('glyph_points.shape')
    print(glyph_points.shape)
    coords = picker.pick_position

    if Controller.shift_pressed:
        print('shift press detected')

    # if picker.actor in red_glyphs.actor.actors:
    # Find which data point corresponds to the point picked:
    # we have to account for the fact that each data point is
    # represented by a glyph with several points

    # print('true point id')
    # print(picker.point_id)

    point_id = picker.point_id/glyph_points.shape[0]
    # print(point_id)
    # If the no points have been selected, we have '-1'
    if point_id != -1:
        int_point_id = int(round(point_id, 0))

        # print('coords')
        # print(coords)
        # input('debug')
        add_red_point(new_p_coords=coords, red_glyphs=red_glyphs)
        # Retrieve the coordinnates coorresponding to that data
        # point
        # print('int_point_id')
        # print(int_point_id)
        x, y, z = x1[int_point_id], y1[int_point_id], z1[int_point_id]
        # Move the outline to the data point.
        outline.bounds = (x-0.1, x+0.1,
                          y-0.1, y+0.1,
                          z-0.1, z+0.1)


picker = figure.on_mouse_pick(picker_callback)

# Decrease the tolerance, so that we can more easily select a precise
# point.
picker.tolerance = 0.01

mlab.title('Click on red balls')


surf_points = np.array([[0,0,0], [1,0,0], [0,1,0], [0,0,1], # tetra
                    [2,0,0], [3,0,0], [3,1,0], [2,1,0],
                    [2,0,1], [3,0,1], [3,1,1], [2,1,1], # Hex
                       # [5, 4, 1], [10, 1, 9], [8, 8, 8]
                    ], 'f')

# shift the points so we can show both.
surf_points[:,1] += 2.0
# The cells
cells = np.array([4, 0, 1, 2, 3, # tetra
               8, 4, 5, 6, 7, 8, 9, 10, 11, # hex
                3, 3, 1, 5
               ])
# The offsets for the cells, i.e. the indices where the cells
# start.
# offset = np.array([0, 5, 14])
offset = np.array([0, 5, 14])
tetra_type = tvtk.Tetra().cell_type  # VTK_TETRA == 10
hex_type = tvtk.Hexahedron().cell_type  # VTK_HEXAHEDRON == 12
cell_types = np.array([tetra_type, hex_type, 5])
# Create the array of cells unambiguously.
cell_array = tvtk.CellArray()
cell_array.set_cells(3, cells)
print('cell_array')
print(cell_array)
# Now create the UG.
ug = tvtk.UnstructuredGrid(points=surf_points)
# Now just set the cell types and reuse the ug locations and cells.
ug.set_cells(cell_types, offset, cell_array)
mlab.pipeline.surface(ug)
# mlab.show()

mlab.show()

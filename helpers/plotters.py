import numpy as np
from mayavi import mlab
from mayavi.modules.surface import Surface
import plotly.figure_factory as FF
import pandas as pd
import plotly.graph_objs as go
from tvtk.api import tvtk

from helpers.helpers import get_pts_cg, get_xyz_coords_frm_sets, \
    subset_points_using_surf


def get_surf_for_points(
        points: list, trace_name: str, trace_color: str, trace_opacity: float):
    """
    getter for 3D surface object plot (mesh-surface intended)
    Parameters
    ----------
    trace_name: str
        name for data series
    trace_color: str
        color for plotted surface
    trace_opacity: float
        0-1 color

    Returns
    -------
    go.Mesh3d
        trace object for provided 3D data

    """

    x_coords, y_coords, z_coords = \
        get_sep_xyz_series_frm_points(points=points)

    trace = go.Scatter3d(x=x_coords, y=y_coords, z=z_coords,
                         opacity=trace_opacity,
                         name=trace_name,
                         mode='markers',
                         marker=dict(size=3))
    # color=trace_color)
    return trace


def get_sep_xyz_series_frm_points(points: list):
    """
    getter for separate x, y, z coord series from provided points list

    Parameters
    ----------
    points: list
        list of entries of Point class

    Returns
    -------
    tuple
        <pd.Series of x coords, pd.Series of y coords, pd.Series of z coords>

    """
    x_coords = []  # pd.Series()
    y_coords = []  # pd.Series()
    z_coords = []  # pd.Series()

    coord_s_iterable = tuple((x_coords, y_coords, z_coords))
    ids = []
    for point in points:
        p_id = point.point_id
        ids.append(p_id)
        for coord_list, coord in zip(coord_s_iterable, point.get_coords()):
            # coord_series.put(p_id, coord)  # [p_id] = coord
            coord_list.append(coord)

    x_series = pd.Series(data=x_coords, index=ids)
    y_series = pd.Series(data=y_coords, index=ids)
    z_series = pd.Series(data=z_coords, index=ids)
    return x_series, y_series, z_series


def get_3d_scatter_trace(
        x: list, y: list, z: list, labels: list, plot_type: str = 'lines'):
    return go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode=plot_type,
        text=labels,
        # ['77', '55999', '4724', '79'],
        marker=dict(
            size=5,
            line=dict(
                color='rgba(217, 217, 217, 0.14)',
                width=0.5
            ),
            opacity=0.8
        )
    )


def get_3d_mesh_trace(x: list, y: list, z: list):

    return go.Mesh3d(
        x=x, y=y, z=z, opacity=0.5)


def plot_single_el(single_el_nodes, all_pts):
    tetra_type = tvtk.Tetra().cell_type  # VTK_TETRA == 10
    pyra_type = tvtk.Pyramid().cell_type
    prism_type = tvtk.PentagonalPrism().cell_type

    if len(single_el_nodes) - 1 == 4:
        el_type = tetra_type
    elif len(single_el_nodes) - 1 == 5:
        el_type = pyra_type
    else:
        el_type = prism_type

    points = [all_pts[node_id - 1][1:] for node_id in single_el_nodes[1:]]
    print(points)
    nodes = \
        [len(single_el_nodes) - 1] + list(range(0, len(single_el_nodes) - 1))
    print(nodes)
    cell_types = [el_type]
    cells = tvtk.CellArray()
    offsets = [0]
    cells.set_cells(1, nodes)
    ug = tvtk.UnstructuredGrid(points=points)
    ug.set_cells(cell_types, offsets, cells)

    ug.point_data.scalars = \
        [el for el in range(len(points))]  # scalars
    ug.point_data.scalars.name = 'scalars'

    mlab.pipeline.surface(ug, opacity=0.75)
    mlab.pipeline.surface(
        ug, representation='wireframe', color=(0, 0, 0), line_width=0.5)
    mlab.show()


def get_3d_maya_mesh(
        els_nodes_list: list, all_points: list, normals: list):

    tri_type = tvtk.Triangle().cell_type
    tetra_type = tvtk.Tetra().cell_type  # VTK_TETRA == 10
    pyra_type = tvtk.Pyramid().cell_type
    # print('tri_type')
    # print(tri_type)
    quad_type = tvtk.Quad().cell_type
    cells = tvtk.CellArray()
    # cell_types = np.array([tri_type, quad_type])
    # cells.from_array(els_nodes_list)

    new_all_surf_pts, new_all_nodes_per_walls = subset_points_using_surf(
        all_pts=all_points, nodes_per_walls=els_nodes_list)

    # print('SANITY CHECK')
    # print(els_nodes_list[:10])
    # print(new_all_nodes_per_walls[:10])
    #
    # for old_node_id, new_node_id \
    #         in zip(els_nodes_list[:10], new_all_nodes_per_walls[:10]):
    #     print('OLD NODE DESIG POINT')
    #     print(all_points[old_node_id])
    #     print('NEW NODE DESIG POINT')
    #     print(new_all_surf_pts[new_node_id])

    all_nodes = []
    offsets = []
    cell_types = []

    # plain_nodes = np.unique(np.array(els_nodes_list).flatten())
    # surface_points = [points_per_el_list[node_id] for node_id in plain_nodes]
    # print(els_nodes_list[: 10])

    for wall_el_nodes in new_all_nodes_per_walls:

        curr_el_node_count = 0
        if len(wall_el_nodes) == 3:
            curr_el_node_count = 3
            cell_types.append(tri_type)
        else:
            curr_el_node_count = 4
            cell_types.append(quad_type)

        offsets.append(len(all_nodes))
        curr_wall_el_line = [curr_el_node_count] + list(wall_el_nodes)

        all_nodes += curr_wall_el_line

    # print('all_nodes')
    # print(all_nodes[:20])
    # print('offsets')
    # print(offsets)

    cells.set_cells(len(new_all_nodes_per_walls), all_nodes)

    # print(cells)
    # print(len(all_nodes))
    # print(len(offsets))
    # print(len(cell_types))
    # print(len(new_all_surf_pts))

    # offset = np.array(range(0, len(els_nodes_list)))

    # print('SURF PLT SANITY CHECK')
    # print(els_nodes_list[0: 5])
    # print(points_per_el_list[:5])
    # print(normals[:5])
    # print(offset[0:5])
    #
    # print(len(els_nodes_list))
    # print(len(points_per_el_list))
    # print(len(normals))
    #
    # input('DEBUG PLT ENDS')

    # print('setting points')
    ug = tvtk.UnstructuredGrid(points=new_all_surf_pts)
    # ug = tvtk.UnstructuredGrid(points=surface_points)

    # print('done')
    # print('setting cells')
    # ug.set_cells(cell_types, offsets, cells)
    ug.set_cells(cell_types, offsets, cells)
    # print('done')
    # input('test')
    # scalars = random.random(points.shape[0])
    ug.point_data.scalars = \
        [1 for el in new_all_surf_pts]  # scalars
    ug.point_data.scalars.name = 'scalars'

    # surf = mlab.pipeline.surface(ug, opacity=0.5)
    # print('creating surf plot')
    # mlab.surf(ug, representation='wireframe')  # , opacity=0.5)
    mlab.pipeline.surface(ug, opacity=0.75)
    mlab.pipeline.surface(
        ug, representation='wireframe', color=(0, 0, 0), line_width=0.5)
    #  , representation='points', opacity=0.5, color=(1, 1, 1))
    # mlab.show()
    # mlab.show()
    # print('surf creation is done')
    # , representation='wireframe')
    # surf.contours.filled_contours = True

    x_cg_coords, y_cg_coords, z_cg_coords = \
        get_pts_cg(els_nodes_list, all_points, skip_first=False)
    # input('DEBUG CG ENDS')
    # normals_scaled = [[coord / 100 for coord in vect] for vect in normals]
    u_norms, v_norms, w_norms = \
        get_xyz_coords_frm_sets(normals, skip_first=False)
    # input('DEBUG NORMS ENDS')

    mlab.quiver3d(
        x_cg_coords, y_cg_coords, z_cg_coords, u_norms, v_norms, w_norms,
        line_width=0.75,
        scale_factor=0.02)  # , mode='2dtriangle')
    mlab.show()

    pass


if __name__ == '__main__':
    # import numpy as np
    # from mayavi import mlab

    points = np.array([[0,0,0], [1,0,0], [0,1,0], [0,0,1], # tetra
                    [2,0,0], [3,0,0], [3,1,0], [2,1,0],
                    [2,0,1], [3,0,1], [3,1,1], [2,1,1], # Hex
                       # [5, 4, 1], [10, 1, 9], [8, 8, 8]
                    ], 'f')

    print(points)
    # shift the points so we can show both.
    points[:,1] += 2.0
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
    ug = tvtk.UnstructuredGrid(points=points)
    # Now just set the cell types and reuse the ug locations and cells.
    ug.set_cells(cell_types, offset, cell_array)
    mlab.pipeline.surface(ug)
    mlab.show()
    # return ug

    # p0 = [0.799319, -3.477045e-01, 0.490093]
    # p1 = [0.852512, 9.113778e-16, -0.522708]
    # p2 = [0.296422, 9.376042e-01, 0.181748]
    #
    # origin = [0, 0, 0]
    # X, Y, Z = zip(origin, origin, origin)
    # U, V, W = zip(p0, p1, p2)
    # #
    # # nodes = [
    # #     [1, 0, 0],
    # #     [0, 1, 0],
    # #     [-1, 0, 0],
    # #     [0, -1, 0],
    # #     [0, 0, 1]]
    # #
    # # mlab.surf(nodes)
    # # mlab.show()
    #
    # # mlab.quiver3d(X, Y, Z, U, V, W)
    # # mlab.show()
    #
    # # from mayavi import mlab
    # # import numpy as np
    # #
    # # a = np.random.random((4, 4))
    # # print(a)
    # # mlab.surf(a)
    # # mlab.show()
    #
    # from numpy import array, random
    # from tvtk.api import tvtk
    #
    # # The numpy array data.
    # # points = array([[0, -0.5, 0], [1.5, 0, 0], [0, 1, 0], [0, 0, 0.5],
    # #                 [-1, -1.5, 0.1], [0, -1, 0.5], [-1, -0.5, 0],
    # #                 [1, 0.8, 0]], 'f')
    # points = array(
    #     [[1, 0, 0],                 # 0
    #      [0, 1, 0],                 # 1
    #      [-1, 0, 0],                 # 2
    #      [0, -1, 0],                 # 3
    #      [0, 0, 1],
    #      [1, 1, 1],
    #      [0, 0, 0]], 'f')                 # 4
    #
    # # triangles = array([[0, 1, 2], [0, 1, 4], [1, 2, 4],
    # #                    [2, 3, 4], [3, 0, 4]])
    # # scalars = random.random(points.shape)
    # #
    # # # The TVTK dataset.
    # # mesh = tvtk.PolyData(points=points, polys=triangles)
    # # mesh.point_data.scalars = scalars
    # # mesh.point_data.scalars.name = 'scalars'
    # #
    # # mlab.pipeline.surface(mesh)
    # # mlab.show()
    #
    # # cells = array([14, 0, 1, 2, 3, 4  # tetra
    # #                # 8, 4, 5, 6, 7, 8, 9, 10, 11  # hex
    # #                ])
    # # # The offsets for the cells, i.e. the indices where the cells
    # # # start.
    #
    # tetra_type = tvtk.Tetra().cell_type  # VTK_TETRA == 10
    # hex_type = tvtk.Hexahedron().cell_type  # VTK_HEXAHEDRON == 12
    # pyra_type = tvtk.Pyramid().cell_type
    # prism_type = tvtk.PentagonalPrism().cell_type
    # tri_type = tvtk.Triangle().cell_type
    # quad_type = tvtk.Quad().cell_type
    # #
    # # print(pyra_type, prism_type)
    # #
    # # cell_types = array([tetra_type, hex_type])
    # cell_types = array([tri_type, quad_type])
    # # # Create the array of cells unambiguously.
    # # cell_array = tvtk.CellArray()
    # # cell_array.set_cells(1, cells)
    # # # # Now create the UG.
    # # ug = tvtk.UnstructuredGrid(points=points)
    # # # Now just set the cell types and reuse the ug locations and cells.
    # # ug.set_cells(cell_types, offset, cell_array)
    # # scalars = random.random(points.shape[0])
    # # ug.point_data.scalars = scalars
    # # ug.point_data.scalars.name = 'scalars'
    # #
    # # mlab.pipeline.surface(ug)
    # # mlab.show()
    #
    # # a = [[0], [1, 2], [3, 4, 5], [6, 7, 8, 9]]
    #
    # # a = [[0, 1, 2, 3]]
    # a = [[0, 1, 4], [0, 1, 2, 3]]
    # cells = tvtk.CellArray()
    # cells.from_array(a)
    # ug = tvtk.UnstructuredGrid(points=points)
    #
    # offset = array([0, 1])
    # ug.set_cells(cell_types, offset, cells)
    #
    # scalars = random.random(points.shape[0])
    # ug.point_data.scalars = [1 for el in range(points.shape[0])]  # scalars
    # ug.point_data.scalars.name = 'scalars'
    #
    # surf = mlab.pipeline.surface(ug, opacity=0.5)  # , representation='wireframe')
    # # surf.contours.filled_contours = True
    #
    # mlab.quiver3d(X, Y, Z, U, V, W, line_width=2)  # , mode='2dtriangle')
    # mlab.show()
    #
    # # print(cells)
    # # a = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]], int)
    # # cells.from_array(a)
    # # l_a = [a[:, :1], a[:2, :2], a]
    # # cells.from_array(a)
    # s2 = Surface()
    # s2.actor.property.trait_set(representation='surface', opacity=0.2)

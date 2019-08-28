import itertools
# import keyboard
from mayavi import mlab
import numpy as np
from pynput.keyboard import Key, Controller
from pynput import keyboard
# import pygame
import re
from tvtk.api import tvtk
import os

from helpers.helpers import read_all_lines, prcs_collection_w_np, \
    subset_points_using_surf
from helpers.mesh_helpers import find_entries_range_and_count, \
    get_all_boundaries_info, add_mayavi_point, remove_last_mayavi_point


class SU2MeshSurfPlotter:

    ffd_mayavi_points_plt = None
    all_points_scatter_plt = None
    # keyboard = Controller()

    @property
    def ignored_surfs_rgx(self):
        return self._ignored_surfs_rgx

    @ignored_surfs_rgx.setter
    def ignored_surfs_rgx(self, new_val: str):
        self._ignored_surfs_rgx = new_val

    @property
    def pth_to_msh(self) -> str:
        return self._pth_to_msh

    @pth_to_msh.setter
    def pth_to_msh(self, new_val: str):
        self._pth_to_msh = new_val

    @property
    def all_su2_msh_lines(self) -> np.array:
        return self._all_su2_msh_lines

    @all_su2_msh_lines.setter
    def all_su2_msh_lines(self, new_val: np.array):
        self._all_su2_msh_lines = new_val

    @property
    def all_msh_points_np(self) -> np.array:
        return self._all_msh_points_np

    @all_msh_points_np.setter
    def all_msh_points_np(self, new_val: np.array):
        self._all_msh_points_np = new_val

    @property
    def all_bounds(self) -> dict:
        return self._all_bounds

    @all_bounds.setter
    def all_bounds(self, new_val: dict):
        self._all_bounds = new_val

    @property
    def allwd_colours(self) -> list:
        return self._allwd_colours

    @allwd_colours.setter
    def allwd_colours(self, new_val: list):
        self._allwd_colours = new_val

    def __init__(self, pth_to_msh: str, ignored_surfs_rgx: str = '^FF|^SYMM'):
        self.pth_to_msh = pth_to_msh
        self.all_bounds = {}
        self.ignored_surfs_rgx = ignored_surfs_rgx
        self.set_allwd_colours()

    def read_su2_msh(self):
        with open(self.pth_to_msh, 'r') as su2_msh_f:
            # self.all_su2_msh_lines = read_all_lines(su2_msh_f)
            self.all_su2_msh_lines = np.array(su2_msh_f.readlines())
            # print(len(self.all_su2_msh_lines))
            # print(self.all_su2_msh_lines[0])
            # print(self.all_su2_msh_lines[-1])

    @staticmethod
    def get_point_np_arr_frm_str(point_str: str):
        # print(point_str)

        coords_list = [float(coord.strip()) for coord in point_str.split('\t')]
        # print(coords_list)

        np_coords_arr = np.array(coords_list)
        # print(np_coords_arr)

        return np_coords_arr

    def set_allwd_colours(self):
        self.allwd_colours = \
            list(el for el in itertools.permutations(
                [0, 0.25, 0.5, 0.75, 1], 3))

    def set_all_points(self):
        print('SETTING ALL POINTS')
        first_pts_line_idx, last_pts_line_idx, all_pts_count = \
            find_entries_range_and_count(
                self.all_su2_msh_lines, entries_marker='^NPOIN=')

        all_pts_subst = \
            self.all_su2_msh_lines[first_pts_line_idx:last_pts_line_idx + 1]

        all_np_pts = \
            prcs_collection_w_np(
                input_collection=all_pts_subst,
                col_el_transformer=SU2MeshSurfPlotter.get_point_np_arr_frm_str)

        self.all_msh_points_np = all_np_pts
        print('SETTING ALL POINTS - DONE')

    def set_all_boundaries(self):
        print('SETTING ALL BOUNDS')
        all_bounds = get_all_boundaries_info(self.all_su2_msh_lines)

        no_ids_pts = np.array([el[:-1] for el in self.all_msh_points_np])

        prcsd_bounds = {}

        for bound_name, bound_info in all_bounds.items():

            bound_strt_ixd = bound_info['bound_start_line_idx']
            bound_end_ixd = bound_info['bound_end_line_idx']

            bound_lines = \
                self.all_su2_msh_lines[bound_strt_ixd:bound_end_ixd + 1]

            all_bound_nodes = []
            el_types = []

            for el_wall_line in bound_lines:

                el_wall_line_list = \
                    [int(node_id.strip())
                     for node_id in el_wall_line.split('\t')]

                el_wall_type = el_wall_line_list[0]
                el_types.append(el_wall_type)

                el_wall_nodes_ids = el_wall_line_list[1:]

                all_bound_nodes.append(el_wall_nodes_ids)

            curr_bound_points, bound_walls = subset_points_using_surf(
                all_pts=no_ids_pts, nodes_per_walls=all_bound_nodes)

            els_mayavi_def = []
            offsets = []

            for bound_wall in bound_walls:
                offsets.append(len(els_mayavi_def))

                els_mayavi_def += [len(bound_wall)] + list(bound_wall)
                # els_mayavi_def.append(curr_bound_wall_def)

            curr_bound_desc = {
                'bound_points': curr_bound_points,
                'els_mayavi_def': els_mayavi_def,
                'offsets': offsets,
                'el_types': el_types}

            self.all_bounds[bound_name] = curr_bound_desc

        print('SETTING ALL BOUNDS - DONE')
        # print('TEST ALL POINTS SUBSET')
        # print(all_np_pts[0])
        # print(all_np_pts[-1])

    def _set_ffd_points_obj(self):

        x_s = np.array([])
        y_s = np.array([])
        z_s = np.array([])

        SU2MeshSurfPlotter.ffd_mayavi_points_plt = \
            mlab.points3d(
                x_s, y_s, z_s, color=(1, 0, 0), resolution=40, scale_factor=0.01)

    def _make_grid_frm_limits(
            self, x_coords, y_coords, z_coords, dist_fact=0.05):

        min_x_a = min(x_coords)
        max_x_a = max(x_coords)

        x_diff = max_x_a - min_x_a

        min_y_a = min(y_coords)
        max_y_a = max(y_coords)

        y_diff = max_y_a - min_y_a

        min_z_a = min(z_coords)
        max_z_a = max(z_coords)

        z_diff = max_z_a - min_z_a

        largest_dim = -1

        for dim in [x_diff, y_diff, z_diff]:
            if dim >= largest_dim:
                largest_dim = dim

        d_dim = round(largest_dim * dist_fact, 4)

        x_divs_coords = \
            self._get_singe_axis_divs(
                dim_diff=x_diff,
                d_dim=d_dim,
                min_dim=min_x_a,
                max_dim=max_x_a)
        y_divs_coords = \
            self._get_singe_axis_divs(
                dim_diff=y_diff,
                d_dim=d_dim,
                min_dim=min_y_a,
                max_dim=max_y_a)
        z_divs_coords = \
            self._get_singe_axis_divs(
                dim_diff=z_diff,
                d_dim=d_dim,
                min_dim=min_z_a,
                max_dim=max_z_a)

        x_grid_a, y_grid_a, z_grid_a = \
            self._get_xyz_grid_points(
                x_divs_coords=x_divs_coords, y_divs_coords=y_divs_coords,
                z_divs_coords=z_divs_coords)

        # print(x_divs_coords)
        # print(y_divs_coords)
        # print(z_divs_coords)

        # x_grid_count = int(x_diff / d_dim)
        #
        # for diff_count in range(x_grid_count + 1, 1):
        #     x_grid.append(diff_count * d_dim)
        # x_grid.append(max_x_a)

        return x_grid_a, y_grid_a, z_grid_a

    def get_xyz_from_poitns(self, points):
        x = []
        y = []
        z = []

        for x_corod, y_coord, z_coord in points:
            x.append(x_corod)
            y.append(y_coord)
            z.append(z_coord)

        return x, y, z

    def _get_xyz_grid_points(self, x_divs_coords, y_divs_coords, z_divs_coords):
        x_grid = []
        y_grid = []
        z_grid = []

        for x_div_coord in x_divs_coords:
            for y_div_coord in y_divs_coords:
                for z_div_coord in z_divs_coords:
                    x_grid.append(x_div_coord)
                    y_grid.append(y_div_coord)
                    z_grid.append(z_div_coord)

        return x_grid, y_grid, z_grid

    def _get_singe_axis_divs(
            self, dim_diff, d_dim, min_dim, max_dim, offset_count: int = 1):
        dim_grid = []
        dim_grid_count = int(dim_diff / d_dim)

        for diff_count in \
                range(0 - offset_count, dim_grid_count + offset_count + 1, 1):
            curr_dim_grid_coord = round(min_dim + diff_count * d_dim, 6)
            dim_grid.append(curr_dim_grid_coord)
        dim_grid.append(max_dim)
        return dim_grid

    def _set_all_pts_scatter_obj(self):

        x_a = []
        y_a = []
        z_a = []

        for x_coord, y_coord, z_coord, point_id in self.all_msh_points_np:
            x_a.append(x_coord)
            y_a.append(y_coord)
            z_a.append(z_coord)

        x_grid, y_grid, z_grid = \
            self._make_grid_frm_limits(x_coords=x_a, y_coords=y_a, z_coords=z_a)

        SU2MeshSurfPlotter.all_points_scatter_plt = \
            mlab.points3d(
                np.array(x_grid),
                np.array(y_grid),
                np.array(z_grid),
                color=(0, 0, 0), resolution=5, scale_factor=0.01, opacity=1)

    def get_scatter_from_points(self, input_xyz_points: np.array):
        x_s = []
        y_s = []
        z_s = []

        for x_coord, y_coord, z_coord in input_xyz_points:
            x_s.append(x_coord)
            y_s.append(y_coord)
            z_s.append(z_coord)

        return mlab.points3d(
                np.array(x_s),
                np.array(y_s),
                np.array(z_s),
                color=(0, 1, 0), resolution=5, scale_factor=0.0005)

    def get_scatter_from_vects(self, x, y, z, opacity: float = 1.0):
        return mlab.points3d(
                np.array(x),
                np.array(y),
                np.array(z),
                color=(0, 0, 0), resolution=10, scale_factor=0.0015,
                opacity=opacity)

        # return selected_points

    def plot_all_boundaries(
            self, dist_fact=0.025, plot_points: bool = True,
            surf_opacity: float = 1.0, reset_fig: bool = True):

        figure = mlab.gcf()
        if reset_fig:
            mlab.clf()
            figure.scene.disable_render = True

        self._set_ffd_points_obj()
        # self._set_all_pts_scatter_obj()

        picker_left = \
            figure.on_mouse_pick(SU2MeshSurfPlotter.left_picker_callback)
        picker_left.tolerance = 0.01

        picker_right = \
            figure.on_mouse_pick(
                callback=SU2MeshSurfPlotter.right_picker_callback,
                button='Right')
        picker_right.tolerance = 0.01

        all_b_x_min = 999999
        all_b_x_max = -999999

        all_b_y_min = 999999
        all_b_y_max = -999999

        all_b_z_min = 999999
        all_b_z_max = -999999

        for bound_name, bound_mayavi_desc in self.all_bounds.items():

            if re.search(self.ignored_surfs_rgx, bound_name):
                continue

            print('Processing {}'.format(bound_name))

            curr_points = np.array(bound_mayavi_desc['bound_points'])
            curr_bound_walls = np.array(bound_mayavi_desc['els_mayavi_def'])
            curr_bound_offsets = np.array(bound_mayavi_desc['offsets'])
            curr_el_types = np.array(bound_mayavi_desc['el_types'])

            x_b_pts, y_b_pts, z_b_pts = self.get_xyz_from_poitns(curr_points)

            if min(x_b_pts) < all_b_x_min:
                all_b_x_min = min(x_b_pts)
            if max(x_b_pts) > all_b_x_max:
                all_b_x_max = max(x_b_pts)

            if min(y_b_pts) < all_b_y_min:
                all_b_y_min = min(y_b_pts)
            if max(y_b_pts) > all_b_y_max:
                all_b_y_max = max(y_b_pts)

            if min(z_b_pts) < all_b_z_min:
                all_b_z_min = min(z_b_pts)
            if max(z_b_pts) > all_b_z_max:
                all_b_z_max = max(z_b_pts)

            # curr_scatter = \
            #     self.get_scatter_from_points(input_xyz_points=curr_points)

            cells = tvtk.CellArray()

            # print('curr_points[:5]')
            # print(curr_points[:5])
            # print('curr_bound_walls[:5]')
            # print(curr_bound_walls[:5])
            # print('curr_bound_offsets[:5]')
            # print(curr_bound_offsets[:5])
            # print('curr_el_types[:5]')
            # print(curr_el_types[:5])

            cells.set_cells(len(curr_el_types), curr_bound_walls)

            ug = tvtk.UnstructuredGrid(points=curr_points)
            ug.set_cells(curr_el_types, curr_bound_offsets, cells)
            ug.point_data.scalars = \
                [1 for el in curr_points]  # scalars
            ug.point_data.scalars.name = 'scalars'

            if not self.allwd_colours:
                print('No colours left - setting surf to white')
                surf_col = (1, 1, 1)
            else:
                col_idx = np.random.randint(0, len(self.allwd_colours) - 1)
                surf_col = self.allwd_colours[col_idx]
                self.allwd_colours = \
                    [el for el_idx, el
                     in enumerate(self.allwd_colours) if el_idx != col_idx]

            mlab.pipeline.surface(ug, opacity=surf_opacity, color=surf_col)
            mlab.pipeline.surface(
                ug, representation='wireframe', color=(0, 0, 0), line_width=0.5,
                opacity=surf_opacity)
            # mlab.show()

            pass

        x_diff = all_b_x_max - all_b_x_min
        y_diff = all_b_y_max - all_b_y_min
        z_diff = all_b_z_max - all_b_z_min

        d_dim = round(max([x_diff, y_diff, z_diff]) * dist_fact, 4)

        #  dim_diff, d_dim, min_dim, max_dim
        x_divs_coords = \
            self._get_singe_axis_divs(
                dim_diff=x_diff, d_dim=d_dim, min_dim=all_b_x_min,
                max_dim=all_b_x_max)

        y_divs_coords = \
            self._get_singe_axis_divs(
                dim_diff=y_diff, d_dim=d_dim, min_dim=all_b_y_min,
                max_dim=all_b_y_max)

        z_divs_coords = \
            self._get_singe_axis_divs(
                dim_diff=z_diff, d_dim=d_dim, min_dim=all_b_z_min,
                max_dim=all_b_z_max)

        x_grid_a, y_grid_a, z_grid_a = \
            self._get_xyz_grid_points(
                x_divs_coords=x_divs_coords, y_divs_coords=y_divs_coords,
                z_divs_coords=z_divs_coords)

        # print(all_b_y_min)
        # print(all_b_z_min)
        # print(z_grid_a)

        if plot_points:
            grid = \
                self.get_scatter_from_vects(
                    x_grid_a, y_grid_a, z_grid_a, opacity=0.2)

    @staticmethod
    def right_picker_callback(picker):
        remove_last_mayavi_point(
            point_glyphs=SU2MeshSurfPlotter.ffd_mayavi_points_plt)

    def print_ffd_box_info(self):
        ffd_box_coords = \
            SU2MeshSurfPlotter.ffd_mayavi_points_plt.mlab_source\
            .get('points')['points']

        print('Selected points are: [X1, Y1, Z1, X2, Y2, Z2, ...]')

        flat_ffd_box_coords = np.array(ffd_box_coords).flatten()
        print(','.join([str(el) for el in list(flat_ffd_box_coords)]))
        # print(np.array(ffd_box_coords).flatten())

    @staticmethod
    def left_picker_callback(picker):
        """ Picker callback: this get called when on pick events.
        """

        curr_glyph_points = \
            np.array(SU2MeshSurfPlotter.ffd_mayavi_points_plt.mlab_source
                     .get('points')['points'])
        # check for point picking
        if curr_glyph_points.shape[0] > 0:
            point_id = picker.point_id / curr_glyph_points.shape[0]
        else:
            point_id = -1
        print('point_id, picker.point_id')
        print(point_id, picker.point_id)
        print('glyph_points.shape')
        print(curr_glyph_points.shape)

        coords = picker.pick_position

        # if not keyboard.shift_pressed:
        #     print('adding new point')

        # with keyboard.pressed(Key.shift):
        #     print(keyboard.shift_pressed)

        # with keyboard.Listener(
        #         on_press=on_press,
        #         on_release=on_release) as listener:
        #     listener.join()

        # if keyboard.is_pressed('shift'):
        #     print('shift is pressed')

        add_mayavi_point(
            new_p_coords=coords,
            point_glyphs=SU2MeshSurfPlotter.ffd_mayavi_points_plt)

        # if keyboard.shift_pressed:
        #     print('shift press detected')

        # if picker.actor in red_glyphs.actor.actors:
        # Find which data point corresponds to the point picked:
        # we have to account for the fact that each data point is
        # represented by a glyph with several points

        # print('true point id')
        # print(picker.point_id)

        # point_id = picker.point_id / glyph_points.shape[0]
        # # print(point_id)
        # # If the no points have been selected, we have '-1'
        # if point_id != -1:
        #     int_point_id = int(round(point_id, 0))
        #
        #     # print('coords')
        #     # print(coords)
        #     # input('debug')
        #     add_red_point(new_p_coords=coords, red_glyphs=red_glyphs)
        #     # Retrieve the coordinnates coorresponding to that data
        #     # point
        #     # print('int_point_id')
        #     # print(int_point_id)
        #     x, y, z = x1[int_point_id], y1[int_point_id], z1[int_point_id]
        #     # Move the outline to the data point.
        #     outline.bounds = (x - 0.1, x + 0.1,
        #                       y - 0.1, y + 0.1,
        #                       z - 0.1, z + 0.1)


if __name__ == '__main__':

    # print(os.getcwd())
    pth_to_msh = 'su2_bench.su2'
    # pth_to_msh = 'project1.su2'
    # pth_to_msh = 'su2_bench_fxd_orient.su2'
    pth_to_msh = 'su2_bench_fxd_orient.su2'
    pth_to_msh = 'jet_cat_su2_test.su2'
    print(os.getcwd())
    pth_to_def_msh = '../../su2_tuts/adj_mesh_comp/ffd_su2_bench_deform.su2'
    # keyboard = Controller

    su2_mp = SU2MeshSurfPlotter(pth_to_msh=pth_to_msh,
                                ignored_surfs_rgx='^FF|^SYMM')
    su2_mp.read_su2_msh()
    su2_mp.set_all_points()
    su2_mp.set_all_boundaries()
    su2_mp.plot_all_boundaries(plot_points=False)
    # mlab.title('FFD box selection widget - please remember that points need to '
    #            'be picked in the same order as in hexa element', height=0.1)

    # su2_mp_def = SU2MeshSurfPlotter(
    #     pth_to_msh=pth_to_def_msh, ignored_surfs_rgx='^FF|^SYMM|^FUS')
    # su2_mp_def.read_su2_msh()
    # su2_mp_def.set_all_points()
    # su2_mp_def.set_all_boundaries()
    # su2_mp_def.plot_all_boundaries(
    #     plot_points=False, surf_opacity=0.3, reset_fig=False)

    mlab.show()
    su2_mp.print_ffd_box_info()
    pass

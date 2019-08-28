import numpy as np
import plotly as ply
import plotly.graph_objs as go
import re

from helpers.plotters import get_3d_scatter_trace


def read_all_lines(input_file, use_numpy: bool = True):
    if use_numpy:

        all_lines = []
        temp_lines_stash = []
        # print(temp_lines_stash)

        for line_idx, line in enumerate(input_file):

            temp_lines_stash.append(line)
            # print(line)

            if line_idx % 10000 == 0:

                if all_lines == []:
                    all_lines = np.array(temp_lines_stash)
                else:
                    all_lines = np.append(all_lines, temp_lines_stash)

                del temp_lines_stash
                temp_lines_stash = []

        all_lines = np.append(all_lines, temp_lines_stash)
        temp_lines_stash = []
        return all_lines
    else:
        print('Cant parse not using numpy! Returning None')
        return None


def find_entries_range_and_count(all_lines, entries_marker: str = '^NELEM='):
    info_line = ''
    info_line_idx = -1
    for line_idx, line in enumerate(all_lines):
        if re.search(entries_marker, line):
            info_line = line
            info_line_idx = line_idx
            break
    first_els_line_idx = info_line_idx + 1
    try:
        all_entries_count = int(info_line.split('=')[-1].strip())
    except Exception as exc:
        right_hand_side = info_line.split('=')[-1].strip()
        all_entries_count = int(right_hand_side.split('\t')[-1].strip())

    last_els_line_idx = first_els_line_idx + all_entries_count - 1
    return first_els_line_idx, last_els_line_idx, all_entries_count


def get_all_boundaries_info(all_lines, boundary_marker: str = '^MARKER_TAG='):
    all_bounds = {}
    for line_idx, line in enumerate(all_lines):
        if re.search(boundary_marker, line):
            bound_name = line.split('=')[-1].strip()
            bound_el_count_line = all_lines[line_idx + 1]
            bound_el_count = int(bound_el_count_line.split('=')[-1].strip())
            bound_start_line_idx = line_idx + 2
            bound_end_line_idx = bound_start_line_idx + bound_el_count - 1
            all_bounds[bound_name] = {
                'bound_start_line_idx': bound_start_line_idx,
                'bound_end_line_idx': bound_end_line_idx,
                'bound_el_count': bound_el_count}
    return all_bounds


def get_boundary_range_and_count():
    pass


if __name__ == '__main__':
    # pth_to_su2_msh = 'mesh_ONERAM6_inv_FFD.su2'

    # pth_to_su2_msh = \
    #     '/home/kebabongo/Projects/aero/su2_tuts/xjet_check/pir_sanity_check.su2'

    pth_to_su2_msh = \
        '/home/kebabongo/Projects/aero/su2_tuts/inv_onera/onera_ffd_msh.su2'

    all_lines = []

    with open(pth_to_su2_msh, 'r') as su2_msh_f:
        all_lines = read_all_lines(su2_msh_f)

    # print(all_lines)

    first_els_line_idx, last_els_line_idx, all_els_count = \
        find_entries_range_and_count(all_lines)
    print('### ELEMENTS ###')
    print(all_lines[first_els_line_idx])
    print(all_lines[last_els_line_idx])
    print(all_els_count)

    first_pts_line_idx, last_pts_line_idx, all_pts_count = \
        find_entries_range_and_count(all_lines, entries_marker='^NPOIN=')

    print('### POINTS ###')
    print(all_lines[first_pts_line_idx])
    print(all_lines[last_pts_line_idx])
    print(all_pts_count)

    first_l_bound_idx, _, all_bounds_count = \
        find_entries_range_and_count(all_lines, entries_marker='^NMARK=')

    print('### BOUNDS ###')
    print(all_lines[first_l_bound_idx])
    # print(all_lines[last_bound_l_idx])
    print(all_bounds_count)

    all_bounds = get_all_boundaries_info(all_lines)
    print(all_bounds)

    for key in all_bounds.keys():
        print(key)

    # print()
    # print(all_lines[all_bounds['LOWER_SIDE']['bound_start_line_idx']])
    # print(all_lines[all_bounds['LOWER_SIDE']['bound_end_line_idx']])

    print(all_lines[0])
    # input('debug')

    all_pts = all_lines[first_pts_line_idx: last_pts_line_idx + 1]

    for bound_name, bound_info in all_bounds.items():

        # continue

        # if bound_name != 'FUS':
        #     continue

        bound_walls = \
            all_lines[
                bound_info['bound_start_line_idx']:
                bound_info['bound_end_line_idx'] + 1]

        # print(bound_name)
        # print(bound_walls[0])
        # print(bound_walls[-1])

        # input('debug')

        traces = []

        all_xs = []
        all_ys = []
        all_zs = []
        all_labels = []

        all_nodes = []

        for bound_el_wall in bound_walls:
            curr_wall_nodes = \
                [int(el.replace('\n', '').strip())
                 for el in bound_el_wall[1:].split('\t') if el != '']

            x_l = []
            y_l = []
            z_l = []
            labels = []

            # print('curr_wall_nodes')
            # print(curr_wall_nodes)
            # print(all_pts[0])
            for node_idx, node in enumerate(curr_wall_nodes):
                # print('all_pts[node]')
                # print(node)
                # print(all_pts[node])
                all_nodes.append(node)
                node_point = [float(el.replace('\n', '').strip())
                              for el in all_pts[node].split('\t') if el != '']

                if node_idx == 0:
                    fn_x = node_point[0]
                    fn_y = node_point[1]
                    fn_z = node_point[2]
                    fn_lab = node

                # print('node_point')
                # print(node)
                # print(node_point)
                # print(node_point)
                # input('node point check')
                all_xs.append(node_point[0])
                all_ys.append(node_point[1])
                all_zs.append(node_point[2])

                x_l.append(node_point[0])
                y_l.append(node_point[1])
                z_l.append(node_point[2])
                labels.append(node)
                # input('node point debug')

            x_l.append(fn_x)
            y_l.append(fn_y)
            z_l.append(fn_z)
            labels.append(fn_z)

            # x: list, y: list, z: list, labels: list, plot_type: str = 'lines'
            # print('x_l')
            # print(x_l)
            # curr_wall_trace = \
            #     get_3d_scatter_trace(x=x_l, y=y_l, z=z_l, labels=labels)
            # traces.append(curr_wall_trace)
            # input('point_check')
        print('##############################')
        print(bound_name)
        print(len(np.unique(all_nodes)))
        print('##############################')

        # print(len(traces))

        # fig = \
        #     go.Figure(
        #         data=traces, layout=go.Layout(
        #             showlegend=False,
        #             xaxis=dict(
        #                 range=[-10, 10]
        #             ),
        #             yaxis=dict(
        #                 range=[-5, 5]
        #             )
        #         ))

        # ply.offline.plot(fig)

        # print(
        #     bound_info['bound_end_line_idx'] -
        #     bound_info['bound_start_line_idx'])

        # print('uniq xs')
        # print(np.unique(all_xs))
        # print('uniq ys')
        # print(np.unique([round(el, 4) for el in all_ys]))
        # print('uniq zs')
        # print(np.unique(all_zs))

        pass

    elemets_lines = []
    points_lines = []
    boundaries = {}
    volumes = {}

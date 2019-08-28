import numpy as np
import re


def find_entries_range_and_count(all_lines, entries_marker: str = '^NELEM='):
    info_line = ''
    info_line_idx = -1
    entries_marker_found = False
    for line_idx, line in enumerate(all_lines):
        # print(line)
        if re.search(entries_marker, line):
            info_line = line
            info_line_idx = line_idx
            entries_marker_found = True
            break
    print('entries_marker_found')
    print(entries_marker_found)
    first_els_line_idx = info_line_idx + 1
    try:
        all_entries_count = int(info_line.split('=')[-1].strip())
    except Exception as exc:
        right_hand_side = info_line.split('=')[-1].strip()
        print(right_hand_side)
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


def add_mayavi_point(new_p_coords: list, point_glyphs):
    curr_points = np.array(point_glyphs.mlab_source.get('points')['points'])
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

    point_glyphs.mlab_source.set(points=appnd_p_list)


def remove_last_mayavi_point(point_glyphs):
    curr_points = np.array(point_glyphs.mlab_source.get('points')['points'])

    if len(curr_points) <= 1:
        # new_points = np.array([[None, None, None], ])
        pass
    else:
        new_points = np.array([point for point in curr_points[:-1]])
        point_glyphs.mlab_source.set(points=new_points)

from collections.abc import Iterable
from copy import deepcopy
import numpy as np
import os
from pyforms.controls import ControlBase, ControlEmptyWidget
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout
from pyvalid import accepts, returns
import re
import tkinter
import traceback
import yaml
import warnings


def read_lines_file(su2_cfg_path):
    """
    Reads entire file into a list

    Parameters
    ----------
    su2_cfg_path: basestring
        path to file to line by line read

    Returns
    -------
    list
        Row by row list of parsed cfg file

    """
    row_by_row_f_list = []
    try:
        with open(su2_cfg_path, 'r') as in_cfg_f:
            print('reading lines')
            row_by_row_f_list = in_cfg_f.readlines()
    except Exception as exc:
        print(exc)

    return row_by_row_f_list


@accepts(object)
def safe_to_str(val_to_cast: object):
    """
    Tries to convert string to int safely
    If it fails returns None

    Parameters
    ----------
    val_to_cast: object
        val to be cast to str

    Returns
    -------
    str or None
        if conversion was a success returns string otherwise None

    """
    if not val_to_cast:
        return ''

    try:
        conv_val = str(val_to_cast)
    except ValueError:
        # print('{} conversion to int failed'.format(val_to_cast))
        return None

    return conv_val


def safe_to_int(val_to_cast: str) -> int or None:
    """
    Tries to convert string to int safely
    If it fails returns None

    Parameters
    ----------
    val_to_cast: str
        str to be converted to int

    Returns
    -------
    int or None
        str converted to int or None

    """

    try:
        conv_val = int(val_to_cast)
    except ValueError:
        print('{} conversion to int failed'.format(val_to_cast))
        return None

    return conv_val


def safe_to_float(val_to_cast: str) -> float or None:
    """
    Tries to convert string to float safely
    If it fails returns None

    Parameters
    ----------
    val_to_cast: str
        str to be converted to int

    Returns
    -------
    float or None
        str converted to float or None

    """
    try:
        conv_val = float(val_to_cast)
    except ValueError:
        # print('{} conversion to int failed'.format(val_to_cast))
        return None

    return conv_val


def _is_rgx_in_str(target_str: str, rgx: str) -> bool:
    """
    Searches for target rgx in the provided str and returns True if found and
    False if not

    Parameters
    ----------
    target_str: str
        string checked ofr regex occurance
    rgx: str
        rgx to be found in string

    Returns
    -------
    bool
        Flag - was the regex found

    """
    prcsd_str = target_str
    if not isinstance(target_str, str):
        prcsd_str = safe_to_str(prcsd_str)

    rgx_found = False
    if not prcsd_str:
        return rgx_found

    if re.search(rgx, prcsd_str):
        rgx_found = True
    print('rgx_found')
    print(rgx)
    print(prcsd_str)
    print(re.search(rgx, prcsd_str))
    print(rgx_found)
    return rgx_found


def get_from_yaml(
        path_to_opts_yaml: str,
        desired_key: str,
        return_plain_val: bool = False) -> tuple or str:
    """
    Gets desired allowed values/options from yaml file

    Parameters
    ----------
    path_to_opts_yaml: str
        yaml file locations
    desired_key: str
        key of desired options in provided yam file

    Returns
    -------
    tuple
        tuple with extracted options

    """

    with open(path_to_opts_yaml, 'r') as opts_f:
        read_dict = yaml.load(opts_f)
    desired_yaml_obj = read_dict.get(desired_key, None)

    if not desired_yaml_obj:
        raise RuntimeError(
            'Please check the opts yaml - key {} was not found'
            .format(desired_key))
    # for opt_key, opt in desired_yaml_obj.items():
    if not return_plain_val:
        return tuple((opt_key, opt) for opt_key, opt
                     in desired_yaml_obj.items())
    return desired_yaml_obj


@accepts(object, str, str, str)
def get_from_yaml_and_set(
        target_obj: object, target_field_name: str,
        value_key: str, yaml_pth: str):

    if not yaml_pth:
        warnings.warn('No path to target yaml specified - no value was set')
        return None

    value = \
        get_from_yaml(
            path_to_opts_yaml=yaml_pth,
            desired_key=value_key,
            return_plain_val=True)
    setattr(target_obj, target_field_name, value)


def unpack_tuple_of_tuples(tuple_of_tuples: tuple) -> tuple:
    """
    Unpacks the tuple containing key-value tuples

    Parameters
    ----------
    tuple_of_tuples: tuple
        tuple containing key-value pair like tuples

    Yields
    -------
    tuple
        unpacked tuple
    """
    for tup_key, tup_val in tuple_of_tuples:
        yield tup_key, tup_val


def get_found_str(subset_str: str, rgx_search_result) -> str:
    """
    EXtracts found string by rgx from provide string

    Parameters
    ----------
    subset_str: str
        the string from which the regex mtch will be extracted
    rgx_search_result: SRE_Match
        the re.search() result

    Returns
    -------
    str
        string containing the subset fonud by rgx

    """

    subset_start_idx: int = rgx_search_result.start() + 1
    subset_end_idx: int = rgx_search_result.end() - 1
    return subset_str[subset_start_idx:subset_end_idx]


def save_to_yaml(
        saved_dict: dict,
        saved_fname: str = 'su2_cfg_template.yaml') -> None:
    """
    Saves field (given by name) of a given object in a yaml format

    Parameters
    ----------
    saved_dict: dict
        dict to be saved as yaml
    saved_fname: str
        string with save path/file name

    Returns
    -------
    None
        None

    """

    with open(saved_fname, 'w') as yaml_f:
        # yaml.dump(data, outfile, default_flow_style=False)
        yaml.dump(saved_dict, yaml_f, default_flow_style=False)


def check_and_make(dir_name: str) -> None:
    """
    Checks if dir is present in folder - if not creates it

    Parameters
    ----------
    dir_name: str
        dir to be checked (and created if not present)

    Returns
    -------
    None
        None

    """
    all_objs_in_curr_dir = os.listdir('./')
    if dir_name not in all_objs_in_curr_dir:
        # create dir
        os.mkdir(dir_name)
    return


@returns(tuple)
def get_screen_res():
    """
    Getter for curr screen size in pxls

    Parameters
    ----------
    self

    Returns
    -------

    """
    root = tkinter.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    return width, height


@accepts(dict)
@returns(dict)
def all_keys_to_upper(input_dict: dict) -> dict:
    """
    Converts all keys from input dict to upper case
    Parameters
    ----------
    input_dict: dict
        dict which keys will be converted to upper

    Returns
    -------

    """
    upper_keys_dict = {}
    for input_d_key, input_d_val in input_dict.items():
        upper_keys_dict[input_d_key.upper()] = deepcopy(input_d_val)
    return deepcopy(upper_keys_dict)


@accepts(str)
@returns(dict)
def get_dict_from_yaml(path_to_yaml: str):
    try:
        with open(path_to_yaml, 'r') as in_y:
            loaded_yaml = yaml.load(in_y)
    except Exception as exc:
        print('Encountered following error while openning yaml under this path:'
              ' {}'.format(path_to_yaml))
        print(exc)
        print('\n\n Full TRACEBACK \n')
        traceback.print_exc()
        print('\n\n TRACEBACK ENDS HERE\n')

    return loaded_yaml


@accepts(dict, str, bool)
@returns(object)
def get_safely_from_dict(
        input_dict: dict, key_to_get: str, warn_instead_of_fail: bool = True):
    """
    Safely gets desired element from provided dict - if the element is not found
    it raises error or warns (preferred)
    Parameters
    ----------
    input_dict: dict
        dict to be chckd for key
    key_to_get: str
        key to look for in input_dict
    warn_instead_of_fail: bool
        should fail or warn

    Returns
    -------
    object
        object found under provided key on None

    """
    des_element = input_dict.get(key_to_get, None)
    error_msg = \
        'The desired key `{}` had no value in provided dict'.format(key_to_get)

    if not des_element:
        if warn_instead_of_fail:
            warnings.warn(error_msg)
        else:
            raise ValueError(error_msg)

    if isinstance(des_element, dict):
        return deepcopy(des_element)
    return des_element


@accepts(str, bool)
@returns(str)
def get_no_ws_and_nl_str(input_str: str, rep_nl_first: bool = True):
    """
    Strips WS from string
    Parameters
    ----------
    input_str

    Returns
    -------

    """
    prcsd_str = input_str
    if rep_nl_first:
        prcsd_1_str = prcsd_str.replace('\n', '')
    else:
        prcsd_1_str = prcsd_str.strip()

    if rep_nl_first:
        prcsd_2_str = prcsd_1_str.strip()
    else:
        prcsd_2_str = prcsd_1_str.replace('\n', '')
    return prcsd_2_str


@accepts(object, str, Iterable)
def init_des_class_fields_frm_yaml(
        trgt_obj: object, yaml_pth: str, class_fields_names: Iterable):
    """
    Initialized desired fields using input iterable

    Parameters
    ----------
    class_fields_names: Iterable
        string or array of class field names to be read from yaml
        Fields in yaml must have same names as fields of object

    Returns
    -------

    """

    if not class_fields_names:
        warnings.warn(
            'No class fields to instantiate specified - '
            'passed list was empty')
        return None

    # target_obj: object, target_field_name: str,
    # value_key: str, yaml_pth: str)

    if isinstance(class_fields_names, str):
        get_from_yaml_and_set(
            target_obj=trgt_obj,
            target_field_name=class_fields_names,
            value_key=class_fields_names,
            yaml_pth=yaml_pth)

    elif isinstance(class_fields_names, Iterable):
        for class_field_name in class_fields_names:
            get_from_yaml_and_set(
                target_obj=trgt_obj,
                target_field_name=class_field_name,
                value_key=class_field_name,
                yaml_pth=yaml_pth)


@accepts(dict, str)
@returns(object)
def get_from_dict_or_warn(input_dict: dict, des_key: str) -> object:
    """
    Gets value from desired key (if present). If no value was found returns None
    Parameters
    ----------
    input_dict: dict
        didt from which value wll be extracted
    des_key: str
        desired key

    Returns
    -------
    object
        desired object from input_dict
    """
    ftchd_obj = input_dict.get(des_key, {})

    if not ftchd_obj:
        warnings.warn(
            'The key: {} in which desired value should be stored does not hold '
            'any values - returning None'.format(des_key))
    return ftchd_obj


@accepts(str, str, str, bool)
@returns(list)
def _get_numbers_from_splt_str(
        input_str: str,
        separator: str = ',',
        number_rgx: str = '[0-9]{1,}',
        rm_par: bool = True) -> list:
    """
    Gets numbers from string split by splitter
    Parameters
    ----------
    input_str: str
        str to spliti and extract numbers from
    separator: str
        separator splitting the string
    number_rgx: str
        number search rgx

    Returns
    -------
    list
        list of numbers found
    """
    if rm_par:
        no_open_par_str = input_str.replace('(', '')
        str_to_splt = no_open_par_str.replace(')', '')
    else:
        str_to_splt = input_str

    splt_str = str_to_splt.split(separator)
    numbers = [el.strip() for el in splt_str if re.search(number_rgx, el)]
    return numbers


# @accepts(str)
# @returns(str)
# def get_relative_pth(trimmed_pth: str):
#     """
#     Replaces curr working dir substring in provided path
#     Parameters
#     ----------
#     trimmed_pth: str
#         path to have absolute piece replaced
#
#     Returns
#     -------
#
#     """
#
#     curr_dir = os.getcwd()
#
#     curr_full_pth = os.getcwd()
#     rel_pth = trimmed_pth.replace(curr_full_pth)
#     return rel_pth


def get_vector_from_points(input_point_list: list, desired_class: callable):
    """
    Getter for vector form list od Points
    Parameters
    ----------
    input_point_list

    Returns
    -------

    """

    # check for points
    for el in input_point_list:
        if not isinstance(el, desired_class):
            raise TypeError(
                'Each element of `input_point_list` must of a Point type')
        
    vect_start_point: desired_class = input_point_list[0]
    vect_end_point: desired_class = input_point_list[1]
    
    x_v_coord = vect_end_point.x_coord - vect_start_point.x_coord
    y_v_coord = vect_end_point.y_coord - vect_start_point.y_coord
    z_v_coord = vect_end_point.z_coord - vect_start_point.z_coord

    return [x_v_coord, y_v_coord, z_v_coord]


def get_face_normal_vect(face_points_list: list):

    first_edge_start = face_points_list[0]
    first_edge_end = face_points_list[1]

    first_edge_vect = get_vect_from_points(
        v_start_point_list=first_edge_start[1:],
        v_end_point_list=first_edge_end[1:]
    )

    sec_edge_start = face_points_list[1]
    sec_edge_end = face_points_list[2]

    sec_edge_vect = get_vect_from_points(
        v_start_point_list=sec_edge_start[1:],
        v_end_point_list=sec_edge_end[1:]
    )

    face_normal_v = np.cross(first_edge_vect, sec_edge_vect)
    normed_face_normal_v = face_normal_v / np.linalg.norm(face_normal_v)

    return normed_face_normal_v


def get_vect_from_points(v_start_point_list: list, v_end_point_list: list):

    start_coords_np = np.array(v_start_point_list)
    end_coords_np = np.array(v_end_point_list)

    vect = end_coords_np - start_coords_np

    return vect


def get_xyz_coords_frm_sets(
        list_of_xyz_per_entry: list, skip_first: bool = True):
    x_coords = []
    y_coords = []
    z_coords = []

    # print('list_of_xyz_per_entry')
    # print(list_of_xyz_per_entry)
    # print('')

    for el in list_of_xyz_per_entry:
        x_coords.append(el[1] if skip_first else el[0])
        y_coords.append(el[2] if skip_first else el[1])
        z_coords.append(el[3] if skip_first else el[2])

    return x_coords, y_coords, z_coords


def subset_points_using_surf(all_pts: list, nodes_per_walls: list):

    new_points = []
    new_to_old_points_map = []
    new_nodes_per_walls = []

    for nodes_per_wall in nodes_per_walls:
        # print('nodes_per_wall')
        # print(nodes_per_wall)

        new_nodes_per_wall = []

        for node in nodes_per_wall:
            if node not in new_to_old_points_map:
                new_to_old_points_map.append(node)
                new_points.append(all_pts[node])
            # else:
            #     continue
            for new_node_id, old_node_id in enumerate(new_to_old_points_map):
                if old_node_id == node:
                    new_nodes_per_wall.append(new_node_id)
                    break

        new_nodes_per_walls.append(np.array(new_nodes_per_wall))

    return np.array(new_points), np.array(new_nodes_per_walls)


def get_pts_cg(nodes_per_els: list, pts_list: list, skip_first: bool = False):
    """
    Gets cg of provided points from list of pts
    each poit is provided in a given format [id, x, y, z]
    Parameters
    ----------
    pts_list

    Returns
    -------

    """

    x_cg_coords = []
    y_cg_coords = []
    z_cg_coords = []

    print(nodes_per_els[:5])

    for nodes_per_el in nodes_per_els:
        wall_pts_list = []
        for node in nodes_per_el:
            wall_pts_list.append(pts_list[node])

        x_coords, y_coords, z_coords = \
            get_xyz_coords_frm_sets(wall_pts_list, skip_first=skip_first)

        # yield el[1], el[2], el[3]
    # return x_coords, y_coords, z_coords

        cg_coords = []

        for coords_fam in [x_coords, y_coords, z_coords]:
            cg_coords.append(np.mean(coords_fam))

        # print(cg_coords)
        # input('test')

        # for cg_coord in cg_coords:
        x_cg_coords.append(cg_coords[0])
        y_cg_coords.append(cg_coords[1])
        z_cg_coords.append(cg_coords[2])

    return x_cg_coords, y_cg_coords, z_cg_coords

    # return cg_coords


def read_all_lines(input_data, use_numpy: bool = True):
    if use_numpy:

        all_lines = []
        temp_lines_stash = []
        # print(temp_lines_stash)

        for el_idx, el in enumerate(input_data):

            temp_lines_stash.append(el)
            # print(line)

            if el_idx % 10000 == 0:

                if all_lines == []:
                    all_lines = np.array(temp_lines_stash)
                else:
                    all_lines = np.append(all_lines, temp_lines_stash)

                del temp_lines_stash
                temp_lines_stash = []
                print(len(all_lines))

        all_lines = np.append(all_lines, temp_lines_stash)
        temp_lines_stash = []
        return all_lines
    else:
        print('Cant parse not using numpy! Returning None')
        return None


def prcs_collection_w_np(
        input_collection, col_el_transformer: callable = None,
        trans_kwargs: dict = {}):

    temp_els_stash = []
    all_transf_els = []

    for el_idx, el in enumerate(input_collection):

        if not col_el_transformer:
            trans_el = el
        else:
            trans_el = col_el_transformer(el, **trans_kwargs)

        temp_els_stash.append(trans_el)

        if el_idx % 10000 == 0:

            if all_transf_els == []:
                all_transf_els = np.array(temp_els_stash)
            else:

                np_temp_els_stash = np.array(temp_els_stash)

                all_transf_els = \
                    np.vstack([all_transf_els, np_temp_els_stash])

            del temp_els_stash
            temp_els_stash = []

    np_temp_els_stash = np.array(temp_els_stash)
    all_transf_els = np.vstack([all_transf_els, np_temp_els_stash])
    temp_lines_stash = []
    return all_transf_els


def replace_all_ws(
        input_str_like: str or Iterable, ws_rplcmnt: str,
        ws_search_str: str = '\\s{1,}|\\t{1,}'):
    """
    Replaces whitespaces insisde string or collection
    Parameters
    ----------
    input_str_like: str or Iterable
        re.sub target
    ws_rplcmnt: str
        replace ws with what?
    ws_search_str: str
        how to find whitespaces

    Returns
    -------
    str or Iterable
        string or collection of strings with no ws

    """

    if isinstance(input_str_like, str):
        return re.sub(ws_search_str, ws_rplcmnt, input_str_like)

    if isinstance(input_str_like, Iterable):
        rtrnd_collection = []
        for el in input_str_like:
            if not isinstance(el, str):
                return None
            rtrnd_collection.append(re.sub(ws_search_str, ws_rplcmnt, el))
        return rtrnd_collection

    return None


def get_pyqt_grpbox(
        grpbox_desc: str, grpbox_stylesheet: str,
        main_grpbox_ctrl: ControlBase, return_container: bool = True):
    """
    Getter for pyqt groupbox for any pyforms control

    Parameters
    ----------
    grpbox_desc: str
        the description of the group
    grpbox_stylesheet: dict
        stylesheet used inside groupbox
    main_grpbox_ctrl: ControlBase
        the pyforms base control to be used inside goupbox
    return_container: bool
        should raw groupbox be returned or the EmptyControlWidget with
        groupbox instead

    Returns
    -------
    QGroupBox or ControlEmptyWidget
        either QGroupBox or ControlEmptyWidget with embedded QGroupBox

    """
    curr_ctrl_groupbox = QGroupBox(grpbox_desc)
    curr_ctrl_groupbox.setStyleSheet(grpbox_stylesheet)

    vert_layout = QVBoxLayout(curr_ctrl_groupbox)
    first_grpbx_row = QHBoxLayout()
    first_grpbx_row.addWidget(main_grpbox_ctrl.form)

    vert_layout.addLayout(first_grpbx_row)

    if not return_container:
        return curr_ctrl_groupbox

    curr_ctrl_cont = ControlEmptyWidget()

    curr_ctrl_cont.form.layout().addWidget(curr_ctrl_groupbox)

    return curr_ctrl_cont


def break_input_str_on_len(
        input_str: str, break_on_len: int = 20, str_spltr: str = ' '):
    """
    Returns the string broken on provided length

    Parameters
    ----------
    input_str: str
        str to break on
    break_on_len: int
        how many chars per line
    str_spltr: str
        by which char line should be split

    Returns
    -------
    str
        the string with newlines

    """

    input_splt = input_str.split(str_spltr)

    curr_line_len = 0
    line_w_nls = ''

    for word in input_splt:
        line_w_nls += word
        curr_line_len += len(word)
        if curr_line_len > break_on_len:
            line_w_nls += '\n'
            curr_line_len = 0

    return line_w_nls

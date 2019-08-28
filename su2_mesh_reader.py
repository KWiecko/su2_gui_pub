from collections.abc import Iterable
from copy import deepcopy
from pyforms.controls import ControlBase
from pyvalid import accepts, returns
import re
import warnings

from helpers.helpers import get_from_yaml_and_set, get_no_ws_and_nl_str, \
    init_des_class_fields_frm_yaml


class SU2MshReader:

    @property
    @returns(str)
    def msh_pth(self) -> str:
        return self._msh_pth

    @msh_pth.setter
    @accepts(object, str)
    def msh_pth(self, new_val: str):
        self._msh_pth = new_val

    @property
    @returns(str)
    def msh_fname_tab_key(self) -> str:
        return self._msh_fname_tab_key

    @msh_fname_tab_key.setter
    @accepts(object, str)
    def msh_fname_tab_key(self, new_val: str):
        self._msh_fname_tab_key = new_val

    @property
    @returns(str)
    def msh_fname_param_key(self) -> str:
        return self._msh_fname_param_key

    @msh_fname_param_key.setter
    @accepts(object, str)
    def msh_fname_param_key(self, new_val: str):
        self._msh_fname_param_key = new_val

    @property
    @returns(ControlBase)
    def msh_fname_ctrl(self) -> ControlBase:
        return self._msh_fname_ctrl

    @msh_fname_ctrl.setter
    @accepts(object, ControlBase)
    def msh_fname_ctrl(self, new_val: ControlBase):
        self._msh_fname_ctrl = new_val

    @property
    @returns(str)
    def msh_rgxs_yaml_pth(self) -> str:
        return self._msh_rgxs_yaml_pth

    @msh_rgxs_yaml_pth.setter
    @accepts(object, str)
    def msh_rgxs_yaml_pth(self, new_val: str):

        if not new_val:
            warnings.warn(
                'No class fields to instantiate specified - '
                'passed list was empty')

        self._msh_rgxs_yaml_pth = new_val

    @property
    @returns(dict)
    def msh_srfs_map(self) -> dict:
        return self._msh_srfs_map

    @msh_srfs_map.setter
    @accepts(object, dict)
    def msh_srfs_map(self, new_val: dict):
        self._msh_srfs_map = deepcopy(new_val)

    @property
    @returns(str)
    def srf_name_rgx(self) -> str:
        return self._srf_name_rgx

    @srf_name_rgx.setter
    @accepts(object, str)
    def srf_name_rgx(self, new_val: str):
        self._srf_name_rgx = new_val

    @property
    @returns(str)
    def srf_el_count_rgx(self) -> str:
        return self._srf_el_count_rgx

    @srf_el_count_rgx.setter
    @accepts(object, str)
    def srf_el_count_rgx(self, new_val: str):
        self._srf_el_count_rgx = new_val

    @property
    @returns(str)
    def srf_name_asgn_spltr(self) -> str:
        return self._srf_name_asgn_spltr

    @srf_name_asgn_spltr.setter
    @accepts(object, str)
    def srf_name_asgn_spltr(self, new_val: str):
        self._srf_name_asgn_spltr = new_val

    def __init__(self, msh_rgxs_yaml_pth: str = 'su2_msh_parsing_params.yaml'):
        """
        Init w params

        Parameters
        ----------
        msh_rgxs_yaml_pth : str
            pth to yaml containing rgxs for su2 msh file parsing
        """

        self.msh_rgxs_yaml_pth = msh_rgxs_yaml_pth
        self.msh_srfs_map = {}
        # trgt_obj: object, msh_rgxs_yaml_pth: str, class_fields_names: Iterable
        init_des_class_fields_frm_yaml(
            trgt_obj=self,
            yaml_pth=self.msh_rgxs_yaml_pth,
            class_fields_names=
            ['msh_fname_tab_key', 'msh_fname_param_key', 'srf_name_rgx',
             'srf_el_count_rgx', 'srf_name_asgn_spltr'])

    # @accepts(object, Iterable)
    # def _init_des_class_fields_frm_yaml(
    #         self, class_fields_names: Iterable):
    #     """
    #     Initialized desired fields using input iterable
    #
    #     Parameters
    #     ----------
    #     class_fields_names: Iterable
    #         string or array of class field names to be read from yaml
    #         Fields in yaml must have same names as fields of object
    #
    #     Returns
    #     -------
    #
    #     """
    #
    #     if not class_fields_names:
    #         warnings.warn(
    #             'No class fields to instantiate specified - '
    #             'passed list was empty')
    #         return None
    #
    #     # target_obj: object, target_field_name: str,
    #     # value_key: str, yaml_pth: str)
    #
    #     if isinstance(class_fields_names, str):
    #         get_from_yaml_and_set(
    #             target_obj=self,
    #             target_field_name=class_fields_names,
    #             value_key=class_fields_names,
    #             yaml_pth=self.msh_rgxs_yaml_pth)
    #
    #     elif isinstance(class_fields_names, Iterable):
    #         for class_field_name in class_fields_names:
    #             get_from_yaml_and_set(
    #                 target_obj=self,
    #                 target_field_name=class_field_name,
    #                 value_key=class_field_name,
    #                 yaml_pth=self.msh_rgxs_yaml_pth)

    def _set_srfs_frm_msh(self, su2_msh_pth: str):
        """
        Setter for all named surfaces found in msh file

        Parameters
        ----------
        su2_msh_pth: str
            pth to su2 msh file

        Returns
        -------

        """
        with open(su2_msh_pth, 'r') as r_msh:
            for line in r_msh:
                has_surf_name = re.search(self.srf_name_rgx, line)
                if has_surf_name:
                    srf_name = self._get_srf_name_w_spltr(msh_line=line)
                    self.msh_srfs_map[srf_name] = True
                    # sef_el_count = None

    @accepts(object, str)
    def _get_srf_name_w_spltr(self, msh_line: str) -> str:
        """
        Splits mesh line which contains the surface name using provided
        spliter and returns the right side of the marker

        Parameters
        ----------
        msh_line: str
            line from which surface name will be extraceted

        Returns
        -------
        str
            str with surface name or empty string

        """

        has_spltr = re.search(self.srf_name_asgn_spltr, msh_line)

        if not has_spltr:
            return ''

        splt_line = msh_line.split(self.srf_name_asgn_spltr)
        des_srf_name = splt_line[-1]
        ws_nl_fxd_srf_name = get_no_ws_and_nl_str(des_srf_name)
        return ws_nl_fxd_srf_name


if __name__ == '__main__':
    test_obj = SU2MshReader()
    test_obj._set_srfs_frm_msh(
        '/home/kebabongo/Projects/aero/su2_tuts/onera_inv/mesh_ONERAM6_inv_FFD.su2')
    print(test_obj.msh_srfs_map)

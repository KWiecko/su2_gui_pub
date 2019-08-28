from copy import deepcopy
from pyvalid import accepts, returns
import re
import warnings

from helpers.helpers import get_from_yaml, safe_to_int, safe_to_float
from su2_config_creator import SU2Config
from su2_config_reader import SU2CfgParser
from vert_tabs_cfg_edit import VerticalTabsWidget


# class SU2ConfigSaver(SU2CfgParser):
class SU2ConfigSaver:

    @property
    @returns(SU2Config)
    def su2_cfg_obj(self):
        return self._su2_cfg_obj

    @su2_cfg_obj.setter
    @accepts(object, SU2Config)
    def su2_cfg_obj(self, new_val: SU2Config):
        self._su2_cfg_obj = new_val

    @property
    @returns(dict)
    def all_params_vals(self) -> dict:
        return self._all_params_vals

    @all_params_vals.setter
    @accepts(object, dict)
    def all_params_vals(self, new_val: dict):
        self._all_params_vals = deepcopy(new_val)

    @property
    @returns(str)
    def param_setting_ptrn(self):
        return self._param_setting_ptrn

    @param_setting_ptrn.setter
    @accepts(object, str)
    def param_setting_ptrn(self, new_val: str):
        self._param_setting_ptrn = new_val

    @property
    @returns(list)
    def lines_to_save(self):
        return self._lines_to_save

    @lines_to_save.setter
    @accepts(object, list)
    def lines_to_save(self, new_val: list):
        self._lines_to_save = new_val.copy()

    @property
    @returns(str)
    def cfg_saver_ptrns_path(self) -> str:
        return self._cfg_saver_ptrns_path

    @cfg_saver_ptrns_path.setter
    @accepts(object, str)
    def cfg_saver_ptrns_path(self, new_val: str):
        self._cfg_saver_ptrns_path = new_val

    @property
    @returns(VerticalTabsWidget)
    def vert_tabs_w(self) -> VerticalTabsWidget:
        return self._vert_tabs_w

    @vert_tabs_w.setter
    @accepts(object, VerticalTabsWidget)
    def vert_tabs_w(self, new_val: VerticalTabsWidget):
        self._vert_tabs_w = new_val

    @property
    @returns(list)
    def dsbld_sctns(self) -> list:
        return self._dsbld_sctns

    @dsbld_sctns.setter
    @accepts(object, list)
    def dsbld_sctns(self, new_val: list):
        self._dsbld_sctns = new_val.copy()

    @property
    @returns(dict)
    def tb_saved_cfg_dict(self) -> dict:
        return self._tb_saved_cfg_dict

    @tb_saved_cfg_dict.setter
    @accepts(object, dict)
    def tb_saved_cfg_dict(self, new_val: dict):
        self._tb_saved_cfg_dict = deepcopy(new_val)

    @property
    @returns(str)
    def chunk_sep_rgx(self) -> str:
        return self._chunk_sep_rgx

    @chunk_sep_rgx.setter
    @accepts(object, str)
    def chunk_sep_rgx(self, new_val: str):
        self._chunk_sep_rgx = new_val

    @property
    @returns(str)
    def chunk_sep_spacer(self) -> str:
        return self._chunk_sep_spacer

    @chunk_sep_spacer.setter
    @accepts(object, str)
    def chunk_sep_spacer(self, new_val: str):
        self._chunk_sep_spacer = new_val

    @property
    @returns(str)
    def cmnt_sign(self) -> str:
        return self._cmnt_sign

    @cmnt_sign.setter
    @accepts(object, str)
    def cmnt_sign(self, new_val: str):
        self._cmnt_sign = new_val

    @property
    def chunk_name_ptrn(self) -> str:
        return self._chunk_name_ptrn

    @chunk_name_ptrn.setter
    def chunk_name_ptrn(self, new_val: str):
        self._chunk_name_ptrn = new_val

    @property
    @returns(str)
    def param_setting_ptrn(self) -> str:
        return self._param_setting_ptrn

    @param_setting_ptrn.setter
    @accepts(object, str)
    def param_setting_ptrn(self, new_val: str):
        self._param_setting_ptrn = new_val

    @property
    @returns(str)
    def pre_param_cmt_ptrn(self) -> str:
        return self._pre_param_cmt_ptrn

    @pre_param_cmt_ptrn.setter
    @accepts(object, str)
    def pre_param_cmt_ptrn(self, new_val: str):
        self._pre_param_cmt_ptrn = new_val
    # @property
    # @returns(list)
    # def saved_lines(self):
    #     return self._saved_lines
    #
    # @saved_lines.setter
    # @accepts(object, list)
    # def saved_lines(self, new_val: list):
    #     self._saved_lines = new_val

    @accepts(object, SU2Config, VerticalTabsWidget, str)
    def __init__(
            self, su2_cfg_obj: SU2Config, vert_tabs_w: VerticalTabsWidget,
            cfg_saver_ptrns_path: str = 'config_saver_patterns.yaml'):
        """
        Init w params
        Parameters
        ----------
        su2_cfg_obj: SU2Config
            ref. to cfg object for su2
        """
        self.su2_cfg_obj = su2_cfg_obj
        self.all_params_vals = {}
        self.param_setting_ptrn = '{}= {}\n'
        self.lines_to_save = []
        self.cfg_saver_ptrns_path = cfg_saver_ptrns_path
        self._set_all_saver_ptrns()
        self.vert_tabs_w = vert_tabs_w

        # super(SU2ConfigSaver, self).__init__(
        #     su2_cfg_path=self.su2_cfg_obj.load_path)

        # self.read_cfg_lines()

        # self._set_all_params_vals()
        # print(self.all_params_vals)
        # self._append_params_to_lines()
        self._set_tb_saved_cfg_dict()
        self._set_lines_to_save()

    def _set_all_saver_ptrns(self):
        self.chunk_sep_rgx = \
            get_from_yaml(
                path_to_opts_yaml=self.cfg_saver_ptrns_path,
                desired_key='chunk_sep_rgx',
                return_plain_val=True)

        self.chunk_sep_spacer = \
            get_from_yaml(
                path_to_opts_yaml=self.cfg_saver_ptrns_path,
                desired_key='chunk_sep_spacer',
                return_plain_val=True)

        self.cmnt_sign = \
            get_from_yaml(
                path_to_opts_yaml=self.cfg_saver_ptrns_path,
                desired_key='cmnt_sign',
                return_plain_val=True)

        self.chunk_name_ptrn = \
            get_from_yaml(
                path_to_opts_yaml=self.cfg_saver_ptrns_path,
                desired_key='chunk_name_ptrn',
                return_plain_val=True)

        self.param_setting_ptrn = \
            get_from_yaml(
                path_to_opts_yaml=self.cfg_saver_ptrns_path,
                desired_key='param_setting_ptrn',
                return_plain_val=True)

        self.pre_param_cmt_ptrn = \
            get_from_yaml(
                path_to_opts_yaml=self.cfg_saver_ptrns_path,
                desired_key='pre_param_cmt_ptrn',
                return_plain_val=True)

    @accepts(object, str)
    @returns(str)
    def _get_fxd_section_name(self, sctn_name: str) -> str:
        """
        Removes \n and whitespaces from provided str

        Parameters
        ----------
        sctn_name: str
            the section name to be processed for nl and ws markers

        Returns
        -------
        str
            string with no undesired chars

        """
        no_nl_sctn_name = sctn_name.replace('\n', '_')
        no_ws_sctn_name = no_nl_sctn_name.replace(' ', '_')
        upp_sctn_name = no_ws_sctn_name.upper()
        return upp_sctn_name

    def _set_dsbld_sctns(self):
        """
        Setter for disabled config sections (dsbld_sctns)

        Returns
        -------

        """
        dsbld_sctns = []
        tab_w = self.vert_tabs_w.vert_tab_w_ctrl.tabs_w
        for tab_idx in range(tab_w.count()):
            tab_status = tab_w.isTabEnabled(tab_idx)
            print(tab_w.tabText(tab_idx), tab_status)
            if not tab_status:
                dsbld_tab_name = tab_w.tabText(tab_idx)
                upp_dsbld_tab_name = self._get_fxd_section_name(dsbld_tab_name)
                dsbld_sctns.append(upp_dsbld_tab_name)
        print(dsbld_sctns)
        self.dsbld_sctns = dsbld_sctns

    def _set_tb_saved_cfg_dict(self):
        """
        Sets dict to be saved based on disabled controls and tabs
        Returns
        -------

        """
        tb_saved_dict = {}
        # self.dsbld_sctns
        self._set_dsbld_sctns()
        for section_key, section in self.su2_cfg_obj.parsed_su2_cfg.items():
            if section_key not in self.dsbld_sctns:
                sctn_params_dict = {}
                for param_name, param_dict in section.items():
                    print(param_name)
                    print(param_dict)
                    if param_dict['control_toogle'].value:
                        sctn_params_dict[param_name] = {}
                        sctn_params_dict[param_name]['tooltip'] = \
                            param_dict['tooltip']

                        saved_param_val = None
                        if 'iter' in param_name or 'ITER' in param_name:
                            print('converting to float')
                            float_frm_str = \
                                safe_to_float(param_dict['control'].value)
                            if not float_frm_str:
                                saved_param_val = None
                            else:
                                saved_param_val = \
                                    safe_to_int(float_frm_str)
                        if not saved_param_val:
                            print('conv to int failed')
                            saved_param_val = param_dict['control'].value

                        sctn_params_dict[param_name]['value'] = saved_param_val
                        # param_dict['control'].value

                if sctn_params_dict:
                    tb_saved_dict[section_key] = sctn_params_dict
        self.tb_saved_dict = tb_saved_dict

    def _set_lines_to_save(self):
        """
        Sets lines to be saved using provided saver patterns
        Uses enabled/disabled flags for sections/controls
        Returns
        -------

        """
        if not self.tb_saved_dict:
            warnings.warn('`tb_saved_dict` is empty')

        lines_to_save = []
        for section_key, section in self.tb_saved_dict.items():
            lines_to_save.append(self._get_secion_name_line(section_key))
            for param_name, param_dict in section.items():
                cmmnt_line = \
                    self.pre_param_cmt_ptrn.format(param_dict['tooltip'])
                if not cmmnt_line:
                    cmmnt_line = '{}\n'.format(self.cmnt_sign)
                lines_to_save.append(cmmnt_line)
                param_line = \
                    self.param_setting_ptrn\
                        .format(param_name, param_dict['value'])
                        # .format(param_name, param_dict['control'].value)
                lines_to_save.append(param_line)

        self.lines_to_save = lines_to_save

    def _get_secion_name_line(self, sctn_name: str, spacers_to_fill: int = 5):
        filler_str = \
            ''.join([self.chunk_sep_spacer for el in range(spacers_to_fill)])
        return self.chunk_name_ptrn.format(filler_str, sctn_name, filler_str)

    def _set_all_params_vals(self):
        """
        Iterates through available params and appends hash map
        Returns
        -------

        """
        for section_key, section in self.su2_cfg_obj.parsed_su2_cfg.items():
            for param_name, param_dict in section.items():
                self.all_params_vals[param_name] = param_dict['control'].value

    def _append_params_to_lines(self):
        """
        Sets values from GUI to lines list
        Returns
        -------

        """

        # self.setting_oper_regex = '\s{0,1}=\s'
        # self.comment_regex = '^%'

        lines_to_save = []
        print(self._row_by_row_cfg)
        for cfg_line in self._row_by_row_cfg:
            if re.search(self.comment_regex, cfg_line):
                # print('cmntd line')
                lines_to_save.append(cfg_line)
                continue

            prm_srch_res = re.search(self.setting_oper_regex, cfg_line)

            if not prm_srch_res:
                # print('no `=` found')
                lines_to_save.append(cfg_line)
                continue

            prm_key = cfg_line[:prm_srch_res.start()]
            prm_val = self.all_params_vals.get(prm_key, None)
            if not prm_val:
                raise ValueError('Parameter: {} has no value set!'
                                 .format(prm_key))
            des_prm_line = self.param_setting_ptrn.format(prm_key, prm_val)
            # print(des_prm_line)
            lines_to_save.append(des_prm_line)

        if lines_to_save:
            self.lines_to_save = lines_to_save

    def write_cfg(self):
        """
        Saves cfg to a desired file
        Returns
        -------

        """
        with open(self.su2_cfg_obj.save_path, 'w') as cfg_out:
            cfg_out.writelines(self.lines_to_save)


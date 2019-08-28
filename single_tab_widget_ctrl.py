from pyforms.controls import ControlBase, ControlText, ControlCombo, \
    ControlCheckBox, ControlEmptyWidget, ControlLabel, ControlButton
from pyforms.basewidget import BaseWidget
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox, QWidget
from pyvalid import accepts, returns
import warnings

from config_param_creator_butt import ConfigParamCreatorButt
from helpers.helpers import get_from_yaml, get_from_yaml_and_set
from srfs_loader_widget import SurfLoader
from srfs_loader_ctrl import SurfLoadButton
from srfs_pick_button import SrfsPickerButton
from param_ctrl_utils import ParamOnOffSwitch
from su2_basic_widget import SU2BasicWidget
from su2_config_creator import SU2Config


class SingleTabWidgetCtrl:
    @property
    @returns(SU2Config)
    def su2_cfg_obj(self) -> SU2Config:
        return self._su2_cfg_obj

    @su2_cfg_obj.setter
    @accepts(object, SU2Config)
    def su2_cfg_obj(self, new_val: SU2Config):
        self._su2_cfg_obj = new_val

    @property
    @returns(str)
    def des_sect_name(self) -> str:
        return self._des_sect_name

    @des_sect_name.setter
    @accepts(object, str)
    def des_sect_name(self, new_val: str):
        self._des_sect_name = new_val

    @property
    @returns(dict)
    def section_def(self) -> dict:
        return self._section_def

    @section_def.setter
    @accepts(object, dict)
    def section_def(self, new_val: dict):
        self._section_def = new_val

    @property
    @returns(str)
    def fxd_des_section_name(self) -> str:
        return self._fxd_des_section_name

    @fxd_des_section_name.setter
    @accepts(object, str)
    def fxd_des_section_name(self, new_val: str):
        self._fxd_des_section_name = new_val

    @property
    @returns(list)
    def section_controls_names(self) -> list:
        return self._section_controls_names

    @section_controls_names.setter
    @accepts(object, list)
    def section_controls_names(self, new_val: list):
        self._section_controls_names = new_val

    @property
    @returns(SU2BasicWidget)
    def ctrld_tab(self) -> SU2BasicWidget:
        return self._ctrld_tab

    @ctrld_tab.setter
    @accepts(object, SU2BasicWidget)
    def ctrld_tab(self, new_val: SU2BasicWidget):
        self._ctrld_tab = new_val

    @property
    @returns(bool)
    def appnd_ctrls_to_cfg(self) -> bool:
        return self._appnd_ctrls_to_cfg

    @appnd_ctrls_to_cfg.setter
    @accepts(object, bool)
    def appnd_ctrls_to_cfg(self, new_val: bool):
        self._appnd_ctrls_to_cfg = new_val

    @property
    @returns(str)
    def global_cfg_pth(self) -> str:
        return self._global_cfg_pth

    @global_cfg_pth.setter
    @accepts(object, str)
    def global_cfg_pth(self, new_val: str):
        self._global_cfg_pth = new_val

    @property
    @returns(SurfLoadButton)
    def srfs_load_butt(self) -> SurfLoadButton:
        return self._srfs_load_butt

    @srfs_load_butt.setter
    @accepts(object, SurfLoadButton)
    def srfs_load_butt(self, new_val: SurfLoadButton):
        self._srfs_load_butt = new_val

    @property
    @returns(str)
    def msh_srfs_loader_butt_target_tab(self) -> str:
        return self._msh_srfs_loader_butt_target_tab

    @msh_srfs_loader_butt_target_tab.setter
    @accepts(object, str)
    def msh_srfs_loader_butt_target_tab(self, new_val: str):
        self._msh_srfs_loader_butt_target_tab = new_val

    @property
    @returns(str)
    def msh_prsng_params_pth(self):
        return self._msh_prsng_params_pth

    @msh_prsng_params_pth.setter
    @accepts(object, str)
    def msh_prsng_params_pth(self, new_val: str):
        self._msh_prsng_params_pth = new_val

    @property
    def tabs_ctrl(self) -> object:
        return self._tabs_ctrl

    @tabs_ctrl.setter
    def tabs_ctrl(self, new_val: object):
        self._tabs_ctrl = new_val

    # @accepts(object, object, SU2Config, str, str)
    def __init__(
            self, ctrld_tab, su2_cfg_obj: SU2Config, des_sect_name: str,
            tabs_ctrl: object, appnd_ctrls_to_cfg: bool = True,
            global_cfg_pth: str = 'main_cfg.yaml'):
        """
        Init with params

        Parameters
        ----------
        su2_cfg_obj: SU2Config
            cfg object which contains parsed config as a dict
        des_sect_name: str
            name of section to be converted into tab widget
        """
        self.su2_cfg_obj = su2_cfg_obj

        print('SingleTabWidgetCtrl su2_cfg_obj')
        print(self.su2_cfg_obj)

        self.tabs_ctrl = tabs_ctrl
        self.global_cfg_pth = global_cfg_pth
        self._set_msh_prsng_params_pth()
        self._set_msh_fname_section_key()
        # self._set_msh_pth_param_key()
        self.appnd_ctrls_to_cfg = appnd_ctrls_to_cfg
        self.des_sect_name = des_sect_name
        self.set_fxd_section_name()
        self._set_cfg_sect_def()
        self.section_controls_names = []
        self.ctrld_tab = ctrld_tab
        self.set_section_ctrls()
        self.set_tab_formset()

    def set_fxd_section_name(self):
        """
        Fixes the tab name so it can be used as a key
        Returns
        -------
        None
            None

        """
        ws_fxd_sect_name = self.des_sect_name.replace(' ', '_')
        self.fxd_des_section_name = ws_fxd_sect_name.replace('\n', '_')

    def _set_cfg_sect_def(self):
        """
        Sets desired section deff based on provided section name
        Returns
        -------
        None
            None

        """

        if not self.set_fxd_section_name:
            self.set_fxd_section_name()

        print('self.fxd_des_section_name')
        print(self.fxd_des_section_name)

        self.section_def = \
            self.su2_cfg_obj.parsed_su2_cfg.get(
                self.fxd_des_section_name, {})

        print('self.section_def')
        print(self.section_def)

        if not self.section_def:
            print('Section is empty')

            # raise ValueError('None instead of dict')

    def _get_param_ctrl_toogle(self, toogled_param: ControlBase):
        """
        Getter for param on-off toogle check box

        Parameters
        ----------
        toogled_param: ControlBase

        Returns
        -------
        ParamOnOffSwitch
            ControlCheckbox which turns on and off edition of param it is
            attached to

        """
        curr_param_toogle = ParamOnOffSwitch(toogled_param=toogled_param)
        return curr_param_toogle

    @accepts(object, QGroupBox, str)
    def _set_grpbx_stylesheet(
            self, modif_grpbx: QGroupBox, des_stylesheet: str = ''):
        appld_stylesheet = des_stylesheet
        if not des_stylesheet:
            appld_stylesheet = \
                'QGroupBox {' \
                'font-size: 12px;'\
                'font: Calibri;}'\
                'QGroupBox:title {'\
                'subcontrol-origin: margin;'\
                'subcontrol-position: top center;'\
                'padding-left: 10px;'\
                'padding-right: 10px;'\
                'padding-top: 12px; }'
        # print(appld_stylesheet)
        modif_grpbx.setStyleSheet(appld_stylesheet)

    @accepts(object, str, ControlBase, object)
    def _get_param_ctrl_cont(
            self, param_label: str,
            param_ctrl: ControlBase,
            srf_sel_button: ControlButton or None = None) -> ControlEmptyWidget:
        """
        Getter for entire 'param ensemble': label, control and on-off param
        edit toogle

        Parameters
        ----------
        param_label: ControlLabel
            control with param label
        param_ctrl: Control Base
            param control

        Returns
        -------
        ControlBaseWidget
            container with entire param control assembly

        """
        param_chckbox = self._get_param_ctrl_toogle(param_ctrl)
        curr_ctrl_groupbox = QGroupBox(param_label)
        self._set_grpbx_stylesheet(curr_ctrl_groupbox)

        vert_layout = QVBoxLayout(curr_ctrl_groupbox)
        first_grpbx_row = QHBoxLayout()
        param_ctrl.form.setMinimumWidth(200)
        param_ctrl.form.setMaximumWidth(200)
        first_grpbx_row.addWidget(param_ctrl.form)
        first_grpbx_row.addWidget(param_chckbox._form)

        vert_layout.addLayout(first_grpbx_row)
        if srf_sel_button is not None:
            srf_sel_button_cont = ControlEmptyWidget()
            srf_sel_button_cont.value = srf_sel_button
            vert_layout.addWidget(srf_sel_button_cont.form)

        curr_ctrl_cont = ControlEmptyWidget()

        curr_ctrl_cont._param_chckbox = param_chckbox
        curr_ctrl_cont.form.layout().addWidget(curr_ctrl_groupbox)  # curr_w

        return curr_ctrl_cont

    @accepts(object, str)
    @returns(ControlLabel)
    def _get_param_label(self, param_name: str) -> ControlLabel:
        curr_label = ControlLabel(param_name)
        # place for setting style
        label_font = QFont("Calibri", 10, QFont.Decorative)
        curr_label._form.label.setFont(label_font)

        return curr_label

    def _get_param_def_val(
            self, curr_param_def: dict, control_key: str,
            def_val_key: str) -> int or float or str:
        """
        Getter for default value of created control -> if control already
        exists the value is taken from it

        Parameters
        ----------
        curr_param_def: dict
            dict with the parameter info
        control_key: str
            by default 'control' - key to get control from dict
        def_val_key: str
            key to get default value from dict

        Returns
        -------
        int or float or str
            the default value of parsed parameter

        """
        curr_control = curr_param_def.get(control_key, None)
        if not curr_control:
            def_val = curr_param_def.get(def_val_key, None)
        else:
            def_val = curr_control.value
        return def_val

    @accepts(object, str, str, str, str, str)
    # @returns(ControlBase)
    def _get_param_ctrl(
            self, param_name: str, alwd_vals_key: str = 'allowed values',
            tooltip_key: str = 'tooltip', def_val_key: str = 'value',
            control_key: str = 'control'):
        """
        Based on param's definition gets proper Control (either text box or
        combo) for a given parameter

        Parameters
        ----------
        param_name: str
            name of the param for which the Control should be created

        Returns
        -------
        ControlBase
            desired control

        """

        curr_param_def = self.section_def.get(param_name, None)

        if not curr_param_def:
            warnings.warn(
                '{} param name was present in section def but no definition '
                'was found - creating plain text box ofr it')

        alwd_vals = curr_param_def.get(alwd_vals_key, None)
        tooltip = curr_param_def.get(tooltip_key, None)

        # curr_control = curr_param_def.get(control_key, None)
        #
        # if not curr_control:
        #     def_val = curr_param_def.get(def_val_key, None)
        # else:
        #     def_val = curr_control.value

        def_val = self._get_param_def_val(
            curr_param_def=curr_param_def, control_key=control_key,
            def_val_key=def_val_key)

        # print(alwd_vals)
        # print(tooltip)
        # print(def_val)

        param_srf_sel_butt = None
        if not alwd_vals:
            # param_ctrl = ControlText(param_name)
            param_ctrl = ControlText()
            if tooltip:
                param_ctrl.form.setToolTip(
                    '<FONT COLOR=black> {} </FONT>'.format(tooltip))
            param_ctrl.value = str(def_val)

            if self.fxd_des_section_name == \
                    self.msh_srfs_loader_butt_target_tab:
                param_srf_sel_butt = SrfsPickerButton(
                    su2_cfg_obj=self.su2_cfg_obj,
                    flld_ctrl_label=param_name,
                    flld_ctrl=param_ctrl,
                    bc_sect_key=self.fxd_des_section_name)

        else:
            # param_ctrl = ControlCombo(param_name)
            param_ctrl = ControlCombo()
            param_ctrl._label = param_name
            for alwd_val_name, alwd_val in alwd_vals.items():
                param_ctrl.add_item(alwd_val_name, alwd_val)
            if def_val:
                param_ctrl.value = str(def_val)

        # param_ctrl._form.resize(200, 50)

        # param_ctrl_label = self._get_param_label(param_name=param_name)
        param_ctrl_cont = \
            self._get_param_ctrl_cont(
                param_label=param_name,
                param_ctrl=param_ctrl,
                srf_sel_button=param_srf_sel_butt)

        if self.appnd_ctrls_to_cfg:
            self.appnd_ctrl_to_prsd_cfg(
                self.fxd_des_section_name, param_name, param_ctrl,
                param_ctrl_cont._param_chckbox,
                srf_sel_button=param_srf_sel_butt)
        # print('param_ctrl: ', param_name, ': ', param_ctrl)
        # param_ctrl._form.setLayout(QVBoxLayout())
        # return param_ctrl
        return param_ctrl_cont

    @accepts(object, str, str, ControlBase, ControlCheckBox, object)
    def appnd_ctrl_to_prsd_cfg(
            self, section_key: str, param_key: str, ctrl: ControlBase,
            ctrl_toogle: ControlCheckBox,
            srf_sel_button: ControlButton or None = None):
        self.su2_cfg_obj.parsed_su2_cfg[section_key][param_key]['control'] = \
            ctrl

        self.su2_cfg_obj \
            .parsed_su2_cfg[section_key][param_key]['control_toogle'] = \
            ctrl_toogle

        self.su2_cfg_obj \
            .parsed_su2_cfg[section_key][param_key]['srf_sel_button'] = \
            srf_sel_button

    def _set_msh_fname_section_key(self):
        """
        Setter for mesh control section key
        Returns
        -------

        """
        # target_obj: object, target_field_name: str,
        # value_key: str, yaml_pth: str):

        self.msh_srfs_loader_butt_target_tab = get_from_yaml(
            path_to_opts_yaml=self.msh_prsng_params_pth,
            desired_key='msh_srfs_loader_butt_target_tab',
            return_plain_val=True)

    # def _set_msh_pth_param_key(self):
    #     """
    #     Setter for mesh control param key
    #     Returns
    #     -------
    #
    #     """
    #     # target_obj: object, target_field_name: str,
    #     # value_key: str, yaml_pth: str):
    #
    #     self.msh_pth_param_key = get_from_yaml(
    #         path_to_opts_yaml=self.msh_prsng_params_pth,
    #         desired_key='msh_pth_param_key',
    #         return_plain_val=True)

    def _set_msh_prsng_params_pth(self):
        """
        Setter for mesh parsing param path
        Returns
        -------

        """
        self.msh_prsng_params_pth = get_from_yaml(
            path_to_opts_yaml=self.global_cfg_pth,
            desired_key='msh_prsng_params_pth',
            return_plain_val=True)

    # @returns(ControlButton)
    def _set_srfs_loader(self):
        """
        Setter for surface loader button
        Returns
        -------
        ControlButton

        """

        # self, su2_cfg_obj: SU2Config,
        # surf_loader_but_label: str = 'Load surfaces from su2 mesh',
        # msh_prsng_params_pth: str = 'su2_msh_parsing_params.yaml'

        _srfs_load_butt = \
            SurfLoader(
                su2_cfg_obj=self.su2_cfg_obj,
                surf_loader_but_label='Load surfaces from su2 mesh',
                msh_prsng_params_pth=self.msh_prsng_params_pth)

        load_butt_cont = ControlEmptyWidget()
        load_butt_cont.value = _srfs_load_butt

        # print(type(_srfs_load_butt))
        # print(isinstance(_srfs_load_butt, ControlButton))
        self.ctrld_tab._srfs_load_butt_cont = load_butt_cont  # load_butt_cont
        # return srfs_load_butt

    def _set_new_param_setter(self):
        """
        Sets a button which spawns new parameter creation dialog
        Returns
        -------

        """
        cpc = ConfigParamCreatorButt(
            su2_cfg_obj=self.su2_cfg_obj,
            des_cfg_section=self.fxd_des_section_name,
            tabs_ctrl=self.tabs_ctrl)

        cpc_cont = ControlEmptyWidget()
        cpc_cont.value = cpc

        self.ctrld_tab._cfg_param_creator = cpc_cont

    def set_section_ctrls(self):
        """
        Sets fields of a given tab using provided section definition
        Returns
        -------
        None
            None

        """
        # print(self.section_def)
        for param_name, param_def in self.section_def.items():
            param_ctrl = self._get_param_ctrl(param_name)
            ctrl_field_name = '_{}'.format(param_name)
            setattr(self.ctrld_tab, ctrl_field_name, param_ctrl)
            self.section_controls_names.append(ctrl_field_name)

    @returns(tuple)
    def _get_tab_title(self):
        """
        Getter for single tab title bar
        Returns
        -------
        tuple
            header row for created tab

        """
        return ' ', 'h4: {}'.format(self.des_sect_name.replace('\n', ' ')), ' '

    @accepts(object, list)
    @returns(list)
    def _get_final_tab_formset(self, ctrls_filled_formset: list):
        """
        Getter for final form of formset param for created tab
        Parameters
        ----------
        ctrls_filled_formset: list
            list of control rows

        Returns
        -------
        list
            final formset for created tab

        """

        final_formset = []
        header_row = self._get_tab_title()
        final_formset.append(header_row)
        for ctrls_formset_row in ctrls_filled_formset:
            final_formset.append(ctrls_formset_row)

        return final_formset.copy()

    def set_tab_formset(self):
        """
        Sets formset (hardcoded) for each tab
        Returns
        -------
        None
            None

        """
        form_row_template = []
        tab_formset = []
        row_idx = 0

        if self.fxd_des_section_name == self.msh_srfs_loader_butt_target_tab:
            print(self.fxd_des_section_name)
            print(self.msh_srfs_loader_butt_target_tab)

            print('SETTING LOADER')
            self._set_srfs_loader()
            tab_formset.append((' ', '_srfs_load_butt_cont', ' '))

        # TODO fix this -> should be a button starting a dialog
        self._set_new_param_setter()
        tab_formset.append((' ', '_cfg_param_creator', ' '))

        for ctrl_name in self.section_controls_names:
            if row_idx >= 3:
                row_idx = 0
                form_row_template.append('||')
                tab_formset.append(tuple(form_row_template))
                form_row_template = []

            form_row_template.append(' ')
            form_row_template.append(ctrl_name)
            row_idx += 1

        # if not tab_formset:
        form_row_template.append(' ')
        # if self.des_sect_name == get

        # print('#### des_sect_name ####')
        # print(self.fxd_des_section_name)
        # print(self.msh_srfs_loader_butt_target_tab)

        tab_formset.append(tuple(form_row_template))
        tab_formset.append(tuple([' ', ' ', ' ']))
        # print(tab_formset)
        self.ctrld_tab.formset = self._get_final_tab_formset(tab_formset)


if __name__ == '__main__':
    sample_dict = {
        'MU_CONSTANT': {
            'allowed values': {},
            'tooltip': 'Molecular Viscosity that would be constant',
            'value': 0},
        'MU_REF': {
            'allowed values': {},
            'tooltip': 'Molecular Viscosity that would be constant',
            'value': 1},
        }

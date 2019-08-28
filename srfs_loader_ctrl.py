from AnyQt.QtWidgets import QFileDialog
from copy import deepcopy
import os
from pprint import pprint
import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton, ControlText
from pyvalid import accepts, returns
from PyQt5.QtWidgets import QMessageBox
import warnings

from helpers.helpers import init_des_class_fields_frm_yaml, \
    get_from_dict_or_warn
from su2_config_creator import SU2Config
from su2_mesh_reader import SU2MshReader


class SurfLoaderCtrl:

    @property
    def ctrld_w(self) -> BaseWidget:
        return self._ctrld_w

    @ctrld_w.setter
    def ctrld_w(self, new_val: BaseWidget):
        self._ctrld_w = new_val

    @property
    def su2_cfg_obj(self) -> SU2Config:
        return self._su2_cfg_obj

    @su2_cfg_obj.setter
    def su2_cfg_obj(self, new_val: SU2Config):
        self._su2_cfg_obj = new_val

    @property
    def surf_loader_but_label(self) -> str:
        return self._surf_loader_but_label

    @surf_loader_but_label.setter
    def surf_loader_but_label(self, new_val: str):
        self._surf_loader_but_label = new_val

    @property
    def msh_prsng_params_pth(self) -> str:
        return self._msh_prsng_params_pth

    @msh_prsng_params_pth.setter
    def msh_prsng_params_pth(self, new_val: str):
        self._msh_prsng_params_pth = new_val

    def __init__(
            self, ctrld_w: BaseWidget,
            su2_cfg_obj: SU2Config,
            surf_loader_but_label: str = 'Load surfaces from su2 mesh',
            msh_prsng_params_pth: str = 'su2_msh_parsing_params.yaml'):
        self.ctrld_w = ctrld_w
        # self, label, su2_cfg_obj: SU2Config,
        # msh_prsng_params_pth

        self.su2_cfg_obj = su2_cfg_obj
        self.surf_loader_but_label = surf_loader_but_label
        self.msh_prsng_params_pth = msh_prsng_params_pth

        self.ctrld_w._srf_load_butt = SurfLoadButton(
            label=self.surf_loader_but_label,
            su2_cfg_obj=self.su2_cfg_obj,
            msh_prsng_params_pth=self.msh_prsng_params_pth)

        # self.ctrld_w.formset = [('_srf_load_butt ')]

        pass

    pass


class SurfLoadButton(ControlButton):

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
    def msh_prsng_params_pth(self) -> str:
        return self._msh_prsng_params_pth

    @msh_prsng_params_pth.setter
    @accepts(object, str)
    def msh_prsng_params_pth(self, new_val: str):
        self._msh_prsng_params_pth = new_val

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
    @returns(str)
    def param_ctrl_key(self) -> str:
        return self._param_ctrl_key

    @param_ctrl_key.setter
    @accepts(object, str)
    def param_ctrl_key(self, new_val: str):
        self._param_ctrl_key = new_val

    @property
    @returns(str)
    def msh_srfs_loader_butt_target_tab(self) -> str:
        return self._msh_srfs_loader_butt_target_tab

    @msh_srfs_loader_butt_target_tab.setter
    @accepts(object, str)
    def msh_srfs_loader_butt_target_tab(self, new_val: str):
        self._msh_srfs_loader_butt_target_tab = new_val

    # @property
    # def trgt_cfg_editor(self):
    #     return self._trgt_cfg_editor
    #
    # @trgt_cfg_editor.setter
    # @accepts(object, CFGEditorWidget)
    # def trgt_cfg_editor(self, new_val: CFGEditorWidget):
    #     self._trgt_cfg_editor = new_val

    # @property
    # @returns(VerticalTabsWidget)
    # def trgt_tabs_w(self):
    #     return self._trgt_tabs_w
    #
    # @trgt_tabs_w.setter
    # @accepts(object, VerticalTabsWidget)
    # def trgt_tabs_w(self, new_val: VerticalTabsWidget):
    #     self._trgt_tabs_w = new_val
    #
    # @property
    # @returns(CFGSectionSelWidget)
    # def trgt_sect_sel_w(self) -> CFGSectionSelWidget:
    #     return self._trgt_sect_sel_w
    #
    # @trgt_sect_sel_w.setter
    # @accepts(object, CFGSectionSelWidget)
    # def trgt_sect_sel_w(self, new_val: CFGSectionSelWidget):
    #     self._trgt_sect_sel_w = new_val

    def __init__(
            self, label: str = 'test_lab', su2_cfg_obj: SU2Config = SU2Config(),
            msh_prsng_params_pth: str = 'su2_msh_parsing_params.yaml'):
        super(SurfLoadButton, self).__init__(label)
        self.su2_cfg_obj = su2_cfg_obj
        self.msh_prsng_params_pth = msh_prsng_params_pth
        init_des_class_fields_frm_yaml(
            trgt_obj=self, yaml_pth=self.msh_prsng_params_pth,
            class_fields_names=[
                'msh_fname_tab_key', 'msh_fname_param_key',
                'param_ctrl_key', 'msh_srfs_loader_butt_target_tab'])
        # self._msh_surf_loader = ControlButton()
        self.value = self._file_oper_click

    def has_su2_cfg_msh_ctr(self):
        """
        Checks if msh path ctrl is present in cfg
        Returns
        -------
        bool
            flag - is msh pth present ni su2_cfg_obj or not

        """
        all_ctrls_dict = self.su2_cfg_obj.parsed_su2_cfg
        if not self.msh_fname_tab_key or \
                self.msh_fname_tab_key not in all_ctrls_dict.keys():
            return False

        if not self.msh_fname_param_key:
            return False

        section_dict = all_ctrls_dict.get(self.msh_fname_param_key, None)
        if not section_dict:
            return False

        return True

    def get_msh_pth_and_set_to_ctrl(self) -> str:
        """
        Gets msh path from dialog and sets it to control holding msh path
        Returns
        -------
        str
            msh path

        """
        msh_pth, _ = \
            QFileDialog.getOpenFileName(
                self.parent, self.label, self.value)

        # print('msh_pth')
        # print(msh_pth)
        # print(self.msh_fname_tab_key)
        # print(self.msh_fname_param_key)
        # print(self.param_ctrl_key)

        des_msh_pth_ctrl = \
            self.su2_cfg_obj.parsed_su2_cfg[self.msh_fname_tab_key]\
            [self.msh_fname_param_key][self.param_ctrl_key]

        # getting only the relaltive piece of the path for SU2 hangs otherwise
        semi_rel_pth = msh_pth.split(os.sep)[-1]
        print('### semi_rel_pth ###')
        print(semi_rel_pth)

        # des_msh_pth_ctrl.value = msh_pth
        des_msh_pth_ctrl.value = semi_rel_pth

        # des_msh_pth_ctrl.form.lineEdit.setText(msh_pth)

        return msh_pth

    def _get_msh_srfs_from_file(self, msh_pth: str):
        """
        Gets the msh surfaces from selected file
        Parameters
        ----------
        msh_pth: str
            path to mesh file

        Returns
        -------
        dict
            deepcopy of srfcs dict extracted from the provided msh file

        """
        mr = SU2MshReader()
        try:
            mr._set_srfs_frm_msh(msh_pth)
        except Exception as exc:
            QMessageBox.about(
                self._form,
                'File {} not found!'.format(msh_pth),
                'Please provide proper mesh path either in GUI '
                '(SECTION: {}, PARAM: {}) or in dialog'
                    .format(
                        self.msh_fname_tab_key,
                        self.msh_fname_param_key))
            msh_pth = self.get_msh_pth_and_set_to_ctrl()

            # msh_pth, _ = \
            #     QFileDialog.getOpenFileName(
            #         self.parent, self.label, self.value)
            if not msh_pth:
                return {}
                # self._get_msh_srfs_from_file(msh_pth='')

            mr._set_srfs_frm_msh(msh_pth)

        rtnd_srfs = deepcopy(mr.msh_srfs_map)
        return rtnd_srfs

    @accepts(object, dict)
    @returns(str)
    def _get_msh_pth_frm_gui(self):
        """
        Getter for mesh path parameter for provided params and given GUI run
        Returns
        -------
        str
            path to specified in cfg file or GUI mesh file

        """

        param_dict = self.su2_cfg_obj.parsed_su2_cfg

        sect_dict: dict = \
            get_from_dict_or_warn(
                input_dict=param_dict, des_key=self.msh_fname_tab_key)
        # sect_dict = param_dict.get(self.msh_pth_section_key, None)

        param_dict: dict = \
            get_from_dict_or_warn(
                input_dict=sect_dict, des_key=self.msh_fname_param_key)
        # param_dict = sect_dict.get(self.msh_pth_param_key, None)

        ctrl: ControlText = \
            get_from_dict_or_warn(
                input_dict=param_dict, des_key=self.param_ctrl_key)

        if not ctrl:
            return ''
        ctrl_val = ctrl.value
        if not ctrl_val:
            warnings.warn('No provided in text box - returning None')
            return ''
        return ctrl_val

    @returns(str)
    def get_msh_pth(self):
        """
        Gets su2 mesh path from GUI - if not possible gets it from dialog
        If no path is specified returns None
        Returns
        -------
        str
            string with mesh path or empty string if mesh path was not provided

        """

        msh_pth = self._get_msh_pth_frm_gui()

        # if msh_pth:
        #
        #     answ = QMessageBox.question(
        #         self._form, '',
        #         "Are you sure to load mesh from file: {}".format(msh_pth),
        #         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        #     if answ == QMessageBox.No:
        #         self.get_msh_pth_and_set_to_ctrl()

        # if not msh_pth:

        msh_pth = self.get_msh_pth_and_set_to_ctrl()

        # msh_pth, _ = \
        #     QFileDialog.getOpenFileName(
        #         self.parent, self.label, self.value)
        # set new path to msh
        # self.su2_cfg_obj.parsed_su2_cfg[msh_pth_section][msh_pth_param]['control'].value = msh_pth
        # warnings.warn('Provided msh path is empty!')
        # msh_pth = ''
        # if not msh_pth:

        return msh_pth

    def _reset_all_stashed_selections(self):
        """
        Resets all stashed selection form selections windows (per marker)
        Returns
        -------

        """
        bc_key = self.msh_srfs_loader_butt_target_tab
        surf_sel_ctrls_chunk = self.su2_cfg_obj.parsed_su2_cfg[bc_key]
        for param_name, param_dict in surf_sel_ctrls_chunk.items():
            pick_srf_but = param_dict.get('srf_sel_button', None)
            if pick_srf_but is None:
                continue
            pick_srf_but.surf_sel_win.surf_sel_w_ctrl.selected_surfs = []

    def _file_oper_click(self):

        # attempting to get mesh path from the GUI
        self._reset_all_stashed_selections()
        self.su2_cfg_obj.available_srfs = {}

        msh_pth = self.get_msh_pth()
        if not msh_pth:
            QMessageBox.about(
                self._form,
                'No SU2 mesh file specified!',
                'Please provide proper mesh path either in GUI '
                '(SECTION: {}, PARAM: {}) or in dialog'
                .format(self.msh_fname_tab_key, self.msh_fname_param_key))
        else:

            srf_map = self._get_msh_srfs_from_file(msh_pth=msh_pth)
            if not srf_map:
                QMessageBox.about(
                    self._form,
                    'No valid surfaces were found in provided SU2 mesh file!',
                    'Please check mesh under path: {} or specify new proper '
                    'mesh file path'.format(msh_pth))
            else:
                pprint(srf_map)
                self.su2_cfg_obj.available_srfs = deepcopy(srf_map)
                pprint('self.su2_cfg_obj.available_srfs')
                pprint(self.su2_cfg_obj.available_srfs)
                # self.su2_cfg_obj.taken_srfs = {}

                # if not self.has_su2_cfg_msh_ctr():
        #     msh_pth, _ = \
        #         QFileDialog.getOpenFileName(
        #             self.parent, self.label, self.value)
        # else:
        #     msh_pth =


if __name__ == '__main__':
    pyforms.start_app(SurfLoadButton)

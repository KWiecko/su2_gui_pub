from pyforms.controls import ControlButton, ControlText, ControlEmptyWidget, \
    ControlCheckBoxList
from PyQt5.QtWidgets import QMessageBox
import re

from helpers.helpers import replace_all_ws, get_pyqt_grpbox, \
    break_input_str_on_len
from su2_config_creator import SU2Config


class CFGSectionCreatorCtrl:

    @property
    def ctrld_w(self) -> object:
        return self._ctrld_w

    @ctrld_w.setter
    def ctrld_w(self, new_val: object):
        self._ctrld_w = new_val

    @property
    def su2_cfg_obj(self) -> SU2Config:
        return self._su2_cfg_obj

    @su2_cfg_obj.setter
    def su2_cfg_obj(self, new_val: SU2Config):
        self._su2_cfg_obj = new_val

    @property
    def tabs_ctrl(self) -> object:
        return self._tabs_ctrl

    @tabs_ctrl.setter
    def tabs_ctrl(self, new_val: object):
        self._tabs_ctrl = new_val

    @property
    def sections_list(self) -> ControlCheckBoxList:
        return self._sections_list

    @sections_list.setter
    def sections_list(self, new_val: ControlCheckBoxList):
        self._sections_list = new_val

    def __init__(
            self, su2_cfg_obj: SU2Config, ctrld_w: object, tabs_ctrl: object,
            sections_list: object = None):
        """
        Init w params
        Parameters
        ----------
        su2_cfg_obj: SU2Config
            cfg object to be used
        ctrld_w: object
            the controlled object
        tabs_ctrl
        """

        self.su2_cfg_obj = su2_cfg_obj
        self.ctrld_w = ctrld_w
        self.tabs_ctrl = tabs_ctrl
        # print('CFGSectionCreatorCtrl tabs_ctrl')
        # print(tabs_ctrl)
        # print('CFGSectionCreatorCtrl su2_cfg_obj')
        # print(su2_cfg_obj)
        self.sections_list = sections_list
        self._set_sect_creat_ctrls()
        self._set_ctrld_w_formset()

    def _set_sect_creat_ctrls(self):

        ctrl_txt = ControlText()
        self.ctrld_w.section_name_ctrl = ctrl_txt

        appld_stylesheet = \
            'QGroupBox {' \
            'font-size: 16px;'\
            'font: Calibri;}'\
            'QGroupBox:title {'\
            'subcontrol-origin: margin;'\
            'subcontrol-position: top center;'\
            'padding-left: 10px;'\
            'padding-right: 10px;'\
            'padding-top: 12px; }'

        # grpbox_desc: str, grpbox_stylesheet: str,
        # main_grpbox_ctrl: ControlBase, return_container: bool = True
        self.ctrld_w.section_name_ctrl_grpbox = get_pyqt_grpbox(
            grpbox_desc='Please provide the name of the new section',
            grpbox_stylesheet=appld_stylesheet, main_grpbox_ctrl=ctrl_txt)
        self.ctrld_w.section_name_ctrl_grpbox.form.setMinimumWidth(600)

        # set cancel button
        self.ctrld_w.cancel_butt = ControlButton()
        self.ctrld_w.cancel_butt.label = 'Cancel'
        self.ctrld_w.cancel_butt.value = self.ctrld_w.form.close

        set_sect_btn = CFGSectionCreatorButton(cfg_sect_creat_ctrl=self)

        self.ctrld_w.set_section_butt = set_sect_btn  # ControlButton()
        # self.ctrld_w.set_section_butt.label = 'Set section'
        # self.ctrld_w.set_section_butt.value = self.ctrld_w.form.close

    def _set_ctrld_w_formset(self):
        # section_name_ctrl
        self.ctrld_w.formset = \
            [(' ', '_section_name_ctrl_grpbox', ' '),
             (' ', '_set_section_butt', ' ', '_cancel_butt', ' ')]


class CFGSectionCreatorButton(ControlButton):

    @property
    def cfg_sect_creat_ctrl(self) -> CFGSectionCreatorCtrl:
        return self._cfg_sect_creat_ctrl

    @cfg_sect_creat_ctrl.setter
    def cfg_sect_creat_ctrl(self, new_val: CFGSectionCreatorCtrl):
        self._cfg_sect_creat_ctrl = new_val

    def __init__(
            self,  # su2_cfg_obj: SU2Config,
            cfg_sect_creat_ctrl: CFGSectionCreatorCtrl,
            sctn_butt_label: str = 'Create section'):
        super(CFGSectionCreatorButton, self).__init__(label=sctn_butt_label)
        self.cfg_sect_creat_ctrl = cfg_sect_creat_ctrl
        # self.su2_cfg_obj = su2_cfg_obj
        self.value = self.click

    def _prcs_sctn_name(self, input_sctn_name: str):
        """
        Process the provided section name
        Parameters
        ----------
        input_sctn_name: str
            section name to be processed

        Returns
        -------
        str, str
            the tab label and the section name

        """
        # replace all ws and tabs with single space
        single_ws_str = \
            replace_all_ws(input_str_like=input_sctn_name, ws_rplcmnt=' ')\
            .upper()
        # replace all ws and tabs with underscore
        usc_rplcd_ws = \
            replace_all_ws(input_str_like=single_ws_str, ws_rplcmnt='_')

        tab_n_w_nls = break_input_str_on_len(single_ws_str)

        return tab_n_w_nls, usc_rplcd_ws

    def _get_chckbx_l_names_w_states(self):
        curr_sect_n_list = list(self.cfg_sect_creat_ctrl.sections_list.value)

        curr_sect_states = []

        for sect_idx, sect_n in enumerate(curr_sect_n_list):
            state_int = self.cfg_sect_creat_ctrl.sections_list._form \
                .listWidget.item(sect_idx).checkState()
            state_bool = False if state_int == 0 else True
            curr_sect_states.append((sect_n, state_bool))

        return curr_sect_states

    def _add_value_to_chckbox(self, sect_n: str):

        curr_sect_states_l = self._get_chckbx_l_names_w_states()

        curr_sect_states_l.append((sect_n, True))
        self.cfg_sect_creat_ctrl.sections_list.value = \
            (el for el in curr_sect_states_l)

    def click(self):
        # get processed value
        crtd_sect_n = self.cfg_sect_creat_ctrl.ctrld_w.section_name_ctrl.value
        if not crtd_sect_n:
            QMessageBox.about(
                self.cfg_sect_creat_ctrl.ctrld_w.form,
                'Section name must not be empty!',
                'The name of the created section must not be an empty string')
            return

        fdx_tab_n, fxd_sect_n = \
            self._prcs_sctn_name(input_sctn_name=crtd_sect_n)
        # print(fdx_tab_n)

        if fxd_sect_n in \
                self.cfg_sect_creat_ctrl.su2_cfg_obj.parsed_su2_cfg.keys():
            QMessageBox.about(
                self.cfg_sect_creat_ctrl.ctrld_w.form,
                'Section is in the config',
                'The section name: {} is already present in the config!'
                    .format(fxd_sect_n))
            return

        self.cfg_sect_creat_ctrl.su2_cfg_obj.parsed_su2_cfg[fxd_sect_n] = {}

        print('cfg keys sections')
        print(self.cfg_sect_creat_ctrl.su2_cfg_obj.parsed_su2_cfg.keys())

        self.cfg_sect_creat_ctrl.tabs_ctrl.create_and_add_tab(fxd_sect_n)

        print('self.cfg_sect_creat_ctrl.sections_list.value')
        print(self.cfg_sect_creat_ctrl.sections_list.value)

        if self.cfg_sect_creat_ctrl.sections_list:
            self._add_value_to_chckbox(sect_n=fdx_tab_n)

        self.cfg_sect_creat_ctrl.ctrld_w.form.close()




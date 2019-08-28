from copy import deepcopy
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlBase, ControlCheckBoxList, ControlButton
from PyQt5.QtGui import QShowEvent, QCloseEvent
from pyvalid import accepts, returns
import warnings

from helpers.helpers import _get_numbers_from_splt_str
from su2_config_creator import SU2Config


class SurfSelectorCtrl:

    @property
    @returns(SU2Config)
    def su2_cfg_obj(self) -> SU2Config:
        return self._su2_cfg_obj

    @su2_cfg_obj.setter
    @accepts(object, SU2Config)
    def su2_cfg_obj(self, new_val: SU2Config):
        self._su2_cfg_obj = new_val

    @property
    @returns(ControlBase)
    def flld_ctrl(self) -> ControlBase:
        return self._flld_ctrl

    @flld_ctrl.setter
    @accepts(object, ControlBase)
    def flld_ctrl(self, new_val: ControlBase):
        self._flld_ctrl = new_val

    @property
    @returns(str)
    def flld_ctrl_label(self) -> str:
        return self._flld_ctrl_label

    @flld_ctrl_label.setter
    @accepts(object, str)
    def flld_ctrl_label(self, new_val: str):
        self._flld_ctrl_label = new_val

    @property
    @returns(BaseWidget)
    def ctrld_w(self) -> BaseWidget:
        return self._ctrld_w

    @ctrld_w.setter
    @accepts(object, BaseWidget)
    def ctrld_w(self, new_val: BaseWidget):
        self._ctrld_w = new_val

    @property
    @returns(str)
    def bc_sect_key(self) -> str:
        return self._bc_sect_key

    @bc_sect_key.setter
    @accepts(object, str)
    def bc_sect_key(self, new_val: str):
        self._bc_sect_key = new_val

    @property
    @returns(str)
    def no_srf_sel_mrkr(self) -> str:
        return self._no_srf_sel_mrkr

    @no_srf_sel_mrkr.setter
    @accepts(object, str)
    def no_srf_sel_mrkr(self, new_val: str):
        self._no_srf_sel_mrkr = new_val

    @property
    @returns(list)
    def selected_surfs(self) -> list:
        return self._selected_surfs

    @selected_surfs.setter
    @accepts(object, list)
    def selected_surfs(self, new_val: list):
        self._selected_surfs = deepcopy(new_val)

    @accepts(object, SU2Config, BaseWidget, str, ControlBase, str)
    def __init__(
            self,
            su2_cfg_obj: SU2Config,
            ctrld_w: BaseWidget,
            flld_ctrl_label: str,
            flld_ctrl: ControlBase,
            bc_sect_key: str,
            no_srf_sel_mrkr: str = '( NONE )'):

        self.su2_cfg_obj = su2_cfg_obj
        self.ctrld_w = ctrld_w
        self.bc_sect_key = bc_sect_key
        self.selected_surfs = []
        self.no_srf_sel_mrkr = no_srf_sel_mrkr

        self.flld_ctrl = flld_ctrl
        self.flld_ctrl_label = flld_ctrl_label

        self._set_chckbx_list()

        self.ctrld_w._apply_button = self._get_apply_button()
        self.ctrld_w._cancel_button = self._get_cancel_butt()

        self.ctrld_w.form.showEvent = self._show_event
        self.ctrld_w.form.closeEvent = self._close_event

    def _set_formset(self):
        self.ctrld_w.formset = [(' ', '_chckbx_list', ' '),
                                (' ', '_cancel_button', '_apply_button', ' ')]

    def _set_chckbx_list_vals(self):
        print('setting _set_chckbx_list_vals !')

        if not self.su2_cfg_obj.available_srfs:
            self.ctrld_w._chckbx_list.value = ()

        chckbx_list_vals = \
            [(srf_name, False)
             for srf_name, is_available
             in self.su2_cfg_obj.available_srfs.items()
             if is_available]

        curr_sel = [(srf_name, True) for srf_name in self.selected_surfs]
        # curr_sel_names = [srf_name for srf_name, _ in curr_sel]
        allowed_choices = tuple(curr_sel + chckbx_list_vals)

        self.ctrld_w._chckbx_list.value = allowed_choices

    def _set_chckbx_list(self):
        self.ctrld_w._chckbx_list = \
            ControlCheckBoxList(
                'Select desired surfaces for {} boundary'
                    .format(self.flld_ctrl_label))

        print('self.su2_cfg_obj.available_srfs')
        print(self.su2_cfg_obj.available_srfs)
        self._set_chckbx_list_vals()  # \
        # ((el, False) for el in self.su2_cfg_obj.available_srfs)

    def _toogle_lock_srfs_pickers(self, pickers_enabled: bool):
        srf_pick_ctrls = \
            self.su2_cfg_obj.parsed_su2_cfg[self.bc_sect_key]
        print('self.bc_sect_key')
        print(self.bc_sect_key)
        for param_name, param_dict in srf_pick_ctrls .items():
            # print(param_dict)
            param_srf_picker = param_dict.get('srf_sel_button', None)
            # print('param_srf_picker')
            # print(param_srf_picker)
            if param_srf_picker:
                param_srf_picker.enabled = pickers_enabled

    def _show_event(self, qt_show_event: QShowEvent):
        print(qt_show_event)
        self._set_chckbx_list_vals()
        # print(kwargs)
        self._toogle_lock_srfs_pickers(pickers_enabled=False)

    def _close_event(self, qt_close_event: QCloseEvent):
        # print(kwargs)
        print(qt_close_event)
        self.selected_surfs = self.ctrld_w._chckbx_list.value
        self._toogle_lock_srfs_pickers(pickers_enabled=True)

    def _get_apply_button(self):
        """
        Getter for apply button for surface selection widget
        Returns
        -------
        ControlButton
            button to apply changes

        """
        app_butt = ApplySrfSelButt(
            su2_cfg_obj=self.su2_cfg_obj,
            srf_sel_w_ctrl=self,
            no_srf_sel_mrkr=self.no_srf_sel_mrkr,
            butt_label='Select Surfaces')
        return app_butt

    def _get_cancel_butt(self):
        """
        Getter for cancel button for surface selection widget
        Returns
        -------
        ControlButton
            button for canceling selection

        """
        cancel_butt = CancelButt(srf_sel_w_ctrl=self)
        return cancel_butt


class ApplySrfSelButt(ControlButton):

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
    def butt_label(self) -> str:
        return self._butt_label

    @butt_label.setter
    @accepts(object, str)
    def butt_label(self, new_val: str):
        self._butt_label = new_val

    @property
    @returns(ControlCheckBoxList)
    def trgt_chckbx_lst(self) -> ControlCheckBoxList:
        return self._trgt_chckbx_lst

    @trgt_chckbx_lst.setter
    @accepts(object, ControlCheckBoxList)
    def trgt_chckbx_lst(self, new_val: ControlCheckBoxList):
        self._trgt_chckbx_lst = new_val

    @property
    @returns(ControlBase)
    def trgt_flld_ctrl(self) -> ControlBase:
        return self._trgt_flld_ctrl

    @trgt_flld_ctrl.setter
    @accepts(object, ControlBase)
    def trgt_flld_ctrl(self, new_val: ControlBase):
        self._trgt_flld_ctrl = new_val

    @property
    def trgt_srf_sel_w(self):
        return self._trgt_srf_sel_w

    @trgt_srf_sel_w.setter
    def trgt_srf_sel_w(self, new_val):
        self._trgt_srf_sel_w = new_val

    @property
    @returns(str)
    def no_srf_sel_mrkr(self) -> str:
        return self._no_srf_sel_mrkr

    @no_srf_sel_mrkr.setter
    @accepts(object, str)
    def no_srf_sel_mrkr(self, new_val: str):
        self._no_srf_sel_mrkr = new_val

    def __init__(
            self, su2_cfg_obj: SU2Config,
            srf_sel_w_ctrl: SurfSelectorCtrl,
            no_srf_sel_mrkr: str,
            butt_label: str = 'Select Surfaces'):

        self.butt_label = butt_label
        self.no_srf_sel_mrkr = no_srf_sel_mrkr

        super(ApplySrfSelButt, self).__init__(self.butt_label)

        self.su2_cfg_obj = su2_cfg_obj

        self.trgt_srf_sel_w = srf_sel_w_ctrl.ctrld_w
        self.trgt_chckbx_lst = srf_sel_w_ctrl.ctrld_w._chckbx_list
        self.trgt_flld_ctrl = srf_sel_w_ctrl.flld_ctrl

        self.value = self._apply_surf_sel

    @accepts(object, str)
    @returns(object)
    def _get_des_field_frm_cfg(self, des_field_name: str):
        """
        General purpose getter for su2 config object fields
        Parameters
        ----------
        des_field_name: str
            name od the desired field

        Returns
        -------
        object
            desired field form su2 config

        """

        des_field = getattr(self.su2_cfg_obj, des_field_name)

        if not des_field:
            return {}

        if not isinstance(des_field, dict):
            warnings.warn(
                '{} field should be a dict and is a {} instead - returning '
                'empty dict'.format(des_field_name, type(des_field)))
            return {}

        return deepcopy(des_field)

    @accepts(object, list)
    @returns(str)
    def join_srfs_name_w_coma(self, srfs_names: list) -> str:
        """
        Joins surfaces' names with coma
        Parameters
        ----------
        srfs_names: list

        Returns
        -------
        str
            string of joined surf names w coma

        """
        return ', '.join(srfs_names)

    def _get_flld_ctrl_str(
            self, des_srfs: list,
            flld_ctrl_pttrn: str = '({})',
            flld_ctrl_val_join_mthd: str = 'join_srfs_name_w_coma'):
        """
        Getter for surf names filled  control value
        (gets string of surfs form selected surf list)
        Parameters
        ----------
        des_srfs: list
            list of surf names to parse
        flld_ctrl_pttrn: str
            container for surface marker tags (i.e. parenthesis in
            `( marker_tag1, ...)`)
        flld_ctrl_val_join_mthd: str
            name of  method used for joining surface names

        Returns
        -------
        str
            string with desired surface names

        """
        joiner_mthd = getattr(self, flld_ctrl_val_join_mthd)
        joined_srfs = joiner_mthd(des_srfs)
        res_str = flld_ctrl_pttrn.format(joined_srfs)
        return res_str

    # @staticmethod
    # @accepts(ControlCheckBoxList, SU2Config)
    def _apply_surf_sel(self):
        """
        Applies surface selection to provided filled controlled value
        Returns
        -------

        """
        # all_ctrl_srfs = self.trgt_chckbx_lst.value
        all_ctrl_srfs = self.trgt_chckbx_lst.items
        print(all_ctrl_srfs)

        sel_srfs = [el for el, state in all_ctrl_srfs if state]

        print(sel_srfs)

        if not sel_srfs:
            self.trgt_flld_ctrl.value = self.no_srf_sel_mrkr
        else:

            nums_from_flld_ctrl = \
                _get_numbers_from_splt_str(self.trgt_flld_ctrl.value)

            srfs_and_nums = sel_srfs + nums_from_flld_ctrl

            self.trgt_flld_ctrl.value = \
                self._get_flld_ctrl_str(
                    des_srfs=srfs_and_nums, flld_ctrl_pttrn='({})',
                    flld_ctrl_val_join_mthd='join_srfs_name_w_coma')

        available_srfs = self._get_des_field_frm_cfg('available_srfs')
        print(available_srfs)
        # taken_srfs = self._get_des_field_frm_cfg('taken_srfs')

        for el, is_chckd in all_ctrl_srfs:
            if not is_chckd:
                available_srfs[el] = True
                # taken_srfs[el] = False
            else:
                available_srfs[el] = False
                # taken_srfs[el] = True

        self.su2_cfg_obj.available_srfs = deepcopy(available_srfs)
        self.trgt_srf_sel_w.close()
        # self.su2_cfg_obj.taken_srfs = deepcopy(taken_srfs)

        # close window


class CancelButt(ControlButton):

    @property
    # TODO fill in types
    def trgt_srf_sel_w(self):
        return self._trgt_srf_sel_w

    @trgt_srf_sel_w.setter
    def trgt_srf_sel_w(self, new_val):
        self._trgt_srf_sel_w = new_val

    # @property
    # def bc_tab(self):
    #     return self._bc_tab
    #
    # @bc_tab.setter
    # def bc_tab(self, new_val):
    #     self._bc_tab = new_val

    def __init__(self, srf_sel_w_ctrl: SurfSelectorCtrl):
        super(CancelButt, self).__init__('Cancel')
        self.trgt_srf_sel_w = srf_sel_w_ctrl.ctrld_w
        self.value = self._cls_win

    def _cls_win(self):
        print('Closing window')
        self.trgt_srf_sel_w.close()
        pass

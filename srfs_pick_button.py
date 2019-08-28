from pyforms.controls import ControlBase, ControlButton
from pyvalid import accepts, returns
from PyQt5.QtWidgets import QMessageBox

from su2_config_creator import SU2Config
from surf_sel_widget import SurfSelector


class SrfsPickerButton(ControlButton):

    @property
    def bc_tab(self):
        return self._bc_tab

    @bc_tab.setter
    def bc_tab(self, new_val):
        self._bc_tab = new_val

    @property
    def surf_sel_win(self):
        return self._surf_sel_win

    @surf_sel_win.setter
    def surf_sel_win(self, new_val):
        self._surf_sel_win = new_val

    @property
    @returns(SU2Config)
    def su2_cfg_obj(self) -> SU2Config:
        return self._su2_cfg_obj

    @su2_cfg_obj.setter
    def su2_cfg_obj(self, new_val: SU2Config):
        self._su2_cfg_obj = new_val

    def __init__(
            self,
            su2_cfg_obj: SU2Config,
            flld_ctrl_label: str,
            flld_ctrl: ControlBase,
            bc_sect_key: str):

        super(SrfsPickerButton, self).__init__(
            'Pick surfs for {}'.format(flld_ctrl_label))

        self.form.setStyleSheet("QPushButton{font-size: 11px}")

        self._su2_cfg_obj = su2_cfg_obj

        self.surf_sel_win = SurfSelector(
            su2_cfg_obj=su2_cfg_obj,
            flld_ctrl_label=flld_ctrl_label,
            flld_ctrl=flld_ctrl,
            bc_sect_key=bc_sect_key)

        # self.click = self._show_srf_sel_win
        # self.value = lambda x: print('test')
        self.value = self._file_oper_click

    def _file_oper_click(self):
        # self.srf_sel_win.parent = self.bc_tab
        # print('window should open')
        if not self.su2_cfg_obj.available_srfs:
            QMessageBox.about(
                self.form,
                'Warning !',
                'No surfaces to assign found - please read proper mesh file')
        elif not any(
                is_avail for srf_name, is_avail
                in self.su2_cfg_obj.available_srfs.items()) \
                and not self.surf_sel_win.surf_sel_w_ctrl.selected_surfs:
            # print(all(
            #     is_avail for srf_name, is_avail
            #     in self.su2_cfg_obj.available_srfs.items()))
            QMessageBox.about(
                self.form,
                'Warning !',
                'All surfaces have already been assigned !')
        else:
            self.surf_sel_win.form.show()

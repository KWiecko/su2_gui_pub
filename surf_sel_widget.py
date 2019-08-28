from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlBase, ControlCheckBoxList, ControlButton, \
    ControlDockWidget
from pyvalid import accepts, returns

from su2_config_creator import SU2Config
from surf_sel_widget_ctrl import SurfSelectorCtrl


class SurfSelector(BaseWidget):

    @property
    @returns(ControlCheckBoxList)
    def _chckbx_list(self) -> ControlCheckBoxList:
        return self.__chckbx_list

    @_chckbx_list.setter
    @accepts(object, ControlCheckBoxList)
    def _chckbx_list(self, new_val: ControlCheckBoxList):
        self.__chckbx_list = new_val

    @property
    @returns(ControlButton)
    def _apply_button(self) -> ControlButton:
        return self.__apply_button

    @_apply_button.setter
    @accepts(object, ControlButton)
    def _apply_button(self, new_val: ControlButton):
        self.__apply_button = new_val
        
    @property
    @returns(ControlButton)
    def _cancel_button(self) -> ControlButton:
        return self.__cancel_button

    @_cancel_button.setter
    @accepts(object, ControlButton)
    def _cancel_button(self, new_val: ControlButton):
        self.__cancel_button = new_val

    @property
    @returns(SurfSelectorCtrl)
    def surf_sel_w_ctrl(self) -> SurfSelectorCtrl:
        return self._surf_sel_w_ctrl

    @surf_sel_w_ctrl.setter
    @accepts(object, SurfSelectorCtrl)
    def surf_sel_w_ctrl(self, new_val: SurfSelectorCtrl):
        self._surf_sel_w_ctrl = new_val

    # @property
    # @returns(str)
    # def flld_ctrl_label(self) -> str:
    #     return self._flld_ctrl_label
    #
    # @flld_ctrl_label.setter
    # @accepts(object, str)
    # def flld_ctrl_label(self, new_val: str):
    #     self._flld_ctrl_label = new_val

    # @accepts(object, SU2Config, ControlBase)
    def __init__(
            self, su2_cfg_obj: SU2Config,
            flld_ctrl_label: str, flld_ctrl: ControlBase, bc_sect_key: str):
        super(SurfSelector, self).__init__(
            label='Select surfaces for {}'.format(flld_ctrl_label))
        self.surf_sel_w_ctrl = \
            SurfSelectorCtrl(
                su2_cfg_obj=su2_cfg_obj,
                ctrld_w=self,
                flld_ctrl_label=flld_ctrl_label,
                flld_ctrl=flld_ctrl,
                bc_sect_key=bc_sect_key)



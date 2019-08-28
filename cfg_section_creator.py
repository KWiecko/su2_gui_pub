import pyforms
from pyforms.controls import ControlButton, ControlText, ControlEmptyWidget, \
    ControlCheckBoxList

from cfg_section_creator_ctrl import CFGSectionCreatorCtrl
from su2_basic_widget import SU2BasicWidget
from su2_config_creator import SU2Config


class CFGSectionCreator(SU2BasicWidget):

    # @property
    # def example_txt_box(self) -> ControlText:
    #     return self._example_txt_box
    #
    # @example_txt_box.setter
    # def example_txt_box(self, new_val: ControlText):
    #     self._example_txt_box = new_val

    @property
    def section_name_ctrl_grpbox(self) -> ControlEmptyWidget:
        return self._section_name_ctrl_grpbox

    @section_name_ctrl_grpbox.setter
    def section_name_ctrl_grpbox(self, new_val: ControlEmptyWidget):
        self._section_name_ctrl_grpbox = new_val

    @property
    def curr_w_ctrl(self) -> CFGSectionCreatorCtrl:
        return self._curr_w_ctrl

    @curr_w_ctrl.setter
    def curr_w_ctrl(self, new_val: CFGSectionCreatorCtrl):
        self._curr_w_ctrl = new_val

    @property
    def section_name_ctrl(self) -> ControlText:
        return self._section_name_ctrl

    @section_name_ctrl.setter
    def section_name_ctrl(self, new_val: ControlText):
        self._section_name_ctrl = new_val

    @property
    def set_section_butt(self) -> ControlButton:
        return self._set_section_butt

    @set_section_butt.setter
    def set_section_butt(self, new_val: ControlButton):
        self._set_section_butt = new_val

    @property
    def cancel_butt(self) -> ControlButton:
        return self._cancel_butt

    @cancel_butt.setter
    def cancel_butt(self, new_val: ControlButton):
        self._cancel_butt = new_val

    def __init__(
            self, su2_cfg_obj: SU2Config = SU2Config(),
            sections_list: ControlCheckBoxList = None,
            tabs_ctrl: object = None,
            label='CFG section creator',
            initial_max_width: int = 400,
            initial_max_height: int = 700, initial_min_width: int = 200,
            initial_min_height: int = 500):

        super(CFGSectionCreator, self).__init__(
            label=label, initial_max_width=initial_max_width,
            initial_max_height=initial_max_height,
            initial_min_width=initial_min_width,
            initial_min_height=initial_min_height)

        # if not su2_cfg_obj:
        #     su2_cfg_obj = SU2Config()

        # print('CFGSectionCreator su2_cfg_obj')
        # print(su2_cfg_obj)

        self.curr_w_ctrl = \
            CFGSectionCreatorCtrl(
                su2_cfg_obj=su2_cfg_obj, ctrld_w=self, tabs_ctrl=tabs_ctrl,
                sections_list=sections_list)

        # self.section_name_ctrl = ControlText()


if __name__ == '__main__':
    pyforms.start_app(CFGSectionCreator, geometry=(400, 500, 500, 500))

import pyforms
from pyforms.controls import ControlButton, ControlCheckBoxList

from su2_config_creator import SU2Config
from su2_basic_widget import SU2BasicWidget
from cfg_section_creator_butt_ctrl import CFGSectionCreatorButtonCtrl


class CFGSectionCreatorButton(SU2BasicWidget):

    @property
    def ctrl(self) -> CFGSectionCreatorButtonCtrl:
        return self._ctrl

    @ctrl.setter
    def ctrl(self, new_val: CFGSectionCreatorButtonCtrl):
        self._ctrl = new_val

    @property
    def create_sect_butt(self) -> ControlButton:
        return self._create_sect_butt

    @create_sect_butt.setter
    def create_sect_butt(self, new_val: ControlButton):
        self._create_sect_butt = new_val

    def __init__(
            self, su2_cfg_obj: SU2Config = SU2Config(),
            tabs_ctrl: object = None,
            sections_list: ControlCheckBoxList = None):
        super(CFGSectionCreatorButton, self).__init__()

        # print('CFGSectionCreatorButton su2_cfg_obj')
        # print(su2_cfg_obj)

        # print('CFGSectionCreatorButton tabs_ctrl')
        # print(tabs_ctrl)
        # input('CFGSectionCreatorButton tabs_ctrl')

        self.ctrl = \
            CFGSectionCreatorButtonCtrl(
                ctrld_w=self, su2_cfg_obj=su2_cfg_obj, tabs_ctrl=tabs_ctrl,
                sections_list=sections_list)


if __name__ == '__main__':
    pyforms.start_app(CFGSectionCreatorButton, geometry=(400, 500, 500, 500))

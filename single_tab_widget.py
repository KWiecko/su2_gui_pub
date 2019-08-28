from pyvalid import accepts, returns
import pyforms

from single_tab_widget_ctrl import SingleTabWidgetCtrl
from su2_basic_widget import SU2BasicWidget
from su2_config_creator import SU2Config


class SingleTabWidget(SU2BasicWidget):

    @property
    @returns(SingleTabWidgetCtrl)
    def single_tab_ctrl(self) -> SingleTabWidgetCtrl:
        return self._single_tab_ctrl

    @single_tab_ctrl.setter
    @accepts(object, SingleTabWidgetCtrl)
    def single_tab_ctrl(self, new_val: SingleTabWidgetCtrl):
        self._single_tab_ctrl = new_val

    # @accepts(object, SU2Config or None, str)
    def __init__(
            self, su2_cfg_obj: SU2Config = None,
            des_sect_name: str = 'VISCOSITY_MODEL', tabs_ctrl: object = None):
        super(SingleTabWidget, self).__init__()
        if not su2_cfg_obj:
            su2_cfg_obj = \
                SU2Config(
                    path_to_cfg='parsed_cfgs/152721_22272019_su2_cfg.yaml')
        self.single_tab_ctrl = \
            SingleTabWidgetCtrl(
                self, su2_cfg_obj=su2_cfg_obj, des_sect_name=des_sect_name,
                tabs_ctrl=tabs_ctrl)


if __name__ == '__main__':
    pyforms.start_app(SingleTabWidget)

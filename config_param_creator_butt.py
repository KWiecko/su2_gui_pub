from pyforms.controls import ControlButton

from config_param_creator_butt_ctrl import ConfigParamCreatorButtCtrl
from su2_basic_widget import SU2BasicWidget
from su2_config_creator import SU2Config


class ConfigParamCreatorButt(SU2BasicWidget):

    @property
    def ctrl(self) -> ConfigParamCreatorButtCtrl:
        return self._ctrl

    @ctrl.setter
    def ctrl(self, new_val: ConfigParamCreatorButtCtrl):
        self._ctrl = new_val

    @property
    def create_param_butt(self) -> ControlButton:
        return self._create_param_butt

    @create_param_butt.setter
    def create_param_butt(self, new_val: ControlButton):
        self._create_param_butt = new_val

    def __init__(
            self, tabs_ctrl: object,
            su2_cfg_obj: SU2Config = None,
            des_cfg_section: str = 'INPUT_OUTPUT_INFORMATION'):

        super(ConfigParamCreatorButt, self).__init__()

        self.ctrl = \
            ConfigParamCreatorButtCtrl(
                ctrld_w=self, su2_cfg_obj=su2_cfg_obj,
                des_cfg_section=des_cfg_section, tabs_ctrl=tabs_ctrl)
        # self.formset = ['_create_param_butt']


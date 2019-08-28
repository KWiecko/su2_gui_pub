import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton, ControlBase

from su2_basic_widget import SU2BasicWidget
from su2_config_creator import SU2Config
from config_param_creator_ctrl import ConfigParamCreatorCtrl


class ConfigParamCreator(SU2BasicWidget):
    # label = '', initial_max_width = None, initial_max_height = None,
    # initial_min_width = None, initial_min_height = None)

    # @property
    # def param_name_ctrl(self) -> ControlBase:
    #     return self._param_name_ctrl
    #
    # @param_name_ctrl.setter
    # def param_name_ctrl(self, new_val: ControlBase):
    #     self._param_name_ctrl = new_val

    @property
    def param_name_ctrl_grpbx(self) -> ControlBase:
        return self._param_name_ctrl_grpbx

    @param_name_ctrl_grpbx.setter
    def param_name_ctrl_grpbx(self, new_val: ControlBase):
        self._param_name_ctrl_grpbx = new_val

    # @property
    # def allwd_vals_ctrl(self) -> ControlBase:
    #     return self._allwd_vals_ctrl
    #
    # @allwd_vals_ctrl.setter
    # def allwd_vals_ctrl(self, new_val: ControlBase):
    #     self._allwd_vals_ctrl = new_val

    @property
    def allwd_vals_ctrl_grpbx(self) -> ControlBase:
        return self._allwd_vals_ctrl_grpbx

    @allwd_vals_ctrl_grpbx.setter
    def allwd_vals_ctrl_grpbx(self, new_val: ControlBase):
        self._allwd_vals_ctrl_grpbx = new_val

    # @property
    # def default_val_ctrl(self) -> ControlBase:
    #     return self._default_val_ctrl
    #
    # @default_val_ctrl.setter
    # def default_val_ctrl(self, new_val: ControlBase):
    #     self._default_val_ctrl = new_val

    @property
    def default_val_ctrl_grpbx(self) -> ControlBase:
        return self._default_val_ctrl_grpbx

    @default_val_ctrl_grpbx.setter
    def default_val_ctrl_grpbx(self, new_val: ControlBase):
        self._default_val_ctrl_grpbx = new_val

    # @property
    # def tooltip_ctrl(self) -> ControlBase:
    #     return self._tooltip_ctrl
    #
    # @tooltip_ctrl.setter
    # def tooltip_ctrl(self, new_val: ControlBase):
    #     self._tooltip_ctrl = new_val

    @property
    def tooltip_ctrl_grpbx(self) -> ControlBase:
        return self._tooltip_ctrl_grpbx

    @tooltip_ctrl_grpbx.setter
    def tooltip_ctrl_grpbx(self, new_val: ControlBase):
        self._tooltip_ctrl_grpbx = new_val

    @property
    def ctrld_cfg_f_creator(self) -> object:
        return self._ctrld_cfg_f_creator

    @ctrld_cfg_f_creator.setter
    def ctrld_cfg_f_creator(self, new_val: object):
        self._ctrld_cfg_f_creator = new_val

    @property
    def config_field_creator_ctr(self) -> ConfigParamCreatorCtrl:
        return self._config_field_creator_ctr

    @config_field_creator_ctr.setter
    def config_field_creator_ctr(self, new_val: ConfigParamCreatorCtrl):
        self._config_field_creator_ctr = new_val

    @property
    def set_param_button(self) -> ControlButton:
        return self._set_param_button

    @set_param_button.setter
    def set_param_button(self, new_val: ControlButton):
        self._set_param_button = new_val

    @property
    def cancel_button(self) -> ControlButton:
        return self._cancel_button

    @cancel_button.setter
    def cancel_button(self, new_val: ControlButton):
        self._cancel_button = new_val

    def __init__(
            self, tabs_ctrl: object, label='Config param creator',
            initial_max_width: int = 400,
            initial_max_height: int = 700, initial_min_width: int = 200,
            initial_min_height: int = 500,
            su2_cfg_obj: SU2Config = None,  # {'example_sect': {}},
            des_cfg_section: str = 'INPUT_OUTPUT_INFORMATION'):

        super(ConfigParamCreator, self).__init__(
            label=label, initial_max_width=initial_max_width,
            initial_max_height=initial_max_height,
            initial_min_width=initial_min_width,
            initial_min_height=initial_min_height)

        if not su2_cfg_obj:
            print('SU2 cfg was not found')
            su2_cfg_obj = SU2Config()
            input('SU2 cfg was not found')

        self.config_field_creator_ctr = \
            ConfigParamCreatorCtrl(
                su2_cfg_obj=su2_cfg_obj, des_cfg_section=des_cfg_section,
                ctrld_cfg_f_creator=self, tabs_ctrl=tabs_ctrl)


if __name__ == '__main__':
    pyforms.start_app(ConfigParamCreator, geometry=(400, 500, 500, 500))
    # test_cfc = ConfigFieldCreator()
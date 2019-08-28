from pyforms.controls import ControlButton, ControlEmptyWidget
from pyvalid import accepts, returns

from config_param_creator import ConfigParamCreator
from su2_config_creator import SU2Config


class ConfigParamCreatorButtCtrl:

    @property
    def ctrld_w(self):
        return self._ctrld_w

    @ctrld_w.setter
    def ctrld_w(self, new_val):
        self._ctrld_w = new_val

    @property
    def su2_cfg_obj(self) -> SU2Config:
        return self._su2_cfg_obj

    @su2_cfg_obj.setter
    def su2_cfg_obj(self, new_val: SU2Config):
        self._su2_cfg_obj = new_val

    @property
    def des_cfg_section(self) -> str:
        return self._des_cfg_section

    @des_cfg_section.setter
    def des_cfg_section(self, new_val: str):
        self._des_cfg_section = new_val

    @property
    def cfg_param_creator_butt_label(self) -> str:
        return self._cfg_param_creator_butt_label

    @cfg_param_creator_butt_label.setter
    def cfg_param_creator_butt_label(self, new_val: str):
        self._cfg_param_creator_butt_label = new_val

    @property
    def tabs_ctrl(self) -> object:
        return self._tabs_ctrl

    @tabs_ctrl.setter
    def tabs_ctrl(self, new_val: object):
        self._tabs_ctrl = new_val

    def __init__(
            self, ctrld_w, tabs_ctrl, su2_cfg_obj: SU2Config = None,
            des_cfg_section: str = 'INPUT_OUTPUT_INFORMATION',
            cfg_param_creator_butt_label: str = 'Add new parameter'):
        self.ctrld_w = ctrld_w
        self.tabs_ctrl = tabs_ctrl
        self.su2_cfg_obj = su2_cfg_obj
        self.des_cfg_section = des_cfg_section
        self.cfg_param_creator_butt_label = cfg_param_creator_butt_label
        self._set_cfg_param_creator_butt()

    def _set_cfg_param_creator_butt(self):
        # su2_cfg: SU2Config = None,
        # des_cfg_section: str = 'INPUT_OUTPUT_INFORMATION',
        # cfg_param_creator_butt_label: str = 'Add new parameter'
        butt_cont = ControlEmptyWidget()
        # butt_cont.value = \
        cpb = \
            CreateParamButt(
                su2_cfg_obj=self.su2_cfg_obj,
                des_cfg_section=self.des_cfg_section,
                cfg_param_creator_butt_label=self.cfg_param_creator_butt_label,
                tabs_ctrl=self.tabs_ctrl)
        self.ctrld_w.create_sect_butt = cpb


class CreateParamButt(ControlButton):

    @property
    @returns(SU2Config)
    def su2_cfg_obj(self) -> SU2Config:
        return self._su2_cfg_obj

    @su2_cfg_obj.setter
    @accepts(object, SU2Config)
    def su2_cfg_obj(self, new_val: SU2Config):
        self._su2_cfg_obj = new_val

    @property
    def des_cfg_section(self) -> str:
        return self._des_cfg_section

    @des_cfg_section.setter
    def des_cfg_section(self, new_val: str):
        self._des_cfg_section = new_val

    @property
    def cfg_param_creator(self) -> ConfigParamCreator:
        return self._cfg_param_creator

    @cfg_param_creator.setter
    def cfg_param_creator(self, new_val: ConfigParamCreator):
        self._cfg_param_creator = new_val

    @property
    def tabs_ctrl(self) -> object:
        return self._tabs_ctrl

    @tabs_ctrl.setter
    def tabs_ctrl(self, new_val: object):
        self._tabs_ctrl = new_val

    def __init__(
            self, tabs_ctrl: object, su2_cfg_obj: SU2Config = None,
            des_cfg_section: str = 'INPUT_OUTPUT_INFORMATION',
            cfg_param_creator_butt_label: str = 'Add new parameter'):

        super(CreateParamButt, self).__init__(cfg_param_creator_butt_label)

        self.su2_cfg_obj = su2_cfg_obj
        self.tabs_ctrl = tabs_ctrl
        self.des_cfg_section = des_cfg_section
        self.value = self._click
        self._set_cfg_param_creator()

    def _set_cfg_param_creator(self):
        self.cfg_param_creator = \
            ConfigParamCreator(
                su2_cfg_obj=self.su2_cfg_obj, des_cfg_section=self.des_cfg_section,
                tabs_ctrl=self.tabs_ctrl)

    def _click(self):
        self.cfg_param_creator.form.show()



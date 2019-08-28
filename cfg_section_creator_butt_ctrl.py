from pyforms.controls import ControlButton, ControlCheckBoxList

from cfg_section_creator import CFGSectionCreator
from su2_config_creator import SU2Config


class CFGSectionCreatorButtonCtrl:

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
    def ctrld_w(self) -> object:
        return self._ctrld_w

    @ctrld_w.setter
    def ctrld_w(self, new_val: object):
        self._ctrld_w = new_val

    @property
    def sections_list(self) -> ControlCheckBoxList:
        return self._sections_list

    @sections_list.setter
    def sections_list(self, new_val: ControlCheckBoxList):
        self._sections_list = new_val

    def __init__(
            self, ctrld_w: object, su2_cfg_obj: SU2Config = SU2Config(),
            tabs_ctrl: object = None,
            sections_list: ControlCheckBoxList = None):
        self.ctrld_w = ctrld_w
        self.su2_cfg_obj = su2_cfg_obj
        self.tabs_ctrl = tabs_ctrl
        self.sections_list = sections_list
        self._set_create_sect_butt()

        # print('CFGSectionCreatorButtonCtrl su2_cfg_obj')
        # print(su2_cfg_obj)

        # print('CFGSectionCreatorButtonCtrl tabs_ctrl')
        # print(self.tabs_ctrl)
        # input('CFGSectionCreatorButtonCtrl tabs_ctrl')

    def _set_create_sect_butt(self):
        self.ctrld_w.create_sect_butt = \
            CreateSectButt(
                tabs_ctrl=self.tabs_ctrl, sections_list=self.sections_list,
                su2_cfg_obj=self.su2_cfg_obj)
        # self.ctrld_w.create_sect_butt.label = 'Create new section'
        # self.ctrld_w.create_sect_butt.value = lambda x: print('click')


class CreateSectButt(ControlButton):

    @property
    def su2_cfg_obj(self) -> SU2Config:
        return self._su2_cfg_obj

    @su2_cfg_obj.setter
    def su2_cfg_obj(self, new_val: SU2Config):
        self._su2_cfg_obj = new_val

    @property
    def cfg_sect_creator(self) -> CFGSectionCreator:
        return self._cfg_sect_creator

    @cfg_sect_creator.setter
    def cfg_sect_creator(self, new_val: CFGSectionCreator):
        self._cfg_sect_creator = new_val

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
            self, tabs_ctrl: object = None,
            su2_cfg_obj: SU2Config = SU2Config(),
            sections_list: ControlCheckBoxList = None,
            cfg_param_creator_butt_label: str = 'Add new section'):

        super(CreateSectButt, self).__init__(cfg_param_creator_butt_label)

        print('CreateSectButt su2_cfg_obj')
        print(su2_cfg_obj)

        # print('CreateSectButt tabs_ctrl')
        # print(tabs_ctrl)
        # input('CreateSectButt tabs_ctrl')

        self.su2_cfg_obj = su2_cfg_obj
        self.tabs_ctrl = tabs_ctrl
        self.sections_list = sections_list
        self.value = self._click
        self._set_cfg_sect_creator()

    def _set_cfg_sect_creator(self):
        self.cfg_sect_creator = \
            CFGSectionCreator(
                su2_cfg_obj=self.su2_cfg_obj, tabs_ctrl=self.tabs_ctrl,
                sections_list=self.sections_list)

    def _click(self):
        self.cfg_sect_creator.form.show()

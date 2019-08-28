import pyforms
from pyforms.controls import ControlButton
from pyforms.basewidget import BaseWidget

from su2_basic_widget import SU2BasicWidget
from su2_config_creator import SU2Config
from srfs_loader_ctrl import SurfLoaderCtrl


class SurfLoader(BaseWidget):

    @property
    def ctrl(self):
        return self._ctrl

    @ctrl.setter
    def ctrl(self, new_val):
        self._ctrl = new_val

    def __init__(
            self, su2_cfg_obj: SU2Config = SU2Config(),
            surf_loader_but_label: str = 'Load surfaces from su2 mesh',
            msh_prsng_params_pth: str = 'su2_msh_parsing_params.yaml'):
        super(SurfLoader, self).__init__('sample')

        self.ctrl = SurfLoaderCtrl(
            ctrld_w=self,
            su2_cfg_obj=su2_cfg_obj,
            surf_loader_but_label=surf_loader_but_label,
            msh_prsng_params_pth=msh_prsng_params_pth)

        # self._qq = ControlButton('sample')
        self.formset = ['_srf_load_butt']


if __name__ == '__main__':
    pyforms.start_app(SurfLoader)

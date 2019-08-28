from collections.abc import Iterable
import numpy as np
import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlDir, ControlFile,\
    ControlButton, ControlEmptyWidget, ControlMdiArea
from PyQt5.QtWidgets import QTabWidget, QWidget

from cfg_sections_selection_widget import CFGSectionSelWidget
from config_editor_widget import CFGEditorWidget
from file_operations_widget import FileOperationsWidget
from home_window_ctrl import SU2GUIHomeWindowCtrl
from su2_config_creator import SU2Config
# from su2_config import SU2Config


class SU2GUIHomeWindow(  # SU2Config,
                       BaseWidget):

    # @property
    # def sections_selection_widget(self) -> CFGSectionSelWidget:
    #     return self._sections_selection_widget
    #
    # @sections_selection_widget.setter
    # def sections_selection_widget(self, new_val: CFGSectionSelWidget):
    #     self._sections_selection_widget = new_val

    @property
    def su2_home_win_ctrl(self):
        return self._su2_home_win_ctrl

    @su2_home_win_ctrl.setter
    def su2_home_win_ctrl(self, new_val: SU2GUIHomeWindowCtrl):
        self._su2_home_win_ctrl = new_val

    def __init__(self):
        # SU2Config.__init__(
        #     self, path_to_cfg='parsed_cfgs/083708_10372018_su2_cfg.yaml')
        BaseWidget.__init__(
            self, title='Welcome to SU2 config GUI')
        # 'parsed_cfgs/083708_10372018_su2_cfg.yaml'
        su2_cfg = \
            SU2Config(path_to_cfg='parsed_cfgs/152721_22272019_su2_cfg.yaml')

        self.su2_home_win_ctrl = \
            SU2GUIHomeWindowCtrl(su2_home_win=self, su2_cfg=su2_cfg)


if __name__ == '__main__':
    pyforms.start_app(SU2GUIHomeWindow)

import pyforms
from PyQt5 import QtCore, QtGui, QtWidgets
from pyvalid import accepts, returns
import tkinter

from su2_basic_widget import SU2BasicWidget
from su2_config_creator import SU2Config
from vert_tabs_cfg_edit_ctrl import ProxyStyle, VerticalTabsWidgetCtrl


class VerticalTabsWidget(SU2BasicWidget):

    @property
    @returns(VerticalTabsWidgetCtrl)
    def vert_tab_w_ctrl(self) -> VerticalTabsWidgetCtrl:
        return self._vert_tab_w

    @vert_tab_w_ctrl.setter
    @accepts(object, VerticalTabsWidgetCtrl)
    def vert_tab_w_ctrl(self, new_val: VerticalTabsWidgetCtrl):
        self._vert_tab_w = new_val

    @accepts(
        object, SU2Config or None, int or None, int or None, int or None,
        int or None)
    def __init__(
            self, su2_cfg_obj: SU2Config = SU2Config(), initial_max_width=None,
            initial_max_height=None, initial_min_width=900,
            initial_min_height=None):
        super(VerticalTabsWidget, self).__init__(
            initial_max_width=initial_max_width,
            initial_max_height=initial_max_height,
            initial_min_width=initial_min_width,
            initial_min_height=initial_min_height)
        # QtWidgets.QApplication.setStyle(ProxyStyle())
        self.vert_tab_w_ctrl = \
            VerticalTabsWidgetCtrl(
                ctrld_vert_tab_w=self, su2_cfg_obj=su2_cfg_obj)


if __name__ == '__main__':
    pyforms.start_app(VerticalTabsWidget, geometry=(500, 500, 500, 500))

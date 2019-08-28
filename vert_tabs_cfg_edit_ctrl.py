from copy import deepcopy
from pprint import pprint
from pyforms.controls import ControlEmptyWidget, ControlButton
from PyQt5 import QtCore, QtGui, QtWidgets
from pyvalid import accepts, returns
import re

from single_tab_widget import SingleTabWidget
from su2_basic_widget import SU2BasicWidget
from su2_config_creator import SU2Config
from test_widget import TestWidget


class TabBar(QtWidgets.QTabBar):
    def tabSizeHint(self, index):
        s = QtWidgets.QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, opt)
            painter.restore()


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QtWidgets.QTabWidget.West)


class ProxyStyle(QtWidgets.QProxyStyle):
    def drawControl(self, element, opt, painter, widget):
        if element == QtWidgets.QStyle.CE_TabBarTabLabel:
            ic = self.pixelMetric(QtWidgets.QStyle.PM_TabBarIconSize)
            r = QtCore.QRect(opt.rect)
            w = 0 if opt.icon.isNull() \
                else opt.rect.width() + \
                self.pixelMetric(QtWidgets.QStyle.PM_TabBarIconSize)
            # r.setHeight(opt.fontMetrics.width(opt.text) + w)
            # r.moveBottom(opt.rect.bottom())
            # opt.rect = r
        QtWidgets.QProxyStyle.drawControl(self, element, opt, painter, widget)


class VerticalTabsWidgetCtrl:

    @property
    def su2_cfg_obj(self):
        return self._su2_cfg

    @su2_cfg_obj.setter
    @accepts(object, SU2Config)
    def su2_cfg_obj(self, new_val: SU2Config):
        self._su2_cfg = new_val

    # @property
    # @returns(dict)
    # def all_tabs(self):
    #     return self._all_tabs
    #
    # @all_tabs.setter
    # @accepts(object, dict)
    # def all_tabs(self, new_val: dict):
    #     self._all_tabs = deepcopy(new_val)

    # TODO change from object to SU2BaseWidget if the type checks out

    @property
    def vert_tab_w(self):
        return self._vert_tab_w

    @vert_tab_w.setter
    @accepts(object, object, SU2Config)
    def vert_tab_w(self, new_val):
        self._vert_tab_w = new_val

    @property
    @returns(TabWidget)
    def tabs_w(self):
        return self._tabs_w

    @tabs_w.setter
    @accepts(object, TabWidget)
    def tabs_w(self, new_val: TabWidget):
        self._tabs_w = new_val

    @property
    @returns(bool)
    def constr_called(self):
        return self._constr_called

    @constr_called.setter
    @accepts(object, bool)
    def constr_called(self, new_val: bool):
        self._constr_called = new_val

    def __init__(self, ctrld_vert_tab_w, su2_cfg_obj):
        """
        init w params

        Parameters
        ----------
        ctrld_vert_tab_w
        su2_cfg_obj
        """
        self.constr_called = False
        # self.tabs_w = None
        self.vert_tab_w = ctrld_vert_tab_w
        self.su2_cfg_obj = su2_cfg_obj
        self._init_all_tabs()
        self._set_tabs()

    def _init_all_tabs(self):
        """
        Instantiates all_tabs field
        Returns
        -------

        """
        self.all_tabs = []

    @accepts(object, str)
    def _get_tab_cont_for_section(self, section):
        tab_container = ControlEmptyWidget()
        tab_container.value = \
            SingleTabWidget(
                su2_cfg_obj=self.su2_cfg_obj, des_sect_name=section,
                tabs_ctrl=self)
        return tab_container

    def reset_desired_tab(self, des_section):
        new_tab_cont = self._get_sect_tab(des_section=des_section)

        if not self.tabs_w:
            print('The tab widget is empty!')
            return

        for curr_tab_idx in range(self.tabs_w.count()):
            curr_tab_sect_name = self.tabs_w.tabText(curr_tab_idx)
            fxd_tab_sect_name = \
                re.sub(
                    '\\s{1,}|\\n{1,}', '_', curr_tab_sect_name)

            # print(curr_tab_sect_name)
            if fxd_tab_sect_name == des_section:
                # print('Deleting {}'.format(curr_tab_sect_name))

                self.tabs_w.insertTab(
                    curr_tab_idx, new_tab_cont, curr_tab_sect_name)

                self.tabs_w.removeTab(curr_tab_idx + 1)

    def _get_sect_tab(self, des_section):
        """
        Generates single resizable tab using provided section input
        Parameters
        ----------
        des_section: str
            the name of the section for which the tab should be prepared

        Returns
        -------
        QScrollArea
            scroll area with desired tab content

        """
        print('des_section')
        print(des_section)
        curr_tab_cont = self._get_tab_cont_for_section(section=des_section)
        scrld_tab = QtWidgets.QScrollArea()
        scrld_tab.setWidget(curr_tab_cont)
        scrld_tab.setWidgetResizable(True)
        return scrld_tab

    def create_and_add_tab(self, section: str):
        scrld_tab = self._get_sect_tab(des_section=section)
        self.tabs_w.addTab(scrld_tab, section)
        pass

    @accepts(object)
    @returns(None)
    def _set_tabs(self):
        """
        Generates tabs for each section provided in config

        Returns
        -------
        None
            None

        """
        if self.constr_called:
            # self.vert_tab_w.layout.removeWidget(self.tabs_w)
            self.tabs_w.setParent(None)

        self.tabs_w = TabWidget()
        # self.tabs_w.setStyleSheet(
        #     """QTabBar::tab:disabaled {background: red;}""")
        self.tabs_w.setStyleSheet(
            'QTabBar::tab { font-size: 8pt; height: 230px; min-width: 40px;}')
        allowed_sections = self.su2_cfg_obj.init_cfg_sections_labels
        print('allowed_sections')
        print(allowed_sections)
        for section in allowed_sections:
            # TODO -> works but was replaced with _get_sect_tab() -> maybe
            #  delete
            # curr_tab_cont = self._get_tab_cont_for_section(section=section)
            # # QtWidgets.QCheckBox("section")
            # scrld_tab = QtWidgets.QScrollArea()
            # scrld_tab.setWidget(curr_tab_cont)
            # # tab1_layout = QtGui.QVBoxLayout(tab1.widget())
            # scrld_tab.setWidgetResizable(True)
            # # self.tabs_w.addTab(curr_tab_cont, section)
            # print('SECTION')
            # print(section)
            self.create_and_add_tab(section=section)
            # scrld_tab = self._get_sect_tab(des_section=section)
            # self.tabs_w.addTab(scrld_tab, section)
            # input('debug section')

        # add mesh plotting tab
        # self.tabs_w.addTab()

        if not self.constr_called:
            self.constr_called = True

        # self.tabs_w.setTabsClosable(True)

        self.vert_tab_w.layout().addWidget(self.tabs_w)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setStyle(ProxyStyle())
    w = TabWidget()
    w.addTab(QtWidgets.QWidget(), QtGui.QIcon("zoom.png"), "ABC")
    w.addTab(QtWidgets.QWidget(), QtGui.QIcon("zoom-in.png"), "ABCDEFGH")
    w.addTab(QtWidgets.QWidget(), QtGui.QIcon("zoom-out.png"), "XYZ")

    w.resize(640, 480)
    w.show()

    for tab_idx in range(0, w.count()):
        # pass
        des_w = w.tabText(tab_idx)
        print(des_w)

    sys.exit(app.exec_())

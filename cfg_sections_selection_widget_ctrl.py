from pyforms.controls import ControlCheckBoxList, ControlEmptyWidget
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5 import QtCore
from pyvalid import accepts, returns
# from cfg_sections_selection_widget import CFGSectionSelWidget

from cfg_section_creator_butt import CFGSectionCreatorButton
from su2_config_creator import SU2Config
from vert_tabs_cfg_edit import VerticalTabsWidget


class CFGSectionSelWidgetCtrl:
    """
    Contorller class for CFGSectionSelWidget
    """
    # controlled widget
    ctrld_widget = None
    # ctrld tabs
    ctrld_tabs_w = None
    # disabled icon
    disabled_icon = QIcon()
    # this is the list to be attached to this controller
    ctrld_list: ControlCheckBoxList or None = None
    # this is the colour map for this controller
    chkbx_col_map: dict = {}

    @property
    def su2_cfg_obj(self) -> SU2Config:
        return self._su2_cfg_obj

    @su2_cfg_obj.setter
    def su2_cfg_obj(self, new_val: SU2Config):
        self._su2_cfg_obj = new_val

    @property
    def sections_chckbox_list(self) -> ControlCheckBoxList:
        return self._sections_chckbox_list

    @sections_chckbox_list.setter
    def sections_chckbox_list(self, new_val: ControlCheckBoxList):
        self._sections_chckbox_list = new_val

    @property
    def sect_creat_btn(self) -> CFGSectionCreatorButton:
        return self._sect_creat_btn

    @sect_creat_btn.setter
    def sect_creat_btn(self, new_val: CFGSectionCreatorButton):
        self._sect_creat_btn = new_val

    @property
    def is_sections_list_set(self) -> bool:
        if not self._is_sections_list_set:
            raise \
                ValueError(
                    'Sections list has not been initialized up to this point'
                    ' and it should have been')
        return self._is_sections_list_set

    @is_sections_list_set.setter
    def is_sections_list_set(self, new_val: bool):
        self._is_sections_list_set = new_val

    # maybe should be done in a different way :(
    # @property
    # @returns(VerticalTabsWidget)
    # def ctrld_tabs_w(self) -> VerticalTabsWidget:
    #     return self._ctrld_tabs_w
    #
    # @ctrld_tabs_w.setter
    # @accepts(object, VerticalTabsWidget)
    # def ctrld_tabs_w(self, new_val: VerticalTabsWidget):
    #     self._ctrld_tabs_w = new_val

    def __init__(
            self, ctrld_widget, su2_cfg_obj: SU2Config,
            ctrld_tabs_w: VerticalTabsWidget = None):
        """
        Init with params
        Parameters
        ----------
        cfg_sect_sel_list: ControlCheckBoxList
            checkboxlist to be controlled via this class
        su2_cfg_obj: SU2Config
            SU2 configuration file object
        """

        self.su2_cfg_obj = su2_cfg_obj

        print('CFGSectionSelWidgetCtrl su2_cfg_obj')
        print(su2_cfg_obj)
        print(self.su2_cfg_obj)

        self.sections_chckbox_list = None
        self.is_sections_list_set = False
        CFGSectionSelWidgetCtrl.ctrld_widget = ctrld_widget
        CFGSectionSelWidgetCtrl._set_disabled_icon()

        if ctrld_tabs_w is not None:
            CFGSectionSelWidgetCtrl.ctrld_tabs_w = ctrld_tabs_w

        self.set_init_chckbx_list_vals()
        self.init_chkbx_col_map()
        CFGSectionSelWidgetCtrl.ctrld_widget.sections_chckbox_list\
            .changed_event = CFGSectionSelWidgetCtrl.dummy_changed_event
        self.set_different_bckgrnd_col()
        self._set_sect_creat_btn()
        self._set_ctrld_w_formset()

        # CFGSectionSelWidgetCtrl.ctrld_list.selection_changed_event = \
        #     CFGSectionSelWidgetCtrl.dummy_changed_event

    def _set_ctrld_w_formset(self):
        CFGSectionSelWidgetCtrl.ctrld_widget.formset = \
            [(' ', '_sect_creat_btn', ' '),
             (' ', '_sections_chckbox_list', ' ')]

    def _set_sect_creat_btn(self):
        # su2_cfg_obj: SU2Config = SU2Config(),
        #             tabs_ctrl

        tabs_ctrl = CFGSectionSelWidgetCtrl.ctrld_tabs_w.vert_tab_w_ctrl
        # print('CFGSectionSelWidgetCtrl tabs_ctrl')
        # print(tabs_ctrl)
        # input('CFGSectionSelWidgetCtrl tabs_ctrl')

        self.sect_creat_btn = \
            CFGSectionCreatorButton(
                su2_cfg_obj=self.su2_cfg_obj,
                tabs_ctrl=CFGSectionSelWidgetCtrl.ctrld_tabs_w.vert_tab_w_ctrl,
                sections_list=CFGSectionSelWidgetCtrl.ctrld_widget.sections_chckbox_list)

        btn_cont = ControlEmptyWidget()
        btn_cont.value = self.sect_creat_btn

        CFGSectionSelWidgetCtrl.ctrld_widget.sect_creat_btn = btn_cont
            # self.sect_creat_btn
        pass

    @staticmethod
    def _set_disabled_icon():
        CFGSectionSelWidgetCtrl.disabled_icon.addPixmap(
            QPixmap("icons/tab_disabled.png"), QIcon.Normal, QIcon.Off)

    def set_chkbx_col_map(self, new_chkbx_col_map: dict):
        """
        Setter for checkboxlist colour map
        Parameters
        ----------
        new_chkbx_col_map: dict
            dict containing new map for active/inactive state of the checkbox

        Returns
        -------

        """
        if not isinstance(new_chkbx_col_map, dict):
            raise TypeError('`chkbx_col_map` field should be of a dict type')
        if len(new_chkbx_col_map.keys()) != 2:
            raise ValueError(
                '`chkbx_col_map` should store two states (active/inactive')
        CFGSectionSelWidgetCtrl.chkbx_col_map = new_chkbx_col_map

    def set_init_chckbx_list_vals(self):
        """
        Creates sections selection checkbox list and populates the list with
        available sections

        Returns
        -------
        None
            None

        """

        if not self.su2_cfg_obj:
            raise ValueError(
                'please check value of su2_cfg_obj - it seems that it`s empty')
        available_sections = self.su2_cfg_obj.init_cfg_sections_labels
        self.sections_chckbox_list = \
            ControlCheckBoxList('Please select desired sections')
        # self._checkbox_list = ControlCheckBoxList('Sample chbx list')
        self.sections_chckbox_list.value = \
            ((el, True) for el in available_sections)
        CFGSectionSelWidgetCtrl.ctrld_widget.sections_chckbox_list = \
            self.sections_chckbox_list
        self.is_sections_list_set = True

    def _set_sections(self):
        available_sections = self.su2_cfg_obj.init_cfg_sections_labels
        self.sections_chckbox_list.value = \
            ((el, True) for el in available_sections)
        self.set_different_bckgrnd_col()
        # CFGSectionSelWidgetCtrl.ctrld_widget.sections_chckbox_list = \
        #     self.sections_chckbox_list

    def get_qt_col(self, r: int, g: int, b: int, alpha: int) -> QBrush:
        """
        Creates brush item for colour setting
        Parameters
        ----------
        r: int
            red colour val
        g: int
            green colour val
        b: int
            blue colour val
        alpha: int
            transarency val

        Returns
        -------
        QBrush
            QBrush item for colouring listWidgetItem

        """
        curr_col = QColor()

        curr_col.setRgb(r, g, b, alpha)

        curr_col_brush = QBrush(curr_col)
        return curr_col_brush

    def set_different_bckgrnd_col(self):
        """
        Sets different backgorunds to even/uneven listWidgetItems of controlled
        list
        Returns
        -------

        """
        for item_idx in range(0, len(CFGSectionSelWidgetCtrl.ctrld_widget
                                     .sections_chckbox_list.items)):
            # print(type(QtCore.Qt.red))

            if item_idx % 2 == 0:
                CFGSectionSelWidgetCtrl.ctrld_widget.sections_chckbox_list \
                    ._form.listWidget .item(item_idx) \
                    .setBackground(self.get_qt_col(155, 180, 160, 83))
            else:
                CFGSectionSelWidgetCtrl.ctrld_widget.sections_chckbox_list \
                    ._form.listWidget.item(item_idx) \
                    .setBackground(self.get_qt_col(155, 180, 160, 30))

    def init_chkbx_col_map(self):
        """
        Initializes checkbox colour map
        Returns
        -------

        """
        CFGSectionSelWidgetCtrl.chkbx_col_map = {
            0: QBrush(QtCore.Qt.darkGray),
            2: QBrush(QtCore.Qt.black)}

    @staticmethod
    @accepts(int)
    @returns(bool)
    def _get_bool_tab_state(pyforms_int_tab_state: int):
        """
        Getter for sedction state bool flag
        Parameters
        ----------
        pyforms_int_tab_state: int
            0 or 2, where 0 means False

        Returns
        -------
        bool
            T/F flag indicating if the tab with given sectino's param should
            be included in the config file

        """
        # is_enabled = True
        if pyforms_int_tab_state == 0:
            return False
        return True

    @staticmethod
    @accepts(int, bool)
    def _change_tab_state(tab_idx: int, is_enabled: bool):
        """
        Setter for tabs disabling
        Parameters
        ----------
        tab_idx: int
            index of a tab to be changed
        is_enabled: bool
            state of the tab to be set

        Returns
        -------

        """
        # print(CFGSectionSelWidgetCtrl.ctrld_tabs_w)
        print(type(CFGSectionSelWidgetCtrl.ctrld_tabs_w))
        if CFGSectionSelWidgetCtrl.ctrld_tabs_w is not None:
            CFGSectionSelWidgetCtrl.ctrld_tabs_w.vert_tab_w_ctrl.tabs_w.\
                setTabEnabled(tab_idx, is_enabled)

    @staticmethod
    def _change_tab_icon(tab_idx: int, is_enabled: bool):
        """
        Changes the icon to disabled icon if disabled state is detected
        Parameters
        ----------
        tab_idx: int
            tab index
        is_enabled: bool
            is the checked tab enabled

        Returns
        -------

        """

        if CFGSectionSelWidgetCtrl.ctrld_tabs_w is not None:
            final_icon = QIcon()
            if is_enabled is False:
                final_icon = CFGSectionSelWidgetCtrl.disabled_icon

            CFGSectionSelWidgetCtrl.ctrld_tabs_w.vert_tab_w_ctrl.tabs_w.\
                setTabIcon(tab_idx, final_icon)

    @staticmethod
    def dummy_changed_event():
        """
        Changes text color according to items' state
        Returns
        -------

        """
        all_chbxs_idxs = range(0, len(CFGSectionSelWidgetCtrl.ctrld_widget
                                      .sections_chckbox_list.items))
        print('changed selection')
        for list_item_idx in all_chbxs_idxs:
            # check state
            curr_item_state = CFGSectionSelWidgetCtrl.ctrld_widget \
                .sections_chckbox_list._form \
                .listWidget.item(list_item_idx).checkState()
            is_enabled = \
                CFGSectionSelWidgetCtrl._get_bool_tab_state(curr_item_state)
            CFGSectionSelWidgetCtrl._change_tab_state(
                tab_idx=list_item_idx, is_enabled=is_enabled)
            CFGSectionSelWidgetCtrl._change_tab_icon(
                tab_idx=list_item_idx, is_enabled=is_enabled)
            # if curr_item_state == 0:
            #     is_enabled = False
            # if CFGSectionSelWidgetCtrl.ctrld_tabs_w is not None:
            #     CFGSectionSelWidgetCtrl.ctrld_tabs_w.tabs_w.setTabEnabled(
            #         list_item_idx, is_enabled)
            print(curr_item_state)

            curr_item_col = \
                CFGSectionSelWidgetCtrl.chkbx_col_map[curr_item_state]

            CFGSectionSelWidgetCtrl.ctrld_widget.sections_chckbox_list._form \
                .listWidget.item(list_item_idx).setForeground(curr_item_col)

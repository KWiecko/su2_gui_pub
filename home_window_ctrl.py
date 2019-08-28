from collections.abc import Iterable
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlEmptyWidget
from pyvalid import accepts, returns

from config_editor_widget import CFGEditorWidget
from cfg_sections_selection_widget import CFGSectionSelWidget
from cfg_sections_selection_widget_ctrl import CFGSectionSelWidgetCtrl
from helpers.helpers import get_screen_res, safe_to_int
from file_operations_widget import FileOperationsWidget
# from home_window import SU2GUIHomeWindow
from su2_config_creator import SU2Config
# from su2_config import SU2Config
from vert_tabs_cfg_edit import VerticalTabsWidget


class SU2GUIHomeWindowCtrl:

    # @property
    # def sections_selection_widget(self) -> CFGSectionSelWidget:
    #     return self._sections_selection_widget
    #
    # @sections_selection_widget.setter
    # def sections_selection_widget(self, new_val: CFGSectionSelWidget):
    #     self._sections_selection_widget = new_val

    @property
    def su2_home_win(self) -> object:  # SU2GUIHomeWindow:
        return self._su2_home_win

    @su2_home_win.setter
    def su2_home_win(self, new_val):
        # if not isinstance(new_val):
        #     raise TypeError('Provided value is not of SU2GUIHomeWindow type')
        self._su2_home_win = new_val

    @property
    def cfg_edit_ctrl(self) -> CFGSectionSelWidgetCtrl:
        return self._cfg_edit_ctrl

    @cfg_edit_ctrl.setter
    def cfg_edit_ctrl(self, new_val: CFGSectionSelWidgetCtrl):
        self.cfg_edit_ctrl = new_val

    @property
    def su2_cfg(self):
        return self._su2_cfg

    @su2_cfg.setter
    def su2_cfg(self, new_val: SU2Config):
        self._su2_cfg = new_val

    @property
    @returns(str)
    def hcded_cfg_yaml_pth(self) -> str:
        return self._hcded_cfg_yaml_pth

    @hcded_cfg_yaml_pth.setter
    @accepts(object, str)
    def hcded_cfg_yaml_pth(self, new_val: str):
        print('Can`t set value to this field - it`s hardcoded')
        print('setting hcded value now!')
        self._hcded_cfg_yaml_pth = 'parsed_cfgs/152721_22272019_su2_cfg.yaml'

    def __init__(
            self, su2_home_win, su2_cfg: SU2Config = None,
            use_def_cfg_for_init: bool = False):
        # SU2Config.__init__(
        #     self, path_to_cfg='parsed_cfgs/083708_10372018_su2_cfg.yaml')
        # BaseWidget.__init__(
        #     self, title='Welcome to SU2 config GUI')

        self.su2_cfg = su2_cfg
        if use_def_cfg_for_init or not self.su2_cfg:
            self.init_su2_cfg()

        self.su2_home_win = su2_home_win

        # self._set_main_menu()

        # self.config_editor = self._get_cfg_edit_w()
        # self._config_editor_container = \
        #     self._get_container_for_widget(self.config_editor)

        # self.set_wdg_to_home_win(
        #     wdg_constr_wrp_name='_get_cfg_edit_w',
        #     su2_home_win_cont_name='_config_editor_container')

        # self.file_operator = self._get_file_operator()
        # self.sections_selection_widget = self._get_cfg_sections_sel_w()

        # multiple widget containers should be implemented here?
        # or should it be placed next ot editor container

        # self._file_operator_container = \
        #     self._get_container_for_widget(
        #         [self.file_operator, self.sections_selection_widget])

        self.set_wdg_to_home_win(
            wdg_constr_wrp_name='_get_cfg_edit_w',
            # ['_get_cfg_edit_w', '_get_file_operator'],
            su2_home_win_cont_name='_cfg_edit_container')

        self.set_wdg_to_home_win(wdg_constr_wrp_name='_get_vert_tab_w',
                                 su2_home_win_cont_name='_vert_tab_container')

        self.set_wdg_to_home_win(
            wdg_constr_wrp_name='_get_cfg_sections_sel_w',
            su2_home_win_cont_name='_sections_sel_container')

        self.set_wdg_to_home_win(
            wdg_constr_wrp_name='_get_file_operator',
            su2_home_win_cont_name='_file_operator_container')

        # self._sections_selector_container = \
        #     self._get_container_for_widget(self.sections_selection_widget)

        # setting layout
        self._set_formset()
        print('TEST FORMSET')
        print(self.su2_home_win.formset)
        # self.formset = [
        #     # (' ', 'h2:Loading options', ' ', '\n'),
        #     (' ', '_file_operator_container', ' ', '_config_editor_container', ' ')
        # (' ', '_file_operator_container', ' ', '_cfg_edit_container', ' '),
        # (' ','_vert_tab_container', ' ')
        # ]

        # print('\n tabs \n')
        # tab_widget = None
        # example_widget = QWidget()
        # for el in self.su2_home_win.config_editor.form._tabs:
        #     if isinstance(el, QTabWidget):
        #         tab_widget = el
        #         print(el)
        # tab_widget.addTab(example_widget, 'test_tab')
        #
        # print('tab count')
        # print(tab_widget.count())

        # for tab in tab_widget.:
        #     print(tab)

        # TODO: make logic which gets the greatest max width per container
        #  if more than one widget provided per container
        # TODO increase basic file operations/sections selection pane width

    def set_wdg_to_home_win(
            self, wdg_constr_wrp_name: str or Iterable,
            su2_home_win_cont_name: str):
        """
        Setter method for single or multiple widgets
        Sets one container per each call


        Parameters
        ----------
        wdg_constr_wrp_name: str or Iterable
            name(s) of constructor(s) wrapper(s) to call (they should be
            members of this class)
        su2_home_win_cont_name: str
            name for created container field in SU2 home window View object

        Returns
        -------
        None
            None

        """
        # get constructor wrapper from this class
        if isinstance(wdg_constr_wrp_name, Iterable) and \
                not isinstance(wdg_constr_wrp_name, str):
            constr_called = []
            for single_wgd_constr_wrp_name in wdg_constr_wrp_name:
                single_wrp = getattr(self, single_wgd_constr_wrp_name)
                single_wrp_inst = single_wrp()
                setattr(
                    self, single_wgd_constr_wrp_name.replace('_get', ''),
                    single_wrp_inst)
                constr_called.append(single_wrp_inst)
        elif isinstance(wdg_constr_wrp_name, str):
            wrp = getattr(self, wdg_constr_wrp_name)
            constr_called = wrp()
            setattr(
                self, wdg_constr_wrp_name.replace('_get', ''), constr_called)
        else:
            raise TypeError('Wrong type of provided wrapper name')
        curr_container = self._get_container_for_widget(constr_called)
        setattr(self.su2_home_win, su2_home_win_cont_name, curr_container)

    def set_file_operator_container(self):
        self.su2_home_win._file_operator_container = \
            self._get_container_for_widget(
                [self.file_operator, self.sections_selection_widget])

    def set_file_operator(self):
        self.file_operator = self._get_file_operator()
        self.sections_selection_widget = self._get_cfg_sections_sel_w()

    def _get_file_operator(self):
        """Getter for specific file operator"""
        # widget_geom = self._file_reader_geom
        # print(self._cfg_edit_w)
        # print(self._vert_tab_w)
        if not self._cfg_edit_w or not self._vert_tab_w \
                or not self._cfg_sections_sel_w:
            raise \
                ValueError(
                    '`self._cfg_edit_w` or `self._vert_tab_w` has no been init'
                    ' yet - please make sure cfg editor get init before '
                    'f_oper_widget')
        print('type(self._cfg_edit_w)')
        print(type(self._cfg_edit_w))
        # su2_cfg, trgt_cfg_editor: CFGEditorWidget
        return FileOperationsWidget(
            su2_cfg=self.su2_cfg, trgt_cfg_editor=self._cfg_edit_w,
            trgt_tabs_w=self._vert_tab_w,
            trgt_sect_sel_w=self._cfg_sections_sel_w)

    @returns(VerticalTabsWidget)
    def _get_vert_tab_w(self, width_decrement: int = 250) -> VerticalTabsWidget:
        """
        Getter  for vertical tabs widget
        width_decrement: int
            the number of pxls to reduce tabs width
        Returns
        -------
        VerticalTabsWidget
            VerticalTabsWidget with desired tabs

        """
        width, height = get_screen_res()
        alwd_width = width - width_decrement
        min_des_width = safe_to_int(val_to_cast=alwd_width * 0.9)

        if not self.su2_cfg:
            raise ValueError('SU2 cfg obejct can t be empty')
        return \
            VerticalTabsWidget(
                su2_cfg_obj=self.su2_cfg,
                # initial_max_height=height,
                initial_min_width=min_des_width,
                initial_max_width=alwd_width)

    def init_su2_cfg(self):
        """
        Initializes config from a default file

        Returns
        -------
        None
            None

        """
        # 'parsed_cfgs/083708_10372018_su2_cfg.yaml'

        self.su2_cfg = \
            SU2Config(path_to_cfg=self._hcded_cfg_yaml_pth)

    def _get_cfg_edit_w(self):
        return CFGEditorWidget(self.su2_cfg)

    def _get_cfg_sections_sel_w(self):
        """
        Private getter for sections selector
        Returns
        -------
        CFGSectionSelWidget
            section selection widget

        """

        if not self._vert_tab_w:
            vert_tab_w = None
        else:
            vert_tab_w = self._vert_tab_w

        return CFGSectionSelWidget(
            su2_cfg_obj=self.su2_cfg, ctrld_tabs_w=vert_tab_w)

    def _set_container_size(self, container, widget):
        # set widget's size
        # max width
        # print(widget.max_width)
        if widget.max_width is not None:
            container.setMaximumWidth(widget.max_width)
        # max height
        if widget.max_height is not None:
            container.setMaximumHeight(widget.max_height)
        # min width
        # print(widget.min_width)

        if widget.min_width is not None:
            # print(widget.min_width)
            container.setMinimumWidth(widget.min_width)
        # min height
        if widget.min_height is not None:
            container.setMinimumHeight(widget.min_height)

    def _get_container_for_widget(self, widget=None):
        """Getter for widget container"""
        container = \
            ControlEmptyWidget(label='Container label')
        if widget is not None:
            container.value = \
                widget

            if isinstance(widget, Iterable):
                sample_widget = widget[0]
                self._set_container_size(container, sample_widget)
            else:
                self._set_container_size(container, widget)

        return container

    @accepts(str)
    @returns(BaseWidget)
    def _get_w_frm_container(self, container_name: str) -> BaseWidget:
        """
        Gets widget from desired container using container field name

        Parameters
        ----------
        container_name: str
            name of container to fetch

        Returns
        -------
        BaseWidget
            the desired widget from provided container name

        """
        des_container = getattr(self, container_name)
        return des_container.value

    def _set_formset(self, formset_obj: list = []):
        if not formset_obj:
            # print('formset_obj')
            # print(formset_obj)
            self.su2_home_win.formset = [
                # (' ', 'h2:Loading options', ' ', '\n'),
                # (' ', '_file_operator_container', ' ', '_config_editor_container', ' ')
                (' ', '_file_operator_container', ' ', '_cfg_edit_container', ' '),
                (' ', '_sections_sel_container', ' ', '_vert_tab_container', ' ')
            ]
        else:
            self.su2_home_win.formset = formset_obj

    def _set_main_menu(self):
        self.su2_home_win.mainmenu = [
            {'Config operations': [
                {'Clear all settings': self._clear_all_fields},
                {'Restore defaults': self._reset_defautls},
                '-',
                {'Sample button': self._sample_button_action},
                # {'Save as': self.__saveAsEvent}
            ]
            },
            {'View': [
                {'Show/hide console': self._toogle_console},
                # {'Past': self.__pastEvent}
            ]
            }
        ]

    def _toogle_console(self):
        pass

    def _sample_button_action(self):
        print('sample button action')

    def _clear_all_fields(self):
        pass

    def _reset_defautls(self):
        pass


# if __name__ == '__main__':
#     pyforms.start_app(SU2GUIHomeWindow)

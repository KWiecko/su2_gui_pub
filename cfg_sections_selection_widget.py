import pyforms
from pyforms.controls import ControlCheckBoxList, ControlButton

from cfg_sections_selection_widget_ctrl import CFGSectionSelWidgetCtrl
from helpers.helper_classes import ParsedCFGReader
from su2_config_creator import SU2Config
from su2_basic_widget import SU2BasicWidget
from vert_tabs_cfg_edit import VerticalTabsWidget


class CFGSectionSelWidget(SU2BasicWidget):
    """
    Widget for su2 config's section selection for editing
    """

    @property
    def su2_cfg_obj(self) -> SU2Config:
        return self._su2_cfg_obj

    @su2_cfg_obj.setter
    def su2_cfg_obj(self, new_val: SU2Config):
        self._su2_cfg_obj = new_val

    # @property
    # def sections_buttons(self) -> tuple:
    #     return tuple(self._sections_buttons)
    #
    # @sections_buttons.setter
    # def sections_buttons(self, new_val: tuple):
    #     self._sections_buttons = list(new_val)

    # @property
    # def sections_buttons_field_names(self) -> tuple:
    #     return tuple(self._sections_buttons_field_names)
    #
    # @sections_buttons_field_names.setter
    # def sections_buttons_field_names(self, new_val: tuple):
    #     self._sections_buttons_field_names = list(new_val)

    @property
    def sections_chckbox_list(self) -> ControlCheckBoxList:
        return self._sections_chckbox_list

    @sections_chckbox_list.setter
    def sections_chckbox_list(self, new_val: ControlCheckBoxList):
        self._sections_chckbox_list = new_val

    @property
    def sect_creat_btn(self) -> ControlButton:
        return self._sect_creat_btn

    @sect_creat_btn.setter
    def sect_creat_btn(self, new_val: ControlButton):
        self._sect_creat_btn = new_val

    # @property
    # def is_sections_list_set(self) -> bool:
    #     if not self._is_sections_list_set:
    #         raise \
    #             ValueError(
    #                 'Sections list has not been initialized up to this point'
    #                 ' and it should have been')
    #     return self._is_sections_list_set
    #
    # @is_sections_list_set.setter
    # def is_sections_list_set(self, new_val: bool):
    #     self._is_sections_list_set = new_val

    def __init__(
            self, su2_cfg_obj: SU2Config = None,
            ctrld_tabs_w: VerticalTabsWidget = None, buttons_per_row: int = 4):
        super(CFGSectionSelWidget, self).__init__()
        """
        Init with params

        Parameters
        ----------
        su2_cfg_obj: SU2Config
            parsed config to be edited
        buttons_per_row: int
            number of buttons per row in the sections selection widget
        """
        print('init w params')
        if not su2_cfg_obj:
            pcr = ParsedCFGReader()
            su2_cfg = SU2Config(read_cfg_obj=pcr)
            su2_cfg_obj = su2_cfg
        self.su2_cfg_obj = su2_cfg_obj

        # print('CFGSectionSelWidget self.su2_cfg_obj')
        # print(su2_cfg_obj)
        # print(self.su2_cfg_obj)

        # self.is_sections_list_set = False
        # self.set_sections_chckbox_list()
        self.chkbx_list_ctrl = \
            CFGSectionSelWidgetCtrl(
                ctrld_widget=self, su2_cfg_obj=self.su2_cfg_obj,
                ctrld_tabs_w=ctrld_tabs_w)

    # def set_sections_chckbox_list(self):
    #     """
    #     Creates sections selection checkbox list and populates the list with
    #     available sections
    #
    #     Returns
    #     -------
    #     None
    #         None
    #
    #     """
    #
    #     if not self.su2_cfg_obj:
    #         raise ValueError(
    #             'please check value of su2_cfg_obj - it seems that it`s empty')
    #     available_sections = self.su2_cfg_obj.init_cfg_sections_labels
    #     self.sections_chckbox_list = \
    #         ControlCheckBoxList('Please select desired sections')
    #     # self._checkbox_list = ControlCheckBoxList('Sample chbx list')
    #     self.sections_chckbox_list.value = \
    #         ((el, True) for el in available_sections)


# class CFGSectionSelWidget(SU2BasicWidget):
#     """
#     Widget for su2 config's section selection for editing
#     """
#
#     @property
#     def su2_cfg_obj(self) -> SU2Config:
#         return self._su2_cfg_obj
#
#     @su2_cfg_obj.setter
#     def su2_cfg_obj(self, new_val: SU2Config):
#         self._su2_cfg_obj = new_val
#
#     @property
#     def sections_buttons(self) -> tuple:
#         return tuple(self._sections_buttons)
#
#     @sections_buttons.setter
#     def sections_buttons(self, new_val: tuple):
#         self._sections_buttons = list(new_val)
#
#     @property
#     def sections_buttons_field_names(self) -> tuple:
#         return tuple(self._sections_buttons_field_names)
#
#     @sections_buttons_field_names.setter
#     def sections_buttons_field_names(self, new_val: tuple):
#         self._sections_buttons_field_names = list(new_val)
#
#     @property
#     def buttons_per_row(self) -> int:
#         return self._buttons_per_row
#
#     @buttons_per_row.setter
#     def buttons_per_row(self, new_val: int):
#         self._buttons_per_row = new_val
#
#     def __init__(self, su2_cfg_obj: SU2Config = None, buttons_per_row: int = 1):
#         super(CFGSectionSelWidget, self).__init__()
#         """
#         Init with params
#
#         Parameters
#         ----------
#         su2_cfg_obj: SU2Config
#             parsed config to be edited
#         buttons_per_row: int
#             number of buttons per row in the sections selection widget
#         """
#         print('init w params')
#         pcr = ParsedCFGReader()
#         su2_cfg = SU2Config(read_cfg_obj=pcr)
#         su2_cfg_obj = su2_cfg
#         self.su2_cfg_obj = su2_cfg_obj
#         self.buttons_per_row = buttons_per_row
#
#         self.sections_buttons = ()
#         self.sections_buttons_field_names = \
#             ('_{}'.format(section_name.lower()) for section_name
#              in self.su2_cfg_obj.init_cfg_sections)
#         self.set_sections_buttons()
#         self.set_sections_buttons_fields()
#         self.set_buttons_formset()
#
#     def set_sections_buttons(self):
#         """
#         Sets buttons for each section found in init
#
#         Returns
#         -------
#
#         """
#         sections_buttons = []
#         # test_lab = 'test_lab'
#         desired_font = QFont()
#         desired_font.setPointSize(8)
#         for el in self.su2_cfg_obj.init_cfg_sections_labels:
#             curr_button = ControlButton(
#                 label=el,
#                 checkable=True)
#             curr_button.checked = True
#             curr_button._form.setFixedSize(300, 30)
#             curr_button._form.setFont(desired_font)
#             # curr_button._form.resize(100, 25)
#             sections_buttons.append(curr_button)
#         self.sections_buttons = tuple(sections_buttons)
#
#     def set_sections_buttons_fields(self):
#         """
#         Sets fields for each button created
#
#         Returns
#         -------
#
#         """
#         # print('test print')
#         for button_field_name, section_button in \
#                 zip(self.sections_buttons_field_names, self.sections_buttons):
#             print(button_field_name.lower())
#             setattr(self, button_field_name, section_button)
#
#     def set_buttons_formset(self):
#         rows_ratio = \
#             len(self.sections_buttons_field_names) / self.buttons_per_row
#         rows_count = ceil(rows_ratio)
#
#         all_buttons_fieldnames = deque(self.sections_buttons_field_names)
#
#         buttons_formset = []
#         max_row_idx = self.buttons_per_row - 1
#         print('setting formset')
#         for row in range(rows_count):
#             row_buttons = []
#             for row_idx in range(self.buttons_per_row):
#                 curr_butt_fieldname = None
#                 try:
#                     curr_butt_fieldname = all_buttons_fieldnames.popleft()
#                 except IndexError as iexc:
#                     print('No more buttons to extract')
#                 if not curr_butt_fieldname:
#                     break
#                 row_buttons.append(curr_butt_fieldname)
#                 if row_idx < max_row_idx:
#                     row_buttons.append('')
#             if not row_buttons:
#                 continue
#             buttons_formset.append(tuple(row_buttons))
#         self.formset = buttons_formset
#         # buttons_formset = [
#         #     ('_physical_problem_combo', '', '_units_combo', '', '_regime_type_combo'),
#         #     (' ', ' ', ' '),
#         #     (' ', ' ', ' '),
#         #     (' ', ' ', ' ')]
#         pass


if __name__ == '__main__':
    # pcr = ParsedCFGReader()
    # su2_cfg = SU2Config(read_cfg_obj=pcr)
    pyforms.start_app(CFGSectionSelWidget)

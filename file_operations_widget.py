from pyvalid import accepts, returns
from AnyQt.QtWidgets import QFileDialog
import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton, \
    ControlFilesTree, ControlLabel, ControlDir, \
    ControlTree, ControlFile, ControlBase

from cfg_sections_selection_widget import CFGSectionSelWidget
from config_editor_widget import CFGEditorWidget
from file_operations_widget_ctrl import FileOperationsWidgetCtrl
from su2_basic_widget import SU2BasicWidget
from vert_tabs_cfg_edit import VerticalTabsWidget


class FileOperationsWidget(SU2BasicWidget):

    @property
    def f_oper_w_ctrl(self):
        return self._f_oper_w_ctrl

    @accepts(FileOperationsWidgetCtrl)
    @f_oper_w_ctrl.setter
    def f_oper_w_ctrl(self, new_val: FileOperationsWidgetCtrl):
        self._f_oper_w_ctrl = new_val

    @property
    def trgt_cfg_editor(self):
        return self.trgt_cfg_editor

    @trgt_cfg_editor.setter
    @accepts(CFGEditorWidget)
    def trgt_cfg_editor(self, new_val: CFGEditorWidget):
        self._trgt_cfg_editor = new_val

    @property
    @returns(VerticalTabsWidget)
    def trgt_tabs_w(self):
        return self._trgt_tabs_w

    @trgt_tabs_w.setter
    @accepts(object, VerticalTabsWidget)
    def trgt_tabs_w(self, new_val: VerticalTabsWidget):
        self._trgt_tabs_w = new_val

    def __init__(
            self, su2_cfg, trgt_cfg_editor: CFGEditorWidget,
            trgt_tabs_w: VerticalTabsWidget,
            trgt_sect_sel_w: CFGSectionSelWidget):
        super(FileOperationsWidget, self).__init__(
            label='Placeholder for all of the file operations',
            initial_max_width=450)
        # self.su2_cfg = su2_cfg
        # self.su2_cfg_raw = None
        # self.trgt_cfg_editor = trgt_cfg_editor
        #
        # self._load_cfg_butt = ControlButton('Load selected config')
        #
        # self._reload_cfg_butt = \
        #     ControlButton('Reload selected config')
        # self._save_cfg_butt = ControlButton('Save config')

        # self._loader = self._get_file_operator('Load su2 config')
        # self._saver = \
        #     self._get_file_operator(
        #         'Save current su2 config', use_save_dialog=True)

        # trld_f_oper_w, su2_cfg, trgt_cfg_editor
        print(type(trgt_cfg_editor))
        self.f_oper_w_ctrl = \
            FileOperationsWidgetCtrl(
                ctrld_f_oper_w=self, su2_cfg=su2_cfg,
                trgt_cfg_editor=trgt_cfg_editor, trgt_tabs_w=trgt_tabs_w,
                trgt_sect_sel_w=trgt_sect_sel_w)

        self.formset = [
            (''),
            ('_loader'),
            ('_saver'),
            (' ', ' ', ' ')]

    # def _get_file_operator(self, button_desc, use_save_dialog=False):
    #     return \
    #         FileOperationButton(
    #             button_desc, use_save_dialog, self.su2_cfg, self.trgt_cfg_editor)


# class FileOperationButton(ControlButton):
#     def __init__(self, label, use_save_dialog, su2_config, su2_gui_home):
#         super(FileOperationButton, self).__init__(label)
#         self.use_save_dialog = use_save_dialog
#         self.su2_config = su2_config
#         self.su2_gui_home = su2_gui_home
#         self.value = self._file_oper_click
#
#     def _file_oper_click(self):
#         value = None
#         if self.use_save_dialog is True:
#             # QFileDialog.getSaveFileName returns (path, AllFiles(*))
#             value, _ = \
#                 QFileDialog.getSaveFileName(
#                     self.parent, self.label, self.value)
#         elif self.use_save_dialog is False:
#             # QFileDialog.getOpenFileName returns (path, AllFiles(*))
#             value, _ = \
#                 QFileDialog.getOpenFileName(
#                     self.parent, self.label, self.value)
#
#         else:
#             raise ValueError(
#                 """Unsupported value for 'use_save_dialog' parameter""")
#
#         value = str(value)
#
#         # print(value)
#         if self.use_save_dialog is True:
#             self.su2_config.save_path = value
#             self.su2_gui_home.config_editor.saved_config_path_label = \
#                 self.su2_config.save_path
#
#         if self.use_save_dialog is False:
#             self.su2_config.load_path = value
#             self.su2_gui_home.config_editor.loaded_config_path_label = \
#                 self.su2_config.load_path
#
#     def _unpack_load_path_value(self, temp_path_value):
#         return temp_path_value[0]


if __name__ == '__main__':
    pyforms.start_app(FileOperationsWidget, geometry=(200, 200, 200, 200))

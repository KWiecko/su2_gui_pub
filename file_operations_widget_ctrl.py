from AnyQt.QtWidgets import QFileDialog
from pyvalid import accepts, returns
from pyforms.controls import ControlButton

from cfg_sections_selection_widget import CFGSectionSelWidget
from config_editor_widget import CFGEditorWidget
from su2_config_reader import SU2CfgParser
from su2_cfg_saver import SU2ConfigSaver
from vert_tabs_cfg_edit import VerticalTabsWidget
# from config_editor_widget import CFGEditorWidget
# from file_operations_widget import FileOperationButton


class FileOperationsWidgetCtrl:

    @property
    def ctrld_f_oper_w(self):
        return self._ctrld_f_oper_w

    @ctrld_f_oper_w.setter
    def ctrld_f_oper_w(self, new_val):
        self._ctrld_f_oper_w = new_val

    @property
    def su2_cfg(self):
        return self._su2_cfg

    @su2_cfg.setter
    def su2_cfg(self, new_val):
        self._su2_cfg = new_val

    @property
    def trgt_cfg_editor(self):
        return self._trgt_cfg_editor

    @trgt_cfg_editor.setter
    @accepts(object, CFGEditorWidget)
    def trgt_cfg_editor(self, new_val: CFGEditorWidget):
        # print(type(trgt_cfg_editor))
        self._trgt_cfg_editor = new_val

    @property
    @returns(VerticalTabsWidget)
    def trgt_tabs_w(self):
        return self._trgt_tatbs_w

    @trgt_tabs_w.setter
    @accepts(object, VerticalTabsWidget)
    def trgt_tabs_w(self, new_val: VerticalTabsWidget):
        self._trgt_tatbs_w = new_val

    @property
    @returns(CFGSectionSelWidget)
    def trgt_sect_sel_w(self) -> CFGSectionSelWidget:
        return self._trgt_sect_sel_w

    @trgt_sect_sel_w.setter
    @accepts(object, CFGSectionSelWidget)
    def trgt_sect_sel_w(self, new_val: CFGSectionSelWidget):
        self._trgt_sect_sel_w = new_val

    def __init__(
            self, ctrld_f_oper_w, su2_cfg,
            trgt_cfg_editor: CFGEditorWidget,
            trgt_tabs_w: VerticalTabsWidget,
            trgt_sect_sel_w: CFGSectionSelWidget):

        self.ctrld_f_oper_w = ctrld_f_oper_w
        self.su2_cfg = su2_cfg
        # print(type(trgt_cfg_editor))
        self.trgt_cfg_editor = trgt_cfg_editor
        self.trgt_tabs_w = trgt_tabs_w
        self.trgt_sect_sel_w = trgt_sect_sel_w

        self.ctrld_f_oper_w._loader = self._get_file_operator('Load su2 config')
        self.ctrld_f_oper_w._saver = \
            self._get_file_operator(
                'Save current su2 config', use_save_dialog=True)

        self.formset = [
            (''),
            ('_loader'),
            ('_saver'),
            (' ', ' ', ' ')]

    # TODO change su2_gui_home to smth which will be seen by ctrl
    def _get_file_operator(self, button_desc, use_save_dialog=False):
        print('_get_file_operator')
        print(type(self.trgt_cfg_editor))
        return \
            FileOperationButton(
                button_desc, use_save_dialog, self.su2_cfg,
                self.trgt_cfg_editor, self.trgt_tabs_w, self.trgt_sect_sel_w)


class FileOperationButton(ControlButton):
    @property
    def trgt_cfg_editor(self):
        return self._trgt_cfg_editor

    @trgt_cfg_editor.setter
    @accepts(object, CFGEditorWidget)
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

    @property
    @returns(CFGSectionSelWidget)
    def trgt_sect_sel_w(self) -> CFGSectionSelWidget:
        return self._trgt_sect_sel_w

    @trgt_sect_sel_w.setter
    @accepts(object, CFGSectionSelWidget)
    def trgt_sect_sel_w(self, new_val: CFGSectionSelWidget):
        self._trgt_sect_sel_w = new_val

    def __init__(
            self, label, use_save_dialog, su2_config,
            trgt_cfg_editor: CFGEditorWidget,
            trgt_tabs_w: VerticalTabsWidget,
            trgt_sect_sel_w: CFGSectionSelWidget):
        super(FileOperationButton, self).__init__(label)
        self.use_save_dialog = use_save_dialog
        self.su2_config = su2_config
        self.trgt_cfg_editor = trgt_cfg_editor
        self.trgt_tabs_w = trgt_tabs_w
        self.trgt_sect_sel_w = trgt_sect_sel_w
        self.value = self._file_oper_click

    def _file_oper_click(self):
        value = None
        if self.use_save_dialog is True:
            # QFileDialog.getSaveFileName returns (path, AllFiles(*))
            value, _ = \
                QFileDialog.getSaveFileName(
                    self.parent, self.label, self.value)
        elif self.use_save_dialog is False:
            # QFileDialog.getOpenFileName returns (path, AllFiles(*))
            value, _ = \
                QFileDialog.getOpenFileName(
                    self.parent, self.label, self.value)

        else:
            raise ValueError(
                """Unsupported value for 'use_save_dialog' parameter""")

        value = str(value)

        # print(value)
        # TODO fix when no load file is provided
        if value:
            if self.use_save_dialog is True:
                self.su2_config.save_path = value
                self.trgt_cfg_editor.saved_config_path_label = \
                    self.su2_config.save_path
                saver = SU2ConfigSaver(
                    su2_cfg_obj=self.su2_config, vert_tabs_w=self.trgt_tabs_w)
                saver.write_cfg()

            if self.use_save_dialog is False:
                self.su2_config.load_path = value
                self._parse_cfg(tb_prsd_cfg_pth=value)
                self.su2_config.set_sections_labels()
                self.trgt_tabs_w.vert_tab_w_ctrl._set_tabs()
                self.trgt_sect_sel_w.chkbx_list_ctrl._set_sections()
                # tabs must be refreshed

                self.trgt_cfg_editor.loaded_config_path_label = \
                    self.su2_config.load_path

    @accepts(object, str)
    def _parse_cfg(self, tb_prsd_cfg_pth: str, cfg_chunk_sep='---'):
        cfg_reader = \
            SU2CfgParser(
                su2_cfg_path=tb_prsd_cfg_pth,
                cfg_chunk_sep=cfg_chunk_sep)
        # print(len(cfg_reader.row_by_row_cfg))
        cfg_reader.parse_cfg()
        cfg_reader.save_prsd_cfg()  # to_yaml=False)
        self.su2_config.parsed_su2_cfg = cfg_reader.yaml_rdy_cfg

    def _unpack_load_path_value(self, temp_path_value):
        return temp_path_value[0]

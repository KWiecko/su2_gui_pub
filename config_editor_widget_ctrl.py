from config_editor_widget import CFGEditorWidget
from cfg_sections_selection_widget import CFGSectionSelWidget


class ConfigEditorWidgetCtrl:
    """
    Controller class for config editor widget
    """
    cfg_editor_widget: CFGEditorWidget = None
    cfg_sections_selection_widget: CFGSectionSelWidget = None

    def __init__(
            self, prv_cfg_editor_widget: CFGEditorWidget,
            cfg_sections_selection_widget: CFGSectionSelWidget):
        ConfigEditorWidgetCtrl.cfg_editor_widget = prv_cfg_editor_widget
        ConfigEditorWidgetCtrl.cfg_sections_selection_widget = \
            cfg_sections_selection_widget
        # TODO implement setting and turning on and off tabs
        # for section_name in \
        #         ConfigEditorWidgetCtrl.cfg_sections_selection_widget\
        #                 .chkbx_list_ctrl:
        #     pass

    # print('\n tabs \n')
    # tab_widget = None
    # example_widget = QWidget()
    # for el in self.config_editor.form._tabs:
    #     if isinstance(el, QTabWidget):
    #         tab_widget = el
    #         print(el)
    # tab_widget.addTab(example_widget, 'test_tab')

    @staticmethod
    def add_tab(tab_name: str):
        ConfigEditorWidgetCtrl.cfg_editor_widget.form

    @staticmethod
    def rmv_tab(tab_name: str):
        pass

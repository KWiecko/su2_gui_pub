from copy import deepcopy
from collections import OrderedDict
from pyforms.controls import ControlLabel, ControlCombo
from PyQt5.QtWidgets import QWidget

from su2_basic_widget import SU2BasicWidget


class CFGEditorWidget(SU2BasicWidget):
    def __init__(self, su2_config):
        super(CFGEditorWidget, self).__init__(
            label='Placeholder for config settings operations',
            initial_min_width=900,
            initial_max_width=1000)
        # super(ConfigEditorWidget, self).__init__('Sample config editor')
        self.su2_config = su2_config

        self._loaded_config_path_label = ControlLabel(
            'Load path not specified yet')
        self._saved_config_path_label = ControlLabel(
            'Save path not specified yet')

        self._curr_case_label = ControlLabel(
            self.su2_config.current_case)

        self._set_combo_values()
        tab_dict = self._get_tabs()
        # print(self.physical_problem_values)

        self.formset = [
            ('Currently loaded config path: ', '_loaded_config_path_label', ' '),
            ('Currently loaded config path: ', '_saved_config_path_label', ' '),
            # tab_dict
            # {
            #     'Problem definition': self._get_problem_definition_formset(),
            #     'Gas Constants': []}
        ]
        # print('self.form.tabs')
        # print(self.form.tabs)
        # print(self.form.__dict__)
        # self.form._tabs = ['one', 'two']
        self.ex_wid_1 = QWidget()
        self.ex_wid_2 = QWidget()
        # self.form.addTab(self.ex_wid, 'one')
        self.form._tabs.append(self.ex_wid_1)
        self.form._tabs.append(self.ex_wid_2)
        # for key, val in self.form.__dict__.items():
        #     print(key, val)

    def _set_combo_values(self):
        print('SETTING VALS')

        self.physical_problem_values = (
            ('Euler', 'EULER'),
            ('Navier Stokes', 'NAVIER_STOKES'),
            ('Wave Equation', 'WAVE_EQUATION'),
            ('Heat Equation', 'HEAT_EQUATION'),
            ('FEM Elasticity', 'FEM_ELASTICITY'),
            ('Poisson Equation', 'POISSON_EQUATION')
        )

        self.units_values = (
            ('SI', 'SI'),
            ('US', 'US')
        )

        self.regime_type_values = (
            ('Compressible', 'COMPRESSIBLE'),
            ('Incompressible', 'INCOMPRESSIBLE')
        )

    def _get_problem_definition_formset(self):
        # self._physical_problem_combo = self._get_combo()
        self._physical_problem_combo = ControlCombo('Governing equations')
        self._populate_physical_problem_combo(self._physical_problem_combo)

        self._units_combo = ControlCombo('Units')
        self._populate_units_combo(self._units_combo)

        self._regime_type_combo = ControlCombo('Compressibility')
        self._populate_regime_type_combo(self._regime_type_combo)

        problem_def_formset = [
            ('_physical_problem_combo', '', '_units_combo', '', '_regime_type_combo'),
            (' ', ' ', ' '),
            (' ', ' ', ' '),
            (' ', ' ', ' ')]

        return problem_def_formset

    def _populate_combo(self, combo, values, action_event_changed):
        # setting (label, value) fields for combo
        for value_label, field_value in values:
            combo.add_item(value_label, field_value)

        # setting selection action for combo
        combo.changed_event = action_event_changed

    def _populate_physical_problem_combo(self, combo):
        self._populate_combo(
            combo, self.physical_problem_values, self._change_physical_problem)

    def _populate_units_combo(self, combo):
        self._populate_combo(combo, self.units_values, self._change_units)

    def _populate_regime_type_combo(self, combo):
        self._populate_combo(
            combo, self.regime_type_values, self._change_regime_type)
        # combo.changed_event = None

    def _get_tabs(self):

        tab_dict = {}
        tab_dict['Problem definition'] = \
            self._get_problem_definition_formset()
        tab_dict['Incompressible'] = [' ']
        tab_dict['Compressible'] = [' ']
        tab_dict['Gas constants'] = []

        return tab_dict

    @property
    def loaded_config_path_label(self):
        # getter for value of path label field
        return self._loaded_config_path_label.value

    @loaded_config_path_label.setter
    def loaded_config_path_label(self, new_loaded_config_path):
        # setter for value of loaded config path
        self._loaded_config_path_label.value = new_loaded_config_path

    @property
    def saved_config_path_label(self):
        # same convention as loaded_config_path_label
        return self._saved_config_path_label.value

    @saved_config_path_label.setter
    def saved_config_path_label(self, new_saved_config_path):
        # same convention as loaded_config_path_label setter
        self._saved_config_path_label.value = new_saved_config_path

    def _change_physical_problem(self):
        self.su2_config.physical_problem = self._physical_problem_combo.value
        # print(self.su2_config.physical_problem)

    def _change_units(self):
        self.su2_config.units = self._units_combo.value
        print(self.su2_config.units)

    def _change_regime_type(self):
        self.su2_config.regime_type = self._regime_type_combo.value
        formset_copy = deepcopy(self.formset)
        for item_label, item_value in self.regime_type_values:
            print('DEBUG PRINT')
            print(item_label)
            print(item_value)
            if item_value == self.su2_config.regime_type:
                print('if condition')
                self._show_hide_tab(formset_copy, item_label, value=[' '])
            else:
                print('else condition')
                self._show_hide_tab(formset_copy, item_label, value=None)
        self.formset = formset_copy

    def _show_hide_tab(self, formset_copy, key, value=None):
        print('SHT KEY VAR')
        print(key)

        for item in formset_copy:
            if isinstance(item, dict):
                print('Itetrating over tabs')
                print(item)
                temp_val = item.get(key, None)
                print('TEMP VAL')
                print(temp_val)
                if temp_val is None and value is not None:
                    item[key] = value
                elif temp_val is not None and value is None:
                    print('Deleting tab')
                    del item[key]
                else:
                    raise RuntimeError(
                        'Unsuppoerted oepration - please check the '
                        '_show_hide_tab definition')

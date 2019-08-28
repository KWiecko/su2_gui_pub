from pyforms.controls import ControlText, ControlEmptyWidget, ControlButton, \
    ControlBase
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QMessageBox

from helpers.helpers import replace_all_ws, get_pyqt_grpbox
from su2_config_creator import SU2Config


class ConfigParamCreatorCtrl:

    @property
    def param_name_ctrl(self) -> str:
        return self._param_name_ctrl

    @param_name_ctrl.setter
    def param_name_ctrl(self, new_val: str):
        self._param_name_ctrl = new_val

    @property
    def allwd_vals_ctrl(self) -> dict:
        return self._allwd_vals_ctrl

    @allwd_vals_ctrl.setter
    def allwd_vals_ctrl(self, new_val: dict):
        self._allwd_vals_ctrl = new_val

    @property
    def default_val_ctrl(self) -> str:
        return self._default_val_ctrl

    @default_val_ctrl.setter
    def default_val_ctrl(self, new_val: str):
        self._default_val_ctrl = new_val

    @property
    def tooltip_ctrl(self) -> str:
        return self._tooltip_ctrl

    @tooltip_ctrl.setter
    def tooltip_ctrl(self, new_val: str):
        self._tooltip_ctrl = new_val

    @property
    def ctrld_cfg_param_creator(self) -> object:
        return self._ctrld_cfg_param_creator

    @ctrld_cfg_param_creator.setter
    def ctrld_cfg_param_creator(self, new_val: object):
        self._ctrld_cfg_param_creator = new_val

    @property
    def new_param_name(self) -> str:
        return self._new_param_name

    @new_param_name.setter
    def new_param_name(self, new_val: str):
        self._new_param_name = new_val

    @property
    def allwd_vals(self) -> dict:
        return self._allwd_vals

    @allwd_vals.setter
    def allwd_vals(self, new_val: dict):
        self._allwd_vals = new_val

    @property
    def default_val(self) -> str:
        return self._default_val

    @default_val.setter
    def default_val(self, new_val: str):
        self._default_val = new_val

    @property
    def tooltip(self) -> str:
        return self._tooltip

    @tooltip.setter
    def tooltip(self, new_val: str):
        self._tooltip = new_val

    @property
    def su2_cfg_obj(self) -> SU2Config:
        return self._su2_cfg_obj

    @su2_cfg_obj.setter
    def su2_cfg_obj(self, new_val: SU2Config):
        self._su2_cfg_obj = new_val

    @property
    def curr_sect_name(self) -> str:
        return self._curr_sect_name

    @curr_sect_name.setter
    def curr_sect_name(self, new_val: str):
        self._curr_sect_name = new_val

    @property
    def tabs_ctrl(self) -> object:
        return self._tabs_ctrl

    @tabs_ctrl.setter
    def tabs_ctrl(self, new_val: object):
        self._tabs_ctrl = new_val

    def __init__(
            self, ctrld_cfg_f_creator: object, su2_cfg_obj: SU2Config,
            des_cfg_section: str, tabs_ctrl: object):
        """
        Init w params
        Parameters
        ----------
        ctrld_cfg_f_creator
        """
        # ConfigParamCreatorCtrl.ctrld_cfg_f_creator = ctrld_cfg_f_creator
        self.ctrld_cfg_param_creator = ctrld_cfg_f_creator
        # print(ConfigFieldCreatorCtrl.ctrld_cfg_f_creator)
        # ConfigParamCreatorCtrl.su2_cfg_obj = su2_cfg_obj
        self.su2_cfg_obj = su2_cfg_obj
        # ConfigParamCreatorCtrl.des_cfg_section = des_cfg_section
        self.des_cfg_section = des_cfg_section
        # ConfigParamCreatorCtrl.tabs_ctrl = tabs_ctrl
        self.tabs_ctrl = tabs_ctrl
        self._set_all_field_creator_ctrls()
        self._set_all_ctrls_to_w()
        self._set_desired_formset()

    def _check_and_set_null(
            self, attr_name: str, val_to_init_w: object = None):
        des_attr = getattr(ConfigParamCreatorCtrl, attr_name)
        if not des_attr:
            setattr(ConfigParamCreatorCtrl, attr_name, val_to_init_w)

    def _set_static_attrs(self):
        self._check_and_set_null('ctrld_cfg_f_creator')
        self._check_and_set_null('su2_cfg_obj', val_to_init_w={})
        # TODO this can't be static ;_;
        des_cfg_section = ''

        param_name_ctrl = None
        allwd_vals_ctrl = None
        default_val_ctrl = None
        tooltip_ctrl = None

    def _set_all_field_creator_ctrls(self):
        """
        Sets all required controls for adding ne parameter
        Returns
        -------

        """
        self.param_name_ctrl = ControlText()  # 'Name of desired field/cfg/variable')
        self.allwd_vals_ctrl = ControlText()  # 'Allowed options for created field')
        self.default_val_ctrl = ControlText()  # 'Default value of the created field')
        self.tooltip_ctrl = ControlText()  # 'Desired tooltip to be shown')

    def _set_desired_button(
            self, button_txt: str, button_action: callable,
            trgt_attr_name: str):
        """
        Setts desired button using provided button spec
        Parameters
        ----------
        button_txt: str
            text to be displayed over button
        button_action: callable
            action to execute when button is clicked
        trgt_attr_name: str
            the target attribute name of view

        Returns
        -------

        """
        # trgt_object = ConfigParamCreatorCtrl.ctrld_cfg_f_creator
        trgt_object = self.ctrld_cfg_param_creator
        curr_butt = ControlButton()
        curr_butt.label = button_txt
        curr_butt.value = button_action
        setattr(trgt_object, trgt_attr_name, curr_butt)

    def _set_all_ctrls_to_w(self):
        """
        Sets to ctrld object created necesary controls
        Returns
        -------

        """
        ctrls_l = \
            [('param_name_ctrl', 'Name of desired parameter', ControlText()),  # self.param_name_ctrl),
             ('allwd_vals_ctrl', 'Allowed options for created parameter', ControlText()),  # self.allwd_vals_ctrl),
             ('default_val_ctrl', 'Default value of the created parameter', ControlText()),  # self.default_val_ctrl),
             ('tooltip_ctrl', 'Desired tooltip to be shown', ControlText())]  # self.tooltip_ctrl)]

        appld_stylesheet = \
            'QGroupBox {' \
            'font-size: 16px;'\
            'font: Calibri;}'\
            'QGroupBox:title {'\
            'subcontrol-origin: margin;'\
            'subcontrol-position: top center;'\
            'padding-left: 10px;'\
            'padding-right: 10px;'\
            'padding-top: 12px; }'
        # print(appld_stylesheet)

        for ctrl_name, ctrl_desc, ctrl in ctrls_l:

            # curr_ctrl_groupbox = QGroupBox(ctrl_desc)
            # curr_ctrl_groupbox.setStyleSheet(appld_stylesheet)
            #
            # vert_layout = QVBoxLayout(curr_ctrl_groupbox)
            # first_grpbx_row = QHBoxLayout()
            # first_grpbx_row.addWidget(ctrl.form)
            #
            # vert_layout.addLayout(first_grpbx_row)
            #
            # curr_ctrl_cont = ControlEmptyWidget()
            #
            # curr_ctrl_cont.form.layout().addWidget(curr_ctrl_groupbox)  # curr_w

            # grpbox_desc: str, grpbox_stylesheet: dict,
            # main_grpbox_ctrl: ControlBase, return_container: bool = True

            curr_ctrl_cont = \
                get_pyqt_grpbox(
                    grpbox_desc=ctrl_desc, grpbox_stylesheet=appld_stylesheet,
                    main_grpbox_ctrl=ctrl)

            curr_ctrl_cont.form.setMinimumWidth(400)

            setattr(
                self.ctrld_cfg_param_creator,
                ctrl_name + '_grpbx',
                curr_ctrl_cont)

            # TODO maybe check if can be set inside controller
            setattr(
                self.ctrld_cfg_param_creator, ctrl_name, ctrl)

        self.ctrld_cfg_param_creator.set_param_button = \
            SetNewParamButton(
                su2_cfg_obj=self.su2_cfg_obj, cfg_param_creat_ctrl=self)

        self._set_desired_button(
            button_txt='Cancel',
            button_action=self.ctrld_cfg_param_creator.form.close,
            trgt_attr_name='cancel_button')

        # print(self.ctrld_cfg_f_creator.form.resize)
        self.ctrld_cfg_param_creator.form.setMaximumWidth(500)
        self.ctrld_cfg_param_creator.form.setMaximumHeight(700)
        self.ctrld_cfg_param_creator.geometry = (400, 500, 500, 700)
        # print(self.ctrld_cfg_f_creator.form.__dict__)
        # print(self.ctrld_cfg_f_creator.form.size)
        # self.ctrld_cfg_f_creator.form.maximized = False
        # print(self.ctrld_cfg_f_creator.form.isMaximized())

    def _set_desired_formset(self):
        """
        Sets formset to controlled config field creator
        Returns
        -------

        """
        # TODO maybe delete? no used right now
        self.ctrld_cfg_param_creator.formset = \
            [(' ', '_param_name_ctrl_grpbx', ' '),
             (' ', '_allwd_vals_ctrl_grpbx', ' '),
             (' ', '_default_val_ctrl_grpbx', ' '),
             (' ', '_tooltip_ctrl_grpbx', ' '),
             (' ', '_set_param_button', ' ', '_cancel_button', ' ')]


class SetNewParamButton(ControlButton):

    @property
    def su2_cfg_obj(self) -> SU2Config:
        return self._su2_cfg_obj

    @su2_cfg_obj.setter
    def su2_cfg_obj(self, new_val: SU2Config):
        self._su2_cfg_obj = new_val

    @property
    def cfg_param_creat_ctrl(self) -> ConfigParamCreatorCtrl:
        return self._cfg_param_creat_ctrl

    @cfg_param_creat_ctrl.setter
    def cfg_param_creat_ctrl(self, new_val: ConfigParamCreatorCtrl):
        self._cfg_param_creat_ctrl = new_val

    def __init__(
            self, su2_cfg_obj: SU2Config,
            cfg_param_creat_ctrl: ConfigParamCreatorCtrl,
            butt_label: str = 'Set parameter'):

        super(SetNewParamButton, self).__init__(label=butt_label)
        self.su2_cfg_obj = su2_cfg_obj

        # print('SetNewParamButton su2_cfg_obj')
        # print(su2_cfg_obj)

        self.cfg_param_creat_ctrl = cfg_param_creat_ctrl
        self.value = self.click

    def get_value_from_ctrl(
            self, prcsd_ctrl: ControlBase, is_list: bool = False,
            list_spltr: str = ',', rplc_all_ws: bool = False,
            ws_rplcmnt: str = '_'):
        """
        Returns the desired value of the privided control
        Parameters
        ----------
        prcsd_ctrl: ControlBase
            control from which value should be extracted
        is_list: bool
            flag - is provided value a list
        list_spltr: str
            a string to split a list by
        rplc_all_ws: bool
            should all whitespaces be replaced?
        ws_rplcmnt: str
            whitespace replacement

        Returns
        -------
        str or dict
            a string or dict extracted from the provided control

        """
        raw_ctrl_val = prcsd_ctrl.value

        # print('raw_ctrl_val')
        # print(prcsd_ctrl.__dict__)

        if not raw_ctrl_val:
            return None

        prcsd_ctrl_val = raw_ctrl_val.strip()

        if is_list:

            if list_spltr not in prcsd_ctrl_val:
                return prcsd_ctrl_val

            prcsd_ctrl_val_list = \
                [el.strip() for el in raw_ctrl_val.split(list_spltr)]
            prcsd_ctrl_val = {}
            for el in prcsd_ctrl_val_list:
                prcsd_ctrl_val[el] = el

        rtrnd_data = prcsd_ctrl_val
        if rplc_all_ws:
            rtrnd_data = replace_all_ws(prcsd_ctrl_val, ws_rplcmnt=ws_rplcmnt)

        return rtrnd_data

    def click(self):
        """
                Extracts desired values from the created controls

                Returns
                -------

                """
        # prcsd_ctrl: ControlBase, is_list: bool = False,
        # list_spltr: str = ','

        # extract values from controls
        raw_param_name = \
            self.get_value_from_ctrl(
                prcsd_ctrl=self.cfg_param_creat_ctrl.ctrld_cfg_param_creator
                .param_name_ctrl,
                rplc_all_ws=True)
        print('param name')
        # print(ConfigParamCreatorCtrl.param_name_ctrl)
        # print(type(ConfigParamCreatorCtrl.param_name_ctrl))
        print(
            self.cfg_param_creat_ctrl.ctrld_cfg_param_creator.param_name_ctrl.value)

        allwd_vals = \
            self.get_value_from_ctrl(
                prcsd_ctrl=self.cfg_param_creat_ctrl.ctrld_cfg_param_creator.allwd_vals_ctrl,
                is_list=True, list_spltr=',')
        default_val = self.get_value_from_ctrl(
            prcsd_ctrl=self.cfg_param_creat_ctrl.ctrld_cfg_param_creator.default_val_ctrl)
        # print(default_val)
        tooltip = self.get_value_from_ctrl(
            prcsd_ctrl=self.cfg_param_creat_ctrl.ctrld_cfg_param_creator.tooltip_ctrl)

        if not raw_param_name or not default_val:
            QMessageBox.about(
                self.cfg_param_creat_ctrl.ctrld_cfg_param_creator.form,
                'No name or default value!',
                'The name of created parameter and it`s default value must be '
                'provided')
            return

        param_name = raw_param_name.upper()

        # check if a proper section is present in the cfg dict
        if not self.cfg_param_creat_ctrl.des_cfg_section or \
                self.cfg_param_creat_ctrl.des_cfg_section not in \
                self.cfg_param_creat_ctrl.su2_cfg_obj.parsed_su2_cfg.keys():
            QMessageBox.about(
                self.cfg_param_creat_ctrl.ctrld_cfg_param_creator.form,
                'Malformed config!',
                'There is no section named {} in provided config file.'
                    .format(self.cfg_param_creat_ctrl.des_cfg_section))
            print(self.cfg_param_creat_ctrl.su2_cfg_obj.parsed_su2_cfg.keys())
            return

        #   KIND_INTERPOLATION:
        #     allowed values:
        #       ISOPARAMETRIC: ISOPARAMETRIC
        #       NEAREST_NEIGHBOR: NEAREST_NEIGHBOR
        #       SLIDING_MESH: SLIDING_MESH
        #     tooltip: Kind of interface interpolation among different zones (NEAREST_NEIGHBOR,
        #       ISOPARAMETRIC, SLIDING_MESH),
        #     value: NEAREST_NEIGHBOR

        param_dict = self.cfg_param_creat_ctrl.su2_cfg_obj.parsed_su2_cfg[
            self.cfg_param_creat_ctrl.des_cfg_section].get(param_name, None)

        if param_dict:
            QMessageBox.about(
                self.cfg_param_creat_ctrl.ctrld_cfg_param_creator.form,
                'Param already in config',
                'There already is a param named {} in provided config file.'
                    .format(param_name))
            return
        else:
            # print('allwd_vals')
            # print(allwd_vals)

            self.cfg_param_creat_ctrl.su2_cfg_obj.parsed_su2_cfg[
                self.cfg_param_creat_ctrl.des_cfg_section][param_name] = {
                'allowed values': allwd_vals,
                'tooltip': tooltip,
                'control_toogle': None,
                'control': None,
                'value': default_val}
            print(param_name)
            # print(self.cfg_param_creat_ctrl.tabs_ctrl)
            self.cfg_param_creat_ctrl.tabs_ctrl.reset_desired_tab(
                des_section=self.cfg_param_creat_ctrl.des_cfg_section)
            print({
                'allowed values': allwd_vals,
                'tooltip': tooltip,
                'control_toogle': None,
                'control': None,
                'value': default_val})
        self.cfg_param_creat_ctrl.ctrld_cfg_param_creator.form.close()

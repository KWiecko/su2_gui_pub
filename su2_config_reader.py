import argparse
from copy import deepcopy
from datetime import datetime
from numbers import Number
from pprint import pprint
from pyvalid import accepts, returns
import re


from helpers.helpers import read_lines_file, safe_to_int, safe_to_float,\
    _is_rgx_in_str, get_from_yaml, unpack_tuple_of_tuples, get_found_str, \
    save_to_yaml, check_and_make, all_keys_to_upper


class SU2CfgParser:
    """Class for config parsing before building proper GUI -
    for config version agnostic GUI"""

    def __init__(
            self,
            su2_cfg_path='config_template.cfg',
            cfg_chunk_sep='% \\-{3,}.*\\-{3,}%'):
        """
        Init with params


        Parameters
        ----------
        su2_cfg_path: str
            The path for the parsed config file
        """
        self._init_properties()
        self.su2_cfg_path = su2_cfg_path
        self.cfg_chunk_sep = cfg_chunk_sep

    def _init_properties(self):
        self._su2_cfg_path = None  # is that needed?
        self._su2_cfg_raw_chunks = dict()
        # to be removed?
        self._su2_chunked_cfg = dict()
        self._cfg_chunk_sep = None  # is that needed?
        self._row_by_row_cfg = list()
        self._chunk_sep_idxs = list()
        self._yaml_rdy_cfg = {}
        self.setting_oper_regex = '\s{0,1}=\s'
        self.comment_regex = '^%'

        self._yes_no_allowed_vals = \
            get_from_yaml('default_allowed_vals.yaml', 'yes_no')
        # (('YES', 'YES'), ('NO', 'NO'))

        self.yes_no_allowed_vals_rgx = \
            get_from_yaml('default_regexs.yaml', 'yes_no_allowed_vals',
                          return_plain_val=True)
        self.common_allowed_vals_rgx = \
            get_from_yaml('default_regexs.yaml', 'common_allowed_vals',
                          return_plain_val=True)
        self.bad_allowed_vals_rm_rgx = \
            get_from_yaml('default_regexs.yaml', 'bad_allowed_vals_rm_rgx',
                          return_plain_val=True)

        self.parenths_rgx = \
            get_from_yaml('default_regexs.yaml', 'parenths_rgx',
                          return_plain_val=True)

    @property
    def chunk_sep_idxs(self) -> list:
        return self._chunk_sep_idxs

    @chunk_sep_idxs.setter
    def chunk_sep_idxs(self, new_value: list):
        self._chunk_sep_idxs = new_value

    @property
    def su2_cfg_path(self) -> str:
        return self._su2_cfg_path

    @su2_cfg_path.setter
    def su2_cfg_path(self, new_value: str):
        self._su2_cfg_path = new_value

    @property
    def su2_cfg_raw_chunks(self) -> dict:
        return self._su2_cfg_raw_chunks

    @su2_cfg_raw_chunks.setter
    def su2_cfg_raw_chunks(self, new_value: dict):
        self._su2_cfg_raw_chunks = new_value

    @property
    def su2_chunked_cfg(self) -> dict:
        return self._su2_chunked_cfg

    @su2_chunked_cfg.setter
    def su2_chunked_cfg(self, new_value: dict):
        self._su2_chunked_cfg = new_value

    @property
    def cfg_chunk_sep(self) -> list:
        return self._cfg_chunk_sep

    @cfg_chunk_sep.setter
    def cfg_chunk_sep(self, new_value: list):
        self._cfg_chunk_sep = new_value

    @property
    def row_by_row_cfg(self) -> list:
        return self._row_by_row_cfg

    @row_by_row_cfg.setter
    def row_by_row_cfg(self, new_value: list):
        self._row_by_row_cfg = new_value

    @property
    def yes_no_allowed_vals(self) -> tuple:
        return self._yes_no_allowed_vals

    @yes_no_allowed_vals.setter
    def yes_no_allowed_vals(self, new_val: tuple):
        self._yes_no_allowed_vals = new_val

    @property
    def yes_no_allowed_vals_rgx(self) -> str:
        return self._yes_no_allowed_vals_rgx

    @yes_no_allowed_vals_rgx.setter
    def yes_no_allowed_vals_rgx(self, new_val: str):
        self._yes_no_allowed_vals_rgx = new_val

    @property
    def common_allowed_vals_rgx(self) -> str:
        return self._common_allowed_vals_rgx

    @common_allowed_vals_rgx.setter
    def common_allowed_vals_rgx(self, new_val: str):
        self._common_allowed_vals_rgx = new_val

    @property
    def bad_allowed_vals_rm_rgx(self) -> str:
        return self._bad_allowed_vals_rm_rgx

    @bad_allowed_vals_rm_rgx.setter
    def bad_allowed_vals_rm_rgx(self, new_val: str):
        self._bad_allowed_vals_rm_rgx = new_val

    @property
    def parenths_rgx(self) -> str:
        return self._parenths_rgx

    @parenths_rgx.setter
    def parenths_rgx(self, new_val: str):
        self._parenths_rgx = new_val

    @property
    @returns(dict)
    def yaml_rdy_cfg(self) -> dict:
        return self._yaml_rdy_cfg

    @yaml_rdy_cfg.setter
    @accepts(object, dict)
    def yaml_rdy_cfg(self, new_val: dict):
        self._yaml_rdy_cfg = deepcopy(new_val)

    @property
    @returns(str)
    def setting_oper_regex(self):
        return self._setting_oper_regex

    @setting_oper_regex.setter
    @accepts(object, str)
    def setting_oper_regex(self, new_val: str):
        self._setting_oper_regex = new_val

    @property
    @returns(str)
    def comment_regex(self):
        return self._comment_regex

    @comment_regex.setter
    @accepts(object, str)
    def comment_regex(self, new_val: str):
        self._comment_regex = new_val

    def get_final_val(self, user_provided_val, field_name: str):
        """
        General method for getting one of the two possible values - user
        provided or config defined

        Parameters
        ----------
        user_provided_val
            value provided by user as param
        field_name: str
            the name of corresponding field name

        Returns
        -------
        Depends on the field type
            Value provided by user or value stored in object (config defined)

        """
        if not user_provided_val:
            return getattr(self, field_name)
        return user_provided_val

    def append_su2_chunked_cfg(self, new_chunk, new_chunk_name):
        """
        Adding new values to config dict

        Parameters
        ----------
        new_chunk: str
            The new chunk to be parsed into GUI consumable stuff
        new_chunk_name: str
            The key for the new chunk in the su2_chunked_cfg dict

        Returns
        -------
        None
            None

        """
        if not self.su2_chunked_cfg.get(new_chunk_name, None):
            print('Adding new chunk to cfg dict - {}'.format(new_chunk_name))
        else:
            print(
                'Overwriting already existing chunk {}'.format(new_chunk_name))
        self.su2_chunked_cfg[new_chunk_name] = new_chunk

    def get_cfg_subset_start_idx(self, curr_sep_idx):
        """
        Getter methods for chunk subset start idx

        Parameters
        ----------
        curr_sep_idx: int
            Current separator idx in reaf lines file

        Returns
        -------
        int
            Int indicating chunk subset start

        """
        # separator is found under `curr_sep_idx` in row by row list
        # So in order to skip this row subset must start at +1 idx

        return curr_sep_idx + 1

    def get_cfg_subset_end_idx(self, curr_chunk_sep_list_idx):
        """
        Getter methods for chunk subset start idx

        Parameters
        ----------
        curr_chunk_sep_list_idx: int
            current separators idx in separators list so next separator could
            be used

        Returns
        -------
        int
           Int indicating chunk subset end

        """

        # subset neds just before next separator so we must find next
        # separator's position and -1 it

        curr_sep_idx = curr_chunk_sep_list_idx + 1
        print('curr_sep_idx')
        print(curr_sep_idx)

        if curr_sep_idx >= len(self.chunk_sep_idxs):
            print('EE')
            return None

        return self.chunk_sep_idxs[curr_chunk_sep_list_idx + 1] - 1

    def get_chunk_key(self, curr_sep_idx, key_extraction_regex='\w{1,}'):
        """
        Getter method for config chunk key extraction from separator row

        Parameters
        ----------
        curr_sep_idx: int
            The position of current separator in file

        Returns
        -------
        str
            key for chunk-by-chunk dict

        """
        chunk_key_components = \
            re.findall(key_extraction_regex, self.row_by_row_cfg[curr_sep_idx])
        return '_'.join(chunk_key_components)

    def generate_chunk(self):
        """
        Generates chunk by chunk based on separators and provided read_lines
        output

        Yields
        -------
        list
            List subset of the read lines file based on the current idxs

        """

        for chunk_sep_list_idx, chunk_sep_idx in enumerate(self.chunk_sep_idxs):

            # print('chunk_sep_list_idx')
            # print(chunk_sep_list_idx)

            subset_start = self.get_cfg_subset_start_idx(chunk_sep_idx)
            subset_end = self.get_cfg_subset_end_idx(chunk_sep_list_idx)

            # subset_end = self.chunk_sep_idxs[chunk_sep_list_idx + 1] - 1
            # extract chunk's dict key form separator
            desired_chunk_key = self.get_chunk_key(chunk_sep_idx)
            # print(desired_chunk_key)
            # print(subset_start)
            # print(subset_end)
            # print(len(self.row_by_row_cfg))
            # print(len(self.chunk_sep_idxs))

            # get desired chunk
            if not subset_end:
                desired_chunk = self.row_by_row_cfg[subset_start:]
            else:
                if subset_end <= subset_start:
                    raise ValueError('subset_end should be greater than start')
                desired_chunk = self.row_by_row_cfg[subset_start:subset_end]

            yield desired_chunk_key, desired_chunk
            # self.row_by_row_cfg[subset_start, subset_end]

    # def test_annotations(self, sample_arg: str='test') -> str:
    #     return '{}'.format(sample_arg)

    def get_raw_chunks(self):
        """
        Splits read cfg into chunks using indices of separators

        Returns
        -------

        """

        for chunk_key, chunk in self.generate_chunk():
            self.su2_cfg_raw_chunks[chunk_key] = chunk

    def extract_param(
            self, line_to_parse: str,
            setting_oper_regex: str = '\\s{0,1}=\\s',
            comment_regex: str = '^%') -> tuple or None:
        """
        Parses single line in search of the param indicator regex - if found
        extracts the param name and the default/assigned value
        
        Parameters
        ----------
        line_to_parse: str
            input line to be scanned for param regex
        setting_oper_regex: str
            regex to find setting operator inside parsed line
        comment_regex: str
            regex to determine if line is commented

        Returns
        -------
        tuple or None
            (param name, default/provided param value)

        """
        print('\n \n # # # # # # #')
        print('parsing param from line')
        print(line_to_parse)
        if re.search(comment_regex, line_to_parse):
            print('this is a commented line - skipping')
            return None

        raw_param_name = re.search(setting_oper_regex, line_to_parse)

        if not raw_param_name:
            print('No setter regex found')
            return None

        param_key = line_to_parse[:raw_param_name.start()]
        param_value_raw = \
            re.sub('[\n\t]$', '', line_to_parse[raw_param_name.end():])

        # conversion
        param_value = safe_to_float(param_value_raw)

        if not param_value:
            param_value = safe_to_int(param_value_raw)
        if not param_value:
            param_value = param_value_raw.strip()

        print(param_key, param_value)
        # print(
        # line_to_parse[:raw_param_name.start()],
        # line_to_parse[raw_param_name.end():])

        # return line_to_parse[:raw_param_name.start()], \
        #     line_to_parse[raw_param_name.end():]
        return param_key, param_value

    def _get_avail_opts_frm_cmmnt(
            self,
            param_def_value: str,
            raw_pre_param_comment: str,
            curr_chunk_name: str,
            yes_no_allowed_vals_rgx: str,
            common_allowed_vals_rgx: str):

        """
        Wrapper around param comment parsing procedure

        Parameters
        ----------
        param_def_value: str
            the param default value
        raw_pre_param_comment: str
            not parsed param comment
        curr_chunk_name: str
            name of currently parsed chunk
        yes_no_allowed_vals_rgx: str
            rgx used for yes/no allowed vals extraction
        common_allowed_vals_rgx: str
            rgx used for common allwd vals extarction

        Returns
        -------
        dict
            dict with allowed options

        """

        param_raw_allowed_vals = self.get_param_allowed_vals(
            param_def_value,
            raw_pre_param_comment=raw_pre_param_comment,
            curr_chunk_name=curr_chunk_name,
            yes_no_allowed_vals_rgx=yes_no_allowed_vals_rgx,
            common_allowed_vals_rgx=common_allowed_vals_rgx)

        print('param_raw_allowed_vals')
        print(param_raw_allowed_vals)

        allowed_vals_dict = {}
        if param_raw_allowed_vals is not None:
            for allowed_val_key, allowed_value in \
                    unpack_tuple_of_tuples(param_raw_allowed_vals):
                allowed_vals_dict[allowed_val_key] = allowed_value
        return deepcopy(allowed_vals_dict)

    def extract_chunk_params(
            self, input_chunk: list,
            raw_chunk_name: str,
            setting_oper_regex: str = '\\s{0,1}=\\s', comment_regex='^%',
            yes_no_allowed_vals_rgx: str = None,
            common_allowed_vals_rgx: str = None,
            bad_allowed_vals_rm_rgx: str = None) -> dict:
        """
        Finds rows in which the parameters are set and extracts the parameter
        name and default assigned value

        Parameters
        ----------
        input_chunk: list
            the list of rows in the parsed chunk
        setting_oper_regex: str
            Regex which will find the lines with setting operation in config
        raw_chunk_name: str
            the name of currently parsed chunk
        comment_regex: str
            the regex allowing to determine whether the row is commented line
            or not
        yes_no_allowed_vals_rgx: str
            rgx used for yes/on allowed values extraction
        common_allowed_vals_rgx: str
            rgx used for common allowed values extraction

        Yields
        -------
        tuple
            tuple which contains (param name, param info).
            param info contains:
                - ('value', `value of parameter read from config`),
                - ('allowed values', possible param values or None if no
                    `possible values` were found),
                - ('tooltip', param's tooltip)

        """

        print('parsing params')

        params = dict()
        for curr_line_idx, curr_line in enumerate(input_chunk):
            param_tuple = \
                self.extract_param(curr_line, setting_oper_regex, comment_regex)

            if not param_tuple:
                # print('skipping for tuple equals: {}'.format(param_tuple))
                continue
            else:
                # get the tooltip and the possible param values from the
                # curr_line_idx
                # print('COMMENT BELOW:')
                # print(self.get_pre_param_comment(
                #     param_line_idx=curr_line_idx, cfg_chunk=input_chunk))
                pre_param_comment = \
                    self.get_pre_param_comment(
                        param_line_idx=curr_line_idx, cfg_chunk=input_chunk)
                preprocessed_pre_param_comment = \
                    self.preprocess_pre_param_comment(pre_param_comment)
                print('PREPROCESSED COMMENT')
                print(preprocessed_pre_param_comment)
                param_name, param_def_value = param_tuple
                print('EXTRACTED OPTS')

                used_yes_no_allowed_vals_rgx = \
                    self.get_final_val(
                        user_provided_val=yes_no_allowed_vals_rgx,
                        field_name='yes_no_allowed_vals_rgx')
                used_common_allowed_vals_rgx = \
                    self.get_final_val(
                        user_provided_val=common_allowed_vals_rgx,
                        field_name='common_allowed_vals_rgx')
                used_bad_allowed_vals_rm_rgx = \
                    self.get_final_val(
                        user_provided_val=bad_allowed_vals_rm_rgx,
                        field_name='bad_allowed_vals_rm_rgx')
                print('used_common_allowed_vals_rgx')
                print(used_common_allowed_vals_rgx)
                # if not common_allowed_vals_rgx:
                #     used_common_allowed_vals_rgx = \
                #       self.common_allowed_vals_rgx

                # param_raw_allowed_vals = self.get_param_allowed_vals(
                #     param_def_value,
                #     raw_pre_param_comment=preprocessed_pre_param_comment,
                #     curr_chunk_name=raw_chunk_name,
                #     yes_no_allowed_vals_rgx=used_yes_no_allowed_vals_rgx,
                #     common_allowed_vals_rgx=used_common_allowed_vals_rgx)
                #
                # print('param_raw_allowed_vals')
                # print(param_raw_allowed_vals)
                #
                # allowed_vals_dict = {}
                # if param_raw_allowed_vals is not None:
                #     for allowed_val_key, allowed_value in \
                #             unpack_tuple_of_tuples(param_raw_allowed_vals):
                #         allowed_vals_dict[allowed_val_key] = allowed_value

                allowed_vals_dict = self._get_avail_opts_frm_cmmnt(
                    param_def_value=param_def_value,
                    raw_pre_param_comment=preprocessed_pre_param_comment,
                    curr_chunk_name=raw_chunk_name,
                    yes_no_allowed_vals_rgx=used_yes_no_allowed_vals_rgx,
                    common_allowed_vals_rgx=used_common_allowed_vals_rgx)

                param_tuple_w_opts = \
                    (('value', param_def_value),
                     ('allowed values', self.get_checked_allowed_vals(
                         param_def_value=param_def_value,
                         allowed_vals_dict=allowed_vals_dict,
                         pre_param_comment=preprocessed_pre_param_comment,
                         curr_chunk_name=raw_chunk_name,
                         yes_no_allowed_vals_rgx=used_yes_no_allowed_vals_rgx,
                         common_allowed_vals_rgx=used_common_allowed_vals_rgx,
                         bad_allowed_vals_rm_rgx=used_bad_allowed_vals_rm_rgx)),
                     ('tooltip', preprocessed_pre_param_comment))
                print('### param_tuple_w_opts ###')
                print(param_tuple_w_opts)
                yield param_name, param_tuple_w_opts

    def _get_fxd_def_val(self, def_val: str):
        """
        Replaces all whitespaces in provided default value with space.
        Then splits using ' ' char and gets frist element
        Created for problems with default values like
        'CENTRIPETAL CENTRIPETAL_AXIAL' have been found
        Parameters
        ----------
        def_val: str
            str containing default value

        Returns
        -------
        str
            first element of split default value

        """
        # replace whitespaces with single space
        def_val_s_ws = re.sub('\\s{1,}', ' ', def_val)
        defl_val_s_splt = def_val.split(' ')
        return defl_val_s_splt[0]

    def _has_def_val_parenthesis(
            self, chkd_def_val, parenths_rgx: str = '\\(.*\\)'):
        if re.search(parenths_rgx, str(chkd_def_val)):
            return True
        return False

    def get_checked_allowed_vals(
            self, param_def_value: str,
            allowed_vals_dict: dict,
            pre_param_comment: str,
            curr_chunk_name: str,
            yes_no_allowed_vals_rgx: str,
            common_allowed_vals_rgx: str,
            bad_allowed_vals_rm_rgx: str = '(\\(|\\s){}(\\)|\\s)') -> dict:

        """
        Final sanity check for extracted options - if the default value is
        not in the possible options then there was a mistake parsing allowed
        values

        Parameters
        ----------
        param_def_value: str
            default val of processed param's
        allowed_vals_dict: dict
            dict with allowed vals
        pre_param_comment:
            pre param comment either raw or preprocessed somehow
        curr_chunk_name: str
            name of currently processed chunk
        yes_no_allowed_vals_rgx: str
            rgx for yes/no allowed vals
        common_allowed_vals_rgx: str
            common allowed vals rgx
        bad_allowed_vals_rm_rgx: str
            bad finds removal rgx

        Returns
        -------
        dict
            deepcopy of found dict

        """

        if self._has_def_val_parenthesis(
                chkd_def_val=param_def_value, parenths_rgx=self.parenths_rgx):
            return {}

        print('default val')
        print(param_def_value)
        print('extracted_allowed_vals')
        pprint(allowed_vals_dict)
        allowed_vals_only = []
        for key, val in allowed_vals_dict.items():
            allowed_vals_only.append(val)

        if not allowed_vals_dict:
            return {}

        if param_def_value not in allowed_vals_only:
            # two cases
            # default value is ok
            # default value is wrorng i.e. CENTRIPETAL CENTRIPETAL_AXIAL

            if isinstance(param_def_value, Number):
                return {}

            if re.search('\\s', param_def_value.strip()):
                fxd_param_def_value = self._get_fxd_def_val(param_def_value)
                return self.get_checked_allowed_vals(
                    param_def_value=fxd_param_def_value,
                    allowed_vals_dict=allowed_vals_dict,
                    pre_param_comment=pre_param_comment,
                    curr_chunk_name=curr_chunk_name,
                    yes_no_allowed_vals_rgx=yes_no_allowed_vals_rgx,
                    common_allowed_vals_rgx=common_allowed_vals_rgx,
                    bad_allowed_vals_rm_rgx=bad_allowed_vals_rm_rgx)

            if not allowed_vals_only:  # or len(allowed_vals_only) == 1:
                return {}

            print('#### RECURRING ####')
            print('allowed_vals_only')
            print(allowed_vals_only)
            print(
                'param_def_val: {} not in allowed_vals'.format(param_def_value))
            # if some sort of params found recur to try and get true opts
            if len(allowed_vals_only) > 1:
                del_rgx = \
                    '|'.join(
                        [bad_allowed_vals_rm_rgx.format(el)
                         for el in allowed_vals_only])
            else:
                del_rgx = bad_allowed_vals_rm_rgx.format(allowed_vals_only[0])

            bad_finds_rm_frm_cmt = \
                re.sub(del_rgx, ' ', pre_param_comment)
            # for found_allwd_val in allowed_vals_only:
            #     bad_finds_rm_frm_allwd_vals = \
            #         bad_finds_rm_frm_allwd_vals.replace(found_allwd_val, '')
            ws_fxd_prcsd_pre_prm_cmnt = \
                re.sub('\\s{1,}', ' ', bad_finds_rm_frm_cmt)

            bad_finds_rmvd_allwd_vals_dict = self._get_avail_opts_frm_cmmnt(
                param_def_value=param_def_value,
                raw_pre_param_comment=ws_fxd_prcsd_pre_prm_cmnt,
                curr_chunk_name=curr_chunk_name,
                yes_no_allowed_vals_rgx=yes_no_allowed_vals_rgx,
                common_allowed_vals_rgx=common_allowed_vals_rgx)

            if not bad_finds_rmvd_allwd_vals_dict:
                return {}

            return self.get_checked_allowed_vals(
                param_def_value=param_def_value,
                allowed_vals_dict=bad_finds_rmvd_allwd_vals_dict,
                pre_param_comment=ws_fxd_prcsd_pre_prm_cmnt,
                curr_chunk_name=curr_chunk_name,
                yes_no_allowed_vals_rgx=yes_no_allowed_vals_rgx,
                common_allowed_vals_rgx=common_allowed_vals_rgx,
                bad_allowed_vals_rm_rgx=bad_allowed_vals_rm_rgx)

        else:
            return deepcopy(allowed_vals_dict)

    def preprocess_pre_param_comment(
            self,
            pre_param_comment: iter,
            comment_marker: str = '%') -> str or None:
        """
        Performs concat on provided list of strings

        Parameters
        ----------
        pre_param_comment: iter
            extracted comment to be concat
        comment_marker: str
            char used for marking commented lines in config

        Returns
        -------
        str or None
            concat string

        """
        if not pre_param_comment:
            return None
        joined_str = ''.join(pre_param_comment)
        nl_trimmed_str = re.sub(',{0,1}\\s{0,}\\n', ',', joined_str)
        ws_fixed_str = re.sub('\\s{1,}', ' ', nl_trimmed_str)
        comment_marker_trimmed_str = re.sub(comment_marker, '', ws_fixed_str)

        return comment_marker_trimmed_str.strip()

    def get_pre_param_comment(
            self, param_line_idx: int, cfg_chunk: list,
            pre_param_comment_stop_rgx: str = '^%\n') -> list:
        """
        Gets the lines which precede param definition from config so tooltip
        and/or possible options can be extracted

        Parameters
        ----------
        param_line_idx: int
            the index at which the parameter was found in the config
        cfg_chunk: list
            line by line parsed config's chunk
        pre_param_comment_stop_rgx: str
            regex which will stop the tooltip extraction (per param)

        Returns
        -------
        list
            line by line lines with tooltip and/or possible options for further
            parsing

        """
        # get pre param comment end
        last_comment_line_idx = param_line_idx - 1

        pre_param_comment = \
            [line_idx for line_idx, line
             in enumerate(cfg_chunk[:last_comment_line_idx])
             if re.search(pre_param_comment_stop_rgx, line)]

        print('cfg_chunk[last_comment_line_idx]')
        print(cfg_chunk[last_comment_line_idx])
        print(cfg_chunk[last_comment_line_idx - 1])
        # if not pre_param_comment:
        #     last_comment_line_idx -= 1

        # extracting closest separator
        print(pre_param_comment)
        try:
            first_comment_line_idx = pre_param_comment.pop() + 1
        except Exception as exc:
            print(
                'No {} before param comment found - assuming that comment '
                'starts in line after the section name'
                .format(pre_param_comment_stop_rgx))
            first_comment_line_idx = 1
        print(first_comment_line_idx)
        return cfg_chunk[first_comment_line_idx:param_line_idx]

    def get_param_tip(
            self,
            param_default_value: str,
            tip_start_marker: str,
            tip_stop_marker: str) -> str:
        """
        Gets tooltip (if one is given) for a given param line
        
        Parameters
        ----------
        param_default_value: str
            extracted default value of the parameter
        tip_start_marker: str
            regex matching the start of the tooltip text
        tip_stop_marker: str
            regex matching the end of the tooltip text

        Returns
        -------
        str
            tooltip text

        """
        
        pass

    def _is_yes_no_opts(
            self,
            search_target: str,
            yes_no_rgx: str = '(\\(|\\s)(YES|NO)(,\\s|\\/)(YES|NO)(\\)|\\s)')\
            -> bool:
        """
        Checks for YES/NO regex, returns bool flag

        Parameters
        ----------
        search_target: str
            str in which the regex will be checked
        yes_no_rgx: str
            regex which allows to check for YES/NO expression presence

        Returns
        -------
        bool
            Flag - was the YES/NO regex found in the parsed string

        """
        if _is_rgx_in_str(search_target, yes_no_rgx):
            # re.search(yes_no_rgx, search_target):
            return True
        return False

    def get_separators_idxs(self):
        """
        Gets idxs of separators

        Returns
        -------
        list
            the list of separators' indices

        """

        sep_idxs = \
            [sep_idx for sep_idx, sep_row in enumerate(self.row_by_row_cfg)
             if re.search(self.cfg_chunk_sep, sep_row)]

        if sep_idxs is None or len(sep_idxs) == 0:
            raise ValueError('There are no chunk separators found in cfg file.'
                             ' please check chunk separator regex')
        return sep_idxs

    def get_allowed_vals_tuple_from_str(
            self, allowed_vals_str: str, opts_splitter: str = ',') -> tuple:
        """
        Coverts the string to tuple of tuples with dict like structure
        ((allowed_val_gui_param, allowed_val_su2_param), ...)
        trims wihitespaces, converts spaces to '_' in allowed_val_gui_param so
        it can be used as variable name later

        Parameters
        ----------
        allowed_vals_str: str
            string storing all extracted allowed vals
        opts_splitter: str
            string indicating the splitter of allowed_vals string

        Yields
        -------
        tuple
            allowed_val_param_key, allowed_val
        """

        split_allowed_vals = \
            [el.strip() for el in allowed_vals_str.split(opts_splitter)]
        su2_gui_var_names = \
            [re.sub('\\s{1,}|\\-', '_', el) for el in split_allowed_vals]

        return tuple((allowed_val_param_key, allowed_val)
                     for allowed_val_param_key, allowed_val
                     in zip(su2_gui_var_names, split_allowed_vals))

        # for allowed_val_param_key, allowed_val \
        #         in zip(su2_gui_var_names, split_allowed_vals):
        #     yield allowed_val_param_key, allowed_val

    def _get_fixed_pre_param_cmnt(self, raw_pre_param_cmnt: str):
        """
        Getter for preprocessed param comment
        removes:
            - tabs
            - newlines
            - commas and dots from the end of param
        Parameters
        ----------
        raw_pre_param_cmnt: str
            input param to be preprocessed

        Returns
        -------
        str
            preprocessed param with faulty features removed

        """

        raw_pre_param_cmnt_no_t = raw_pre_param_cmnt.replace('\n', '')
        raw_pre_param_cmnt_no_n = raw_pre_param_cmnt_no_t.replace('\t', '')
        pre_param_comment = re.sub(',$|\\.$', '', raw_pre_param_cmnt_no_n)
        # raw_pre_param_cmnt_no_n.replace('', '')
        return pre_param_comment

    def get_param_allowed_vals(
            self,
            param_default_value: str,
            raw_pre_param_comment: str,
            curr_chunk_name: str,
            yes_no_allowed_vals_rgx: str =
            '(\\(|\\s)(YES|NO)(,\\s|\\/)(YES|NO)(\\)|\\s)',
            common_allowed_vals_rgx: str =
            '(\\(|\\s)(([A-Z]{1,})((\\_|\\-){0,1})([A-Z]{1,})'
            '(,\\s){0,1}){1,}(\\)|\\s)',
            # common_allowed_vals_rgx='(\(|\s)(((\_|\-){0,1}([A-Z]{1,})(\_|\-){0,1}){1,}(,\s){0,1}){1,}(\)|\s)',
            different_sections: tuple =
            (('OPTIMAL_SHAPE_DESIGN_DEFINITION', ''),)) -> tuple or None:
        """
        Gets available options (if they are given) for a given param line

        Parameters
        ----------
        param_default_value: str
            extracted default value of the parameter
        raw_pre_param_comment: str
            extracted comment preceding the parameter flattened to single
            string
        curr_chunk_name: str
            the extracted namae of currently processed chunk
        yes_no_allowed_vals_rgx: str
            rgx used for YES/NO allowed values extraction
        common_allowed_vals_rgx: str
            rgx for all other allowed vals extraction
        different_sections: tuple
            tuple-like dict storing special sections rgxs ina  way
            ((chunk name, chunk rgx), ..)

        Returns
        -------
        tuple or None
            tuple with possible options for a given parameter

        """
        is_param_string = False

        cast_defualt_val = safe_to_int(param_default_value)

        if not cast_defualt_val:
            cast_defualt_val = safe_to_float(param_default_value)

        if not cast_defualt_val:
            is_param_string = True

        if not is_param_string:
            return None

        # check trivial case - YES/No dict
        # raw_pre_param_cmnt_no_t = raw_pre_param_comment.replace('\n', '')
        # pre_param_comment = raw_pre_param_cmnt_no_t.replace('\t', '')

        pre_param_comment = \
            self._get_fixed_pre_param_cmnt(
                raw_pre_param_cmnt=raw_pre_param_comment)

        print('pre_param_comment')
        print(pre_param_comment)
        if self._is_yes_no_opts(
                pre_param_comment, yes_no_rgx=yes_no_allowed_vals_rgx):
            return self.yes_no_allowed_vals

        different_sections_info = {}
        for section_name, section_rgx in unpack_tuple_of_tuples(
                different_sections):
            different_sections_info[section_name] = section_rgx

        if curr_chunk_name in different_sections_info.keys():
            # parse chunk using special provided rgx
            return None
        else:
            print('common_allowed_vals_rgx')
            print(common_allowed_vals_rgx)
            print('pre_param_comment')
            print(pre_param_comment)
            opts_founds_occurances = \
                re.search(common_allowed_vals_rgx, pre_param_comment)
            print('opts_founds_occurances')
            print(opts_founds_occurances)

            if not opts_founds_occurances:
                return None
            found_string = \
                get_found_str(pre_param_comment, opts_founds_occurances)
            found_opts = self.get_allowed_vals_tuple_from_str(found_string)
            return found_opts

    def read_cfg_lines(self):
        """
        Reads line by line cfg
        Returns
        -------

        """
        self.row_by_row_cfg = read_lines_file(self.su2_cfg_path)

    def parse_cfg(self):
        """
        Parses chunk by chunk config under path provided in args.

        Returns
        -------
        None
            None

        """
        # read desired file
        self.row_by_row_cfg = read_lines_file(self.su2_cfg_path)
        print(len(self.row_by_row_cfg))

        # for line in self.row_by_row_cfg:
        #     print(line)

        # get chunks separators
        self.chunk_sep_idxs = self.get_separators_idxs()

        # get chunks
        self.get_raw_chunks()
        # self.chunks =

        for raw_chunk_key, raw_chunk in self.su2_cfg_raw_chunks.items():
            curr_chunk_dict = {}
            for param_name, param_tuple_w_opts in \
                    self.extract_chunk_params(
                        raw_chunk, raw_chunk_name=raw_chunk_key):
                curr_chunk_dict[param_name] = {}
                for param_info_key, param_info_val in param_tuple_w_opts:
                    curr_chunk_dict[param_name][param_info_key] = \
                        param_info_val

            self.su2_chunked_cfg[raw_chunk_key] = curr_chunk_dict
            # self.extract_chunk_params(raw_chunk)

    def save_prsd_cfg(
            self, dump_fname: str = '{}_su2_cfg.yaml',
            yaml_dump_dir: str = 'parsed_cfgs',
            upper_cfg_keys: bool = True, to_yaml: bool = True) -> None:
        """
        Dumps parsed structure to yaml file (parsing can be time consuming)

        Parameters
        ----------
        dump_fname: str
            name of config dumo file
        yaml_dump_dir: str
            name of config dump dir

        Returns
        -------
        None
            None

        """
        check_and_make(yaml_dump_dir)
        # getting prefix
        date_prefix = datetime.strftime(datetime.now(), '%H%M%S_%d%M%Y')
        final_fname = dump_fname.format(date_prefix)
        final_path = '{}/{}'.format(yaml_dump_dir, final_fname)

        if upper_cfg_keys:
            saved_dict = all_keys_to_upper(self.su2_chunked_cfg)
        else:
            saved_dict = deepcopy(self.su2_chunked_cfg)

        self.yaml_rdy_cfg = saved_dict

        if to_yaml:
            save_to_yaml(saved_dict=saved_dict, saved_fname=final_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--su2_cfg_path',
        default='config_template.cfg',
        help='path to su2 config file')

    parser.add_argument(
        '--cfg_chunk_sep',
        default='---',
        help='string indicating that the row is a config chunk separator'
             ' (regex not supportedd for now)')

    args = parser.parse_args()
    # print(args.su2_cfg_path)

    cfg_reader = \
        SU2CfgParser(
            su2_cfg_path=args.su2_cfg_path, cfg_chunk_sep=args.cfg_chunk_sep)
    # print(len(cfg_reader.row_by_row_cfg))
    cfg_reader.parse_cfg()
    cfg_reader.save_prsd_cfg()

    for chunk_title, chunk_params in cfg_reader.su2_chunked_cfg.items():
        print()
        print("CHUNK's TITLE")
        print(chunk_title)
        pprint(chunk_params)

    # for chunk_key, chunk in cfg_reader.su2_cfg_raw_chunks.items():
    #     print('\n\n Now printing the {} chunk \n'.format(chunk_key))
    #     # print(chunk_key)
    #     for line_num, line in enumerate(chunk):
    #         print('{} :: {}'.format(line_num, line))
    #         # print(len(chunk))

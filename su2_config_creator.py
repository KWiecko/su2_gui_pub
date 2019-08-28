from copy import deepcopy
from pyvalid import accepts, returns

from helpers.helper_classes import ParsedCFGReader


class SU2Config:
    """
    Automatic creator for SUConfig class
    """

    @property
    def parsed_su2_cfg(self) -> dict:
        return self._parsed_su2_cfg

    @parsed_su2_cfg.setter
    def parsed_su2_cfg(self, new_reader_obj: dict or ParsedCFGReader):
        """
        Sets new provided value to parsed_su2_cfg field
        Uses either provided dict or input from provided config reader class

        Parameters
        ----------
        new_reader_obj: dict or ParsedCFGReader
            object holding new data for parsed_su2_cfg field

        Returns
        -------

        """
        if isinstance(new_reader_obj, dict):
            if not new_reader_obj:
                raise ValueError('new_reader_obj dict is empty '
                                 '(parsed_su2_cfg setter)')
            # print('getting obj from dict')
            self._parsed_su2_cfg = new_reader_obj
        elif isinstance(new_reader_obj, ParsedCFGReader):
            if not ParsedCFGReader.from_yaml_cfg_dict:
                raise ValueError('new_reader_obj '
                                 '(ParsedCFGReader.from_yaml_cfg_dict) '
                                 'is an empty dict or None')
            # print('getting obj form reader')
            self._parsed_su2_cfg = new_reader_obj.from_yaml_cfg_dict
        else:
            raise ValueError(
                'Wrong type of `su2_obj_cfg` - need dict or ParsedCFGReader')

    @property
    def desired_su2_cfg(self) -> dict:
        return self._desired_su2_cfg

    @desired_su2_cfg.setter
    def desired_su2_cfg(self, new_val: dict):
        self._desired_su2_cfg = new_val

    @property
    def init_cfg_sections(self) -> tuple:
        return tuple(self._init_cfg_sections)

    @init_cfg_sections.setter
    def init_cfg_sections(self, new_val: tuple):
        self._init_cfg_sections = list(new_val)

    @property
    def desired_cfg_sections(self) -> tuple:
        return tuple(self._desired_cfg_sections)

    @desired_cfg_sections.setter
    def desired_cfg_sections(self, new_val: tuple):
        self._desired_cfg_sections = list(new_val)

    @property
    def init_cfg_sections_labels(self) -> tuple:
        return tuple(self._init_cfg_sections_proc)

    @init_cfg_sections_labels.setter
    def init_cfg_sections_labels(self, new_val: tuple):
        self._init_cfg_sections_proc = list(new_val)

    @property
    def load_path(self) -> str:
        return self._load_path

    @load_path.setter
    def load_path(self, new_load_path: str):
        self._load_path = new_load_path

    @property
    def save_path(self) -> str:
        return self._save_path

    @save_path.setter
    def save_path(self, new_save_path: str):
        self._save_path = new_save_path

    @property
    def path_to_cfg(self) -> str:
        return self._path_to_cfg

    @path_to_cfg.setter
    def path_to_cfg(self, new_val: str):
        self._path_to_cfg = new_val

    @property
    def current_case(self) -> str:
        return self._current_case

    @current_case.setter
    def current_case(self, new_val: str):
        self._current_case = new_val

    @property
    @returns(dict)
    def edited_cfg(self) -> dict:
        return self.edited_cfg

    @edited_cfg.setter
    @accepts(object, dict)
    def edited_cfg(self, new_val: dict):
        self._edited_cfg = new_val

    @property
    @returns(dict)
    def available_srfs(self) -> dict:
        return self._available_srfs

    @available_srfs.setter
    @accepts(object, dict)
    def available_srfs(self, new_val: dict):
        self._available_srfs = new_val

    @property
    @returns(dict)
    def taken_srfs(self) -> dict:
        return self._taken_srfs

    @taken_srfs.setter
    @accepts(object, dict)
    def taken_srfs(self, new_val: dict):
        self._taken_srfs = new_val

    def __init__(
            self,
            read_cfg_obj: dict or ParsedCFGReader = None,
            path_to_cfg: str = 'parsed_cfgs/152721_22272019_su2_cfg.yaml'):
        """
        Init with params

        Parameters
        ----------
        read_cfg_obj: ParsedCFGReader
            initiated cfg reader with already read cfg (or naa empty field)
        """
        self.path_to_cfg = path_to_cfg
        if not read_cfg_obj:
            self.parsed_su2_cfg = \
                ParsedCFGReader(path_to_yaml=self.path_to_cfg)
        else:
            self.parsed_su2_cfg = read_cfg_obj
        self.init_cfg_sections = tuple(self.parsed_su2_cfg.keys())
        # self.init_cfg_sections_labels = []
        self.set_sections_labels()
        # print(self.init_cfg_sections)
        self.desired_su2_cfg = {}
        self.desired_cfg_sections = []
        self.current_case = None
        self._set_edited_cfg()
        self.available_srfs = {}

    def _update_init_cfg_sections(self):
        """
        Updates sections with latest values
        Returns
        -------

        """
        self.init_cfg_sections = tuple(self.parsed_su2_cfg.keys())

    def _set_edited_cfg(self):
        """
        Setter for edited config field
        Returns
        -------
        None
            None

        """
        if not self.parsed_su2_cfg:
            raise ValueError('`parsed_su2_cfg` of su2_cfg_obj is empty')
        self.edited_cfg = deepcopy(self.parsed_su2_cfg)

    def set_desired_cfg(self):
        """
        Subsets desired sections to edit from parsed config

        Returns
        -------

        """
        if not self.desired_cfg_sections:
            self.desired_su2_cfg = deepcopy(self.parsed_su2_cfg)

        desired_cfg = {}
        for des_section_name in self.desired_cfg_sections:
            des_section = self.parsed_su2_cfg.get(des_section_name, None)
            if not des_section:
                continue
            desired_cfg[des_section_name] = des_section

    def set_sections_labels(
            self, in_name_separator: str = '_', single_line_max_len: int = 20):
        """
        Prepares seciton names for display (subsets `_` with ` `)

        Parameters
        ----------
        in_name_separator: str
            string which separates words in string
        single_line_max_len: int
            max line length of the given label (after that many signs line
            will be broken with \n)

        Returns
        -------
        None
            None

        """
        self._update_init_cfg_sections()
        strings_to_proc = self.init_cfg_sections
        if not strings_to_proc:
            raise ValueError('No initial sections names found')

        processed_strings = \
            (section_name.replace(in_name_separator, ' ').upper()
             for section_name in strings_to_proc)

        len_fixed_section_names = []
        for section_name in processed_strings:
            section_name_len = len(section_name)

            fixed_section_name = section_name

            if section_name_len >= single_line_max_len:
                print('string too long - fixing')
                split_section_name = section_name.split(' ')

                if len(split_section_name) == 1:
                    # fixed_section_name = section_name
                    # len_fixed_section_names.append(section_name)
                    continue

                from_break_cum_len = 0
                secion_name_newl_ad = split_section_name[0]
                for name_chunk in split_section_name[1:]:
                    from_break_cum_len += len(name_chunk)
                    if from_break_cum_len >= single_line_max_len:
                        chunk_sep = '\n'
                        from_break_cum_len = 0
                    else:
                        chunk_sep = ' '
                    secion_name_newl_ad += '{}{}'.format(chunk_sep, name_chunk)

                fixed_section_name = secion_name_newl_ad

            len_fixed_section_names.append(fixed_section_name)
        print(len_fixed_section_names)
        self.init_cfg_sections_labels = len_fixed_section_names


if __name__ == '__main__':
    # def_reader = ParsedCFGReader()
    su2_cfg_creat = SU2Config()  # read_cfg_obj=def_reader)

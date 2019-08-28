import yaml


class ButtonsCreator:
    """
    Class for parsing yaml with su2_config and creating all buttons based on
    that specification
    """

    @property
    def su2_config_dict(self) -> dict:
        return self._su2_config_dict

    @su2_config_dict.setter
    def su2_config_dict(self, new_val: dict):
        self._su2_config_dict = new_val

    @property
    def path_to_config_yaml(self) -> str:
        return self._path_to_config_yaml

    @path_to_config_yaml.setter
    def path_to_config_yaml(self, new_val: str):
        self._path_to_config_yaml = new_val

    @property
    def path_to_config_dir(self) -> str:
        return self._path_to_config_dir

    @path_to_config_dir.setter
    def path_to_config_dir(self, new_val: str):
        self._path_to_config_dir = new_val

    def __init__(
            self,
            path_to_config_dict: str='parsed_cfgs/083708_10372018_su2_cfg.yaml'):
        """
        Init with params

        Parameters
        ----------
        path_to_config_dict: :str
            string directing to parsed config yaml
        """
        self.path_to_config_dir = path_to_config_dict
        self.get_desired_cfg_dict()

    def get_desired_cfg_dict(self) -> None:
        """
        Reads parsed cfg from provided file

        Returns
        -------
        None
            None

        """

        with open(self.path_to_config_dir, 'r') as cfg_yaml_f:
            self.su2_config_dict = yaml.load(cfg_yaml_f)

    def get_proper_control(self, field_key: str, section_key: str):
        pass

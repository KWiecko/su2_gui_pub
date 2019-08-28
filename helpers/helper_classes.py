from abc import ABC, abstractclassmethod
from copy import deepcopy
import os
from pprint import pprint
import traceback
import yaml


class ParsedCFGReader:
    """
    Abstraction of a yaml operations based class

    """

    @property
    def parsed_cfg_path(self) -> str:
        return self._parsed_cfg_path

    @parsed_cfg_path.setter
    def parsed_cfg_path(self, new_val: str):
        self._parsed_cfg_path = new_val

    @property
    def from_yaml_cfg_dict(self) -> dict or None:
        return deepcopy(self._from_yaml_cfg_dict)

    @from_yaml_cfg_dict.setter
    def from_yaml_cfg_dict(self, new_val: dict):
        self._from_yaml_cfg_dict = deepcopy(new_val)

    def __init__(
            self,
            path_to_yaml: str = 'parsed_cfgs/083708_10372018_su2_cfg.yaml'):
        """
        Init with params

        Parameters
        ----------
        path_to_yaml: str
            path to parsed yaml
        """
        self.parsed_cfg_path = path_to_yaml
        self.get_cfg_from_yaml()

    def get_cfg_from_yaml(self):
        """
        Gets desired config and loads it from file

        Returns
        -------

        """
        try:
            with open(self.parsed_cfg_path, 'r') as cfg_yaml:
                self.from_yaml_cfg_dict = yaml.load(cfg_yaml)
        except Exception as exc:
            print(exc)
            traceback.print_exc()
            self.from_yaml_cfg_dict = {}


class InletStaticMachCalc:

    @property
    def input_p0(self) -> float:
        return self._input_p0

    @input_p0.setter
    def input_p0(self, new_val: float):
        self._input_p0 = new_val

    @property
    def input_ma0(self) -> float:
        return self._input_ma0

    @input_ma0.setter
    def input_ma0(self, new_val: float):
        self._input_ma0 = new_val

    @property
    def input_t0(self) -> float:
        return self._input_t0

    @input_t0.setter
    def input_t0(self, new_val: float):
        self._input_t0 = new_val

    @property
    def kappa(self) -> float:
        return self._kappa

    @kappa.setter
    def kappa(self, new_val: float):
        self._kappa = new_val

    @property
    def input_mass_flow(self) -> float:
        return self._input_mass_flow

    @input_mass_flow.setter
    def input_mass_flow(self, new_val: float):
        self._input_mass_flow = new_val

    @property
    def gas_const(self) -> float:
        return self._gas_const

    @gas_const.setter
    def gas_const(self, new_val: float):
        self._gas_const = new_val

    @property
    def ma_allwd_err(self) -> float:
        return self._ma_allwd_err

    @ma_allwd_err.setter
    def ma_allwd_err(self, new_val: float):
        self._ma_allwd_err = new_val

    @property
    def area_allwd_err(self) -> float:
        return self._area_allwd_err

    @area_allwd_err.setter
    def area_allwd_err(self, new_val: float):
        self._area_allwd_err = new_val

    @property
    def area_station1(self) -> float:
        return self._area_station1

    @area_station1.setter
    def area_station1(self, new_val: float):
        self._area_station1 = new_val

    @property
    def area_station2(self) -> float:
        return self._area_station2

    @area_station2.setter
    def area_station2(self, new_val: float):
        self._area_station2 = new_val

    @property
    def ma_station1(self) -> float:
        return self._ma_station1

    @ma_station1.setter
    def ma_station1(self, new_val: float):
        self._ma_station1 = new_val

    @property
    def ma_station2(self) -> float:
        return self._ma_station2

    @ma_station2.setter
    def ma_station2(self, new_val: float):
        self._ma_station2 = new_val

    @property
    def mass_flow_allwd_err(self) -> float:
        return self._mass_flow_allwd_err

    @mass_flow_allwd_err.setter
    def mass_flow_allwd_err(self, new_val: float):
        self._mass_flow_allwd_err = new_val
    #
    # @property
    # def dma(self) -> float:

    def __init__(
            self,
            input_p0: float,
            input_ma0: float,
            input_t0: float,
            input_mass_flow: float,
            area_station1: float = None,
            area_station2: float = None,
            kappa: float = 1.4,
            gas_const: float = 287.06,
            mass_flow_allwd_err: float = 0.01):
        """
        Init w params
        Parameters
        ----------
        input_p0: float
        input_ma0: float
        input_t0: float
        input_mass_flow: float
        area_station1: float
        area_station2: float
        kappa: float
        gas_const: float
        ma_allwd_err: float
        """

        self.input_p0 = input_p0
        self.input_ma0 = input_ma0
        self.input_t0 = input_t0
        self.input_mass_flow = input_mass_flow
        self.area_station1 = area_station1
        self.area_station2 = area_station2
        self.kappa = kappa
        self.gas_const = gas_const
        self.mass_flow_allwd_err = mass_flow_allwd_err

    def get_m1(self):
        """
        getter for M1 mach number (at the lip of the inlet)
        Returns
        -------
        float
            Mach number at station 1 (lip of the inlet)

        """

        pass

    def get_m2(self):
        """
        getter for M2 mach number (at the lip of the inlet)
        Returns
        -------
        float
            Mach number at station 2 (lip of the inlet)

        """
        pass

    def solve_for_ma(self, station_idx: int = 2):

        # curr_inlet_area = None
        calc_ma_attr_name = ''

        if station_idx == 1:
            curr_inlet_area = self.area_station1
            calc_ma_attr_name = 'ma_station1'
        elif station_idx == 2:
            curr_inlet_area = self.area_station2
            calc_ma_attr_name = 'ma_station2'
        else:
            raise ValueError(
                'Wrong station idx provided: {}'.format(station_idx))

        if not curr_inlet_area:
            raise ValueError('`curr_inlet_area` must not be None')

        right_hand_mass_flow = 0
        curr_ma = self.input_ma0
        dma = 0.001 * self.input_ma0
        print(dma)

        while abs(self.input_mass_flow - right_hand_mass_flow) > \
                self.mass_flow_allwd_err:

            right_hand_mass_flow = \
                self._get_right_hand_side(
                    curr_inlet_area=curr_inlet_area, curr_ma=curr_ma)
            print('des. mdot:  {}, curr. mdot: {}, curr. Ma: {}'
                  .format(self.input_mass_flow, right_hand_mass_flow, curr_ma))
            # input(' debug ')
            if right_hand_mass_flow > self.input_mass_flow:
                curr_ma -= dma
            elif right_hand_mass_flow < self.input_mass_flow:
                curr_ma += dma
            else:
                break
        setattr(self, calc_ma_attr_name, curr_ma)

    def _get_right_hand_side(self, curr_inlet_area: float, curr_ma: float):
        """
        calculates tight hand sided of the equation for A/Ma
        Returns
        -------
        float
            result of the right hand eq

        """
        velo_bit = \
            self.input_p0 * curr_inlet_area * curr_ma / \
            (self.gas_const * self.input_t0 / self.kappa) ** 0.5
        total_temp_ratio = 1 + (self.kappa - 1) / 2 * curr_ma ** 2
        exponent = -1 / 2 * (self.kappa + 1) / (self.kappa - 1)
        res = velo_bit * total_temp_ratio ** exponent
        return res


if __name__ == '__main__':

    ismc = InletStaticMachCalc(
        input_p0=1e5,
        input_ma0=0.8,
        input_t0=288.15,
        input_mass_flow=0.4,
        area_station1=0.0036,
        area_station2=0.006345,
        kappa=1.4,
        gas_const=287.06,
        mass_flow_allwd_err=0.001)
    # pcr = ParsedCFGReader()
    # print(os.getcwd())
    # print(os.listdir('parsed_cfgs'))
    # print(pcr.parsed_cfg_path)
    ismc.solve_for_ma(station_idx=1)
    print(ismc.ma_station1)

    # pprint(pcr.from_yaml_cfg_dict)

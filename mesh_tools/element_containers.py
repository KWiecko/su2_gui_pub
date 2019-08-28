from abc import ABC, abstractmethod
from collections import namedtuple
from copy import deepcopy

import numpy as np
from helpers.helpers import safe_to_int


class BasicElement(ABC):
    pass


class BasicElementContainer(ABC):
    """
    Blueprint class for any element container of any type
    """

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_val: str):
        self._name = new_val

    @property
    def element_count(self) -> int:
        return self._element_count

    @element_count.setter
    def element_count(self, new_val: int):
        self._element_count = new_val

    @property
    def elements(self) -> list:
        return self._elements

    @elements.setter
    def elements(self, new_val: list):
        self._elements = new_val.copy()

    @property
    def all_msh_elements(self) -> dict:
        return self._all_msh_elements

    @all_msh_elements.setter
    def all_msh_elements(self, new_val: dict):
        self._all_msh_elements = new_val

    def __init__(
            self, name: str, element_count: int, elements: list,
            all_msh_elements: dict):

        self.name = name
        self.element_count = element_count
        self.elements = elements
        self.all_msh_elements = all_msh_elements


class BasicMeshContainer(ABC):
    @property
    def all_msh_elements(self) -> dict:
        return self._all_msh_elements

    @all_msh_elements.setter
    def all_msh_elements(self, new_val: dict):
        self._all_msh_elements = new_val

    @property
    def all_msh_elements_np(self) -> namedtuple:
        return self._all_msh_elements_np

    @all_msh_elements_np.setter
    def all_msh_elements_np(self, new_val: namedtuple):
        self._all_msh_elements_np = new_val

    @property
    def all_boundaries(self) -> dict:
        return self._all_boundaries

    @all_boundaries.setter
    def all_boundaries(self, new_val: dict):
        self._all_boundaries = new_val  # deepcopy(new_val)

    @property
    def all_boundaries_np(self) -> namedtuple:
        return self._all_boundaries_np

    @all_boundaries_np.setter
    def all_boundaries_np(self, new_val: namedtuple):
        self._all_boundaries_np = new_val

    @property
    def all_points(self) -> dict:
        return self._all_points

    @all_points.setter
    def all_points(self, new_val: dict):
        self._all_points = new_val

    @property
    def all_points_np(self) -> namedtuple:
        return self._all_points_np

    @all_points_np.setter
    def all_points_np(self, new_val: namedtuple):
        self._all_points_np = new_val

    @property
    def all_volumes(self) -> dict:
        return self._all_volumes

    @all_volumes.setter
    def all_volumes(self, new_val: dict):
        self._all_volumes = new_val

    @property
    def all_volumes_np(self) -> np.array:
        return self._all_volumes_np

    @all_volumes_np.setter
    def all_volumes_np(self, new_val: np.array):
        self._all_volumes_np = new_val

    @property
    def mesh_path(self) -> str:
        return self._mesh_path

    @mesh_path.setter
    def mesh_path(self, new_val: str):
        self._mesh_path = new_val

    @property
    def all_elements_count(self) -> int:
        return self._all_elements_count

    @all_elements_count.setter
    def all_elements_count(self, new_val: int):
        self._all_elements_count = new_val

    # @property
    # def mesh_parser(self) -> callable:
    #     return self._mesh_parser
    #
    # @mesh_parser.setter
    # def mesh_parser(self, new_val: callable):
    #     self._mesh_parser = new_val

    @property
    def volumes_count(self) -> int:
        return self._volumes_count

    @volumes_count.setter
    def volumes_count(self, new_val: int):
        self._volumes_count = new_val

    @property
    def volumes_info(self) -> dict:
        return self._volumes_info

    @volumes_info.setter
    def volumes_info(self, new_val: dict):
        self._volumes_info = new_val  # deepcopy(new_val)

    @property
    def boundaries_count(self) -> int:
        return self._boundaries_count

    @boundaries_count.setter
    def boundaries_count(self, new_val: int):
        self._boundaries_count = new_val

    @property
    def boundaries_info(self) -> dict:
        return self._boundaries_info

    @boundaries_info.setter
    def boundaries_info(self, new_val: dict):
        self._boundaries_info = new_val  # deepcopy(new_val)
        
    @property
    def points_count(self) -> int:
        return self._points_count
    
    @points_count.setter
    def points_count(self, new_val: int):
        self._points_count = new_val
        
    @property
    def tetra_count(self) -> int:
        return self._tetra_count
    
    @tetra_count.setter
    def tetra_count(self, new_val: int):
        self._tetra_count = new_val

    @property
    def penta_count(self) -> int:
        return self._penta_count

    @penta_count.setter
    def penta_count(self, new_val: int):
        self._penta_count = new_val
    
    @property
    def hexa_count(self) -> int:
        return self._hexa_count

    @hexa_count.setter
    def hexa_count(self, new_val: int):
        self._hexa_count = new_val
        
    @property
    def pyra_count(self) -> int:
        return self._pyra_count

    @pyra_count.setter
    def pyra_count(self, new_val: int):
        self._pyra_count = new_val

    @property
    def all_elements_count(self) -> int:
        return self._all_elements_count

    @all_elements_count.setter
    def all_elements_count(self, new_val: int):
        self._all_elements_count = new_val

    @property
    def ndim(self) -> int:
        return self._ndim

    @ndim.setter
    def ndim(self, new_val: int):
        self._ndim = new_val
        
    @property
    def all_tetras(self) -> np.array:
        return self._all_tetras
    
    @all_tetras.setter
    def all_tetras(self, new_val: np.array):
        self._all_tetras = new_val

    @property
    def all_pentas(self) -> np.array:
        return self._all_pentas

    @all_pentas.setter
    def all_pentas(self, new_val: np.array):
        self._all_pentas = new_val

    @property
    def all_hexas(self) -> np.array:
        return self._all_hexas

    @all_hexas.setter
    def all_hexas(self, new_val: np.array):
        self._all_hexas = new_val

    @property
    def all_pyras(self) -> np.array:
        return self._all_pyras

    @all_pyras.setter
    def all_pyras(self, new_val: np.array):
        self._all_pyras = new_val

    @property
    def curr_elements_count(self) -> int:
        return self._curr_elements_count

    @curr_elements_count.setter
    def curr_elements_count(self, new_val: int):
        self._curr_elements_count = new_val

    @property
    def all_points_w_els_np(self) -> np.array:
        return self._all_points_w_els_np

    @all_points_w_els_np.setter
    def all_points_w_els_np(self, new_val: np.array):
        self._all_points_w_els_np = new_val

    def __init__(self, mesh_path: str, ndim: int = 3, **kwargs):
        super(BasicMeshContainer, self).__init__(**kwargs)

        self.mesh_path = mesh_path
        self.ndim = ndim
        self.all_points = {}
        self.all_points_np = []  # np.empty(shape=(1, 4))
        # different type just for initialization shape
        self.all_points_w_els_np = []
        self.all_msh_elements = {}
        # should be deleted
        self.all_msh_elements_np = None

        self.all_tetras = []  # np.empty(shape=(1, 5))
        self.all_pentas = []  # np.empty(shape=(1, 7))
        self.all_hexas = []  # np.empty(shape=(1, 9))
        self.all_pyras = []  # np.empty(shape=(1, 6))
        self.curr_elements_count = 0
        # self.set_curr_elements_count()

        self.all_boundaries = {}
        self.all_boundaries_np = None
        self.all_volumes = {}
        self.all_volumes_np = []
        self.all_elements_count = 0
        self.volumes_count = 0
        self.volumes_info = {}
        self.boundaries_count = 0
        self.boundaries_info = {}
        self.points_count = 0
        self.tetra_count = 0
        self.penta_count = 0
        self.hexa_count = 0
        self.pyra_count = 0

    def set_curr_elements_count(self):
        """
        sets current element count using currently available elements
        collections
        Returns
        -------

        """

        self.curr_elements_count = \
            len(self.all_tetras) + len(self.all_pentas) + \
            len(self.all_hexas) + len(self.all_pyras)

    # @abstractmethod
    def get_des_nt_constr(
            self, des_count_attr_name: str,
            des_nt_class_name: str,
            nt_key_prfx: str) -> callable:
        """
        Getter method for desired namedtuple constructor
        Parameters
        ----------
        des_count_attr_name: str
            name of attribute holding count info
        des_nt_class_name: str
            name of the namedtuple callable created
        nt_key_prfx: str
            prefix for namedtuple keys

        Returns
        -------
        callable
            namedtuple callable

        """

        entries_count = getattr(self, des_count_attr_name)

        chck_entries_count = safe_to_int(entries_count)
        # print('{}_{}'.format(nt_key_prfx, str(0)))

        entries_names = \
            ['{}_{}'.format(nt_key_prfx, entry_id)
             for entry_id in range(1, int(chck_entries_count) + 1)]
        # print(entries_names)

        return namedtuple(des_nt_class_name, ' '.join(entries_names))

    @abstractmethod
    def get_all_points_nt_constr(self) -> callable:
        return None

    @abstractmethod
    def get_all_elements_nt_constr(self) -> callable:
        return None

    @abstractmethod
    def get_all_boundaries_nt_constr(self) -> callable:
        return None

    @abstractmethod
    def get_all_volumes_nt_constr(self) -> callable:
        return None

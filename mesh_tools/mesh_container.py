from collections import namedtuple
from numbers import Number
import numpy as np

from mesh_tools.element_containers import BasicElementContainer, \
    BasicMeshContainer, BasicElement
from helpers.helpers import get_vector_from_points, safe_to_int


class PointBucket:

    @property
    def point_count(self) -> int:
        return self._point_count

    @point_count.setter
    def point_count(self, new_val: int):
        self._point_count = new_val

    @property
    def point_attr_prfx(self) -> str:
        return self._point_attr_prfx

    @point_attr_prfx.setter
    def point_attr_prfx(self, new_val: str):
        self._point_attr_prfx = new_val

    def __init__(self, point_count: str or int, point_attr_prfx: str = 'point'):
        self.point_count = safe_to_int(point_count)
        self.point_attr_prfx = point_attr_prfx
        self._set_all_points_attrs()

    def _set_all_points_attrs(self):
        if not self.point_count:
            raise ValueError('`point_count` attribute must not be empty')

        for point_id in range(1, self.point_count + 1):
            setattr(self, '{}_{}'.format(self.point_attr_prfx, point_id),
                    Point(0, 0, 0, 0))


class Point:
    """
    Abstraction of 3D point in space
    """
    
    @property
    def x_coord(self) -> Number:
        return self._x_coord
    
    @x_coord.setter
    def x_coord(self, new_val: Number):
        self._x_coord = new_val

    @property
    def y_coord(self) -> Number:
        return self._y_coord

    @y_coord.setter
    def y_coord(self, new_val: Number):
        self._y_coord = new_val

    @property
    def z_coord(self) -> Number:
        return self._z_coord

    @z_coord.setter
    def z_coord(self, new_val: Number):
        self._z_coord = new_val

    @property
    def point_id(self) -> int:
        return self._point_id

    @point_id.setter
    def point_id(self, new_val: int):
        self._point_id = new_val
        
    def __init__(
            self, 
            x_coord: Number, y_coord: Number, z_coord: Number, point_id: int):
        """
        Init w params
        
        Parameters
        ----------
        x_coord: Number
            x coordinate of the point
        y_coord: Number
            y coordinate of the point
        z_coord: Number
            z coordinate of the point
        point_id: int
            int unique point id
        """
        
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.z_coord = z_coord
        self.point_id = point_id

    def get_coords(self) -> tuple:
        """
        getter method for point's coords
        Returns
        -------
        tuple
            tuple of coords <x, y, z>

        """
        return self.x_coord, self.y_coord, self.z_coord


class CFXElementWall:
    """
    Stores info about single element surface
    """

    @property
    def node_count(self) -> int:
        return self._node_count

    @node_count.setter
    def node_count(self, new_val: int):
        # TODO - check for max node count for CFD meshes and account for
        #  it in the setter
        self._node_count = new_val

    # @property
    # def surf_def(self) -> dict:
    #     return self._surf_def
    #
    # @surf_def.setter
    # def surf_def(self, new_val: dict):
    #     self._surf_def = deepcopy(new_val)

    @property
    def wall_id(self) -> int:
        return self._wall_id

    @wall_id.setter
    def wall_id(self, new_val: int):
        self._wall_id = new_val

    @property
    def wall_normal_v(self) -> dict:
        return self._wall_normal_v

    @wall_normal_v.setter
    def wall_normal_v(self, new_val: dict):
        self._wall_normal_v = new_val

    @property
    def wall_nodes_idxs(self) -> list:
        return self._wall_nodes_idxs

    @wall_nodes_idxs.setter
    def wall_nodes_idxs(self, new_val: list):
        self._wall_nodes_idxs = new_val

    @property
    def wall_nodes(self) -> list:
        return self._wall_nodes

    @wall_nodes.setter
    def wall_nodes(self, new_val: list):
        self._wall_nodes = new_val  # .copy()

    def __init__(
            self, wall_id: int,  wall_node_seq: list,  el_nodes: dict):

        self.wall_id = wall_id
        self.wall_nodes_idxs = wall_node_seq

        # print(el_nodes)

        self._set_wall_nodes(el_nodes)

        pass

    def _set_wall_nodes(self, el_nodes_dict):
        wall_nodes = []
        # print('el_nodes_dict')
        # print(el_nodes_dict)
        # print(self.wall_nodes_idxs)
        for wall_node_idx in self.wall_nodes_idxs:

            # des_point = el_nodes_dict[wall_node_idx]
            des_point_info = el_nodes_dict[wall_node_idx]
            des_point = des_point_info.get('node', None)
            if not des_point:
                raise ValueError(
                    '`des_point` not found in provided element nodes')
            wall_nodes.append(des_point)

        # TODO  uncomment for debug
        # print('wall nodes for {}'.format(self.wall_id))
        # print([wn.point_id for wn in wall_nodes])

        self.wall_nodes = wall_nodes

    def _set_wall_orient(self):
        first_wall_edge = self.wall_nodes[:2]
        second_wall_edge = self.wall_nodes[1:3]

        first_wall_vect = get_vector_from_points(first_wall_edge, Point)
        second_wall_vect = get_vector_from_points(second_wall_edge, Point)

        self.wall_normal_v = np.cross(
            np.array(first_wall_vect),
            np.array(second_wall_vect))


class CFXElement(BasicElement):
    # @property
    # def all_msh_points(self) -> dict:
    #     return self._all_msh_points
    #
    # @all_msh_points.setter
    # def all_msh_points(self, new_val: dict):
    #     self._all_msh_points = new_val

    @property
    def wall_count(self) -> int:
        return self._wall_count

    @wall_count.setter
    def wall_count(self, new_val: int):
        self._wall_count = new_val

    @property
    def node_count(self) -> int:
        return self._node_count

    @node_count.setter
    def node_count(self, new_val: int):
        self._node_count = new_val

    @property
    def nodes(self) -> dict:
        return self._nodes

    @nodes.setter
    def nodes(self, new_val: dict):
        self._nodes = new_val  # deepcopy(new_val)

    @property
    def walls(self) -> dict:
        return self._walls

    @walls.setter
    def walls(self, new_val: dict):
        self._walls = new_val  # deepcopy(new_val)

    @property
    def el_type_map(self) -> dict:
        return self._el_type_map

    @el_type_map.setter
    def el_type_map(self, new_val: dict):
        self._el_type_map = new_val  # deepcopy(new_val)

    @property
    def el_struct(self) -> dict:
        return self._el_struct

    @el_struct.setter
    def el_struct(self, new_val: dict):
        self._el_struct = new_val  # deepcopy(new_val)

    @property
    def el_nodes_ids(self) -> list:
        return self._el_nodes_ids

    @el_nodes_ids.setter
    def el_nodes_ids(self, new_val: list):
        self._el_nodes_ids = new_val  # new_val.copy()

    @property
    def global_el_id(self) -> int:
        return self._global_el_id

    @global_el_id.setter
    def global_el_id(self, new_val: int):
        self._global_el_id = new_val

    def __init__(
            self, el_nodes_ids: list,  all_msh_points: dict, el_type_map: dict,
            global_el_id: int):

        super(CFXElement, self).__init__()

        self.el_nodes_ids = el_nodes_ids
        # self.all_msh_points = all_msh_points
        # self.el_type_map = el_type_map
        self.global_el_id = global_el_id
        self._set_nodes(all_msh_points)
        # print(self.nodes)
        self._set_node_count()
        self._set_el_struct(el_type_map=el_type_map)
        self._set_walls()

    # def _set_el_type_struct(self):
    #
    #     cfx_el_type = len(self.el_nodes_ids)
    #     cfx_el_struct = self.el_type_map.get(cfx_el_type, {})
    #     if not cfx_el_struct:
    #         raise ValueError('Unknown element type - check element map for cfx')
    #
    #     pass

    def _set_nodes(self, all_msh_points: dict):

        nodes = {}

        # print(self.el_nodes_ids)

        for in_el_node_idx, node_el_id in enumerate(self.el_nodes_ids):
            curr_node = all_msh_points.get(node_el_id, None)
            if not curr_node:
                raise ValueError(
                    'Missing point from `all_msh_points`: {}'
                    .format(node_el_id))
            node_info = {
                'node': curr_node,
                'global_node_id': node_el_id}
            in_el_node_id = in_el_node_idx + 1
            nodes[in_el_node_id] = node_info
            # print('{} {} {} {}'.format(
            #     curr_node.point_id, curr_node.x_coord, curr_node.y_coord,
            #     curr_node.z_coord))
            # input('debug')

        # for node_id, node_def in nodes.items():
        #     curr_node = node_def.get('node')
            # print('{}: {} {} {}'.format(
            #     curr_node.point_id, curr_node.x_coord, curr_node.y_coord,
            #     curr_node.z_coord))

        self.nodes = nodes
        pass

    def _set_node_count(self):
        self.node_count = len(self.nodes)

    def _set_el_struct(self, el_type_map: dict):
        self.el_struct = el_type_map.get(self.node_count, {})
        if not self.el_struct:
            raise ValueError(
                'Empty element structure - this must not happen!!!')

    def _set_walls(self):
        walls_def = self.el_struct.get('walls_def', {})
        # print('walls_def')
        # print(walls_def)
        if not walls_def:
            raise ValueError(
                'Empty walls definition - this must not happen!!!')

        self.walls = {}
        for wall_idx, curr_wall_node_seq in walls_def.items():

            # print('curr_wall_node_seq')
            # print(curr_wall_node_seq)
            # print(self.nodes)

            curr_wall = \
                CFXElementWall(
                    wall_id=wall_idx,
                    wall_node_seq=curr_wall_node_seq,
                    el_nodes=self.nodes)

            self.walls[wall_idx] = curr_wall


class BoundarySurface(BasicElementContainer):
    # @property
    # def boundary_name(self) -> str:
    #     return self._boundary_name
    #
    # @boundary_name.setter
    # def boundary_name(self, new_val: str):
    #     self._boundary_name = new_val
    #
    # @property
    # def boundary_el_count(self) -> int:
    #     return self._boundary_el_count
    #
    # @boundary_el_count.setter
    # def boundary_el_count(self, new_val: int):
    #     self._boundary_el_count = new_val
    #
    # @property
    # def boundary_els(self) -> list:
    #     return self._boundary_els
    #
    # @boundary_els.setter
    # def boundary_els(self, new_val: list):
    #     self._boundary_els = new_val

    @property
    def boundary_elements_w_walls(self) -> dict:
        return self._boundary_elements_w_walls

    @boundary_elements_w_walls.setter
    def boundary_elements_w_walls(self, new_val: dict):
        self._boundary_elements_w_walls = new_val

    # @property
    # def all_elements(self) -> dict:
    #     return self._all_elements
    #
    # @all_elements.setter
    # def all_elements(self, new_val: dict):
    #     self._all_elements = deepcopy(new_val)

    def __init__(
            self,
            boundary_name: str,
            boundary_el_count: int,
            boundary_els_w_walls: tuple,
            all_msh_elements: dict):

        super(BoundarySurface, self).__init__(
            name=boundary_name, element_count=boundary_el_count,
            elements=[], all_msh_elements={})  # all_msh_elements)

        # self.boundary_name = boundary_name
        # self.boundary_el_count = boundary_el_count
        # self.all_elements = all_elements
        self._set_boundary_els_w_walls(
            boundary_els_w_walls=boundary_els_w_walls,
            all_msh_elements=all_msh_elements)

        pass

    def _iter_over_els_w_walls(
            self, els_w_walls: tuple, all_msh_elements: dict):
        """
        Generator for elements in given boundary elements set
        Parameters
        ----------
        els_w_walls: tuple
            tuple of tuples

        Yields
        -------
        CFXElement
            tuple: elementn_id, cfx element object, el_wall_id

        """
        for el_id, el_wall_id in els_w_walls:

            # print('## EL ID | EL WALL ID ##')
            # print('{} --> {}'.format(el_id, el_wall_id))
            # input('debug')

            # el_w_walls = {}
            curr_el = all_msh_elements.get(el_id, None)

            if not curr_el:
                raise ValueError(
                    'Element of id {} not found in `all_elements` param')
            yield el_id, curr_el, el_wall_id

    def _set_elements(self, boundary_els_w_walls, all_msh_elements: dict):
        """
        Setter using element info generator
        Parameters
        ----------
        boundary_els_w_walls: tuple
            tuple of tuples containing <el_id, wall_id> pair

        Returns
        -------

        """
        self.elements = []
        for _, el, _ in self._iter_over_els_w_walls(
                els_w_walls=boundary_els_w_walls,
                all_msh_elements=all_msh_elements):
            self.elements.append(el)

    # TODO get this done
    def _set_boundary_els_w_walls(
            self, boundary_els_w_walls: tuple, all_msh_elements: dict):

        self.boundary_elements_w_walls = {}

        for curr_el_id, curr_el, curr_el_wall_id in \
                self._iter_over_els_w_walls(
                    els_w_walls=boundary_els_w_walls,
                    all_msh_elements=all_msh_elements):

            el_w_walls = self.boundary_elements_w_walls.get(curr_el_id, {})

            # curr_bound_el = self.all_msh_elements.get(curr_el_id, None)
            #
            # if not curr_bound_el:
            #     raise ValueError(
            #         'Element of id {} not found in `all_elements` param')

            el_w_walls['element'] = curr_el
            el_w_walls[curr_el_wall_id] = curr_el.walls[curr_el_wall_id]

            self.boundary_elements_w_walls[curr_el_id] = el_w_walls


class FlowFieldVolume(BasicElementContainer):

    # @property
    # def all_elements(self) -> dict:
    #     return self._all_elements
    #
    # @all_elements.setter
    # def all_elements(self, new_val: dict):
    #     self._all_elements = deepcopy(new_val)
    #
    # @property
    # def volume_name(self) -> str:
    #     return self._volume_name
    #
    # @volume_name.setter
    # def volume_name(self, new_val: str):
    #     self._volume_name = new_val

    # TODO finish this up
    def __init__(
            self,
            volume_name: str,
            volume_el_count: int,
            volume_els_ids: list,
            all_msh_elements: dict):

        super(FlowFieldVolume, self).__init__(
            name=volume_name,
            element_count=volume_el_count,
            elements=[],
            all_msh_elements=all_msh_elements)

        # print('volume_els_ids')
        # print(volume_els_ids[:100])
        # print('all_msh_elements')
        # iter_idx = 0
        # for ex_el_id, ex_el in self.all_msh_elements.items():
        #     print('{} --> {}'.format(ex_el_id, ex_el))
        #     iter_idx += 1
        #     if iter_idx >= 100:
        #         break
        self._set_vol_elements(volume_els_ids=volume_els_ids)

    def _iter_over_volume_els(self, volume_els_ids: list):
        """
        Generator for iteration over volume's elements
        Parameters
        ----------
        volume_els_ids: list
            list of ids of volume's elements

        Returns
        -------

        """

        if not self.all_msh_elements:
            raise ValueError(
                '`all_msh_elements` must be filled before iterating over them '
                'for {} volume'.format(self.name))

        for el_id in volume_els_ids:
            curr_el = self.all_msh_elements.get(el_id, None)

            # print('curr_el')
            # print('{} ---> {}'.format(el_id, curr_el))
            # print('{} | {} # {} # {}'
            #       .format(
            #        el_id, curr_el.x_coord, curr_el.y_coord, curr_el.z_coord))

            if not curr_el:
                raise ValueError(
                    'Element of id {} not found in `all_elements` param'
                    .format(el_id))
            yield el_id, curr_el

    def _set_vol_elements(self, volume_els_ids: list):
        """
        Setter method fot all volume's elements
        Parameters
        ----------
        volume_els_ids: list
            list of elements' ids

        Returns
        -------

        """
        self.elements = []

        for _, curr_el in \
                self._iter_over_volume_els(volume_els_ids=volume_els_ids):
            self.elements.append(curr_el)


class CFX5MeshContainer(BasicMeshContainer):
    """
    Storage for mesh objects (i.e. during mesh conversion)
    """

    @property
    def boundary_surfs(self) -> dict:
        return self._boundary_surfs

    @boundary_surfs.setter
    def boundary_surfs(self, new_val: dict):
        self._boundary_surfs = new_val  # deepcopy(new_val)

    @property
    def flow_field_volumes(self) -> dict:
        return self._flow_field_volumes

    @flow_field_volumes.setter
    def flow_field_volumes(self, new_val: dict):
        self._flow_field_volumes = new_val  # deepcopy(new_val)

    @property
    def mesh_points(self) -> dict:
        return self._mesh_points

    @mesh_points.setter
    def mesh_points(self, new_val: dict):
        self._mesh_points = new_val

    @property
    def el_types(self) -> dict:
        return self._el_types

    @el_types.setter
    def el_types(self, new_val: dict):
        self._el_types = new_val  # deepcopy(new_val)

    @property
    def aoa_offset(self) -> float:
        return self._aoa_offset

    @aoa_offset.setter
    def aoa_offset(self, new_val: float):
        self._aoa_offset = new_val

    @property
    def aos_offset(self) -> float:
        return self._aos_offset

    @aos_offset.setter
    def aos_offset(self, new_val: float):
        self._aos_offset = new_val

    def __init__(
            self, mesh_path: str, ndim: int = 3, aoa_offset: float = 0,
            aos_offset: float = 0, **kwargs):
        super(CFX5MeshContainer, self)\
            .__init__(mesh_path=mesh_path, ndim=ndim, **kwargs)
        self.aoa_offset = aoa_offset
        self.aos_offset = aos_offset

    def get_all_points_nt_constr(self) -> callable:
        """
        Getter for namedtuple constructor representing container for all points

        Returns
        -------
        callable
            callable of namedtuple for all points

        """

        AllPoints = self.get_des_nt_constr('points_count', 'AllPoints', 'point')

        return AllPoints

    def get_all_elements_nt_constr(self) -> callable:
        """
        Getter for namedtuple constructor representing container for all
        elements

        Returns
        -------
        callable
            callable for namedtuple for all elements

        """
        AllElements = \
            self.get_des_nt_constr(
                'all_elements_count', 'AllElements', 'element')

        return AllElements

    def get_all_boundaries_nt_constr(self) -> callable:
        """
        Getter for namedtuple constructor representing container for all
        boundaries
        ,
        Returns
        -------
        callable

        """
        AllBoundaries = \
            self.get_des_nt_constr(
                'boundaries_count', 'AllBoundaries', 'boundary')

        return AllBoundaries

    def get_all_volumes_nt_constr(self) -> namedtuple:
        """
        Getter for namedtuple constructor representing container for all
        volumes

        Returns
        -------

        """
        AllVolumes= \
            self.get_des_nt_constr(
                'boundaries_count', 'AllVolumes', 'volume')

        return AllVolumes


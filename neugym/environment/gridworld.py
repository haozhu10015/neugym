import numpy as np
import networkx as nx
import copy
import warnings
from ._object import _Object


class GridWorld:
    def __init__(self, origin_shape=(1, 1)):
        self.world = nx.Graph()
        self.num_area = 0
        # Add origin
        if origin_shape == (1, 1):
            self.world.add_node((0, 0, 0))
        else:
            m, n = origin_shape
            origin = nx.grid_2d_graph(m, n)
            mapping = {}
            for key in origin.nodes:
                mapping[key] = tuple([0] + list(key))
            origin = nx.relabel_nodes(origin, mapping)
            self.world.update(origin)
        self.alias = {}
        self.objects = []
        self.actions = ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))

        # Agent information.
        self.have_agent = False
        self.time = None
        self.init_state = None
        self.current_state = None

    def add_area(self, shape, access_from=(0, 0, 0), access_to=(0, 0), register_action=None):
        if len(access_to) != 2:
            msg = "Tuple of length 2 expected for argument 'access_to', got {}".format(len(access_to))
            raise ValueError(msg)
        access_to = tuple([self.num_area + 1] + list(access_to))

        world_backup = copy.deepcopy(self.world)

        m, n = shape
        new_area = nx.grid_2d_graph(m, n)
        mapping = {}
        for key in new_area.nodes:
            mapping[key] = tuple([self.num_area + 1] + list(key))
        new_area = nx.relabel_nodes(new_area, mapping)

        self.world.update(new_area)

        try:
            self.add_path(access_from, access_to, register_action)
        except ValueError:
            self.world = world_backup
            raise
        self.num_area += 1

    def remove_area(self, area_idx):
        new_world = copy.deepcopy(self.world)
        if area_idx == 0:
            raise ValueError("Not allowed to remove origin area")

        # Remove area
        node_list = list(new_world.nodes)
        for node in node_list:
            if node[0] == area_idx:
                new_world.remove_node(node)
            elif node[0] > area_idx:
                new_label = tuple([node[0] - 1] + list(node[1:]))
                new_world = nx.relabel_nodes(new_world, {node: new_label})

        if not nx.is_connected(new_world):
            msg = "Not allowed to remove area {}, world is no longer connected".format(area_idx)
            raise RuntimeError(msg)

        self.world = new_world
        self.num_area -= 1

        # Remove invalid alias.
        new_alias = {}
        for key, value in self.alias.items():
            if key[0] == area_idx:
                continue
            elif key[0] > area_idx:
                new_key = tuple([key[0] - 1] + list(key[1:]))
            else:
                new_key = key

            if value[0] == area_idx:
                continue
            elif value[0] > area_idx:
                new_value = tuple([value[0] - 1] + list(value[1:]))
            else:
                new_value = value
            new_alias[new_key] = new_value

        self.alias = new_alias

        # Remove objects in the area to be removed.
        new_objects = []
        for i, obj in enumerate(self.objects):
            if obj.coord[0] < area_idx:
                new_objects.append(obj)
            elif obj.coord[0] == area_idx:
                continue
            else:
                obj.coord = tuple([obj.coord[0] - 1] + list(obj.coord[1:]))
                new_objects.append(obj)
        self.objects = new_objects

    def add_path(self, coord_from, coord_to, register_action=None):
        if len(coord_from) != 3:
            msg = "Tuple of length 3 expected for argument 'coord_from', got {}".format(len(coord_from))
            raise ValueError(msg)
        if not self.world.has_node(coord_from):
            msg = "'coord_from' coordinate {} out of world".format(coord_from)
            raise ValueError(msg)
        if self.world.degree(coord_from) == 4:
            msg = "Maximum number of connections (4) for position {} reached, not allowed to access from it".format(
                coord_from)
            raise ValueError(msg)

        if len(coord_to) != 3:
            msg = "Tuple of length 3 expected for argument 'coord_to', got {}".format(len(coord_to))
            raise ValueError(msg)
        if not self.world.has_node(coord_to):
            msg = "'coord_to' coordinate {} out of world".format(coord_to)
            raise ValueError(msg)
        elif self.world.degree(coord_to) == 4:
            msg = "Maximum number of connections (4) for position {} reached, not allowed to access to it".format(
                coord_to)
            raise ValueError(msg)

        if (coord_from, coord_to) in self.world.edges:
            msg = "Path already exists between {} and {}".format(coord_from, coord_to)
            raise ValueError(msg)

        free_actions = []
        for action in self.actions:
            dx, dy = action
            alias_to = tuple([coord_from[0]] + [coord_from[1] + dx] + [coord_from[2] + dy])
            alias_from = tuple([coord_to[0]] + [coord_to[1] - dx] + [coord_to[2] - dy])
            if self.world.has_node(alias_to) or self.world.has_node(alias_from) or \
                    alias_to in self.alias.keys() or alias_from in self.alias.keys():
                continue
            free_actions.append(action)

        if len(free_actions) == 0:
            msg = "Unable to connect two areas from 'coord_from' {} to 'coord_to' {}, " \
                  "all allowed actions allocated".format(coord_from, coord_to[1:])
            raise ValueError(msg)

        if register_action is not None:
            if register_action not in self.actions:
                msg = "Illegal 'register_action' {}, expected one of {}".format(register_action, self.actions)
                raise ValueError(msg)
            if register_action not in free_actions:
                msg = "Unable to register action 'register_action' {}, already allocated".format(register_action)
                raise ValueError(msg)
            dx, dy = register_action
        else:
            dx, dy = free_actions[0]

        self.alias[tuple([coord_from[0]] + [coord_from[1] + dx] + [coord_from[2] + dy])] = coord_to
        self.alias[tuple([coord_to[0]] + [coord_to[1] - dx] + [coord_to[2] - dy])] = coord_from
        self.world.add_edge(coord_from, coord_to)

    def remove_path(self, coord_from, coord_to):
        if len(coord_from) != 3 or len(coord_to) != 3:
            msg = "Tuple of length 3 expected for position coordinate"
            raise ValueError(msg)

        remove_list = []
        for action in self.actions:
            dx, dy = action
            alias_to = tuple([coord_from[0]] + [coord_from[1] + dx] + [coord_from[2] + dy])
            alias_from = tuple([coord_to[0]] + [coord_to[1] - dx] + [coord_to[2] - dy])

            if self.alias.get(alias_to) == coord_to and self.alias.get(alias_from) == coord_from:
                remove_list.append(alias_to)
                remove_list.append(alias_from)

        if len(remove_list) == 0:
            msg = "Inter-area path not found between {} and {}, noting to do".format(coord_from, coord_to)
            warnings.warn(msg)
        else:
            assert len(remove_list) == 2
            for key in remove_list:
                self.alias.pop(key)
            self.world.remove_edge(coord_from, coord_to)

    def set_path_attr(self):
        pass

    def add_object(self, coord, reward, prob, punish=0):
        if coord in self.world.nodes:
            self.objects.append(_Object(reward, punish, prob, coord))
        else:
            msg = "Coordinate {} out of world".format(coord)
            raise ValueError(msg)

    def remove_object(self, coord):
        pop_idx = None
        for i, obj in enumerate(self.objects):
            if coord == obj.coord:
                pop_idx = i
                break
        if pop_idx is not None:
            self.objects.pop(pop_idx)
        else:
            msg = "No object found at {}".format(coord)
            raise ValueError(msg)

    def update_object(self, coord, **kwargs):
        for obj in self.objects:
            if coord == obj.coord:
                for key, value in kwargs.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                    else:
                        msg = "'Object' object don't have attribute '{}', ignored.".format(key)
                        warnings.warn(msg)
                return

        msg = "No object found at {}".format(coord)
        raise ValueError(msg)

    def set_slope(self, area_idx, altitude_mat):
        pass

    def init_agent(self):
        pass

    def step(self):
        pass

    def reset(self):
        pass


class DelayedRewardGridWord(GridWorld):
    pass

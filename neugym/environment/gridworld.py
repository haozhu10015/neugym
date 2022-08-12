import numpy as np
import networkx as nx
import copy
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

        self.actions = ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))
        self.alias = {}
        self.objects = []

    def add_area(self, shape, access_from=(0, 0, 0), access_to=(0, 0), register_action=None):
        new_world = copy.deepcopy(self.world)

        m, n = shape
        new_area = nx.grid_2d_graph(m, n)
        mapping = {}
        for key in new_area.nodes:
            mapping[key] = tuple([self.num_area + 1] + list(key))
        new_area = nx.relabel_nodes(new_area, mapping)

        new_world.update(new_area)

        if len(access_from) != 3:
            msg = "Tuple of length 3 expected for argument 'access_from', got {}".format(len(access_from))
            raise ValueError(msg)
        if not new_world.has_node(access_from):
            msg = "'access_from' coordinate {} out of world".format(access_from)
            raise ValueError(msg)
        if new_world.degree(access_from) == 4:
            msg = "Maximum number of connections (4) for position {} reached, not allowed to access from it".format(
                access_from)
            raise ValueError(msg)

        access_to = tuple([self.num_area + 1] + list(access_to))
        if len(access_to) != 3:
            msg = "Tuple of length 2 expected for argument 'access_to', got {}".format(len(access_to) - 1)
            raise ValueError(msg)
        if not new_world.has_node(access_to):
            msg = "'access_to' coordinate {} out of world".format(access_to[1:])
            raise ValueError(msg)
        elif new_world.degree(access_to) == 4:
            msg = "Maximum number of connections (4) for position {} reached, not allowed to access to it".format(
                access_to[1:])
            raise ValueError(msg)

        free_actions = []
        for action in self.actions:
            dx, dy = action
            to_alias = tuple([access_from[0]] + [access_from[1] + dx] + [access_from[2] + dy])
            from_alias = tuple([access_to[0]] + [access_to[1] - dx] + [access_to[2] - dy])
            if new_world.has_node(to_alias) or new_world.has_node(from_alias) or \
                    to_alias in self.alias.keys() or from_alias in self.alias.keys():
                continue
            free_actions.append(action)

        if len(free_actions) == 0:
            msg = "Unable to connect two areas from 'access_from' {} to 'access_to' {}, " \
                  "all allowed actions allocated".format(access_from, access_to[1:])
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

        self.alias[tuple([access_from[0]] + [access_from[1] + dx] + [access_from[2] + dy])] = access_to
        self.alias[tuple([access_to[0]] + [access_to[1] - dx] + [access_to[2] - dy])] = access_from
        new_world.add_edge(access_from, access_to)
        self.world = new_world
        self.num_area += 1

    def remove_area(self, area_idx):
        if area_idx == 0:
            raise ValueError("Not allowed to remove origin area")

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

        # Remove area
        node_list = list(self.world.nodes)
        for node in node_list:
            if node[0] == area_idx:
                self.world.remove_node(node)
            elif node[0] > area_idx:
                new_label = tuple([node[0] - 1] + list(node[1:]))
                self.world = nx.relabel_nodes(self.world, {node: new_label})
        self.num_area -= 1

    def add_path(self):
        pass

    def remove_path(self):
        pass

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
                        msg = "'Object' object don't have attribute '{}'".format(key)
                        raise AttributeError(msg)
                return

        msg = "No object found at {}".format(coord)
        raise ValueError(msg)

    def set_slope(self, area_idx, altitude_mat):
        pass

import numpy as np
import networkx as nx
from ._object import _Object


class GridWorld:
    def __init__(self):
        self.world = nx.Graph()
        self.world.add_node((0, 0, 0))
        self.num_area = 0

        self.objects = []

    def add_area(self, shape, access_from=(0, 0, 0), access_to=(0, 0)):
        self.num_area += 1

        m, n = shape
        new_area = nx.grid_2d_graph(m, n)

        mapping = {}
        for key in new_area.nodes:
            mapping[key] = tuple([self.num_area] + list(key))
        new_area = nx.relabel_nodes(new_area, mapping)

        self.world.update(new_area)
        if len(access_from) != 3:
            msg = "Tuple of length 3 expected for argument 'access_from', got {}".format(len(access_from))
            raise ValueError(msg)
        if access_from not in self.world.nodes:
            msg = "'access_from' coordinate {} out of world".format(access_from)
            raise ValueError(msg)

        if len(access_to) != 2:
            msg = "Tuple of length 2 expected for argument 'access_to', got {}".format(len(access_to))
            raise ValueError(msg)
        if access_to[0] >= shape[0] or access_to[1] >= shape[1]:
            msg = "'access_to' coordinate {} out of world".format(access_to)
            raise ValueError(msg)

        self.world.add_edge(access_from, tuple([self.num_area] + list(access_to)))

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

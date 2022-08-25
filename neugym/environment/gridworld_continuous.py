import copy
import warnings

import networkx as nx
import numpy as np

import neugym as ng
from .gridworld import GridWorld
from ._object import _RewardPool


__all__ = [
    "GridWorldContinuous"
]


class GridWorldContinuous(GridWorld):
    def __init__(self):
        super(GridWorldContinuous, self).__init__()

    def add_reward_pool(self):
        pass

    def remove_reward_pool(self):
        pass

    def step(self, action):
        pass

    def __repr__(self):
        pass

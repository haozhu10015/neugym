import numpy as np


class _Object:
    def __init__(self, reward, punish, prob, coord):
        self.reward: float = reward
        self.punish: float = punish
        self.prob: float = prob
        self.coord: tuple = coord

    def get_reward(self):
        if np.random.uniform() < self.prob:
            return self.reward
        else:
            return self.punish

    def __repr__(self):
        return "Object(reward={}, punish={}, prob={}, coord={})".format(
            self.reward,
            self.punish,
            self.prob,
            self.coord
        )


class _RewardPool:
    def __init__(self, coord):
        self.coord: float = coord

    def __repr__(self):
        return "RewardPool(coord={})".format(self.coord)

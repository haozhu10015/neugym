class _Object:
    def __init__(self, reward, punish, prob, coord):
        self.reward: float = reward
        self.punish: float = punish
        self.prob: float = prob
        self.coord: tuple = coord

    def __repr__(self):
        return "Object(reward={}, punish={}, prob={}, coord={})".format(
            self.reward,
            self.punish,
            self.prob,
            self.coord
        )
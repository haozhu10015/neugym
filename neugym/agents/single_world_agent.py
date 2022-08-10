import numpy as np


class EpsilonGreedyAverager:
    def __init__(self, num_action, init=0):
        self.q = None
        if type(init) == int or type(init) == float:
            self.q = np.ones(num_action) * init
        elif init == 'randn':
            self.q = np.random.randn(num_action)
        else:
            raise ValueError("Unknown initialization parameter 'init'. Should be number or 'randn'.")

        self.num_action = num_action

    def get_action(self, greedy=0.1):
        if np.random.uniform() > greedy:
            return np.argmax(self.q)
        else:
            return np.random.choice(self.num_action)

    def learn(self, action, reward, lr=0.001):
        self.q[action] += lr * (reward - self.q[action])

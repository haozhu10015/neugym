import numpy as np


class Task:
    def forward(self):
        raise NotImplementedError

    def info(self):
        raise NotImplementedError


class Bandit(Task):
    def __init__(self,
                 success_reward,
                 success_prob,
                 fail_reward=0,
                 effort=0):
        self.success_reward = success_reward
        self.fail_reward = fail_reward

        self.init_success_prob = success_prob
        self.current_success_prob = success_prob

        self.effort = effort

    def forward(self):
        if np.random.uniform() < self.current_success_prob:
            return self.success_reward - self.effort
        else:
            return self.fail_reward - self.effort

    def update(self, **kwargs):
        try:
            self.current_success_prob = kwargs['success_prob']
        except KeyError:
            raise TypeError("Bandit.update() need keyword argument 'success_prob', but not provided.")

    def reset(self):
        self.current_success_prob = self.init_success_prob

    def info(self):
        pass

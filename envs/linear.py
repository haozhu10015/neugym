import numpy as np


class Bandit:
    def __init__(self,
                 num_arm,
                 reward_prob,
                 reward=1.0
                 ):
        """
        Multi-armed Bandit problem.

        Parameters
        ----------
        num_arm : int
            Number of arms.
        reward_prob : List
            List containing the probability of getting a reward after pulling each arm.
        reward : List or float, default: 1.0
            Reward for each arm.
            If a list is passed in, then it should have the same length as the number of arms.
            If a number is passed in, all arms will have the same reward equals to this value.
        """
        self.num_arm = num_arm
        if len(reward_prob) != num_arm:
            raise RuntimeError("Number of arms don't match number of reward probabilities given.")
        else:
            self.reward_prob = reward_prob

        if type(reward) == list or type(reward) == np.ndarray:
            if len(reward) != num_arm:
                raise RuntimeError("Number of arms don't match number of rewards given.")
            self.reward = reward
        elif type(reward) == float or type(reward) == int:
            self.reward = [float(reward) for _ in range(num_arm)]
        else:
            raise TypeError("Reward should be a List or float.")

    def step(self, action):
        """
        Pull the bandit.

        Parameters
        ----------
        action : int
            Index of arm to pull.

        Returns
        -------
        reward: float
            Reward after pulling the arm.

        """
        p = np.random.uniform()
        if p > self.reward_prob[action]:
            return self.reward[action]
        else:
            return 0

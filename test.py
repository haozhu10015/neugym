import neugym.environment.world as wd
import neugym.environment.task as tsk
from neugym.agent import EpsilonGreedyAverager


if __name__ == '__main__':
    world = wd.SimpleWorld()
    world.add_task(
        tsk.Bandit(1, 0.7),
        tsk.Bandit(1, 0.3)
    )

    agent = EpsilonGreedyAverager(num_action=len(world.actions), init=0.5)
    q_rec = []
    for e in range(10000):
        action = agent.get_action()
        reward = world.step(action)
        agent.learn(action=action, reward=reward, lr=0.01)

        if world.time % 1000 == 0:
            p_0 = world.objects["Tasks"][0].current_success_prob
            p_1 = world.objects["Tasks"][1].current_success_prob
            world.update_task(0, success_prob=p_1)
            world.update_task(1, success_prob=p_0)

        q_rec.append(agent.q.copy())

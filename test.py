import environment as env


if __name__ == '__main__':
    world = env.world.SimpleWorld()
    world.add_task(
        env.task.Bandit(1, 0.8),
        env.task.Bandit(1, 0.2)
    )
    world.update_task(0, success_prob=0.5)
    pass

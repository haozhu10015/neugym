import numpy as np


class World:
    def __init__(self):
        self.objects = {}
        self.actions = []
        self.time = 0

    def add_task(self):
        raise NotImplementedError

    def step(self, action):
        raise NotImplementedError

    def update_task(self, task_id):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def info(self):
        raise NotImplementedError


class SimpleWorld(World):
    def __init__(self):
        super(SimpleWorld, self).__init__()
        self.objects["Tasks"] = []

    def add_task(self, *args):
        for task in args:
            self.objects["Tasks"].append(task)
            self.actions.append(len(self.actions))

    def step(self, action):
        if action not in self.actions:
            raise ValueError("Action not in the action space.")

        self.time += 1
        return self.objects["Tasks"][action].forward()

    def update_task(self, task_id, **kwargs):
        try:
            self.objects["Tasks"][task_id].update(**kwargs)
        except AttributeError:
            raise AttributeError("'update' attribute not found. Task {} cannot be updated.".format(task_id))

    def reset(self):
        for task in self.objects["Tasks"]:
            try:
                task.reset()
            except AttributeError:
                continue
        self.time = 0

    def info(self):
        print("World Name: SimpleWorld")
        print("Tasks: {")
        for i, task in enumerate(self.objects["Tasks"]):
            info = task.get_info()
            print("Task {}: {}".format(i, info))
        print("}")
        print("Actions: {}".format(self.actions))


class GridWorld(World):
    def __init__(self):
        super(GridWorld, self).__init__()

    def add_task(self):
        pass

    def step(self, action):
        pass

    def update_task(self, task_id):
        pass

    def reset(self):
        pass

    def add_region(self):
        pass

    def info(self):
        pass

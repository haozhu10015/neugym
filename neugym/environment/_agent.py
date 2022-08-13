import warnings


class Agent:
    def __init__(self, init_state):
        self._time = 0
        self._init_state = init_state
        self._current_state = init_state

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == "time":
                self._time = value
            elif key == "init_state":
                if type(value) == tuple or len(value) == self._init_state:
                    self._init_state = value
                else:
                    msg = "Unable to update attribute 'init_state', unsupported type or length, ignored"
                    warnings.warn(msg)
            elif key == "current_state":
                if type(value) == tuple or len(value) == self._current_state:
                    self._current_state = value
                else:
                    msg = "Unable to update attribute 'current_state', unsupported type or length, ignored"
                    warnings.warn(msg)
            else:
                msg = "'Agent' object don't have attribute '{}', ignored.".format(key)
                warnings.warn(msg)

    def reset(self):
        self._time = 0
        self._current_state = self._init_state

    def time(self):
        return self._time

    def current_state(self):
        return self._current_state

    def __repr__(self):
        return "Agent(time={}, current_state={}, init_state={})".format(
            self._time,
            self._current_state,
            self._init_state
        )

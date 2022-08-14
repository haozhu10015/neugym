import pickle


__all__ = [
    "save_env",
    "load_env"
]


def save_env(env, file, protocol=pickle.HIGHEST_PROTOCOL):
    with open(file, 'wb') as f:
        pickle.dump(env, f, protocol=protocol)


def load_env(file):
    with open(file, 'rb') as f:
        return pickle.load(f)

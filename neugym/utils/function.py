import pickle
import networkx as nx


__all__ = [
    "save_env",
    "load_env",
    "show"
]


def save_env(env, filename, protocol=pickle.HIGHEST_PROTOCOL):
    """Save environment in Python pickle format.

    Parameters
    ----------
    env : environment object
        NeuGym environment object.

    filename : str
       Filename to write.
       Filenames ending in .gz or .bz2 will be compressed.
    protocol : integer
        Pickling protocol to use. Default value: ``pickle.HIGHEST_PROTOCOL``.

    Examples
    --------
    >>> W = GridWorld()
    >>> ng.save_env(W, "test.pkl")

    References
    ----------
    .. [#] https://docs.python.org/3/library/pickle.html

    """
    with open(filename, 'wb') as f:
        pickle.dump(env, f, protocol=protocol)


def load_env(filename):
    """Load environment in Python pickle format.

    Parameters
    ----------
    filename : str
        Filename to read.
        Filenames ending in .gz or .bz2 will be uncompressed.

    Returns
    -------
    W : environment object
        NeuGym environment object.

    Examples
    --------
    >>> W = GridWorld()
    >>> ng.save_env(W, "test.pkl")
    >>> W = ng.load_env("test.pkl")

    References
    ----------
    .. [*] https://docs.python.org/3/library/pickle.html

    """
    with open(filename, 'rb') as f:
        return pickle.load(f)


def show(env, layout='spring'):
    """Show environment area connections.

    Parameters
    ----------
    env : environment object
        NeuGym environment object.
    layout : str {"circular", "spring", "shell", "spectral"} (default: "circular")
        Layout with which to show the area connections.

    Examples
    --------
    >>> W = GridWorld()
    >>> W.add_area((1, 1))
    >>> W.add_area((1, 1), access_from=(1, 0, 0), register_action=(0, -1))
    >>> W.add_area((1, 1), access_from=(2, 0, 0), register_action=(-1, 0))
    >>> W.add_path((3, 0, 0), (0, 0, 0))
    >>> ng.show(W)
    """
    g = nx.Graph()

    labels = {}
    for area_idx in range(env.num_area + 1):
        try:
            alias = env.get_area_name(area_idx)
        except RuntimeError:
            alias = None

        g.add_node(area_idx)

        label = '{}\n({})'.format(area_idx, alias) if alias is not None else str(area_idx)
        labels[area_idx] = label

    for start, end in env.world.edges():
        if start[0] != end[0]:
            g.add_edge(start[0], end[0])

    if layout == 'circular':
        pos = nx.circular_layout(g)
    elif layout == 'spring':
        pos = nx.spring_layout(g)
    elif layout == 'shell':
        pos = nx.shell_layout(g)
    elif layout == 'spectral':
        pos = nx.spectral_layout(g)
    else:
        msg = "Invalid layout '{}', should be one of " \
              "['circular', 'spring', 'shell', 'spectral']".format(layout)
        raise ValueError(msg)

    nx.draw_networkx(g, pos=pos, labels=labels)

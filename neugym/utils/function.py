import pickle
import networkx as nx
import numpy as np


__all__ = [
    "save_env",
    "load_env",
    "show_area_connection",
    "show_area"
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


def show_area_connection(env, layout='spring'):
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
    >>> W.add_path((0, 0, 0), (1, 0, 0))
    >>> W.add_area((1, 1))
    >>> W.add_path((1, 0, 0), (2, 0, 0), register_action=(0, -1))
    >>> W.add_area((1, 1))
    >>> W.add_path((2, 0, 0), (3, 0, 0), register_action=(-1, 0))
    >>> W.add_path((3, 0, 0), (0, 0, 0))
    >>> ng.show_area_connection(W)
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


def show_area(env, area, show_altitude=False, figsize=None):
    """Show details for one area.

    Visualize altitude, objects, and blocks within one area.
    Grid color indicates state altitude.
    Blocked states will be marked with black cross.
    Objects are shown in red dots.

    Parameters
    ----------
    env : environment object
        NeuGym environment object.
    area : int or str
        Index or name of the area to show.
    show_altitude : bool (default: False)
        Whether to show state altitude value.
    figsize : tuple of ints (optional, default=None)
        Size of the figure.

    Examples
    -------
    >>> W = GridWorld()
    >>> W.add_area((3, 5), name='slope')
    >>> W.add_path((0, 0, 0), (1, 0, 0))
    >>> W.set_altitude(1, np.random.randn(3, 5))
    >>> W.block((1, 2, 4))
    >>> W.add_object((1, 2, 4), 0.5, 1)
    >>> W.add_object((1, 0, 3), 0.5, 1)
    >>> ng.show_area(W, 1, show_altitude=True)
    """

    import matplotlib.pyplot as plt

    if type(area) == str:
        area_idx = env.get_area_index(area)
    elif type(area) == int:
        area_idx = area
    else:
        msg = "int for area index or str for area name " \
              "expected, got '{}'".format(type(area))
        raise TypeError(msg)

    if area_idx > env.num_area or area_idx < 0:
        msg = "Area {} not found".format(area_idx)
        raise ValueError(msg)

    vmin = min(nx.get_node_attributes(env.world, "altitude").values())
    vmax = max(nx.get_node_attributes(env.world, "altitude").values())

    shape = env.get_area_shape(area_idx)
    fig, ax = plt.subplots(1, 1, figsize=figsize)

    title = "Area[{}]".format(area_idx)
    try:
        alias = env.get_area_name(area_idx)
    except RuntimeError:
        pass
    else:
        title += " ({})".format(alias)

    mat = env.get_area_altitude(area_idx)
    ax.matshow(mat, cmap='Blues',
               vmin=vmin, vmax=vmax)
    ax.set_title(title)

    for x in range(shape[0]):
        for y in range(shape[1]):
            coord = (area_idx, x, y)
            blocked = nx.get_node_attributes(env.world, 'blocked')[coord]
            if blocked:
                ax.scatter(y, x, s=500, color='k', marker='X')
            else:
                altitude = mat[x, y]
                if show_altitude:
                    ax.annotate("{}\n{}".format(
                                coord, np.around(altitude, decimals=2)),
                                (y, x),
                                horizontalalignment='center',
                                verticalalignment='bottom')
                else:
                    ax.annotate("{}".format(coord),
                                (y, x),
                                horizontalalignment='center',
                                verticalalignment='bottom')

            for action in env.actions:
                dx, dy = action
                alias = (area_idx, x + dx, y + dy)
                try:
                    next_state = env._path_alias[alias]
                except KeyError:
                    continue

                ax.plot((y, alias[2]), (x, alias[1]),
                        color='r', linewidth=3, linestyle=':')
                ax.annotate("{}".format(
                    next_state),
                    (alias[2], alias[1]),
                    horizontalalignment='center', verticalalignment='bottom')

    for obj in env._objects:
        a, x, y = obj.coord
        if a != area_idx:
            continue
        else:
            ax.scatter(y, x, s=500, color='r', alpha=0.5)

    ax.axis('off')
    plt.tight_layout()
    plt.show()

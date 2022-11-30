========
Tutorial
========

.. currentmodule:: neugym

This guide help you start working with NeuGym.
We will lead you to build a GridWorld environment
for potential reinforcement learning tasks.

Creating a world
================

Create a gridworld environment with only an one-state origin.
The origin area will be marked as Area[0] and automatically given a alias name "origin".

    >>> import neugym as ng
    >>> import neugym.environment as env

    >>> W = env.GridWorld()
    >>> print(W)
    GridWorld:
    ==========
    time: 0
    areas:
        [0][origin] Area(shape=(1, 1))
    inter-area connections: None
    objects: None
    actions: ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))
    agent: None
    has_reset_state: False
    ==========

Now the gridworld only has one state: ``(0, 0, 0)``. Every state in the gridworld is
represented by a tuple of length 3, where the first element denotes the
area index (index of the origin is 0, index for all other potential areas
will start from 1), and the two other elements are the state coordinate within the
area, respectively.

The world can be grown in several aspects.

Expanding the world
===================

Areas
-----

Areas in the gridworld are represented by a 2D grid network where each state connects
to its nearest 4 other states.

Add two areas of shape ``(2, 2)``.

    >>> W.add_area((2, 2))
    >>> W.add_area((2, 2))
    >>> print(W)
    GridWorld:
    ==========
    time: 0
    areas:
        [0][origin] Area(shape=(1, 1))
        [1][] Area(shape=(2, 2))
        [2][] Area(shape=(2, 2))
    inter-area connections: None
    objects: None
    actions: ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))
    agent: None
    has_reset_state: False
    ==========

You can specifying an alias name for an area when adding it.

    >>> W.add_area((2, 2), name="ThirdArea")
    >>> print(W)
    GridWorld:
    ==========
    time: 0
    areas:
        [0][origin] Area(shape=(1, 1))
        [1][] Area(shape=(2, 2))
        [2][] Area(shape=(2, 2))
        [3][ThirdArea] Area(shape=(2, 2))
    inter-area connections: None
    objects: None
    actions: ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))
    agent: None
    has_reset_state: False
    ==========

If you want to set or modify alias name for an exist area, you can use
``W.set_area_name`` function.

    >>> W.set_area_name(1, "FirstArea")
    >>> W.set_area_name(2, "SecondArea")
    >>> print(W)
    GridWorld:
    ==========
    time: 0
    areas:
        [0][origin] Area(shape=(1, 1))
        [1][FirstArea] Area(shape=(2, 2))
        [2][SecondArea] Area(shape=(2, 2))
        [3][ThirdArea] Area(shape=(2, 2))
    inter-area connections: None
    objects: None
    actions: ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))
    agent: None
    has_reset_state: False
    ==========

At any time, you can get the number of areas (without the origin) of the world with:

    >>> W.num_area
    3

To get the shape of an area, you can use:

    >>> W.get_area_shape(area=1)
    (2, 2)

Besides, the states and paths of the world are represented by a NetworkX ``Graph`` object.
You can get a copy of the ``Graph`` object by:

 >>> G = W.world

More information about NetworkX ``Graph`` object can be found at `NetworkX Documentation
<https://networkx.org/documentation/stable/reference/classes/graph.html>`_.

Objects
-------

In the gridworld, some states have ``objects`` aligned to them where the agent can get
a reward (or punishment) with a fixed probability. One state is allowed to have only
one object.

To add an object, you can use the ``W.add_object`` function, where you need to specify the
state coordinate to place the object for the first parameter:

    >>> W.add_object((1, 1, 1), reward=1, prob=0.7)
    >>> W.add_object((2, 0, 1), reward=1, prob=0.3, punish=-1)
    >>> print(W)
    GridWorld:
    ==========
    time: 0
    areas:
        [0][origin] Area(shape=(1, 1))
        [1][FirstArea] Area(shape=(2, 2))
        [2][SecondArea] Area(shape=(2, 2))
        [3][ThirdArea] Area(shape=(2, 2))
    inter-area connections: None
    objects:
        [0] Object(reward=1, punish=0, prob=0.7, coord=(1, 1, 1))
        [1] Object(reward=1, punish=-1, prob=0.3, coord=(2, 0, 1))
    actions: ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))
    agent: None
    has_reset_state: False
    ==========

Setting world details
=====================

Inter-area paths
----------------

When we add a new area to the world, it cannot be accessed from any of the
other existing areas since no inter-area path has been registered.
To make these dangling areas accessible, function ``W.add_path`` can help.

    >>> W.add_path(coord_from=(0, 0, 0), coord_to=(1, 0, 0))
    >>> W.add_path(coord_from=(0, 0, 0), coord_to=(2, 1, 1))
    >>> W.add_path(coord_from=(1, 0, 1), coord_to=(3, 1, 1))

You can also manually specify action to register for the inter-area path.

    >>> W.add_path(coord_from=(2, 0, 0), coord_to=(3, 1, 0),
    ...            register_action=(-1, 0))
    >>> print(W)
    GridWorld:
    ==========
    time: 0
    areas:
        [0][origin] Area(shape=(1, 1))
        [1][FirstArea] Area(shape=(2, 2))
        [2][SecondArea] Area(shape=(2, 2))
        [3][ThirdArea] Area(shape=(2, 2))
    inter-area connections:
        (0, 0, 0) + (1, 0) -> (1, 0, 0)
        (0, 0, 0) + (-1, 0) -> (2, 1, 1)
        (1, 0, 1) + (-1, 0) -> (3, 1, 1)
        (2, 0, 0) + (-1, 0) -> (3, 1, 0)
    objects:
        [0] Object(reward=1, punish=0, prob=0.7, coord=(1, 1, 1))
        [1] Object(reward=1, punish=-1, prob=0.3, coord=(2, 0, 1))
    actions: ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))
    agent: None
    has_reset_state: False
    ==========

    .. note::
        - Since gridworld only allow 5 actions: **STAY(0, 0)**, **UP(1, 0)**, **DOWN(-1, 0)**,
          **RIGHT(0, 1)**, and **LEFT(0, -1)**, each state can connect with at most 4 other
          states corresponding to these actions, i.e. the start and end state of the
          inter-area path can only be chosen from the states at the area margin.
        - The registered path should be reversible. E.g. when action **UP(1, 0)** will
          transport the agent from state ``(0, 0, 0)`` to state ``(1, 0, 0)``, then action
          **DOWN(-1, 0)** must be able to transport the agent from state ``(1, 0, 0)`` to
          state ``(0, 0, 0)``. When adding a new path, both two directions will be generated.
        - If the action to register is not manually set, then the first allowed path will be
          searched and set in the following order: **UP(1, 0)** -> **DOWN(-1, 0)** -> **RIGHT(0, 1)** ->
          **LEFT(0, -1)**.
        - Adding a path within the same area is not allowed.

State altitude
--------------

One of our idea for trying to make the gridworld more like the behavior chamber
used for real world experiments is that we can specify an ``altitude`` attribute to
every states, so that when the agent moves from one state to another, it would get a
reward from the difference between the state altitude:

.. math::
    R_{move} = A_s - A_{s + 1}

where $R_{move}$ is the movement reward and $A$
represents the altitude of current state $s$ and next state $s + 1$.

Instead of specifying the ``altitude`` per state, we use an altitude matrix to
set the altitude for all states in an area at the same time.

    >>> import numpy as np
    >>> np.random.seed(10015)
    >>> altitude_mat = np.random.randn(2, 2)
    >>> W.set_altitude(area=1, altitude_mat=altitude_mat)

    .. note::
        - The shape of ``altitude_mat`` should be the same as the shape of area with
          index ``area_idx``, so that the element ``[x, y]`` of the matrix will be
          set to be the altitude of state ``(area_idx, x, y)``.
        - By default, the altitude of all states will be set to ``0``.
        - If you call ``W.set_altitude`` multiple times for one area, the altitude
          of the states within will be overwritten.

You can have a look at the altitude of all states in an area with:

    >>> W.get_area_altitude(area=1)
    array([[-0.96776909,  0.35446728],
           [ 0.75243532,  1.42340557]])

Modifying the world
===================

Removing areas and paths
------------------------

If you for some reason want to remove a certain area or path from the world,
you can use ``W.remove_area`` and ``W.remove_path`` respectively.

For demonstration, we will first add a new area and an extra path.

    >>> W.add_area((5, 5))
    >>> W.add_path((3, 1, 1), (4, 0, 0))
    >>> print(W)
    GridWorld:
    ==========
    time: 0
    areas:
        [0][origin] Area(shape=(1, 1))
        [1][FirstArea] Area(shape=(2, 2))
        [2][SecondArea] Area(shape=(2, 2))
        [3][ThirdArea] Area(shape=(2, 2))
        [4][] Area(shape=(5, 5))
    inter-area connections:
        (0, 0, 0) + (1, 0) -> (1, 0, 0)
        (0, 0, 0) + (-1, 0) -> (2, 1, 1)
        (1, 0, 1) + (-1, 0) -> (3, 1, 1)
        (2, 0, 0) + (-1, 0) -> (3, 1, 0)
        (3, 1, 1) + (0, 1) -> (4, 0, 0)
    objects:
        [0] Object(reward=1, punish=0, prob=0.7, coord=(1, 1, 1))
        [1] Object(reward=1, punish=-1, prob=0.3, coord=(2, 0, 1))
    actions: ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))
    agent: None
    has_reset_state: False
    ==========

To remove the new-added area:

    >>> W.remove_area(area=4)

.. note::
    - Objects within one area will also be removed when removing the area.
    - Everytime when an area is removed, all indexes for other states (including
      objects within them) and areas remained will be checked and renamed to
      guarantee the index is still continuous.

Then we add the new area back again and generate a new path.

    >>> W.add_area((5, 5))
    >>> W.add_path((3, 1, 1), (4, 0, 0))
    >>> W.add_path(coord_from=(4, 4, 4), coord_to=(3, 1, 0))

To remove the new generated path but keep the area:

    >>> W.remove_path(coord_from=(4, 4, 4), coord_to=(3, 1, 0))
    >>> W.world.has_edge((4, 4, 4), (3, 1, 0))
    False

.. note::
    - When removing a path from ``coord_from`` to ``coord_to``, the reverse
      path from ``coord_to`` to ``coord_from`` will also be removed at the same time.

Removing and updating objects
-----------------------------

For this demonstration we will first add some new objects to ``Area[4]``.

    >>> W.add_object((4, 0, 0), reward=10, prob=0.5)
    >>> W.add_object((4, 1, 1), reward=100, prob=0.1)
    >>> print(W)
    GridWorld:
    ==========
    time: 0
    areas:
        [0][origin] Area(shape=(1, 1))
        [1][FirstArea] Area(shape=(2, 2))
        [2][SecondArea] Area(shape=(2, 2))
        [3][ThirdArea] Area(shape=(2, 2))
        [4][] Area(shape=(5, 5))
    inter-area connections:
        (0, 0, 0) + (1, 0) -> (1, 0, 0)
        (0, 0, 0) + (-1, 0) -> (2, 1, 1)
        (1, 0, 1) + (-1, 0) -> (3, 1, 1)
        (2, 0, 0) + (-1, 0) -> (3, 1, 0)
        (3, 1, 1) + (0, 1) -> (4, 0, 0)
    objects:
        [0] Object(reward=1, punish=0, prob=0.7, coord=(1, 1, 1))
        [1] Object(reward=1, punish=-1, prob=0.3, coord=(2, 0, 1))
        [2] Object(reward=10, punish=0, prob=0.5, coord=(4, 0, 0))
        [3] Object(reward=100, punish=0, prob=0.1, coord=(4, 1, 1))
    actions: ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))
    agent: None
    has_reset_state: False
    ==========

To remove an object, you can use the ``remove_object`` function and specifying the
coordinate of object to be removed:

    >>> W.remove_object((4, 0, 0))

To update the configuration of an object, you can use the ``update_object`` function.

    >>> W.update_object((4, 1, 1), reward=99, prob=0.9)
    >>> print(W)
    GridWorld:
    ==========
    time: 0
    areas:
        [0][origin] Area(shape=(1, 1))
        [1][FirstArea] Area(shape=(2, 2))
        [2][SecondArea] Area(shape=(2, 2))
        [3][ThirdArea] Area(shape=(2, 2))
        [4][] Area(shape=(5, 5))
    inter-area connections:
        (0, 0, 0) + (1, 0) -> (1, 0, 0)
        (0, 0, 0) + (-1, 0) -> (2, 1, 1)
        (1, 0, 1) + (-1, 0) -> (3, 1, 1)
        (2, 0, 0) + (-1, 0) -> (3, 1, 0)
        (3, 1, 1) + (0, 1) -> (4, 0, 0)
    objects:
        [0] Object(reward=1, punish=0, prob=0.7, coord=(1, 1, 1))
        [1] Object(reward=1, punish=-1, prob=0.3, coord=(2, 0, 1))
        [2] Object(reward=99, punish=0, prob=0.9, coord=(4, 1, 1))
    actions: ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))
    agent: None
    has_reset_state: False
    ==========

You can get the value of the object attribute by:

    >>> W.get_object_attribute((4, 1, 1), "reward")
    99

.. note::
    Except for the coordinate (``coord``) attribute of objects, all other three
    attributes (``reward``, ``punish``, ``prob``) can be updated. To do this just
    provide them as keyword argument and specify a new value.

Resetting the world
===================

You will need to first set a reset checkpoint to store the states for rolling back
the environment.

    >>> W.set_reset_checkpoint()
    >>> W.has_reset_checkpoint
    True

Then you can reset the gridworld environment any time you want with:

    >>> W.reset()

.. note::
    When resetting the environment, not only the configuration of areas, paths
    and objects but the state of the agent and environment time
    will be rolled back to the checkpoint.


Controlling an agent in the world
=================================

You can control an ``agent`` to freely move and explore the gridworld
environment. To do this, you will need to initialize an agent first.

.. note::

    Only one agent is allowed to exist in the gridworld.

Initializing an agent
---------------------

Gridworld attribute function ``init_agent`` has two parameters. The first one
``init_coord`` specifies the initial state coordinate where the agent will be placed
and it's also the "respawn point" when the agent finishes this trial. If this
parameter is not given, the initial state of the agent will be the origin of
the world ``(0, 0, 0)``.

    >>> W.init_agent(init_coord=(1, 0, 0))

It is also possible to modify the initial state after agent initialization by
setting the ``overwrite`` parameter to be ``True``.

    >>> W.init_agent(init_coord=(0, 0, 0), overwrite=True)

Exploring the world
-------------------

After initializing an agent in the world, we can control it to explore the
world with ``W.step(action)``. The action space of the environment can be
get with:

    >>> W.actions
    ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))

Each action indicates the change of state coordinate (``(dx, dy)``), and
every time a ``step`` function is called, the agent coordinate will first
be tried to change from ``(ara_idx, x, y)`` to ``(area_idx, x + dx, y + dy)``,
if the new coordinate is out of world, the existence of an inter-area path
will then be checked, and if there is, the agent will be transported to another
area. Otherwise the agent will be forced to stay in the same state as an action
**STAY(0, 0)** is performed.

As a result, the new state of the agent, reward of this step and
a marker indicating whether this trial is finished will be returned.

    >>> W.get_agent_state()
    (0, 0, 0)
    >>> W.step((1, 0))
    ((1, 0, 0), 2.155696549284321, False)
    >>> W.get_agent_state()
    (1, 0, 0)
    >>> W.step((0, 1))
    ((1, 0, 1), -1.3006420952687736, False)
    >>> W.get_agent_state()
    (1, 0, 1)

.. note::
    In gridworld, a trial is considered to be finished when the agent gets to a
    state with a object, and the agent will be transported to its initial state
    right after.

Every time ``W.step`` is called, the time of the environment will plus one which
indicates the total number of steps that the agent has moved, and you can get the
environment time with:

    >>> W.time
    2

Tutorial
========

.. currentmodule:: neugym

This guide help you start working with NeuGym.

Creating a world
----------------

Create a gridworld with only an one-state origin.

    >>> import neugym as ng
    >>> import neugym.environment as env

    >>> W = env.GridWorld()
    >>> print(W)
    GridWorld(
        time=0
        origin=Origin([0])(shape=(1, 1))
        areas=()
        objects=()
        actions=((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))
        agent=None
        has_reset_state=False
    )


Now the gridworld only has one state: (0, 0, 0). Every state in the gridworld will
be represented by a tuple of length 3, where the first element denotes the
area index (index of the origin is 0, index for all other potential areas
will start from 1), and the two other elements are the state coordinate within the
area, respectively.

The world can be grown in several aspects.

Adding areas, objects, and agent
--------------------------------

Areas
^^^^^

Add one area of shape (2, 2).

    >>> W.add_area((2, 2))
    GridWorld(
        time=0
        origin=Origin([0])(shape=(1, 1))
        areas=(
            [1] Area(shape=(2, 2))
        )
        objects=()
        actions=((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))
        agent=None
        has_reset_state=False
    )

By default, adding a new area like this will connect the (0, 0) state of the new area
with the gridworld origin (0, 0, 0). One can also manually specify the start and end state.

    >>> W.add_area((2, 2), access_from=(0, 0, 0), access_to=(1, 1))

It is even possible to further register a certain action for this path.

    >>> W.add_area((2, 2),
    ...            access_from=(0, 0, 0), access_to=(1, 1),
    ...            register_action=(-1, 0))

.. note::

    - When specifying the end state, only its coordinate within the new area need to be
      provided.
    - Since girdworld only allow 5 actions: STAY(0, 0), UP(1, 0), DOWN(-1, 0), RIGHT(0, 1),
      and LEFT(0, -1), each state can connect with at most 4 other states corresponding
      to these actions, i.e. the start and end state of the inter-area path can only
      be chosen from the states at the area margin.
    - The registered path should be reversible. E.g. when action UP(1, 0) will
      transport the agent from state (0, 0, 0) to state (1, 0, 0), then action
      DOWN(-1, 0) must be able to transport the agent from state (1, 0, 0) to state (0, 0, 0).
    - If the action to register is not manually set, then the first allowed path will be
      searched and set in the following order: UP(1, 0) -> DOWN(-1, 0) -> RIGHT(0, 1) ->
      LEFT(0, -1).

Objects
^^^^^^^

Agent
^^^^^

Adding details
--------------

More paths
^^^^^^^^^^

Altitude
^^^^^^^^

Modifying the world
-------------------

Removing Areas
^^^^^^^^^^^^^^

Removing Paths
^^^^^^^^^^^^^^

Removing and updating objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Resetting the world
------------------------

Setting checkpoint
^^^^^^^^^^^^^^^^^^

Resetting
^^^^^^^^^

Moving the agent in the world
-----------------------------


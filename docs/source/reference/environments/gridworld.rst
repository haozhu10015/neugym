.. _gridworld:

=========
GridWorld
=========

Overview
========

.. currentmodule:: neugym.environment.gridworld


.. autoclass:: GridWorld

Methods
=======

Configuring the environment
---------------------------

.. autosummary::
    :toctree: generated/

    GridWorld.__init__
    GridWorld.add_area
    GridWorld.remove_area
    GridWorld.add_path
    GridWorld.remove_path
    GridWorld.add_object
    GridWorld.remove_object
    GridWorld.update_object
    GridWorld.set_altitude
    GridWorld.init_agent
    GridWorld.set_reset_checkpoint
    GridWorld.reset

Get environment information
---------------------------

.. autosummary::
    :toctree: generated/

    GridWorld.world
    GridWorld.time
    GridWorld.num_area
    GridWorld.actions
    GridWorld.has_reset_checkpoint
    GridWorld.get_area_shape
    GridWorld.get_area_altitude
    GridWorld.get_object_attribute
    GridWorld.get_agent_state

Moving the agent
----------------

.. autosummary::
    :toctree: generated/

    GridWorld.step
.. _gridworld:

=========
GridWorld
=========

Overview
========

.. automodule:: neugym.environment.gridworld


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

    GridWorld.get_object_attribute
    GridWorld.get_area_shape
    GridWorld.get_area_altitude

Moving the agent
----------------

.. autosummary::
    :toctree: generated/

    GridWorld.step
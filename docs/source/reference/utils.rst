=========
Utilities
=========

.. automodule:: neugym.utils

Saving and loading environment
==============================

.. autosummary::
    :toctree: generated/

    save_env
    load_env

Drawing
=======

It is hard to provide a proper environment visualization
especially when the environment is large and
complex. The aim of these functions is to provide a convenient
and fast check of environment structure. For a more thorough and
beautiful visualization, people can use graph visualization tools
to show the state-level detailed environment structure. Notable
examples of dedicated and fully-featured graph visualization tools
are `Cytoscape <http://www.cytoscape.org/>`_,
`Gephi <https://gephi.org/>`_,
`Graphviz <http://www.graphviz.org/>`_.
To use these and other such tools, you can export the NetworkX
graph that represents the environment (``W.world``)
into a format that can be read by those tools.
More information can be found at
`Reading and writing graphs - NetworkX
<https://networkx.org/documentation/stable/reference/readwrite/index.html>`_.
People can also refers to the
`NetworkX <https://networkx.org/documentation/stable/reference/drawing.html>`_
built-in features for graph visualization.

.. autosummary::
    :toctree: generated/

    show_area_connection
    show_area
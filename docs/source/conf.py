import os
import sys
sys.path.insert(0, os.path.abspath("../.."))

import neugym as ng

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'NeuGym'
copyright = '2022, Hao Zhu'
author = 'Hao Zhu'
release = ng.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "numpydoc"
]

templates_path = ['_templates']
exclude_patterns = []
suppress_warnings = ["ref.citation", "ref.footnote"]

autosummary_generate = True
add_module_names = False
numpydoc_show_class_members = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_title = "NeuGym {} Documentation".format(release)

html_theme_options = {
    "collapse_navigation": True,
    "navigation_depth": 3,
    "show_prev_next": False
}

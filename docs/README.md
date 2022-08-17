# Building docs

Sphinx is used for generating the API and reference documentation.

## Instructions

After installing NeuGym and its dependencies, install the Python
packages needed to build the documentation by entering:

    pip install -r requirements_docs.txt

in the `docs/` directory.

To build the HTML documentation, enter:

    make html

in the `doc/` directory. This will generate a `build/html` subdirectory
containing the built documentation.

To build the PDF documentation, enter:

    make latexpdf

This will generate a `build/latex` subdirectory containing the PDF 
format built documentation.
You will need to have LaTeX installed for this.
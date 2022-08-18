=======
Install
=======

NeuGym is tested on Python 3.8, 3.9, and 3.10. If you do not already
have a Python environment configured on your computer, this instructions
for installing the full `scientific Python stack <https://scipy.org/install.html>`_
could be a good start.

Before installation, make sure you have the latest version of the Python
package manager ``pip`` installed. If it's not the case, you can refer to
the `Pip documentation <https://pip.pypa.io/en/stable/installation/>`_ and
install ``pip`` first.

Install the released version
============================

You can install the current release of NeuGym package on your computer
with ``pip`` by entering::

    $ pip install neugym

Alternatively, you can also manually download NeuGym source code from
`GitHub <https://github.com/HaoZhu10015/neugym/releases>`_ or
`PyPI <https://pypi.org/project/neugym/>`_.
To install one of these versions, unpack it and run the
following command from the top-level source directory using the terminal::

    $ pip install .

Install the development version
===============================

You will need `Git <https://git-scm.com/>`_ installed on your computer to install the development
version of NeuGym.

Before installing the development version, you may need to uninstall the
standard version of NeuGym using ``pip``::

    $ pip uninstall neugym

Then enter::

    $ git clone https://github.com/HaoZhu10015/neugym.git
    $ cd neugym
    $ pip install -e .

If you want to update NeuGym at any time, in the same directory do::

    $ git pull

Testing
=======

NeuGym uses the Python ``pytest`` testing package. More information
can be found at their `homepage <https://pytest.org>`_.

You can test the complete package from the unpacked source directory with::

    pytest neugym


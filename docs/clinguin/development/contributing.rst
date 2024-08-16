Contributing
============

To improve code quality, we use Nox to run linters, type checkers, unit tests,
documentation, and more. We recommend installing Nox using pipx to have it
available globally.

.. code-block:: console

    # Install
    python -m pip install pipx
    python -m pipx install nox

    # Run all sessions
    nox

    # List all sessions
    nox -l

    # Run an individual session
    nox -s session_name

    # Run an individual session (reuse install)
    nox -Rs session_name

Note that the Nox sessions create [editable] installs. In case there are issues,
try recreating environments by dropping the `-R` option. If your project is
incompatible with editable installs, adjust the `noxfile.py` to disable them.

Installing from Source
+++++++++++++++++++++++

The project is hosted on `GitHub <https://github.com/potassco/clinguin>`_ and can
also be installed from source. We recommend this only for development purposes.

.. note::
    The pip package `setuptools` must be installed beforehand.

Execute the following commands in the top-level Clinguin directory:

.. code-block:: console

    $ git clone https://github.com/potassco/clinguin
    $ cd clinguin
    $ pip install .[all]

